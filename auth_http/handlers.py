import base64
from auth_http.exceptions import AuthorizationError, DataFetchError
from settings import settings

class Handler:
    """
    Base class for handling requests in the chain.
    """
    def __init__(self, successor=None):
        """
        Initialize the handler.

        :param successor: The next handler in the chain.
        """
        self._successor = successor

    async def handle_request(self, **kwargs):
        """
        Handle the request. If a successor exists, delegate the request.

        :param kwargs: Additional keyword arguments.
        :return: Result of the request handling.
        """
        if self._successor:
            return await self._successor.handle_request(**kwargs)
        return None

class AuthorizationHandler(Handler):
    """
    Handler for authenticating the client.
    """
    def __init__(self, http_client, successor=None):
        """
        Initialize the AuthorizationHandler.

        :param http_client: An aiohttp.ClientSession object.
        :param successor: The next handler in the chain.
        """
        super().__init__(successor) 
        self._http_client = http_client

    async def handle_request(self, user_name, password, **kwargs):
        """
        Handle authentication request. If successful, delegate to the successor.

        :param user_name: Client's username.
        :param password: Client's password.
        :param kwargs: Additional keyword arguments.
        :return: Result of the request handling.
        :raises AuthorizationError: If authentication fails.
        """
        try:
            access_token = await self.authenticate(user_name, password)
            if access_token:
                kwargs['access_token'] = access_token
                return await super().handle_request(**kwargs)
            raise AuthorizationError("Authentication failed")
        except Exception as e:
            raise AuthorizationError(e) from e

    async def authenticate(self, user_name, password):
        """
        Authenticate the client using the mock authentication server.

        This function sends a request to the mock authentication server to authenticate the client.
        It encodes the header using base64.

        :param user_name: The client username.
        :param password: The client password.
        :return: The access token if authentication is successful, otherwise an AuthorizationError.
        """
        auth_server_url = "http://" + settings.AUTHORIZATION_HOST\
        + ":" + str(settings.AUTHORIZATION_PORT)\
        + settings.AUTHORIZATION_ENDPOINT
        headers = {"Authorization": self._create_basic_auth_header(user_name, password)}

        try:
            async with self._http_client.post(auth_server_url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["access_token"]
                elif response.status == 401:
                    raise AuthorizationError("Authentication failed")
                else:
                    raise AuthorizationError(response.status)
        except Exception as e:
            raise AuthorizationError("Authentication request failed") from e

    def _create_basic_auth_header(self, user_name, password):
        """
        Create a Basic Authentication header using the provided client credentials.

        :param user_name: The client username.
        :param password: The client password.
        :return: The Basic Authentication header value.
        """
        credentials = f"{user_name}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode('utf8')).decode('utf8')
        return f"Basic {encoded_credentials}"

class DataFetchingHandler(Handler):
    """
    Handler for fetching data.
    """
    def __init__(self, http_client, successor=None):
        """
        Initialize the DataFetchingHandler.

        :param http_client: An aiohttp.ClientSession object.
        :param successor: The next handler in the chain.
        """
        super().__init__(successor)
        self.http_client = http_client

    async def handle_request(self, access_token):
        """
        Handle data fetching request.

        :param access_token: Access token for authorization.
        :param kwargs: Additional keyword arguments.
        :return: Fetched data.
        :raises DataFetchError: If data fetching fails.
        """
        try:
            data = await self.fetch_data(access_token)
            return data
        except Exception as e:
            raise DataFetchError("Data fetching failed") from e

    async def fetch_data(self, access_token):
        """
        Fetch data using access token.

        :param access_token: Access token for authorization.
        :return: Fetched data.
        :raises DataFetchError: If data fetching fails.
        """
        resource_api_url = "http://" + settings.API_HOST\
        + ":" + str(settings.API_PORT)\
        + settings.API_ENDPOINT
        headers = {"Authorization": f"Bearer {access_token}"}
        async with self.http_client.get(resource_api_url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data['data']
            else:
                    raise DataFetchError("Error fetching data")


