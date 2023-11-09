DROP DATABASE IF EXISTS myride_transactional_db;
CREATE DATABASE myride_transactional_db;

DROP TABLE IF EXISTS costumer;
CREATE TABLE costumer (
    user_id INT PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    date_of_birth DATE,
    residence VARCHAR(255),
    email VARCHAR(255),
    phone_number VARCHAR(255), -- not INT as you want to specify the prefix (e.g. +39)
    passw VARCHAR(50), -- password max length: 50
    account_status VARCHAR(8), --disabled, active
    rating INT
);

DROP TABLE IF EXISTS vehicle;
CREATE TABLE vehicle (
    vehicle_id INT PRIMARY KEY,
    licence_plate_num VARCHAR(255), ---> change on base of the mx lenght of plate
    manufacturer VARCHAR(255),
    model VARCHAR(255),
    manifacture_year INT,
    car_policy_num VARCHAR(255), --> change to max length
    car_type VARCHAR(6), -- normal, high
    fuel VARCHAR(8), -- diesel, electric, other
    seats_num INT,
    kids_seats_num INT,
    wheelchair_seat INT -- 0 = no, 1 = yes
);

DROP TABLE IF EXISTS driver;
CREATE TABLE driver (
    driver_id INT PRIMARY KEY,
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
    FOREIGN KEY (vehicle_id) REFERENCES vehicle(vehicle_id)
);

DROP TABLE IF EXISTS payment;
CREATE TABLE payment (
    payment_id INT PRIMARY KEY,
    payment_type VARCHAR(5), -- cash, card, gift, mix
    fare_amount INT,
    promo_code VARCHAR(255)
);

DROP TABLE IF EXISTS ride;
CREATE TABLE ride (
    ride_id INT PRIMARY KEY,
    driver_id INT,
    user_id INT,
    -- ride_status VARCHAR(50),
    request_code INT,
    route_to_pickup VARCHAR(255), --------------> CHECK AGAIN
    route_to_dropoff VARCHAR(255), --------------> CHECK AGAIN
    request_date DATE,
    pickup_date TIMESTAMP WITHOUT TIME ZONE,
    dropoff_date TIMESTAMP WITHOUT TIME ZONE,
    rating INT,
    payment_ID INT,
    passengers_num INT,
    FOREIGN KEY (user_id) REFERENCES costumer(user_id),
    FOREIGN KEY (driver_id) REFERENCES driver(driver_id),
    FOREIGN KEY (payment_id) REFERENCES payment(payment_id)
);

DROP TABLE IF EXISTS refused_rides;
CREATE TABLE refused_rides (
    ride_id INT,
    driver_id INT,
    PRIMARY KEY (ride_id, driver_id),
    FOREIGN KEY (ride_id) REFERENCES ride(ride_id),
    FOREIGN KEY (driver_id) REFERENCES driver(driver_id)
);


-- TEST
SELECT * FROM costumer;
SELECT * FROM vehicle;
SELECT * FROM driver;
SELECT * FROM ride;
SELECT * FROM refused_rides;