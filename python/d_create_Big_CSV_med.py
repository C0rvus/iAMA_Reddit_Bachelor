# Sources used within this class:
# 1. (26.03.2016 @ 15:40) -
# https://stackoverflow.com/questions/14693646/writing-to-csv-file-python
# 2. (26.03.2016 @ 18:03) -
# https://stackoverflow.com/questions/12400256/python-converting-epoch-time-into-the-datetime
# 3. (26.03.2016 @ 18:43) -
# http://effbot.org/pyfaq/how-do-i-copy-an-object-in-python.htm
# 4. (01.04.2016 @ 15:45) -
# http://stackoverflow.com/questions/7301110/why-does-return-list-sort-return-none-not-the-list

import copy                      # Necessary to copy value of the starting year - needed for correct csv file name
import csv                       # Necessary to write data to csv files
import datetime                  # Necessary for calculating time differences
import numpy as np               # Necessary for calculating the arithmetic median of values
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

    global argument_year_beginning, argument_year_ending

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
    """Starts the whole combination of generating data, checking data and writing them into csv files

    1. Triggers the data generation process and moves forward within the years -
        by moving through the years a csv file will be created for every year

    Args:
        -
    Returns:
        -
    """

    global year_actually_in_progress

    # Copies the value of the beginning year, because it will be changed due to moving forward within the years
    year_actually_in_progress = copy.copy(argument_year_beginning)

    while year_actually_in_progress != argument_year_ending:
        generate_data()
        add_actual_year_list_to_global_list(list_current_year)
        write_csv_data(list_current_year)
        year_actually_in_progress += 1

        # Reinitializes the mongodb with new year parameter here
        # noinspection PyTypeChecker
        initialize_mongo_db_parameters(year_actually_in_progress)

    if year_actually_in_progress == argument_year_ending:
        generate_data()
        add_actual_year_list_to_global_list(list_current_year)
        write_csv_data(list_current_year)

        # Value setting is necessary for correct file writing
        year_actually_in_progress = "ALL"

    # Writes a csv file containing information for all years..
    # This is very useful, so we do not have to merge all those .csv-files by hand
    write_csv_data(list_global_year)


def generate_data():
    """Starts calculating various information about thread and iama behaviour related to the year which is currently
        being processed

    After the caluclations have every iteration the results will ber appended to a list, which will contain all that
        information for the current year... That list will be writtend to csv and appended to a global list in other
        methods

    Args:
        -
    Returns:
        -
    """

    global list_current_year

    # Empty that list for correct processing
    list_current_year = []

    print("Generating data for year " + str(year_actually_in_progress) + " now...")

    # noinspection PyTypeChecker
    for j, val in enumerate(mongo_DB_Thread_Collection):

        # Skips the system.indexes-table which is automatically created by  mongodb itself
        if not val == "system.indexes":

            # Temporary value assignments for better code understanding
            temp_thread = mongo_DB_Threads_Instance[val]
            temp_thread_creation_time = temp_thread.find()[0].get("created_utc")
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

            # Will contain information different thread calculations
            values_for_analysis = process_specific_thread(val, temp_thread_creation_time, temp_thread_author)

            # Whenever the thread calculation is not None
            # It is only None whenever only 1 (from "AutoModerator") or 0 comments / reactions have been postedd
            if values_for_analysis is not None:

                dict_to_append = {
                    'Year': year_actually_in_progress,
                    'Thread_id': str(val),
                    'Thread_author': temp_thread_author,
                    'Thread_ups': temp_thread_ups,
                    'Thread_downs': temp_thread_downs,
                    'Thread_creation_time_stamp': temp_thread_creation_time,

                    'Thread_average_comment_vote_score_total': values_for_analysis["comment_total_vote_average"],
                    'Thread_average_comment_vote_score_tier_1': values_for_analysis["comment_tier_1_vote_average"],
                    'Thread_average_comment_vote_score_tier_x': values_for_analysis["comment_tier_x_vote_average"],

                    'Thread_average_question_vote_score_total': values_for_analysis["question_total_vote_average"],
                    'Thread_average_question_vote_score_tier_1': values_for_analysis["question_tier_1_vote_average"],
                    'Thread_average_question_vote_score_tier_x': values_for_analysis["question_tier_x_vote_average"],


                    'Thread_num_comments_total_skewed': temp_thread_num_comments_skewed,
                    'Thread_num_comments_total': values_for_analysis["comments_total"],
                    'Thread_num_comments_tier_1': values_for_analysis["comments_tier_1"],
                    'Thread_num_comments_tier_x': values_for_analysis["comments_tier_x"],

                    'Thread_num_questions_total': values_for_analysis["questions_total"],
                    'Thread_num_questions_tier_1': values_for_analysis["questions_tier_1"],
                    'Thread_num_questions_tier_x': values_for_analysis["questions_tier_x"],


                    'Thread_num_questions_answered_by_iama_host_total':
                        values_for_analysis["questions_answered_by_iama_host_total"],

                    'Thread_num_questions_answered_by_iama_host_tier_1':
                        values_for_analysis["questions_answered_by_iama_host_tier_1"],

                    'Thread_num_questions_answered_by_iama_host_tier_x':
                        values_for_analysis["questions_answered_by_iama_host_tier_x"],


                    'Thread_num_comments_answered_by_iama_host_total':
                        values_for_analysis["comments_answered_by_iama_host_total"],

                    'Thread_num_comments_answered_by_iama_host_tier_1':
                        values_for_analysis["comments_answered_by_iama_host_tier_1"],

                    'Thread_num_comments_answered_by_iama_host_tier_x':
                        values_for_analysis["comments_answered_by_iama_host_tier_x"],


                    'Thread_average_reaction_time_between_comments_total':
                        values_for_analysis["reaction_time_between_comments_total_average"],

                    'Thread_average_reaction_time_between_comments_tier_1':
                        values_for_analysis["reaction_time_between_comments_tier_1_average"],

                    'Thread_average_reaction_time_between_comments_tier_x':
                        values_for_analysis["reaction_time_between_comments_tier_x_average"],


                    'Thread_average_reaction_time_between_questions_total':
                        values_for_analysis["reaction_time_between_questions_total_average"],

                    'Thread_average_reaction_time_between_questions_tier_1':
                        values_for_analysis["reaction_time_between_questions_tier_1_average"],

                    'Thread_average_reaction_time_between_questions_tier_x':
                        values_for_analysis["reaction_time_between_questions_tier_x_average"],


                    'Thread_average_iama_host_response_to_question_time_total':
                        values_for_analysis["iama_host_response_to_question_time_total_average"],

                    'Thread_average_iama_host_response_to_question_time_tier_1':
                        values_for_analysis["iama_host_response_to_question_time_tier_1_average"],

                    'Thread_average_iama_host_response_to_question_time_tier_x':
                        values_for_analysis["iama_host_response_to_question_time_tier_x_average"],


                    'Thread_average_iama_host_response_to_comment_time_total':
                        values_for_analysis["iama_host_response_to_comment_time_total_average"],

                    'Thread_average_iama_host_response_to_comment_time_tier_1':
                        values_for_analysis["iama_host_response_to_comment_time_tier_1_average"],

                    'Thread_average_iama_host_response_to_comment_time_tier_x':
                        values_for_analysis["iama_host_response_to_comment_time_tier_x_average"],


                    'Thread_life_span_question': values_for_analysis["time_value_of_last_question"],
                    'Thread_life_span_comment': values_for_analysis["time_value_of_last_comment"],

                    'Thread_amount_of_questioners_total': values_for_analysis["amount_of_questioners_total"],
                    'Thread_amount_of_questioners_tier_1': values_for_analysis["amount_of_questioners_tier_1"],
                    'Thread_amount_of_questioners_tier_x': values_for_analysis["amount_of_questioners_tier_x"],

                    'Thread_amount_of_commentators_total': values_for_analysis["amount_of_commentators_total"],
                    'Thread_amount_of_commentators_tier_1': values_for_analysis["amount_of_commentators_tier_1"],
                    'Thread_amount_of_commentators_tier_x': values_for_analysis["amount_of_commentators_tier_x"]

                }

                list_current_year.append(dict_to_append)


def process_specific_thread(thread_id, thread_creation_time_stamp, thread_author):
    """Does the needed operations, for gaining information / knowledge about threads on the given thread id

    After the caluclations have every iteration the results will ber appended to a list, which will contain all that
        information for the current year... That list will be writtend to csv and appended to a global list in other
        methods

    Args:
        thread_id (str) : The id, needed for operating (i.E. comparison of parent - child relation)
        thread_creation_time_stamp (int) : Creation time stamp of thread, needed for time difference calculation
        thread_author (str): The name of the threads author, needed for answer checking of a post
    Returns:
        -
    """

    # Makes the global comments instance locally available here
    global mongo_DB_Comments_Instance

    comments_collection = mongo_DB_Comments_Instance[thread_id]

    # Generating a list out of the cursor is absolutely necessary, because the cursor can be exhausted..
    # During the calculations we have to do many iterations on a thread, but by using only one cursor for many
    # iterations I will be depleted very fast...
    # To not always generate a new cursor for each iteration this is a way more performant way to do the stuff
    comments_cursor = list(comments_collection.find())

    # Comments and questions are seperated from another !!

    dict_with_values_to_be_returned = {
        "comment_total_vote_average": [],
        "comment_tier_1_vote_average": [],
        "comment_tier_x_vote_average": [],

        "question_total_vote_average": [],
        "question_tier_1_vote_average": [],
        "question_tier_x_vote_average": [],

        "reaction_time_between_comments_total_average": [],
        "reaction_time_between_comments_tier_1_average": [],
        "reaction_time_between_comments_tier_x_average": [],

        "reaction_time_between_questions_total_average": [],
        "reaction_time_between_questions_tier_1_average": [],
        "reaction_time_between_questions_tier_x_average": [],

        "iama_host_response_to_comment_time_total_average": [],
        "iama_host_response_to_comment_time_tier_1_average": [],
        "iama_host_response_to_comment_time_tier_x_average": [],

        "iama_host_response_to_question_time_total_average": [],
        "iama_host_response_to_question_time_tier_1_average": [],
        "iama_host_response_to_question_time_tier_x_average": [],

        # Comments from the iama host are excluded
        "comments_total": 0,
        "comments_tier_1": 0,
        "comments_tier_x": 0,

        # Questions from the iama host are excluded
        "questions_total": 0,
        "questions_tier_1": 0,
        "questions_tier_x": 0,

        "questions_answered_by_iama_host_total": 0,
        "questions_answered_by_iama_host_tier_1": 0,
        "questions_answered_by_iama_host_tier_x": 0,

        "comments_answered_by_iama_host_total": 0,
        "comments_answered_by_iama_host_tier_1": 0,
        "comments_answered_by_iama_host_tier_x": 0,

        "time_value_of_last_comment": 0,
        "time_value_of_last_question": 0,

        # Questioners do not include the iama host itself
        "amount_of_questioners_total": 0,
        "amount_of_questioners_tier_1": [],
        "amount_of_questioners_tier_x": [],

        # Commentators do not include the iama host itself
        "amount_of_commentators_total": 0,
        "amount_of_commentators_tier_1": [],
        "amount_of_commentators_tier_x": []
    }

    # Every comment
    for i, val in enumerate(comments_cursor):

        # Whenever the iterated comment was created by user "AutoModerator" skip it
        if val.get("author") != "AutoModerator":

            comment_text = val.get("body")
            comment_author = val.get("author")
            comment_parent_id = val.get("parent_id")
            comment_actual_id = val.get("name")

            # Check whether that iterated comment is answered by the host
            comment_has_been_answered_by_thread_author = check_if_comment_has_been_answered_by_thread_author(
                thread_author, comment_actual_id, comments_cursor)

            if comment_text is not None and comment_author is not None and comment_parent_id is not None:

                comment_creation_time = float(val.get("created_utc"))

                bool_comment_is_question = check_if_comment_is_a_question(comment_text)

                bool_comment_is_on_tier_1 = check_if_comment_is_on_tier_1(comment_parent_id)

                bool_comment_is_not_from_thread_author = check_if_comment_is_not_from_thread_author(
                    thread_author, comment_author)

                # Whenever the iterated "reaction" is a question
                if bool_comment_is_question is True and bool_comment_is_not_from_thread_author is True:
                    dict_with_values_to_be_returned["questions_total"] += 1
                    dict_with_values_to_be_returned["question_total_vote_average"].append(val.get("ups"))
                    dict_with_values_to_be_returned["reaction_time_between_questions_total_average"]. \
                        append(comment_creation_time)

                    if comment_creation_time > dict_with_values_to_be_returned["time_value_of_last_question"]:
                        dict_with_values_to_be_returned["time_value_of_last_question"] = comment_creation_time

                    else:
                        pass

                    if comment_has_been_answered_by_thread_author["question_Answered_From_Host"] is True:
                        dict_with_values_to_be_returned["questions_answered_by_iama_host_total"] += 1

                        answer_time_stamp_iama_host = comment_has_been_answered_by_thread_author["time_Stamp_Answer"]

                        # Adds the calculated answer time to a local list for TOTAL
                        # noinspection PyTypeChecker
                        answer_time_iama_host_in_seconds = calculate_time_difference(
                            comment_creation_time, answer_time_stamp_iama_host)

                        dict_with_values_to_be_returned["iama_host_response_to_question_time_total_average"] \
                            .append(answer_time_iama_host_in_seconds)
                    else:
                        pass

                    # Whenever we are on tier 1
                    if bool_comment_is_on_tier_1 is True:
                        dict_with_values_to_be_returned["questions_tier_1"] += 1
                        dict_with_values_to_be_returned["question_tier_1_vote_average"].append(val.get("ups"))
                        dict_with_values_to_be_returned["reaction_time_between_questions_tier_1_average"]. \
                            append(comment_creation_time)

                        if comment_author not in dict_with_values_to_be_returned["amount_of_questioners_tier_1"]:
                            dict_with_values_to_be_returned["amount_of_questioners_tier_1"].append(comment_author)

                        else:
                            pass

                        if comment_has_been_answered_by_thread_author["question_Answered_From_Host"] is True:
                            dict_with_values_to_be_returned["questions_answered_by_iama_host_tier_1"] += 1

                            answer_time_stamp_iama_host = \
                                comment_has_been_answered_by_thread_author["time_Stamp_Answer"]

                            # Adds the calculated answer time to a local list for TIER 1
                            # noinspection PyTypeChecker
                            answer_time_iama_host_in_seconds = calculate_time_difference(
                                comment_creation_time, answer_time_stamp_iama_host)

                            dict_with_values_to_be_returned["iama_host_response_to_question_time_tier_1_average"] \
                                .append(answer_time_iama_host_in_seconds)

                        else:
                            pass
                    # Whenever we are NOT on tier 1 but on any other tier
                    else:
                        dict_with_values_to_be_returned["questions_tier_x"] += 1
                        dict_with_values_to_be_returned["question_tier_x_vote_average"].append(val.get("ups"))
                        dict_with_values_to_be_returned["reaction_time_between_questions_tier_x_average"]. \
                            append(comment_creation_time)

                        if comment_author not in dict_with_values_to_be_returned["amount_of_questioners_tier_x"]:
                            dict_with_values_to_be_returned["amount_of_questioners_tier_x"].append(comment_author)
                        else:
                            pass

                        if comment_has_been_answered_by_thread_author["question_Answered_From_Host"] is True:
                            dict_with_values_to_be_returned["questions_answered_by_iama_host_tier_x"] += 1

                            answer_time_stamp_iama_host = \
                                comment_has_been_answered_by_thread_author["time_Stamp_Answer"]

                            # Adds the calculated answer time to a local list for TIER X
                            # noinspection PyTypeChecker
                            answer_time_iama_host_in_seconds = calculate_time_difference(
                                comment_creation_time, answer_time_stamp_iama_host)

                            dict_with_values_to_be_returned["iama_host_response_to_question_time_tier_x_average"] \
                                .append(answer_time_iama_host_in_seconds)
                        else:
                            pass

                # Whenever the iterated "reaction" is just a comment and no question
                elif bool_comment_is_question is False and bool_comment_is_not_from_thread_author is True:
                    dict_with_values_to_be_returned["comments_total"] += 1
                    dict_with_values_to_be_returned["comment_total_vote_average"].append(val.get("ups"))
                    dict_with_values_to_be_returned["reaction_time_between_comments_total_average"]. \
                        append(comment_creation_time)

                    if comment_creation_time > dict_with_values_to_be_returned["time_value_of_last_comment"]:
                        dict_with_values_to_be_returned["time_value_of_last_comment"] = comment_creation_time

                    else:
                        pass

                    if comment_has_been_answered_by_thread_author["question_Answered_From_Host"] is True:
                        dict_with_values_to_be_returned["comments_answered_by_iama_host_total"] += 1

                        answer_time_stamp_iama_host = comment_has_been_answered_by_thread_author["time_Stamp_Answer"]

                        # Adds the calculated answer time to a local list for TOTAL
                        # noinspection PyTypeChecker
                        answer_time_iama_host_in_seconds = calculate_time_difference(
                            comment_creation_time, answer_time_stamp_iama_host)

                        dict_with_values_to_be_returned["iama_host_response_to_comment_time_total_average"] \
                            .append(answer_time_iama_host_in_seconds)
                    else:
                        pass

                    # Whenever that reaction is a comment and on tier 1
                    if bool_comment_is_on_tier_1 is True:
                        dict_with_values_to_be_returned["comments_tier_1"] += 1
                        dict_with_values_to_be_returned["comment_tier_1_vote_average"].append(val.get("ups"))
                        dict_with_values_to_be_returned["reaction_time_between_comments_tier_1_average"]. \
                            append(comment_creation_time)

                        if comment_author not in dict_with_values_to_be_returned["amount_of_commentators_tier_1"]:
                            dict_with_values_to_be_returned["amount_of_commentators_tier_1"].append(comment_author)
                        else:
                            pass

                        if comment_has_been_answered_by_thread_author["question_Answered_From_Host"] is True:
                            dict_with_values_to_be_returned["comments_answered_by_iama_host_tier_1"] += 1

                            answer_time_stamp_iama_host = \
                                comment_has_been_answered_by_thread_author["time_Stamp_Answer"]

                            # Adds the calculated answer time to a local list for TIER 1
                            # noinspection PyTypeChecker
                            answer_time_iama_host_in_seconds = calculate_time_difference(
                                comment_creation_time, answer_time_stamp_iama_host)

                            dict_with_values_to_be_returned["iama_host_response_to_comment_time_tier_1_average"] \
                                .append(answer_time_iama_host_in_seconds)
                        else:
                            pass

                    # Whenever this reaction is a comment and on tier x
                    else:
                        dict_with_values_to_be_returned["comments_tier_x"] += 1
                        dict_with_values_to_be_returned["comment_tier_x_vote_average"].append(val.get("ups"))
                        dict_with_values_to_be_returned["reaction_time_between_comments_tier_x_average"]. \
                            append(comment_creation_time)

                        if comment_author not in dict_with_values_to_be_returned["amount_of_commentators_tier_x"]:
                            dict_with_values_to_be_returned["amount_of_commentators_tier_x"].append(comment_author)
                        else:
                            pass

                        if comment_has_been_answered_by_thread_author["question_Answered_From_Host"] is True:
                            dict_with_values_to_be_returned["comments_answered_by_iama_host_tier_x"] += 1
                            answer_time_stamp_iama_host = \
                                comment_has_been_answered_by_thread_author["time_Stamp_Answer"]

                            # Adds the calculated answer time to a local list for TIER 1
                            # noinspection PyTypeChecker
                            answer_time_iama_host_in_seconds = calculate_time_difference(
                                comment_creation_time, answer_time_stamp_iama_host)

                            dict_with_values_to_be_returned["iama_host_response_to_comment_time_tier_x_average"] \
                                .append(answer_time_iama_host_in_seconds)
                        else:
                            pass

                # Whenever that iterated "reaction" is a comment or question FROM the thread author (!)
                else:
                    pass

            else:
                pass

    # noinspection PyNoneFunctionAssignment,PyTypeChecker
    average_reaction_time_comments_total = calculate_reaction_time_average(sorted(
        dict_with_values_to_be_returned["reaction_time_between_comments_total_average"]), thread_creation_time_stamp)

    # noinspection PyNoneFunctionAssignment,PyTypeChecker
    average_reaction_time_comments_tier_1 = calculate_reaction_time_average(sorted(
        dict_with_values_to_be_returned["reaction_time_between_comments_tier_1_average"]), thread_creation_time_stamp)

    # noinspection PyNoneFunctionAssignment,PyTypeChecker
    average_reaction_time_comments_tier_x = calculate_reaction_time_average(sorted(
        dict_with_values_to_be_returned["reaction_time_between_comments_tier_x_average"]), thread_creation_time_stamp)

    # noinspection PyNoneFunctionAssignment,PyTypeChecker
    average_reaction_time_questions_total = calculate_reaction_time_average(sorted(
        dict_with_values_to_be_returned["reaction_time_between_questions_total_average"]), thread_creation_time_stamp)

    # noinspection PyNoneFunctionAssignment,PyTypeChecker
    average_reaction_time_questions_tier_1 = calculate_reaction_time_average(sorted(
        dict_with_values_to_be_returned["reaction_time_between_questions_tier_1_average"]), thread_creation_time_stamp)

    # noinspection PyNoneFunctionAssignment,PyTypeChecker
    average_reaction_time_questions_tier_x = calculate_reaction_time_average(sorted(
        dict_with_values_to_be_returned["reaction_time_between_questions_tier_x_average"]), thread_creation_time_stamp)

    dict_life_span_values = calculate_life_span(thread_creation_time_stamp,
                                                dict_with_values_to_be_returned["time_value_of_last_comment"],
                                                dict_with_values_to_be_returned["time_value_of_last_question"])

    # Filling the dict, which we want to return, with values here
    if dict_with_values_to_be_returned["comment_total_vote_average"]:
        dict_with_values_to_be_returned["comment_total_vote_average"] = \
            np.median(dict_with_values_to_be_returned["comment_total_vote_average"])

    if dict_with_values_to_be_returned["comment_tier_1_vote_average"]:
        dict_with_values_to_be_returned["comment_tier_1_vote_average"] = \
            np.median(dict_with_values_to_be_returned["comment_tier_1_vote_average"])

    if dict_with_values_to_be_returned["comment_tier_x_vote_average"]:
        dict_with_values_to_be_returned["comment_tier_x_vote_average"] = \
            np.median(dict_with_values_to_be_returned["comment_tier_x_vote_average"])

    if dict_with_values_to_be_returned["question_total_vote_average"]:
        dict_with_values_to_be_returned["question_total_vote_average"] = \
            np.median(dict_with_values_to_be_returned["question_total_vote_average"])

    if dict_with_values_to_be_returned["question_tier_1_vote_average"]:
        dict_with_values_to_be_returned["question_tier_1_vote_average"] = \
            np.median(dict_with_values_to_be_returned["question_tier_1_vote_average"])

    if dict_with_values_to_be_returned["question_tier_x_vote_average"]:
        dict_with_values_to_be_returned["question_tier_x_vote_average"] = \
            np.median(dict_with_values_to_be_returned["question_tier_x_vote_average"])

    dict_with_values_to_be_returned["reaction_time_between_comments_total_average"] = \
        average_reaction_time_comments_total
    dict_with_values_to_be_returned["reaction_time_between_comments_tier_1_average"] = \
        average_reaction_time_comments_tier_1
    dict_with_values_to_be_returned["reaction_time_between_comments_tier_x_average"] = \
        average_reaction_time_comments_tier_x

    dict_with_values_to_be_returned["reaction_time_between_questions_total_average"] = \
        average_reaction_time_questions_total
    dict_with_values_to_be_returned["reaction_time_between_questions_tier_1_average"] = \
        average_reaction_time_questions_tier_1
    dict_with_values_to_be_returned["reaction_time_between_questions_tier_x_average"] = \
        average_reaction_time_questions_tier_x

    dict_with_values_to_be_returned["amount_of_questioners_total"] = (
        len(dict_with_values_to_be_returned["amount_of_questioners_tier_1"]) +
        len(dict_with_values_to_be_returned["amount_of_questioners_tier_x"])
    )

    dict_with_values_to_be_returned["amount_of_commentators_total"] = (
        len(dict_with_values_to_be_returned["amount_of_commentators_tier_1"]) +
        len(dict_with_values_to_be_returned["amount_of_commentators_tier_x"])
    )

    dict_with_values_to_be_returned["time_value_of_last_question"] = \
        dict_life_span_values["lifespan_thread_last_question"]

    dict_with_values_to_be_returned["time_value_of_last_comment"] = \
        dict_life_span_values["lifespan_thread_last_comment"]

    # Checks all list if they are empty or not.. Whenever they are empty set its value to None.. Because setting it
    # to 0 or some other datatype affects the statistical calculations in a bad way
    
    if not dict_with_values_to_be_returned["comment_total_vote_average"]:
        dict_with_values_to_be_returned["comment_total_vote_average"] = None

    if not dict_with_values_to_be_returned["comment_tier_1_vote_average"]:
        dict_with_values_to_be_returned["comment_tier_1_vote_average"] = None

    if not dict_with_values_to_be_returned["comment_tier_x_vote_average"]:
        dict_with_values_to_be_returned["comment_tier_x_vote_average"] = None

    if not dict_with_values_to_be_returned["question_total_vote_average"]:
        dict_with_values_to_be_returned["question_total_vote_average"] = None

    if not dict_with_values_to_be_returned["question_tier_1_vote_average"]:
        dict_with_values_to_be_returned["question_tier_1_vote_average"] = None

    if not dict_with_values_to_be_returned["question_tier_x_vote_average"]:
        dict_with_values_to_be_returned["question_tier_x_vote_average"] = None

    if dict_with_values_to_be_returned["iama_host_response_to_comment_time_total_average"]:
        dict_with_values_to_be_returned["iama_host_response_to_comment_time_total_average"] = \
            np.median(dict_with_values_to_be_returned["iama_host_response_to_comment_time_total_average"])
    else:
        dict_with_values_to_be_returned["iama_host_response_to_comment_time_total_average"] = None

    if dict_with_values_to_be_returned["iama_host_response_to_comment_time_tier_1_average"]:
        dict_with_values_to_be_returned["iama_host_response_to_comment_time_tier_1_average"] = \
            np.median(dict_with_values_to_be_returned["iama_host_response_to_comment_time_tier_1_average"])
    else:
        dict_with_values_to_be_returned["iama_host_response_to_comment_time_tier_1_average"] = None

    if dict_with_values_to_be_returned["iama_host_response_to_comment_time_tier_x_average"]:
        dict_with_values_to_be_returned["iama_host_response_to_comment_time_tier_x_average"] = \
            np.median(dict_with_values_to_be_returned["iama_host_response_to_comment_time_tier_x_average"])
    else:
        dict_with_values_to_be_returned["iama_host_response_to_comment_time_tier_x_average"] = None

    if dict_with_values_to_be_returned["iama_host_response_to_question_time_total_average"]:
        dict_with_values_to_be_returned["iama_host_response_to_question_time_total_average"] = \
            np.median(dict_with_values_to_be_returned["iama_host_response_to_question_time_total_average"])
    else:
        dict_with_values_to_be_returned["iama_host_response_to_question_time_total_average"] = None

    if dict_with_values_to_be_returned["iama_host_response_to_question_time_tier_1_average"]:
        dict_with_values_to_be_returned["iama_host_response_to_question_time_tier_1_average"] = \
            np.median(dict_with_values_to_be_returned["iama_host_response_to_question_time_tier_1_average"])
    else:
        dict_with_values_to_be_returned["iama_host_response_to_question_time_tier_1_average"] = None

    if dict_with_values_to_be_returned["iama_host_response_to_question_time_tier_x_average"]:
        dict_with_values_to_be_returned["iama_host_response_to_question_time_tier_x_average"] = \
            np.median(dict_with_values_to_be_returned["iama_host_response_to_question_time_tier_x_average"])
    else:
        dict_with_values_to_be_returned["iama_host_response_to_question_time_tier_x_average"] = None

    if dict_with_values_to_be_returned["amount_of_questioners_total"] == 0:
        dict_with_values_to_be_returned["amount_of_questioners_total"] = None

    if not dict_with_values_to_be_returned["amount_of_questioners_tier_1"]:
        dict_with_values_to_be_returned["amount_of_questioners_tier_1"] = None
    else:
        dict_with_values_to_be_returned["amount_of_questioners_tier_1"] = len(dict_with_values_to_be_returned
                                                                              ["amount_of_questioners_tier_1"])
    if not dict_with_values_to_be_returned["amount_of_questioners_tier_x"]:
        dict_with_values_to_be_returned["amount_of_questioners_tier_x"] = None
    else:
        dict_with_values_to_be_returned["amount_of_questioners_tier_x"] = len(dict_with_values_to_be_returned
                                                                              ["amount_of_questioners_tier_x"])
    if dict_with_values_to_be_returned["amount_of_commentators_total"] == 0:
        dict_with_values_to_be_returned["amount_of_commentators_total"] = None

    if not dict_with_values_to_be_returned["amount_of_commentators_tier_1"]:
        dict_with_values_to_be_returned["amount_of_commentators_tier_1"] = None
    else:
        dict_with_values_to_be_returned["amount_of_commentators_tier_1"] = len(dict_with_values_to_be_returned
                                                                               ["amount_of_commentators_tier_1"])
    if not dict_with_values_to_be_returned["amount_of_commentators_tier_x"]:
        dict_with_values_to_be_returned["amount_of_commentators_tier_x"] = None
    else:
        dict_with_values_to_be_returned["amount_of_commentators_tier_x"] = len(dict_with_values_to_be_returned
                                                                               ["amount_of_commentators_tier_x"])

    # Final checking for return here !
    # Whenever one of the two time values is negative (which means nobody or only "AutoModerator" have responded
    # Return nothing, otherwise return the dict

    # Whenever there only comments were made but no questions have been asked
    if (dict_with_values_to_be_returned["time_value_of_last_comment"] > 0) and \
            (dict_with_values_to_be_returned["time_value_of_last_question"] < 0):
        dict_with_values_to_be_returned["time_value_of_last_question"] = None
    else:
        pass

    # Whenever only questions have asked made but no comments have been made
    if (dict_with_values_to_be_returned["time_value_of_last_comment"] < 0) and \
            (dict_with_values_to_be_returned["time_value_of_last_question"] > 0):
        dict_with_values_to_be_returned["time_value_of_last_comment"] = None
    else:
        pass

    # Whenever no questions and no comments have been made (and even the AutoModerator didn't do anything)
    if (dict_with_values_to_be_returned["time_value_of_last_comment"] is None or
                dict_with_values_to_be_returned["time_value_of_last_comment"] < 0) and \
            (dict_with_values_to_be_returned["time_value_of_last_question"] is None or
                     dict_with_values_to_be_returned["time_value_of_last_question"] < 0):

        dict_with_values_to_be_returned["time_value_of_last_comment"] = None
        dict_with_values_to_be_returned["time_value_of_last_question"] = None
    else:
        pass

    return dict_with_values_to_be_returned


def check_if_comment_is_a_question(given_string):
    """Simply checks whether a given string is a question or not

    This method simply checks wether a question mark exists within that string or not..
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


def check_if_comment_has_been_answered_by_thread_author(author_of_thread, comment_actual_id, comments_cursor):
    """Checks whether both strings are equal or not

    1. A dictionary containing flags whether that a question is answered by the host with the appropriate timestamp will
        be created in the beginning.
    2. Then the method iterates over every comment within that thread
        1.1. Whenever an answer is from the iAMA hosts and the processed comments 'parent_id' matches the iAMA hosts
            comments (answers) id, the returned dict will contain appropriate values and will be returned
        1.2. If this is not the case, it will be returned in its default condition

    Note: We take a list as 'comments_cursor' and not a real cursor, because real cursors can be exhausted, which
            could lead to, that not all comments will be iterated.. This is especially critical when you have to do
            many iterations with only one cursor... [took me 8 hours to figure this "bug" out...]

    Args:
        author_of_thread (str) : The name of the thread author (iAMA-Host)
        comment_actual_id (str) : The id of the actually processed comment
        comments_cursor (list) : The list containing all comments
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
    for i, val in enumerate(comments_cursor):

        check_comment_parent_id = val.get("parent_id")
        actual_comment_author = val.get("author")

        # Whenever the iterated comment is from the iAMA-Host and that
        # comment has the question as parent_id
        if (check_if_comment_is_not_from_thread_author(author_of_thread, actual_comment_author) == False) and \
                (check_comment_parent_id == comment_actual_id):

            dict_to_be_returned["question_Answered_From_Host"] = True
            dict_to_be_returned["time_Stamp_Answer"] = val.get("created_utc")

            return dict_to_be_returned

    # This is the case whenever a comment has not a single thread or the comment / question has not been answered
    return dict_to_be_returned


def calculate_time_difference(comment_time_stamp, answer_time_stamp_iama_host):
    """Calculates the time difference in seconds between the a comment and its answer from the iama host

    1. The time stamps will be converted from epoch
        into float and afterwards into str again
        (necessary for correct subtraction)
    2. Then the time stamps will be subtracted from each other
    3. The containing time difference will be converted into seconds (int)

    Args:
        comment_time_stamp (str): The time stamp of the comment
        answer_time_stamp_iama_host (str): The time stamp of the iAMA hosts answer
    Returns:
        time_difference_in_seconds (int) : The time difference of the comment and its answer by the iAMA host in seconds
    """

    # Converts the time_Value into float, otherwise it could not be processed any further...
    comment_time_value = float(comment_time_stamp)
    comment_time_converted = datetime.datetime.fromtimestamp(
        comment_time_value).strftime('%d-%m-%Y %H:%M:%S')
    comment_time_converted_for_subtraction = datetime.datetime.strptime(
        comment_time_converted, '%d-%m-%Y %H:%M:%S')

    # Converts the time_Value into float, otherwise it could not be processed any further...
    answer_time_iama_host = float(answer_time_stamp_iama_host)
    answer_time_iama_host_converted = datetime.datetime.fromtimestamp(
        answer_time_iama_host).strftime('%d-%m-%Y %H:%M:%S')
    answer_time_iama_host_converted_for_subtraction = datetime.datetime.strptime(
        answer_time_iama_host_converted, '%d-%m-%Y %H:%M:%S')

    # Calculates the time difference between the comment and the iAMA hosts answer
    time_difference_in_seconds = (
        answer_time_iama_host_converted_for_subtraction -
        comment_time_converted_for_subtraction
    ).total_seconds()

    return time_difference_in_seconds


def calculate_reaction_time_average(list_to_be_processed, thread_creation_time_stamp):
    """Calculates the reaction time of a list with time values in it

    Args:
        list_to_be_processed (list) : The list which contains time values (utc epoch)
        thread_creation_time_stamp (str) : The string which contains the creation date of the thread (utc epoch)
    Returns:
        None : Whenever there were no time values given
        np.median(time_difference) (float) : Time arithmetic median of the reaction time in seconds

    """

    # Will contain the time difference between each "reactions" in seconds
    time_difference = []

    for i, val in enumerate(list_to_be_processed):
        # Convert the time_Value into float, otherwise it could not be converted...
        time_value_current = float(val)

        current_time_converted = datetime.datetime.fromtimestamp(
            time_value_current).strftime('%d-%m-%Y %H:%M:%S')

        current_time_converted_for_subtraction = datetime.datetime.strptime(
            current_time_converted, '%d-%m-%Y %H:%M:%S')

        # Whenever a thread only has one single comment which is not null
        if len(list_to_be_processed) == 1:
            # Converts the thread creation date into a comparable time format
            temp_creation_date_of_thread = float(thread_creation_time_stamp)

            temp_creation_date_of_thread_converted = datetime.datetime.fromtimestamp(
                temp_creation_date_of_thread).strftime('%d-%m-%Y %H:%M:%S')

            # Subtracts the comment creation time from the thread creation time
            temp_thread_time = datetime.datetime.strptime(
                temp_creation_date_of_thread_converted, '%d-%m-%Y %H:%M:%S')

            # Add the difference between those two times, in seconds, to that list
            time_difference.append(
                (current_time_converted_for_subtraction - temp_thread_time).total_seconds())

        # Whenever the last list object is iterated over skip anything because there will be no future object
        elif i != len(list_to_be_processed) - 1:
            # Convers the next time_Value into float
            time_value_next = float(list_to_be_processed[i + 1])
            next_time_converted = datetime.datetime.fromtimestamp(
                time_value_next).strftime('%d-%m-%Y %H:%M:%S')

            next_time_converted_for_subtraction = datetime.datetime.strptime(
                next_time_converted, '%d-%m-%Y %H:%M:%S')

            # Whenever the first commented gets iterated over, build the
            # difference between thread and 1st comment creation date
            if i == 0:
                # Converts the thread creation date into a comparable time format
                temp_creation_date_of_thread = float(thread_creation_time_stamp)

                temp_creation_date_of_thread_converted = datetime.datetime.fromtimestamp(
                    temp_creation_date_of_thread).strftime('%d-%m-%Y %H:%M:%S')

                # Subtracts the comment creation time from the thread creation time
                temp_thread_time = datetime.datetime.strptime(
                    temp_creation_date_of_thread_converted, '%d-%m-%Y %H:%M:%S')

                # Add the difference between those two times, in seconds, to that list
                time_difference.append(
                    (current_time_converted_for_subtraction -
                     temp_thread_time).total_seconds())

            else:
                # Appends the difference between the time of the current and next comment into the time_difference
                # variable
                time_difference.append(
                    (next_time_converted_for_subtraction - current_time_converted_for_subtraction).total_seconds())

        else:
            pass

    if len(time_difference) is 0:
        return None
    else:
        return np.median(time_difference)


def calculate_life_span(thread_creation_time_stamp, time_value_of_last_comment, time_value_of_last_question):
    """Calculates the life span between to time stamps

    1. The creation date of a thread gets determined
    2. Then the comments will be iterated over, creating a dictionary which is structured as follows:
      {
          ('first_Comment_After_Thread_Started', int),
          ('thread_life_span', int),
          ('arithmetic_Mean_Response_Time', int),
          ('median_Response_Time', int),
          ('id')
      }
    3. That returned dictionary will be appended to a global list
    4. That List will be iterated later on and the appropriate graph will be plotted

    Args:
        thread_creation_time_stamp (float) : The time stamp (utc epoch) of the thread creation
        time_value_of_last_comment (float) : The time stamp (utc epoch) of the threads last comment
        time_value_of_last_question (float) : The time stamp (utc epoch) of the threads last question
    Returns:
        dict_to_be_returned (dict) : Containing information about the time differences:
            Thread creation timestamp <-> Last question time stamp
            Thread creation timestamp <-> Last comment time stamp

    """

    # Conversion of threads creation timestamp
    temp_creation_date_of_thread = datetime.datetime.fromtimestamp(float(thread_creation_time_stamp)) \
        .strftime('%d-%m-%Y %H:%M:%S')
    temp_creation_date_of_thread_converted = datetime.datetime.strptime(
        temp_creation_date_of_thread, '%d-%m-%Y %H:%M:%S')

    # Conversion of threads last comement time stamp
    temp_time_stamp_last_comment = datetime.datetime.fromtimestamp(float(time_value_of_last_comment)) \
        .strftime('%d-%m-%Y %H:%M:%S')
    temp_time_stamp_last_comment_converted = datetime.datetime.strptime(
        temp_time_stamp_last_comment, '%d-%m-%Y %H:%M:%S')

    # Conversion of threads last question time stamp
    temp_time_stamp_last_question = datetime.datetime.fromtimestamp(float(time_value_of_last_question)) \
        .strftime('%d-%m-%Y %H:%M:%S')
    temp_time_stamp_last_question_converted = datetime.datetime.strptime(
        temp_time_stamp_last_question, '%d-%m-%Y %H:%M:%S')

    # The dictionary containing information about both life spans
    dict_to_be_returned = {
        "lifespan_thread_last_comment": (temp_time_stamp_last_comment_converted -
                                         temp_creation_date_of_thread_converted).total_seconds(),
        "lifespan_thread_last_question": (temp_time_stamp_last_question_converted -
                                          temp_creation_date_of_thread_converted).total_seconds()
    }

    return dict_to_be_returned


def add_actual_year_list_to_global_list(list_to_append):
    """Iterates over a given list with thread information and adds every single element to a global list
        The global list will be printed to csv in the end

    Args:
        list_to_append (list) : List with thread information which will be appended to a global list
    Returns:
        -
    """

    global list_global_year

    for item in list_to_append:
        list_global_year.append(item)


def write_csv_data(list_with_information):
    """Creates a csv file containing all necessary information about the thread and its mannerism to do research on

    Args:
        list_with_information (list) : Contains various information about threads mannerism
    Returns:
        -
    """

    print("---- Writing csv containing all thread information for year " + str(year_actually_in_progress) + " now")
    # Empty print line here for a more beautiful console output
    print("")

    file_name_csv = str(os.path.basename(__file__))[0:len(os.path.basename(__file__)) - 3] + \
                    '_' + \
                    str(argument_year_beginning) + \
                    '_until_' + \
                    str(argument_year_ending) + \
                    '_' + \
                    "BIGDATA" + \
                    '_' + \
                    str(year_actually_in_progress) + \
                    '.csv'

    with open(file_name_csv, 'w', newline='') as fp:
        csv_writer = csv.writer(fp, delimiter=',')

        # The heading of the csv file.. sep= is needed, otherwise Microsoft Excel would not recognize seperators..
        data = [['Year',
                 'Thread id',
                 'Thread author',
                 'Thread ups',
                 'Thread downs',
                 'Thread creation time stamp',

                 'Thread average comment vote score total',
                 'Thread average comment vote score tier 1',
                 'Thread average comment vote score tier x',

                 'Thread average question vote score total',
                 'Thread average question vote score tier 1',
                 'Thread average question vote score tier x',

                 'Thread num comments total skewed',
                 'Thread num comments total',
                 'Thread num comments tier 1',
                 'Thread num comments tier x',

                 'Thread num questions total',
                 'Thread num questions tier 1',
                 'Thread num questions tier x',

                 'Thread num questions answered by iama host total',
                 'Thread num questions answered by iama host tier 1',
                 'Thread num questions answered by iama host tier x',

                 'Thread num comments answered by iama host total',
                 'Thread num comments answered by iama host tier 1',
                 'Thread num comments answered by iama host tier x',

                 'Thread average reaction time between comments total',
                 'Thread average reaction time between comments tier 1',
                 'Thread average reaction time between comments tier x',

                 'Thread average reaction time between questions total',
                 'Thread average reaction time between questions tier 1',
                 'Thread average reaction time between questions tier x',

                 'Thread average response to question time iama host total',
                 'Thread average response to question time iama host tier 1',
                 'Thread average response to question time iama host tier x',

                 'Thread average response to comment time iama host total',
                 'Thread average response to comment time iama host tier 1',
                 'Thread average response to comment time iama host tier x',

                 'Thread amount of questioners total',
                 'Thread amount of questioners tier 1',
                 'Thread amount of questioners tier x',

                 'Thread amount of commentators total',
                 'Thread amount of commentators tier 1',
                 'Thread amount of commentators tier x',

                 'Thread life span until last comment',
                 'Thread life span until last question']]

        # Iterates over that generated sorted and counts the amount of questions which have not been answered
        for item in list_with_information:

            temp_list = [str(item.get("Year")),
                         str(item.get("Thread_id")),
                         str(item.get("Thread_author")),
                         str(item.get("Thread_ups")),
                         str(item.get("Thread_downs")),
                         str(item.get("Thread_creation_time_stamp")),

                         str(item.get("Thread_average_comment_vote_score_total")),
                         str(item.get("Thread_average_comment_vote_score_tier_1")),
                         str(item.get("Thread_average_comment_vote_score_tier_x")),

                         str(item.get("Thread_average_question_vote_score_total")),
                         str(item.get("Thread_average_question_vote_score_tier_1")),
                         str(item.get("Thread_average_question_vote_score_tier_x")),

                         str(item.get("Thread_num_comments_total_skewed")),
                         str(item.get("Thread_num_comments_total")),
                         str(item.get("Thread_num_comments_tier_1")),
                         str(item.get("Thread_num_comments_tier_x")),

                         str(item.get("Thread_num_questions_total")),
                         str(item.get("Thread_num_questions_tier_1")),
                         str(item.get("Thread_num_questions_tier_x")),

                         str(item.get("Thread_num_questions_answered_by_iama_host_total")),
                         str(item.get("Thread_num_questions_answered_by_iama_host_tier_1")),
                         str(item.get("Thread_num_questions_answered_by_iama_host_tier_x")),

                         str(item.get("Thread_num_comments_answered_by_iama_host_total")),
                         str(item.get("Thread_num_comments_answered_by_iama_host_tier_1")),
                         str(item.get("Thread_num_comments_answered_by_iama_host_tier_x")),


                         str(item.get("Thread_average_reaction_time_between_comments_total")),
                         str(item.get("Thread_average_reaction_time_between_comments_tier_1")),
                         str(item.get("Thread_average_reaction_time_between_comments_tier_x")),

                         str(item.get("Thread_average_reaction_time_between_questions_total")),
                         str(item.get("Thread_average_reaction_time_between_questions_tier_1")),
                         str(item.get("Thread_average_reaction_time_between_questions_tier_x")),

                         str(item.get("Thread_average_iama_host_response_to_question_time_total")),
                         str(item.get("Thread_average_iama_host_response_to_question_time_tier_1")),
                         str(item.get("Thread_average_iama_host_response_to_question_time_tier_x")),

                         str(item.get("Thread_average_iama_host_response_to_comment_time_total")),
                         str(item.get("Thread_average_iama_host_response_to_comment_time_tier_1")),
                         str(item.get("Thread_average_iama_host_response_to_comment_time_tier_x")),

                         str(item.get("Thread_amount_of_questioners_total")),
                         str(item.get("Thread_amount_of_questioners_tier_1")),
                         str(item.get("Thread_amount_of_questioners_tier_x")),

                         str(item.get("Thread_amount_of_commentators_total")),
                         str(item.get("Thread_amount_of_commentators_tier_1")),
                         str(item.get("Thread_amount_of_commentators_tier_x")),

                         str(item.get("Thread_life_span_comment")),
                         str(item.get("Thread_life_span_question"))]

            data.append(temp_list)

        # Writes data into the csv file
        csv_writer.writerows(data)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Necessary variables and scripts are here

# Contains the year which is given as an argument
argument_year_beginning = 0

# Contains the year which is given as an argument
argument_year_ending = 0

# Contains the year which will be processed at the moment
year_actually_in_progress = 0

# Contains information for the current year
list_current_year = []

# Contains information for all years about all threads within reddit
list_global_year = []


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Methods which are to be called are here

# Executes necessary checks
check_script_arguments()

# Initializes the mongoDB with the arguments given via command line
initialize_mongo_db_parameters(argument_year_beginning)

# Starts the data generation and writes csv files containg these information
start_data_generation_for_analysis()
