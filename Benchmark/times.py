import time
import csv

# Function to measure the execution time of a task and write it to a CSV file
def t(task, parameters, csv_filename):
    start_time = time.time()
    task(*parameters)  # Execute the task with the given parameters
    duration = time.time() - start_time
    
    # Save the results to a CSV file
    with open(csv_filename, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([task.__name__, duration])

    return csv_filename
