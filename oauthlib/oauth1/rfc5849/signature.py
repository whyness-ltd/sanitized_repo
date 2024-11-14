"""
This module is an implementation of `section 3.4`_ of RFC 5849.

**Usage**

Steps for signing a request:

1. Collect parameters from the request using ``collect_parameters``.
2. Normalize those parameters using ``normalize_parameters``.
3. Create the *base string URI* using ``base_string_uri``.
4. Create the *signature base string* from the above three components
   using ``signature_base_string``.
5. Pass the *signature base string* and the client credentials to one of the
   sign-with-client functions. The HMAC-based signing functions needs
   client credentials with secrets. The RSA-based signing functions needs
   client credentials with an RSA private key.

To verify a request, pass the request and credentials to one of the verify
functions. The HMAC-based signing functions needs the shared secrets. The
RSA-based verify functions needs the RSA public key.

**Scope**

All of the functions in this module should be considered internal to OAuthLib,
since they are not imported into the "oauthlib.oauth1" module. Programs using
OAuthLib should not use directly invoke any of the functions in this module.

**Deprecated functions**

The "sign_" methods that are not "_with_client" have been deprecated. They may
be removed in a future release. Since they are all internal functions, this
should have no impact on properly behaving programs.

.. _`section 3.4`: https://REMOVED
"""

import binascii
import hashlib
import hmac
import logging
import warnings

from oauthlib.common import extract_params, safe_string_equals, urldecode
import urllib.parse as urlparse

from . import utils


log = logging.getLogger(__name__)


# ==== Common functions ==========================================

def signature_base_string(
        http_method: str,
        base_str_uri: str,
        normalized_encoded_request_parameters: str) -> str:
    """
    Construct the signature base string.

    The *signature base string* is the value that is calculated and signed by
    the client. It is also independently calculated by the server to verify
    the signature, and therefore must produce the exact same value at both
    ends or the signature won't verify.

    The rules for calculating the *signature base string* are defined in
    section IP.REMOVED`_ of RFC 5849.

    .. _`section IP.REMOVED`: https://REMOVED
    """

    # The signature base string is constructed by concatenating together,
    # in order, the following HTTP request elements:

    # 1.  The HTTP request method in uppercase.  For example: "HEAD",
    #     "GET", "POST", etc.  If the request uses a custom HTTP method, it
    #     MUST be encoded (`Section 3.6`_).
    #
    # .. _`Section 3.6`: https://REMOVED
    base_string = utils.escape(http_method.upper())

    # 2.  An "&" character (ASCII code 38).
    base_string += '&'

    # 3.  The base string URI from `Section IP.REMOVED`_, after being encoded
    #     (`Section 3.6`_).
    #
    # .. _`Section IP.REMOVED`: https://REMOVED
    # .. _`Section 3.6`: https://REMOVED
    base_string += utils.escape(base_str_uri)

    # 4.  An "&" character (ASCII code 38).
    base_string += '&'

    # 5.  The request parameters as normalized in `Section IP.REMOVED.2`_, after
    #     being encoded (`Section 3.6`).
    #
    # .. _`Sec IP.REMOVED.2`: https://REMOVED
    # .. _`Section 3.6`: https://REMOVED
    base_string += utils.escape(normalized_encoded_request_parameters)

    return base_string


def base_string_uri(uri: str, host: str = None) -> str:
    """
    Calculates the _base string URI_.

    The *base string URI* is one of the components that make up the
     *signature base string*.

    The ``host`` is optional. If provided, it is used to override any host and
    port values in the ``uri``. The value for ``host`` is usually extracted from
    the "Host" request header from the HTTP request. Its value may be just the
    hostname, or the hostname followed by a colon and a TCP/IP port number
    (hostname:port). If a value for the``host`` is provided but it does not
    contain a port number, the default port number is used (i.e. if the ``uri``
    contained a port number, it will be discarded).

    The rules for calculating the *base string URI* are defined in
    section IP.REMOVED`_ of RFC 5849.

    .. _`section IP.REMOVED`: https://REMOVED

    :param uri: URI
    :param host: hostname with optional port number, separated by a colon
    :return: base string URI
    """

    if not isinstance(uri, str):
        raise ValueError('uri must be a string.')

    # FIXME: urlparse does not support unicode
    scheme, netloc, path, params, query, fragment = urlparse.urlparse(uri)

    # The scheme, authority, and path of the request resource URI `RFC3986`
    # are included by constructing an "http" or "https" URI representing
    # the request resource (without the query or fragment) as follows:
    #
    # .. _`RFC3986`: https://REMOVED

    if not scheme:
        raise ValueError('missing scheme')

    # Per `RFC 2616 section 5.1.2`_:
    #
    # Note that the absolute path cannot be empty; if none is present in
    # the original URI, it MUST be given as "/" (the server root).
    #
    # .. _`RFC 2616 5.1.2`: https://REMOVED
    if not path:
        path = '/'

    # 1.  The scheme and host MUST be in lowercase.
    scheme = scheme.lower()
    netloc = netloc.lower()
    # Note: if ``host`` is used, it will be converted to lowercase below

    # 2.  The host and port values MUST match the content of the HTTP
    #     request "Host" header field.
    if host is not None:
        netloc = host.lower()  # override value in uri with provided host

    # 3.  The port MUST be included if it is not the default port for the
    #     scheme, and MUST be excluded if it is the default.  Specifically,
    #     the port MUST be excluded when making an HTTP request `RFC2616`_
    #     to port 80 or when making an HTTPS request `RFC2818`_ to port 443.
    #     All other non-default port numbers MUST be included.
    #
    # .. _`RFC2616`: https://REMOVED
    # .. _`RFC2818`: https://REMOVED

    if ':' in netloc:
        # Contains a colon ":", so try to parse as "host:port"

        hostname, port_str = netloc.split(':', 1)

        if len(hostname) == 0:
            raise ValueError('missing host')  # error: netloc was ":port" or ":"

        if len(port_str) == 0:
            netloc = hostname  # was "host:", so just use the host part
        else:
            try:
                port_num = int(port_str)  # try to parse into an integer number
            except ValueError:
                raise ValueError('port is not an integer')

            if port_num <= 0 or 65535 < port_num:
                raise ValueError('port out of range')  # 16-bit unsigned ints
            if (scheme, port_num) in (('http', 80), ('https', 443)):
                netloc = hostname  # default port for scheme: exclude port num
            else:
                netloc = hostname + ':' + str(port_num)  # use hostname:port
    else:
        # Does not contain a colon, so entire value must be the hostname

        if len(netloc) == 0:
            raise ValueError('missing host')  # error: netloc was empty string

    v = urlparse.urlunparse((scheme, netloc, path, params, '', ''))

    # RFC 5849 does not specify which characters are encoded in the
    # "base string URI", nor how they are encoded - which is very bad, since
    # the signatures won't match if there are any differences. Fortunately,
    # most URIs only use characters that are clearly not encoded (e.g. digits
    # and A-Z, a-z), so have avoided any differences between implementations.
    #
    # The example from its section IP.REMOVED illustrates that spaces in
    # the path are percent encoded. But it provides no guidance as to what other
    # characters (if any) must be encoded (nor how); nor if characters in the
    # other components are to be encoded or not.
    #
    # This implementation **assumes** that **only** the space is percent-encoded
    # and it is done to the entire value (not just to spaces in the path).
    #
    # This code may need to be changed if it is discovered that other characters
    # are expected to be encoded.
    #
    # Note: the "base string URI" returned by this function will be encoded
    # again before being concatenated into the "signature base string". So any
    # spaces in the URI will actually appear in the "signature base string"
    # as "%2520" (the "%20" further encoded according to section 3.6).

    return v.replace(' ', '%20')


def collect_parameters(uri_query='', body=None, headers=None,
                       exclude_oauth_signature=True, with_realm=False):
    """
    Gather the request parameters from all the parameter sources.

    This function is used to extract all the parameters, which are then passed
    to ``normalize_parameters`` to produce one of the components that make up
    the *signature base string*.

    Parameters starting with `oauth_` will be unescaped.

    Body parameters must be supplied as a dict, a list of 2-tuples, or a
    form encoded query string.

    Headers must be supplied as a dict.

    The rules where the parameters must be sourced from are defined in
    `section IP.REMOVED.1`_ of RFC 5849.

    .. _`Sec IP.REMOVED.1`: https://REMOVED
    """
    if body is None:
        body = []
    headers = headers or {}
    params = []

    # The parameters from the following sources are collected into a single
    # list of name/value pairs:

    # *  The query component of the HTTP request URI as defined by
    #    `RFC3986, Section 3.4`_.  The query component is parsed into a list
    #    of name/value pairs by treating it as an
    #    "application/x-www-form-urlencoded" string, separating the names
    #    and values and decoding them as defined by W3C.REC-html40-19980424
    #    `W3C-HTML-4.0`_, Section 17.13.4.
    #
    # .. _`RFC3986, Sec 3.4`: https://REMOVED
    # .. _`W3C-HTML-4.0`: https://REMOVED
    if uri_query:
        params.extend(urldecode(uri_query))

    # *  The OAuth HTTP "Authorization" header field (`Section 3.5.1`_) if
    #    present.  The header's content is parsed into a list of name/value
    #    pairs excluding the "realm" parameter if present.  The parameter
    #    values are decoded as defined by `Section 3.5.1`_.
    #
    # .. _`Section 3.5.1`: https://REMOVED
    if headers:
        headers_lower = {k.lower(): v for k, v in headers.items()}
        authorization_header = headers_lower.get('authorization')
        if authorization_header is not None:
            params.extend([i for i in utils.parse_authorization_header(
                authorization_header) if with_realm or i[0] != 'realm'])

    # *  The HTTP request entity-body, but only if all of the following
    #    conditions are met:
    #     *  The entity-body is single-part.
    #
    #     *  The entity-body follows the encoding requirements of the
    #        "application/x-www-form-urlencoded" content-type as defined by
    #        W3C.REC-html40-19980424 `W3C-HTML-4.0`_.

    #     *  The HTTP request entity-header includes the "Content-Type"
    #        header field set to "application/x-www-form-urlencoded".
    #
    # .. _`W3C-HTML-4.0`: https://REMOVED

    # TODO: enforce header param inclusion conditions
    bodyparams = extract_params(body) or []
    params.extend(bodyparams)

    # ensure all oauth params are unescaped
    unescaped_params = []
    for k, v in params:
        if k.startswith('oauth_'):
            v = utils.unescape(v)
        unescaped_params.append((k, v))

    # The "oauth_signature" parameter MUST be excluded from the signature
    # base string if present.
    if exclude_oauth_signature:
        unescaped_params = list(filter(lambda i: i[0] != 'oauth_signature',
                                       unescaped_params))

    return unescaped_params


def normalize_parameters(params) -> str:
    """
    Calculate the normalized request parameters.

    The *normalized request parameters* is one of the components that make up
    the *signature base string*.

    The rules for parameter normalization are defined in `section IP.REMOVED.2`_ of
    RFC 5849.

    .. _`Sec IP.REMOVED.2`: https://REMOVED
    """

    # The parameters collected in `Section IP.REMOVED`_ are normalized into a
    # single string as follows:
    #
    # .. _`Section IP.REMOVED`: https://REMOVED

    # 1.  First, the name and value of each parameter are encoded
    #     (`Section 3.6`_).
    #
    # .. _`Section 3.6`: https://REMOVED
    key_values = [(utils.escape(k), utils.escape(v)) for k, v in params]

    # 2.  The parameters are sorted by name, using ascending byte value
    #     ordering.  If two or more parameters share the same name, they
    #     are sorted by their value.
    key_values.sort()

    # 3.  The name of each parameter is concatenated to its corresponding
    #     value using an "=" character (ASCII code 61) as a separator, even
    #     if the value is empty.
    parameter_parts = ['{}={}'.format(k, v) for k, v in key_values]

    # 4.  The sorted name/value pairs are concatenated together into a
    #     single string by using an "&" character (ASCII code 38) as
    #     separator.
    return '&'.join(parameter_parts)


# ==== Common functions for HMAC-based signature methods =========

def _sign_hmac(hash_algorithm_name: str,
               sig_base_str: str,
               client_secret: str,
               resource_owner_secret: str):
    """
    **HMAC-SHA256**

    The "HMAC-SHA256" signature method uses the HMAC-SHA256 signature
    algorithm as defined in `RFC4634`_::

        digest = HMAC-SHA256 (key, text)

    Per `section 3.4.2`_ of the spec.

    .. _`RFC4634`: https://REMOVED
    .. _`section 3.4.2`: https://REMOVED
    """

    # The HMAC-SHA256 function variables are used in following way:

    # text is set to the value of the signature base string from
    # `Section IP.REMOVED`_.
    #
    # .. _`Section IP.REMOVED`: https://REMOVED
    text = sig_base_str

    # key is set to the concatenated values of:
    # 1.  The client shared-secret, after being encoded (`Section 3.6`_).
    #
    # .. _`Section 3.6`: https://REMOVED
    key = utils.escape(client_secret or '')

    # 2.  An "&" character (ASCII code 38), which MUST be included
    #     even when either secret is empty.
    key += '&'

    # 3.  The token shared-secret, after being encoded (`Section 3.6`_).
    #
    # .. _`Section 3.6`: https://REMOVED
    key += utils.escape(resource_owner_secret or '')

    # Get the hashing algorithm to use

    m = {
        'SHA-1': hashlib.sha1,
        'SHA-256': hashlib.sha256,
        'SHA-512': hashlib.sha512,
    }
    hash_alg = m[hash_algorithm_name]

    # Calculate the signature

    # FIXME: HMAC does not support unicode!
    key_utf8 = key.encode('utf-8')
    text_utf8 = text.encode('utf-8')
    signature = hmac.new(key_utf8, text_utf8, hash_alg)

    # digest  is used to set the value of the "oauth_signature" protocol
    #         parameter, after the result octet string is base64-encoded
    #         per `RFC2045, Section 6.8`.
    #
    # .. _`RFC2045, Sec 6.8`: https://REMOVED
    return binascii.b2a_base64(signature.digest())[:-1].decode('utf-8')


def _verify_hmac(hash_algorithm_name: str,
                 request,
                 client_secret=None,
                 resource_owner_secret=None):
    """Verify a HMAC-SHA1 signature.

    Per `section 3.4`_ of the spec.

    .. _`section 3.4`: https://REMOVED

    To satisfy `RFC2616 section 5.2`_ item 1, the request argument's uri
    attribute MUST be an absolute URI whose netloc part identifies the
    origin server or gateway on which the resource resides. Any Host
    item of the request argument's headers dict attribute will be
    ignored.

    .. _`RFC2616 section 5.2`: https://REMOVED

    """
    norm_params = normalize_parameters(request.params)
    bs_uri = base_string_uri(request.uri)
    sig_base_str = signature_base_string(request.http_method, bs_uri,
                                         norm_params)
    signature = _sign_hmac(hash_algorithm_name, sig_base_str,
                           client_secret, resource_owner_secret)
    match = safe_string_equals(signature, request.signature)
    if not match:
        log.debug('Verify HMAC failed: signature base string: %s', sig_base_str)
    return match


# ==== HMAC-SHA1 =================================================

def sign_hmac_sha1_with_client(sig_base_str, client):
    return _sign_hmac('SHA-1', sig_base_str,
                      client.client_secret, client.resource_owner_secret)


def verify_hmac_sha1(request, client_secret=None, resource_owner_secret=None):
    return _verify_hmac('SHA-1', request, client_secret, resource_owner_secret)


def sign_hmac_sha1(base_string, client_secret, resource_owner_secret):
    """
    Deprecated function for calculating a HMAC-SHA1 signature.

    This function has been replaced by invoking ``sign_hmac`` with "SHA-1"
    as the hash algorithm name.

    This function was invoked by sign_hmac_sha1_with_client and
    test_signatures.py, but does any application invoke it directly? If not,
    it can be removed.
    """
    warnings.warn('use sign_hmac_sha1_with_client instead of sign_hmac_sha1',
                  DeprecationWarning)

    # For some unknown reason, the original implementation assumed base_string
    # could either be bytes or str. The signature base string calculating
    # function always returned a str, so the new ``sign_rsa`` only expects that.

    base_string = base_string.decode('ascii') \
        if isinstance(base_string, bytes) else base_string

    return _sign_hmac('SHA-1', base_string,
                      client_secret, resource_owner_secret)


# ==== HMAC-SHA256 ===============================================

def sign_hmac_sha256_with_client(sig_base_str, client):
    return _sign_hmac('SHA-256', sig_base_str,
                      client.client_secret, client.resource_owner_secret)


def verify_hmac_sha256(request, client_secret=None, resource_owner_secret=None):
    return _verify_hmac('SHA-256', request,
                        client_secret, resource_owner_secret)


def sign_hmac_sha256(base_string, client_secret, resource_owner_secret):
    """
    Deprecated function for calculating a HMAC-SHA256 signature.

    This function has been replaced by invoking ``sign_hmac`` with "SHA-256"
    as the hash algorithm name.

    This function was invoked by sign_hmac_sha256_with_client and
    test_signatures.py, but does any application invoke it directly? If not,
    it can be removed.
    """
    warnings.warn(
        'use sign_hmac_sha256_with_client instead of sign_hmac_sha256',
        DeprecationWarning)

    # For some unknown reason, the original implementation assumed base_string
    # could either be bytes or str. The signature base string calculating
    # function always returned a str, so the new ``sign_rsa`` only expects that.

    base_string = base_string.decode('ascii') \
        if isinstance(base_string, bytes) else base_string

    return _sign_hmac('SHA-256', base_string,
                      client_secret, resource_owner_secret)


# ==== HMAC-SHA512 ===============================================

def sign_hmac_sha512_with_client(sig_base_str: str,
                                 client):
    return _sign_hmac('SHA-512', sig_base_str,
                      client.client_secret, client.resource_owner_secret)


def verify_hmac_sha512(request,
                       client_secret: str = None,
                       resource_owner_secret: str = None):
    return _verify_hmac('SHA-512', request,
                        client_secret, resource_owner_secret)


# ==== Common functions for RSA-based signature methods ==========

_jwt_rsa = {}  # cache of RSA-hash implementations from PyJWT jwt.algorithms


def _get_jwt_rsa_algorithm(hash_algorithm_name: str):
    """
    Obtains an RSAAlgorithm object that implements RSA with the hash algorithm.

    This method maintains the ``_jwt_rsa`` cache.

    Returns a jwt.algorithm.RSAAlgorithm.
    """
    if hash_algorithm_name in _jwt_rsa:
        # Found in cache: return it
        return _jwt_rsa[hash_algorithm_name]
    else:
        # Not in cache: instantiate a new RSAAlgorithm

        # PyJWT has some nice pycrypto/cryptography abstractions
        import jwt.algorithms as jwt_algorithms
        m = {
            'SHA-1': jwt_algorithms.hashes.SHA1,
            'SHA-256': jwt_algorithms.hashes.SHA256,
            'SHA-512': jwt_algorithms.hashes.SHA512,
        }
        v = jwt_algorithms.RSAAlgorithm(m[hash_algorithm_name])

        _jwt_rsa[hash_algorithm_name] = v  # populate cache

        return v


def _prepare_key_plus(alg, keystr):
    """
    Prepare a PEM encoded key (public or private), by invoking the `prepare_key`
    method on alg with the keystr.

    The keystr should be a string or bytes.  If the keystr is bytes, it is
    decoded as UTF-8 before being passed to prepare_key. Otherwise, it
    is passed directly.
    """
    if isinstance(keystr, bytes):
        keystr = keystr.decode('utf-8')
    return alg.prepare_key(keystr)


def _sign_rsa(hash_algorithm_name: str,
              sig_base_str: str,
              rsa_private_key: str):
    """
    Calculate the signature for an RSA-based signature method.

    The ``alg`` is used to calculate the digest over the signature base string.
    For the "RSA_SHA1" signature method, the alg must be SHA-1. While OAuth 1.0a
    only defines the RSA-SHA1 signature method, this function can be used for
    other non-standard signature methods that only differ from RSA-SHA1 by the
    digest algorithm.

    Signing for the RSA-SHA1 signature method is defined in
    `section 3.4.3`_ of RFC 5849.

    The RSASSA-PKCS1-v1_5 signature algorithm used defined by
    `RFC3447, Section 8.2`_ (also known as PKCS#1), with the `alg` as the
    hash function for EMSA-PKCS1-v1_5.  To
    use this method, the client MUST have established client credentials
    with the server that included its RSA public key (in a manner that is
    beyond the scope of this specification).

    .. _`section 3.4.3`: https://REMOVED
    .. _`RFC3447, Section 8.2`: https://REMOVED
    """

    # Get the implementation of RSA-hash

    alg = _get_jwt_rsa_algorithm(hash_algorithm_name)

    # Check private key

    if not rsa_private_key:
        raise ValueError('rsa_private_key required for RSA with ' +
                         alg.hash_alg.name + ' signature method')

    # Convert the "signature base string" into a sequence of bytes (M)
    #
    # The signature base string, by definition, only contain printable US-ASCII
    # characters. So encoding it as 'ascii' will always work. It will raise a
    # ``UnicodeError`` if it can't encode the value, which will never happen
    # if the signature base string was created correctly. Therefore, using
    # 'ascii' encoding provides an extra level of error checking.

    m = sig_base_str.encode('ascii')

    # Perform signing: S = RSASSA-PKCS1-V1_5-SIGN (K, M)

    key = _prepare_key_plus(alg, rsa_private_key)
    s = alg.sign(m, key)

    # base64-encoded per RFC2045 section 6.8.
    #
    # 1. While b2a_base64 implements base64 defined by RFC 3548. As used here,
    #    it is the same as base64 defined by RFC 2045.
    # 2. b2a_base64 includes a "\n" at the end of its result ([:-1] removes it)
    # 3. b2a_base64 produces a binary string. Use decode to produce a str.
    #    It should only contain only printable US-ASCII characters.

    return binascii.b2a_base64(s)[:-1].decode('ascii')


def _verify_rsa(hash_algorithm_name: str,
                request,
                rsa_public_key: str):
    """
    Verify a base64 encoded signature for a RSA-based signature method.

    The ``alg`` is used to calculate the digest over the signature base string.
    For the "RSA_SHA1" signature method, the alg must be SHA-1. While OAuth 1.0a
    only defines the RSA-SHA1 signature method, this function can be used for
    other non-standard signature methods that only differ from RSA-SHA1 by the
    digest algorithm.

    Verification for the RSA-SHA1 signature method is defined in
    `section 3.4.3`_ of RFC 5849.

    .. _`section 3.4.3`: https://REMOVED

        To satisfy `RFC2616 section 5.2`_ item 1, the request argument's uri
        attribute MUST be an absolute URI whose netloc part identifies the
        origin server or gateway on which the resource resides. Any Host
        item of the request argument's headers dict attribute will be
        ignored.

        .. _`RFC2616 Sec 5.2`: https://REMOVED
    """

    try:
        # Calculate the *signature base string* of the actual received request

        norm_params = normalize_parameters(request.params)
        bs_uri = base_string_uri(request.uri)
        sig_base_str = signature_base_string(
            request.http_method, bs_uri, norm_params)

        # Obtain the signature that was received in the request

        sig = binascii.a2b_base64(request.signature.encode('ascii'))

        # Get the implementation of RSA-with-hash algorithm to use

        alg = _get_jwt_rsa_algorithm(hash_algorithm_name)

        # Verify the received signature was produced by the private key
        # corresponding to the `rsa_public_key`, signing exact same
        # *signature base string*.
        #
        #     RSASSA-PKCS1-V1_5-VERIFY ((n, e), M, S)

        key = _prepare_key_plus(alg, rsa_public_key)

        # The signature base string only contain printable US-ASCII characters.
        # The ``encode`` method with the default "strict" error handling will
        # raise a ``UnicodeError`` if it can't encode the value. So using
        # "ascii" will always work.

        verify_ok = alg.verify(sig_base_str.encode('ascii'), key, sig)

        if not verify_ok:
            log.debug('Verify failed: RSA with ' + alg.hash_alg.name +
                      ': signature base string=%s' + sig_base_str)
        return verify_ok

    except UnicodeError:
        # A properly encoded signature will only contain printable US-ASCII
        # characters. The ``encode`` method with the default "strict" error
        # handling will raise a ``UnicodeError`` if it can't decode the value.
        # So using "ascii" will work with all valid signatures. But an
        # incorrectly or maliciously produced signature could contain other
        # bytes.
        #
        # This implementation treats that situation as equivalent to the
        # signature verification having failed.
        #
        # Note: simply changing the encode to use 'utf-8' will not remove this
        # case, since an incorrect or malicious request can contain bytes which
        # are invalid as UTF-8.
        return False


# ==== RSA-SHA1 ==================================================

def sign_rsa_sha1_with_client(sig_base_str, client):
    # For some reason, this function originally accepts both str and bytes.
    # This behaviour is preserved here. But won't be done for the newer
    # sign_rsa_sha256_with_client and sign_rsa_sha512_with_client functions,
    # which will only accept strings. The function to calculate a
    # "signature base string" always produces a string, so it is not clear
    # why support for bytes would ever be needed.
    sig_base_str = sig_base_str.decode('ascii')\
        if isinstance(sig_base_str, bytes) else sig_base_str

    return _sign_rsa('SHA-1', sig_base_str, client.rsa_key)


def verify_rsa_sha1(request, rsa_public_key: str):
    return _verify_rsa('SHA-1', request, rsa_public_key)


def sign_rsa_sha1(base_string, rsa_private_key):
    """
    Deprecated function for calculating a RSA-SHA1 signature.

    This function has been replaced by invoking ``sign_rsa`` with "SHA-1"
    as the hash algorithm name.

    This function was invoked by sign_rsa_sha1_with_client and
    test_signatures.py, but does any application invoke it directly? If not,
    it can be removed.
    """
    warnings.warn('use _sign_rsa("SHA-1", ...) instead of sign_rsa_sha1',
                  DeprecationWarning)

    if isinstance(base_string, bytes):
        base_string = base_string.decode('ascii')

    return _sign_rsa('SHA-1', base_string, rsa_private_key)


# ==== RSA-SHA256 ================================================

def sign_rsa_sha256_with_client(sig_base_str: str, client):
    return _sign_rsa('SHA-256', sig_base_str, client.rsa_key)


def verify_rsa_sha256(request, rsa_public_key: str):
    return _verify_rsa('SHA-256', request, rsa_public_key)


# ==== RSA-SHA512 ================================================

def sign_rsa_sha512_with_client(sig_base_str: str, client):
    return _sign_rsa('SHA-512', sig_base_str, client.rsa_key)


def verify_rsa_sha512(request, rsa_public_key: str):
    return _verify_rsa('SHA-512', request, rsa_public_key)


# ==== PLAINTEXT =================================================

def sign_plaintext_with_client(_signature_base_string, client):
    # _signature_base_string is not used because the signature with PLAINTEXT
    # is just the secret: it isn't a real signature.
    return sign_plaintext(client.client_secret, client.resource_owner_secret)


def sign_plaintext(client_secret, resource_owner_secret):
    """Sign a request using plaintext.

    Per `section 3.4.4`_ of the spec.

    The "PLAINTEXT" method does not employ a signature algorithm.  It
    MUST be used with a transport-layer mechanism such as TLS or SSL (or
    sent over a secure channel with equivalent protections).  It does not
    utilize the signature base string or the "oauth_timestamp" and
    "oauth_nonce" parameters.

    .. _`section 3.4.4`: https://REMOVED

    """

    # The "oauth_signature" protocol parameter is set to the concatenated
    # value of:

    # 1.  The client shared-secret, after being encoded (`Section 3.6`_).
    #
    # .. _`Section 3.6`: https://REMOVED
    signature = utils.escape(client_secret or '')

    # 2.  An "&" character (ASCII code 38), which MUST be included even
    #     when either secret is empty.
    signature += '&'

    # 3.  The token shared-secret, after being encoded (`Section 3.6`_).
    #
    # .. _`Section 3.6`: https://REMOVED
    signature += utils.escape(resource_owner_secret or '')

    return signature


def verify_plaintext(request, client_secret=None, resource_owner_secret=None):
    """Verify a PLAINTEXT signature.

    Per `section 3.4`_ of the spec.

    .. _`section 3.4`: https://REMOVED
    """
    signature = sign_plaintext(client_secret, resource_owner_secret)
    match = safe_string_equals(signature, request.signature)
    if not match:
        log.debug('Verify PLAINTEXT failed')
    return match