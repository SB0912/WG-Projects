import http.client
import json
import urllib.parse
import requests

class GoZone:

    def __init__(self):
        
        # Initializes the GoZone class, setting up the HTTPS connection.
        
        self.conn = http.client.HTTPSConnection("api-usb.smartwifiplatform.com", timeout=None)
        self.headers = {}

    def getConnections(self, auth, start, end):
        
        # Fetches connection data from the GoZone API within a specified time range.
        
        # :param auth: API token for authentication
        # :param start: Start date for fetching connection data
        # :param end: End date for fetching connection data
        # :return: List of connections as a JSON object
        
        payload = ''
        self.conn.request("GET", f"/v2/client/connections?api_token={auth}&from={start}&to={end}", payload, self.headers)
        res = self.conn.getresponse()
        self.confirm = json.loads(res.read().decode('utf-8'))
        print(self.confirm)
        return self.confirm

    def getHotSpots(self, auth):
        
        # Fetches hotspot data from the GoZone API.
        
        # :param auth: API token for authentication
        # :return: List of hotspots as a JSON object
        
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