import requests
import secrets
import logging
import sys
from names_generator import generate_name

logging.basicConfig(level=logging.INFO)

class UserParser :
    def __init__(self, host, port):
        self.base_url = f"http://{host}:{port}/auth/"
        self.credentials_list = []

    def generate_data(self):
        logging.info("Generating user data...")
        credentials = generate_name(style='capital')

        while credentials in self.credentials_list or len(credentials) > 20:
            logging.warning("Generated credentials are invalid. Retrying...")
            credentials = generate_name(style='capital')

        self.credentials_list.append(credentials)
        credentials = credentials.split(" ")

        name = credentials[0]
        surname = credentials[1]
        username = name.lower() + "_" + surname.lower()
        email = username.replace("_", "") + "@gmail.com"
        password = secrets.token_urlsafe(20)

        return {
            "name": name,
            "surname": surname,
            "username": username,
            "email": email,
            "password": password
        }

    def sign_up(self, data):
        SIGN_UP_URL = self.base_url + "signup"
        logging.info("Signing up...")

        try:
            response = requests.post(SIGN_UP_URL, data=data)
            status = response.status_code
            logging.info(f"Sign in response status code: {status}")

            if status >= 300:
                logging.error("Failed to sign up: Bad response received from server")
                logging.info("Response: %s", response.text)
                logging.info("Exiting with 0...")
                sys.exit(0)
        except Exception as e:
            logging.error("Failed to sign up: %s", e)
            logging.info("Exiting with 1...")
            sys.exit(1)

    def sign_in(self, login, password):
        SIGN_IN_URL = self.base_url + "signin"
        form_data = {'login': login, 'password': password}
        logging.info(f"Signing in... [login: {login}, password: {password}]")

        try:
            response = requests.post(SIGN_IN_URL, data=form_data)
            status = response.status_code
            logging.info(f"Sign in response status code: {status}")

            if status >= 300:
                logging.error("Failed to sign in: Bad response received from server")
                logging.info("Response: %s", response.text)
                logging.info("Exiting with 0...")
                sys.exit(0)

            response_json = response.json()
            logging.info("Signed in and received access token successfully.")

            return response_json['accessToken']
        except Exception as e:
            logging.error("Failed to sign in: %s", e)
            logging.info("Exiting with 1...")
            sys.exit(1)

    def create_user(self):
        logging.info('Creating a user...')

        user_data = self.generate_data()
        self.sign_up(user_data)
        token = self.sign_in(user_data['username'], user_data['password'])

        return token

