from os import name
import sys

sys.path.append('..\\Repos')

from Classes.Quividi import Quividi
from Classes.FD import FreshdeskAPI

import pandas as pd
import requests
import json
import http.client

qv_api = Quividi('d2lyZWxlc3NndWFyZGlhbl9zYmVybnN0ZWluOmM4YmVmYTI2N2ZkOTQ5MWFjZThiMTExMzQ2NzczYzE2NjMzM2I1MzQ=')

fd_api = FreshdeskAPI('amhPd2VObDVacTlNWmJXVlExSDg=')

def getSites():

    sitesDf = pd.DataFrame(qv_api.get_sites(),None, ['id','label'])
    sitesDf = sitesDf.rename(columns={'id': 'site_id'})
    sitesDf['label'] = sitesDf['label'].str[:5]
    siteID = sitesDf[sitesDf['label'].str[:2].isin(['AA', 'AB'])]
    # print(siteID)
    return siteID

# getSites()

def getAllTickets():

    ticketsDf = pd.DataFrame(fd_api.get_tickets('2024-01-01'))
    ticketsDf['cf_system'] = ticketsDf['custom_fields'].apply(lambda x: x['cf_system'])
    ticketsDf['cf_site_location'] = ticketsDf['custom_fields'].apply(lambda x: x['cf_site_location'])
    ticketsDf['cf_site_location'] = ticketsDf['cf_site_location'].str[:5]
    quividiTickets = ticketsDf[ticketsDf['cf_system'].isin(['Server and Media Players'])]
    return quividiTickets

# getAllTickets()

def getAlerts():

    alertsDf = pd.DataFrame(qv_api.get_all_alerts())
    # print(alertsDf)
    return alertsDf

# getAlerts()

def compileQuividiAlerts():
    
    sites = getSites()
    alerts = getAlerts()

    combine = pd.merge(sites, alerts, left_on='site_id', right_on='site', how='left')
    print(combine)
    return combine

# compileQuividiAlerts()

def compileTickets():
    
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

compileTickets()