import http.client
import json
import requests

class Quividi:

    def __init__(self, auth):
        
        # Initializes the Quividi class with authentication details and sets up the connection and headers.
        
        # :param auth: Base64 encoded authentication string for Quividi API
        
        self.auth = auth
        self.conn = http.client.HTTPSConnection("vidicenter.quividi.com", timeout=None)
        self.headers = {
            "Authorization": f"Basic {self.auth}",
            "Cookie": "csrftoken=07ePFTLNE8GJHoqI7rkSZtLQP2wPq2AY"
        }

    def get_sites(self):
        
        # Fetches site data from Quividi API.
        
        # :return: List of sites as a JSON object
        
        payload = ''
        self.conn.request("GET", "/api/v1/sites/", payload, self.headers)
        res = self.conn.getresponse()
        self.confirm = json.loads(res.read().decode('utf-8'))
        return self.confirm

    def get_data(self, datatype, start, end, locations):
        
        # Fetches specific data from Quividi API based on datatype, start time, end time, and locations.
        
        # :param datatype: Type of data to fetch
        # :param start: Start time for data
        # :param end: End time for data
        # :param locations: Locations for which data is to be fetched
        # :return: Response data as a JSON object
        
        url = f"https://vidicenter.quividi.com/api/v1/data?data_type={datatype}&time_resolution=finest&start={start}&end={end}&locations={locations}"
        payload = {}
        self.response = requests.request("GET", url, headers=self.headers, data=payload).json()
        print(self.response)
        return self.response

    def get_all_alerts(self, hours=None):
        
        # Fetches all alerts from Quividi API. Optionally, fetches alerts from the past specified number of hours.
        
        # :param hours: Number of hours to look back for alerts (optional)
        # :return: List of alerts as a JSON object
        
        url = "https://vidicenter.quividi.com/api/v1/alerts"
        if hours is not None:
            print(f"gathering alerts for past {hours} hours...")
            url += f"?hours={hours}"
        payload = {}
        self.response = requests.request("GET", url, headers=self.headers, data=payload).json()
        return self.response

    def get_site_alerts(self, site, hours=None):
        
        # Fetches alerts for a specific site from Quividi API. Optionally, fetches alerts from the past specified number of hours.
        
        # :param site: Site ID for which to fetch alerts
        # :param hours: Number of hours to look back for alerts (optional)
        # :return: List of alerts for the specified site as a JSON object
        
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