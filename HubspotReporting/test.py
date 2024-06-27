import pandas as pd
from cache_pandas import timed_lru_cache

# Define a function that loads or creates the DataFrame
@timed_lru_cache(seconds=604800, maxsize=None)

def load_data():
    # Your data loading code here
    return pd.read_csv('C:\\Users\\SlaterBernstein\\OneDrive - Wireless Guardian\\Documents\\Repos\\HubspotReporting\\SandboxFolder\\slaters-view.csv')

# Call the function to load or create the DataFrame
df = load_data()

# Now you can work with the DataFrame as usual
print(df)
