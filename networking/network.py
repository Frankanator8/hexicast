import requests
class Networking:
    def __init__(self, url):
        self.url = url

    def get(self, path, **params):
        data = requests.get(f"{self.url}/{path}", params=params)
        return data.json()

    def post(self, path, data):
        data = requests.post(f"{self.url}/{path}", data=data)
        return data.json()
