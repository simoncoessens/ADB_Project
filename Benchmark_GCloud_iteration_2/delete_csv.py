import os
import glob

def delete_csv (path):
    # Specify the directory where CSV files are located
    directory = path

    # Use the glob module to find all CSV files in the directory
    csv_files = glob.glob(os.path.join(directory, '*.csv'))

    # Remove each found CSV file
    for csv_file in csv_files:
        os.remove(csv_file)

    print("CSV files successfully deleted.")

def delete_txt (path):
    # Specify the directory where CSV files are located
    directory = path

    # Use the glob module to find all CSV files in the directory
    csv_files = glob.glob(os.path.join(directory, '*.txt'))

    # Remove each found CSV file
    for csv_file in csv_files:
        os.remove(csv_file)

    print("txt files successfully deleted.")