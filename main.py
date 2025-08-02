from parsers.items_parser import ItemsParser

from dotenv import load_dotenv
import os

load_dotenv()

# TODO: Add config validation
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DEFAULT_PATH = os.getenv("DEFAULT_PATH")
TEMP_PATH = os.getenv("TEMP_PATH")
DF_PATH = os.getenv("DF_PATH")

items_parser = ItemsParser(HOST, PORT, DEFAULT_PATH, TEMP_PATH, DF_PATH)

items_parser.main("", "", "phones")