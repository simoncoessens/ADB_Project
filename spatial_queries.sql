select count(*) from rides;
-- SPATIAL QUERIES
select * from areas;

-- give the distance between pickup and dropoff for all locations
SELECT ride_id,
       ST_Distance(pickup_location::geography, dropoff_location::geography) AS distance_meters
FROM rides;

-- give all the rides within a certain radius from a point
SELECT ride_id,
       pickup_location
FROM rides
WHERE ST_DWithin(pickup_location, ST_MakePoint(-73.9851, 40.7589)::geography, 1000);

-- Count the Number of Rides that Start and End Within a Certain Area: (here id = 1: Rancio - Laorca)
SELECT count(*)
FROM rides
WHERE ST_Contains((SELECT geom FROM areas WHERE id = 1), pickup_location);

-- Rides longer than a certain distance
SELECT ride_id
FROM rides
WHERE ST_Distance(pickup_location::geography, dropoff_location::geography) > 5000;

-- Rides Originating in a Specific Area and Ending in Another:
SELECT ride_id
FROM rides
WHERE ST_Contains((SELECT geom FROM areas WHERE id = '1'), pickup_location);

-- Average Distance of Rides for a Specific Driver:
SELECT driver_id, AVG(ST_Distance(pickup_location, dropoff_location)) as avg_distance
FROM rides
GROUP BY driver_id;

-- Find Average Distance Travelled by Each Driver:
SELECT d.driver_id, d.first_name, d.last_name, AVG(ST_Distance(r.pickup_location::geography, r.dropoff_location::geography)) AS avg_distance
FROM drivers d
JOIN rides r ON d.driver_id = r.driver_id
GROUP BY d.driver_id;

-- List All Rides That Cross a Specific Area:
WITH AreaBoundary AS (
  SELECT geom FROM areas WHERE id = 1
)
SELECT r.ride_id
FROM rides r, AreaBoundary ab
WHERE ST_Crosses(ST_MakeLine(r.pickup_location, r.dropoff_location), ab.geom);

-- Calculate Total Distance Covered by Each Vehicle:
SELECT v.vehicle_id, SUM(ST_Distance(r.pickup_location, r.dropoff_location)) AS total_distance
FROM vehicles v, rides r, drivers d
WHERE r.driver_id = d.driver_id AND v.vehicle_id = d.driver_id
GROUP BY v.vehicle_id;

-- Identify Areas with Highest Pickup Frequencies:
SELECT a.name_g, COUNT(r.ride_id) AS pickup_count
FROM areas a
JOIN rides r ON ST_Contains(a.geom, r.pickup_location)
GROUP BY a.name_g
ORDER BY pickup_count DESC;

-- Identify Popular Dropoff Locations Within a Date Range:
SELECT v.car_type, MAX(ST_Distance(r.pickup_location::geography, r.dropoff_location::geography)) AS longest_ride
FROM vehicles v, rides r, drivers d
WHERE r.driver_id = d.driver_id and  v.vehicle_id = d.vehicle_id
GROUP BY v.car_type;

-- Find Users Who Have Never Ridden in a Certain Type of Vehicle:
SELECT u.user_id, u.first_name, u.last_name
FROM users u
WHERE NOT EXISTS (
  SELECT 1 FROM rides r, vehicles v, drivers d
    WHERE r.driver_id = d.driver_id and  v.vehicle_id = d.vehicle_id
    AND u.user_id = r.user_id AND v.car_type = 'high'
);

-- Aggregate Total Distance Covered by Rides Starting from a Specific Area:
SELECT a.name_g, SUM(ST_Distance(r.pickup_location::geography, r.dropoff_location::geography)) AS total_distance
FROM areas a
JOIN rides r ON ST_Contains(a.geom, r.pickup_location)
WHERE a.name_g = 'Rancio - Laorca'
GROUP BY a.name_g;

-- Spatial indexes
-- Rides Table
CREATE INDEX idx_rides_pickup_location ON rides USING GIST (pickup_location);
CREATE INDEX idx_rides_dropoff_location ON rides USING GIST (dropoff_location);

-- Areas Table
CREATE INDEX idx_areas_geom ON areas USING GIST (geom);