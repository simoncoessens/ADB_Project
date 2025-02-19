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
            'driver_id': random.randint(1, number_of_drivers - 1),
            'user_id': random.randint(1, number_of_users - 1),
            'ride_status': random.choice(['completed', 'cancelled', 'no_show']),
            'request_code': fake.random_int(min=10000, max=99999),
            'pickup_location_lat': random_coordinates_within_lecco_lat(),
            'pickup_location_lon': random_coordinates_within_lecco_lon(),
            'dropoff_location_lat': random_coordinates_within_lecco_lat(),
            'dropoff_location_lon': random_coordinates_within_lecco_lon(),
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

def random_coordinates_within_lecco_lat():
    lat_min, lat_max = 45.812884, 45.898247
    return random.uniform(lat_min, lat_max)

def random_coordinates_within_lecco_lon():
    lon_min, lon_max = 9.361704, 9.452684
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

