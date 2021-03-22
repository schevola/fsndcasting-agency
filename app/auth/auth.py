import json
from flask import request
from functools import wraps
from jose import jwt, JWTError
from urllib.request import urlopen

AUTH0_DOMAIN = 'schevola-coffee-shop.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'castingAgency'

class AuthnError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    authHeader = request.headers.get("Authorization", None)
    return validate_auth_header(authHeader)


def validate_auth_header(authHeader):
    if authHeader is not None:
        split = authHeader.split()
        if len(split) == 2 and split[0].upper() == "BEARER":
            return split[1]
    raise AuthnError({"code": "Invalid_Token_Auth",
                     "description": "Authorization token is expected"}, 401)


def check_permissions(permission, payload):
    if payload.get('permissions') is not None and permission in payload.get('permissions'):
        return True
    raise AuthnError({"code": "Invalid_Permissions",
                     "description": "Valid Permissions Expected"}, 401)


def verify_decode_jwt(token):
    url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(url.read())
    try:
        unverified_header = jwt.get_unverified_header(token)
    except JWTError:
        raise AuthnError({
            'code': 'invalid_token',
            'description': 'token is invalid'
        }, 400)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthnError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthnError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthnError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthnError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthnError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)


def authRequired(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
