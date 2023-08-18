# Python DevOps Engineer Assignment

This project implements an authorization flow between a client, an Authorization Server, and a Resource API.

## Components

- `auth_server.py`: Contains the mock authorization server  to handle authentication.
- `client.py`: Contains the Client class for client-side operations.
- `exceptions.py`: Contains the error handling classes.
- `handlers.py`: Implements handling the requests using the chain of responsibility method design pattern.
- `main.py`: Runs the authentication and resource access flow.
- `resource_api.py`: Contains the mock resource API webserver to handle resource retrieval.
- `settings.py`: contains essential constants and configuration including mocking database behavoir.

## Success Scenario
First, the Authorization server and Resource API server are started. Then client sends the username and password
to the request handler. The request handler calls the authorization server with credentials. if the credentials are correct,
the authorization server provides an access token. The access token is used by resource API to check that the user is authorized.
If the access token belongs to a user recognized by resource API, the "mock_data" will be returned and printed in the console.

## Prequitise
This project is compatible with Python versions 3.7 and above.

## Setup and Usage

1. Clone this repository to your local machine.
2. Set up a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run the main script: `python main.py`

## Testing

Run unit tests using the following command:
```
python -m unittest tests.test_components
```
possible tests:
```
python -m unittest tests.test_client
python -m unittest tests.test_handlers
python -m unittest tests.test_auth_server
python -m unittest tests.test_resource_api
```

## Chain of responsibility design pattern
This design pattern is suited for authentication and authorization because it promotes the idea of building a chain of handlers, each responsible for processing a specific request(or action). Each handler has the ability to process the request or delegate it to the next handler in the chain.

## Asynchronous connection
Using asynchronous connections allows handling multiple concurrent requests efficiently without blocking the execution of other tasks. Asynchronous programming is generally suited for scenarios involving network communication, such as authentication and data fetching.

## Security
In this project, basic security concepts are applied. JWT secret key is used to sign and verify the access token. SHA256 encoding plus a unique salt per user is used for hashing the password. yet for a real-world environment better security practices should be applied such as using SSL. 




   
   
