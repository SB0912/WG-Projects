import http.client
import json
from unittest import skip
import requests
import http
import pandas as pd
import csv
import sys
import os


def getGoZone():

    api_tokens = {
        'CLV_':'63ffc424-18c8-43d6-8a10-d58dc1a80a3c',
        'Mason_City_Arena_':'76817361-0fdf-4541-ba12-26207a53dfb8',
        'Lydias_on_H_':'32c4b828-e578-47c8-a153-b0d211cfe8d2',
        'Wireless_Guardian_':'360c2952-786c-46fe-9ba0-07b6b2b0f652'
    }

    dest_path = 'C:\\Users\\SlaterBernstein\\OneDrive - Wireless Guardian\\Documents\\Repos\\GoZonePulls\\output\\'

    for token in api_tokens.values():

        url = f"https://api-usb.smartwifiplatform.com/v2/client/connections?api_token={token}&from=2024-05-01&to=2024-05-31"

        payload = {}
        try:
            res = requests.request("GET", url, headers=None, data=payload).json()
        except:
            continue
        else:
            df = pd.DataFrame(res)
            df.to_csv(dest_path + f'{token}OptWifiMAY24.csv')

# getGoZone()



def compile(directory_path):

    # List to hold individual DataFrames
    data_frames = []

    # Loop through the directory
    for file_name in os.listdir(directory_path):
        # Check if the file is a CSV
        if file_name.endswith('.csv'):
            # Create the full file path
            file_path = os.path.join(directory_path, file_name)
            # Load the CSV file into a DataFrame and append to the list
            df = pd.read_csv(file_path)
            data_frames.append(df)

    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(data_frames, ignore_index=True)
    combined_df.to_csv('C:\\Users\\SlaterBernstein\\OneDrive - Wireless Guardian\\Documents\\Repos\\GoZonePulls\\output' + 'Wifi.csv')
    # print(combined_df.info())

compile(directory_path='C:\\Users\\SlaterBernstein\\OneDrive - Wireless Guardian\\Desktop\\WG materials\\SaaM Raw Data\\Wifi')
