CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100),
    salary NUMERIC(10,2)
);

INSERT INTO employees (name, email, salary)
VALUES
('Arun', 'arun@gmail.com', 50000),
('Bala', 'bala@gmail.com', 45000),
('Charan', 'charan@gmail.com', 60000),
('David', 'david@gmail.com', 55000),
('Eshan', 'eshan@gmail.com', 70000);

EXPLAIN ANALYZE
SELECT * FROM employees
WHERE email = 'charan@gmail.com';

CREATE INDEX idx_employee_email
ON employees(email);

EXPLAIN ANALYZE
SELECT * FROM employees
WHERE email = 'charan@gmail.com';

----------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100),
    salary NUMERIC(10,2)
);

INSERT INTO employees(name,email,salary)
VALUES
('Arun','arun@gmail.com',50000),
('Bala','bala@gmail.com',45000),
('Charan','charan@gmail.com',60000),
('David','david@gmail.com',55000),
('Eshan','eshan@gmail.com',70000);

EXPLAIN ANALYZE
SELECT * FROM employees
WHERE email = 'charan@gmail.com';

CREATE INDEX idx_hash_email
ON employees USING HASH(email);

EXPLAIN ANALYZE
SELECT * FROM employees
WHERE email = 'charan@gmail.com';

-------------------------------------------------------------------------------------------------------------------------------------------

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

----------------------------------------------------------------------------------------------------------------------------------------------

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    skills TEXT[]
);

INSERT INTO employees(name, skills)
VALUES
('Arun', ARRAY['Python','SQL']),
('Bala', ARRAY['Java','Spring']),
('Charan', ARRAY['Python','Django']),
('David', ARRAY['React','NodeJS']),
('Eshan', ARRAY['Python','FastAPI']);

EXPLAIN ANALYZE
SELECT *
FROM employees
WHERE skills @> ARRAY['Python'];

CREATE INDEX idx_skills
ON employees
USING GIN(skills);

EXPLAIN ANALYZE
SELECT *
FROM employees
WHERE skills @> ARRAY['Python'];


------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    skills TEXT[]
);

INSERT INTO employees(name, skills)
VALUES
('Arun', ARRAY['Python','SQL']),
('Bala', ARRAY['Java','Spring']),
('Charan', ARRAY['Python','Django']),
('David', ARRAY['React','NodeJS']),
('Eshan', ARRAY['Python','FastAPI']);

EXPLAIN ANALYZE
SELECT *
FROM employees
WHERE skills @> ARRAY['Python'];

CREATE INDEX idx_skills
ON employees
USING GIN(skills);

EXPLAIN ANALYZE
SELECT *
FROM employees
WHERE skills @> ARRAY['Python'];

-----------------------------------------------------------------------------------------------------------------------------------------------------------------