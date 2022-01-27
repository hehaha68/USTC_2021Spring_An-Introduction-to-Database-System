####第一题####
Create table Book(
					ID char(8) Primary Key,
                    name varchar(50) NOT NULL,
                    author varchar(10),
                    price float,
                    status int Default 0);
Create table Reader(
					ID char(8) Primary Key,
                    name varchar(10),
                    age int,
                    address varchar(20));
Create table Borrow(
					book_ID char(8),
                    Reader_ID char(8),
                    Borrow_Data date,
                    Return_Data date,
                    Primary Key(book_ID,Reader_ID),
                    Foreign Key(book_ID) references Book(ID),
                    Foreign Key(Reader_ID) references Reader(ID));

####第二题####
#实体完整性
INSERT INTO `lab1`.`book` (`ID`, `name`, `author`, `price`, `status`) VALUES ('b10', '随机过程', '陈', '1', '0');
UPDATE `lab1`.`book` SET `ID` = 'b200' WHERE (`ID` = 'b9');
INSERT INTO `lab1`.`READER` (`ID`, `name`) VALUES ('r6', 'a');
INSERT INTO `lab1`.`READER` (`ID`, `name`) VALUES (null, 'a');
#参照完整性
INSERT INTO `lab1`.`BORROW` (`book_ID`, `Reader_ID`, `borrow_date`) VALUES ('b100', 'r5', '2021-02-22');
UPDATE `lab1`.`BORROW` SET `Reader_ID` = 'r200' WHERE (`book_ID` = 'b9') and (`Reader_ID` = 'r2');
DELETE FROM book WHERE id='b10';
#用户自定义完整性
INSERT INTO `lab1`.`book` (`ID`, `name`, `author`, `price`, `status`) VALUES ('b100', NULL, '陈', '1', '0');

####第三题####
##（1）##
select	ID,address
from	reader
where	name='Rose';
##（2）##
select	B.name as Book_name,Borrow_date
from	Book B,Reader R,Borrow
where	R.ID=Borrow.Reader_ID and Borrow.book_ID=B.ID and
		R.name='Rose';
##（3）##        
select	R.name as Reader_name
from	Reader R
where	R.ID NOT IN(select Reader_ID
					from Borrow);
##（4）##                    
select	name,price
from	Book
where	author='Ullman';
##（5）##
select	Book_ID,B.name
from	Reader R,Book B,Borrow
where	R.ID=Borrow.Reader_ID and Borrow.book_ID=B.ID and
		R.name='李林' and return_date is NULL;
##（6）##        
select	name
from	Reader
where	ID IN(	select R.ID
				from	Reader R,Borrow
				where	R.ID=Borrow.Reader_ID
                group by	R.ID
                having	count(book_ID)>3);
##（7）##               
select	R.name,R.ID as Reader_ID
from	Reader R
where	NOT EXISTS(	select	*
					from	Borrow
					where	R.ID=Borrow.Reader_ID and
							book_ID in(select	Book_ID
										from	Reader R,Borrow
										where	R.ID=Borrow.Reader_ID and R.name='李林'
										));
##（8）##						
select	name,ID
from	Book
where	name LIKE '%Oracle%';
##（9）##
DROP view IF EXISTS Message;
create view Message as(	select	Reader_ID,R.name as Reader_name,Book_ID,B.name as Book_name,Borrow.Borrow_date
						from	Reader R,Book B,Borrow
						where	R.ID=Borrow.Reader_ID and Borrow.book_ID=B.ID);
						
select	Reader_ID,count(distinct Book_ID) as Book_num
from	Message
where	year(from_days(to_days(now())-to_days(borrow_date))) < 1
group by 	Reader_ID;
DROP view Message;

####第四题####
##(1)##如果可以使用FOREIGN_KEY_CHECKS
Delimiter //
DROP PROCEDURE IF EXISTS UD_BOOKID;
CREATE PROCEDURE UD_BOOKID(IN old_id char(8),IN new_id char(8),OUT state int)
BEGIN
	DECLARE s INT DEFAULT 0;
    DECLARE c char(8);
	DEClARE	CONTINUE HANDLER FOR NOT FOUND SET s = 1;
    DEClARE	CONTINUE HANDLER FOR 1451 SET s = 2;
    DEClARE	CONTINUE HANDLER FOR 1452 SET s = 3;
    START TRANSACTION;
    SELECT ID FROM Book WHERE ID = old_id INTO c;
	SET	FOREIGN_KEY_CHECKS = 0;
	UPDATE	Book	SET ID = new_id	WHERE ID = old_id;
	UPDATE	Borrow	SET Book_ID = new_id	WHERE Book_ID = old_id;
	SET FOREIGN_KEY_CHECKS = 1;
    IF s = 0 THEN
	  SET state = 0;
	  COMMIT;
	ELSE
	  CASE s
		WHEN 1 THEN	SET state = 1;
		WHEN 2 THEN	SET state = 2;
        WHEN 3 THEN SET state = 3;
	  END CASE;
      ROLLBACK;
	END IF;
END //
Delimiter ;
CALL UD_BOOKID('b12','b21',@state);
SELECT @state;
##(2)##如果不能使用FOREIGN_KEY_CHECKS
Delimiter //
DROP PROCEDURE IF EXISTS UD_BOOKID;
CREATE PROCEDURE UD_BOOKID(IN old_id char(8),IN new_id char(8),OUT state int)
BEGIN
	DECLARE s,status1 INT DEFAULT 0;
	DECLARE c,name1,author1 char(8);
	DECLARE price1 float;
	DEClARE	CONTINUE HANDLER FOR NOT FOUND SET s = 1;
    DEClARE	CONTINUE HANDLER FOR 1451 SET s = 2;
    DEClARE	CONTINUE HANDLER FOR 1452 SET s = 3;
    START TRANSACTION;
    SELECT status from Book where ID = old_id into status1;
    SELECT name from Book where ID = old_id into name1;
    SELECT author from Book where ID = old_id into author1;
    SELECT price from Book where ID = old_id into price1;
    
    SELECT ID FROM Borrow WHERE Book_ID = old_id INTO c;
    IF s=1 THEN
		UPDATE	Book	SET ID = new_id	WHERE ID = old_id;
	ELSE
		INSERT INTO book(ID,name,author,price,status)
        VALUES(new_id,name1,author1,price1,status1);
        UPDATE	Borrow	SET Book_ID = new_id	WHERE Book_ID = old_id;
        DELETE FROM Book WHERE ID = old_id;
	END IF;

    IF s = 0 THEN
	  SET state = 0;
	  COMMIT;
	ELSE
	  CASE s
		WHEN 1 THEN	SET state = 1;
		WHEN 2 THEN	SET state = 2;
        WHEN 3 THEN SET state = 3;
	  END CASE;
      ROLLBACK;
	END IF;
END //
Delimiter ;

####第五题####
Delimiter //
DROP PROCEDURE IF EXISTS CHECK_book_status;
CREATE PROCEDURE CHECK_book_status(OUT num int,OUT state int)
BEGIN
	DECLARE s INT DEFAULT 0;
    DECLARE n INT DEFAULT 0;
	DEClARE	CONTINUE HANDLER FOR NOT FOUND SET s = 1;

    START TRANSACTION;
    DROP VIEW IF EXISTS temp;
	CREATE VIEW temp (ID)
    AS(	select B.book_ID
		from borrow B
		where return_date is null
		group by B.book_ID);
					
	SELECT COUNT(DISTINCT B.id)
	FROM temp,book B
	WHERE B.status != 1 AND B.id IN (SELECT id FROM temp)
    INTO n;
    SET num = n;
    
    SELECT COUNT(DISTINCT B.id)
	FROM temp,book B
	WHERE B.status != 0 AND B.id NOT IN (SELECT id FROM temp)
    INTO n;
    SET num = num + n;
    
	DROP VIEW temp;
    IF s = 0 THEN
	  SET state = 0;
	  COMMIT;
	ELSE
	  SET state = 1;
	  ROLLBACK;
	END IF;
END //
Delimiter ;

CALL CHECK_book_status(@num,@state);
SELECT @num,@state;

####第六题####
Delimiter //
DROP TRIGGER IF EXISTS UPDATE_book_status;
CREATE TRIGGER UPDATE_book_status AFTER INSERT ON Borrow FOR EACH ROW
BEGIN	
    SET	SQL_SAFE_UPDATES = 0;
	UPDATE	Book	SET status = 1
	WHERE 	ID IN (select B.book_ID
					from borrow B
					where return_date is null
					group by B.book_ID);
    SET SQL_SAFE_UPDATES = 1;
END //
Delimiter ;

Delimiter //
DROP TRIGGER IF EXISTS UPDATE_book_status_2;
CREATE TRIGGER UPDATE_book_status_2 AFTER UPDATE ON Borrow FOR EACH ROW
BEGIN	
    SET	SQL_SAFE_UPDATES = 0;

    UPDATE	Book	SET status = 0
	WHERE	ID NOT IN (select B.book_ID
						from borrow B
						where return_date is null
						group by B.book_ID);
    SET SQL_SAFE_UPDATES = 1;
END //
Delimiter ;