@Echo off

setlocal

REM Restores all threads into the database
mongorestore.exe --host localhost --db iAMA_Reddit_Threads_2009 T:\iAMA_Reddit_Threads_2009\
mongorestore.exe --host localhost --db iAMA_Reddit_Threads_2010 T:\iAMA_Reddit_Threads_2010\
mongorestore.exe --host localhost --db iAMA_Reddit_Threads_2011 T:\iAMA_Reddit_Threads_2011\
mongorestore.exe --host localhost --db iAMA_Reddit_Threads_2012 T:\iAMA_Reddit_Threads_2012\
mongorestore.exe --host localhost --db iAMA_Reddit_Threads_2013 T:\iAMA_Reddit_Threads_2013\
mongorestore.exe --host localhost --db iAMA_Reddit_Threads_2014 T:\iAMA_Reddit_Threads_2014\
mongorestore.exe --host localhost --db iAMA_Reddit_Threads_2015 T:\iAMA_Reddit_Threads_2015\
mongorestore.exe --host localhost --db iAMA_Reddit_Threads_2016 T:\iAMA_Reddit_Threads_2016\

REM Restores all comments into the database
mongorestore.exe --host localhost --db iAMA_Reddit_Comments_2009 T:\iAMA_Reddit_Comments_2009\
mongorestore.exe --host localhost --db iAMA_Reddit_Comments_2010 T:\iAMA_Reddit_Comments_2010\
mongorestore.exe --host localhost --db iAMA_Reddit_Comments_2011 T:\iAMA_Reddit_Comments_2011\
mongorestore.exe --host localhost --db iAMA_Reddit_Comments_2012 T:\iAMA_Reddit_Comments_2012\
mongorestore.exe --host localhost --db iAMA_Reddit_Comments_2013 T:\iAMA_Reddit_Comments_2013\
mongorestore.exe --host localhost --db iAMA_Reddit_Comments_2014 T:\iAMA_Reddit_Comments_2014\
mongorestore.exe --host localhost --db iAMA_Reddit_Comments_2015 T:\iAMA_Reddit_Comments_2015\
mongorestore.exe --host localhost --db iAMA_Reddit_Comments_2016 T:\iAMA_Reddit_Comments_2016\