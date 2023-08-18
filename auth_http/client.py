from auth_http.exceptions import AuthorizationError, DataFetchError

class Client:
    """
    Client class responsible for initiating the chain of responsibility.
    """
    def __init__(self, authorization_handler):
        """
        Initialize the client.

        :param authorization_handler: An instance of AuthorizationHandler.
        """
        self._handler_chain = authorization_handler

    async def process_request(self, user_name, password):
        """
        Process the client's request.

        :param user_name: User's name.
        :param password: User's password.
        :return: Result of the request processing.
        """
        try:
            data = await self._handler_chain.handle_request(user_name, password)
            return data
        except AuthorizationError as auth_error:
            return str(auth_error)
        except DataFetchError as fetch_error:
            return str(fetch_error)
