import requests
import json
from websockets.sync.client import connect
import certifi
import ssl

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())

class Networking:
    def __init__(self, url, wsUrl):
        self.url = url
        self.wsUrl = wsUrl

        self.websocket = None

    def get(self, path, **params):
        data = requests.get(f"{self.url}/{path}", params=params)
        return data.json()

    def post(self, path, data):
        data = requests.post(f"{self.url}/{path}", json=data)
        return data.json()

    def connect(self):
        self.websocket = connect(self.wsUrl, ssl_context=ssl.SSLContext(ssl.PROTOCOL_TLS))

    def sendWS(self, data):
        if self.websocket is not None:
            self.websocket.send(json.dumps(data))
            res = json.loads(self.websocket.recv())
            return res


    def close(self):
        if self.websocket is not None:
            self.websocket.close()
