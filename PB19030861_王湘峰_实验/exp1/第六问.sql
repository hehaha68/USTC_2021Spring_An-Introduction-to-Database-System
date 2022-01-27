CREATE DEFINER=`root`@`localhost` TRIGGER `updatestate1` AFTER INSERT ON `borrow` FOR EACH ROW 
BEGIN
	if new.Return_Date is null then
		update book set status=1 where ID=new.Book_ID;
	else if new.Return_Date>=new.Borrow_Date then
		update book set status=0 where ID=new.Book_ID;
		end if;
	end if;
END

#设计了两个触发器，分别应对borrow表插入和更新数据时对book的state的修改

CREATE DEFINER=`root`@`localhost` TRIGGER `updatestate2` AFTER UPDATE ON `borrow` FOR EACH ROW 
BEGIN
	if new.Return_Date is null then
		update book set status=1 where ID=new.Book_ID;
	else if new.Return_Date>=new.Borrow_Date then
		update book set status=0 where ID=new.Book_ID;
		end if;
	end if;
END