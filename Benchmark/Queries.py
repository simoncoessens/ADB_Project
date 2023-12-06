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
    
    transaction_count = 0  # Inicializar el contador de transacciones

    start_time = time.time()
    for i in range(scale_driver):
        cur.execute(query, (i+1,))
        transaction_count += 1

    conn.commit()
    duration = time.time() - start_time
    durations.append(['Query1', duration,transaction_count])
    
    # print('Query2')
    # query = """
    # select * from areas;
    # """
    # transaction_count = 0  # Inicializar el contador de transacciones
    # start_time = time.time()
    # cur.execute(query)
    # transaction_count += 1
    # conn.commit()
    # transaction_count = 0  # Inicializar el contador de transacciones
    # duration = time.time() - start_time
    # durations.append(['Query2', duration,transaction_count])
    
    print('Query3')
    query = """
    SELECT ride_id,
    ST_Distance(pickup_location::geography, dropoff_location::geography) AS distance_meters
    FROM rides;
    """
    


    transaction_count = 0  # Inicializar el contador de transacciones
    start_time = time.time()
    cur.execute(query)
    transaction_count += 1
    conn.commit()
    duration = time.time() - start_time
    durations.append(['Query3', duration,transaction_count])
    
    print('Query4')
    query = """
    SELECT ride_id,
    pickup_location
    FROM rides
    WHERE ST_DWithin(pickup_location, ST_MakePoint(-73.9851, 40.7589)::geography, %s);
    """
    distances=[100,500,1000]
    transaction_count = 0  # Inicializar el contador de transacciones

    start_time = time.time()
    for i in distances:
        cur.execute(query, (i+1,))
        transaction_count += 1

    conn.commit()
    duration = time.time() - start_time
    durations.append(['Query4', duration,transaction_count])
    
    print('Query5')
    query = """
    SELECT count(*)
    FROM rides
    WHERE ST_Contains(
        (SELECT ST_SetSRID(geom, 4326) FROM areas WHERE id = %s),
        ST_SetSRID(pickup_location, 4326)
    );
    """
    transaction_count = 0  # Inicializar el contador de transacciones

    start_time = time.time()
    for i in range(22):
        cur.execute(query, (i+1,))
        transaction_count += 1
    conn.commit()
    duration = time.time() - start_time
    durations.append(['Query5', duration,transaction_count])
    
    print('Query6')
    query = """
    SELECT ride_id
    FROM rides
    WHERE ST_Distance(pickup_location::geography, dropoff_location::geography) > %s;
    """
    distances=[1000,2000,3000,4000,5000]
    transaction_count = 0  # Inicializar el contador de transacciones

    start_time = time.time()
    for i in distances:
        cur.execute(query, (i+1,))
        transaction_count += 1
    conn.commit()
    duration = time.time() - start_time
    durations.append(['Query6', duration,transaction_count])
    
    print('Query7')
    query = """
    SELECT ride_id
    FROM rides
    WHERE ST_Contains(
        (SELECT ST_SetSRID(geom, 4326) FROM areas WHERE id = %s),
        ST_SetSRID(pickup_location, 4326)
    );
    """
    transaction_count = 0  # Inicializar el contador de transacciones

    start_time = time.time()
    for i in range(22):
        cur.execute(query, (i+1,))
        transaction_count += 1
    conn.commit()
    duration = time.time() - start_time
    durations.append(['Query7', duration,transaction_count])
    
    print('Query8')
    query = """
    SELECT driver_id, AVG(ST_Distance(pickup_location, dropoff_location)) as avg_distance
    FROM rides
    GROUP BY driver_id;
    """
    transaction_count = 0  # Inicializar el contador de transacciones
    start_time = time.time()
    cur.execute(query)
    transaction_count += 1
    conn.commit()
    duration = time.time() - start_time
    durations.append(['Query8', duration,transaction_count])
    
    print('Query9')
    query = """
    SELECT d.driver_id, d.first_name, d.last_name, AVG(ST_Distance(r.pickup_location::geography, r.dropoff_location::geography)) AS avg_distance
    FROM drivers d
    JOIN rides r ON d.driver_id = r.driver_id
    GROUP BY d.driver_id;
    """
    transaction_count = 0  # Inicializar el contador de transacciones
    start_time = time.time()
    cur.execute(query)
    transaction_count += 1
    conn.commit()
    duration = time.time() - start_time
    durations.append(['Query9', duration,transaction_count])
    
    print('Query10')
    query = """
    WITH AreaBoundary AS (
        SELECT ST_SetSRID(geom, 4326) AS geom FROM areas WHERE id = %s
    )
    SELECT r.ride_id
    FROM rides r, AreaBoundary ab
    WHERE ST_Crosses(ST_SetSRID(ST_MakeLine(r.pickup_location, r.dropoff_location), 4326), ab.geom);

    """
    transaction_count = 0  # Inicializar el contador de transacciones
    start_time = time.time()
    for i in range(22):
        cur.execute(query, (i+1,))
        transaction_count += 1
    conn.commit()
    duration = time.time() - start_time
    durations.append(['Query10', duration,transaction_count])
    
    print('Query11')
    query = """
    SELECT v.vehicle_id, SUM(ST_Distance(r.pickup_location, r.dropoff_location)) AS total_distance
    FROM vehicles v, rides r, drivers d
    WHERE r.driver_id = d.driver_id AND v.vehicle_id = d.driver_id
    GROUP BY v.vehicle_id;
    """
    transaction_count = 0  # Inicializar el contador de transacciones
    start_time = time.time()
    cur.execute(query)
    transaction_count += 1
    conn.commit()
    duration = time.time() - start_time
    durations.append(['Query11', duration,transaction_count])
    
    print('Query12')
    query = """
    SELECT a.name_g, COUNT(r.ride_id) AS pickup_count
    FROM areas a
    JOIN rides r ON ST_Contains(a.geom, ST_SetSRID(r.pickup_location, 4326))
    GROUP BY a.name_g
    ORDER BY pickup_count DESC;

    """
    transaction_count = 0  # Inicializar el contador de transacciones
    start_time = time.time()
    cur.execute(query)
    transaction_count += 1
    conn.commit()
    duration = time.time() - start_time
    durations.append(['Query12', duration,transaction_count])
    
    print('Query13')
    query = """
    SELECT v.car_type, MAX(ST_Distance(r.pickup_location::geography, r.dropoff_location::geography)) AS longest_ride
    FROM vehicles v, rides r, drivers d
    WHERE r.driver_id = d.driver_id and  v.vehicle_id = d.vehicle_id
    GROUP BY v.car_type;

    """
    transaction_count = 0  # Inicializar el contador de transacciones
    start_time = time.time()
    cur.execute(query)
    transaction_count += 1
    conn.commit()
    duration = time.time() - start_time
    durations.append(['Query13', duration,transaction_count])
    
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
    transaction_count = 0  # Inicializar el contador de transacciones
    start_time = time.time()
    cur.execute(query)
    transaction_count += 1
    conn.commit()
    duration = time.time() - start_time
    durations.append(['Query14', duration,transaction_count])
    
    print('Query15')
    query = """
    SELECT a.name_g, COUNT(r.ride_id) AS pickup_count
    FROM areas a
    JOIN rides r ON ST_Contains(a.geom, ST_SetSRID(r.pickup_location, 4326))
    WHERE a.name_g = 'Rancio - Laorca'
    GROUP BY a.name_g
    ORDER BY pickup_count DESC;
    """
    transaction_count = 0  # Inicializar el contador de transacciones
    start_time = time.time()
    cur.execute(query)
    transaction_count += 1
    conn.commit()
    duration = time.time() - start_time
    durations.append(['Query15', duration,transaction_count])
    
    print('Query16')
    query = """
    INSERT INTO rides (
        ride_id, driver_id, user_id, ride_status, request_code,
        pickup_location,dropoff_location,request_date, pickup_date, dropoff_date,
        ride_rating, payment_id, passengers_num
    ) VALUES (
        %s, 3, 56, 'TEST', 27164,
        ST_MakePoint(40.89911326259291, -74.19879968),
        ST_MakePoint(40.89119552115688, -73.78466389),
        '2023-05-04', '2023-07-07 20:03', '2023-08-23 07:54',
        4, 1, 2
    );
    """

    transaction_count = 0  # Inicializar el contador de transacciones
    start_time = time.time()
    for i in range(scale_rides, scale_rides+100):
        cur.execute(query, (i+1,))
        transaction_count += 1
    conn.commit()
    duration = time.time() - start_time
    durations.append(['Query16', duration,transaction_count])

    print('Query17')
    query = """
    INSERT INTO rides (
        ride_id, driver_id, user_id, ride_status, request_code,
        pickup_location,dropoff_location,request_date, pickup_date, dropoff_date,
        ride_rating, payment_id, passengers_num
    ) VALUES (
        %s, 3, 56, 'TEST', 27164,
        ST_MakePoint(40.89911326259291, -74.19879968),
        ST_MakePoint(40.89119552115688, -73.78466389),
        '2023-05-04', '2023-07-07 20:03', '2023-08-23 07:54',
        4, 1, 2
    );
    """

    transaction_count = 0  # Inicializar el contador de transacciones
    start_time = time.time()
    for i in range(scale_rides+100, scale_rides+600):
        cur.execute(query, (i+1,))
        transaction_count += 1
    conn.commit()
    duration = time.time() - start_time
    durations.append(['Query17', duration,transaction_count])

    print('Query18')
    query = """
    INSERT INTO payments (
        payment_id, payment_type, fare_amount, promo_code
    ) VALUES (
        %s, 'cash', 415, 'TEST'

    );

    """
    transaction_count = 0  # Inicializar el contador de transacciones
    start_time = time.time()
    for i in range(scale_rides, scale_rides+100):
        cur.execute(query, (i+1,))
        transaction_count += 1
    conn.commit()
    duration = time.time() - start_time
    durations.append(['Query18', duration,transaction_count])

    print('Query19')
    query = """
    UPDATE drivers
    SET
        rating = (rating * nrating + 5) / (nrating + 1),
        nrating = nrating + 1
    WHERE driver_id = %s;

    """
    transaction_count = 0  # Inicializar el contador de transacciones
    start_time = time.time()
    for i in range(scale_driver):
        cur.execute(query, (i+1,))
        transaction_count += 1
    conn.commit()
    duration = time.time() - start_time
    durations.append(['Query19', duration,transaction_count])

    print('Query20')
    query = """
    UPDATE drivers
    SET
        rating = (rating * nrating + 5) / (nrating + 1),
        nrating = nrating + 1
    WHERE driver_id = %s;

    """
    transaction_count = 0  # Inicializar el contador de transacciones
    start_time = time.time()
    for i in range(scale_driver, scale_driver+500):
        cur.execute(query, (i+1,))
        transaction_count += 1
    conn.commit()
    duration = time.time() - start_time
    durations.append(['Query20', duration,transaction_count])

    print('Query21')
    query = """
    UPDATE drivers
    SET
        rating = (rating * nrating + 5) / (nrating + 1),
        nrating = nrating + 1
    WHERE driver_id = %s;

    """
    transaction_count = 0  # Inicializar el contador de transacciones
    start_time = time.time()
    for i in range(scale_driver+500, scale_driver+1500):
        cur.execute(query, (i+1,))
        transaction_count += 1
    conn.commit()
    duration = time.time() - start_time
    durations.append(['Query21', duration,transaction_count])





    filename = f'Query_times_{scale}.txt'

    # Save the results to a CSV file
    with open(filename, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        for value in durations:
            writer.writerow([value])  # Escribe cada valor en una fila separada

    print('Times saved')
    return filename




    
