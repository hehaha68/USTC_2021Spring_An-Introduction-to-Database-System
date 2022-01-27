use exp1;
CREATE VIEW `Reader_Borrow` AS
select Reader.ID as readerID,Reader.name as readername ,Book.ID as bookID,Book.name as bookname,Borrow_Date
from book,borrow,reader
where reader.ID=borrow.Reader_ID and borrow.Book_ID=Book.ID;

select readerID,count(distinct bookID)
from reader_borrow rb
where rb.Borrow_Date>date_sub(now(),interval 1 year)
group by readerID;