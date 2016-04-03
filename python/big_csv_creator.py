import collections               # Necessary to sort collections alphabetically
import copy                      # Necessary to copy value of the starting year - needed for correct csv file name
import csv                       # Necessary to write data to csv files
import datetime                  # Necessary for calculating time differences
import numpy as np               # Necessary for mean calculation
import os                        # Necessary to get the name of currently processed file
import sys                       # Necessary to use script arguments
from pymongo import MongoClient  # Necessary to make use of MongoDB


def check_script_arguments():
    """Checks if enough and correct arguments have been given to run this script adequate

    1. It checks in the first instance if enough arguments have been given
    2. Then necessary variables will be filled with appropriate values

    Args:
        -
    Returns:
        -
    """

    global argument_year_beginning, argument_year_ending, argument_calculation

    # Whenever not enough arguments were given
    if len(sys.argv) < 2:
        print("Not enough arguments were given...")
        print("Terminating script now!")
        sys.exit()
    else:
        # Writes necessary values into the variables
        argument_year_beginning = int(sys.argv[1])
        argument_year_ending = int(sys.argv[2])


def initialize_mongo_db_parameters(actually_processed_year):
    """Instantiates all necessary variables for the correct usage of the mongoDB-Client

    Args:
        actually_processed_year (int) : The year with which parameters the database should be accessed
    Returns:
        -
    """

    global mongo_DB_Client_Instance
    global mongo_DB_Threads_Instance
    global mongo_DB_Thread_Collection
    global mongo_DB_Comments_Instance

    mongo_DB_Client_Instance = MongoClient('localhost', 27017)
    mongo_DB_Threads_Instance = mongo_DB_Client_Instance['iAMA_Reddit_Threads_' + str(actually_processed_year)]
    mongo_DB_Thread_Collection = mongo_DB_Threads_Instance.collection_names()
    mongo_DB_Comments_Instance = mongo_DB_Client_Instance['iAMA_Reddit_Comments_' + str(actually_processed_year)]


def start_data_generation_for_analysis():

    while year_actually_in_progress != argument_year_ending:
        print("IM WHILE")
    if year_actually_in_progress == argument_year_ending:
        print("EQUAL")


def start_data_generation():

    print("Generating data for year " + str(year_actually_in_progress) + " now...")

    # noinspection PyTypeChecker
    for j, val in enumerate(mongo_DB_Thread_Collection):

        # Skips the system.indexes-table which is automatically created by  mongodb itself
        if not val == "system.indexes":
            # References the actual iterated thread
            temp_thread = mongo_DB_Threads_Instance[val]

            # Gets the creation date of that iterated thread
            temp_thread_creation_time = temp_thread.find()[0].get("created_utc")

            # Gets the title of that iterated thread
            temp_thread_title = temp_thread.find()[0].get("title")

            temp_thread_downs = temp_thread.find()[0].get("downs")
            temp_thread_ups = temp_thread.find()[0].get("ups")
            temp_thread_author = temp_thread.find()[0].get("author")
            temp_thread_num_comments_skewed = temp_thread.find()[0].get("num_Comments")

            # Removes iAMA-Requests out of our selection
            if "request" in temp_thread_title.lower() \
                    and "as requested" not in temp_thread_title.lower() \
                    and "by request" not in temp_thread_title.lower() \
                    and "per request" not in temp_thread_title.lower() \
                    and "request response" not in temp_thread_title.lower():
                # Continue skips processing of those elements which are requests here
                continue

            # Will contain information about time calculation methods
            returned_dict = process_specific_thread(val, temp_thread_creation_time, temp_thread_author)


            dict_to_append_to_global_list = {
                'Year': year_actually_in_progress,

                'Thread_id': str(val),
                'Thread_author': temp_thread_author,
                'Thread_ups': temp_thread_ups,
                'Thread_downs': temp_thread_downs,
                'Thread_creation_time_stamp': temp_thread_creation_time,

                'Thread_num_comments_total_skewed': temp_thread_num_comments_skewed,
                'Thread_num_comments_total': 0,
                'Thread_num_comments_total_tier_1': 0,
                'Thread_num_comments_total_tier_x': 0,

                'Thread_num_questions_total_total': 0,
                'Thread_num_questions_total_tier_1': 0,
                'Thread_num_questions_total_tier_x': 0,

                'Thread_num_questions_answered_by_iama_host_total': 0,
                'Thread_num_questions_answered_by_iama_host_tier_1': 0,
                'Thread_num_questions_answered_by_iama_host_tier_x': 0,

                'Thread_num_comments_answered_by_iama_host_total': 0,
                'Thread_num_comments_answered_by_iama_host_tier_1': 0,
                'Thread_num_comments_answered_by_iama_host_tier_x': 0,

                'Thread_average_reaction_time_between_comments_total': 0,
                'Thread_average_reaction_time_between_comments_tier_1': 0,
                'Thread_average_reaction_time_between_comments_tier_x': 0,

                'Thread_average_reaction_time_between_questions_total': 0,
                'Thread_average_reaction_time_between_questions_tier_1': 0,
                'Thread_average_reaction_time_between_questions_tier_x': 0,

                'Thread_average_iama_host_response_to_question_time_total': 0,
                'Thread_average_iama_host_response_to_question_time_tier_1': 0,
                'Thread_average_iama_host_response_to_question_time_tier_x': 0,

                'Thread_life_span_question': 0,
                'Thread_life_span_comment': 0,

                'Thread_average_comment_vote_score_total': 0,
                'Thread_average_comment_vote_score_tier_1': 0,
                'Thread_average_comment_vote_score_tier_x': 0,

                'Thread_average_question_vote_score_total': 0,
                'Thread_average_question_vote_score_tier_1': 0,
                'Thread_average_question_vote_score_tier_x': 0,
            }


def process_specific_thread(thread_id, thread_creation_time_stamp, thread_author):
    # Makes the global comments instance locally available here
    global mongo_DB_Comments_Instance

    comments_collection = mongo_DB_Comments_Instance[thread_id]
    comments_cursor = comments_collection.find()

    # Comments and questions are seperated from another !!

    comment_total_vote_average = []
    comment_tier_1_vote_average = []
    comment_tier_x_vote_average = []

    question_total_vote_average = []
    question_tier_1_vote_average = []
    question_tier_x_vote_average = []

    comments_total = 0
    comments_tier_1 = 0
    comments_tier_x = 0

    questions_total = 0
    questions_tier_1 = 0
    questions_tier_x = 0

    questions_answered_by_iama_host_total = 0
    questions_answered_by_iama_host_tier_1 = 0
    questions_answered_by_iama_host_tier_x = 0

    comments_answered_by_iama_host_total = 0
    comments_answered_by_iama_host_tier_1 = 0
    comments_answered_by_iama_host_tier_x = 0

    time_value_of_last_comment = 0
    time_value_of_last_question = 0

    # iterates over every comment
    for collection in comments_cursor:

        # Whenever the iterated comment was created by user "AutoModerator" skip it
        if (collection.get("author")) != "AutoModerator":

            comment_text = collection.get("body")
            comment_author = collection.get("author")
            comment_parent_id = collection.get("parent_id")
            comment_actual_id = collection.get("name")
            comment_creation_time = collection.get("created_utc")

            if comment_text is not None and comment_author is not None and comment_parent_id is not None:

                bool_comment_is_question = check_if_comment_is_a_question(comment_text)

                bool_comment_is_question_on_tier_1 = check_if_comment_is_on_tier_1(comment_parent_id)

                bool_comment_is_not_from_thread_author = check_if_comment_is_not_from_thread_author(
                    thread_author, comment_author)

                # Whenever the iterated "reaction" is a question
                if bool_comment_is_question is True:
                    questions_total += 1
                    question_total_vote_average.append(collection.get("ups"))

                    if comment_creation_time > time_value_of_last_question:
                        time_value_of_last_question = comment_creation_time

                    # Check whether that iterated comment is answered by the host
                    answer_is_from_thread_author = check_if_comment_is_answer_from_thread_author(
                        thread_author, comment_actual_id, comments_cursor)

                    if answer_is_from_thread_author["question_Answered_From_Host"] is True:
                        questions_answered_by_iama_host_total += 1

                    if bool_comment_is_question_on_tier_1 is True:
                        questions_tier_1 += 1
                        question_tier_1_vote_average.append(collection.get("ups"))

                        if answer_is_from_thread_author["question_Answered_From_Host"] is True:
                            questions_answered_by_iama_host_tier_1 += 1

                    else:
                        questions_tier_x += 1
                        question_tier_x_vote_average.append(collection.get("ups"))

                        if answer_is_from_thread_author["question_Answered_From_Host"] is True:
                            questions_answered_by_iama_host_tier_x += 1

                # Whenever the iterated "reaction" is just a comment and no question
                else:
                    comments_total += 1
                    comment_total_vote_average.append(collection.get("ups"))

                    if comment_creation_time > time_value_of_last_comment:
                        time_value_of_last_comment = comment_creation_time

                    if answer_is_from_thread_author["question_Answered_From_Host"] is True:
                        comments_answered_by_iama_host_total += 1

                    if bool_comment_is_question_on_tier_1 is True:
                        comments_tier_1 += 1
                        comment_tier_1_vote_average.append(collection.get("ups"))

                        if answer_is_from_thread_author["question_Answered_From_Host"] is True:
                            comments_answered_by_iama_host_tier_1 += 1

                    else:
                        comments_tier_x += 1
                        comment_tier_x_vote_average.append(collection.get("ups"))

                        if answer_is_from_thread_author["question_Answered_From_Host"] is True:
                            comments_answered_by_iama_host_tier_x += 1





def check_if_comment_is_a_question(given_string):
    """Simply checks whether a given string is a question or not

    1. This method simply checks wether a question mark exists within that string or not..
        This is just that simple because messing around with natural processing kits to determine the semantic sense
        would blow up my bachelor work...

    Args:
        given_string (int) : The string which will be checked for a question mark
    Returns:
        True (bool): Whenever the given string is a question
        False (bool): Whenever the given string is not a question

    """

    if "?" in given_string:
        return True
    else:
        return False


def check_if_comment_is_on_tier_1(comment_parent_id):
    """Checks whether a comment relies on the first tier or any other tier

    Args:
        comment_parent_id (str) : The name id of the comments parent
    Returns:
        True (bool): Whenever the comment lies on tier 1
        False (bool): Whenever the comment lies on any other tier
    """

    if "t3_" in comment_parent_id:
        return True
    else:
        return False


def check_if_comment_is_not_from_thread_author(author_of_thread, comment_author):
    """Checks whether both strings are equal or not

    1. This method simply checks wether both strings match each other or not.
        I have built this extra method to have a better overview in the main code..

    Args:
        author_of_thread (str) : The name of the thread author (iAMA-Host)
        comment_author (str) : The name of the comments author
    Returns:
        True (bool): Whenever the strings do not match
        False (bool): Whenever the strings do match
         answered that given question)
    """
    if author_of_thread != comment_author:
        return True
    else:
        return False


def check_if_comment_is_answer_from_thread_author(author_of_thread, comment_actual_id, comments_cursor):
    """Checks whether both strings are equal or not

    1. A dictionary containing flags whether that a question is answered by the host with the appropriate timestamp will
        be created in the beginning.
    2. Then the method iterates over every comment within that thread
        1.1. Whenever an answer is from the iAMA hosts and the processed comments 'parent_id' matches the iAMA hosts
            comments (answers) id, the returned dict will contain appropriate values and will be returned
        1.2. If this is not the case, it will be returned in its default condition

    Args:
        author_of_thread (str) : The name of the thread author (iAMA-Host)
        comment_actual_id (str) : The id of the actually processed comment
        comments_cursor (Cursor) : The cursor which shows to the amount of comments which can be iterated
    Returns:
        True (bool): Whenever the strings do not match
        False (bool): Whenever the strings do match
         answered that given question)
    """
    dict_to_be_returned = {
        "question_Answered_From_Host": False,
        "time_Stamp_Answer": 0
    }

    # Iterates over every comment
    for collection in comments_cursor:

        # Whenever the iterated comment was created by user "AutoModerator"
        # skip it
        if (collection.get("author")) != "AutoModerator":
            check_comment_parent_id = collection.get("parent_id")
            actual_comment_author = collection.get("author")

            # Whenever the iterated comment is from the iAMA-Host and that
            # comment has the question as parent_id
            if (check_if_comment_is_not_from_thread_author(author_of_thread, actual_comment_author) == False) and \
                    (check_comment_parent_id == comment_actual_id):

                dict_to_be_returned["question_Answered_From_Host"] = True
                dict_to_be_returned["time_Stamp_Answer"] = collection.get("created_utc")

                return dict_to_be_returned
            else:
                return dict_to_be_returned
        else:
            return dict_to_be_returned

    # This is the case whenever a comment has not a single thread
    return dict_to_be_returned





# Contains the year which is given as an argument
argument_year_beginning = 0

# Contains information what data you want to be calculated
argument_calculation = ""

# Contains the year which is given as an argument
argument_year_ending = 0

# Contains the year which will be processed at the moment
year_actually_in_progress = 0

