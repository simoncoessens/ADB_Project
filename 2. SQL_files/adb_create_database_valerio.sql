--DROP DATABASE IF EXISTS myride_transactional_db;
--CREATE DATABASE myride_transactional_db;

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

-- Rides Table with Geographic Columns
DROP TABLE IF EXISTS rides CASCADE;
CREATE TABLE rides (
    ride_id SERIAL PRIMARY KEY,
    driver_id INT,
    user_id INT,
    ride_status VARCHAR(50),
    request_code INT,
    pickup_location GEOGRAPHY(Point, 4326),
    dropoff_location GEOGRAPHY(Point, 4326),
    request_date DATE,
    pickup_date DATE,
    dropoff_date DATE,
    rating INT,
    payment_id INT,
    passengers_num INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (driver_id) REFERENCES drivers(driver_id),
    FOREIGN KEY (payment_id) REFERENCES payments(payment_id)
);

CREATE EXTENSION IF NOT EXISTS postgis;
DROP TABLE IF EXISTS AREAS;

CREATE TABLE areas (
    id SERIAL PRIMARY KEY,
    name_g VARCHAR(50),
    geom GEOMETRY(POLYGON, 4326)
    
);



INSERT INTO areas (name_g,geom) VALUES
	 ('Rancio - Laorca','SRID=4326;POLYGON ((9.3903324 45.8690007, 9.3998199 45.865462, 9.4063002 45.8623091, 9.406938 45.860993, 9.4123883 45.8618596, 9.414813 45.8612619, 9.4151807 45.8624949, 9.4252443 45.8672914, 9.416555 45.8733978, 9.4214045 45.8767143, 9.4153058 45.8879922, 9.4087431 45.8887791, 9.3903324 45.8690007))'),
	 ('Santo Stefano','SRID=4326;POLYGON ((9.3998199 45.865462, 9.3864788 45.8703097, 9.3748488 45.8688753, 9.3832173 45.8561825, 9.3849768 45.8589023, 9.3880024 45.8572285, 9.3915643 45.8583792, 9.3944555 45.8597389, 9.3969231 45.8613229, 9.3982321 45.8629815, 9.3980604 45.8637735, 9.3998199 45.865462))'),
	 ('Castello - Olate','SRID=4326;POLYGON ((9.4092167 45.8585645, 9.4075447 45.8598285, 9.4063002 45.8623091, 9.3998199 45.865462, 9.3980604 45.8637735, 9.3982321 45.8629815, 9.3969231 45.8613229, 9.3944555 45.8597389, 9.3915643 45.8583792, 9.3958559 45.8523864, 9.3991818 45.8535403, 9.4034231 45.8550974, 9.4092167 45.8585645))'),
	 ('Acquate - Piani DErnia','SRID=4326;POLYGON ((9.4346144 45.8457007, 9.437561 45.8600293, 9.4252443 45.8672914, 9.4151807 45.8624949, 9.414813 45.8612619, 9.4123883 45.8618596, 9.406938 45.860993, 9.4075447 45.8598285, 9.4092167 45.8585645, 9.4117272 45.8565022, 9.4138515 45.853872, 9.4153535 45.8537823, 9.4174523 45.851294, 9.416641 45.8448893, 9.4346144 45.8457007))'),
	 ('Lecco Centro','SRID=4326;POLYGON ((9.3877878 45.8526405, 9.3925728 45.8515644, 9.3958559 45.8523864, 9.3915643 45.8583792, 9.3880024 45.8572285, 9.3849768 45.8589023, 9.3832173 45.8561825, 9.3877878 45.8526405))'),
	 ('Bione','SRID=4326;POLYGON ((9.3857922 45.854168, 9.3872513 45.849505, 9.3954911 45.8465157, 9.4004692 45.8390715, 9.4043316 45.8398489, 9.4057478 45.8443633, 9.403645 45.8490267, 9.3991818 45.8535403, 9.3958559 45.8523864, 9.3925728 45.8515644, 9.3877878 45.8526405, 9.3857922 45.854168))'),
	 ('Ospedale Manzoni','SRID=4326;POLYGON ((9.3991818 45.8535403, 9.403645 45.8490267, 9.4057478 45.8443633, 9.416641 45.8448893, 9.4174779 45.8511818, 9.4153535 45.8537823, 9.4138515 45.853872, 9.4117272 45.8565022, 9.4092167 45.8585645, 9.4034231 45.8550974, 9.3991818 45.8535403))'),
	 ('Maggianico','SRID=4326;POLYGON ((9.4057478 45.8443633, 9.4043316 45.8398489, 9.4004692 45.8390715, 9.4178774 45.8131061, 9.430237 45.8137043, 9.4207098 45.8312298, 9.4352152 45.8400802, 9.4346144 45.8457007, 9.4057478 45.8443633))'),
	 ('Malgrate Lungolago','SRID=4326;POLYGON ((9.3954911 45.8465157, 9.3872513 45.849505, 9.3752569 45.8543636, 9.3759865 45.8567547, 9.3663735 45.8598033, 9.3668026 45.8656608, 9.363541 45.8650632, 9.3654722 45.8563214, 9.3667168 45.8551258, 9.367618 45.8548717, 9.3688626 45.853706, 9.3722529 45.8499696, 9.370665 45.8479668, 9.3766731 45.8494465, 9.3777889 45.8478921, 9.3928817 45.8451298, 9.3958322 45.8460267, 9.3954911 45.8465157))'),
	 ('Pescate','SRID=4326;POLYGON ((9.3958322 45.8460267, 9.3928817 45.8451298, 9.3916157 45.8366166, 9.392002 45.8198106, 9.3978814 45.8201695, 9.4004692 45.8390715, 9.3958322 45.8460267))'),
	 ('Orsa Maggiore','SRID=4326;POLYGON ((9.3748488 45.8688753, 9.3864788 45.8703097, 9.3701684 45.8811434, 9.3672501 45.880994, 9.3748488 45.8688753))'),
	 ('Rancio - Laorca','SRID=4326;POLYGON ((9.3903324 45.8690007, 9.3998199 45.865462, 9.4063002 45.8623091, 9.406938 45.860993, 9.4123883 45.8618596, 9.414813 45.8612619, 9.4151807 45.8624949, 9.4252443 45.8672914, 9.416555 45.8733978, 9.4214045 45.8767143, 9.4153058 45.8879922, 9.4087431 45.8887791, 9.3903324 45.8690007))'),
	 ('Santo Stefano','SRID=4326;POLYGON ((9.3998199 45.865462, 9.3864788 45.8703097, 9.3748488 45.8688753, 9.3832173 45.8561825, 9.3849768 45.8589023, 9.3880024 45.8572285, 9.3915643 45.8583792, 9.3944555 45.8597389, 9.3969231 45.8613229, 9.3982321 45.8629815, 9.3980604 45.8637735, 9.3998199 45.865462))'),
	 ('Castello - Olate','SRID=4326;POLYGON ((9.4092167 45.8585645, 9.4075447 45.8598285, 9.4063002 45.8623091, 9.3998199 45.865462, 9.3980604 45.8637735, 9.3982321 45.8629815, 9.3969231 45.8613229, 9.3944555 45.8597389, 9.3915643 45.8583792, 9.3958559 45.8523864, 9.3991818 45.8535403, 9.4034231 45.8550974, 9.4092167 45.8585645))'),
	 ('Acquate - Piani DErnia','SRID=4326;POLYGON ((9.4346144 45.8457007, 9.437561 45.8600293, 9.4252443 45.8672914, 9.4151807 45.8624949, 9.414813 45.8612619, 9.4123883 45.8618596, 9.406938 45.860993, 9.4075447 45.8598285, 9.4092167 45.8585645, 9.4117272 45.8565022, 9.4138515 45.853872, 9.4153535 45.8537823, 9.4174523 45.851294, 9.416641 45.8448893, 9.4346144 45.8457007))'),
	 ('Lecco Centro','SRID=4326;POLYGON ((9.3877878 45.8526405, 9.3925728 45.8515644, 9.3958559 45.8523864, 9.3915643 45.8583792, 9.3880024 45.8572285, 9.3849768 45.8589023, 9.3832173 45.8561825, 9.3877878 45.8526405))'),
	 ('Bione','SRID=4326;POLYGON ((9.3857922 45.854168, 9.3872513 45.849505, 9.3954911 45.8465157, 9.4004692 45.8390715, 9.4043316 45.8398489, 9.4057478 45.8443633, 9.403645 45.8490267, 9.3991818 45.8535403, 9.3958559 45.8523864, 9.3925728 45.8515644, 9.3877878 45.8526405, 9.3857922 45.854168))'),
	 ('Ospedale Manzoni','SRID=4326;POLYGON ((9.3991818 45.8535403, 9.403645 45.8490267, 9.4057478 45.8443633, 9.416641 45.8448893, 9.4174779 45.8511818, 9.4153535 45.8537823, 9.4138515 45.853872, 9.4117272 45.8565022, 9.4092167 45.8585645, 9.4034231 45.8550974, 9.3991818 45.8535403))'),
	 ('Maggianico','SRID=4326;POLYGON ((9.4057478 45.8443633, 9.4043316 45.8398489, 9.4004692 45.8390715, 9.4178774 45.8131061, 9.430237 45.8137043, 9.4207098 45.8312298, 9.4352152 45.8400802, 9.4346144 45.8457007, 9.4057478 45.8443633))'),
	 ('Malgrate Lungolago','SRID=4326;POLYGON ((9.3954911 45.8465157, 9.3872513 45.849505, 9.3752569 45.8543636, 9.3759865 45.8567547, 9.3663735 45.8598033, 9.3668026 45.8656608, 9.363541 45.8650632, 9.3654722 45.8563214, 9.3667168 45.8551258, 9.367618 45.8548717, 9.3688626 45.853706, 9.3722529 45.8499696, 9.370665 45.8479668, 9.3766731 45.8494465, 9.3777889 45.8478921, 9.3928817 45.8451298, 9.3958322 45.8460267, 9.3954911 45.8465157))'),
	 ('Pescate','SRID=4326;POLYGON ((9.3958322 45.8460267, 9.3928817 45.8451298, 9.3916157 45.8366166, 9.392002 45.8198106, 9.3978814 45.8201695, 9.4004692 45.8390715, 9.3958322 45.8460267))'),
	 ('Orsa Maggiore','SRID=4326;POLYGON ((9.3748488 45.8688753, 9.3864788 45.8703097, 9.3701684 45.8811434, 9.3672501 45.880994, 9.3748488 45.8688753))');

