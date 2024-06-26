import http.client
import json
import re

class FreshdeskAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.conn = http.client.HTTPSConnection("wirelessguardian.freshdesk.com", timeout=None)
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            'Content-Type': 'application/json'
        }

    def get_tickets(self, updated_since):
        print('Getting FD Tickets...')
        page = 1
        exists = True
        FDTickets = []

        while exists:
            payload = ''
            self.conn.request("GET", f"/api/v2/tickets?&include=stats&updated_since={updated_since}&per_page=100&page={page}", payload, self.headers)
            res = self.conn.getresponse()
            confirm = json.loads(res.read().decode('utf-8'))

            for row in confirm:
                FDTickets.append(row)

            page += 1
            if len(confirm) < 100:
                exists = False

        return FDTickets

    # Added by SB: 6/18 - Get specific ticket based on ticket ID
    def get_ticket(self, ticket_id):
        print('Getting FD Ticket...')
        FDTicket = None

        payload = ''
        self.conn.request("GET", f"/api/v2/tickets/{ticket_id}?include=stats", payload, self.headers)
        res = self.conn.getresponse()
        FDTicket = json.loads(res.read().decode('utf-8'))
        return FDTicket
    
    # Added by SB: 6/18 - Get list of custom site objects
    def get_custom_site_objects(self):
        print('Getting FD Custom Sites...')
        FDSites = []

        payload = ''
        self.conn.request("GET", f"/api/v2/custom_objects/schemas/3621063/records?page_size=100", payload, self.headers)
        res = self.conn.getresponse()
        confirm = json.loads(res.read().decode('utf-8'))

        for row in confirm["records"]:
            FDSites.append(row)

        while 'next' in confirm['_links']:
            pattern = r'next_token=([^\s]+)'
            match = re.search(pattern, confirm['_links']["next"]["href"])
            next_token_value = match.group(1)
            self.conn.request("GET", f"/api/v2/custom_objects/schemas/3621063/records?page_size=100&next_token={next_token_value}", payload, self.headers)
            res = self.conn.getresponse()
            confirm = json.loads(res.read().decode('utf-8'))

            for row in confirm["records"]:
                FDSites.append(row)

        return FDSites

    # Added by SB: 6/18 - Update specific ticket based on ticket ID. This API update does not accept the same ticket object from the "get" function so you have to pass
    # the payload as only the field(s) you want updated. Example: payload = '{"custom_fields" : { "cf_site" : "' + ticket['custom_fields']['cf_site'] + '"}}' 
    def update_ticket(self, ticket_id, payload):
        print('Updating FD Ticket...')

        self.conn.request("PUT", f"/api/v2/tickets/{ticket_id}", payload, self.headers)
        res = self.conn.getresponse()
        confirm = json.loads(res.read().decode('utf-8'))
        return confirm

# ---Example Usage----

# # imports
# from FD import FreshdeskAPI

# # Initialize APIs
# fd_api = FreshdeskAPI('your_fd_api_key')
# # "Authorization": "Bearer Token"  


# # Example usage
# fd_tickets = fd_api.get_tickets('2023-05-01')
# print(fd_tickets)


