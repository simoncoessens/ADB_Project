from time import perf_counter
import csv

# Function to measure the execution time of a task and write it to a CSV file
def t(task, parameters, csv_filename):
    start_time = perf_counter() 
    task(*parameters)  # Execute the task with the given parameters
    duration = perf_counter()  - start_time
    
    # Save the results to a CSV file
    with open(csv_filename, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([task.__name__, duration])

    return csv_filename

#time.perf_counter