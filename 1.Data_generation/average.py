import ast
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline


# Define your file paths for each scale factor

# Define your file paths for each scale factor

file_paths_10 = [
    r"Benchmark_Azure_iteration2/SF=10/Query_times_10_0.txt",
    r"Benchmark_Azure_iteration2/SF=10/Query_times_10_1.txt",
    r"Benchmark_Azure_iteration2/SF=10/Query_times_10_2.txt",
    r"Benchmark_Azure_iteration2/SF=10/Query_times_10_3.txt",
    r"Benchmark_Azure_iteration2/SF=10/Query_times_10_4.txt",
    r"Benchmark_Azure_iteration2/SF=10/Query_times_10_5.txt",
    r"Benchmark_Azure_iteration2/SF=10/Query_times_10_6.txt",
    r"Benchmark_Azure_iteration2/SF=10/Query_times_10_7.txt",
    r"Benchmark_Azure_iteration2/SF=10/Query_times_10_8.txt",
    r"Benchmark_Azure_iteration2/SF=10/Query_times_10_9.txt"
]

file_paths_100 = [
    r"Benchmark_Azure_iteration2/SF=100/Query_times_100_0.txt",
    r"Benchmark_Azure_iteration2/SF=100/Query_times_100_1.txt",
    r"Benchmark_Azure_iteration2/SF=100/Query_times_100_2.txt",
    r"Benchmark_Azure_iteration2/SF=100/Query_times_100_3.txt",
    r"Benchmark_Azure_iteration2/SF=100/Query_times_100_4.txt",
    r"Benchmark_Azure_iteration2/SF=100/Query_times_100_5.txt",
    r"Benchmark_Azure_iteration2/SF=100/Query_times_100_6.txt",
    r"Benchmark_Azure_iteration2/SF=100/Query_times_100_7.txt",
    r"Benchmark_Azure_iteration2/SF=100/Query_times_100_8.txt",
    r"Benchmark_Azure_iteration2/SF=100/Query_times_100_9.txt"
]

file_paths_1000 = [
    r"Benchmark_Azure_iteration2/SF=1000/Query_times_1000_0.txt",
    r"Benchmark_Azure_iteration2/SF=1000/Query_times_1000_1.txt",
    r"Benchmark_Azure_iteration2/SF=1000/Query_times_1000_2.txt",
    r"Benchmark_Azure_iteration2/SF=1000/Query_times_1000_3.txt",
    r"Benchmark_Azure_iteration2/SF=1000/Query_times_1000_4.txt",
    r"Benchmark_Azure_iteration2/SF=1000/Query_times_1000_5.txt",
    r"Benchmark_Azure_iteration2/SF=1000/Query_times_1000_6.txt",
    r"Benchmark_Azure_iteration2/SF=1000/Query_times_1000_7.txt",
    r"Benchmark_Azure_iteration2/SF=1000/Query_times_1000_8.txt",
    r"Benchmark_Azure_iteration2/SF=1000/Query_times_1000_9.txt"
]

# Initialize dictionaries to store the total time and count for each query for each scale factor
total_time_10, total_time_100, total_time_1000 = {}, {}, {}
count_10, count_100, count_1000 = {}, {}, {}

transaction_10, transaction_100, transaction_1000 = [], [], []

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
process_files(file_paths_10, total_time_10, count_10)
process_files(file_paths_100, total_time_100, count_100)
process_files(file_paths_1000, total_time_1000, count_1000)

# Calculate the average time for each query for each scale factor
average_time_10 = {query: time / count_10[query] for query, time in total_time_10.items()}
average_time_100 = {query: time / count_100[query] for query, time in total_time_100.items()}
average_time_1000 = {query: time / count_1000[query] for query, time in total_time_1000.items()}

# Compute transactions per minute for each scale factor
tpm_10 = [compute_transactions_per_minute(transaction_10[i], time) for i, (query, time) in enumerate(average_time_10.items())]
tpm_100 = [compute_transactions_per_minute(transaction_100[i], time) for i, (query, time) in enumerate(average_time_100.items())]
tpm_1000 = [compute_transactions_per_minute(transaction_1000[i], time) for i, (query, time) in enumerate(average_time_1000.items())]

# Get the average times for each scale factor and sort the element
average_times_10 = [time for query, time in average_time_10.items()]
avg10 = sorted(average_times_10)

average_times_100 = [time for query, time in average_time_100.items()]
avg100 = sorted(average_times_100)

average_times_1000 = [time for query, time in average_time_1000.items()]
avg1000=sorted(average_times_1000)


# Create a new figure
plt.figure()

# Plot transactions per minute for scale factor 10
plt.plot(avg10, tpm_10, label='Scale factor 10')
#plt.plot(avg10[:len(smooth_tpm_10)], smooth_tpm_10, label='Scale factor 10')


# Plot transactions per minute for scale factor 100
plt.plot(avg100, tpm_100, label='Scale factor 100')

# Plot transactions per minute for scale factor 1000
plt.plot(avg1000, tpm_1000, label='Scale factor 1000')

# Add a legend
plt.legend()

# Add labels for the x and y axes
plt.xlabel('Average Time (seconds)')
plt.ylabel('Transactions per Minute')



# Show the plot
plt.show()

