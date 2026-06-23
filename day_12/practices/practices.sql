CREATE TABLE departments (
    dept_id SERIAL PRIMARY KEY,
    dept_name VARCHAR(50) UNIQUE NOT NULL
);



CREATE TABLE employees (
    emp_id SERIAL PRIMARY KEY,
    emp_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    gender VARCHAR(10) CHECK (gender IN ('Male', 'Female')),
    salary NUMERIC(10,2) CHECK (salary > 0),
    age INT CHECK (age >= 18),
    city VARCHAR(50) DEFAULT 'Chennai',
    dept_id INT,
    joining_date DATE DEFAULT CURRENT_DATE,

    CONSTRAINT fk_department
    FOREIGN KEY (dept_id)
    REFERENCES departments(dept_id)
);


INSERT INTO departments (dept_name)
VALUES
('IT'),
('HR'),
('Finance'),
('Marketing');


INSERT INTO employees
(emp_name,email,gender,salary,age,city,dept_id)
VALUES
('Arun','arun@gmail.com','Male',50000,25,'Chennai',1),
('Priya','priya@gmail.com','Female',60000,27,'Bangalore',2),
('Rahul','rahul@gmail.com','Male',45000,23,'Mumbai',1),
('Sneha','sneha@gmail.com','Female',70000,30,'Delhi',3),
('Karthik','karthik@gmail.com','Male',55000,28,'Chennai',4),
('Anitha','anitha@gmail.com','Female',80000,35,'Hyderabad',1),
('Vijay','vijay@gmail.com','Male',65000,32,'Pune',2),
('Meena','meena@gmail.com','Female',52000,26,'Chennai',3);


SELECT * FROM employees;

SELECT emp_name, salary
FROM employees;


SELECT * FROM employees
WHERE city = 'Chennai';


SELECT *
FROM employees
WHERE salary > 50000
AND city = 'Chennai';


SELECT *
FROM employees
WHERE city = 'Chennai'
OR city = 'Mumbai';


UPDATE employees
SET salary = 75000
WHERE emp_id = 1;


UPDATE employees
SET city = 'Coimbatore'
WHERE emp_name = 'Rahul';


DELETE FROM employees
WHERE emp_id = 8;


SELECT * FROM employees
ORDER BY salary;

SELECT * FROM employees
ORDER BY salary DESC;


SELECT * FROM employees
ORDER BY salary DESC
LIMIT 3;

SELECT DISTINCT city
FROM employees;

SELECT *
FROM employees
WHERE emp_name LIKE 'A%';


SELECT *
FROM employees
WHERE emp_name LIKE '%a';

SELECT *
FROM employees
WHERE emp_name LIKE '%ar%';


SELECT *
FROM employees
WHERE city IN ('Chennai','Mumbai');


SELECT *
FROM employees
WHERE salary BETWEEN 50000 AND 70000;


SELECT COUNT(*) FROM employees;


SELECT SUM(salary) FROM employees;

SELECT AVG(salary) FROM employees;

SELECT MAX(salary) FROM employees;


SELECT MIN(salary) FROM employees;

SELECT city,COUNT(*) AS total_employees
FROM employees GROUP BY city;

SELECT dept_id, COUNT(*)
FROM employees
GROUP BY dept_id
HAVING COUNT(*) > 1;


SELECT e.emp_name, d.dept_name FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id;

SELECT e.emp_name, d.dept_name FROM employees e LEFT JOIN departments d ON e.dept_id = d.dept_id;

SELECT e.emp_name, d.dept_name
FROM employees e
RIGHT JOIN departments d ON e.dept_id = d.dept_id;

SELECT e.emp_name,
       d.dept_name
FROM employees e
FULL JOIN departments d
ON e.dept_id = d.dept_id;


ALTER TABLE employees ADD phone VARCHAR(15);

ALTER TABLE employees ALTER COLUMN phone TYPE VARCHAR(20);

ALTER TABLE employees DROP COLUMN phone;


BEGIN;

UPDATE accounts
SET balance = balance - 1000
WHERE account_id = 1;

SAVEPOINT sp1;

UPDATE accounts
SET balance = balance + 1000
WHERE account_id = 2;

ROLLBACK TO sp1;

COMMIT;