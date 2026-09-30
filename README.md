<!-- readme-type: tool -->
# python-nginx-signing

Signs urls to work with the Secure Link module of nginx

nginx's [Secure Link](http://wiki.nginx.org/HttpSecureLinkModule) module can
protect a URL with a hashed signature and an expiration, but generating that
signature outside nginx means reimplementing its MD5-and-base64 scheme by
hand. python-nginx-signing does that math in Python instead, producing the
same `st`/`e` values nginx's `secure_link_md5` directive expects. It provides
two signers: one for signing an entire URL, one for signing a single query
argument.

**Status:** unmaintained since 2015 — Python 2 only. `nginx_signing.signing`
fails to import under Python 3 (confirmed here: `ModuleNotFoundError: No
module named 'urlparse'`).

## Quick start

Needs: Python 2.7 to actually sign anything (see Status above); installing
and checking the version work on Python 3 too.

```bash
git clone https://github.com/gjcourt/python-nginx-signing && cd python-nginx-signing
pip install .
python -c "import nginx_signing; print(nginx_signing.__version__)"
```

```text
0.1.6
```

## Usage

Sign an entire URI, appending `st` and `e` to its query string:

```python
from nginx_signing.signing import UriSigner

signer = UriSigner(SECRET_KEY)
signer.sign('http://gjcourt.com')
```

```text
'http://gjcourt.com?st=N22oa2M9bMxj-RUMGp4QMw&e=1790834527'
```

Sign a single query argument instead of the whole URI:

```python
from urllib import quote
from nginx_signing.signing import UriQuerySigner

signer = UriQuerySigner(SECRET_KEY)
signer.sign('url', quote('http://gjcourt.com/', safe=''))
```

```text
'url=http%3A%2F%2Fgjcourt.com%2F&st=H7XDtdgjdj-TMfjlCd82HQ&e=1790834527'
```

## Configuration

Both signers take the same constructor arguments, defined on the base
`Signer` class in `nginx_signing/signing.py`:

| Name | Default | Meaning |
|---|---|---|
| `key` | *(required)* | The shared secret, matching `secure_link_md5` in nginx. |
| `timeout` | `86400` (24 hours) | Seconds from now until the signature expires. Pass `None` to sign without an expiration. |
| `format` | `'{key}{value}{expiration}'` | Template for the string that gets hashed; must match the expression nginx is configured to hash. |

## How it works

`Signer.signature()` fills `format` with the key, the value being signed,
and the computed expiration, MD5-hashes the result, and base64url-encodes
the digest with trailing `=` stripped — the same recipe nginx's
`secure_link_md5` module computes when it checks an incoming request.
`UriSigner` appends the result to a full URL as `st`/`e` query parameters;
`UriQuerySigner` returns just the `key=value&st=...&e=...` pair for signing
one argument.

## Development

There is no Makefile, test suite, or CI configured for this repo yet.

```bash
pip install -e .
```

## License

No licence file yet.
