import pytest
import unittest
from freezegun import freeze_time
from nginx_signing.signing import Nginx, UriSigner, UriQuerySigner


class TestNginx(unittest.TestCase):

    @freeze_time("1970-01-01")
    def test_get_expiration(self):
        signer = Nginx('SECRET', timeout=60)
        self.assertEquals(signer.get_expiration(), '60')

    @freeze_time("1970-01-01")
    def test_signature(self):
        signer = Nginx('SECRET', timeout=60)
        self.assertEquals(signer.signature('uri'), ('jtRlAsbqul2YrhTNSc0rQQ', '60'))


class TestUriSigner(unittest.TestCase):

    @freeze_time("1970-01-01")
    def test_sign(self):
        signer = UriSigner('SECRET', timeout=60)
        self.assertEquals(signer.sign('/'), '/?st=3RlvH8cotvNZCeobCvbuBQ&e=60')


class TestUriQuerySigner(unittest.TestCase):

    @freeze_time("1970-01-01")
    def test_sign(self):
        signer = UriQuerySigner('SECRET', timeout=60)
        self.assertEqual(signer.sign('key', 'value'), 'key=value&st=H3rKl3peau20Sml2IH7GjQ&e=60')
