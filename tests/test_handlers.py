import asynctest
from asynctest import CoroutineMock, patch
from auth_http.exceptions import AuthorizationError, DataFetchError
from auth_http.handlers import AuthorizationHandler, DataFetchingHandler

class TestAuthorizationHandler(asynctest.TestCase):

    @patch('aiohttp.ClientSession')  
    async def test_authentication_success(self, MockClientSession):
        http_client = MockClientSession()
        response_mock = CoroutineMock(status=200, json=CoroutineMock(return_value={"access_token": "mock_access_token"}))
        http_client.post.return_value.__aenter__.return_value = response_mock
        handler = AuthorizationHandler(http_client = http_client)

        access_token = await handler.authenticate("mock_user_name", "mock_password")

        self.assertEqual(access_token, "mock_access_token")

    @patch('aiohttp.ClientSession')
    async def test_authentication_failure(self, MockClientSession):
        http_client = MockClientSession()
        response_mock = CoroutineMock(status=401)
        http_client.post.return_value.__aenter__.return_value = response_mock
        handler = AuthorizationHandler(http_client = http_client)

        with self.assertRaises(AuthorizationError):
            await handler.authenticate("mock_user_name", "mock_password")

class TestDataFetchingHandler(asynctest.TestCase):

    @patch('aiohttp.ClientSession')
    async def test_fetch_data_success(self, MockClientSession):
        http_client = MockClientSession()
        http_client.get.return_value.__aenter__.return_value = CoroutineMock(status=200, json=CoroutineMock(return_value={"data": "mock_data"}))
        handler = DataFetchingHandler(http_client = http_client)

        data = await handler.fetch_data("mock_access_token")

        self.assertEqual(data, "mock_data")

    @patch('aiohttp.ClientSession')
    async def test_fetch_data_failure(self, MockClientSession):
        http_client = MockClientSession()
        http_client.get.return_value.__aenter__.return_value = CoroutineMock(status=403, text="Access denied")
        handler = DataFetchingHandler(http_client = http_client)

        with self.assertRaises(DataFetchError):
            await handler.fetch_data("mock_access_token")

if __name__ == '__main__':
    asynctest.main()
