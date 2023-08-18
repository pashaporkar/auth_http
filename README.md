# Python Python DevOps Engineer Assignment

This project implements an authorization flow between a client, an Authorization Server, and a Resource API.

## Components

- `auth_server.py`: Contains the mock authorization server  to handle authentication.
- `client.py`: Contains the Client class for client-side operations.
- `exceptions.py`: Contains the error handling classes.
- `handlers.py`: Implements handling the requests using the chain of responsibility method design pattern.
- `main.py`: Runs the authentication and resource access flow.
- `resource_api.py`: Contains the mock resource API web server to handle resource retrieval.

## Scenario
First the Authorizartion server and Resource API server are started. Then client sends the username and password
to the request handler. Request handler first calls the authorization server with credentials. if the credentials are correct,
the authorization server provide an access token. Access token is passed to the resource API illustrating that the user is authorized.
If the access token belongs to a user recognized by authorization server, the "mock_data" will be returned and printed in the console.

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
for example:
```
python -m unittest tests.test_client

python -m unittest tests.test_handlers
```

## Chain of responsibility design pattern
This design pattern is suited for authentication and authorization because it promotes the idea of building a chain of handlers, each responsible for processing a specific request(or action). Each handler has the ability to process the request or delegate it to the next handler in the chain.

## Asynchronous connection
Using asynchronous connections allows handling multiple concurrent requests efficiently without blocking the execution of other tasks. Asynchronous programming in general is suited for scenarios involving network communication, such as authentication and data fetching.

## Security
In this project basic security concepts are applied. yet for a real world environment better security practices should be applied.
For instance using SSL. 




   
   
