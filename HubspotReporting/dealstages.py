import http.client
import json
import pandas as pd
import time
import datetime
import hashlib
import os
import csv
from datetime import datetime, timedelta, timezone, date
from hubspot import HubSpot

# API key for authentication with HubSpot API
apiKey = '<API Key>'

# Initialize the HubSpot client
api_client = HubSpot(access_token=apiKey)

# Destination path for saving output files
destPath = 'C:\\Users\\SlaterBernstein\\OneDrive - Wireless Guardian\\Documents\\Repos\\HubspotReporting\\Outputs\\'

# List of properties to be fetched from HubSpot API
properties = [
    'hs_v2_latest_time_in_102243492',
    'hs_v2_latest_time_in_143496326',
    'hs_v2_latest_time_in_143496327',
    'hs_v2_latest_time_in_143496328',
    'hs_v2_latest_time_in_143496329',
    'hs_v2_latest_time_in_157459726',
    'hs_v2_latest_time_in_78544787'
]

def getDeals():
    
    # Fetches deal data from the HubSpot API, converts it to a DataFrame, and saves it as a CSV file.
    
    conn = http.client.HTTPSConnection("api.hubapi.com", timeout=None)
    payload = ''
    headers = {
        'Authorization': 'Bearer ' + apiKey
    }

    conn.request("GET", f"/crm/v3/objects/deals?limit=100&properties=hs_v2_latest_time_in_102243492", payload, headers)
    res = conn.getresponse()
    confirm = json.loads(res.read().decode('utf-8'))
    deals_df = pd.json_normalize(confirm['results'])
    print(deals_df.info())
    deals_df.to_csv(destPath + 'deals.csv')
# getDeals()

def getCompanies():
    
    # Fetches company data from the HubSpot API and converts it to a DataFrame.
    
    conn = http.client.HTTPSConnection("api.hubapi.com", timeout=None)
    payload = ''
    headers = {
        'Authorization': 'Bearer ' + apiKey
    }

    conn.request("GET", f"/crm/v3/objects/companies?limit=10", payload, headers)
    res = conn.getresponse()
    confirm = json.loads(res.read().decode('utf-8'))
    companies_df = pd.json_normalize(confirm['results'])
    print(companies_df.head())
# getCompanies()

def getContacts():
    
    # Fetches contact data from the HubSpot API and converts it to a DataFrame.
    
    conn = http.client.HTTPSConnection("api.hubapi.com", timeout=None)
    payload = ''
    headers = {
        'Authorization': 'Bearer ' + apiKey
    }

    conn.request("GET", f"/crm/v3/objects/contacts?limit=10", payload, headers)
    res = conn.getresponse()
    confirm = json.loads(res.read().decode('utf-8'))
    contacts_df = pd.json_normalize(confirm['results'])
    print(contacts_df.head())
getContacts()
