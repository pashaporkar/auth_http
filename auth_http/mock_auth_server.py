"""
Mock Authorization Server

This script simulates an authorization server that authenticates clients and issues access tokens.
It is only intended to illustrate the basic concepts of an authorization server.
"""
from aiohttp import web
import base64
import hashlib
import jwt
from settings import settings

async def authenticate(request):
    """
    Authenticate the client using basic authentication and SHA-256 hashing.

    This function handles the authentication process using basic authentication headers.
    The provided client password is securely hashed using SHA-256 along with a unique salt.

    :param request: The HTTP request object.
    :return: A JSON response with an access token if authentication is successful,
             or an Unauthorized response.
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return web.Response(status=401, text='Unauthorized', headers={'WWW-Authenticate': 'Basic'})

    try:
        auth_type, credentials = auth_header.split()
        if auth_type.lower() != 'basic':
            raise ValueError

        decoded_credentials = base64.b64decode(credentials.encode('utf-8')).decode('utf-8')
        user_name, password = decoded_credentials.split(':')

        if user_name in settings.AUTH_CREDENTIALS:
            stored_salt = settings.AUTH_CREDENTIALS[user_name]['salt']
            stored_hash = settings.AUTH_CREDENTIALS[user_name]['hash']

            hashed_secret = hashlib.sha256(password.encode() + stored_salt).hexdigest()

            if stored_hash == hashed_secret:
                access_token = jwt.encode({"user_name": user_name}, settings.JWT_SECRET_KEY, algorithm="HS256")
                response_data = {'access_token': access_token}
                return web.json_response(response_data)

        return web.Response(status=401, text='Unauthorized', headers={'WWW-Authenticate': 'Basic'})

    except (ValueError, UnicodeDecodeError):
        return web.Response(status=400, text='Bad Request')

app = web.Application()
app.router.add_post('/authenticate', authenticate)

