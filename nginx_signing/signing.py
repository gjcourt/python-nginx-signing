from base64 import urlsafe_b64encode
from hashlib import md5
from time import time
from urlparse import urlparse, urlunparse, ParseResult


class Signer(object):
    def __init__(self, key, timeout=None):
        self.key = key
        self.timeout = timeout or 60*60*24  # 24 hours

    def sign(self, *args, **kwargs):
        raise NotImplementedError


class Nginx(Signer):
    def encode(self, s):
        return urlsafe_b64encode(s).replace('=', '')

    def to_hash(self, value):
        return md5(value).digest()

    def get_expiration(self):
        return str(int(self.timeout+time()))

    def signature(self, s):
        expiration = self.get_expiration()
        string = self.key + s + expiration
        return self.encode(self.to_hash(string)), expiration


class UriSigner(Nginx):
    def sign(self, uri):
        sig, exp = self.signature(uri)

        parsed = urlparse(uri)

        query = parsed.query
        if query:
            query += '&'
        query += 'st=%s&e=%s' % (sig, exp)

        return urlunparse(ParseResult(parsed.scheme, parsed.netloc,
            parsed.path, parsed.params, query, parsed.fragment))


class UriQuerySigner(Nginx):
    def sign(self, key, value):
        sig, exp = self.signature(value)
        return '%s=%s&st=%s&e=%s' % (key, value, sig, exp)

