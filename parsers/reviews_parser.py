import pandas as pd
import requests
import os
import logging
import sys
import json
from random import randint
from parsers.user_parser import UserParser

logging.basicConfig(level=logging.INFO)

class ReviewsParser():
    def __init__(self, host, port, json_path, df_path):
        self.base_url = f"http://{host}:{port}/reviews/"
        self.json_path = json_path
        self.df_path = df_path
        self.headers = {}
        self.items_dict = None
        self.user_parser = UserParser(host, port)
        self.df = None

    def init_df(self):
        logging.info("Initializing dataframe...")
        try:
            self.df = pd.read_csv(self.df_path)
            logging.info("Dataframe initialized successfully.")
        except Exception as e:
            logging.error("Failed to initialize dataframe: %s", e)
            logging.info("Exiting with 1...")
            sys.exit(1)

    def init_json(self):
        logging.info("Initializing JSON file...")

        if not os.path.exists(self.json_path):
            logging.error("Failed to initialize JSON: File does not exist")
            logging.info("Exiting with 1...")
            sys.exit(1)

        try:
            with open(self.json_path, 'r') as f:
                json_data = json.load(f)

            if len(json_data) < 1 or json_data is None:
                logging.error("Failed to initialize JSON: File is empty or broken")
                logging.info("Exiting with 1...")
                sys.exit(1)

            self.items_dict = json_data

            logging.info("JSON file initialized successfully. Data saved.")
        except Exception as e:
            logging.error("Failed to add data to JSON: %s", e)
            logging.info("Exiting with 1...")
            sys.exit(1)

    def validate_nan(self, value):
        if pd.isna(value):
            return ''
        return value

    def build_data(self, data):
        logging.info("Validating and building data...")

        use_period = self.validate_nan(data['experience']).capitalize()
        text = self.validate_nan(data['comment'])
        liked = self.validate_nan(data['liked'])
        disliked = self.validate_nan(data['disliked'])

        logging.info("Form data built successfully.")

        return {
            "usePeriod": use_period,
            "liked": liked,
            "disliked": disliked,
            "text": text
        }

    def send_post(self, url, form_data):
        logging.info(f"Sending POST request to <{url}>...")
        try:
            response = requests.post(url, data=form_data, headers=self.headers)
            status = response.status_code
            logging.info(f"Add review response status code: {status}")

            if status >= 300:
                logging.error("Failed to add a review: Bad response received from server")
                logging.info("Response: %s", response.text)

                cont = input("Continue operations?\n[Y] - Yes\n[N] - No\n").lower()
                if cont != "y":
                    if cont != "n":
                        logging.warning("Invalid input, proceeding exit...")
                    logging.info("Exiting with 0...")
                    sys.exit(0)

                logging.info("Continuing...")
                return status
            else:
                logging.info("Review added successfully.")
                return status

        except Exception as e:
            logging.error("Failed to add a review: %s", e)
            logging.info("Exiting with 1...")
            sys.exit(1)

    def find_item_id(self, item_name):
        logging.info("Searching for item id by name...")
        try:
            return self.items_dict[item_name]
        except Exception:
            return -1


    def add_reviews(self, chance):
        token = self.user_parser.create_user()
        self.headers["Authorization"] = f"Bearer {token}"

        for _, row in self.df.iterrows():
            logging.info("Adding an item...")
            item_id = self.find_item_id(row['name'])

            if item_id == -1:
                logging.warning("Failed to find an item id: Item not found")

                cont = input("Continue operations?\n[Y] - Yes\n[N] - No\n").lower()
                if cont != "y":
                    if cont != "n":
                        logging.warning("Invalid input, proceeding exit...")
                    logging.info("Exiting with 0...")
                    sys.exit(0)

                logging.info("Continuing...")
                continue

            logging.info(f"Item found. Item id: {item_id}")

            form_data = self.build_data(row)
            text = form_data['text']

            if text == '':
                logging.warning("Invalid text filed data. Ignoring...")
                continue

            add_url = self.base_url + item_id
            status = self.send_post(add_url, form_data)

            if randint(0, 10) >= chance:
                logging.info("Lucky point! Changing user credentials...")
                token = self.user_parser.create_user()
                self.headers["Authorization"] = f"Bearer {token}"
                
            while status != 201:
                logging.warning("Failed to add a review. Retrying for a new user...")
                token = self.user_parser.create_user()
                self.headers["Authorization"] = f"Bearer {token}"
                status = self.send_post(add_url, form_data)

            logging.info("All reviews added successfully.")

    def main(self, chance):
        logging.info("Starting reviews parsing process...")

        if chance not in range(1, 11):
            logging.error("Wrong <chance> value. Should be between 1 and 10.")
            logging.info("Exiting with 1...")
            sys.exit(1)

        self.init_df()
        self.init_json()
        self.add_reviews(chance)

        logging.info("Reviews parsing process finished successfully.")