# Sources used within this class:
# 1. (08.02.2016 @ 15:43) -
# https://api.mongodb.org/python/current/tutorial.html
#
# This script has been developed by using PRAW 3.3.0

from pymongo import MongoClient     # Necessary to interact with MongoDB
from datetime import datetime       # Necessary to create the year out of the thread utc
import praw                         # Necessary for praw usage
import sys                          # Necessary to use script arguments
import collections                  # Necessary to sort the dictionary before it will be written into the database


def check_script_arguments():
    """Checks if enough and correct arguments have been given to run this script adequate

    1. It checks in the first instance if enough arguments have been given
    2. Then necessary variables will be filled with appropriate values

    Args:
        -
    Returns:
        -
    """

    global argument_year_beginning, argument_year_ending, argument_inverse_crawling

    # Whenever not enough arguments were given
    if len(sys.argv) <= 2:

        print("Not enough arguments were given...")
        print("Terminating script now!")
        sys.exit()

    else:

        # Writes necessary values into the variables
        argument_year_beginning = str(sys.argv[1])

        # It is necessary to add + 1 here, otherwise it would only crawl the amount "argument_hours_to_shift" for the
        # given year and it would end after one crawl attempt..
        argument_year_ending = str(sys.argv[2])

        # Contains information about the direction of diff - crawling (forwards / backwards)
        # This is necessary if you want to fill the database much faster and want to avoid double entries by crawling.
        argument_inverse_crawling = str(sys.argv[3])


def initialize_mongo_db_parameters():
    """Instantiates all necessary variables for the correct usage of the mongoDB-Client

    Args:
        -
    Returns:
        -
    """

    global reddit_Instance
    global mongo_DB_Client_Instance
    global mongo_DB_Threads_Instance
    global mongo_DB_Thread_Collection
    global mongo_DB_Comments_Instance
    global mongo_DB_Comments_Collection

    mongo_DB_Client_Instance = MongoClient('localhost', 27017)

    mongo_DB_Threads_Instance = mongo_DB_Client_Instance['iAMA_Reddit_Threads_' + argument_year_beginning]
    mongo_DB_Thread_Collection = mongo_DB_Threads_Instance.collection_names()

    mongo_DB_Comments_Instance = mongo_DB_Client_Instance['iAMA_Reddit_Comments_' + argument_year_beginning]
    mongo_DB_Comments_Collection = mongo_DB_Comments_Instance.collection_names()

    reddit_Instance = praw.Reddit(user_agent="University_Regensburg_iAMA_Crawler_0.001")


def crawl_missing_collection_into_comments_database(name_of_missing_collection):
    """ Crawls a specific thread, which is missing in the comments database and writes the appropriate entry in the db

        The method works as follows:
        1. It checks whether that thread / collection is really missing (even when that has been done before, we check
            it again here, just to make sure that collection has not been created in the meanwhile by another crawling
            process.
        2. Now the comments will be crawled from the reddit servers with flattened hierarchy
        3. Yet the comments will be written into the appropriate comments database. The correct database will be
            deviated from the threads creation timestamp.


    Args:
        name_of_missing_collection (str) : The id of the collection which is actually missing in the comments database
    Returns:
        -
    """

    # Because crawling could take many hours / days the previously assigned variables could be old
    # and therefore values could be written twice into the database.
    # Therefore we reassign the actual collection name to double check we do not write data twice

    # The mongo client, necessary to connect to mongoDB
    temp_mongo_db_client_instance = mongo_DB_Client_Instance
    # The data base instance for the comments
    temp_mongo_db_comments_instance = temp_mongo_db_client_instance['iAMA_Reddit_Comments_' + argument_year_beginning]

    # Contains all collection names of the comments database
    temp_mongo_db_comments_collection = temp_mongo_db_comments_instance.collection_names()

    # Double checks that data so that not both crawler overwrite each other
    if name_of_missing_collection not in temp_mongo_db_comments_collection:

        # The Main reddit functionality
        reddit_instance = praw.Reddit(
            user_agent="University_Regensburg_iAMA_Crawler_0.001")
        # The thread which is to be crawled
        submission_thread = reddit_instance.get_submission(
            submission_id='' +
            name_of_missing_collection
        )

        # Replaces the objects of Type praw.MoreComments with comments (i.e.
        # iterates their tree to the end / expands all comments)
        submission_thread.replace_more_comments(limit=None, threshold=0)

        # Breaks the tree hierarchy and returns a plain straight aligned list containing all fulltext comments
        flat_comments = praw.helpers.flatten_tree(submission_thread.comments)

        # Whenever a thread does not contain a single comment -> create a null
        # entry collection inside the database
        if len(flat_comments) == 0:
            print(
                "    ----- " +
                str(name_of_missing_collection) +
                " does not contain single comment. Creation empty collection now")

            # noinspection PyTypeChecker
            data_to_write_into_db = dict({
                'author': None,
                'body': None,
                'created_utc': None,
                'name': None,
                'parent_id': None,
                'ups': None
            })

            # Sorts that dictionary alphabetically ordered
            data_to_write_into_db = collections.OrderedDict(sorted(data_to_write_into_db.items()))

            # Converts the unix utc_time into a date format and converts it to string afterwards
            temp_submission_creation_year = str(datetime.fromtimestamp(submission_thread.created_utc))
            temp_submission_creation_year = temp_submission_creation_year[:4]

            # This method says to look into the appropriate database, depending
            # on the year the thread was created
            mongo_db_reddit = mongo_DB_Client_Instance["iAMA_Reddit_Comments_" + temp_submission_creation_year]

            # Writes the crawled information into the mongoDB
            collection = mongo_db_reddit[str(submission_thread.id)]

            # Write the dictionary "data_to_write_into_db" into the mongo db right now!
            collection.insert_one(data_to_write_into_db)
            print(
                "    +++++ Finished writing " +
                str(name_of_missing_collection) +
                " into " +
                "iAMA_Reddit_Comments_" +
                temp_submission_creation_year +
                "\n")

        # Whenever there were comments / answers within that crawled thread
        else:

            # Iterates over every single comment within the thread [and write
            # it into the appropriate collection in the comments database]
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

                # Converts the unix utc_time into a date format and converts it
                # to string afterwards
                temp_submission_creation_year = str(datetime.fromtimestamp(submission_thread.created_utc))
                temp_submission_creation_year = temp_submission_creation_year[:4]

                # This method says to look into the appropriate database,
                # depending on the year the thread was created
                mongo_db_reddit = mongo_DB_Client_Instance[
                    "iAMA_Reddit_Comments_" + temp_submission_creation_year]

                # Writes the crawled information into the mongoDB
                collection = mongo_db_reddit[str(submission_thread.id)]

                # Write the dictionary "data_to_write_into_db" into the mongo db right now!
                collection.insert_one(data_to_write_into_db)

            # noinspection PyUnboundLocalVariable
            print(
                "    +++++ Finished writing " +
                str(name_of_missing_collection) +
                " into " +
                "iAMA_Reddit_Comments_" +
                temp_submission_creation_year +
                "\n")


def check_if_collection_is_missing_in_comments_database():
    """ Checks if a specific collection (thread) is missing in the appropriate comments database

        The method starts the diff checking for all collections within the threads database.
        Whenever a thread exists in the comment database but not in the threads database it will be crawled from the
        reddit servers and written into the database.

    Args:
        -
    Returns:
        -
    """

    # Crawls in the forward direction, beginning with the first collection to the last collection
    if argument_inverse_crawling == "forward":
        # Iterate over every collection within the thread database
        # noinspection PyTypeChecker
        for j in range(0, len(mongo_DB_Thread_Collection)):

            # If that iterated collection does not exist within the comments database - get that data
            # and create that collection
            if not mongo_DB_Thread_Collection[j] in mongo_DB_Comments_Collection:

                print(
                    "The following collection is missing in iAMA_Reddit_Comments_" +
                    str(argument_year_beginning) +
                    ": " + mongo_DB_Thread_Collection[j]
                )

                crawl_missing_collection_into_comments_database(str(mongo_DB_Thread_Collection[j]))

    # Crawls in the backward direction, beginning with the latest collection to the first collection
    else:

        # Iterate over every collection within the thread database
        # noinspection PyTypeChecker
        for j in range(0, len(mongo_DB_Thread_Collection)):

            # If that iterated collection does not exist within the comments
            # database - get that data and create that collection
            # noinspection PyTypeChecker
            if not mongo_DB_Thread_Collection[len(mongo_DB_Thread_Collection) - 1 - j] \
                    in mongo_DB_Comments_Collection:

                # noinspection PyTypeChecker
                print(
                    "The following collection is missing in iAMA_Reddit_Comments_" +
                    str(argument_year_beginning) +
                    ": " +
                    mongo_DB_Thread_Collection[len(mongo_DB_Thread_Collection) - 1 - j])

                # noinspection PyTypeChecker
                crawl_missing_collection_into_comments_database(str(
                    mongo_DB_Thread_Collection[len(mongo_DB_Thread_Collection) - 1 - j]))


def crawl_missing_collection_into_threads_database(name_of_missing_collection):
    """ Crawls a specific thread, which is missing in the thread database and writes the appropriate entry in the db

        The method works as follows:
        1. It checks whether that thread / collection is really missing (even when that has been done before, we check
            it again here, just to make sure that collection has not been created in the meanwhile by another crawling
            process.
        2. Now the the thread will be crawled from the reddit servers
        3. Yet the thread will be written into the appropriate threads database. The correct database will be
            deviated from the threads creation timestamp.

    Args:
        name_of_missing_collection (str) : The id of the collection which is actually missing in the comments database
    Returns:
        -
    """

    # Because crawling could take many hours /
    # days the previously assigned variables could be old and therefore values could be written twice into the database.
    # Therefore we reassign the actual collection name to double check we do
    # not write data twice

    # The mongo client, necessary to connect to mongoDB
    temp_mongo_db_client_instance = mongo_DB_Client_Instance
    # The data base instance for the threads
    temp_mongo_db_threads_instance = temp_mongo_db_client_instance['iAMA_Reddit_Threads_' + argument_year_beginning]

    # Contains all collection names of the thread database
    temp_mongo_db_thread_collection = temp_mongo_db_threads_instance.collection_names()

    # Double checks that data so that not both crawler overwrite each other
    if name_of_missing_collection not in temp_mongo_db_thread_collection:

        # The Main reddit functionality
        reddit_instance = praw.Reddit(user_agent="University_Regensburg_iAMA_Crawler_0.001")
        # The thread which is to be crawled
        submission = reddit_instance.get_submission(submission_id='' + name_of_missing_collection)

        # Because down votes are not accessable via reddit API, we have calculated it by our own here
        ratio = reddit_instance.get_submission(submission.permalink).upvote_ratio

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

        # Converts the unix utc_time into a date format and converts it to
        # string afterwards
        temp_submission_creation_year = str(datetime.fromtimestamp(submission.created_utc))
        temp_submission_creation_year = temp_submission_creation_year[:4]

        # This method says to look into the appropriate database, depending on the year the thread was created
        mongo_db_reddit = mongo_DB_Client_Instance["iAMA_Reddit_Threads_" + temp_submission_creation_year]

        # Writes the crawled information into the mongoDB
        collection = mongo_db_reddit[str(submission.id)]

        # Write the dictionary "data_to_write_into_db" into the mongo db right now!
        collection.insert_one(data_to_write_into_db)

        print(
            "    +++++ Finished writing " +
            str(name_of_missing_collection) +
            " into " +
            "iAMA_Reddit_Threads_" +
            temp_submission_creation_year +
            "\n"
        )


def check_if_collection_is_missing_in_threads_database():
    """ Checks if a specific collection (thread) is missing in the appropriate threads database

        The method starts the diff checking for all collections within the threads database.
        Whenever a thread exists in the comment database but not in the threads database it will be crawled from the
        reddit servers and written into the database.

    Args:
        -
    Returns:
        -
    """

    # Crawls in the forward direction, beginning with the first collection to the last collection
    if argument_inverse_crawling == "forward":

        # Iterate over every collection within the comments database
        # noinspection PyTypeChecker
        for j in range(0, len(mongo_DB_Comments_Collection)):

            # If that iterated collection does not exist within the thread database
            # - get that data and create that collection
            if not mongo_DB_Comments_Collection[j] in mongo_DB_Thread_Collection:
                print(
                    "The following collection is missing in iAMA_Reddit_Threads_" +
                    str(argument_year_beginning) +
                    ": " +
                    mongo_DB_Comments_Collection[j])
                crawl_missing_collection_into_threads_database(str(mongo_DB_Comments_Collection[j]))

    # Crawls in the backward direction, beginning with the latest collection to the first collection
    else:
        # Iterate over every collection within the comments database
        # noinspection PyTypeChecker
        for j in range(0, len(mongo_DB_Comments_Collection)):

            # If that iterated collection does not exist within the thread database
            # - get that data and create that collection
            # noinspection PyTypeChecker
            if not mongo_DB_Comments_Collection[
                    len(mongo_DB_Comments_Collection) - 1 - j] in mongo_DB_Thread_Collection:
                # noinspection PyTypeChecker
                print(
                    "The following collection is missing in iAMA_Reddit_Threads_" +
                    str(argument_year_beginning) +
                    ": " +
                    mongo_DB_Comments_Collection[len(mongo_DB_Comments_Collection) - 1 - j])

                # noinspection PyTypeChecker
                crawl_missing_collection_into_threads_database(str(
                    mongo_DB_Comments_Collection[len(mongo_DB_Comments_Collection) - 1 - j]))


def start_crawling_for_diffs():
    """ This method starts the crawling, with the method you have defined in your arguments

    Args:
        -
    Returns:
        -
    """

    global argument_year_beginning

    # Whenever the user wants to crawl many years at all
    while argument_year_beginning != argument_year_ending:

        # Creates missing collections within the comments database
        check_if_collection_is_missing_in_comments_database()

        # Creates missing collections within the threads database
        check_if_collection_is_missing_in_threads_database()

        # Increase the year counter by one so the data for the next year can be crawled
        argument_year_beginning = str(int(argument_year_beginning) + 1)

        # Database variables need to be refreshed because the year has changed
        initialize_mongo_db_parameters()

    # Whenever the user only wants to crawl one year
    if argument_year_beginning == argument_year_ending:

        # Database variables need to be refreshed because the year has changed
        initialize_mongo_db_parameters()

        # Creates missing collections within the comments database
        check_if_collection_is_missing_in_comments_database()

        # Creates missing collections within the threads database
        check_if_collection_is_missing_in_threads_database()

    print("Crawling for diffs has finished!")
    print("Terminating script now!")
    sys.exit()

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Methods which are to be called are here

# Executes necessary checks
check_script_arguments()

# Initializes the mongoDB with the arguments given via command line
initialize_mongo_db_parameters()


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Necessary variables and scripts are here

# The mongo client, necessary to connect to mongoDB
mongo_DB_Client_Instance = None

# The data base instance for the threads
mongo_DB_Threads_Instance = None

# Contains all collection names of the thread database
mongo_DB_Thread_Collection = None

# The data base instance for the comments
mongo_DB_Comments_Instance = None

# Contains all collection names of the comments database
mongo_DB_Comments_Collection = None

# Will contain the starting year to crawl data for in epoch time
argument_year_beginning = ""

# Will contain the ending year to crawl data for in epoch time
argument_year_ending = ""

# Will contain the information in which direction the crawler should start its work
argument_inverse_crawling = ""


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Methods which are to be called are here

# Executes necessary checks
check_script_arguments()

# Initializes the mongoDB with the arguments given via command line
initialize_mongo_db_parameters()

# Starts the crawling for diffs
start_crawling_for_diffs()
