# -*- coding: utf-8 -*-

from urlparse import urljoin, parse_qs
from random import choice
import urllib

from qiniu import Auth
from qiniu import BucketManager
from qiniu import put_data
from qiniu import urlsafe_base64_encode


class Qiniu(object):

    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):

        self.access_key = self.app.config['QINIU_ACCESS_KEY']
        self.secret_key = self.app.config['QINIU_SECRET_KEY']
        self.bucket_name = self.app.config['QINIU_BUCKET']
        self.bucket_alias = self.app.config.get('QINIU_BUCKET_ALIAS', None)
        self.base_url = self.app.config.get('QINIU_BASIC_URL', None)
        self.custom_urls = self.app.config.get('QINIU_CUSTOM_URLS', None)
        self.custom_scheme = self.app.config.get('QINIU_CUSTOM_SCHEME', 'http')

        self.q = Auth(self.access_key, self.secret_key)
        self.bucket = BucketManager(self.q)

    def _get_bucket_name(self, bucket):
        if not self.bucket_alias or not bucket:
            return self.bucket_name
        bucket_name = self.bucket_alias.get(bucket)
        if not bucket_name:
            return self.bucket_name
        return bucket_name

    def cdn_url(self):
        domain = self.base_url or choice(self.custom_urls)
        return '%s://%s/' % (self.custom_scheme, domain)

    def upload_token(self, policy=None, bucket=None):
        bucket_name = self._get_bucket_name(bucket)
        return self.q.upload_token(bucket_name, policy=policy)

    def verify_callback(self, origin_authorization, url, body, content_type='application/x-www-form-urlencoded'):
        return self.q.verify_callback(origin_authorization, url, body, content_type)

    def upload_token_with_callback(self, callback_url, custom_keys):
        """ Return a upload_token string with policy

        :param callback_url: String of callback url
        :param custom_keys: Array of callback body key
        """

        body_dict = {}
        for key in custom_keys:
            body_dict[key] = '$(x:{})'.format(key)
        body = urllib.urlencode(body_dict)
        body = urllib.unquote(body)
        return self.upload_token(
                policy=dict(callbackUrl=callback_url, callbackBody=body)
        )

    def public_url(self, key, suffix=None):
        if not key or key.startswith(('http:', 'https:')):
            return key

        if suffix:
            key += suffix

        return urljoin(self.cdn_url(), key)

    def private_url(self, key, suffix=None):
        if not key or key.startswith(('http:', 'https:')):
            return key

        if suffix:
            key += suffix

        url = urljoin(self.cdn_url(), key)
        return self.q.private_download_url(url)

    def upload_stream(self, file_stream, key, policy=None):
        uptoken = self.upload_token(policy=None)
        ret, info = put_data(uptoken, key, file_stream)
        if ret is None:
            raise UploadError(info)

    def fetch_url(self, file_url, key, bucket=None):
        bucket_name = self._get_bucket_name(bucket)
        ret, info = self.bucket.fetch(file_url, bucket_name, key)
        if ret is None:
            raise FetchError(info)

    def fetch_urls(self, file_urls, keys, retry=2):
        for file_url, key in zip(file_urls, keys):
            # print file_url, key
            for attempt in range(1, retry+1):
                try:
                    self.fetch_url(file_url, key)
                except FetchError:
                    # raise for the last trial
                    if attempt == retry:
                        raise
                    else:
                        continue
                # run without error break from attempt
                break

    def encode_key(self, key, bucket=None):
        # encode custom key and bucket to base64
        # http://developer.qiniu.com/article/developer/format.html#encodentry
        bucket_name = self._get_bucket_name(bucket)
        return urlsafe_base64_encode(bucket_name + ':' + key)


class UploadError(Exception):
    pass


class FetchError(Exception):
    pass
