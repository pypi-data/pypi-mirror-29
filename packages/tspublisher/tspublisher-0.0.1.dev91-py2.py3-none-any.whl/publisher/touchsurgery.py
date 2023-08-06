import requests


class TouchSurgery(object):

    def __init__(self):
        self.auth_token = None

    def authorized(self):
        return bool(self.auth_token)

    def login(self, email, password):
        response = requests.post(
            'https://live.touchsurgery.com/api/v3/user/login',
            data=dict(
                email=email,
                password=password)
        )
        if response.status_code != 200:
            return

        payload = response.json()
        self.auth_token = payload['access_token']
