import http.client
import json
import urllib.parse
import requests

class GoZone:

    def __init__(self):
        self.conn = http.client.HTTPSConnection("api-usb.smartwifiplatform.com", timeout=None)
        self.headers = {}

    def getConnections(self, auth, start, end):
        payload = ''
        self.conn.request("GET", f"/v2/client/connections?api_token={auth}&from={start}&to={end}", payload, self.headers)
        res = self.conn.getresponse()
        self.confirm = json.loads(res.read().decode('utf-8'))
        print(self.confirm)
        return self.confirm
    
    def getHotSpots(self, auth):
        payload = ''
        self.conn.request("GET", f"/v2/zapier/client/dropdown/hotspots?api_token={auth}", payload, self.headers)
        res = self.conn.getresponse()
        self.confirm = json.loads(res.read().decode('utf-8'))
        print(self.confirm)
        return self.confirm
    
#Example usage:

#imports and define authentication token
    # import sys
    # sys.path.append('..\\Classes')
    # from Classes.GoZone import GoZone
    # auth = '<API key>'

#define and perform login:
    # login = GoZone()

#define and perform necessary calls
    # connections = login.getConeections(auth)