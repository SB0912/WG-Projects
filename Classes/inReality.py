import http.client
import json
import requests

class inReality:

    def __init__(self):
        
        # Initializes the inReality class, setting up the HTTPS connection.
        
        self.conn = http.client.HTTPSConnection("api.inreality.com", timeout=None)
        self.headers = {}

    def getStores(self, auth):
        
        # Fetches store data from the inReality API.
        
        # :param auth: API key for authentication
        # :return: List of stores as a JSON object
        
        payload = ''
        self.conn.request("GET", f"/v3.1/stores?api_key={auth}", payload, self.headers)
        res = self.conn.getresponse()
        self.confirm = json.loads(res.read().decode('utf-8'))
        print(self.confirm)
        return self.confirm

    def getDemographics(self, auth):
        
        # Fetches demographic data from the inReality API in CSV format.
        
        # :param auth: API key for authentication
        # :return: List containing the CSV data as strings
        
        url = f"https://api.inreality.com/v3.1/data/correlated/demographics/csv?api_key={auth}"
        payload = {}
        content = []
        try:
            response = requests.get(url, payload)
            if response.text:
                content.append(response.text)
                return content
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