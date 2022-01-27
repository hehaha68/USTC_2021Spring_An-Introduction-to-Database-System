Delimiter //
DROP PROCEDURE IF EXISTS cxyear;
create 
	definer = root@localhost procedure cxyear(
    IN ye int, in bank_name varchar(50), OUT money float, OUT num int)
BEGIN

    select sum(Balance)
    from account,saving_account
    where year(Opening_Date) = ye
      and account.A_ID = saving_account.A_ID
      and B_Name = bank_name
	into money;
      
	select count(C_ID)
    from checking
    where A_Type = 1
    and B_Name = bank_name
	and A_ID in (	select A_ID
					from account
					where year(Opening_Date) = ye)
	into num;
    
    if money is null then
        set money = 0;
    end if;
    
    if num is null then
        set num = 0;
    end if;
END //
Delimiter ;

Delimiter //
DROP PROCEDURE IF EXISTS cxmonth;
create 
	definer = root@localhost procedure cxmonth(
    IN ye int, IN mo int, in bank_name varchar(50), OUT money float, OUT num int)
BEGIN

    select sum(Balance)
    from account,saving_account
    where year(Opening_Date) = ye
	and month(Opening_Date) = mo
	and account.A_ID = saving_account.A_ID
	and B_Name = bank_name
	into money;
      
	select count(C_ID)
    from checking
    where A_Type = 1
    and B_Name = bank_name
	and A_ID in (	select A_ID
					from account
					where year(Opening_Date) = ye
                    and month(Opening_Date) = mo)
	into num;
    
    if money is null then
        set money = 0;
    end if;
    
    if num is null then
        set num = 0;
    end if;
END //
Delimiter ;

Delimiter //
DROP PROCEDURE IF EXISTS cxseason;
create 
	definer = root@localhost procedure cxseason(
    IN ye int, IN se int, in bank_name varchar(50), OUT money float, OUT num int)
BEGIN

    select sum(Balance)
    from account,saving_account
    where year(Opening_Date) = ye
	and month(Opening_Date) <= se*3
    and month(Opening_Date) > (se-1)*3
	and account.A_ID = saving_account.A_ID
	and B_Name = bank_name
	into money;
      
	select count(C_ID)
    from checking
    where A_Type = 1
    and B_Name = bank_name
	and A_ID in (	select A_ID
					from account
					where year(Opening_Date) = ye
                    and month(Opening_Date) <= se*3
					and month(Opening_Date) > (se-1)*3)
	into num;
    
    if money is null then
        set money = 0;
    end if;
    
    if num is null then
        set num = 0;
    end if;
END //
Delimiter ;