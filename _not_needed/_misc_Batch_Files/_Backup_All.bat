@Echo off

REM Backup of Comments
mongodump -d iAMA_Reddit_Comments_2009 -o Y:\_Backups\mongoDB\%date%\
mongodump -d iAMA_Reddit_Comments_2010 -o Y:\_Backups\mongoDB\%date%\
mongodump -d iAMA_Reddit_Comments_2011 -o Y:\_Backups\mongoDB\%date%\
mongodump -d iAMA_Reddit_Comments_2012 -o Y:\_Backups\mongoDB\%date%\
mongodump -d iAMA_Reddit_Comments_2013 -o Y:\_Backups\mongoDB\%date%\
mongodump -d iAMA_Reddit_Comments_2014 -o Y:\_Backups\mongoDB\%date%\
mongodump -d iAMA_Reddit_Comments_2015 -o Y:\_Backups\mongoDB\%date%\
mongodump -d iAMA_Reddit_Comments_2016 -o Y:\_Backups\mongoDB\%date%\

REM Backup of Threads
mongodump -d iAMA_Reddit_Threads_2009 -o Y:\_Backups\mongoDB\%date%\
mongodump -d iAMA_Reddit_Threads_2010 -o Y:\_Backups\mongoDB\%date%\
mongodump -d iAMA_Reddit_Threads_2011 -o Y:\_Backups\mongoDB\%date%\
mongodump -d iAMA_Reddit_Threads_2012 -o Y:\_Backups\mongoDB\%date%\
mongodump -d iAMA_Reddit_Threads_2013 -o Y:\_Backups\mongoDB\%date%\
mongodump -d iAMA_Reddit_Threads_2014 -o Y:\_Backups\mongoDB\%date%\
mongodump -d iAMA_Reddit_Threads_2015 -o Y:\_Backups\mongoDB\%date%\
mongodump -d iAMA_Reddit_Threads_2016 -o Y:\_Backups\mongoDB\%date%\
