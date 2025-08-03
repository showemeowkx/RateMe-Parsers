from dotenv import load_dotenv
import logging
import sys
import os

load_dotenv()
logging.basicConfig(level=logging.INFO)

DEFAULT_CONFIG = {
    "HOST": "localhost",
    "PORT": 3001,
    "DEFAULT_PATH": "./public/item_default.jpg",
    "TEMP_PATH": "./public/temp",
    "JSON_PATH": "./data/items.json",
    "DF_PATH": "./public/reviews_marked_iphone.csv",
    "LOGIN": None,  # No default, required
    "PASSWORD": None,  # No default, required
    "CATEGORY": "phones",
    "CHANCE": 3
}

REQUIRED = ["LOGIN", "PASSWORD"]

def validate_config():
    config = {}
    errors = []
    
    for key, default_value in DEFAULT_CONFIG.items():
        config[key] = os.getenv(key, default_value)
    
    missing = [var for var in REQUIRED if config[var] is None]
    if missing:
        errors.append(f"Missing required configuration: {', '.join(missing)}")
    
    try:
        config["PORT"] = int(config["PORT"])
        if not (1 <= config["PORT"] <= 65535):
            errors.append("PORT must be between 1 and 65535")
    except ValueError:
        errors.append("PORT must be a valid integer")
    
    try:
        config["CHANCE"] = int(config["CHANCE"])
        if not (0 <= config["CHANCE"] <= 10):
            errors.append("CHANCE must be between 0 and 10")
    except ValueError:
        errors.append("CHANCE must be a valid integer")
    
    path_vars = ["DEFAULT_PATH", "TEMP_PATH", "JSON_PATH", "DF_PATH"]
    for path_var in path_vars:
        path = config[path_var]
        if not os.path.isabs(path):
            config[path_var] = os.path.abspath(path)
    
    if errors:
        raise ValueError("\n".join(errors))
    
    return config

try:
    config = validate_config()
    
    HOST = config["HOST"]
    PORT = config["PORT"]
    DEFAULT_PATH = config["DEFAULT_PATH"]
    TEMP_PATH = config["TEMP_PATH"]
    JSON_PATH = config["JSON_PATH"]
    DF_PATH = config["DF_PATH"]
    LOGIN = config["LOGIN"]
    PASSWORD = config["PASSWORD"]
    CATEGORY = config["CATEGORY"]
    CHANCE = config["CHANCE"]
    
except ValueError as e:
    logging.error(f"Configuration error:\n{e}")
    sys.exit(1)