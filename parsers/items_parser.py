import pandas as pd
import os
import uuid
import requests

# PARSE ABSOLUTE PATHS HERE
default_abs_path = ""
temp_abs_path = ""
df_path = ""

try:
    os.mkdir(temp_abs_path)
    print(f"Directory '{temp_abs_path}' created successfully.")
except FileExistsError:
    print(f"Directory '{temp_abs_path}' already exists.")

df = pd.read_csv(df_path)

sign_in_url = "http://localhost:3001/auth/signin"

# PARSE CREDENTIALS HERE
form_data = {'login': '', 'password': ''}

response = requests.post(sign_in_url, data=form_data)

print("Sign in status: ", response.status_code)
response_json = response.json()
token = response_json['accessToken']

add_url = "http://localhost:3001/items/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Referer": "https://hotline.ua/",
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5","Authorization": "Bearer {}".format(token)}

def get_image(url, headers, default_path, temp_path):
    try:
        img_response = requests.get(url, headers=headers)
        img_response.raise_for_status()
        content = img_response.content
        img_filename = f"image{uuid.uuid4()}.jpg"
        img_path = os.path.join(temp_path, img_filename)
        with open(img_path, "wb") as file:
            file.write(content)
        print("LOADED!")
        return img_path
    except:
        return default_path
    
def send_post(url, headers, image_path, form_data):
    try:
        with open(image_path, "rb") as file:
            files = {
                "file": (os.path.basename(image_path), file, "image/jpeg")
            }
            data = form_data
            response = requests.post(url, files=files, data=data, headers=headers)
            print("Status code:", response.status_code)
            print("Response:", response.text)
        os.remove(image_path)
    except Exception as e:
        print(f"Error sending image: {e}")

def get_ratings(df):
    item_dict = {}
    for _, row in df.iterrows():
        if row['name'] not in item_dict:
            item_dict[row['name']] = {'rating': 1 if row['recommend'] == 'рекомендує цей товар' else 0, 'count': 1}
        else:
            if row['recommend'] == 'рекомендує цей товар':
                item_dict[row['name']]['rating'] += 1
                item_dict[row['name']]['count'] += 1
            else: item_dict[row['name']]['count'] += 1
        
    return item_dict

def calc_rating(item_dict):
    item_rating = {}

    for name, data in item_dict.items():
        item_rating[name] = round((data['rating'] / data['count'])*100, 2)
    
    return item_rating

used_urls = []
item_rating = calc_rating(get_ratings(df))

for _, row in df.iterrows():
    image_url = row['pic']
    if image_url not in used_urls:
        used_urls.append(image_url)
        image_load = get_image(image_url, headers, default_abs_path, temp_abs_path)
    else: print(f'[USED!] url: ${image_url}')

    form_data = {'category': 'phones', 'name': row['name'], 'link': row['link'], 'description': row['description'], "rating": item_rating[row['name']]}

    send_post(add_url, headers, image_load, form_data)  
    print("Add item status: ",response.status_code)

os.rmdir(temp_abs_path)