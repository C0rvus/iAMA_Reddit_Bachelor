# What is this all about?
This repository contains code for an iAMA overhaul I have to create because of my bachelor thesis, which is about the design and implementation of an overhaul for the iAMA subreddit to enhance the users reading experience.
So this is a two step process. First some reddit data needs to be analyzed and afterwards upon the gained insights I will create and implement a better dashboard / layout.

## What does this repository offer me?
1. Scripts to crawl data from reddit and write them into a database
2. Scripts to analyze the crawled data
2. The new iAMA - overhaul

## What languages / setup do you want use to acheive your goals?
Python, HTML5, CoffeeScript, LESS, MongoDB

## How can I use it?
### Crawling data:
1. Install mongoDB on your client (localhost) and do not set up any special permissions. Also make sure you have enough disk space available (~50 GB)
2. Install Python 3.5.1
3. Run the scripts with the prefix "crawl" within ./python/ - Folder.

*Usage examples down below*

    code python crawl_threads_n_comments.py threads 2009 2014 96
    code python crawl_differences.py 2009 2010 backward

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

    code python crawl_threads_n_comments.py {crawl_type} {year_begin} {year_end} {shift_hours}
>	{crawl_type}	= 		the type of data you want to be crawled and written into the database
>			=		threads || comments
>	{year_begin}	= 		The year you want the start the crawling process on
>			=		2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016
>	{year_end}	= 		The year you want the crawling process to stop. The year defined here is included (!!) within the crawling process..
>	  		=		2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016
>	{shift_hours}	=		The time units (hours) the crawler will move forward in crawling.. Because crawling stepwise asks the reddit server for new data, it is necessary to do this is little intervals.. a value of 96 is good
>			=		{int}

*Usage examples down below*

    code python crawl_threads_n_comments.py threads 2009 2014 96
    code python crawl_threads_n_comments.py threads 2009 2014 96
    code python crawl_threads_n_comments.py threads 2009 today 128



* [Commit Type]: [#IssueID] [Main Description]

It should look like the following:

* Added:    #120 Finished exercise 1
* Changed:  #124 Changed behaviour of method XY
* Fixed:    #127 Fixed null point reference

## Authors:
* C0rvus                        (Benedikt Hierl)