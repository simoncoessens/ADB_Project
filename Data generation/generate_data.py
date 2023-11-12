import psycopg2
from psycopg2 import extras
from faker import Faker
import random
import csv
import geopy
fake = Faker()

def generate_data(scale):
    # Initialize the data containers for each table
    users_data = []
    vehicles_data = []
    drivers_data = []
    payments_data = []
    rides_data = []
    refused_rides_data = []

    # Generate data for the vehicle table
    for vehicle_id in range(1, scale + 1):
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
    for user_id in range(1, scale + 1):
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
            'rating': random.randint(1, 5)
        }
        users_data.append(user)

    # Generate data for the driver table
    for driver_id in range(1, scale + 1):
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
            'passw': fake.password(length=10)
        }
        drivers_data.append(driver)

    # Generate data for the payment table
    for payment_id in range(1, scale + 1):
        payment = {
            'payment_id': payment_id,
            'payment_type': random.choice(['cash', 'card', 'gift', 'mix']),
            'fare_amount': random.randint(5, 500),
            'promo_code': fake.bothify(text='?????-#####') if random.choice([True, False]) else ""
        }
        payments_data.append(payment)

    # Generate data for the ride table
    for ride_id in range(1, scale + 1):
        payment = payments_data[ride_id - 1]  # Match each ride with a payment
        ride = {
            'ride_id': ride_id,
            'driver_id': random.randint(1, scale),
            'user_id': random.randint(1, scale),
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
        'Users': ('users.csv', ['user_id', 'first_name', 'last_name', 'date_of_birth', 'residence', 'email', 'phone_number', 'passw', 'account_status', 'rating']),
        'Vehicles': ('vehicles.csv', ['vehicle_id', 'licence_plate_num', 'manufacturer', 'model', 'manifacture_year', 'car_policy_num', 'car_type', 'fuel', 'seats_num', 'kids_seats_num', 'wheelchair_seat']),
        'Drivers': ('drivers.csv', ['driver_id', 'first_name', 'last_name', 'driver_status', 'date_of_birth', 'place_of_birth', 'place_of_residence', 'nationality', 'email', 'phone_number', 'licence_id', 'taxi_licence_id', 'rating', 'vehicle_id', 'join_date', 'passw']),
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

def insert_data_to_db(host, dbname, user, password, port, data_function, scale):
    # Establish a connection to the database
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True
    cur = conn.cursor()

    try:
        # Call your data generation function
        users_data, vehicles_data, drivers_data, payments_data, rides_data, refused_rides_data = data_function(scale)

        # Define insert statements
        insert_users = "INSERT INTO costumer VALUES %s"
        insert_vehicles = "INSERT INTO vehicles VALUES %s"
        insert_drivers = "INSERT INTO drivers VALUES %s"
        insert_payments = "INSERT INTO payments VALUES %s"
        insert_rides = "INSERT INTO rides VALUES %s"
        insert_refused_rides = "INSERT INTO refused_rides VALUES %s"

        # Execute insert statements
        extras.execute_values(cur, insert_users, users_data)
        extras.execute_values(cur, insert_vehicles, vehicles_data)
        extras.execute_values(cur, insert_drivers, drivers_data)
        extras.execute_values(cur, insert_payments, payments_data)
        extras.execute_values(cur, insert_rides, rides_data)
        extras.execute_values(cur, insert_refused_rides, refused_rides_data)

        print("Data inserted successfully")

    except Exception as e:
        print("An error occurred:", e)
        conn.rollback()

    finally:
        cur.close()
        conn.close()


# Replace the 'your_generate_data' with your generate_data function name
#insert_data_to_db('localhost', 'ADB_db', 'postgres', 'datamining', 5433, generate_data, 10)
write_data_to_csv(generate_data, 100)