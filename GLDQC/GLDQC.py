from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import datetime
import os
import shutil
import hashlib
from datetime import datetime
import http.client
import json
import csv


# variables used for the mapping table function raw data path is where all of the output files will be stored 
raw_data_path = "C:\\Users\\SlaterBernstein\\OneDrive - Wireless Guardian\\Documents - Wireless Guardian\\Data Department\Monthly Executive Reports\\Raw Data\\December 2023"
sandbox_path = "C:\\Users\SlaterBernstein\\OneDrive - Wireless Guardian\\Desktop\WG materials\\GLDQC"
chrome_d_path = "C:\\Users\\SlaterBernstein\\OneDrive - Wireless Guardian\\Documents - Wireless Guardian\\Data Department\\Python Scripts\\Final Versions\\SentinelScraper\\chromedriver.exe"



# Convert the time to a Unix timestamp in milliseconds
current_time = time.localtime()
now = int(time.mktime(current_time) * 1000)
now_time = str(now)
#print(now_time)

token_secret = 'b0um83r0g4ziinzigxdfymtuenn42hms'
x_sentinel_time = now_time

# Concatenate the strings
input_string = token_secret + ':' + x_sentinel_time

# Calculate the SHA256 hash
sha256_hash = hashlib.sha256(input_string.encode()).hexdigest()

conn = http.client.HTTPSConnection("data.wgsentinel.com", timeout=None)
payload = ''
headers = {
    'x-sentinel-data': 'XDCh8bb2Y3KSblVXsDY6Q4mnfmXwXqb_RJQWwlhBnry9_uUoBCeZvJFV8KlQhJRaKwlwaVyB1lCkBcAa1b1mSHLeI8PcY8uIeZrdJ2e8RF1YYOBeqEziA8ORneYXSeC5',
    'x-sentinel-time': now_time,
    'x-sentinel-secret': sha256_hash
}

# allSigints function from Lab API
def allSigints(all_sigints_path):
    conn.request("GET", f"/api/v1/sigint", payload, headers)
    res = conn.getresponse()
    confirm = json.loads(res.read().decode('utf-8'))
    j_name = 'sigints.json'
    csv_file = "all_sigints.csv"
    with open(f"{all_sigints_path}\\{j_name}", 'w') as json_file:
        json.dump(confirm, json_file, indent=4)

    # Specify the CSV file name
 
    with open(f"{all_sigints_path}\\{csv_file}", mode="w", newline="", encoding="utf-8") as csv_file:
        #Create a CSV writer
        csv_writer = csv.writer(csv_file)

        # Write the header row
        header = [key for key in confirm[0].keys()]
        csv_writer.writerow(header)

        # Write data rows
        for row in confirm:
            row_data = [value for key, value in row.items()]
            csv_writer.writerow(row_data)
    
    print(f"CSV file '{csv_file}' has been created.")
    return "all_sigints.csv"



# WGDataLab pulls inside of a function
def database_sites(csv_file_name):
    conn = http.client.HTTPSConnection("api.wgdatalab.com", timeout=None)
    payload = ''
    headers = {
        'X-API-KEY': 'YRn6!sEt9nVDuqb5rFR8QM9TMD4#qVDxY442Rs8rQhKa%tgVhXtrWVe2KZjx7z6YKy*@BceaQ8mdhvNP2x7s%sB#fDN%zgd5F5D'
    }

    conn.request("GET", f"/api/v1/sites/search", payload, headers)
    res = conn.getresponse()
    confirm = json.loads(res.read().decode('utf-8'))

    # Specify the CSV file name
    sites_file_name = "all_sites_wg.csv"
    # Open the CSV file for writing
    with open(f"{csv_file_name}\\{sites_file_name}", mode="w", newline="", encoding="utf-8") as csv_file:
        # Create a CSV writer
        csv_writer = csv.writer(csv_file)

        # Write the header row
        header = ['WGSiteID', 'GoLive', 'AADT', 'Site Name', 'Reseller Name', 'site']
        csv_writer.writerow(header)

        # Write data rows
        for row in confirm:
            row_data = [row['wgSiteId'], str(row['goLiveDate']), row['aadt'], row['siteName'], row['resellerName'], row['sentinelAliasIds']]
            csv_writer.writerow(row_data)

    print(f"CSV file '{csv_file_name}' has been created.")
    print(confirm)
    print("HOOORRAYYYY!!!")
    return sites_file_name




def map_table(raw_data_folder, chrome_path):
    
    # Path to your ChromeDriver executable
    chrome_driver_path = chrome_path

    # Create a new instance of the Chrome driver with the Service class
    driver = webdriver.Chrome(service=Service(chrome_driver_path))

    # Navigate to a website
    driver.get("https://wgsentinel.com/login")
    driver.maximize_window()
    username = 'sbevilacqua'
    password = 'LetsGetScrapy1!'

    login = driver.find_element(By.CSS_SELECTOR, "input[type='text']").send_keys(username)
    password = driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(password)
    password = driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(Keys.RETURN)
    
    time.sleep(7)
    # Click the site groups button
    site_groups_button = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-orange')))
    site_groups_button.click()

    # Give some extra time for the next page to load (adjust this timing as needed)
    time.sleep(7)

    # Click the export button
    export_button = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-outline-purple')))
    export_button.click()
    time.sleep(7)
    # Close the browser at the end, ensuring it closes regardless of the outcome
    driver.quit() 
    
    # Path to  Downloads folder and the destination folder
    downloads_folder = "C:\\Users\\SlaterBernstein\\Downloads"
    destination_folder = raw_data_folder
    
    # Get a list of files in the Downloads folder along with their modification times
    files = []
    for filename in os.listdir(downloads_folder):
        file_path = os.path.join(downloads_folder, filename)
        if os.path.isfile(file_path):
            modification_time = os.path.getmtime(file_path)
            files.append((file_path, modification_time))

    # Sort the files by modification time (newest first)
    files.sort(key=lambda x: x[1], reverse=True)

    # Check if there are files in the Downloads folder
    if files:
        # Get the path of the most recent file
        most_recent_file_path = files[0][0]
        
        new_file_name = "sentinel_sites.csv"

        new_file_path = os.path.join(destination_folder, new_file_name)
        # Move the most recent file to the destination folder
        shutil.move(most_recent_file_path, new_file_path)
        print(f"Moved {most_recent_file_path} to {destination_folder}")
    else:
        print("No files found in the Downloads folder")
    


    
    # The pathways for the 3 files used to create the mapping table this should be in the 
    # Shared One Drive
    all_sigs_file = allSigints(all_sigints_path=raw_data_folder)
    sites_file = database_sites(csv_file_name=raw_data_folder)

    # Creating the different dataframes for the three files in the aforementioned pathways
  
    df_wg_alvan = pd.read_csv(f"{raw_data_folder}\\{sites_file}")
    # df_sentinel = pd.read_csv(f"{raw_data_folder}\\{new_file_name}")
    df = pd.read_csv(f"{raw_data_folder}\\{all_sigs_file}")
    df = pd.read_csv(f"{raw_data_folder}\\all_sigints.csv")
    df_sentinel = pd.read_csv(f"{raw_data_folder}\\sentinel_sites.csv")

    # function that converts unixcode time into actual time
    def convert(timestamp_ms):

        # Unix timestamp in milliseconds
        # Convert milliseconds to seconds
        timestamp_sec = timestamp_ms // 1000

        # Create a datetime object from the Unix timestamp in seconds
        dt = datetime.fromtimestamp(timestamp_sec)

        # Convert datetime object to a formatted string
        formatted_datetime = dt.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_datetime


    # while loop to convert unixtimecode in the activated and deactivated columns of the all sigints file
    i = 0 
    while i < len(df):
        df.at[i, 'activated'] = convert(df.iloc[i]['activated'])
        if df.iloc[i]['deactivated'] != 0:
            df.at[i, 'deactivated'] = convert(df.iloc[i]['deactivated'])
        i += 1
        

    # while loop that maps the sigints with the proper WG Site ID from the sites file. In the loop the Site Name gets parsed to extract AA###
    df_sentinel['WGSite'] = 'missing'
    i = 0 
    while i < len(df_sentinel):
        if df_sentinel.iloc[i]['Site Name'][1] == 'A':
            x = df_sentinel.iloc[i]['Site Name'][:5]
            df_sentinel.at[i, 'WGSite'] = df_sentinel.iloc[i]['Site Name'][:5]
        else:
            df_sentinel.at[i, 'WGSite'] = df_sentinel.iloc[i]['Site Name'][:6]
        i += 1

    # Empty arrays that store all of the needed values for the corresponding columns
    aa_num = []
    sitegroup_list = []
    site_name_list = []

    # While loop that matches the site from the sigints file to find and store the values corresponding WGSiteID, Sitegroup Name, and Site Name
 
    i = 0
    while i< len(df):
        j = 0
        if df.iloc[i]['site'] == df_sentinel.iloc[i]['Site']:
            aa_num.append(df_sentinel.iloc[i]['WGSite'])
            sitegroup_list.append(df_sentinel.iloc[i]['Sitegroup Name'])
            site_name_list.append(df_sentinel.iloc[i]['Site Name'])

        else:
            while j < len(df_sentinel):
                
                if df.iloc[i]['site'] == df_sentinel.iloc[j]['Site']:
                    aa_num.append(df_sentinel.iloc[j]['WGSite'])
                    sitegroup_list.append(df_sentinel.iloc[j]['Sitegroup Name'])
                    site_name_list.append(df_sentinel.iloc[j]['Site Name'])

                    break
                elif j == len(df_sentinel) -1:
                    aa_num.append('Not Found')
                    sitegroup_list.append('Not Found')
                    site_name_list.append('Not Found')

                    break
                else:
                    j += 1

        i += 1

    # adding the lists with the values to the dataframe which will be the final df used for the mapping table
    df['WGSite_ID'] = aa_num
    df['Sitegroup Name'] = sitegroup_list
    df['Site Name'] = site_name_list
        
    # empty arrays used to store the GoLive and AADT values 
    gld_list = []
    aadt_list = []

    # While loop that matches the WGSite ID to find and store the values corresponding to the GoLive date and the AADT number
 
    i = 0
    while i< len(df):
        j = 0
        if df.iloc[i]['WGSite_ID'] == df_wg_alvan.iloc[i]['WGSiteID']:
            gld_list.append(df_wg_alvan.iloc[i]['GoLive'])
            aadt_list.append(df_wg_alvan.iloc[i]['AADT'])
        else:
            while j < len(df_wg_alvan):   
                x = df.iloc[i]['WGSite_ID']
                if df.iloc[i]['WGSite_ID'] == df_wg_alvan.iloc[j]['WGSiteID']:
                    gld_list.append(df_wg_alvan.iloc[j]['GoLive'])
                    aadt_list.append(df_wg_alvan.iloc[j]['AADT'])
                    break
                elif df.iloc[i]['WGSite_ID'] == 'Not Found' or j == len(df_wg_alvan) -1:
                    gld_list.append('Not Found')
                    aadt_list.append('Not Found')
                    break
                else:
                    j += 1
        i += 1
    # adding the lists with values to the dataframe
    df['GoLiveDate'] = gld_list
    df['AADT'] = aadt_list
    
    output_file = f"{raw_data_folder}\\Info Pb.csv"
    df.to_csv(output_file, index=False)
    
    # SLATERS ADDITIONS HERE -----------------------------------------------------------
    # find activated date, then QC check between activated date and GLD, (i.e. GLD before install or activation date), flag sites with anomolous dates somehow, if no anomolies, print message
    
    df_info_pb = pd.read_csv(f"{sandbox_path}\\Info Pb.csv")
    df_all_sigints = pd.read_csv(f"{sandbox_path}\\all_sigints.csv")
    
    # converting to Datetime object in the df
    df_info_pb['activated'] = pd.to_datetime(df_info_pb['activated'], utc=True)
    df_info_pb['GoLiveDate'] = pd.to_datetime(df_info_pb['GoLiveDate'], format="%Y-%m-%dT%H:%M:%S.%f%z", errors='coerce')
    
    # Epoch to UTC conversion in all_sigints df
    i = 0 
    while i < len(df_all_sigints):
        df_all_sigints.at[i, 'activated'] = convert(df_all_sigints.iloc[i]['activated'])
        if df_all_sigints.iloc[i]['deactivated'] != 0:
            df_all_sigints.at[i, 'deactivated'] = convert(df_all_sigints.iloc[i]['deactivated'])
        i += 1
        
    # check for activation dates that are later than go live dates    
    df_filtered_dates = df_info_pb[df_info_pb['activated'] > df_info_pb['GoLiveDate']]
    df_filtered_dates = df_filtered_dates.drop_duplicates()
    
    # grabbing unique site values from filtered dates df and running it against all sigints df to get all entries for anomoulous dates
    matching_values = df_filtered_dates['site'].unique()
    df_matched_rows = df_all_sigints[df_all_sigints['site'].isin(matching_values)]
    df_matched_rows = pd.merge(df_matched_rows, df_filtered_dates[['sigint', 'GoLiveDate']], on='sigint', how='inner')
    
    # create seperate df for ONLY sites with duplicate siteIDs for deactivation insights
    df_deactivated = df_matched_rows[df_matched_rows.duplicated(subset='site', keep=False)]
    
    # converting the dataframe to the Info Pb csv Mapping Table

    df.to_csv(output_file, index=False)
    df_matched_rows.to_csv(f"{sandbox_path}\\wrongDates.csv", index=False)
    df_deactivated.to_csv(f"{sandbox_path}\\deactivated.csv", index=False)
    
    #deleting extra files in folder
    
    files_to_delete = ['all_sigints.csv', 'all_sites_wg.csv', 'sentinel_sites.csv', 'sigints.json']
    
    for file_name in files_to_delete:
        file_path = os.path.join(sandbox_path, file_name)
        try:
            os.remove(file_path)
            print(f"deleted: {file_path}")
        except Exception as e:
            print(f"no bueno: {e}")
    

    return print(f"\n\nInfo Pb table has been created at: {output_file}\n\nWrong dates table has been created at: {output_file}\n\nDeactivated sites table has been created at: {output_file}")

map_table(raw_data_folder=sandbox_path, chrome_path=chrome_d_path)

