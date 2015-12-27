from base64 import urlsafe_b64encode
from hashlib import md5
from time import time
from six.moves.urllib.parse import urlparse, urlunparse, ParseResult

DEFAULT = object()


def generate_key(s):
    return urlsafe_b64encode(md5(s.encode('utf-8')).digest()).decode().rstrip('=')


class Signer(object):
    def __init__(self, key, timeout=DEFAULT, format='{key}{value}{expiration}'):
        self.key = key
        if timeout is DEFAULT:
            self.timeout = 60*60*24  # 24 hours
        else:
            self.timeout = timeout
        self.format = format

    def sign(self, *args, **kwargs):
        raise NotImplementedError


class Nginx(Signer):
    def get_expiration(self):
        if self.timeout is not None:
            return str(int(self.timeout+time()))
        return ''

    def signature(self, s):
        expiration = self.get_expiration()
        string = self.format.format(key=self.key, value=s, expiration=expiration)
        return generate_key(string), expiration


class UriSigner(Nginx):
    def sign(self, uri):
        sig, exp = self.signature(uri)

        parsed = urlparse(uri)

        query = parsed.query
        if query:
            query += '&'
        query += 'st=%s&e=%s' % (sig, exp)

        return urlunparse(ParseResult(
            parsed.scheme, parsed.netloc,
            parsed.path, parsed.params, query, parsed.fragment))


class UriQuerySigner(Nginx):
    def sign(self, key, value):
        sig, exp = self.signature(value)
        return '%s=%s&st=%s&e=%s' % (key, value, sig, exp)
