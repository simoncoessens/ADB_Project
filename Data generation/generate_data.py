import psycopg2
from psycopg2 import extras
from faker import Faker
import random
import csv
import geopy
import time
import os
fake = Faker()


def generate_data(scale):
    # Initialize the data containers for each table
    users_data = []
    vehicles_data = []
    drivers_data = []
    payments_data = []
    rides_data = []
    refused_rides_data = []

    number_of_users = 10*scale
    number_of_drivers = scale
    number_of_rides = 100*scale

    # Generate data for the vehicle table
    for vehicle_id in range(1, number_of_drivers + 1):
        vehicle = {
            'vehicle_id': vehicle_id,
            'licence_plate_num': fake.license_plate(),
            'manufacturer': fake.company(),
            'model': fake.word(),
            'manifacture_year': random.randint(1990, 2023),
            'car_policy_num': fake.bban(),
            'car_type': random.choice(['normal', 'high']),
            'fuel': random.choice(['diesel', 'electric', 'hybrid']),
            'seats_num': random.randint(2, 8),
            'kids_seats_num': random.randint(0, 2),
            'wheelchair_seat': bool(random.getrandbits(1))  # Random True/False for boolean field
        }
        vehicles_data.append(vehicle)

    # Generate data for the user table
    # Here we create 10 times more users that there are drivers
    for user_id in range(1, number_of_users + 1):
        user = {
            'user_id': user_id,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=70),
            'residence': fake.city(),
            'email': fake.email(),
            'phone_number': fake.phone_number(),
            'passw': fake.password(length=10),
            'account_status': random.choice(['active', 'disabled']),
            'rating': random.randint(1, 5),
            'nrating': random.randint(1, 400)
        }
        users_data.append(user)

    # Generate data for the driver table
    for driver_id in range(1, number_of_drivers + 1):
        vehicle = vehicles_data[driver_id - 1]  # Match each driver with a vehicle
        driver = {
            'driver_id': driver_id,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'driver_status': random.choice(['available', 'unavailable', 'disabled']),
            'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=70),
            'place_of_birth': fake.city(),
            'place_of_residence': fake.city(),
            'nationality': fake.country(),
            'email': fake.email(),
            'phone_number': fake.phone_number(),
            'licence_id': fake.random_int(min=1000, max=9999),
            'taxi_licence_id': fake.random_int(min=10000, max=99999),
            'rating': random.randint(1, 5),
            'vehicle_id': vehicle['vehicle_id'],  # Assign vehicle to driver
            'join_date': fake.date_between(start_date="-5y", end_date="today"),
            'passw': fake.password(length=10),
            'nrating': random.randint(1, 400)
        }
        drivers_data.append(driver)

    # Generate data for the payment table
    # We create 100 times the scale number of rides
    for payment_id in range(1, number_of_rides + 1):
        payment = {
            'payment_id': payment_id,
            'payment_type': random.choice(['cash', 'card', 'gift', 'mix']),
            'fare_amount': random.randint(5, 500),
            'promo_code': fake.bothify(text='?????-#####') if random.choice([True, False]) else ""
        }
        payments_data.append(payment)

    # Generate data for the ride table
    for ride_id in range(1, number_of_rides + 1):
        payment = payments_data[ride_id - 1]  # Match each ride with a payment
        ride = {
            'ride_id': ride_id,
            'driver_id': random.randint(1, number_of_drivers),
            'user_id': random.randint(1, number_of_users),
            'ride_status': random.choice(['completed', 'cancelled', 'no_show']),
            'request_code': fake.random_int(min=10000, max=99999),
            'pickup_location_lat': random_coordinates_within_nyc_lat(),
            'pickup_location_lon': random_coordinates_within_nyc_lon(),
            'dropoff_location_lat': random_coordinates_within_nyc_lat(),
            'dropoff_location_lon': random_coordinates_within_nyc_lon(),
            'request_date': fake.date_between(start_date="-1y", end_date="today"),
            'pickup_date': fake.date_time_this_year(before_now=True, after_now=False),
            'dropoff_date': fake.date_time_this_year(before_now=True, after_now=False),
            'ride_rating': random.randint(1, 5),
            'payment_id': payment['payment_id'],
            'passengers_num': random.randint(1, 4)
        }
        rides_data.append(ride)

    # If you want to generate refused rides data, uncomment this section and make
    cancelled_rides = [ride for ride in rides_data if ride['ride_status'] == 'cancelled']

    for ride in cancelled_rides:
        # Assuming that each driver has a chance to refuse a ride
        possible_drivers = [driver for driver in drivers_data if driver['driver_id'] != ride['driver_id']]
        if possible_drivers:
            driver_id = random.choice(possible_drivers)['driver_id']
            refused_rides_data.append({
                'ride_id': ride['ride_id'],
                'driver_id': driver_id,
            })
        # Now return all the data
    return {
        'Users': users_data,
        'Vehicles': vehicles_data,
        'Drivers': drivers_data,
        'Payments': payments_data,
        'Rides': rides_data,
        'HasRefusedRides': refused_rides_data
    }

def random_coordinates_within_nyc_lat():
    lat_min, lat_max = 40.477399, 40.917577
    return random.uniform(lat_min, lat_max)

def random_coordinates_within_nyc_lon():
    lon_min, lon_max = -74.259090, -73.700272
    return random.uniform(lon_min, lon_max)

def write_data_to_csv(data_function, scale):
    # Generate the data using the provided function
    data = data_function(scale)

    # Prepare the CSV file parameters
    csv_info = {
        'Users': ('users.csv', ['user_id', 'first_name', 'last_name', 'date_of_birth', 'residence', 'email', 'phone_number', 'passw', 'account_status', 'rating', 'nrating']),
        'Vehicles': ('vehicles.csv', ['vehicle_id', 'licence_plate_num', 'manufacturer', 'model', 'manifacture_year', 'car_policy_num', 'car_type', 'fuel', 'seats_num', 'kids_seats_num', 'wheelchair_seat']),
        'Drivers': ('drivers.csv', ['driver_id', 'first_name', 'last_name', 'driver_status', 'date_of_birth', 'place_of_birth', 'place_of_residence', 'nationality', 'email', 'phone_number', 'licence_id', 'taxi_licence_id', 'rating', 'vehicle_id', 'join_date', 'passw', 'nrating']),
        'Payments': ('payments.csv', ['payment_id', 'payment_type', 'fare_amount', 'promo_code']),
        'Rides': ('rides.csv', ['ride_id', 'driver_id', 'user_id', 'ride_status', 'request_code', 'pickup_location_lat', 'pickup_location_lon','dropoff_location_lat', 'dropoff_location_lon', 'request_date', 'pickup_date', 'dropoff_date', 'ride_rating', 'payment_id', 'passengers_num']),
        'HasRefusedRides': ('refused_rides.csv', ['ride_id', 'driver_id'])
    }

    # Write data to CSV files for each category
    for category, (filename, headers) in csv_info.items():
        with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()  # Write the headers first
            writer.writerows(data[category])  # Write the data rows

    print('Data written to CSV files successfully.')

def copy_from_csv(table_name, csv_file_path):
    # Establish a connection to the database
    conn_local = psycopg2.connect(
        dbname='myride_transactional_db',
        user='postgres',
        password='datamining',
        host='localhost',
        port=5433
    )

    #conn_gcloud = psycopg2.connect(
    #    dbname = 'myride_transactional_db',
    #    user = 'postgres',
    #    password = '6x*i3MNUa*L6vRJYr#DJjsEufe7',
    #    host = '35.184.55.57',
    #    port = 5432
    #)

    # Local conection Maria Camila
    #conn_azure = psycopg2.connect(
    #     dbname='myride_transactional_db',
    #     user='Maria',
    #     password='Advance10+',
    #     host="db-project.postgres.database.azure.com",
    #     port=5432
    #)
    
    conn_local.autocommit = True
    cur = conn_local.cursor()

    with open(csv_file_path, 'r') as f:
        cur.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV HEADER DELIMITER ','", f)

def create_database(sql_file):
    # Establish a connection to the database
    #Conection for azure
    conn = psycopg2.connect(
        dbname='proyecto',
        user='postgres',
        password='postgres',
        host="localhost",
        #port=5433
    )
    # Local conection Maria Camila
    # conn = psycopg2.connect(
    #     dbname='myride_transactional_db',
    #     user='postgres',
    #     password='postgres',
    #     host="localhost",
    #     #port=5433
    # )

    conn.autocommit = True
    cur = conn.cursor()

    sql_filename = sql_file
    with open(sql_filename, 'r') as file:
        sql_query = file.read()
    cur.execute(sql_query)

def fill_database(scale):
    tables = [
    {'name': 'users','file': 'users.csv'},
    {'name': 'vehicles','file': 'vehicles.csv'},
    {'name': 'drivers','file': 'drivers.csv'},
    {'name': 'payments','file': 'payments.csv'},
    {'name': 'rides','file': 'rides.csv'},
    
]
    csv_filename = f"Loading_time_{scale}.csv"
    with open(csv_filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['table_name', 'elapsed_time'])


            for table in tables:
                table_name = table['name']
                file = table['file']
                
                start_time = time.time()
                copy_from_csv(table_name,file)
                elapsed_time = time.time() - start_time
                print (table_name,elapsed_time)
                # Guardar el tiempo de ejecución en un archivo CSV
                csv_writer.writerow([table_name, elapsed_time])
    conn = psycopg2.connect(
       dbname='proyecto',
       user='postgres',
       password='postgres',
       host="localhost",
       #port=5433
    )


    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("""
            SELECT pg_size_pretty(pg_database_size(current_database())) AS size;
        """)
    total_database_size = cur.fetchone()[0]
    return print(f"Total_size: {total_database_size}")

def calculate_csv_size(scale):
    # Generate data and write to CSV
    write_data_to_csv(generate_data, scale)

    # List of CSV files
    csv_files = ['users.csv', 'vehicles.csv', 'drivers.csv', 'payments.csv', 'rides.csv']

    # Calculate total size of CSV files in bytes
    total_size_bytes = sum(os.path.getsize(f) for f in csv_files if os.path.isfile(f))

    # Convert size to gigabytes
    total_size_gb = total_size_bytes / (1024**3)

    # Clean up: remove the CSV files after calculating size
    #for f in csv_files:
    #    if os.path.exists(f):
    #        os.remove(f)

    return total_size_gb


# Example Usage

#write_data_to_csv(generate_data, 100)

# Usage
# 0. Create database.
# 1. Generate the data and write to csv with: write_data_to_csv(generate_data, 100).
# 2. run copy_from_csv to push data to db, copy_from_csv( 'costumer', 'users.csv').

scale=10
#write_data_to_csv(generate_data, scale)
#copy_from_csv( 'users', 'users.csv')
##copy_from_csv( 'vehicles', 'vehicles.csv')
#copy_from_csv( 'drivers', 'drivers.csv')
#copy_from_csv('payments','payments.csv')
#copy_from_csv('rides','rides.csv')
#create_database("../adb_create_database_valerio.sql")
#fill_database(scale)

print("Number of GB:")
print(calculate_csv_size(20000))




