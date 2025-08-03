from parsers.items_parser import ItemsParser
from parsers.reviews_parser import ReviewsParser

from dotenv import load_dotenv
import os
import logging
import sys

load_dotenv()

# TODO: Add config validation
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DEFAULT_PATH = os.getenv("DEFAULT_PATH")
TEMP_PATH = os.getenv("TEMP_PATH")
JSON_PATH = os.getenv("JSON_PATH")
DF_PATH = os.getenv("DF_PATH")
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")
CATEGORY = os.getenv("CATEGORY")
CHANCE = int(os.getenv("CHANCE"))

items_parser = ItemsParser(HOST, PORT, DEFAULT_PATH, JSON_PATH, TEMP_PATH, DF_PATH)
review_parser = ReviewsParser(HOST, PORT, JSON_PATH, DF_PATH)

order = input("Welcome to RateMe Parser! What do you need to parse today?\n[1] - items\n[2] - reviews\n[3] - both\n")

while order not in ["1", "2", "3"]:
    logging.info("Invalid input. Please follow the instructions.")
    order = input("Welcome to RateMe Parser! What do you need to parse today?\n[1] - items\n[2] - reviews\n[3] - both\n")

if order == "1":
    logging.info("---PARSING ONLY ITEMS---")
    items_parser.main(LOGIN, PASSWORD, CATEGORY)
    logging.info("---PROCESS FINISHED SUCCESSFULLY---")

elif order == "2":
    logging.info("---PARSING ONLY REVIEWS---")
    review_parser.main(CHANCE)
    logging.info("---PROCESS FINISHED SUCCESSFULLY---")

elif order == "3":
    logging.info("---PARSING ITEMS AND REVIEWS---")

    items_parser.main(LOGIN, PASSWORD, CATEGORY)

    cont = input("Continue operations?\n[Y] - Yes\n[N] - No\n").lower()
    if cont != "y":
        if cont != "n":
            logging.warning("Invalid input, proceeding exit...")
        logging.info("Exiting with 0...")
        sys.exit(0)

    logging.info("Continuing...")

    review_parser.main(CHANCE)
    logging.info("---PROCESS FINISHED SUCCESSFULLY---")
