import requests


class UserNotFoundError(Exception):
    pass

def get_info_about_user(username: str):
    url = f"https://leetcode-stats-api.herokuapp.com/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    raise UserNotFoundError(f"Пользователь '{username}' не найден.")



