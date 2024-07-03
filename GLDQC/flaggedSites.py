import pandas as pd
from datetime import datetime

info_pb_file = "C:\\Users\\SlaterBernstein\\OneDrive - Wireless Guardian\\Desktop\\WG materials\\GLDQC\\Info Pb.csv"
all_sigints_file = "C:\\Users\\SlaterBernstein\\OneDrive - Wireless Guardian\\Desktop\\WG materials\\GLDQC\\all_sigints.csv"

df_info_pb = pd.read_csv(info_pb_file)
df_all_sigints = pd.read_csv(all_sigints_file)

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

df_info_pb['activated'] = pd.to_datetime(df_info_pb['activated'], utc=True)
df_info_pb['GoLiveDate'] = pd.to_datetime(df_info_pb['GoLiveDate'], format="%Y-%m-%dT%H:%M:%S.%f%z", errors='coerce')

i = 0 
while i < len(df_all_sigints):
    df_all_sigints.at[i, 'activated'] = convert(df_all_sigints.iloc[i]['activated'])
    if df_all_sigints.iloc[i]['deactivated'] != 0:
        df_all_sigints.at[i, 'deactivated'] = convert(df_all_sigints.iloc[i]['deactivated'])
    i += 1

print(df_all_sigints.iloc[0])

print(len(df_info_pb))
print(df_info_pb.info())
print(df_info_pb.iloc[0])


df_filtered_dates = df_info_pb[df_info_pb['activated'] > df_info_pb['GoLiveDate']]
df_filtered_dates = df_filtered_dates.drop_duplicates()


print(len(df_filtered_dates))
print(df_filtered_dates.iloc[0])
print(df_filtered_dates)

matching_values = df_filtered_dates['site'].unique()
df_matched_rows = df_all_sigints[df_all_sigints['site'].isin(matching_values)]
df_matched_rows = pd.merge(df_matched_rows, df_filtered_dates[['sigint', 'GoLiveDate']], on='sigint', how='inner')

print(len(df_matched_rows))
print(df_matched_rows)
print(df_matched_rows.iloc[0])

df_deactivated = df_matched_rows[df_matched_rows.duplicated(subset='site', keep=False)]

df_deactivated.to_csv(r'C:\Users\SlaterBernstein\OneDrive - Wireless Guardian\Documents\Repos\GLDQC\2f2.csv', index=False)

df_matched_rows.to_csv(r'C:\Users\SlaterBernstein\OneDrive - Wireless Guardian\Documents\Repos\GLDQC\2f2.csv', index=False)