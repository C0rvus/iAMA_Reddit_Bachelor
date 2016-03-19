# What is this all about?
This repository contains code for an iAMA overhaul I have to create because of my bachelor thesis, which is about the design and implementation of an overhaul for the iAMA subreddit to enhance the users reading experience.
So this is a two step process. First some reddit data needs to be analyzed and afterwards upon the gained insights I will create and implement a better dashboard / layout.

## What does this repository offer to me?
1. Scripts to crawl data from reddit and write them into a database
2. Scripts to analyze the crawled data
2. The new iAMA - overhaul

## What languages / setup do you want use to acheive your goals?
Python, HTML5, CoffeeScript, LESS, MongoDB

## How can I use it?

### Prerequisites

1. Install mongoDB on your client (localhost) and do not set up any special permissions. Also make sure you have enough disk space available (~50 GB)
2. Install Python 3.5.1

### Crawling data:

1. Run the scripts with the prefix "crawl" within ./python/ - Folder.

The Crawling scripts automatically create the databases they write their information into by theirselves. 
You will be having database of two types:

>iAMA\_Reddit\_Threads_{year}

>iAMA\_Reddit\_Comments_{year}

Each database contains a collection with the name of the appropriate crawled thread.

In the "iAMA\_Reddit\_Threads_{year}" each document only holds one collection containing the following information about a thread:

>	"_id"		=		The dynamically generated id from the mongo db

>	"author"	=		The author of the thread

>	"created_utc"	=		The timestamp when that thread has been created (timestamp is in unix epoch formatation)

>	"downs"		=		The amount of downvotes that thread has received

>	"num_Comments"	=		The amount of comments that thread has received.. (This number differs from the actually parsed comments [this is because reddit does not allow you to crawl already deleted comments...]

>	"selftext"	=		The selftext of the thread. In the early years of reddit there were no selftext, therefore that value may be empty in some databases

>	"title"		=		The iAMAs title

>	"ups"		=		The amount of upvotes

In the "iAMA\_Reddit\_Comments_{year}" each document holds one collection for every comment within that thread, containing the following information:

>	"_id"		=		The dynamically generated id from the mongo db

>	"author"	=		The author of the thread

>	"body"		=		The text of the comment

>	"name"		=		The id of the thread within the hierarchy [i.e. t1_c09vabt]

>	"parent_id"	=		The id to which that comment relates to in the hierarchy [i.e. t3_8nron]

>	"ups"		=		The amount of upvotes

#### crawl\_threads\_n\_comments.py

* Crawls threads and comments into the regarding databases*

    code python crawl_threads_n_comments.py {crawl_type} {year_begin} {year_end} {shift_hours}
    
>	{crawl_type}	= 		the type of data you want to be crawled and written into the database

>			=		threads || comments

>	{year_begin}	= 		The year you want the start the crawling process on

>			=		2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016

>	{year_end}	= 		The year you want the crawling process to stop. The year defined here is included (!!) within the crawling process..

>	  		=		2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016

>	{shift_hours}	=		The time units (hours) the crawler will move forward in crawling.. Because crawling stepwise asks the reddit server for new data, it is necessary to do this is little intervals.. a value of 96 is good

>			=		{int}

*Usage examples shown down below*

    code python crawl_threads_n_comments.py threads 2009 2014 96
    code python crawl_threads_n_comments.py threads 2009 2014 96
    code python crawl_threads_n_comments.py threads 2009 today 128
    
#### crawl\_differences.py

* Compares regarding threads and comments databases and crawls missing collections* 

    code python crawl_differences.py {year_begin} {year_end} {direction}
    
    
>	{year_begin}	= 		The year you want the start the crawling process on

>			=		2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016

>	{year_end}	= 		The year you want the crawling process to stop. The year defined here is included (!!) within the crawling process..

>			=		2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016

>	{direction}	=		Defines the direction in which the comparison and crawling process should be started (from the last to the first collection - and vice versa). This is helpful if you want to speed up the crawling process so you can start one crawler forward and the other one backward. The scripts have a fallback mechanism which enables them to not write information twice into the database. So before every write process into the database it will be checked whether that actually processed collection already exists in the database or not.

>			=		forward || backward

*Usage examples shown down below*

    code python crawl_differences.py 2009 2010 backward
    code python crawl_differences.py 2009 2016 forward
    code python crawl_differences.py 2009 2009 forward


### Analyzing data:

1. Run the scripts with the prefix "analyze" within ./python/ - Folder.

The analyzing scripts iterates over the documents / collections within the databases and calculate various things which will be explained down below:


#### analyze_thread_lifeSpan_n_average_commentTime_pieChart.py 

* Calculates how long a thread lives and the average comment time - for the given year

    code python analyze_thread_lifeSpan_n_average_commentTime_pieChart.py {year} {calc} {time}
    
>		{year} 		= 		the year which is to be used for the calculation

>			=		2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016

>	{calc}		= 		the data you want to calculate

>			=		lifespan || comment

>			=		lifespan if you want to calculate the lifespan of a thread, comment is when you want to calculate the average mean comment time within the thread

>	{time}		=		the time units in which the calculated values will be seperated into.. (necessary for graph plotting)

>			=		min || hours || days

>			=		min is for minutes, hours is for separation into hours, days is for seperation into days   