import requests
import secrets
from names_generator import generate_name

credentials_list = []

def generate_data():
    credentials = generate_name(style='capital').split(" ")
    while credentials in credentials_list:
        print("ALREADY EXISTS")
        credentials = generate_name(style='capital').split(" ")
    credentials_list.append(credentials)
    name = credentials[0]
    surname = credentials[1]
    username = credentials[0].lower() + "_" + credentials[1].lower()
    email = username.replace("_", "") + "@gmail.com"
    password = secrets.token_urlsafe(20)
    data = {
        "name": name,
        "surname": surname,
        "username": username,
        "email": email,
        "password": password
    }
    return data

def sign_up(data, url):
    response = requests.post(url, data=data)
    print("Sign up status code:", response.status_code)
    print("Response:", response.text)

def sign_in(username, password, url):
    data = {'login': username, 'password': password}
    response = requests.post(url, data=data)
    token = response.json()['accessToken']
    output = {'token': token, 'status_code': response.status_code}
    print("Sign in status code:", output['status_code'])
    return output
