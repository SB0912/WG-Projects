from datetime import datetime, timedelta, timezone

class DataProcessor:
    @staticmethod
    def convert(timestamp_ms): 
        timestamp_sec = timestamp_ms // 1000
        dt = datetime.fromtimestamp(timestamp_sec) # type: ignore
        formatted_datetime = dt.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_datetime
        

    @staticmethod
    # To convert regular date and time to Unix timestamp
    def convert_date_time(dateTimeString):
        # Convert the date string to a datetime object
        date_object = datetime.strptime(dateTimeString, '%Y-%m-%d %H:%M:%S')
        date_object_utc = date_object.replace(tzinfo=timezone.utc)
        # Calculate the Unix timestamp in milliseconds
        unix_time = int(date_object_utc.timestamp() * 1000)
        # Calculate the Unix timestamp in milliseconds
        return unix_time
        
    @staticmethod
    def convert_date(dateString):
        # Convert the date string to a datetime object
        date_object = datetime.strptime(dateString, '%Y-%m-%d')
        date_object_utc = date_object.replace(tzinfo=timezone.utc)
        # Calculate the Unix timestamp in milliseconds
        unix_time = int(date_object_utc.timestamp() * 1000)
        # Calculate the Unix timestamp in milliseconds
        return unix_time
    
    @staticmethod
    def regular_date(date_string):   
        date_object = datetime.strptime(date_string, "%Y-%m-%dT00:00:00.000Z")
        new_date_string = date_object.strftime("%m/%d/%Y")
        return new_date_string
        
    @staticmethod
    def convert_date_string(date_string):
        original_date = datetime.strptime(date_string, "%m/%d/%Y")
        new_date_string = original_date.strftime("%Y-%m-%dT00:00:00.000Z")
        return new_date_string
        
    @staticmethod
    def file_aggregator(path, name, ends,condition, output):
        """
        This funciton is used in order to aggregate multiple files into either a single dataframe
        or a single csv output file

        Args:
            path (string): this is the path of the target folder
            name (string): this should be the name the user desires the output csv file to be
            ends (bool): user passes True if the filename check is "endswith" False otherwise
            condition (string): filename conditiona check for files to be aggregated ie combine all files ends/starts with 'MAC.csv'
            output (bool): user passes True if the end result is an outputted csv file

        Returns:
            object (dataframe): this returns a Pandas Dataframe object for the user
        """
        import pandas as pd
        import os
        for filename in os.listdir(path):
            if ends:
                if filename.endswith(condition):
                    file_path = os.path.join(path, filename)
                    df = pd.read_csv(file_path)
                    master_df = pd.concat([master_df, df], ignore_index=True)
            else:
                if filename.startswith(condition):
                    file_path = os.path.join(path, filename)
                    df = pd.read_csv(file_path)
                    master_df = pd.concat([master_df, df], ignore_index=True)

        if output:
            master_df.to_csv(f"{path}\\{name}")
        else:
            return master_df
    


# Example usage
# timestamp_string = "2024-05-14T00:00:00.000Z"
# converted_date = TimestampConverter.convert_to_mm_dd_yyyy(timestamp_string)
# print(converted_date)  # Output: 05/14/2024


# ---Example Usage---
# from datetime import datetime, timezone
# from DataProcessor import DataProcessor  # Import the DataProcessor class

# # Usage example for the convert static method
# timestamp_ms = 1621000000
# formatted_datetime = DataProcessor.convert(timestamp_ms)
# print(formatted_datetime)

# # Usage example for the convert_date_time static method
# dateTimeString = '2024-05-14 12:00:00'
# unix_time = DataProcessor.convert_date_time(dateTimeString)
# print(unix_time)

