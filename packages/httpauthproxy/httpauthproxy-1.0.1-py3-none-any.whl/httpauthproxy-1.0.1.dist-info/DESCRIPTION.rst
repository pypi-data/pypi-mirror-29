authproxy
=========

A simple Python 3 service that accepts HTTP requests with an
``Authorization`` header, and authenticates the credentials against an
identity backend service, such as LDAP.

This is particularly useful in combination with
`ngx_http_auth_request_module <http://nginx.org/en/docs/http/ngx_http_auth_request_module.html>`_.

Usage
-----

::

    usage: authproxy [-h] [-b BIND] -u URL [--ca-certs-file] [--ca-certs-dir]
                     [--no-verify] [--ldap-user-pattern] [--ldap-member-attr]

    Simple HTTP server to proxy authentication requests.

    optional arguments:
      -h, --help            show this help message and exit
      -b BIND, --bind BIND  IP:port to bind to (default: 127.0.0.1:8018)
      -u URL, --url URL     URL of auth server (multiple, required)
      --ca-certs-file       Path to CA certs bundle file
      --ca-certs-dir        Path to directory containing CA certs
      --no-verify           Skip TLS verification
      --ldap-user-pattern   User DN string with {} for username
      --ldap-member-attr    User attribute containing group memberships

Example
-------

.. code-block:: bash

    authproxy -u ldaps://ipa.localdomain.tld \
        --ca-certs-file /etc/ipa/ca.crt \
        --ldap-user-pattern uid={},cn=users,cn=accounts,dc=localdomain,dc=tld



