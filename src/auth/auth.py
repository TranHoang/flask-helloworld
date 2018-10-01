"""
Validate the Auth0 access token sent from client. This emplement is based
on the following reference links
https://auth0.com/docs/api-auth/tutorials/verify-access-token
https://auth0.com/docs/quickstart/backend/python/01-authorization
https://auth0.com/docs/jwks#using-the-jwks-in-your-application-to-verify-a-jwt
"""

import os
import json
import jwt
from flask import request, _request_ctx_stack
from functools import wraps
from urllib.request import urlopen
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend

from .exceptions import AuthError

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = [os.getenv('AUTH0_ALGORITHMS')]
API_AUDIENCE = os.getenv('AUTH0_API_AUDIENCE')


def get_token_auth_header():
    """
    Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token

def requires_auth(f):
    """
    Determines if the Access Token is valid
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        assert AUTH0_DOMAIN and ALGORITHMS and API_AUDIENCE, \
            "Missing autho0 domain or algorithm or api audience configuration."

        access_token = get_token_auth_header()
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read().decode('utf-8'))

        unverified_header = jwt.get_unverified_header(access_token)
        if "kid" not in unverified_header:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "x5c": key['x5c'][0]
                }
        
        if rsa_key:
            cert = '-----BEGIN CERTIFICATE-----\n' + rsa_key['x5c'] + '\n-----END CERTIFICATE-----'
            certificate = load_pem_x509_certificate(str.encode(cert), default_backend())
            publickey = certificate.public_key()

            try:
                payload = jwt.decode(
                    access_token,
                    publickey,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, 401)
            except Exception:
                raise AuthError({
                    "code": "invalid_header",
                    "description": "Unable to parse authentication token."}, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        else:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)
    
    return decorated


def get_identity():
    """
    Reuturn the user id from Token information which
    already saved in _request_ctx_stack.top.current_user
    when requires_auth decorate function execution.
    """
    payload = getattr(_request_ctx_stack.top, 'current_user', None)
    if payload and 'sub' in payload:
        return payload['sub']
    
    return None
