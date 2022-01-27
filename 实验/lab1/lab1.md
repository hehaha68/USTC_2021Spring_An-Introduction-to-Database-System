## LAB01   SQL

设某图书馆数据库包含下面的基本表：

- **Book**（<u>ID</u>:  char(8)，name:  varchar(10)，author:  varchar(10)，price:  float， status:  int）

   图书号 ID 为主键，书名不能为空。状态（status）为1表示书被借出，0 表示在馆，默认值为 0。 

- **Reader**（<u>ID</u>:  char(8)，name:  varchar(10)，age:  int，address:  varchar(20)） 

  读者号 ID 为 主键。 

- **Borrow**（<u>book_ID</u>:  char(8)，<u>Reader_ID</u>:  char(8)，Borrow_Date:  date， Return_Date:  date） 

  其中：还期 Return_Date 为 NULL 表示该书未还。主键为（图书号，读者号），图书号为外键，引用图书表的图书号，读者号为外键，引用读者表的读者号。 



1、创建上述基本表，并插入部分测试数据

```mysql
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
```

2、设计例子，验证实体完整性、参照完整性、用户自定义完整性

​	**插入**或**对主码列进行更新操作**，DBMS会按照实体完整性规则自动进行检查

- 检查**主码值是否唯一**，如果不唯一则拒绝插入或修改
- 检查**主码的各个属性是否为空**，只要有一个为空就拒绝插入或修改

```mysql
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
```

3、用 SQL 语言完成下面小题，并测试运行结果：

(1) 检索读者 Rose 的读者号和地址

```mysql
select	ID,address
from	reader
where	name='Rose';
```

(2) 检索读者 Rose 所借阅读书（包括已还和未还图书）的图书名和借期

```mysql
select	B.name as Book_name,Borrow_date
from	Book B,Reader R,Borrow
where	R.ID=Borrow.Reader_ID and Borrow.book_ID=B.ID and
		R.name='Rose';
```

(3) 检索未借阅图书的读者姓名

```mysql
select	R.name as Reader_name
from	Reader R
where	R.ID NOT IN(select Reader_ID
					from Borrow);
#----------------or-------------------#
select	R.name as Reader_name
from	Reader R
where NOT Exists(	select *
					from Borrow
					where R.ID=Borrow.Reader_ID);
```

(4) 检索 Ullman 所写的书的书名和单价

```mysql
select	name,price
from	Book
where	author='Ullman';
```

(5) 检索读者“李林”借阅未还的图书的图书号和书名

```mysql
select	Book_ID,B.name
from	Reader R,Book B,Borrow
where	R.ID=Borrow.Reader_ID and Borrow.book_ID=B.ID and
		R.name='李林' and return_date is NULL;
```

(6) 检索借阅图书数目超过 3 本的读者姓名

```mysql
select	name
from	Reader
where	ID IN(	select R.ID
				from	Reader R,Borrow
				where	R.ID=Borrow.Reader_ID
                group by	R.ID
                having	count(book_ID)>3);
```

(7) 检索没有借阅读者“李林”所借的任何一本书的读者姓名和读者号

```mysql
select	R.name,R.ID as Reader_ID
from	Reader R
where	NOT EXISTS(	select	*
					from	Borrow
					where	R.ID=Borrow.Reader_ID and
							book_ID in(select	Book_ID
										from	Reader R,Borrow
										where	R.ID=Borrow.Reader_ID and R.name='李林'
										));
```

(8) 检索书名中包含“Oracle”的图书书名及图书号

```mysql
select	name,ID
from	Book
where	name LIKE '%Oracle%';
```

(9) 创建一个读者借书信息的视图，该视图包含读者号、姓名、所借图书号、图书名 和借期；并使用该视图查询最近一年所有读者的读者号以及所借阅的不同图书数

```mysql
DROP view IF EXISTS Message;
create view Message as(	select	Reader_ID,R.name as Reader_name,Book_ID,B.name as Book_name,Borrow.Borrow_date
						from	Reader R,Book B,Borrow
						where	R.ID=Borrow.Reader_ID and Borrow.book_ID=B.ID);
						
select	Reader_ID,count(distinct Book_ID) as Book_num
from	Message
where	year(from_days(to_days(now())-to_days(borrow_date))) < 1
group by 	Reader_ID;
DROP view Message;
```

4、 设计一个存储过程，实现对 Book 表的 ID 的修改（==本题要求不得使用外键定义时的 on update cascade 选项，因为该选项不是所有 DBMS 都支持==）

```mysql
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
```

5、 设计一个存储过程，检查每本图书 status 是否正确，并返回 status 不正确的图书数

```mysql
Delimiter //
DROP PROCEDURE IF EXISTS CHECK_book_status;
CREATE PROCEDURE CHECK_book_status(OUT num int,OUT state int)
BEGIN
	DECLARE s INT DEFAULT 0;
    DECLARE n INT DEFAULT 0;
	DEClARE	CONTINUE HANDLER FOR NOT FOUND SET s = 1;

    START TRANSACTION;
    #创建视图
    DROP VIEW IF EXISTS temp;
	CREATE VIEW temp (ID)
    AS(	select B.book_ID
		from borrow B
		where return_date is null
		group by B.book_ID);
	 #检查借阅状态				
	SELECT COUNT(DISTINCT B.id)
	FROM temp,book B
	WHERE B.status != 1 AND B.id IN (SELECT id FROM temp)
    INTO n;
    SET num = n;
    #检查归还状态
    SELECT COUNT(DISTINCT B.id)
	FROM temp,book B
	WHERE B.status != 0 AND B.id NOT IN (SELECT id FROM temp)
    INTO n;
    SET num = num + n;
    #删除视图
	DROP VIEW temp;
	#异常处理
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
```

6、 设计触发器，实现：当一本书被借出时，自动将 Book 表中相应图书的 status 修改为 1；当某本书被归还时，自动将 status 改为 0

```mysql
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
```

