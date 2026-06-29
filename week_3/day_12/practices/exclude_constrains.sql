CREATE EXTENSION IF NOT EXISTS btree_gist;

CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    room_no INT,
    stay_period DATERANGE,

    EXCLUDE USING gist (
        room_no WITH =, -- same room_no
        stay_period WITH && -- different time period
        -- WITH <> -- no different values
    )
);

INSERT INTO bookings (room_no, stay_period) VALUES
(101, DATERANGE('2026-06-01', '2026-06-05')); -- Success

INSERT INTO bookings (room_no, stay_period) VALUES
(101, DATERANGE('2026-06-05', '2026-06-10')); -- Success

INSERT INTO bookings (room_no, stay_period) VALUES
(101, DATERANGE('2026-06-03', '2026-06-07')); -- overlaping

-- Error

