import requests

# Замените URL на адрес вашего Flask-приложения
base_url = 'http://127.0.0.1:5000'

# GET запрос
response_get = requests.get(f'{base_url}/get_form')
print('GET Response:', response_get.text)

# POST запрос
data = {
    'f_name1': 'John',
    'value1': '+7 999 123 45 67',
    'f_name2': 'email@example.com',
    'value2': '01.01.2000'
}

response_post = requests.post(f'{base_url}/get_form', data=data)
print('POST Response:', response_post.text)