from parsers.items_parser import ItemsParser
from parsers.reviews_parser import ReviewsParser
from config import *
import sys

items_parser = ItemsParser(HOST, PORT, DEFAULT_PATH, JSON_PATH, TEMP_PATH, DF_PATH)
review_parser = ReviewsParser(HOST, PORT, JSON_PATH, DF_PATH)

order = input("Welcome to RateMe Parser! What do you need to parse today?\n[1] - items\n[2] - reviews\n[3] - both\n")

while order not in ["1", "2", "3"]:
    print("Invalid input. Please follow the instructions.")
    order = input("Welcome to RateMe Parser! What do you need to parse today?\n[1] - items\n[2] - reviews\n[3] - both\n")

if order == "1":
    print("---PARSING ONLY ITEMS---")
    items_parser.main(LOGIN, PASSWORD, CATEGORY)
    print("---PROCESS FINISHED SUCCESSFULLY---")

elif order == "2":
    print("---PARSING ONLY REVIEWS---")
    review_parser.main(CHANCE)
    print("---PROCESS FINISHED SUCCESSFULLY---")

elif order == "3":
    print("---PARSING ITEMS AND REVIEWS---")

    items_parser.main(LOGIN, PASSWORD, CATEGORY)

    cont = input("Continue operations?\n[Y] - Yes\n[N] - No\n").lower()
    if cont != "y":
        if cont != "n":
            print("Invalid input, proceeding exit...")
        print("Exiting with 0...")
        sys.exit(0)

    print("Continuing...")

    review_parser.main(CHANCE)
    print("---PROCESS FINISHED SUCCESSFULLY---")
