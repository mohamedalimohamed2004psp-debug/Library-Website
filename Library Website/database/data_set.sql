USE library_db;

INSERT INTO AUTHOR (name, country) VALUES 
('Naguib Mahfouz', 'Egypt'),
('Ahmed Khaled Tawfik', 'Egypt'),
('William Shakespeare', 'England');

INSERT INTO BOOK (title, price, author_id) VALUES 
('Palace Walk', 150.00, 1),
('The Minor Experiment', 120.00, 1),
('Utopia', 110.00, 2),
('The Legend of Thirst', 90.00, 2),
('Hamlet', 200.00, 3),
('Romeo and Juliet', 180.00, 3);