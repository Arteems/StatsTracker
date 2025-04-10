from http.client import responses

import requests


def get_info_about_user(username: str, limit: int, offset: int):
    url = f"/x/api/v3/users/search?search={username}&limit={limit}&offset={offset}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    return None
