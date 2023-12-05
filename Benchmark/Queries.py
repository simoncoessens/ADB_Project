import psycopg2
import sched, time
import numpy as np
import sqlalchemy
import csv
import pandas as pd


def workload(scale,conexion):
    durations=[]
    scale_driver = scale
    scale_rides = 100*scale
    scale_payment = scale
    scale_user = 10*scale
    scale_vehicle = scale

    

    conn = conexion
    conn.autocommit = True
    cur = conn.cursor()

    print('Query1')
    query = """
    UPDATE drivers
    SET driver_status = 2
    WHERE driver_id = %s;
    """
    start_time = time.time()
    for i in range(scale_driver):
        cur.execute(query, (i+1,))
    conn.commit()
    duration = time.time() - start_time
    durations.append({'Query1': duration})
    
    print('Query2')
    query = """
    select * from areas;
    """
    start_time = time.time()
    cur.execute(query)
    conn.commit()
    duration = time.time() - start_time
    durations.append({'Query2': duration})

    print('Query3')
    query = """
    SELECT ride_id,
    ST_Distance(pickup_location::geography, dropoff_location::geography) AS distance_meters
    FROM rides;
    """
    start_time = time.time()
    cur.execute(query)
    conn.commit()
    duration = time.time() - start_time
    durations.append({'Query3': duration})

    print('Query4')
    query = """
    SELECT ride_id,
    pickup_location
    FROM rides
    WHERE ST_DWithin(pickup_location, ST_MakePoint(-73.9851, 40.7589)::geography, 1000);
    """
    start_time = time.time()
    cur.execute(query)
    conn.commit()
    duration = time.time() - start_time
    durations.append({'Query4': duration})

    print('Query5')
    query = """
    SELECT count(*)
    FROM rides
    WHERE ST_Contains(
        (SELECT ST_SetSRID(geom, 4326) FROM areas WHERE id = 1),
        ST_SetSRID(pickup_location, 4326)
    );
    """
    start_time = time.time()
    cur.execute(query)
    conn.commit()
    duration = time.time() - start_time
    durations.append({'Query5': duration})

    print('Query6')
    query = """
    SELECT ride_id
    FROM rides
    WHERE ST_Distance(pickup_location::geography, dropoff_location::geography) > 5000;
    """
    start_time = time.time()
    cur.execute(query)
    conn.commit()
    duration = time.time() - start_time
    durations.append({'Query6': duration})

    print('Query7')
    query = """
    SELECT ride_id
    FROM rides
    WHERE ST_Contains(
        (SELECT ST_SetSRID(geom, 4326) FROM areas WHERE id = '1'),
        ST_SetSRID(pickup_location, 4326)
    );
    """
    start_time = time.time()
    cur.execute(query)
    conn.commit()
    duration = time.time() - start_time
    durations.append({'Query7': duration})

    print('Query8')
    query = """
    SELECT driver_id, AVG(ST_Distance(pickup_location, dropoff_location)) as avg_distance
    FROM rides
    GROUP BY driver_id;
    """
    start_time = time.time()
    cur.execute(query)
    conn.commit()
    duration = time.time() - start_time
    durations.append({'Query8': duration})

    print('Query9')
    query = """
    SELECT d.driver_id, d.first_name, d.last_name, AVG(ST_Distance(r.pickup_location::geography, r.dropoff_location::geography)) AS avg_distance
    FROM drivers d
    JOIN rides r ON d.driver_id = r.driver_id
    GROUP BY d.driver_id;
    """
    start_time = time.time()
    cur.execute(query)
    conn.commit()
    duration = time.time() - start_time
    durations.append({'Query9': duration})

    print('Query10')
    query = """
    WITH AreaBoundary AS (
        SELECT ST_SetSRID(geom, 4326) AS geom FROM areas WHERE id = 1
    )
    SELECT r.ride_id
    FROM rides r, AreaBoundary ab
    WHERE ST_Crosses(ST_SetSRID(ST_MakeLine(r.pickup_location, r.dropoff_location), 4326), ab.geom);

    """
    start_time = time.time()
    cur.execute(query)
    conn.commit()
    duration = time.time() - start_time
    durations.append({'Query10': duration})

    print('Query11')
    query = """
    SELECT v.vehicle_id, SUM(ST_Distance(r.pickup_location, r.dropoff_location)) AS total_distance
    FROM vehicles v, rides r, drivers d
    WHERE r.driver_id = d.driver_id AND v.vehicle_id = d.driver_id
    GROUP BY v.vehicle_id;
    """
    start_time = time.time()
    cur.execute(query)
    conn.commit()
    duration = time.time() - start_time
    durations.append({'Query11': duration})

    print('Query12')
    query = """
    SELECT a.name_g, COUNT(r.ride_id) AS pickup_count
    FROM areas a
    JOIN rides r ON ST_Contains(a.geom, ST_SetSRID(r.pickup_location, 4326))
    GROUP BY a.name_g
    ORDER BY pickup_count DESC;

    """
    start_time = time.time()
    cur.execute(query)
    conn.commit()
    duration = time.time() - start_time
    durations.append({'Query12': duration})

    print('Query13')
    query = """
    SELECT v.car_type, MAX(ST_Distance(r.pickup_location::geography, r.dropoff_location::geography)) AS longest_ride
    FROM vehicles v, rides r, drivers d
    WHERE r.driver_id = d.driver_id and  v.vehicle_id = d.vehicle_id
    GROUP BY v.car_type;

    """
    start_time = time.time()
    cur.execute(query)
    conn.commit()
    duration = time.time() - start_time
    durations.append({'Query13': duration})

    print('Query14')
    query = """
    SELECT u.user_id, u.first_name, u.last_name
    FROM users u
    WHERE NOT EXISTS (
    SELECT 1 FROM rides r, vehicles v, drivers d
        WHERE r.driver_id = d.driver_id and  v.vehicle_id = d.vehicle_id
        AND u.user_id = r.user_id AND v.car_type = 'high'
    );

    """
    start_time = time.time()
    cur.execute(query)
    conn.commit()
    duration = time.time() - start_time
    durations.append({'Query14': duration})

    print('Query15')
    query = """
    SELECT a.name_g, COUNT(r.ride_id) AS pickup_count
    FROM areas a
    JOIN rides r ON ST_Contains(a.geom, ST_SetSRID(r.pickup_location, 4326))
    WHERE a.name_g = 'Rancio - Laorca'
    GROUP BY a.name_g
    ORDER BY pickup_count DESC;


    

    """
    start_time = time.time()
    cur.execute(query)
    conn.commit()
    duration = time.time() - start_time
    durations.append({'Query15': duration})

    filename = f'Query_times_{scale}.txt'

    # Save the results to a CSV file
    with open(filename, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        for value in durations:
            writer.writerow([value])  # Escribe cada valor en una fila separada

    print('Times saved')
    return filename




    
