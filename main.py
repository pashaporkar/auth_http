import asyncio
from aiohttp import ClientSession, web
from auth_http.handlers import AuthorizationHandler, DataFetchingHandler
from auth_http.client import Client
from auth_http.mock_auth_server import app as auth_app
from auth_http.mock_resource_api import app as resource_api_app
from settings import settings

#Defining runners for authorization server and resource API
auth_server_runner = web.AppRunner(auth_app)
resource_api_runner = web.AppRunner(resource_api_app)

async def main():
    await run_servers()
    async with ClientSession() as http_client:
        data_handler = DataFetchingHandler(http_client=http_client)
        auth_handler = AuthorizationHandler(http_client=http_client, successor = data_handler)
        client = Client(authorization_handler = auth_handler)

        result = await client.process_request(settings.USER_NAME, settings.PASSWORD)
        print("Successfully received: " + result)
        #Stop handling all servers and cleanup used resources.
        await auth_server_runner.cleanup()
        await resource_api_runner.cleanup()

async def run_servers():
    """
    Run the authorization server and resource API servers.

    This function sets up and starts the authorization server and resource API servers.

    :return: None
    """
    await auth_server_runner.setup()
    auth_site = web.TCPSite(auth_server_runner, settings.AUTHORIZATION_HOST, settings.AUTHORIZATION_PORT)
    await auth_site.start()

    await resource_api_runner.setup()
    resource_api_site = web.TCPSite(resource_api_runner, settings.API_HOST, settings.API_PORT)
    await resource_api_site.start()

if __name__ == "__main__":
    asyncio.run(main(),
    debug=settings.DEBUG_MODE)