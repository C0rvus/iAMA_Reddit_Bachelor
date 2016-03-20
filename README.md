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

1. Install mongoDB on your client (localhost) and do not set up any special permissions (so everbody can access it). Also make sure you have enough disk space available (~50 GB)
2. Install Python 3.5.1 on your client
3. Make sure having needed python modules (praw, numpy, pymongo) installed on your client

### Crawling data:
1. Run the scripts with the prefix "***crawl***" within **./python/** - folder.

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
Crawls threads and comments into the regarding databases

    python crawl_threads_n_comments.py {crawl_type} {year_begin} {year_end} {shift_hours}

    
* **crawl_type** = **[threads || comments]** *The type of data you want to be crawled and written into the database*
 
* **year_begin** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]** *The year you want the start the crawling process on*

* **year_end** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]** *The year you want the crawling process to stop. The year defined here is included (!!) within the crawling process..*

* **shift_hours**	= **[int]** *The time units (hours) the crawler will move forward in crawling.. Because crawling stepwise asks the reddit server for new data, it is necessary to do this is little intervals.. a value of 96 is good*

*Usage examples shown down below*

    python crawl_threads_n_comments.py threads 2009 2014 96
    python crawl_threads_n_comments.py threads 2009 2014 96
    python crawl_threads_n_comments.py threads 2009 today 128

    
#### crawl\_differences.py
Compares regarding threads and comments databases and crawls missing collections

    python crawl_differences.py {year_begin} {year_end} {direction}
    
    
* **year_begin** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]** The year you want the start the crawling process on 

* **year_end** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]** The year you want the crawling process to stop. The year defined here is included (!!) within the crawling process..

* **direction**	= **[forward || backward]** Defines the direction in which the comparison and crawling process should be started (from the last to the first collection - and vice versa). This is helpful if you want to speed up the crawling process so you can start one crawler forward and the other one backward. The scripts have a fallback mechanism which enables them to not write information twice into the database. So before every write process into the database it will be checked whether that actually processed collection already exists in the database or not.

*Usage examples shown down below*

    python crawl_differences.py 2009 2010 backward
    python crawl_differences.py 2009 2016 forward
    python crawl_differences.py 2009 2009 forward


### Analyzing data:
1. Run the scripts with the prefix ***"analyze"*** within **./python/** - folder.

The analyzing scripts iterates over the documents / collections within the databases and calculate various things which will be explained down below:


#### analyze\_correlation\_upvote\_reaction\_time\_pieChart.py

Plots a scatter chart which contains values of the upvotes of answered questions (by the iAMA host) and the repsonse time of the iAma host to those questions. Additionally Pearsons Ro und the regarding p-value will be calculated and printed into the plots title bar.

    python analyze_correlation_upvote_reaction_time_pieChart.py {year} {tier} {time} {plot_x_limit}

    
* **year** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]** The year which is to be used for the calculation

* **tier** = **[1 || x || any]** The tier which will be in scope. 1 only looks at the first tier, x looks on any other tier except tier 1, any looks on all tiers

* **time** = **[minutes || hours]** The time units in which the calculated values will be seperated into.. (necessary for graph plotting)

* **plot_x_limit**	=	**[int]**	Limits the plot on the x scale.. Useful if you only want to look at given response times.. 0 means no limit


*Usage examples shown down below*

    python analyze_correlation_upvote_reaction_time_pieChart.py 2009 any hours 0
    python analyze_correlation_upvote_reaction_time_pieChart.py 2010 1 minutes 500
    python analyze_correlation_upvote_reaction_time_pieChart.py 2009 x hours 200


#### analyze\_thread\_lifeSpan\_n\_average\_commentTime_pieChart.py 
Calculates how long a thread lives and the average comment time - for the given year and additionally plots a pie chart with that information.

    python analyze_thread_lifeSpan_n_average_commentTime_pieChart.py {year} {calc} {time}

    
* **year** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]** The year which is to be used for the calculation 

* **calc** = **[lifespan || comment]** The data you want to calculate 

* **time** = **[min || hours || days]** The time units in which the calculated values will be seperated into for plotting.. 



*Usage examples shown down below*

    python analyze_thread_lifeSpan_n_average_commentTime_pieChart.py 2009 lifespan days
    python analyze_thread_lifeSpan_n_average_commentTime_pieChart.py 2014 comment hours
    python analyze_thread_lifeSpan_n_average_commentTime_pieChart.py 2012 lifespan minutes


#### analyze\_tier\_answered\_percentage\_pieChart.py
Plots a pieChart which contains the distribution of questions answered per tier for the given year.

    python analyze_tier_answered_percentage_pieChart.py {year} {tier}

    
* **year** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]** The year which is to be used for the calculation 

* **tier** = **[1 || x || any]** The tier which will be in scope. 1 only looks at the first tier, x looks on any other tier except tier 1, any looks on all tiers

*Usage examples shown down below*

    python analyze_tier_answered_percentage_pieChart.py 2009 1
    python analyze_tier_answered_percentage_pieChart.py 2011 x
    python analyze_tier_answered_percentage_pieChart.py 2015 any    


#### analyze\_tier\_answered\_time\_pieChart.py 
Calculates the arithmetic mean of the iAMA hosts response time to questions depending on the tier and the time_value given and plots a pie chart with those information.

    python analyze_tier_answered_time_pieChart.py {year} {tier} {time}

    
* **year** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]** The year which is to be used for the calculation 

* **tier** = **[1 || x || any]** The tier which will be in scope. 1 only looks at the first tier, x looks on any other tier except tier 1, any looks on all tiers

* **time** = **[minutes || hours]** The time units in which the calculated values will be seperated into.. (necessary for graph plotting) 

*Usage examples shown down below*

    python analyze_tier_answered_time_pieChart.py 2011 1 minutes
    python analyze_tier_answered_time_pieChart.py 2012 x hours
    python analyze_tier_answered_time_pieChart.py 2009 any hours    


#### analyze\_tier\_question\_distribution\_pieChart.py
Plots a pieChart which shows the distrubtion of questions on tier 1 and the rest - how many questions rely on the first tier and how mana rely on the remaining tiers.

    python analyze_tier_question_distribution_pieChart.py {year}

    
* **year** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]** The year which is to be used for the calculation 


*Usage examples shown down below*

    python analyze_tier_question_distribution_pieChart.py 2009
    python analyze_tier_question_distribution_pieChart.py 2011
    python analyze_tier_question_distribution_pieChart.py 2014


#### analyze\_top100\_pieChart.py 
Calculates how many of the top / worst 100 questions have been answered. A top / worst question is a question with the highest / lowest amount of votes. A pie chart will be plotted for visualisation.

    python analyze_top100_pieChart.py {year} {rate}

    
* **year** = **[2009 || 2010 || 2011 || 2012 || 2013 || 2014 || 2015 || 2016]** The year which is to be used for the calculation 

* **rate** = **[top || worst]** The best or worst voted questions you want to have a look at 

*Usage examples shown down below*

    python analyze_top100_pieChart.py 2009 top
    python analyze_top100_pieChart.py 2011 worst
    python analyze_top100_pieChart.py 2010 worst

### Usage of overhaul:

This is actually not in development yet.