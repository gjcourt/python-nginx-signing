Python Nginx Signing
====================

Nginx is an amazing little web server that can do a lot of work for you so that you don't have to!. Why worry about signing and unsigning
requests when your web server can handle that for you. Now you don't have to.

This simple library allows you to sign requests as required by the Nginx [Secure Link](http://wiki.nginx.org/HttpSecureLinkModule) module.



Installation
------------

`>>> pip install nginx_signing`


Uri Example
-----------

The following example shows you how to sign an entire uri as documented in the nginx configuration [here](http://wiki.nginx.org/HttpSecureLinkModule#Example_usage:)

    >>> from nginx_signing.signing import UriSigner
    >>> signer = UriSigner(SECRET_KEY)
    >>> signer.sign('http://gjcourt.com')
    'http://gjcourt.com?&st=uDqsQqA_ysTYR_bUdMUAGw&e=1365903669'


Query String Example
--------------------

You can do more complex things. Say for example you only wanted to sign on a specific query string argument.

    >>> from nginx_signing.signing import UriQuerySigner
    >>> signer = UriQuerySigner(SECRET_KEY)
    >>> signer.sign('url', quote('http://gjcourt/com/', safe='/'))
    'url=http%3A%2F%2Fgjcourt.com&st=5w5aZT_WaMY8LhvQL055gg&e=1365904071'


That's about it. Happy signing.
