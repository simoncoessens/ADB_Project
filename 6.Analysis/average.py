import ast
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import csv

# Define your file paths for each scale factor

# Define your file paths for each scale factor
# Define your file paths for each scale factor
# Define your file paths for each scale factor
file_paths_1 = [
    r"Benchmark_GCloud_iteration_2/Query_times_{}_{}.txt".format(2, i) for i in range(4,10)
]

file_paths_10 = [
    r"Benchmark_GCloud_iteration_2/Query_times_{}_{}.txt".format(10, i) for i in range(4,10)
]

file_paths_100 = [
    r"Benchmark_GCloud_iteration_2/Query_times_{}_{}.txt".format(100, i) for i in range(4,10)
]

file_paths_1000 = [
    r"Benchmark_GCloud_iteration_2/Query_times_{}_{}.txt".format(1000, i) for i in range(4,10)
]



# Initialize dictionaries to store the total time and count for each query for each scale factor
total_time_1, total_time_10, total_time_100, total_time_1000 = {}, {}, {}, {}
count_1, count_10, count_100, count_1000 = {}, {}, {}, {}

transaction_1, transaction_10, transaction_100, transaction_1000 = [], [], [], []

# Get the transaction in the files
def get_transactions(file_paths, last_elements):
    # Open the first file
    with open(file_paths[0], 'r') as file:
        # Read the data from the file line by line
        for line in file:
            # Remove the enclosing double quotes
            line = line.strip().strip('"')

            # Parse the line into a list
            query_data = ast.literal_eval(line)

            # Extract the last element and add it to the list
            last_elements.append(query_data[-1])


# Process the first file for each scale factor
get_transactions(file_paths_1, transaction_1)
get_transactions(file_paths_10, transaction_10)
get_transactions(file_paths_100, transaction_100)
get_transactions(file_paths_1000, transaction_1000)


def compute_transactions_per_minute(num_transactions, average_time_seconds):
    # Compute transactions per minute
    transactions_per_minute = (num_transactions / average_time_seconds) * 60

    return transactions_per_minute


# Function to process a set of files
def process_files(file_paths, total_time, count):
    # Iterate over the file paths
    for file_path in file_paths:
        # Open each file
        with open(file_path, 'r') as file:
            # Read the data from the file line by line
            for line in file:
                # Remove the enclosing double quotes
                line = line.strip().strip('"')

                # Parse the line into a list
                query_data = ast.literal_eval(line)

                # If the query is already in the dictionary, add the time to the total and increment the count
                if query_data[0] in total_time:
                    total_time[query_data[0]] += float(query_data[1])
                    count[query_data[0]] += 1
                # If the query is not in the dictionary, add it with the time as the value and set the count to 1
                else:
                    total_time[query_data[0]] = float(query_data[1])
                    count[query_data[0]] = 1


# Process the files for each scale factor
process_files(file_paths_1, total_time_1, count_1)
process_files(file_paths_10, total_time_10, count_10)
process_files(file_paths_100, total_time_100, count_100)
process_files(file_paths_1000, total_time_1000, count_1000)

# Calculate the average time for each query for each scale factor
average_time_1 = {query: time / count_1[query] for query, time in total_time_1.items()}
average_time_10 = {query: time / count_10[query] for query, time in total_time_10.items()}
average_time_100 = {query: time / count_100[query] for query, time in total_time_100.items()}
average_time_1000 = {query: time / count_1000[query] for query, time in total_time_1000.items()}


def write_combined_csv(file_name, data_dicts):
    # Assuming all dictionaries have the same keys
    queries = data_dicts[0].keys()

    with open(file_name, mode='w', newline='') as csv_file:
        fieldnames = ['Query', 'Average Time (seconds)_1', 'Average Time (seconds)_10', 'Average Time (seconds)_100',
                      'Average Time (seconds)_1000']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for query in queries:
            row = {
                'Query': query,
                'Average Time (seconds)_1': data_dicts[0].get(query, 0),
                'Average Time (seconds)_10': data_dicts[1].get(query, 0),
                'Average Time (seconds)_100': data_dicts[2].get(query, 0),
                'Average Time (seconds)_1000': data_dicts[3].get(query, 0)
            }
            writer.writerow(row)


# Call the function with all dictionaries
write_combined_csv('Analysis/combined_average_times.csv', [average_time_1, average_time_10, average_time_100, average_time_1000])