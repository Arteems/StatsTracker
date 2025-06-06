import requests


class UserNotFoundError(Exception):
    pass

def get_user_info(username: str):
    url = f"https://www.codewars.com/api/v1/users/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    raise UserNotFoundError(f"Пользователь '{username}' не найден.")


