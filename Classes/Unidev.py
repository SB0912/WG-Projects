import http.client
import json
from random import randrange
import time
import datetime
from datetime import datetime, timedelta, timezone, date
import os


class Unidev:
    def __init__(self, api_key, payload):
        self.api_key = api_key
        self.username = os.environ.get('labyrinthDTUsername')
        self.password = os.environ.get('labyrinthDTPassword')
        self.payload = payload
        self.conn = http.client.HTTPConnection('unidev.thewirelessguardian.net')
        self.headers = None

    def login(self):
        self.conn.request("POST", f"/users/login?user=" + self.username + "&pass=" + self.password, self.payload, {})
        res = self.conn.getresponse()
        confirm = json.loads(res.read().decode('utf-8'))
        print('Successful Login')
        self.headers = {'x-sentinel': confirm['token']}
        return self.headers

    def get_devices(self):
        self.conn.request("GET", f"/devices/search", self.payload, self.headers)
        res = self.conn.getresponse()
        confirm = json.loads(res.read().decode('utf-8'))
        return confirm
    
    def get_device_logs(self, sn):
        # numOfOfflineLogs = 0
        while True:
            try:
                self.conn.request("GET", f"/devices/sn/" + sn + "/logs", self.payload, self.headers)
                res = self.conn.getresponse()
                confirm = json.loads(res.read().decode('utf-8'))
                return 
            
                # for row in confirm:
                #     if row['msg'] == '!!! Device lost power !!!':
                #         date = datetime.strptime(convert(row['time']), '%Y-%m-%d %H:%M:%S')

                #         # If the log date is within 5 days
                #         if datetime.now() - date <= timedelta(hours=120):
                #             numOfOfflineLogs += 1
                # if res.status == 404:
                #     return 0
                # else:
                #     return numOfOfflineLogs

            except Exception as e:
                print(f"An error occurred: {e}")
                time.sleep(randrange(1, 3))

    
    def get_device_status_ts(self, sn):
        while True:
            try:
                self.conn.request("GET", f"/devices/sn/" + sn + "/status", self.payload, self.headers)
                res = self.conn.getresponse()
                confirm = json.loads(res.read().decode('utf-8'))

                if res.status == 404:
                    return 0
                else:
                    return confirm['dataUploadWatermark']

            except Exception as e:
                print(f"An error occurred: {e}")
                time.sleep(randrange(1, 3))

# ---Example Usage---
# In your main script
from Unidev import Unidev

# Initialize the WirelessGuardianClient
wg_client = Unidev('apikey')

# Login
headers = wg_client.login()

# Get device logs
sn = "your_device_serial_number"
num_logs = wg_client.get_device_logs(sn)
print("Number of offline logs:", num_logs)



