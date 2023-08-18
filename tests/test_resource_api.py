import asynctest
import jwt
import time
from aiohttp import web
from aiohttp.test_utils import TestServer, TestClient as AioHTTPTestClient
from auth_http.mock_resource_api import get_data
from settings import settings

class TestResourceAPI(asynctest.TestCase):

    async def setUp(self):
        self.app = web.Application()
        self.app.router.add_get('/get_data', get_data)
        self.server = TestServer(self.app)
        self.client = AioHTTPTestClient(self.server)
        await self.client.start_server()

    async def tearDown(self):
        await self.client.close()

    async def test_valid_token(self):
        auth_header = 'Bearer ' + jwt.encode({'user_name': settings.USER_NAME}, settings.JWT_SECRET_KEY, algorithm='HS256')
        response = await self.client.get('/get_data', headers={'Authorization': auth_header})
        self.assertEqual(response.status, 200)
        self.assertEqual(await response.json(), {'data': 'mock_data'})

    async def test_missing_auth_header(self):
        response = await self.client.get('/get_data')
        self.assertEqual(response.status, 401)

    async def test_invalid_auth_type(self):
        auth_header = 'InvalidType ' + jwt.encode({'user_name': settings.USER_NAME}, settings.JWT_SECRET_KEY, algorithm='HS256')
        response = await self.client.get('/get_data', headers={'Authorization': auth_header})
        self.assertEqual(response.status, 401)

    async def test_expired_token(self):
        token_payload = {'user_name': settings.USER_NAME, 'exp': int(time.time()) - 3600}  # One hour ago
        expired_token = jwt.encode(token_payload, settings.JWT_SECRET_KEY, algorithm='HS256')
        auth_header = 'Bearer ' + expired_token
        response = await self.client.get('/get_data', headers={'Authorization': auth_header})
        self.assertEqual(response.status, 401)

    async def test_invalid_token(self):
        auth_header = 'Bearer invalid_token'
        response = await self.client.get('/get_data', headers={'Authorization': auth_header})
        self.assertEqual(response.status, 401)

    async def test_unknown_user(self):
        auth_header = 'Bearer ' + jwt.encode({'user_name': 'unknown_user'}, settings.JWT_SECRET_KEY, algorithm='HS256')
        response = await self.client.get('/get_data', headers={'Authorization': auth_header})
        self.assertEqual(response.status, 401)

if __name__ == '__main__':
    asynctest.main()
