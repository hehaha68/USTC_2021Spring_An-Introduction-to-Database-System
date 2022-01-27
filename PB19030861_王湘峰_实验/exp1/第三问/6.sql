use exp1;
select name
from reader,borrow where reader.ID=borrow.Reader_ID
group by reader_ID 
having count(Book_ID)>3 ;