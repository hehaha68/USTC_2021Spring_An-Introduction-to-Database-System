CREATE DEFINER=`root`@`localhost` PROCEDURE `alterid`(in oldid varchar(45),in newid varchar(45),out state int)
# oldid和newid分别是更改前后book的id，state代表执行状态，0代表成功，-1代表失败
BEGIN
    declare a varchar(10);
    set state=0;
    start transaction;
	SET FOREIGN_KEY_CHECKS=0;
    select ID into a from book where ID=oldid;
    if a is not null then
		set state=0;
        update book set ID=newid where ID=oldid;
		update borrow set Book_ID=newid where Book_ID=oldid;
		SET FOREIGN_KEY_CHECKS=1;
		commit;
	else
        set state=-1;
        rollback;
	end if;
END