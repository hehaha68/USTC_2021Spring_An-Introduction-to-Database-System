use exp1;
select book.name,Borrow_Date
from book,borrow,reader
where book.ID=borrow.Book_ID and reader.ID=borrow.Reader_ID
and reader.name='Rose';