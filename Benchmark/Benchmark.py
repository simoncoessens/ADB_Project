import generate_data as gd
import create_database as cdb
import push_database as pdb
import times 
import Queries
import delete_csv
import psycopg2
from psycopg2 import extras
import os

local_mc=psycopg2.connect(
        dbname='proyecto',
        user='postgres',
        password='postgres',
        host='localhost',
        port=5432
    )

# conn_gcloud = psycopg2.connect(
#     dbname='myride_transactional_db',
#     user='postgres',
#     password='6x*i3MNUa*L6vRJYr#DJjsEufe7',
#     host='35.184.55.57',
#     port=5432
# )


# conn_azure = psycopg2.connect(
#         dbname='myride_transactional_db',
#         user='Maria',
#         password='Advance10+',
#         host="db-project.postgres.database.azure.com",
#         port=5432
# )

#Parameters
scales = [10]
conexion=local_mc


delete_csv.delete_txt(os.getcwd())
for scale in scales:
    for i in range(15):
        print(f"{scale} starts")
        file= f"results_{scale}_{i}"

        times.t(gd.write_data_to_csv, [gd.generate_data, scale], f'{file}_{i}.txt')
        times.t(cdb.create_database, ["adb_create_database.sql", conexion], f'{file}_{i}.txt')
        times.t(pdb.push_to_db_from_csv, ['users.csv', 'users', conexion],f'{file}_{i}.txt')
        times.t(pdb.push_to_db_from_csv, ['vehicles.csv', 'vehicles', conexion], f'{file}_{i}.txt')
        times.t(pdb.push_to_db_from_csv, ['drivers.csv', 'drivers', conexion], f'{file}_{i}.txt')
        times.t(pdb.push_to_db_from_csv, ['payments.csv', 'payments', conexion], f'{file}_{i}.txt')
        times.t(pdb.push_to_db_from_csv, ['rides.csv', 'rides', conexion], f'{file}_{i}.txt')
        delete_csv.delete_csv(os.getcwd())
        Queries.workload(scale,conexion,i)
        print(f"{scale} finished")
