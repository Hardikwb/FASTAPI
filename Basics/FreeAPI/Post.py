import requests

url = "https://api.freeapi.app/api/v1/users/register"

payload = {
    "email": "user.email@domain.com",
    "password": "test@123",
    "role": "ADMIN",
    "username": "doejohn"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())