#   Tutorials used within this class:
#   1. (06.02.2016 @ 15:23) -
#           http://www.esqsoft.com/javascript_examples/date-to-epoch.htm
#   2. (06.02.2016 @ 15:48) -
#           https://www.reddit.com/r/redditdev/comments/2zdyy2/praw_continue_getting_posts_after_given_post_id/
#   3. (06.02.2016 @ 16:20) -
#           https://www.linuxquestions.org/questions/programming-9/python-datetime-to-epoch-4175520007/
#   4. (06.02.2016 @ 16:30) -#
#           https://stackoverflow.com/questions/11743019/convert-python-datetime-to-epoch-with-strftime
#   This script is developed with PRAW 3.3.0

import praw                                 # Necessary for crawling data from reddit
import time                                 # Necessary to do some time calculations
import collections                          # Necessary for dictionary sorting
import sys                                  # Necessary to use script arguments
from pymongo import MongoClient             # Necessary to interact with MongoDB
from datetime import datetime, timedelta    # Necessary to calculate time shifting windows for onward crawling


def initialize_mongo_db_parameters():
    """Instantiates all necessary variables for the correct usage of the mongoDB-Client

    Args:
        -
    Returns:
        -
    """

    global mongo_DB_Client_Instance
    global reddit_Instance
    mongo_DB_Client_Instance = MongoClient('localhost', 27017)
    reddit_Instance = praw.Reddit(user_agent="University_Regensburg_iAMA_Crawler_0.001")


def check_script_arguments():
    """Checks if enough and correct arguments have been given to run this script adequate

    1. It checks in the first instance if enough arguments have been given
    2. Then necessary variables will be filled with appropriate values

    Args:
        -
    Returns:
        -
    """

    global argument_year_beginning, argument_year_end, argument_hours_to_shift, argument_crawl_type

    # Whenever not enough arguments were given
    if len(sys.argv) <= 3:
        print("Not enough arguments were given...")
        print("Terminating script now!")
        sys.exit()
    else:

        # Decides what to crawl here. Comments or threads
        argument_crawl_type = str(sys.argv[1])

        # Writes necessary values into the variables
        argument_year_beginning = convert_argument_year_to_epoch(str(sys.argv[2]))

        # It is necessary to add + 1 here, otherwise it would only crawl the amount "argument_hours_to_shift" for the
        # given year and it would end after one crawl attempt..
        argument_year_end = convert_argument_year_to_epoch(str(int(sys.argv[3]) + 1))

        # The amount of hours the crawler will shift into the "future"
        argument_hours_to_shift = int(sys.argv[4])


def convert_argument_year_to_epoch(year):
    """ "Converts" a given string into the appropriate epoch string format (int)

    Args:
        year (str) : The year which will be "converted" into epoch format (necessary for correct PRAW API behaviour)
    Returns:
        year (int) : The year "converted" into epoch format as integer
    """

    if year == "2009":
        # Starting time of the first iAMA post of Reddit    [ 2009-05-28 02:03:46 ]
        return 1243469026

    elif year == "2010":
        # [ 2010-01-01 00:00:00 ]
        return 1262300400

    elif year == "2011":
        # [ 2011-01-01 00:00:00 ]
        return 1293836400

    elif year == "2012":
        # [ 2012-01-01 00:00:00 ]
        return 1325372400

    elif year == "2013":
        # [ 2013-01-01 00:00:00 ]
        return 1356994800

    elif year == "2014":
        # [ 2014-01-01 00:00:00 ]
        return 1388530800

    elif year == "2015":
        # [ 2015-01-01 00:00:00 ]
        return 1420066800

    elif year == "2016":
        # [ 2016-01-01 00:00:00 ]
        return 1451602800

    elif year == "today":
        return int(time.time())

    else:
        print("Epoch time for given argument does not exist in the method 'convert_argument_year_to_epoch()' ")
        print("Using the current time instead of the given argument..")
        return int(time.time())


def crawl_data():
    """Crawls data from reddit, depending on the first argument (threads / comments) you give the script

    Args:
        -
    Returns:
        -
    """

    if argument_crawl_type == "threads":
        crawl_threads()
    elif argument_crawl_type == "comments":
        crawl_comments()
    else:
        print("Can not understand what you want me to crawl..")
        print("Terminating script now !")
        sys.exit()


def crawl_threads():
    """Crawls thread information and writes them into the mongoDB storage
    It works as follwoing:

    1. At first an attempt to the amazon cloud search will be made, with necessary parameters which returns an object,
        of the class "Generator" which contains all threads for the given / crawled time windows

    2. After that the "Generator"s elements will be iterated over

        2.1. It will be checked if that iterated collection already exists within the database or not

            2.2.1. If it already exists, it will be checked whether if it is up to date or not
                2.2.1.1. If up2date: do nothing
                2.2.1.2. If not up2date: drop that collection within the database and crawl the collection anew

            2.2.2. If it does not yet exist: create that collection in the database with the necessary information

    3. Whenever there are no elements left to iterate over the time crawling window will be shifted into the future by
        using the given amount in hours (third argument), whenever the ending year (second argument) is not reached yet

    Args:
        -
    Returns:
        -
    """

    global argument_year_beginning, time_shift_difference

    # Below is the crawl command to search within a dedicated time span from argument_year_beginning
    # to time_shift_difference. Time is used in epoch format

    posts = reddit_Instance.search(
        'timestamp:' +
        str(argument_year_beginning) +
        '..' +
        str(time_shift_difference),
        subreddit='iAMA',
        sort="new",
        limit=900,
        syntax="cloudsearch")

    for submission in posts:

        # Whenver the collection already exists in the database (True)
        if check_if_coll_in_db_already_exists_up2date(submission) is True:
            print("++ Thread " + str(submission.id) +
                  " already exists in mongoDB and is up2date")

        # Whenever the thread does not exist within the mongoDB (anymore) (False)
        else:
            print("    -- Thread " +
                  str(submission.id) +
                  " will be created now")

            # Because down votes are not accessable via reddit API, we have calculated it by our own here
            ratio = reddit_Instance.get_submission(submission.permalink).upvote_ratio

            total_votes = int(round((ratio * submission.score) / (2 * ratio - 1))
                              if ratio != 0.5 else round(submission.score / 2))

            downs = total_votes - submission.score

            # noinspection PyTypeChecker
            data_to_write_into_db = dict({
                'author': str(submission.author),
                'created_utc': str(submission.created_utc),
                'downs': int(downs),
                'num_Comments': str(submission.num_comments),
                'selftext': str(submission.selftext),
                'title': str(submission.title),
                'ups': int(submission.ups)
            })

            # Sorts that dictionary alphabetically ordered
            data_to_write_into_db = collections.OrderedDict(sorted(data_to_write_into_db.items()))

            # Converts the unix utc_time into a date format and converts it to string afterwards
            temp_submission_creation_year = str(datetime.fromtimestamp(submission.created_utc))

            temp_submission_creation_year = temp_submission_creation_year[:4]

            # This method says to look into the appropriate database, depending on the year the thread was created
            mongo_db_reddit = mongo_DB_Client_Instance["iAMA_Reddit_Threads_" + temp_submission_creation_year]

            # Writes the crawled information into the mongoDB
            collection = mongo_db_reddit[str(submission.id)]

            # Write the dictionary "data_to_write_into_db" into the mongo db right now!
            collection.insert_one(data_to_write_into_db)

    print(
        "------------ completed crawling data for " +
        str(argument_hours_to_shift) +
        " hours.. Continuing to the next time frame...")

    # Shifts argument_year_beginning with "argument_hours_to_shift" hours into the future
    argument_year_beginning = int(round(time.mktime((datetime.fromtimestamp(argument_year_beginning) +
                                                     timedelta(hours=argument_hours_to_shift)).timetuple())))

    # Shifts time_shift_difference with "argument_hours_to_shift" hours into the future
    time_shift_difference = int(round(time.mktime((datetime.fromtimestamp(time_shift_difference) +
                                                   timedelta(hours=argument_hours_to_shift)).timetuple())))

    # Whenever the destination time (time_shift_difference) to be crawled is newer than the
    # defined ending time:      set time_shift_difference to the argument_year_end
    if time_shift_difference > argument_year_end:
        time_shift_difference = argument_year_end

    # Whenever the starting time (argument_year_beginning) to be crawled is newer than the defined
    # ending time   :           end this method here
    elif argument_year_beginning > argument_year_end:
        return

    # Continue crawling
    else:
        crawl_threads()


def crawl_comments():
    """Crawls thread information and writes them into the mongoDB storage
    It works as follwoing:

    1. At first an attempt to the amazon cloud search will be made, with necessary parameters which returns an object,
        of the class "Generator" which contains all comments for the given / crawled time windows

    2. After that the "Generator"s elements will be iterated over

        2.1. It will be checked if that iterated collection already exists within the database or not

            2.2.1. If it already exists, it will be checked whether if it is up to date or not
                2.2.1.1. If up2date: do nothing
                2.2.1.2. If not up2date: drop that collection within the database and crawl the collection anew

            2.2.2. If it does not yet exist: create that collection in the database with the necessary information

    3. Whenever there are no elements left to iterate over the time crawling window will be shifted into the future by
        using the given amount in hours (fourth argument), whenever the ending year (third argument) is not reached yet

    Args:
        -
    Returns:
        -
    """

    global argument_year_beginning, time_shift_difference

    # Below is the crawl command to search within a dedicated time span from argument_year_beginning
    # to time_shift_difference. Time is used in epoch format
    posts = reddit_Instance.search(
        'timestamp:' +
        str(argument_year_beginning) +
        '..' +
        str(time_shift_difference),
        subreddit='iAMA',
        sort="new",
        limit=1000,
        syntax="cloudsearch"
    )

    for submission in posts:
        # Whenver the collection already exists in the database (True)
        if check_if_coll_in_db_already_exists_up2date(submission):
            print("++ Comments for " + str(submission.id) + " already exist in mongoDB and are up2date")

        # Whenever the thread does not yet exist within the mongoDB (anymore) (False)
        else:
            print("    -- Comments for " + str(submission.id) + " will be created now")

            # Replaces the objects of Type praw.MoreComments with comments
            # (i.e. iterates their tree to the end / expands all comments)
            submission.replace_more_comments(limit=None, threshold=0)

            # Breaks the tree hierarchy and returns a plan straight aligned
            # list containing all fulltext comments
            flat_comments = praw.helpers.flatten_tree(submission.comments)

            # Iterates over every single comment within the thread
            for idx, val in enumerate(flat_comments):

                # noinspection PyTypeChecker
                data_to_write_into_db = dict({
                    'author': str(val.author),
                    'body': str(val.body),
                    'created_utc': str(val.created_utc),
                    'name': str(val.name),
                    'parent_id': str(val.parent_id),
                    'ups': int(val.ups)
                })

                # Sorts that dictionary alphabetically ordered
                data_to_write_into_db = collections.OrderedDict(sorted(data_to_write_into_db.items()))

                # Converts the unix utc_time into a date format and converts it to string afterwards
                temp_submission_creation_year = str(datetime.fromtimestamp(submission.created_utc))
                temp_submission_creation_year = temp_submission_creation_year[:4]

                # This method says to look into the appropriate database,
                # depending on the year the thread was created
                mongo_db_reddit = mongo_DB_Client_Instance["iAMA_Reddit_Comments_" + temp_submission_creation_year]

                # Writes the crawled information into the mongoDB
                collection = mongo_db_reddit[str(submission.id)]

                # Write the dictionary "data_to_write_into_db" into the mongo db right now!
                collection.insert_one(data_to_write_into_db)

    print(
        "------------ completed crawling data for " + str(argument_hours_to_shift) +
        " hours.. Continuing to the next time frame now")

    # Shifts argument_year_beginning with "argument_hours_to_shift" hours into the future
    argument_year_beginning = int(round(time.mktime((datetime.fromtimestamp(argument_year_beginning) +
                                                     timedelta(hours=argument_hours_to_shift)).timetuple())))

    # Shifts time_shift_difference with "argument_hours_to_shift" hours into the future
    time_shift_difference = int(round(time.mktime((datetime.fromtimestamp(time_shift_difference) +
                                                   timedelta(hours=argument_hours_to_shift)).timetuple())))

    # Whenever the destination time (time_shift_difference) to be crawled is newer than the
    # defined ending time:      set time_shift_difference to the argument_year_end
    if time_shift_difference > argument_year_end:
        time_shift_difference = argument_year_end

    # Whenever the starting time (argument_year_beginning) to be crawled is newer than the defined
    # ending time   :      end this method here
    elif argument_year_beginning > argument_year_end:
        return

    # Continue crawling
    else:
        crawl_comments()


def check_if_coll_in_db_already_exists_up2date(submission):
    """Checks if a collection already exists in the database or not

    This is necessary, otherwise thread information would be written into the database twice.
    It works the following way:

    1. Define a tolerance factor (necessary because reddit skews information about the amount of
        "upvotes"). Without defining that tolerance factor every thread would be created anew.
        After messing around a few days I found this one to be the best value to work with

    2. Create values for temporary values for checking

    3. Check and recreate collection if necessary

    4. Return appropriate boolean value if collection already existed within the database or not


    Args:
        submission (Submission) : The thread which will be processed / iterated over at the moment
    Returns:
        True / False (bool) : Whenever the collection already exists within the database (True) or not (False)
    """

    # This is a tolerance factor because Reddit screws the "ups" - value. The "num_comments" - value remains consistent
    tolerance_factor = 25

    # Converts the unix utc_time into a date format and converts it to string afterwards
    temp_submission_creation_year = str(datetime.fromtimestamp(submission.created_utc))

    temp_submission_creation_year = temp_submission_creation_year[:4]

    # This method says to look into the appropriate database, depending on the year the thread was created
    mongo_db_reddit = mongo_DB_Client_Instance["iAMA_Reddit_Threads_" + temp_submission_creation_year]

    # Get all collections within that database
    mongo_db_collection = mongo_db_reddit.collection_names()

    # If it already exists, check whether it is up to date or not!
    if (str(submission.id)) in mongo_db_collection:

        # Select the appropriate collection within the database
        collection = mongo_db_reddit[str(submission.id)]

        # And store the selection in a cursor
        cursor = collection.find()

        # Because the amount of comments crawled (comments db) will always differ
        # (due to api restrictions) from the num_comments value
        # we check here wether the num_comments value has changed.. Whenever that is true the comments
        # collection in the comments database gets dropped
        # and has to be crawled anew by using the appropriate diff-crawler
        # script
        if cursor[0].get("num_Comments") != str(submission.num_comments):

            # Creates a new connect to the mongoDB
            comments_mongo_db_client_instance = MongoClient('localhost', 27017)

            # References to the appropriate year
            comments_mongo_db_reddit = comments_mongo_db_client_instance["iAMA_Reddit_Comments_" +
                                                                         temp_submission_creation_year]

            # Tells mongoDB to drop that collection within the comments DB
            comments_mongo_db_reddit.drop_collection(str(submission.id))
            print("--- Comments for " + str(submission.id) +
                  " have changed and therefore that collection has been dropped from comments DB")

        # Check various details to validate wether there is a need to recreate that collection or not
        # We are checking the ups by calculating some tolerance factor because
        # reddit scews that data
        if (
            cursor[0].get("author") != str(
                submission.author)) or (
            cursor[0].get("num_Comments") != str(
                submission.num_comments)) or (
                    cursor[0].get("selftext") != str(
                        submission.selftext)) or (
                            cursor[0].get("title") != str(
                                submission.title)) or (
                                    cursor[0].get("ups") +
                                    tolerance_factor < int(
                                        submission.ups)) or (
                                            cursor[0].get("ups") -
                                            tolerance_factor > int(
                                                submission.ups)):
            # Delete that collection so that it gets recreated again
            mongo_db_reddit.drop_collection(str(submission.id))

            print("--- Thread " + str(submission.id) + " was not up2date and therefore has been dropped")

            # Because the information in the database were old we dropped it and therefore we return False
            return False

        # Whenever the collection already exists and it is already up to date
        else:
            return True

    # Whenever the collection does not yet exist
    else:
        return False

# The mongo client, necessary to connect to mongoDB
mongo_DB_Client_Instance = None

# The Main reddit functionality
reddit_Instance = None

# Will contain the type - what we want to crawl.. threads or comments
argument_crawl_type = None

# Will contain the starting year to crawl data for in epoch time
argument_year_beginning = None

# Will contain the ending year to crawl data for in epoch time
argument_year_end = None

# <editor-fold desc="Information about this variable is inside here">
# Will contain the steps in hours to go forward in crawling process..
# 1000 threads can be crawled at one shift at maximum.. (the return limit is 1000).
# So it is useful to not set this value to high...
# i.E. if you set it to 10000 the crawler goes forward 10000 hours, but you can only receive 1000 threads due to
# reddits api restriction.. therefore you will miss other threads...
# Best value for this variable is 96
# </editor-fold>
argument_hours_to_shift = None


# Executes necessary checks
check_script_arguments()


# Initializes the mongoDB with the arguments given via command line
initialize_mongo_db_parameters()


# <editor-fold desc="Description of time_shift_difference inside here">
# 1. At first x hours are added to the epoch format of argument_year_beginning
#   1.1. At this step epoch gets converted to String
# 2. String gets converted back to epoch time
#   2.1. Due to conversion the time is in float format [1201907536.0]
# 3. Converts float to int while rounding it
#   3.1. Rounding does not the numbers in front of the comma [1201907536]
# </editor-fold>
# noinspection PyTypeChecker
time_shift_difference = int(
    round(time.mktime(
        (datetime.fromtimestamp(argument_year_beginning) +
         timedelta(
             hours=argument_hours_to_shift)
         ).timetuple()
    )
    )
)


# Executes the crawling, depending on the argument given.
crawl_data()
