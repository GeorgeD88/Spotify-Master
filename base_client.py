from configuration import *
import requests
import datetime
import base64
import json


class SpotifyAPI():
    client_id = None
    client_secret = None
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
    
    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        if  self.client_id == None or self.client_secret == None:
            raise Exception('You must set client_id and client_secret')
        client_creds = self.client_id + ':' + self.client_secret  # TODO: F STRING THIS BITCH
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {'Authorization': 'Basic ' + client_creds_b64.decode()}  # TODO: F STRING THIS BITCH

    def get_token_data(self):
        return {'grant_type': 'client_credentials'}

    def perform_auth(self):
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(self.token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):  # checks whether the status code is not passing
            return False
        data = r.json()
        now = datetime.datetime.now()
        self.access_token = data['access_token']
        self.access_token_expires = expires = now + datetime.timedelta(seconds=data['expires_in'])
        self.access_token_did_expire = expires < now
        return True
