
-- Data types 
-- Numerical Type : SMALLINT, INTEGER, BIGINT, DECIMAL, SERIAL, BIGSERIAL
-- Character Type : CHAR(n), VARCHAR(n), TEXT
-- Date/Time Type : DATE, TIME, TIMESTAMP, TIMESTAMPZ
-- BOOLEAN/ BYTE  : BOOLEAN, BYTEA
-- DOCUMENT Type  : JSON, JSONB, HSTORE, XML


-- Constraints
-- Check Constrains - it allow to specify that the value in certain column must satisfy a boolean expression
-- NOT NULL Constrains - it ensure that the cloumn is not empty
-- Unique Constrains - it ensure that the data contain in column or group of columns is unique 
-- Primary Constrains - it ensure the unique identifiers for rows in table.
-- Foregin Constrains - the values in columns or group of columns must match the values in some row of another table
-- Exclude Constrains - Prevent specific relationships between rows


-- types of Joins 
-- 1) left Join (or) Join - it return values from full left table values and common values from right tables
-- 2) right Join - it return values from full right values and common values from left tables
-- 3) inner Join - it return common values from both tables
-- 4) outer join - it return the common values from both tables and also uncommon values 
-- 5) cross join - it allow us to combine rows from two or more tables without any specific relationship between them



CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    gender VARCHAR(6) UNIQUE NOT NULL,
    country VARCHAR(50) DEFAULT 'India';
)


INSERT INTO users (name, email, gender, country) VALUES
('Arun Kumar', 'arun.kumar@example.com', 'Male', 'India'),
('Priya Sharma', 'priya.sharma@example.com', 'Female', 'India'),
('Rahul Verma', 'rahul.verma@example.com', 'Male', 'India'),
('Sneha Reddy', 'sneha.reddy@example.com', 'Female', 'India'),
('Vikram Singh', 'vikram.singh@example.com', 'Male', 'India'),
('Anjali Gupta', 'anjali.gupta@example.com', 'Female', 'India'),
('Karthik Raj', 'karthik.raj@example.com', 'Male', 'India'),
('Meera Nair', 'meera.nair@example.com', 'Female', 'India'),
('Rohit Patil', 'rohit.patil@example.com', 'Male', 'India'),
('Divya Iyer', 'divya.iyer@example.com', 'Female', 'India');


SELECT * FROM users;

SELECT * FROM users WHERE gender = 'Male';

SELECT * FROM users WHERE gender != 'Male';

SELECT * FROM users order by name;

SELECT name, country FROM users;

SELECT * FROM users WHERE name like '%A%' ;

SELECT * FROM users WHERE name ilike '%A%' order by name desc;

SELECT * FROM users WHERE name like '%A%' order by name; 

ALTER TABLE user RENAME COLUMN country to address;

ALTER TABLE user ADD COLUMN phone_no VARCHAR(10) unique;

ALTER TABLE user DROP COLUMN phone_no;

ALTER TABLE user RENAME TO user_details;

UPDATE user SET gender = 'Male' WHERE id = 7;

DELETE FROM user WHERE id = 10;

