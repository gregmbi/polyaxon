# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from six.moves import urllib

from polyaxon_stores.clients import gc_client
from polyaxon_stores.exceptions import PolyaxonStoresException
from polyaxon_stores.logger import logger
from polyaxon_stores.utils import (
    append_basename,
    check_dirname_exists,
    get_files_in_current_directory
)


class GCSStore(object):
    def __init__(self, client=None, **kwargs):
        self._client = client
        self._project_id = kwargs.get('project_id')
        self._credentials = kwargs.get('credentials')
        self._key_path = kwargs.get('key_path')
        self._keyfile_dict = kwargs.get('keyfile_dict')
        self._scopes = kwargs.get('scopes')
        self._encoding = kwargs.get('encoding', 'utf-8')

    @property
    def client(self):
        if self._client is None:
            self.set_client(project_id=self._project_id,
                            key_path=self._key_path,
                            keyfile_dict=self._keyfile_dict,
                            scopes=self._scopes,
                            credentials=self._credentials)
        return self._client

    def set_client(self,
                   project_id=None,
                   key_path=None,
                   keyfile_dict=None,
                   credentials=None,
                   scopes=None):
        """
        Sets a new gc client.

        :param project_id: The project if.
        :type project_id: str
        :param key_path: The path to the json key file.
        :type key_path: str
        :param keyfile_dict: The dict containing the auth data.
        :type keyfile_dict: str | dict
        :param credentials: The credentials to use.
        :type credentials: Credentials instance
        :param scopes: The scopes.
        :type scopes: list

        :return: Service client instance
        """
        self._client = gc_client.get_gc_client(
            project_id=project_id,
            key_path=key_path,
            keyfile_dict=keyfile_dict,
            credentials=credentials,
            scopes=scopes,
        )

    @staticmethod
    def parse_gcs_url(gcs_url):
        """
        Parses and validates a google cloud storage url.

        :return: tuple(bucket_name, blob).
        """
        parsed_url = urllib.parse.urlparse(gcs_url)
        if not parsed_url.netloc:
            raise PolyaxonStoresException('Received an invalid url `{}`'.format(gcs_url))
        if parsed_url.scheme != 'gs':
            raise PolyaxonStoresException('Received an invalid url `{}`'.format(gcs_url))
        blob = parsed_url.path.lstrip('/')
        return parsed_url.netloc, blob

    def get_bucket(self, bucket_name):
        """
        Gets a bucket by name.

        :param bucket_name: Name of the bucket
        :type bucket_name: str
        """
        return self.client.get_bucket(bucket_name)

    def delete(self, key, bucket_name=None):
        if not bucket_name:
            bucket_name, key = self.parse_gcs_url(key)
        bucket = self.get_bucket(bucket_name)
        bucket.delete_blob(key)

    def check_blob(self, blob, bucket_name=None):
        """
        Checks for the existence of a file in Google Cloud Storage.

        :param blob: the path to the object to check in the Google cloud storage bucket.
        :type blob: string
        :param bucket_name: Name of the bucket in which the file is stored
        :type bucket_name: str
        """
        if not bucket_name:
            bucket_name, blob = self.parse_gcs_url(blob)
        try:
            self.client.objects().get(bucket=bucket_name, object=blob).execute()
            return True
        except Exception as e:
            logger.info('Block does not exist %s', e)
            return False

    def get_blob(self, blob, bucket_name=None):
        """
        Get a file in Google Cloud Storage.

        :param blob: the path to the object to check in the Google cloud storage bucket.
        :type blob: string
        :param bucket_name: Name of the bucket in which the file is stored
        :type bucket_name: str
        """
        if not bucket_name:
            bucket_name, blob = self.parse_gcs_url(blob)

        bucket = self.get_bucket(bucket_name)
        # Wrap google.cloud.storage's blob to raise if the file doesn't exist
        obj = bucket.get_blob(blob)

        if obj is None:
            raise PolyaxonStoresException('File does not exist: {}'.format(blob))

        return obj

    def list(self, key, bucket_name=None, path=None, delimiter='/', blobs=True, prefixes=True):
        """
        List prefixes and blobs in a bucket.

        :param key: a key prefix.
        :type key: str
        :param bucket_name: the name of the bucket.
        :type bucket_name: str
        :param path: an extra path to append to the key.
        :type path: str
        :param delimiter: the delimiter marks key hierarchy.
        :type delimiter: str
        :param blobs: if it should include blobs.
        :type blobs: bool
        :param prefixes: if it should include prefixes.
        :type prefixes: bool

        :return: Service client instance
        """
        if not bucket_name:
            bucket_name, key = self.parse_gcs_url(key)

        bucket = self.get_bucket(bucket_name)

        if key and not key.endswith('/'):
            key += '/'

        prefix = key
        if path:
            prefix = os.path.join(prefix, path)

        if prefix and not prefix.endswith('/'):
            prefix += '/'

        iterator = bucket.list_blobs(prefix=prefix, delimiter=delimiter)

        def get_blobs(_blobs):
            list_blobs = []
            for blob in _blobs:
                name = blob.name[len(key) + 1:]
                list_blobs.append((name, blob.size))
            return list_blobs

        def get_prefixes(_prefixes):
            list_prefixes = []
            for folder_path in _prefixes:
                name = folder_path[len(key) + 1: -1]
                list_prefixes.append(name)
            return list_prefixes

        results = {
            'blobs': [],
            'prefixes': []
        }

        if blobs:
            results['blobs'] = get_blobs(list(iterator))

        if prefixes:
            for page in iterator.pages:
                results['prefixes'] = get_prefixes(page.prefixes)

        return results

    def upload_file(self, filename, blob, bucket_name=None, use_basename=True):
        """
        Uploads a local file to Google Cloud Storage.

        :param filename: the file to upload.
        :type filename: str
        :param blob: blob to upload to.
        :type blob: str
        :param bucket_name: the name of the bucket.
        :type bucket_name: str
        :param use_basename: whether or not to use the basename of the filename.
        :type use_basename: bool
        """
        if not bucket_name:
            bucket_name, blob = self.parse_gcs_url(blob)

        if use_basename:
            blob = append_basename(blob, filename)

        obj = self.get_blob(blob, bucket_name)
        obj.upload_from_filename(filename)

    def download_file(self, blob, local_path, bucket_name=None, use_basename=True):
        """
        Downloads a file from Google Cloud Storage.

        :param blob: blob to download.
        :type blob: str
        :param local_path: the path to download to.
        :type local_path: str
        :param bucket_name: the name of the bucket.
        :type bucket_name: str
        :param use_basename: whether or not to use the basename of the blob.
        :type use_basename: bool
        """
        if not bucket_name:
            bucket_name, blob = self.parse_gcs_url(blob)

        if use_basename:
            local_path = append_basename(local_path, blob)

        check_dirname_exists(local_path)

        blob = self.get_blob(blob=blob, bucket_name=bucket_name)
        blob.download_to_filename(local_path)

    def upload_files(self, dirname, blob, bucket_name=None, use_basename=True):
        """
        Uploads a local directory to to Google Cloud Storage.

        :param dirname: name of the directory to upload.
        :type dirname: str
        :param blob: blob to upload to.
        :type blob: str
        :param bucket_name: the name of the bucket.
        :type bucket_name: str
        :param use_basename: whether or not to use the basename of the directory.
        :type use_basename: bool
        """
        if not bucket_name:
            bucket_name, blob = self.parse_gcs_url(blob)

        if use_basename:
            blob = append_basename(blob, dirname)

        # Turn the path to absolute paths
        dirname = os.path.abspath(dirname)
        with get_files_in_current_directory(dirname) as files:
            for f in files:
                file_blob = os.path.join(blob, os.path.relpath(f, dirname))
                self.upload_file(filename=f,
                                 blob=file_blob,
                                 bucket_name=bucket_name,
                                 use_basename=False)

    def download_files(self, blob, local_path, bucket_name=None, use_basename=True):
        """
        Download a directory from Google Cloud Storage.

        :param blob: blob to download.
        :type blob: str
        :param local_path: the path to download to.
        :type local_path: str
        :param bucket_name: Name of the bucket in which to store the file.
        :type bucket_name: str
        :param use_basename: whether or not to use the basename of the key.
        :type use_basename: bool
        """
        if not bucket_name:
            bucket_name, blob = self.parse_gcs_url(blob)

        if use_basename:
            local_path = append_basename(local_path, blob)

        try:
            check_dirname_exists(local_path, is_dir=True)
        except PolyaxonStoresException:
            os.mkdir(local_path)

        results = self.list(bucket_name=bucket_name, key=blob, delimiter='/')

        # Create directories
        for prefix in sorted(results['prefixes']):
            direname = os.path.join(local_path, prefix)
            prefix = os.path.join(blob, prefix)
            # Download files under
            self.download_files(blob=prefix,
                                local_path=direname,
                                bucket_name=bucket_name,
                                use_basename=False)

        # Download files
        for file_key in results['blobs']:
            file_key = file_key[0]
            filename = os.path.join(local_path, file_key)
            file_key = os.path.join(blob, file_key)
            self.download_file(blob=file_key,
                               local_path=filename,
                               bucket_name=bucket_name,
                               use_basename=False)
