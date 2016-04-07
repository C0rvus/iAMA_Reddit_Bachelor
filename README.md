# What is this all about?
This repository contains code for an iAMA overhaul I have to create because of my bachelor thesis, which is about the
design and implementation of an overhaul for the ***iAMA***-subreddit to enhance the users reading experience.
So this is a three step process.
First some reddit data needs to be crawled into a local database.
Second that locally stored informatio needs to be analyzed.
Third depending on the analyzation results the new webpage will have to be built equivalent. 
 
## What does this repository offer to me?
1. Scripts to crawl data from reddit and write them into a database
2. Scripts to analyze the crawled data
3. The new iAMA - overhaul

## What languages / setup do you want use to acheive your goals?
Python, HTML5, CoffeeScript, LESS, MongoDB

## How can I use it?
To make use of this repository please follow the instructions below.

### Prerequisites

1. Make sure you have enough disk space available (~50 GB) (necessary because of data crawling).
2. Install mongoDB on your client (localhost) and do not set up any special permissions (so everbody can access it). 
3. Install Python 3.5.1 on your client (I recommend using the 64 bit version, because it uses up lots of RAM).
4. Make sure you have the necessary python modules (praw, numpy, pandas, pymongo) installed on your client.
5. Make sure to have your mongoDB up, running and accessible (you can check that i.E. by connecting via **Robomongo**)

# Crawl data:
1. Run the scripts with the prefix "***c_***" within **./python/** - folder.

The Crawling scripts automatically create the databases they write their information into by theirselves. 
You will be having database of two types:

>iAMA\_Reddit\_Threads_{year}

>iAMA\_Reddit\_Comments_{year}

Each database contains a collection with the name of the appropriate crawled thread.

In the "iAMA\_Reddit\_Threads_{year}" database each document only holds one collection containing the 
following thread information:

>	"_id"	 =		The dynamically generated id from the mongo db

>	"author"	    =		The author of the thread

>	"created_utc"	=		The timestamp when that thread has been created (timestamp is in unix epoch formatation)

>	"downs"		=		The amount of downvotes that thread has received

>	"num_Comments"	=		The amount of comments that thread has received.. (skewed by Reddit Anti-Bot system..)

>	"selftext"	=		The selftext of the thread. Value can be empty on some years

>	"title"		=		The iAMA threads title

>	"ups"		=		The amount of upvotes

In the "iAMA\_Reddit\_Comments_{year}" database  each document holds one collection for every comment within that thread,
containing the following information:

>	"_id"		=		The dynamically generated id from the mongo db

>	"author"	=		The author of the thread

>	"body"		=		The text of the comment

>	"name"		=		The id of the thread within the hierarchy [i.e. t1_c09vabt]

>	"parent_id"	=		The id to which that comment relates to in the hierarchy [i.e. t3_8nron]

>	"ups"		=		The amount of upvotes

For a better understanding simply look at the picture in **.\_picutres\db_hierarchy.jpg** within this repository.

## c\_crawl\_Differences.py
Compares threads and comments databases and crawls missing collections.
By initially crawling information about threads and database you can sometimes have an unequal amount of documents
between the databases. This is because crawling uses some sort of amazon cloud search which is not always working 
reliable.

    python crawl_differences.py {year_beginning} {year_ending} {direction}
    
    
* **year_begin** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]** The year you want the start
 the crawling process on 

* **year_end** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]** The year you want the crawling
 process to stop. The year defined here is included (!!) within the crawling process..

* **direction** = **[forward || backward]** Defines the direction in which the comparison and crawling process 
 should be started (from the last to the first collection - and vice versa). This is helpful if you want to speed up 
 the crawling process so you can start one crawler forward and the other one backward. The scripts have a fallback 
 mechanism which enables them to not write information twice into the database. So before every write process into the 
 database it will be checked whether that actually processed collection already exists in the database or not.

*Usage examples shown down below*

    python crawl_differences.py 2009 2010 backward
    python crawl_differences.py 2009 2016 forward
    python crawl_differences.py 2009 2009 forward


## c\_crawl\_Threads\_N\_Comments.py
Crawls threads and comments into the regarding databases

    python crawl_threads_n_comments.py {crawl_type} {year_begin} {year_end} {shift_hours}

    
* **crawl_type** = **[threads || comments]** *The type of data you want to be crawled and written into the database*
 
* **year_begin** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]** *The year you want the start
 the crawling process on*

* **year_end** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]** *The year you want the crawling
 process to stop. The year defined here is included (!!) within the crawling process..*

* **shift_hours** = **[int]** *The time units (hours) the crawler will move forward in crawling.. 
 Because crawling  asks the reddit server for new data stepwise - so it is necessary to do this is little intervals..
  a value of 96 is good*

*Usage examples shown down below*

    python crawl_threads_n_comments.py threads 2009 2014 96
    python crawl_threads_n_comments.py threads 2009 2014 96
    python crawl_threads_n_comments.py threads 2009 today 128


# Analyze data:
1. Run the scripts with the prefix ***"a_"*** within **./python/** - folder.

The analyzing scripts iterate over the documents / collections within the databases and calculate various things
 which will be explained down below:

## a\_everything\_Big\_CSV\_analyzer.py

This script calculates all possible correlations / arithmetic means, etc.. with the data, stored in csv-files, which
have been exported from the database. We use .csv-files for it because it allows use to user alternative
analysis-frameworks like **WEKA**.

To make use of it, you just need two .csv-files within the same folder the script is running in.

* **d\_create\_Big\_CSV\_2009\_until\_2016\_BIGDATA\_ALL.csv**
* **a\_question_Answered\_Yes\_No\_Tier\_Percentage\_2009\_until\_2016\_ALL\_tier\_any.csv**

You get those two .csv files by running 

    python d_create_Big_CSV.py 2009 2016
    python a_question_Answered_Yes_No_Tier_Percentage.py 2009 2016 any
    
It printlines the various calculation results into the console output.


## a\_iAMA\_Commenttime.py

This script script calculates the time the iAma host needs to react / respond to a comment / question which has been
posted in his thread.
It also creates .csv-values with all values for the currently processed year (and all years) and additionally
 creates an interactive chart which gives you some visual insight into the data and relations.

    python a_iAMA_Commenttime.py {year_beginning} {year_ending} {tier} {time}

    
* **year_beginning** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]** 
The year which is to be used for the calculation

* **year_ending** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]**
The year which is to be used for the calculation and represents when the calculation should stop

* **tier** = **[1 || x || any]** The tier which will be in scope. 1 only looks at the first tier,
 x looks on any other tier except tier 1, any looks on all tiers

* **time** = **[minutes || hours || days]** The time units in which the calculated values will be seperated into..
 (necessary for graph plotting)


*Usage examples shown down below*

    python a_iAMA_Commenttime.py 2009 2016 any days
    python a_iAMA_Commenttime.py 2012 2016 1 minutes
    python a_iAMA_Commenttime.py 2009 2010 x hours


## a\_question_Answered\_Yes\_No\_Extrema 
Calculates how many of the top / worst X questions have been answered.
A top / worst question is a question with the highest / lowest amount of votes. X is the amount of questions you want
the script to do calculations on.

It also creates .csv-values with all values for the currently processed year (and all years) and additionally
 creates an interactive chart which gives you some visual insight into the data and relations.
 

    python a_question_Answered_Yes_No_Extrema.py {year_beginning} {year_ending} {rate}

    
* **year_beginning** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]** 
The year which is to be used for the calculation

* **year_ending** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]**
The year which is to be used for the calculation and represents when the calculation should stop  

* **rate** = **[top || worst]** The best or worst voted questions you want to have a look at

*Usage examples shown down below*

    python a_question_Answered_Yes_No_Extrema 2009 2016 top
    python a_question_Answered_Yes_No_Extrema 2009 2016 worst
    python a_question_Answered_Yes_No_Extrema 2012 2014 top


## a\_question\_Answered\_Yes\_No\_Tier\_Percentage.py
Analyzes how many questions have been answered by the iAMA host on a given time span and year.

It also creates .csv-values with all values for the currently processed year (and all years) and additionally
 creates an interactive chart which gives you some visual insight into the data and relations.

    python a_question_Answered_Yes_No_Tier_Percentage.py {year_beginning} {year_ending} {tier}

    
* **year_beginning** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]** 
The year which is to be used for the calculation

* **year_ending** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]**
The year which is to be used for the calculation and represents when the calculation should stop 

* **tier** = **[1 || x || any]** The tier which will be in scope. 1 only looks at the first tier,
 x looks on any other tier except tier 1, any looks on all tiers


*Usage examples shown down below*

    python a_question_Answered_Yes_No_Tier_Percentage.py 2009 2016 any
    python a_question_Answered_Yes_No_Tier_Percentage.py 2009 2013 1
    python a_question_Answered_Yes_No_Tier_Percentage.py 2009 2011 x
    
    
## a\_question\_Tier\_Distribution.py
Calculates the distribution of questions for the given years. It only decides whether a question has been posted
on tier 1 or on any other tier.

It also creates .csv-values with all values for the currently processed year (and all years) and additionally
 creates an interactive chart which gives you some visual insight into the data and relations.


    python a_question_Tier_Distribution.py {year_beginning} {year_ending}

    
* **year_beginning** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]** 
The year which is to be used for the calculation

* **year_ending** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]**
The year which is to be used for the calculation and represents when the calculation should stop  


*Usage examples shown down below*

    python analyze_tier_question_distribution_pieChart.py 2009 2016
    python analyze_tier_question_distribution_pieChart.py 2011 2012
    python analyze_tier_question_distribution_pieChart.py 2010 2013


## a\_thread\_Lifespan\_N\_Average\_Commenttime.py
This script calculates two things

1. The average lifespan of a thread until the last reaction had been done (last question / comment posted)

2. The average reaction time between posted comments 
(so you can say.. in the year 2009 ever X seconds a new comment has been posted)

It also creates .csv-values with all values for the currently processed year (and all years) and additionally
 creates an interactive chart which gives you some visual insight into the data and relations.

    python a_thread_Lifespan_N_Average_Commenttime.py {year_beginning} {year_ending} {calc_type} {time}

    
* **year_beginning** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]** 
The year which is to be used for the calculation

* **year_ending** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]**
The year which is to be used for the calculation and represents when the calculation should stop

* **calc** = **[lifespan || comment]** The type of data you want to calculate 

* **time** = **[minutes || hours || days]** The time units in which the calculated values will be seperated into..
 (necessary for graph plotting)


*Usage examples shown down below*

    python a_thread_Lifespan_N_Average_Commenttime 2009 2016 lifespan days
    python a_thread_Lifespan_N_Average_Commenttime 2009 2012 comment hours
    python a_thread_Lifespan_N_Average_Commenttime 2009 2010 lifespan minutes


# Generate one big data file:

## d\_create\_Big\_CSV.py

Every analyze script creates its own inidivual .csv - files.. So it might be difficult to do calculations on the ***WHOLE***
 reddit dataset by using those seperated files, because they contain slightly different information, depending on the 
 script they were created from. (Some scripts need some special filtering [i.E. skipping thread with no questions in it, etc.].

To not fiddle around with those seperated scripts and to have one conglomerat containing all information ever possible
you can use this script here.
 
I really recommend using ***this script*** if you want to do complete research on the ***WHOLE*** reddit
dataset

    python d_create_Big_CSV.py {year_beginning} {year_ending}
    
   
* **year_beginning** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]** 
The year which is to be used for the calculation

* **year_ending** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]**
The year which is to be used for the calculation and represents when the calculation should stop

*Usage examples shown down below*

    python d_create_Big_CSV.py 2009 2016
    python d_create_Big_CSV.py 2009 2012
    python d_create_Big_CSV.py 2012 2013

## Usage of overhaul:

This is actually not in development yet.