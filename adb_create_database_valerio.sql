DROP DATABASE IF EXISTS myride_transactional_db;
CREATE DATABASE myride_transactional_db;

DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    date_of_birth DATE,
    residence VARCHAR(255),
    email VARCHAR(255),
    phone_number VARCHAR(255), -- not INT as you want to specify the prefix (e.g. +39)
    passw VARCHAR(50), -- password max length: 50
    account_status VARCHAR(8), --disabled, active
    rating INT,
    nrating INT
);

DROP TABLE IF EXISTS vehicles CASCADE;
CREATE TABLE vehicles (
    vehicle_id SERIAL PRIMARY KEY,
    licence_plate_num VARCHAR(255), ---> change on base of the mx lenght of plate
    manufacturer VARCHAR(255),
    model VARCHAR(255),
    manifacture_year INT,
    car_policy_num VARCHAR(255), --> change to max length
    car_type VARCHAR(6), -- normal, high
    fuel VARCHAR(8), -- diesel, electric, other
    seats_num INT,
    kids_seats_num INT,
    wheelchair_seat VARCHAR(8) -- 0 = no, 1 = yes
);

DROP TABLE IF EXISTS drivers CASCADE;
CREATE TABLE drivers (
    driver_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    driver_status VARCHAR(11), --available, unavailable, disabled
    date_of_birth DATE,
    place_of_birth VARCHAR(255),
    place_of_residence VARCHAR(255),
    nationality VARCHAR(255),
    email VARCHAR(255),
    phone_number VARCHAR(255),
    licence_id INT,
    taxi_licence_id INT,
    rating INT,
    vehicle_id INT,
    join_date DATE,
    passw VARCHAR(50),
    nrating INT,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id)
);

DROP TABLE IF EXISTS payments CASCADE;
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    payment_type VARCHAR(5), -- cash, card, gift, mix
    fare_amount INT,
    promo_code VARCHAR(255)
);

DROP TABLE IF EXISTS rides CASCADE;
CREATE TABLE rides (
    ride_id SERIAL PRIMARY KEY,
    driver_id INT,
    user_id INT,
    ride_status VARCHAR(50),
    request_code INT,
    pickup_location_lat FLOAT,
    pickup_location_lon FLOAT,
    dropoff_location_lat FLOAT,
    dropoff_location_lon FLOAT,
    request_date DATE,
    pickup_date DATE,
    dropoff_date DATE,
    rating INT,
    payment_ID INT,
    passengers_num INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (driver_id) REFERENCES drivers(driver_id),
    FOREIGN KEY (payment_id) REFERENCES payments(payment_id)
);

--DROP TABLE IF EXISTS refused_rides;
--CREATE TABLE refused_rides (
--    ride_id INT,
--    driver_id INT,
--    PRIMARY KEY (ride_id, driver_id),
--    FOREIGN KEY (ride_id) REFERENCES ride(ride_id),
--    FOREIGN KEY (driver_id) REFERENCES driver(driver_id)
--);

