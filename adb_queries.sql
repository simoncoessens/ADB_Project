-- Change "driverStatus" (0 = Available, 1 = Busy, 2 = Unavailable)
UPDATE driver
SET driver_status = '{random_status}'
WHERE driver_id = '{random_driver_id}';