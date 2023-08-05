from contextlib import contextmanager
import io
import json
import logging
import math
import os
import time

from clint.textui import progress
import requests

from modelforge.progress_bar import progress_bar
from modelforge.storage_backend import StorageBackend, TransactionRequiredError

INDEX_FILE = "index.json"  #: Models repository index file name.


class Tracker:
    """
    Wrapper around a bytes buffer which follows the file position and updates
    the console progressbar mimicking a file object.
    """
    def __init__(self, data, logger):
        self._file = io.BytesIO(data)
        self._size = len(data)
        self._enabled = logger.isEnabledFor(logging.INFO)
        if self._enabled:
            self._progress = progress.Bar(expected_size=self._size)
        else:
            logger.debug("Progress indication is not enabled")

    def read(self, size=None):
        pos_before = self._file.tell()
        result = self._file.read(size)
        if self._enabled:
            pos = self._file.tell()
            if pos != pos_before:
                if pos < self._size:
                    self._progress.show(pos)
                else:
                    self._progress.done()
        return result

    def __len__(self):
        return self._size


class GCSBackend(StorageBackend):
    NAME = "gcs"
    DEFAULT_CHUNK_SIZE = 65536
    INDEX_FILE = "index.json"

    def __init__(self, bucket: str, credentials: str="", log_level: int=logging.DEBUG):
        """
        Initializes a new instance of :class:`GCSBackend`.

        :param bucket: The name of the Google Cloud Storage bucket to use.
        :param log_level: The logging level of this instance.
        """
        super().__init__()
        if not isinstance(bucket, str):
            raise TypeError("bucket must be a str")
        self._bucket_name = bucket
        if not isinstance(credentials, str):
            raise TypeError("credentials must be a str")
        self._credentials = credentials
        self._log = logging.getLogger("gcs-backend")
        self._log.setLevel(log_level)
        self._bucket = None

    @property
    def bucket_name(self):
        return self._bucket_name

    @property
    def credentials(self):
        return self._credentials

    def fetch_model(self, source: str, file: str) -> None:
        self._fetch(source, file)

    def fetch_index(self) -> dict:
        buffer = io.BytesIO()
        self._fetch("https://storage.googleapis.com/%s/%s?ignoreCache=1" %
                    (self.bucket_name, self.INDEX_FILE),
                    buffer)
        return json.loads(buffer.getvalue().decode("utf8"))

    @contextmanager
    def lock(self):
        """
        This is the best we can do. It is impossible to acquire the lock reliably without
        using any additional services. test-and-set is impossible to implement.
        :return:
        """
        log = self._log
        log.info("Locking the bucket...")

        # Client should be imported here because grpc starts threads during import
        # and if you call fork after that, a child process will be hang during exit
        from google.cloud.storage import Client

        if self.credentials:
            client = Client.from_service_account_json(self.credentials)
        else:
            client = Client()
        bucket = client.get_bucket(self.bucket_name)
        self._bucket = bucket
        sentinel = bucket.blob("index.lock")
        try:
            while sentinel.exists():
                log.warning("Failed to acquire the lock, waiting...")
                time.sleep(1)
            sentinel.upload_from_string(b"")
            # Several agents can get here. No test-and-set, sorry!
            yield None
        finally:
            self._bucket = None
            if sentinel is not None:
                try:
                    sentinel.delete()
                except:
                    pass

    def upload_model(self, path, meta, force):
        bucket = self._bucket
        if bucket is None:
            raise TransactionRequiredError
        blob = bucket.blob("models/%s/%s.asdf" % (meta["model"], meta["uuid"]))
        if blob.exists() and not force:
            self._log.error("Model %s already exists, aborted.", meta["uuid"])
            return 1
        self._log.info("Uploading %s from %s...", meta["model"], os.path.abspath(path))

        def tracker(data):
            return Tracker(data, self._log)

        make_transport = blob._make_transport

        def make_transport_with_progress(client):
            transport = make_transport(client)
            request = transport.request

            def request_with_progress(method, url, data=None, headers=None, **kwargs):
                return request(method, url, data=tracker(data), headers=headers, **kwargs)

            transport.request = request_with_progress
            return transport

        blob._make_transport = make_transport_with_progress

        with open(path, "rb") as fin:
            blob.upload_from_file(fin, content_type="application/x-yaml")
        blob.make_public()
        return blob.public_url

    def upload_index(self, index):
        bucket = self._bucket
        if bucket is None:
            raise TransactionRequiredError
        blob = bucket.blob(self.INDEX_FILE)
        blob.cache_control = "no-cache"
        blob.upload_from_string(json.dumps(index, indent=4, sort_keys=True))
        blob.make_public()

    def _fetch(self, url, where, chunk_size=DEFAULT_CHUNK_SIZE):
        self._log.info("Fetching %s...", url)
        r = requests.get(url, stream=True)
        if isinstance(where, str):
            os.makedirs(os.path.dirname(where), exist_ok=True)
            f = open(where, "wb")
        else:
            f = where
        try:
            total_length = int(r.headers.get("content-length"))
            num_chunks = math.ceil(total_length / chunk_size)
            if num_chunks == 1:
                f.write(r.content)
            else:
                for chunk in progress_bar(
                        r.iter_content(chunk_size=chunk_size),
                        self._log, expected_size=num_chunks):
                    if chunk:
                        f.write(chunk)
        finally:
            if isinstance(where, str):
                f.close()
