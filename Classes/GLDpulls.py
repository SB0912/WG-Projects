import http.client
import json
import csv
from WgDataApi import WGDataApi # type: ignore

class gldPulls:
    def gld(self, api_key, endpoint, csv_file_name):
        base_url = "api.wgdatalab.com"
        headers = {'X-API-KEY': api_key}
        gld_data = []

        # Fetch data from API
        conn = http.client.HTTPSConnection(base_url, timeout=None)
        conn.request("GET", endpoint, '', headers)
        res = conn.getresponse()
        confirm = json.loads(res.read().decode('utf-8'))

        # Write data to CSV
        with open(csv_file_name, mode="w", newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            header = ['WGSiteID', 'GoLive', 'AADT', 'Site Name', 'Reseller Name', 'validationDate']
            csv_writer.writerow(header)
            for row in confirm:
                row_data = [row['wgSiteId'], str(row['goLiveDate']), row['aadt'], row['siteName'], row['resellerName'], row['validationDate']]
                csv_writer.writerow(row_data)
        print(f"CSV file '{csv_file_name}' has been created.")



# Example usage:

# from GLDpulls import gldPulls
# api_key = '<API Key>'
# endpoint = "/api/v1/sites/search?pageSize=3000"
# csv_file_name = "C:\\Users\\NamrathaGanesh\\OneDrive - Wireless Guardian\\Desktop\\ScriptResults\\all_sitesTest2.csv"


# pulls_instance = gldPulls()

# pulls_instance.gld(api_key, endpoint, csv_file_name)

# print("HOOORRAYYYY!!!")
