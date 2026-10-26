USE company;

INSERT INTO DEPARTMENT (Dnumber, Dname, mgr_start_date) VALUES (1, 'HR', '2020-01-01');
INSERT INTO DEPARTMENT (Dnumber, Dname, mgr_start_date) VALUES (2, 'IT', '2019-05-15');
INSERT INTO DEPARTMENT (Dnumber, Dname, mgr_start_date) VALUES (3, 'Sales', '2021-03-10');

INSERT INTO EMPLOYEE (ssn, fname, lname, bdate, address, gender, salary, Dno) 
VALUES (101, 'Ahmed', 'Ali', '1990-05-20', 'Alexandria', 'M', 5000.00, 1);

INSERT INTO EMPLOYEE (ssn, fname, lname, bdate, address, gender, salary, Dno) 
VALUES (102, 'Mona', 'Omar', '1992-08-15', 'Cairo', 'F', 6000.00, 2);

INSERT INTO EMPLOYEE (ssn, fname, lname, bdate, address, gender, salary, Dno) 
VALUES (103, 'Omar', 'Hassan', '1988-11-30', 'Giza', 'M', 5500.00, 3);

UPDATE DEPARTMENT SET mgr_ssn = 101 WHERE Dnumber = 1;
UPDATE DEPARTMENT SET mgr_ssn = 102 WHERE Dnumber = 2;
UPDATE DEPARTMENT SET mgr_ssn = 103 WHERE Dnumber = 3;

INSERT INTO PROJECT (Pnumber, Pname, Plocation, Dno) VALUES (10, 'Project A', 'Alexandria', 2);
INSERT INTO PROJECT (Pnumber, Pname, Plocation, Dno) VALUES (20, 'Project B', 'Cairo', 3);
INSERT INTO PROJECT (Pnumber, Pname, Plocation, Dno) VALUES (30, 'Project C', 'Giza', 1);