import asynctest
from aiohttp.test_utils import TestServer, TestClient as AioHTTPTestClient
from aiohttp import web
from auth_http.mock_auth_server import authenticate

class TestAuthorizationServer(asynctest.TestCase):
    async def setUp(self):
        self.app = web.Application()
        self.app.router.add_get('/authenticate', authenticate)
        self.server = TestServer(self.app)
        self.client = AioHTTPTestClient(self.server)
        await self.client.start_server()

    async def tearDown(self):
        await self.client.close()

    async def test_authentication_success(self):
        response = await self.client.get("/authenticate", headers={'Authorization': 'Basic QUJOQU1STzpBQk5BTVJP'})
        self.assertEqual(response.status, 200)
        data = await response.json()
        self.assertIn("access_token", data)

    async def test_authentication_failure(self):
        response = await self.client.get("/authenticate", headers={'Authorization': 'Basic QUJOQU1STzpBQk5BTVYY'})
        self.assertEqual(response.status, 401)

if __name__ == "__main__":
    asynctest.main()
