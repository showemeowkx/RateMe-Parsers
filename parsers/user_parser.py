import requests
import secrets
import sys
import os
from names_generator import generate_name

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logger import Logger

class UserParser :
    def __init__(self, host, port):
        self.base_url = f"http://{host}:{port}/auth/"
        self.credentials_list = []
        self.logger = Logger('UserParser')

    def generate_data(self):
        self.logger.info("Generating user data...")
        credentials = generate_name(style='capital')

        while credentials in self.credentials_list or len(credentials) > 20:
            self.logger.warning("Generated credentials are invalid. Retrying...")
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
        self.logger.info("Signing up...")

        try:
            response = requests.post(SIGN_UP_URL, data=data)
            status = response.status_code
            self.logger.info(f"Sign up response status code: {status}")

            if status >= 300:
                self.logger.warning("Failed to sign up: Bad response received from server")
                self.logger.info("Response: %s", response.text)
                self.logger.info("Retrying...")
            else:
                self.logger.info("Signed up successfully.")

            return status
        except Exception as e:
            self.logger.error_and_exit(f"Failed to sign up: {e}", 1)

    def sign_in(self, login, password):
        SIGN_IN_URL = self.base_url + "signin"
        form_data = {'login': login, 'password': password}
        self.logger.info(f"Signing in... [login: {login}, password: {password}]")

        try:
            response = requests.post(SIGN_IN_URL, data=form_data)
            status = response.status_code
            self.logger.info(f"Sign in response status code: {status}")

            if status >= 300:
                self.logger.error_and_exit(f"Failed to sign in: Bad response received from server\nResponse: {response.text}", 0)

            response_json = response.json()
            self.logger.info("Signed in and received access token successfully.")

            return response_json['accessToken']
        except Exception as e:
            self.logger.error_and_exit(f"Failed to sign in: {e}", 1)

    def create_user(self):
        self.logger.info('Creating a user...')

        user_data = self.generate_data()
        status = self.sign_up(user_data)

        while status != 201:
            user_data = self.generate_data()
            status = self.sign_up(user_data)

        token = self.sign_in(user_data['username'], user_data['password'])

        return token

