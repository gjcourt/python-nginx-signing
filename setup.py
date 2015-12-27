import nginx_signing
from setuptools import setup

setup(
    name='nginx_signing',
    version=nginx_signing.__version__,
    author="George Courtsunis",
    author_email="gjcourt@gmail.com",
    description="Signs urls to work with the nginx Secure Link module",
    license="MIT License",
    packages=['nginx_signing'],
    keywords="nginx signing secure_link",
    url="https://github.com/gjcourt/python-nginx-signing",
    install_requires = ['six']
)
