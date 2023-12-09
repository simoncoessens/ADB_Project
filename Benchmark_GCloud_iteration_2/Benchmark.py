import generate_data as gd
import create_database as cdb
import push_database as pdb
import times
import Queries
import delete_csv
import psycopg2
from psycopg2 import extras
import os

#local_mc = psycopg2.connect(
#    dbname='ADB_db',
#    user='postgres',
#    password='datamining',
#    host='localhost',
#    port=5433
#)

conn_gcloud = psycopg2.connect(
     dbname='myride_transactional_db',
    user='postgres',
     password='6x*i3MNUa*L6vRJYr#DJjsEufe7',
     host='35.184.55.57',
     port=5432
)


#conn_azure = psycopg2.connect(
#         dbname='myrides_transactional_db',
#         user='simon',
#         password='6x*i3MNUa*L6vRJYr#DJjsEufe7',
#         host="simon-44.postgres.database.azure.com",
#         port=5432
#)

# Parameters
scales = [10,100,1000]
conexion = conn_gcloud

for scale in scales:
    filel = f"loading_{scale}"
    gd.write_data_to_csv(gd.generate_data, scale)
    times.t(cdb.create_database, ["adb_create_database.sql", conexion], f'{filel}.txt')
    times.t(pdb.push_to_db_from_csv, ['users.csv', 'users', conexion], f'{filel}.txt')
    times.t(pdb.push_to_db_from_csv, ['vehicles.csv', 'vehicles', conexion], f'{filel}.txt')
    times.t(pdb.push_to_db_from_csv, ['drivers.csv', 'drivers', conexion], f'{filel}.txt')
    times.t(pdb.push_to_db_from_csv, ['payments.csv', 'payments', conexion], f'{filel}.txt')
    times.t(pdb.push_to_db_from_csv, ['rides.csv', 'rides', conexion], f'{filel}.txt')
    for i in range(10):
        print(f"{scale} starts")
        file = f"results_{scale}_{i}"

        Queries.workload(scale, conexion, i)
        print(f"{scale} finished")
