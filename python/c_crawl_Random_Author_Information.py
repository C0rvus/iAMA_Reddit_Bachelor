# Sources used within this class:
# 1. (09.06.2016 @ 18:20) -
# http://alan-wright.com/programming/tutorial/python/2014/03/09/praw-tutorial/
# 2. (09.06.2016 @ 22:30) -
# https://m.reddit.com/r/RequestABot/comments/42lmgv/need_a_bot_that_can_pull_all_users_and_account/
# 3. (09.06.2016 @ 22:42) -
# https://github.com/alanwright/RedditBots/blob/master/scripts/UserGoneWild.py

import praw                         # Necessary to access the reddit api
import sys                          # Necessary to use script arguments
import datetime                     # Necessary to calculate differences between time values
import numpy as np                  # Necessary to calculate arithmetic means of values
import collections                  # Necessary to sort collections alphabetically
from pymongo import MongoClient     # Necessary to interact with MongoDB


def check_script_arguments():
    """Checks if enough and correct arguments have been given to run this script adequate

    1. It checks in the first instance if enough arguments have been given
    2. Then necessary variables will be filled with appropriate values

    Args:
        -
    Returns:
        -
    """

    global argument_limit_crawling_amount

    # Whenever not enough arguments were given
    if len(sys.argv) <= 1 or len(sys.argv) > 2:
        print("Not enough arguments were given...")
        print("Terminating script now!")
        sys.exit()

    else:
        # Contains information about the direction of diff - crawling (forwards / backwards)
        # This is necessary if you want to fill the database much faster and want to avoid double entries by crawling.
        argument_limit_crawling_amount = int(sys.argv[1])


def initialize_mongo_db_parameters():
    """Instantiates all necessary variables for the correct usage of the mongoDB client

    Args:
        -
    Returns:
        -
    """

    global mongo_db_client_instance
    global mongo_db_random_author_instance
    global mongo_db_random_author_collection
    global mongo_db_iama_author_instance
    global mongo_db_iama_author_collection
    global mongo_db_iama_author_collection_amount

    mongo_db_client_instance = MongoClient('localhost', 27017)
    mongo_db_random_author_instance = mongo_db_client_instance['iAMA_Reddit_Authors_Random']
    mongo_db_random_author_collection = mongo_db_random_author_instance.collection_names()
    
    mongo_db_iama_author_instance = mongo_db_client_instance['iAMA_Reddit_Authors']
    mongo_db_iama_author_collection = mongo_db_iama_author_instance.collection_names()
    mongo_db_iama_author_collection_amount = len(mongo_db_iama_author_collection)


def start_data_generation_for_analysis():
    """Starts the data processing by swichting through the years
        After every year cycle the mongo db parameters will be reinitialized

    Args:
        -
    Returns:
        -
    """

    # The counter which gets added up per iteration
    actual_counter = 0

    # As long as the iteration limit is not reached and the amount of entries within the 'random' database does not
    # exceed the amount of entries within the iama data base
    while actual_counter != argument_limit_crawling_amount and \
                    len(mongo_db_client_instance['iAMA_Reddit_Authors_Random'].collection_names()) != \
                    mongo_db_iama_author_collection_amount:

        # Defines variables per random
        rand_submission = reddit_instance.get_random_submission()
        rand_submission_subreddit = str(rand_submission.subreddit).lower()

        # Make sure, the submissions subreddit is not iAMA, because we already have that data in the original author db
        if rand_submission_subreddit != "iama":

            # Describes the randomly crawled author
            rand_submission_author = str(rand_submission.author)

            # Starts retrieving and checking necessary data
            generate_data_now(rand_submission_author)

            # Increase the actual counter by one
            actual_counter += 1

        else:
            pass


def generate_data_now(randomized_author_name):
    """Crawls author information and writes them into the mongoDB database with the name 'iAMA_Reddit_Authors_Random'

    It does this by first checking the given crawling direction. The ability to crawl bidirectional allows you to build
    up you database in a much more faster way, because you can start one instance crawling forward while the other
    instance crawls backward.

    This method works in the following way:

    1. Checks for crawling direction
    2. It checks whether an iterated collection is no "system.indexes".
    3. By iterating over all collections it checks for iAMA-Requests and skips them. Because we do not want requests
    in our dataset, because we want data of actually created iama threads

    4. Now it will be checked whether the author already exists within the database (collection name). This will be
    done by always re-initialising the collection.names() which is necessary to always have a up2date-overview!

        4.1. Whenever the author does not exist yet get the necessary information and write it into the database

        4.2. Whenever the author does already exist skip that calculation part

    Args:
        -
    Returns:
        -
    """

    print("Crawling random author data for '" + randomized_author_name + "' now...")

    # Refreshes the collection initialization for prevention of duplicate writing errors
    if (str(randomized_author_name)) in mongo_db_client_instance['iAMA_Reddit_Authors_Random'].collection_names() or \
            (str(randomized_author_name) in mongo_db_iama_author_collection):
        print("Author: " + str(randomized_author_name) + " already exists in data base.. Skipping crawling"
                                                     " this author.")

    else:
        returned_value = get_author_information(randomized_author_name)

        # Value could be none if it has i.E. no values or HTTP-Errors appeared
        if returned_value is not None:

            # Writes the crawled information into the mongoDB
            collection = mongo_db_random_author_instance[str(randomized_author_name)]

            # Write the dictionary "returned_value" into the mongo db right now!
            collection.insert_one(returned_value)

        else:
            print("Error getting user information.. It has probably been deleted...")
            pass


def calculate_time_difference(time_value_1, time_value_2):
    """Calculates the time difference between two floats in epoch style and returns seconds

    Args:
        time_value_1 (float): The first time value to be used for calculation
        time_value_2 (float): The second time value to be used for calculation
    Returns:
        time_diff_seconds (int): The amount of time difference in seconds
    """

    # Converts the the first time unit into a comparable format
    temp_time_value_1 = float(time_value_1)

    temp_time_value_1_converted_1 = datetime.datetime.fromtimestamp(
        temp_time_value_1).strftime('%d-%m-%Y %H:%M:%S')

    # Reformatation of time string
    temp_time_value_1_converted_2 = datetime.datetime.strptime(
        temp_time_value_1_converted_1, '%d-%m-%Y %H:%M:%S')

    # Converts the current time into a comparable time format
    temp_time_value_2 = float(time_value_2)

    temp_time_value_2_converted_1 = datetime.datetime.fromtimestamp(
        temp_time_value_2).strftime('%d-%m-%Y %H:%M:%S')

    # Reformatation of time string
    temp_time_value_2_converted_2 = datetime.datetime.strptime(
        temp_time_value_2_converted_1, '%d-%m-%Y %H:%M:%S')

    # Contains the amount of time units (minutes)
    time_diff_seconds = (temp_time_value_2_converted_2 - temp_time_value_1_converted_2).total_seconds()

    return time_diff_seconds


def get_author_information(name_of_author):
    """Calculates various information about the author
        Because I have created this script shortly before my evaluation everything listed here is not outsourced by
        written in a very sequential / procedural way, therefore I ask for you understanding.

        The method does the following:

        1. Referencing a reddit author object, which is necessary to get all that necessary data
        2. Declaration of necessary variables for later assignment
        3. Trial of receiving the authors birthday
            We have to try this here, because, if the account has already been deleted a http error will be thrown
            and we would have to recrawl all that data.
        4. Receival authors comment / link karma - amount
        5. Trial of receiving of all links / comments the author every made
            Because it could happen, that there is an internal error in reddit ongoing (Error 500) which will reset
            the connection and therefore we would have to recrawl all of our data
        6. Iteration of all comments / links and therefore saving the time difference (in seconds) between each created
            comment / link
        7. Calculation of time difference between acc birth & first iama in seconds
        8. Patching up a big dictionary which will be sorted (alphabetically correct)
        9. Return that dictionary

    Args:
        name_of_author (str): The name of the author which information need to be calculated
    Returns:
        dict_to_be_returned (dict): Dictionary containing various information about the author. It will be written
    """

    # Retrieves the reddit object, containing the hosts name
    reddit_thread_host = reddit_instance.get_redditor(name_of_author)

    # Amount of comments the redditor every made in total
    amount_of_comments_except_iama = 0
    amount_of_comments_iama = 0

    # Amount of threads the host created
    amount_creation_iama_threads = 0
    amount_creation_other_threads = 0

    # The timestamp in epoch utc of the first iama
    timestamp_first_iama = 0

    # Timestamps of every single link / thread created by the author
    timestamps_threads = []

    # Contains the difference in seconds between every thread created
    timestamps_threads_difference = []

    # Timestamps of every single comment created by the author
    timestamps_comments = []

    # Contains the difference in seconds between every comment created
    timestamps_comments_difference = []

    # noinspection PyBroadException
    # Because it could probably happen, that the author has been deleted in the meanwhile
    try:
        # The birthdate of the account in utc epoch time format
        author_birthday = reddit_thread_host.refresh().created_utc
    # Because there are a lot of exceptions we except anything...
    except:
        return None

    # Amount of comment karma
    author_comment_karma_amount = reddit_thread_host.refresh().comment_karma

    # Amount of link / thread karma
    author_link_karma_amount = reddit_thread_host.refresh().link_karma

    # Contains all submissions of the thread creator
    submitted = reddit_thread_host.get_submitted(limit=None)

    # Contains all comments of the thread creator
    comments = reddit_thread_host.get_comments(limit=None)

    # <editor-fold desc="Retrieves all comments per author">
    # noinspection PyBroadException
    # Because the Reddit Server often returns an 500 error, we have to try receiving comments here
    try:
        for comment in comments:

            # Checks for submission of that comment (i.e. plasticsurgerybeauty)
            name_of_subreddit_the_host_commented_to = comment.subreddit.display_name.lower()

            comment_creation_date = comment.created_utc

            timestamps_comments.append(comment_creation_date)

            # Whenever the author contributed an comment to iama
            if name_of_subreddit_the_host_commented_to == "iama":

                amount_of_comments_iama += 1

            # Whenever he did not
            else:
                amount_of_comments_except_iama += 1

    # Because there are a lot of exceptions we except anything...
    except:
        return None
    # </editor-fold>

    # <editor-fold desc="Retrieves all threads created per author">
    # noinspection PyBroadException
    # Because the reddit server often returns an 500 error, we have to try receiving links here
    try:
        for link in submitted:

            # The name of the subreddit in lowercase
            subreddit = link.subreddit.display_name.lower()

            # The creation date of the
            link_creation_date = link.created_utc

            # Appends that timestamp to a time stamp list for correct time difference calculation
            timestamps_threads.append(link_creation_date)

            if subreddit == "iama":
                amount_creation_iama_threads += 1

                # <editor-fold desc="Defines the first iAMA thread created by the author">
                # Necessary for calculating the correct time difference between acc birthday and the authors first iama
                if timestamp_first_iama == 0:
                    timestamp_first_iama = link_creation_date

                elif link_creation_date < timestamp_first_iama:
                    timestamp_first_iama = link_creation_date

                # Else is here only for optical reasons
                else:
                    pass
                # </editor-fold>

            else:
                amount_creation_other_threads += 1

    # Because there are a lot of exceptions we except anything...
    except:
        return None
    # </editor-fold>

    # To avoid lurkers we skip all authors who have created no thread at all
    if amount_creation_other_threads == 0:
        return None
    else:
        pass

    # Sort the content of the lists descending, which is necessary for correct time calculation
    timestamps_threads.sort(key=float, reverse=True)
    timestamps_comments.sort(key=float, reverse=True)

    # <editor-fold desc="Calculates all time diffs between all threads & comments in seconds">
    for i in range(0, len(timestamps_comments)):

        # Avoids index out of bounds error message
        if i != len(timestamps_comments) - 1:
            timestamps_comments_difference.append(calculate_time_difference(timestamps_comments[i + 1],
                                                                            timestamps_comments[i]))

    for i in range(0, len(timestamps_threads)):

        # Avoids index out of bounds error message
        if i != len(timestamps_threads) - 1:
            timestamps_threads_difference.append(calculate_time_difference(timestamps_threads[i + 1],
                                                                           timestamps_threads[i]))
            # </editor-fold>

    # To not run into index out of bounds message we check for the length
    if len(timestamps_threads) > 1:

        # Contains the difference in seconds between the acc birth date and the first thread created
        time_diff_acc_creation_n_first_thread = calculate_time_difference(author_birthday,
                                                                          timestamps_threads[
                                                                              len(timestamps_threads) - 1])
    else:
        time_diff_acc_creation_n_first_thread = None

    # To not run into index out of bounds message we check for the length
    if len(timestamps_comments) > 1:

        # Contains the difference in seconds between the acc birth date and the first comment created
        time_diff_acc_creation_n_first_comment = calculate_time_difference(author_birthday,
                                                                           timestamps_comments[
                                                                               len(timestamps_comments) - 1])
    else:
        time_diff_acc_creation_n_first_comment = None
    # </editor-fold>

    # <editor-fold desc="If checking to prevent incorrent mean calculation">

    # If the author created more than one thread
    if len(timestamps_threads_difference) > 1:
        thread_creation_every_x_sec = np.mean(timestamps_threads_difference)
    else:
        thread_creation_every_x_sec = None

    # If the author posted more than one comment
    if len(timestamps_comments_difference) > 1:
        comment_creation_every_x_sec = np.mean(timestamps_comments_difference)
    else:
        comment_creation_every_x_sec = None
    # </editor-fold>

    # Contains all necessary information about the author
    dict_to_be_returned = {
        "author_name": name_of_author,
        "author_birth_date": author_birthday,
        "amount_of_comments_except_iama": amount_of_comments_except_iama,
        "amount_of_comments_iama": amount_of_comments_iama,
        "amount_creation_iama_threads": amount_creation_iama_threads,
        "amount_creation_other_threads": amount_creation_other_threads,
        "time_diff_acc_creation_n_first_thread": time_diff_acc_creation_n_first_thread,
        "time_diff_acc_creation_n_first_comment": time_diff_acc_creation_n_first_comment,
        "author_comment_karma_amount": author_comment_karma_amount,
        "author_link_karma_amount": author_link_karma_amount,
        "thread_creation_every_x_sec": thread_creation_every_x_sec,
        "comment_creation_every_x_sec": comment_creation_every_x_sec,
        "time_acc_birth_first_iama_thread": calculate_time_difference(timestamp_first_iama, author_birthday)
    }

    # Sorts that dictionary so the dictionary is in alphabetically ascending order
    dict_to_be_returned = collections.OrderedDict(sorted(dict_to_be_returned.items()))

    return dict_to_be_returned


# Limits the amount of crawling
argument_limit_crawling_amount = None

# The mongo client, necessary to connect to mongoDB
mongo_db_client_instance = None

# The data base instance for all random author information
mongo_db_random_author_instance = None

# Will contain all author (random) names later on
mongo_db_random_author_collection = None

# The data base instance for all iama authors
mongo_db_iama_author_instance = None

# Will contain all authors from the iAMA-DB
mongo_db_iama_author_collection = None

# Will contain the amount of entries within the original author data base
mongo_db_iama_author_collection_amount = 0

# Instanciates the reddit instace for crawling behaviour
reddit_instance = praw.Reddit(user_agent="University_Regensburg_iAMA_Crawler_0.001")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Methods which are to be called are here

# Executes necessary checks
check_script_arguments()

# Initializes the mongoDB with the arguments given via command line
initialize_mongo_db_parameters()

# Starts the data generation process and writes csv files
start_data_generation_for_analysis()
