use exp1;
select book.ID,book.name
from book inner join borrow on book.ID=borrow.Book_ID inner join reader on borrow.Reader_ID=reader.ID
where reader.name='李林' and Return_Date is null;