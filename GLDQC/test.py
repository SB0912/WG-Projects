# import csv
# from datetime import datetime

# def process_csv(input_file, output_file, columns_to_modify, date1_column, date2_column):
#     try:
#         with open(input_file, 'r', newline='') as input_csv, open(output_file, 'w', newline='') as output_csv:
#             reader = csv.reader(input_csv)
#             writer = csv.writer(output_csv)
            
#             header = next(reader)
#             writer.writerow(header)
            
#             for row in reader:
#                 modify_row = False

#                 for column_index in columns_to_modify:
#                     if len(row) > column_index:
#                         if column_index == date2_column:
#                         # Modify the specified column
#                             row[column_index] = row[column_index][:10]
#                         if column_index == date1_column:
#                             row[column_index] = datetime.strftime(datetime.strptime(row[column_index], "%m/%d/%Y %H:%M"), "%Y-%m-%d")
#                         modify_row = True

#                 # Compare dates and modify row if necessary
#                 if len(row) > date1_column and len(row) > date2_column:
#                     date1 = row[date1_column]
#                     date2 = row[date2_column]

#                     # Keep rows where difference
#                     if date1 > date2:
#                         modify_row = True
#                     else:
#                         modify_row = False

#                 # Write the modified row to the new CSV file
#                 if modify_row:
#                     writer.writerow(row)

#         print(f"Processing completed. Modified data written to {output_file}")

#     except Exception as e:
#         print(f"Error: {e}")


# input_csv_file = "C:\\Users\\SlaterBernstein\\OneDrive - Wireless Guardian\\Desktop\\WG materials\\GLDQC\\Info Pb.csv"
# output_csv_file = "C:\\Users\\SlaterBernstein\\OneDrive - Wireless Guardian\\Documents\\Repos\\GLDQC\\outputs.csv" 
# columns_indices_to_modify = [5, 12]
# date1_column_index = 5 
# date2_column_index = 12

# process_csv(input_csv_file, output_csv_file, columns_indices_to_modify, date1_column_index, date2_column_index)

import csv
from datetime import datetime
import pandas as pd

def process_csv(input_file, output_file, columns_to_modify, date1_column, date2_column):
    try:
        modified_data = []

        with open(input_file, 'r', newline='') as input_csv:
            reader = csv.reader(input_csv)
            
            header = next(reader)

            for row in reader:
                modify_row = False

                for column_index in columns_to_modify:
                    if column_index < len(row):  # Check if the column index is within the row length
                        if column_index == date2_column:
                            row[column_index] = row[column_index][:10]
                        if column_index == date1_column:
                            row[column_index] = datetime.strftime(datetime.strptime(row[column_index], "%m/%d/%Y %H:%M"), "%Y-%m-%d")
                        modify_row = True

                if len(row) > date1_column and len(row) > date2_column:
                    date1 = row[date1_column]
                    date2 = row[date2_column]

                    if date1 > date2:
                        modify_row = True
                    else:
                        modify_row = False

                if modify_row:
                    modified_data.append(row)

        with open(output_file, 'w', newline='') as output_csv:
            writer = csv.writer(output_csv)
            writer.writerow(header)
            writer.writerows(modified_data)

        print(f"Processing completed. Modified data written to {output_file}")

    except Exception as e:
        print(f"Error: {e}")

def extract_matching_rows(output_file, column_to_compare, other_csv_file, matching_output_file):
    try:
        matching_results = []

        with open(output_file, 'r', newline='') as output_csv, open(other_csv_file, 'r', newline='') as other_csv:
            output_reader = csv.reader(output_csv)
            other_reader = csv.reader(other_csv)

            output_header = next(output_reader)
            other_header = next(other_reader)

            if column_to_compare not in output_header:
                print(f"Error: Column '{column_to_compare}' not found in the output CSV header.")
                return None

            if column_to_compare not in other_header:
                print(f"Error: Column '{column_to_compare}' not found in the other CSV header.")
                return None

            output_column_index = output_header.index(column_to_compare)
            other_column_index = other_header.index(column_to_compare)

            for output_row in output_reader:
                site_to_match = output_row[output_column_index]
                other_csv.seek(0)  # Reset the other CSV reader to the beginning for each output row

                matching_rows = []

                for other_row in other_reader:
                    if other_column_index < len(other_row):  # Check if the other column index is within the row length
                        if site_to_match == other_row[other_column_index]:
                            matching_rows.append(other_row)

                matching_results.extend(matching_rows)

        with open(matching_output_file, 'w', newline='') as matching_csv:
            writer = csv.writer(matching_csv)
            if matching_results:
                writer.writerow(other_header)
                writer.writerows(matching_results)

        print(f"All matching rows from other CSV written to {matching_output_file}")
        return matching_results

    except Exception as e:
        print(f"Error: {e}")
        return None

# Specify the columns and file paths
column_to_compare = "site"  # column name to compare for duplicates
input_csv_file = "C:\\Users\\SlaterBernstein\\OneDrive - Wireless Guardian\\Desktop\\WG materials\\GLDQC\\Info Pb.csv"
modified_output_csv_file = output_csv_file = "C:\\Users\\SlaterBernstein\\OneDrive - Wireless Guardian\\Documents\\Repos\\GLDQC\\results.csv" 
other_csv_file = "C:\\Users\\SlaterBernstein\\OneDrive - Wireless Guardian\\Desktop\\WG materials\\GLDQC\\all_sigints.csv"
matching_output_csv_file = output_csv_file = "C:\\Users\\SlaterBernstein\\OneDrive - Wireless Guardian\\Documents\\Repos\\GLDQC\\matching.csv"

# date columns needing to be modified
columns_indices_to_modify = [5, 12]
date1_column_index = 5
date2_column_index = 12

process_csv(input_csv_file, output_csv_file, columns_indices_to_modify, date1_column_index, date2_column_index)

# Extract matching rows and save to a separate CSV file
matching_results = extract_matching_rows(output_csv_file, column_to_compare, other_csv_file, matching_output_csv_file)
print("Matching results:", matching_results)


