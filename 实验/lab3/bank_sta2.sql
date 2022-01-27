Delimiter //
DROP PROCEDURE IF EXISTS dkyear;
create 
	definer = root@localhost procedure dkyear(
    IN ye int, in bank_name varchar(50), OUT money float, OUT num int)
BEGIN

    select sum(P_Amount)
    from loan,apply
    where year(Pay_Date) = ye
	and loan.L_ID = apply.L_ID
	and B_Name = bank_name
	into money;
      
	select distinct count(C_ID)
    from loan,apply
    where B_Name = bank_name
	and loan.L_ID = apply.L_ID
    and year(Pay_Date) = ye
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
DROP PROCEDURE IF EXISTS dkmonth;
create 
	definer = root@localhost procedure dkmonth(
    IN ye int, IN mo int, in bank_name varchar(50), OUT money float, OUT num int)
BEGIN

    select sum(P_Amount)
    from loan,apply
    where year(Pay_Date) = ye
    and month(Pay_Date) = mo
	and loan.L_ID = apply.L_ID
	and B_Name = bank_name
	into money;
      
	select distinct count(C_ID)
    from loan,apply
    where B_Name = bank_name
	and loan.L_ID = apply.L_ID
    and year(Pay_Date) = ye
    and month(Pay_Date) = mo
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
DROP PROCEDURE IF EXISTS dkseason;
create 
	definer = root@localhost procedure dkseason(
    IN ye int, IN se int, in bank_name varchar(50), OUT money float, OUT num int)
BEGIN

    select sum(P_Amount)
    from loan,apply
    where year(Pay_Date) = ye
    and month(Pay_Date) <= se*3
    and month(Pay_Date) > (se-1)*3
	and loan.L_ID = apply.L_ID
	and B_Name = bank_name
	into money;
      
	select distinct count(C_ID)
    from loan,apply
    where B_Name = bank_name
	and loan.L_ID = apply.L_ID
    and year(Pay_Date) = ye
    and month(Pay_Date) <= se*3
    and month(Pay_Date) > (se-1)*3
	into num;
    
    if money is null then
        set money = 0;
    end if;
    
    if num is null then
        set num = 0;
    end if;
END //
Delimiter ;