use exp1;
select reader.name,reader.ID
from reader
where reader.ID not in(
select distinct reader.ID from (borrow inner join reader on reader.ID=borrow.Reader_ID)
where Book_ID in
(select Book_ID from (borrow inner join reader on reader.ID=borrow.Reader_ID)
where reader.name='李林')
);