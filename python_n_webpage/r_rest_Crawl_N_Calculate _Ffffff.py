# Sources used within this class:
# 1. (09.06.2016 @ 18:20) -
# http://alan-wright.com/programming/tutorial/python/2014/03/09/praw-tutorial/
# 2. (09.06.2016 @ 22:30) -
# https://m.reddit.com/r/RequestABot/comments/42lmgv/need_a_bot_that_can_pull_all_users_and_account/
# 3. (09.06.2016 @ 22:42) - https://github.com/alanwright/RedditBots/blob/master/scripts/UserGoneWild.py

import praw                         # Necessary to access the reddit api
import sys                          # Necessary to use script arguments
import csv                          # Necessary to write data to csv files
import copy                         # Necessary to copy value of the starting year - needed for correct csv file name
import datetime                     # Necessary to calculate differences between time values
import numpy as np                  # Necessary to calculate arithmetic means of values
import collections                  # Necessary to sort collections alphabetically
import os                           # Necessary to get the name of currently processed file
from pymongo import MongoClient     # Necessary to interact with MongoDB


# TODO: 3. Den Wert korrekt in eine CSV reinschreiben (siehe bisherige Scripte)
# TODO: 4. Korrekt kommentieren und Datei sauber anpassen
# TODO: 5. Dieses Script analog den anderen Crawlern aufbauen und in der Readme.MD hinterlegen
# TODO: 6. Diese Sachen alle auswerten in dem dicken Analyzer Script
# TODO: Ne globale Liste erstellen, in der dann gefragt wird, ob der Author denn da schon drinnen is..
# Diese Liste wird während der Iteration abgefragt und wenn einer drinnen is, wird der aktuelle Thread geskippt


def check_script_arguments():
    """Checks if enough and correct arguments have been given to run this script adequate

    1. It checks in the first instance if enough arguments have been given
    2. Then necessary variables will be filled with appropriate values

    Args:
        -
    Returns:
        -
    """

    global argument_year_beginning, argument_year_ending

    # Whenever not enough arguments were given
    if len(sys.argv) <= 1 or len(sys.argv) > 2:
        print("Not enough arguments were given...")
        print("Terminating script now!")
        sys.exit()

    else:
        # Parses the first two arguments to the appropriate variables
        argument_year_beginning = int(sys.argv[1])
        argument_year_ending = int(sys.argv[2])


def initialize_mongo_db_parameters():
    """Instantiates all necessary variables for the correct usage of the mongoDB client

    Args:
        -
    Returns:
        -
    """

    global mongo_db_client_instance
    global mongo_db_author_random_instance
    global mongo_db_author_random_collection

    mongo_db_client_instance = MongoClient('localhost', 27017)
    mongo_db_author_random_instance = mongo_db_client_instance['iAMA_Reddit_Authors_Random']
    mongo_db_author_random_collection = mongo_db_author_random_instance.collection_names()


def start_data_generation_for_analysis():
    """Starts the data processing by swichting through the years

    Args:
        -
    Returns:
        -
    """

    global argument_year_beginning, year_actually_in_progress, author_information_list

    # Copies the value of the beginning year, because it will be changed due to moving forward within the years
    year_actually_in_progress = copy.copy(argument_year_beginning)

    # As long as the ending year has not been reached
    while year_actually_in_progress != argument_year_ending:

        # Starts retrieving and checking necessary data
        generate_data_now()

        # Writes a csv file for the actually processed year
        # write_csv(author_information_list)

        # Empty that list
        # author_information_list = []

        # Progresses in the year, necessary for onward year calculation
        year_actually_in_progress += 1

        # Reinitializes the mongodb with new year parameter here
        # noinspection PyTypeChecker
        initialize_mongo_db_parameters(year_actually_in_progress)

    # Will be entered whenever the last year is beeing processed
    if year_actually_in_progress == argument_year_ending:

        # Starts retrieving and checking necessary data
        generate_data_now()

    # Writes a csv file with information for all years
    # write_csv(global_year_author_information_list)


def generate_data_now():

    print("Generating data for year " + str(year_actually_in_progress) + " now...")
    # noinspection PyTypeChecker
    for j, val in enumerate(mongo_db_author_random_collection):

        print(str(j), "/", len(mongo_db_author_random_collection))

        # Skips the system.indexes-table which is automatically created by mongodb itself
        if not val == "system.indexes":

            # References the actual iterated thread
            temp_thread = mongo_db_author_random_collection[val]

            # Gets the authors name of the iterated thread
            temp_thread_author = temp_thread.find()[0].get("author")

            # Gets the title of that iterated thread
            temp_thread_title = temp_thread.find()[0].get("title")

            # removes iAMA-Requests out of our selection
            if "request" in temp_thread_title.lower() \
                    and "as requested" not in temp_thread_title.lower() \
                    and "by request" not in temp_thread_title.lower() \
                    and "per request" not in temp_thread_title.lower() \
                    and "request response" not in temp_thread_title.lower():
                continue


            # Whenever the author has not appeared yet (he did not create a iama a second, x.. time)
            if temp_thread_author not in global_author_check_list:

                global_author_check_list.append(temp_thread_author)
                returned_value = get_author_information(temp_thread_author)

                # Writes the crawled information into the mongoDB
                collection = mongo_db_author_random_instance[str(temp_thread_author)]

                # Write the dictionary "data_to_write_into_db" into the mongo db right now!
                collection.insert_one(returned_value)


                # Value could be none if it has i.E. no values
                if returned_value is not None:
                    author_information_list.append(returned_value)
                    global_year_author_information_list.append(returned_value)

                else:
                    pass

            # If the author already exists within that check list then skip processing that thread
            else:
                continue


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

    reddit_thread_host = reddit_instance.get_redditor(name_of_author)

    # Amount of comments the redditor every made in total
    amount_of_comments_except_iama = 0
    amount_of_comments_iama = 0

    # Amount of threads the host created
    amount_creation_iama_threads = 0
    amount_creation_other_threads = 0

    # Timestamps of every single link / thread created by the author
    timestamps_threads = []

    # Contains the difference in seconds between every thread created
    timestamps_threads_difference = []

    # Timestamps of every single comment created by the author
    timestamps_comments = []

    # Contains the difference in seconds between every comment created
    timestamps_comments_difference = []

    # The birthdate of the account in utc epoch time format
    author_birtday = reddit_thread_host.refresh().created_utc

    # Amount of comment karma
    author_comment_karma_amount = reddit_thread_host.refresh().comment_karma

    # Amount of link / thread karma
    author_link_karma_amount = reddit_thread_host.refresh().link_karma

    # Contains all submissions of the thread creator
    submitted = reddit_thread_host.get_submitted(limit=None)

    # Contains all comments of the thread creator
    comments = reddit_thread_host.get_comments(limit=None)

    # <editor-fold desc="Retrieves all comments per author">
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
    # </editor-fold>

    # <editor-fold desc="Retrieves all threads created per author">
    for link in submitted:

        subreddit = link.subreddit.display_name.lower()
        link_creation_date = link.created_utc

        timestamps_threads.append(link_creation_date)

        if subreddit == "iama":
            amount_creation_iama_threads += 1
        else:
            amount_creation_other_threads += 1
    # </editor-fold>

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

    # Contains the difference in seconds between the acc birth date and the first thread created
    time_diff_acc_creation_n_first_thread = calculate_time_difference(author_birtday,
                                                                      timestamps_threads[
                                                                          len(timestamps_threads) - 1])

    # Contains the difference in seconds between the acc birth date and the first comment created
    time_diff_acc_creation_n_first_comment = calculate_time_difference(author_birtday,
                                                                       timestamps_comments[
                                                                           len(timestamps_comments) - 1])
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
        "author_birth_date": author_birtday,
        "amount_of_comments_except_iama": amount_of_comments_except_iama,
        "amount_of_comments_iama": amount_of_comments_iama,
        "amount_creation_iama_threads": amount_creation_iama_threads,
        "amount_creation_other_threads": amount_creation_other_threads,
        "time_diff_acc_creation_n_first_thread": time_diff_acc_creation_n_first_thread,
        "time_diff_acc_creation_n_first_comment": time_diff_acc_creation_n_first_comment,
        "author_comment_karma_amount": author_comment_karma_amount,
        "author_link_karma_amount": author_link_karma_amount,
        "thread_creation_every_x_sec": thread_creation_every_x_sec,
        "comment_creation_every_x_sec": comment_creation_every_x_sec
    }

    # Sorts that dictionary so the dictionary structure is standardized
    dict_to_be_returned = collections.OrderedDict(sorted(dict_to_be_returned.items()))

    print(dict_to_be_returned)

    return dict_to_be_returned


def write_csv(list_with_information):
    """Creates a c

    Args:
        list_with_information (list) : Contains information about questions for the current year
    Returns:
        -
    """

    print("---- Writing csv containing all author information for year " + str(year_actually_in_progress) + " now")
    # Empty print line here for a more beautiful console output
    print("")

    file_name_csv = str(os.path.basename(__file__))[0:len(os.path.basename(__file__)) - 3] + \
                    '_' + \
                    str(argument_year_beginning) + \
                    '_until_' + \
                    str(argument_year_ending) + \
                    '_' + \
                    str(year_actually_in_progress) + \
                    '.csv'

    # The csv writer gets referenced here
    with open(file_name_csv, 'w', newline='') as fp:
        csv_writer = csv.writer(fp, delimiter=',')

        # The heading of the csv file..
        data = [['Year',
                 'Author name',
                 'Author birthdate utc epoch',
                 'Author comment karma',
                 'Author link karma',
                 'Amount comments wo iama',
                 'Amount comments iama',
                 'Amount created threads wo iama',
                 'Amount created threads iama',
                 'Time diff acc creation n first thread',
                 'Time diff acc creation n first comment',
                 'Thread creation every x sec',
                 'Comment creation every x sec']]

        # Iterates over that generated sorted and counts the amount of questions which have not been answered
        for item in list_with_information:
            temp_list = [str(item.get("author_name")),
                         str(item.get("author_birth_date")),
                         str(item.get("amount_of_comments_except_iama")),
                         str(item.get("amount_of_comments_iama")),
                         str(item.get("amount_creation_iama_threads")),
                         str(item.get("amount_creation_other_threads")),
                         str(item.get("time_diff_acc_creation_n_first_thread")),
                         str(item.get("time_diff_acc_creation_n_first_comment")),
                         str(item.get("author_comment_karma_amount")),
                         str(item.get("author_link_karma_amount")),
                         str(item.get("thread_creation_every_x_sec")),
                         str(item.get("comment_creation_every_x_sec"))]
            data.append(temp_list)

        # Writes data into the csv file
        csv_writer.writerows(data)

# Contains the author which is to be crawled into the database
argument_author_to_be_crawled = None

# Contains the year which is given as an argument
argument_year_beginning = 0

# Contains the year which will be processed at the moment
year_actually_in_progress = 0

# Contains the year which is given as argument
argument_year_ending = 0

# The mongo client, necessary to connect to mongoDB
mongo_db_client_instance = None

# The data base instance for all author information
mongo_db_author_random_instance = None

# Instanciates the reddit instace for crawling behaviour
reddit_instance = praw.Reddit(user_agent="University_Regensburg_iAMA_Crawler_0.001")

# Will contain information about all authors for a given year
author_information_list = []

# Will contain information about every author for all years given the calculation
global_year_author_information_list = []

# This list contains only the author name of every iterated thread.. necessary to prevent duplicate names in csv later
global_author_check_list = []

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Methods which are to be called are here

# Executes necessary checks
check_script_arguments()

# Initializes the mongoDB with the arguments given via command line
initialize_mongo_db_parameters(argument_year_beginning)

# Starts the data generation process and writes csv files
start_data_generation_for_analysis()
