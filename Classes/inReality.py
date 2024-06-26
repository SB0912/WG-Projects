import http.client
import json
from flask import request_started
import requests
import csv
import time

class inReality:

    def __init__(self):
        self.conn = http.client.HTTPSConnection("api.inreality.com", timeout=None)
        self.headers = {}

    def getStores(self, auth):
        payload = ''
        self.conn.request("GET", f"/v3.1/stores?api_key={auth}", payload, self.headers)
        res = self.conn.getresponse()
        self.confirm = json.loads(res.read().decode('utf-8'))
        print(self.confirm)
        return self.confirm


    def getDemographics(self, auth):
        url = f"https://api.inreality.com/v3.1/data/correlated/demographics/csv?api_key={auth}"
        payload = {}
        content = []
        try:
            response = requests.get(url, payload)
            if response.text:
                content.append(response.text)
                # print(content)
                return content
            response = requests.get(url, payload)
        except requests.RequestException as e:
            raise SystemExit(f"API Request failed: {e}")
        
#Example usage:

#imports and define authentication token
    # import sys
    # sys.path.append('..\\Classes')
    # from Classes.inReality import inReality
    # auth = '<API key>'

#define and perform login:
    # login = inReality()

#define and perform necessary calls
    # connections = login.getStores(auth)