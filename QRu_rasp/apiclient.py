import requests

class APIClient():
    def __init__(self, api_key, api_url):
        self.api_key = api_key
        self.api_url = api_url

    def verify_token(self, token):
        payload = {'key': self.api_key, 'token': token}
        resp = requests.post(self.api_url, json=payload)
        if resp.status_code == 200:
            return True
        else:
            return False
