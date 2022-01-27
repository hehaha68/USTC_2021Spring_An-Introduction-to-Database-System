use exp1;
select name from reader
where reader.ID not in
(select distinct Reader_ID from borrow);