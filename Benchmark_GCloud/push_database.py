import psycopg2
from psycopg2 import extras
from faker import Faker
import random
import csv
import geopy
import time
import os
fake = Faker()


def push_to_db_from_csv(file_path, table_name,conexion):
    conn = conexion

    conn.autocommit = True
    cur = conn.cursor()

    try:
        if table_name != 'rides':
            with open(file_path, 'r', encoding='utf-8') as file:
                cur.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV HEADER DELIMITER ','", file)
        else:
            # Handle the 'rides' table specially for PostGIS types
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    cur.execute("""
                                    INSERT INTO rides (ride_id, driver_id, user_id, ride_status, request_code, pickup_location,  dropoff_location, request_date, pickup_date, dropoff_date, ride_rating, payment_id, passengers_num)
                                    VALUES (%s, %s, %s, %s, %s, ST_MakePoint(%s, %s), ST_MakePoint(%s, %s), %s, %s, %s, %s, %s, %s)
                                    
                                """, (
                        row['ride_id'], row['driver_id'], row['user_id'], row['ride_status'], row['request_code'],
                        row['pickup_location_lon'], row['pickup_location_lat'],
                        row['dropoff_location_lon'], row['dropoff_location_lat'],
                        row['request_date'], row['pickup_date'], row['dropoff_date'],
                        row['ride_rating'], row['payment_id'], row['passengers_num']
                    ))
        
        # Commit the transaction
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        print('Push Succesfully')
        cur.close()