import os
import pandas as pd
import shutil
import zipfile
from datetime import date, datetime, timedelta

# Define folder paths
downloads_folder = 'C:\\Users\\SlaterBernstein\\Downloads'
top_folder = 'C:\\Users\\SlaterBernstein\\OneDrive - Wireless Guardian\\Documents\\Repos\\HubspotReporting\\'
sandbox_folder = 'C:\\Users\\SlaterBernstein\\OneDrive - Wireless Guardian\\Documents\\Repos\\HubspotReporting\\SandboxFolder\\'
outputs_folder = 'C:\\Users\\SlaterBernstein\\OneDrive - Wireless Guardian\\Documents\\Repos\\HubspotReporting\\Outputs\\'
archive_folder = 'C:\\Users\\SlaterBernstein\\OneDrive - Wireless Guardian\\Documents\\Repos\\HubspotReporting\\Archive\\'

# Get today's date as a string
todaysCount = str(date.today())

def get_mod_time(file):
    
    # Gets the modification time of a file and converts it to a string format.
    
    # :param file: Path to the file
    # :return: Modification time as a string
    
    mod_time = os.path.getmtime(file)
    convert = str(date.fromtimestamp(mod_time))
    return convert

def move_to_sandbox(src_folder, dest_folder):
    
    # Moves the latest HubSpot CRM export file from the downloads folder to the sandbox folder.
    
    # :param src_folder: Source folder path
    # :param dest_folder: Destination folder path
    
    src_files = sorted(os.listdir(src_folder), key=lambda x: os.stat(os.path.join(src_folder, x)).st_mtime, reverse=True)
    print(len(src_files))
    
    filter_files = [f for f in src_files if os.path.isfile(os.path.join(src_folder, f))]
    print(len(filter_files))
    print(filter_files)
    
    if len(filter_files) == 0:
        print("try again")
        return
    
    if '~$' in str(filter_files[0]):
        file = filter_files[1]
        print(file)
    else:
        file = filter_files[0]
        print(file)
    
    if "hubspot-crm-exports" not in str(file).lower():
        print("try again")
        return
    
    src_file_path = os.path.join(src_folder, file)
    print(src_file_path)
    dest_file_path = os.path.join(dest_folder, file)
    print(dest_file_path)
    
    if file.lower().endswith('.zip'):
        with zipfile.ZipFile(src_file_path, 'r') as zipper:
            zipper.extractall(dest_folder)
    else:
        shutil.copy(src_file_path, dest_file_path)

move_to_sandbox(src_folder=downloads_folder, dest_folder=sandbox_folder)

def data_frame(dest_folder, src_folder):
    
    # Processes the most recent file in the sandbox folder, extracts deal stage and reseller counts,
    # and saves the results as CSV files. Moves the processed file to the archive folder.
    
    # :param dest_folder: Destination folder path
    # :param src_folder: Source folder path
    
    find_it = sorted(os.listdir(dest_folder), key=lambda x: os.stat(os.path.join(dest_folder, x)).st_mtime, reverse=True)
    df_file = find_it[0]
    print(df_file)
    
    df_file_path = os.path.join(dest_folder, df_file)
    print(df_file_path)

    mod_date = sorted(os.listdir(src_folder), key=lambda x: os.stat(os.path.join(src_folder, x)).st_mtime, reverse=True)
    output_csv_mdate = os.path.join(src_folder, mod_date[0])
    
    if df_file_path.lower().endswith('.xlsx') or df_file_path.lower().endswith('.xls'):
        week_df = pd.read_excel(df_file_path)
        print(week_df)
    else:
        week_df = pd.read_csv(df_file_path)
        print(week_df)
    print(week_df.info())
    
    deal_stages = [
        '3. Contracts & Committments', '4A. Site Hold Invoiced', '4B. Site Walk Invoiced',
        '5A. Site Hold Paid', '5B. Site Walk Paid', '6. Sales Review', '7. RF Review',
        '8. Ops Review', '9. Equipment Review', '10. Equipment Invoiced', '11. Equipment Paid',
        '12. Equipment Shipped/Awaiting Install', '13. Installed Pending LPR', '14. Deal Won/ Installed'
    ]
    counts_data = {'Pull Date': date.today(), 'Deal Stage': deal_stages}
    counts_df = pd.DataFrame(counts_data)

    for stage in deal_stages:
        count = (week_df['Deal Stage'] == stage).sum()
        counts_df.loc[counts_df['Deal Stage'] == stage, 'Count'] = count
    # print(counts_df)
    
    resellers = ['Apex', 'SVR', 'C&M', 'TD Synnex', 'OG Guard']
    counts_data = {'Pull Date': date.today(), 'Resellers': resellers}
    purg_counts_df = pd.DataFrame(counts_data)

    for reseller in resellers:
        count = ((week_df['Deal Stage'] == 'Purgatory') & (week_df['Tier 1 (Reseller)'].str.contains(reseller))).sum()
        painInMyAss = ((week_df['Deal Stage'] == 'Purgatory') & (week_df['Tier 2 (Reseller Sales Org)'].str.contains('SVR'))).sum()
        purg_counts_df.loc[purg_counts_df['Resellers'] == reseller, 'Count'] = count
        purg_counts_df.loc[purg_counts_df['Resellers'] == 'SVR', 'Count'] = painInMyAss
    # print(purg_counts_df)
        
    counts_df.to_csv(get_mod_time(output_csv_mdate) + '_Deal_stage_counts.csv', index=False, float_format='{:0.0f}'.format)
    purg_counts_df.to_csv(get_mod_time(output_csv_mdate) + '_Purgatory_counts.csv', index=False, float_format='{:0.0f}'.format)
    
    shutil.move(df_file_path, archive_folder + df_file)

data_frame(dest_folder=sandbox_folder, src_folder=downloads_folder)

def output(top_dir, outputs_folder):
    
    # Placeholder function for processing output files.
    
    # :param top_dir: Top directory path
    # :param outputs_folder: Outputs folder path
    
    purg_delta_df = {}
    deals_delta_df = {}
    
    src_files = sorted(os.listdir(top_dir), key=lambda x: os.stat(os.path.join(top_dir, x)).st_mtime, reverse=True)
    print(src_files)
    
    for file in src_files:
        name, date = os.path.splitext(file)[0][-10:], os.path.splitext(file)[0]

output(top_dir=top_folder, outputs_folder=outputs_folder)

def organize(sandbox_folder, archive_folder, output_folder, src_folder):
    
    # Placeholder function for organizing files.
    
    # :param sandbox_folder: Sandbox folder path
    # :param archive_folder: Archive folder path
    # :param output_folder: Outputs folder path
    # :param src_folder: Source folder path
    
    src_files = sorted(os.listdir(sandbox_folder), key=lambda x: os.stat(os.path.join(sandbox_folder, x)).st_mtime, reverse=True)
    print(src_files)

organize(sandbox_folder=sandbox_folder, archive_folder=archive_folder, output_folder=outputs_folder, src_folder=downloads_folder)
