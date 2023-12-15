import psycopg2
from psycopg2 import extras
from faker import Faker
import random
import csv
import geopy
import time
import os
fake = Faker()


def create_database(sql_file,conexion):

    conn = conexion

    conn.autocommit = True
    cur = conn.cursor()

    sql_filename = sql_file
    with open(sql_filename, 'r') as file:
        sql_query = file.read()
    cur.execute(sql_query)
    print ('database created succesfully')