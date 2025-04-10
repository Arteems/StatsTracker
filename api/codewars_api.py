import requests


def get_user_info(username: str):
    url = f"https://www.codewars.com/api/v1/users/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    return None
