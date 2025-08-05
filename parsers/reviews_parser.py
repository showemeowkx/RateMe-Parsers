import pandas as pd
import requests
import os
import sys
import json
from random import randint
from parsers.user_parser import UserParser

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logger import Logger

class ReviewsParser():
    def __init__(self, host, port, json_path, df_path):
        self.base_url = f"http://{host}:{port}/reviews/"
        self.json_path = json_path
        self.df_path = df_path
        self.headers = {}
        self.items_dict = None
        self.user_parser = UserParser(host, port)
        self.logger = Logger("ReviewsParser")
        self.df = None

    def init_df(self):
        self.logger.info("Initializing dataframe...")
        try:
            self.df = pd.read_csv(self.df_path)
            self.logger.info("Dataframe initialized successfully.")
        except Exception as e:
            self.logger.error_and_exit(f"Failed to initialize dataframe: {e}", 1)

    def init_json(self):
        self.logger.info("Initializing JSON file...")

        if not os.path.exists(self.json_path):
            self.logger.error_and_exit("Failed to initialize JSON: File does not exist", 1)

        try:
            with open(self.json_path, 'r') as f:
                json_data = json.load(f)

            if len(json_data) < 1 or json_data is None:
                self.logger.error_and_exit("Failed to initialize JSON: File is empty or broken", 1)

            self.items_dict = json_data

            self.logger.info("JSON file initialized successfully. Data saved.")
        except Exception as e:
            self.logger.error_and_exit(f"Failed to add data to JSON: {e}", 1)

    def validate_nan(self, value):
        if pd.isna(value):
            return ''
        return value

    def build_data(self, data):
        self.logger.info("Validating and building data...")

        use_period = self.validate_nan(data['experience']).capitalize()
        text = self.validate_nan(data['comment'])
        liked = self.validate_nan(data['liked'])
        disliked = self.validate_nan(data['disliked'])

        self.logger.info("Form data built successfully.")

        return {
            "usePeriod": use_period,
            "liked": liked,
            "disliked": disliked,
            "text": text
        }

    def send_post(self, url, form_data):
        self.logger.info(f"Sending POST request to <{url}>...")
        try:
            response = requests.post(url, data=form_data, headers=self.headers)
            status = response.status_code
            self.logger.info(f"Add review response status code: {status}")

            if status >= 300:
                self.logger.error("Failed to add a review: Bad response received from server")
                self.logger.info("Response: %s", response.text)

                cont = input("Continue operations?\n[Y] - Yes\n[N] - No\n").lower()
                if cont != "y":
                    if cont != "n":
                        self.logger.warning("Invalid input, proceeding exit...")
                    self.logger.info("Exiting with 0...")
                    sys.exit(0)

                self.logger.info("Continuing...")
                return status
            else:
                self.logger.info("Review added successfully.")
                return status

        except Exception as e:
            self.logger.error_and_exit(f"Failed to add a review: {e}", 1)

    def find_item_id(self, item_name):
        self.logger.info("Searching for item id by name...")
        try:
            return self.items_dict[item_name]
        except Exception:
            return -1


    def add_reviews(self, chance):
        token = self.user_parser.create_user()
        self.headers["Authorization"] = f"Bearer {token}"

        for _, row in self.df.iterrows():
            self.logger.info("Adding an item...")
            item_id = self.find_item_id(row['name'])

            if item_id == -1:
                self.logger.warning("Failed to find an item id: Item not found")

                cont = input("Continue operations?\n[Y] - Yes\n[N] - No\n").lower()
                if cont != "y":
                    if cont != "n":
                        self.logger.warning("Invalid input, proceeding exit...")
                    self.logger.info("Exiting with 0...")
                    sys.exit(0)

                self.logger.info("Continuing...")
                continue

            self.logger.info(f"Item found. Item id: {item_id}")

            form_data = self.build_data(row)
            text = form_data['text']

            if text == '':
                self.logger.warning("Invalid text filed data. Ignoring...")
                continue

            add_url = self.base_url + item_id
            status = self.send_post(add_url, form_data)

            if randint(0, 10) >= chance:
                self.logger.info("Lucky point! Changing user credentials...")
                token = self.user_parser.create_user()
                self.headers["Authorization"] = f"Bearer {token}"
                
            while status != 201:
                self.logger.warning("Failed to add a review. Retrying for a new user...")
                token = self.user_parser.create_user()
                self.headers["Authorization"] = f"Bearer {token}"
                status = self.send_post(add_url, form_data)

            self.logger.info("All reviews added successfully.")

    def main(self, chance):
        self.logger.info("Starting reviews parsing process...")

        self.init_df()
        self.init_json()
        self.add_reviews(chance)

        self.logger.info("Reviews parsing process finished successfully.")