import pandas as pd
import requests
from random import randint
from user_parser import*

#PARSE ABSOLUTE PATHS HERE
df_path = ""
df = pd.read_csv(df_path)

def get_item_id(row):
    name = row['name']
    name = name.replace(" ", "_")
    response = requests.get(f"http://localhost:3002/items?name={name}").json()
    try:
        print(response)
        item = response['items'][0]
    except Exception as e:
        print(f"JSON decode error: {e}")
        return None
    if len(item) == 0:
        print(f"Item {name} not found")
        return None

    return item['id']

def validate_nan(value):
    if pd.isna(value):
        return ''
    return value

def validate_use_period(value):
    if value == 'кілька годин':
        return "Кілька годин"
    elif value == 'кілька днів':
        return "Кілька днів"
    elif value == 'кілька тижнів':
        return "Кілька тижнів"
    elif value == 'кілька місяців':
        return "Кілька місяців"
    elif value == 'рік і більше':
        return "Рік і більше"

def build_data(row):
    use_period = validate_use_period(row['experience'])
    text = validate_nan(row['comment'])
    liked = validate_nan(row['liked'])
    disliked = validate_nan(row['disliked'])
    return {
        "usePeriod": use_period,
        "liked": liked,
        "disliked": disliked,
        "text": text
    }

def create_user(sign_up_url, sign_in_url):
    print("Creating user")
    user_data = generate_data()
    sign_up(user_data, sign_up_url)
    return sign_in(user_data['username'], user_data['password'], sign_in_url)

def add_review(add_url, form_data, token):
    headers = {"Authorization": "Bearer {}".format(token)}
    response = requests.post(add_url, data=form_data, headers=headers)
    print("Status code:", response.status_code)
    print("Response:", response.text)
    return response.status_code

data = create_user("http://localhost:3002/auth/signup", "http://localhost:3002/auth/signin")
token = data['token']  

for _, row in df.iterrows():
    item_id = get_item_id(row)
    print(f"Item ID: {item_id}")
    form_data = build_data(row)
    text = form_data['text']
    if item_id is None or text == '':
        continue
    add_url = f"http://localhost:3002/reviews/{item_id}"
    status = add_review(add_url, form_data, token)
    if randint(0, 10) >= 3:
        data = create_user("http://localhost:3002/auth/signup", "http://localhost:3002/auth/signin")
        token = data['token']
    while status != 201:
        data = create_user("http://localhost:3002/auth/signup", "http://localhost:3002/auth/signin")
        token = data['token']
        status = add_review(add_url, form_data, token)

