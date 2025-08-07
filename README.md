# RateMe Parsers

## Overview

RateMe Parsers is a collection of scripts created in order to parse items/users/reviews data if you are starting our [RateMe](https://github.com/showemeowkx/RateMe) application fresh on a new device. Basically an additional helping terminal tool.

## Dependencies

- Python 3.10 or higher
- Account on a local RateMe
- Running RateMe backend server

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/showemeowkx/RateMe-Parsers
   cd RateMe-Parsers
   ```

2. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install requirements:

   ```bash
   pip install -r requirements.txt
   ```

4. Create an environment file in the root directory (`./.env`).
5. Configure the environment file:

   ```bash
   #Host where the app is running
   HOST = [DEFAULT: localhost]
   #Port where the backend is running
   PORT = [DEFAULT: 3001]
   #Path to a default item image
   DEFAULT_PATH = [DEFAULT: ./public/item_default.jpg]
   #Path to a temporary directory
   TEMP_PATH = [DEFAULT: ./public/temp/]
   #Path to a dataframe .csv file
   DF_PATH = [DEFAULT: ./public/reviews_marked_iphone.csv]
   #Path to a JSON file for storing data
   JSON_PATH = [DEFAULT: ./data/items.json]
   #Your login for RateMe account
   LOGIN = [REQUIRED]
   #Your password for RateMe account
   PASSWORD = [REQUIRED]
   #Name of a category, where the items will be parsed
   CATEGORY = [DEFAULT: phones]
   #A value between 0 to 10 that determines whether a new user will be created on parsing a review
   CHANCE = [DEFAULT: 3]
   ```

## Usage

1. Launch the RateMe application ([RateMe README](https://github.com/showemeowkx/RateMe?tab=readme-ov-file#-getting-started)).
2. Run the main file in another terminal:

   ```bash
   python main.py
   ```

3. Follow the instructions from the terminal.

## Contributing

Feel free to open issues or submit pull requests.
