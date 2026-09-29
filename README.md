Python Nginx Signing
====================

A small library for generating the `st`/`e` signature and expiration
parameters expected by nginx's [Secure Link](http://wiki.nginx.org/HttpSecureLinkModule)
module, so requests can be signed on the Python side without reimplementing
nginx's MD5/base64 scheme by hand.

This targets Python 2: `nginx_signing/signing.py` imports the standalone
`urlparse` module, which no longer exists in Python 3.

Installation
------------

    pip install nginx_signing

Uri Example
-----------

`UriSigner` signs an entire URI, matching the ["Example usage"](http://wiki.nginx.org/HttpSecureLinkModule#Example_usage:)
section of the nginx docs. It appends `st` and `e` to the URI's query
string:

    >>> from nginx_signing.signing import UriSigner
    >>> signer = UriSigner(SECRET_KEY)
    >>> signer.sign('http://gjcourt.com')
    'http://gjcourt.com?st=uDqsQqA_ysTYR_bUdMUAGw&e=1365903669'

Query String Example
--------------------

`UriQuerySigner` signs a single value instead of a whole URI, for when
only one query string argument needs to be protected:

    >>> from nginx_signing.signing import UriQuerySigner
    >>> signer = UriQuerySigner(SECRET_KEY)
    >>> signer.sign('url', quote('http://gjcourt.com/', safe=''))
    'url=http%3A%2F%2Fgjcourt.com%2F&st=5w5aZT_WaMY8LhvQL055gg&e=1365904071'

Configuration
-------------

Both signers are constructed with the same arguments, defined on the
base `Signer` class in `nginx_signing/signing.py`:

- `key` - the shared secret, matching whatever is configured for
  `secure_link_md5` in nginx.
- `timeout` - seconds from now until the signature expires. Defaults to
  86400 (24 hours). Pass `None` to sign without an expiration.
- `format` - the template used to build the string that gets hashed.
  Defaults to `'{key}{value}{expiration}'` and must match the expression
  nginx is configured to hash on its end.
