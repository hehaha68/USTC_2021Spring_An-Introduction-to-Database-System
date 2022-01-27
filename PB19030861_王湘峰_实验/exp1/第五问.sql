CREATE DEFINER=`root`@`localhost` PROCEDURE `bcheck`(out counter int)
BEGIN
	declare state int default 0;
    declare a int;
    declare c int default 0;
    declare c1 int default 0;
    # c表示在borrow表中有记录的错误的book数，c1表示在borrow表中无记录但是status为1的book数
	declare bo date;
    declare re date;
    declare st int;
    declare myid varchar(8);
    
    declare bstate cursor for
	select book.status,Book_ID,max(Borrow_Date) as b,min(Return_Date) as r
	from borrow inner join book on book.ID=borrow.Book_ID
	group by Book_ID;
    
    declare continue handler for not found set state=1;
    
	open bstate;
    while state=0 do
		fetch bstate into st,myid,bo,re;
        if re is null and st=0 then
			set c=c+1;
		else if re>=bo and st=1 then
			set c=c+1;
		else if re<bo and st=0 then
			set c=c+1;
            end if;
		end if;
		end if;
	end while;
    close bstate;
    
	select sum(status) as total from(
    select status from book where ID not in
    (select distinct Book_ID from borrow)
    )bid
    into a;
    if a is not null then
		set c1=a;
	end if;
    
    set counter=c+c1;
END