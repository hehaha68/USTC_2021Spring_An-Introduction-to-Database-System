#检验实体完整性
INSERT INTO `exp1`.`book` (`ID`, `name`, `author`, `price`, `status`) VALUES (null, 'as', 'b', '1', 0);
#检验参照完整性
INSERT INTO `exp1`.`borrow` (`Book_ID`, `Reader_ID`, `Borrow_Date`, `Return_Date`) VALUES ('b100', 'r1', '2020-4-1', '2021-4-1');
#检验用户自定义完整性（status只能为int型变量）
INSERT INTO `exp1`.`book` (`ID`, `name`, `author`, `price`, `status`) VALUES ('b13', 'test', 'test', '4.04', '未借出');