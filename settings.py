from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "CERN run DB"
    DEBUG_MODE: bool = True

    # authorization Server Settings
    AUTHORIZATION_HOST: str = "localhost"
    AUTHORIZATION_PORT: int = 8080
    AUTHORIZATION_ENDPOINT : str = "/authenticate"

    # resource API Settings
    API_HOST: str = "localhost"
    API_PORT: int = 8081
    API_ENDPOINT : str = "/get_data"

    # user Credentials
    USER_NAME: str = "ABNAMRO"
    PASSWORD: str = "ABNAMRO"
    # Mock database storing hashed client secrets
    # Ideally this should be stored securely in a database.
    AUTH_CREDENTIALS: dict = {
    'ABNAMRO': {
        'salt': b'g\x12/8\xb8dY\x8c\xc7\xf0}\xc7\xc0\x81\xd0\x82',
        'hash': '91a290de1508b81b91ef2d017f3f06487130028c9c6af239564c9fcaacf33f00'
        }
    }

    # shared secret key for JWT
    JWT_SECRET_KEY: str = "iNzszLnvWXALoVicnqCVViIB3CjPy65Q"

settings = Settings()
