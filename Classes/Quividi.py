import http.client
import json
import urllib.parse
import requests

class Quividi:

    def __init__(self, auth):
        self.auth = auth
        self.conn = http.client.HTTPSConnection("vidicenter.quividi.com", timeout=None)
        self.headers = {
        "Authorization": f"Basic {self.auth}",
        "Cookie": "csrftoken=07ePFTLNE8GJHoqI7rkSZtLQP2wPq2AY"
        }


    def get_sites(self):
        payload = ''
        self.conn.request("GET", "/api/v1/sites/", payload, self.headers)
        res = self.conn.getresponse()
        self.confirm = json.loads(res.read().decode('utf-8'))
        # print(self.confirm)
        return self.confirm
    

    def get_data(self, datatype, start, end, locations):
        url = f"https://vidicenter.quividi.com/api/v1/data?data_type={datatype}&time_resolution=finest&start={start}&end={end}&locations={locations}"

        payload = {}

        self.response = requests.request("GET", url, headers=self.headers, data=payload).json()
        print(self.response)
        return self.response
    
    
    def get_all_alerts(self, hours=None):
        url = f"https://vidicenter.quividi.com/api/v1/alerts"
        if hours is not None:
            print(f"gathering alerts for past {hours} hours...")
            url += f"?hours={hours}"

        payload = {}

        self.response = requests.request("GET", url, headers=self.headers, data=payload).json()
        # print(self.response)
        return self.response
    

    def get_site_alerts(self, site, hours=None):
        url = f"https://vidicenter.quividi.com/api/v1/site/{site}/alerts"
        if hours is not None:
            print(f"getting alerts for past {hours} hours...")
            url += f"?hours={hours}"

        payload = {}

        self.response = requests.request("GET", url, headers=self.headers, data=payload).json()
        print(self.response)
        return self.response
    

#Example usage:

#imports and define authentication token
    # import sys
    # sys.path.append('..\\Classes')
    # from Classes.Quividi import Quividi
    # auth = '<API key>'

#define and perform login:
    # login = Quividi(auth)

#define and perform necessary calls
    # sites = login.get_sites()