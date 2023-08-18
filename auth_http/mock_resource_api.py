import jwt
from aiohttp import web
from settings import settings

async def get_data(request):
    """
    Endpoint to simulate fetching data from the Resource API.

    This endpoint validates the access token and returns mock data as a response.

    :param request: The HTTP request object.
    :return: A JSON response with mock data if the token is valid, otherwise Unauthorized response.
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return web.Response(status=401, text='Unauthorized')

    try:
        auth_type, access_token = auth_header.split()
        if auth_type.lower() != 'bearer':
            raise ValueError
        # Verify the access token using the SECRET_KEY
        payload = jwt.decode(access_token, settings.JWT_SECRET_KEY, algorithms=["HS256"])

        # Check if the user_name is a valid user
        user_name = payload.get('user_name')
        if user_name not in settings.AUTH_CREDENTIALS:
            return web.Response(status=401, text='Unauthorized')

        response_data = {'data': 'mock_data'}
        return web.json_response(response_data)
    except jwt.ExpiredSignatureError:
        return web.Response(status=401, text='Token has expired')
    except (jwt.DecodeError , ValueError):
        return web.Response(status=401, text='Invalid token')


app = web.Application()
app.router.add_get('/get_data', get_data)
