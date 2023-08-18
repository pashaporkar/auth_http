import asynctest
from asynctest import CoroutineMock, patch
from auth_http.exceptions import AuthorizationError
from auth_http.client import Client


class TestClient(asynctest.TestCase):

    @patch('auth_http.handlers.AuthorizationHandler')
    async def test_successful_request(self, MockAuthorizationHandler):
        """
        Test the successful processing of a client request.

        This test simulates the client processing a successful request where the handlers return valid data.

        :param MockAuthorizationHandler: Mocked AuthorizationHandler class.
        """
        async def fake_handle_request(user_name, password):
            return "mock_data"

        mock_auth_handler_instance = MockAuthorizationHandler.return_value
        mock_auth_handler_instance.handle_request = CoroutineMock(side_effect=fake_handle_request)

        client = Client(authorization_handler=mock_auth_handler_instance)

        result = await client.process_request("mock_user_name", "mock_password")

        self.assertEqual(result, "mock_data")

    @patch('auth_http.handlers.AuthorizationHandler')
    async def test_authorization_error(self, MockAuthorizationHandler):
        """
        Test handling an authorization error.

        This test checks the scenario where the authorization handler raises an AuthorizationError.

        :param MockAuthorizationHandler: Mocked AuthorizationHandler class.
        """
        mock_auth_handler_instance = MockAuthorizationHandler.return_value
        mock_auth_handler_instance.handle_request.side_effect = AuthorizationError("Authorization failed")

        client = Client(authorization_handler=mock_auth_handler_instance)

        result = await client.process_request("mock_user_name", "mock_password")

        self.assertEqual(result, "Authorization failed")

if __name__ == '__main__':
    asynctest.main()
