USE library_db;

-- إدخال المؤلفين مع تحديد user_id (نفترض أنه 1)
INSERT INTO AUTHOR (name, country, user_id) VALUES
('Naguib Mahfouz', 'Egypt', 1),
('Ahmed Khaled Tawfik', 'Egypt', 1),
('William Shakespeare', 'England', 1);

-- إدخال الكتب مع تحديد user_id (نفترض أنه 1)
INSERT INTO BOOK (title, price, author_id, user_id) VALUES
('Palace Walk', 150.00, 1, 1),
('The Mirror Experiment', 120.00, 1, 1),
('Utopia', 110.00, 2, 1),
('The Legend of Thirst', 90.00, 2, 1),
('Hamlet', 200.00, 3, 1),
('Romeo and Juliet', 180.00, 3, 1);