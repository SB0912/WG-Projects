import sys

# Add the path to the repositories to the system path
sys.path.append('..\\Repos')

# Import necessary classes and libraries
from Classes.Quividi import Quividi
from Classes.FD import FreshdeskAPI
import pandas as pd
import requests
import json
import http.client

# Initialize the Quividi and FreshdeskAPI objects
qv_api = Quividi('')
fd_api = FreshdeskAPI('')

def getSites():
    
    # Fetches site data from Quividi API, filters and returns a DataFrame containing site IDs and labels.
    # Only includes sites where the label starts with 'AA' or 'AB'.
    
    sitesDf = pd.DataFrame(qv_api.get_sites(), None, ['id', 'label'])
    sitesDf = sitesDf.rename(columns={'id': 'site_id'})
    sitesDf['label'] = sitesDf['label'].str[:5]
    siteID = sitesDf[sitesDf['label'].str[:2].isin(['AA', 'AB'])]
    return siteID

def getAllTickets():

    # Fetches ticket data from Freshdesk API, extracts and returns a DataFrame containing relevant ticket information.
    # Filters tickets to include only those related to 'Server and Media Players'.

    ticketsDf = pd.DataFrame(fd_api.get_tickets('2024-01-01'))
    ticketsDf['cf_system'] = ticketsDf['custom_fields'].apply(lambda x: x['cf_system'])
    ticketsDf['cf_site_location'] = ticketsDf['custom_fields'].apply(lambda x: x['cf_site_location'])
    ticketsDf['cf_site_location'] = ticketsDf['cf_site_location'].str[:5]
    quividiTickets = ticketsDf[ticketsDf['cf_system'].isin(['Server and Media Players'])]
    return quividiTickets

def getAlerts():
    
    # Fetches alert data from Quividi API and returns it as a DataFrame.
    
    alertsDf = pd.DataFrame(qv_api.get_all_alerts())
    return alertsDf

def compileQuividiAlerts():
    
    # Compiles alerts from Quividi API with site information.
    # Merges site data and alert data, and returns the combined DataFrame.
    
    sites = getSites()
    alerts = getAlerts()
    combine = pd.merge(sites, alerts, left_on='site_id', right_on='site', how='left')
    print(combine)
    return combine

def compileTickets():
    
    # Compiles tickets from Freshdesk API with alert information.
    # Merges alert data and ticket data, and saves the combined DataFrame as a CSV file.
    
    tickets = getAllTickets()
    alerts = compileQuividiAlerts()
    combine = pd.merge(alerts, tickets, left_on='label_x', right_on='cf_site_location', how='left')
    combine = combine[[
        'id_x', 
        'network', 
        'site_id', 
        'location',
        'box', 
        'label_x',
        'timestamp', 
        'host_timestamp',
        'label_y', 
        'status_x', 
        'alert_type', 
        'extra_data', 
        'linked_alerthistory', 
        'id_y', 
        'subject', 
        'priority', 
        'status_y', 
        'type', 
        'due_by', 
        'created_at', 
        'cf_system', 
        'cf_site_location'
    ]]
    combine.to_csv('C:\\Users\\SlaterBernstein\\OneDrive - Wireless Guardian\\Documents\\Repos\\QuividiSitRep\\combine.csv', index=False)

# Compile the tickets and save the result to a CSV file
compileTickets()
