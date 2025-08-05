import pandas as pd
import os
import uuid
import requests
import json
import sys
from parsers.user_parser import UserParser

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logger import Logger

class ItemsParser:
    def __init__(self, host, port, default_path, json_path, temp_path, df_path):
        self.base_url = f"http://{host}:{port}/items/"
        self.default_path = default_path
        self.temp_path = temp_path
        self.df_path = df_path
        self.json_path = json_path
        self.df = None
        self.logger = Logger('ItemsParser')
        self.user_parser = UserParser(host, port)
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
            "Referer": "https://hotline.ua/",
            "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5"}

    def init_temp(self):
        self.logger.info("Creating temporary directory...")
        try:
            os.mkdir(self.temp_path)
            self.logger.info("Temporary directory created successfully.")
        except FileExistsError:
            self.logger.info("Temporary directory already exists.")
        except Exception as e:
            self.logger.error_and_exit(f"Failed to create temporary directory: {e}", 1)

    def init_df(self):
        self.logger.info("Initializing dataframe...")
        try:
            self.df = pd.read_csv(self.df_path)
            self.logger.info("Dataframe initialized successfully.")
        except Exception as e:
            self.logger.error_and_exit(f"Failed to initialize dataframe: {e}", 1)

    def init_json(self):
        if os.path.exists(self.json_path):
            self.logger.info("JSON file exists. Overwriting...")
        else:
            self.logger.info("Creating a JSON file...")

        try:
            with open(self.json_path, "w") as f:
                json.dump({}, f)

            self.logger.info("JSON file initialized successfully.")
        except Exception as e:
            self.logger.error_and_exit(f"Failed to initialize JSON: {e}", 1)

    def get_image(self, url):
        self.logger.info("Loading an image...")
        try:
            img_response = requests.get(url, headers=self.headers)
            img_response.raise_for_status()
            content = img_response.content
            img_filename = f"image{uuid.uuid4()}.jpg"
            img_path = os.path.join(self.temp_path, img_filename)
            with open(img_path, "wb") as file:
                file.write(content)
            self.logger.info("Image loaded successfully. Saved as <%s>", img_filename)
            return img_path
        except:
            self.logger.warning("Failed to load an image. Returning default one...")
            return self.default_path
        
    def add_to_json(self, data):
        self.logger.info("Adding data to JSON...")
        try:
            with open(self.json_path, 'r') as f:
                json_data = json.load(f)

            json_data.update(data)

            with open(self.json_path, 'w') as f:
                json.dump(json_data, f, indent=4)
        except Exception as e:
            self.logger.error_and_exit(f"Failed to add data to JSON: {e}", 1)
    
    def send_post(self, url, image_path, form_data):
        self.logger.info(f"Sending POST request to <{url}>...")
        try:
            with open(image_path, "rb") as file:
                files = {
                    "file": (os.path.basename(image_path), file, "image/jpeg")
                }
                response = requests.post(url, files=files, data=form_data, headers=self.headers)
                status = response.status_code
                self.logger.info(f"Add item response status code: {status}")

                if status >= 300:
                    self.logger.error("Failed to add an item: Bad response received from server")
                    self.logger.info("Response: %s", response.text)

                    cont = input("Continue operations?\n[Y] - Yes\n[N] - No\n").lower()
                    if cont != "y":
                        if cont != "n":
                            self.logger.warning("Invalid input, proceeding exit...")
                        self.logger.info("Exiting with 0...")
                        sys.exit(0)

                    self.logger.info("Continuing...")

                else:
                    response_json = response.json()
                    item_id = response_json['itemId']
                    self.add_to_json({form_data['name']: item_id})

                    self.logger.info("Item added successfully.")

            if image_path != self.default_path:
                self.logger.info("Removing image from temp directory...")
                try:
                    os.remove(image_path)
                except Exception as e:
                    self.logger.warning("Failed to remove an image: %s", e)
        except Exception as e:
            self.logger.error_and_exit(f"Failed to add an item: {e}", 1)

    def add_items(self, item_category):
        ADD_URL = self.base_url
        item_names = []

        for _, row in self.df.iterrows():
            self.logger.info("Adding an item...")

            if row['name'] not in item_names:
                item_names.append(row['name'])

                image_url = row['pic']
                image_load = self.get_image(image_url)
                form_data = {'categorySlug': item_category, 'name': row['name'], 'description': row['description']}

                self.send_post(ADD_URL, image_load, form_data)  
            else:
                self.logger.info("Found an item with the same name. Ignoring...")

        self.logger.info("All items added successfully.")
        self.logger.info("Removing temp directory...")

        try:
            os.rmdir(self.temp_path)
        except Exception as e:
            self.logger.warning("Failed to remove temp directory: %s", e)

    def main(self, login, password, item_category):
        self.logger.info("Starting items parsing process...")

        self.init_temp()
        self.init_df()
        self.init_json()
        token = self.user_parser.sign_in(login, password)
        self.headers["Authorization"] = f"Bearer {token}"
        self.add_items(item_category)

        self.logger.info("Items parsing process finished successfully.")