from setuptools import setup
from nginx_signing import __version__

setup(
    name = 'nginx_signing',
    version = __version__,
    author = "George Courtsunis",
    author_email = "gjcourt@gmail.com",
    description = "Signs urls to work with the nginx Secure Link module",
    license = "MIT License",
    keywords = "nginx signing secure_link",
    url = "http://github.com/gjcourt/python-nginx-signer",
)
