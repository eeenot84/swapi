import requests
from pathlib import Path


class APIRequester:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, path=''):
        base = self.base_url.rstrip('/')
        tail = path.lstrip('/')
        url = f'{base}/{tail}'
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as http_err:
            print('Возникла ошибка при выполнении запроса')
            return f'HTTP error occurred: {http_err}'
        except requests.exceptions.ConnectionError as conn_err:
            print('Возникла ошибка при выполнении запроса')
            return f'Connection error occurred: {conn_err}'
        except requests.exceptions.Timeout as timeout_err:
            print('Возникла ошибка при выполнении запроса')
            return f'Timeout error: {timeout_err}'
        except requests.exceptions.RequestException as req_err:
            print('Возникла ошибка при выполнении запроса')
            return f'Unexpected error: {req_err}'


class SWRequester(APIRequester):
    def __init__(self, base_url='https://swapi.dev/api/'):
        super().__init__(base_url)

    def get_sw_categories(self):
        response = self.get('/')
        if response:
            return response.json().keys()
        return []

    def get_sw_info(self, sw_type):
        response = self.get(sw_type + '/')
        if isinstance(response, requests.Response):
            return response.text
        return f'Error fetching data: {response}'


def save_sw_data():
    requester = SWRequester('https://swapi.dev/api')
    Path("data").mkdir(exist_ok=True)

    categories = requester.get_sw_categories()

    for category in categories:
        data = requester.get_sw_info(category)
        file_path = f'data/{category}.txt'
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(data)
