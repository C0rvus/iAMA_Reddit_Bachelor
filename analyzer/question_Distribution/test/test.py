# Tutorials used within this class:
# 1. (12.03.2016 @ 16:53) -
# https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-values-of-the-dictionary-in-python

import collections               # Necessary to sort collections alphabetically
import datetime                     # Necessary to do time calculation
from pymongo import MongoClient     # Necessary to make use of MongoDB

# The mongo client, necessary to connect to mongoDB
mongo_DB_Client_Instance = MongoClient('localhost', 27017)

# The data base instance for the threads
mongo_DB_Threads_Instance_2009 = mongo_DB_Client_Instance.iAMA_Reddit_Threads_2009

# Contains all collection names of the thread database
mongo_DB_Thread_Collection_2009 = mongo_DB_Threads_Instance_2009.collection_names()

# The data base instance for the comments
mongo_DB_Comments_Instance_2009 = mongo_DB_Client_Instance.iAMA_Reddit_Comments_2009

# Will contain all analyzed time information for threads & comments
list_To_Be_Plotted = []

# Calculates the time difference between to time stamps in seconds


def calculate_time_difference(comment_time_stamp, answer_time_stamp_iama_host):

    # Converts the time_Value into float, otherwise it could not be processed
    # any further...
    comment_time_value = float(comment_time_stamp)
    comment_time_converted = datetime.datetime.fromtimestamp(
        comment_time_value).strftime('%d-%m-%Y %H:%M:%S')
    comment_time_converted_for_subtraction = datetime.datetime.strptime(
        comment_time_converted, '%d-%m-%Y %H:%M:%S')

    # Converts the time_Value into float, otherwise it could not be processed
    # any further...
    answer_time_iama_host = float(answer_time_stamp_iama_host)
    answer_time_iama_host_converted = datetime.datetime.fromtimestamp(
        answer_time_iama_host).strftime('%d-%m-%Y %H:%M:%S')
    answer_time_iama_host_converted_for_subtraction = datetime.datetime.strptime(
        answer_time_iama_host_converted, '%d-%m-%Y %H:%M:%S')

    # Calculates the time difference between the comment and the iAMA hosts
    # answer
    time_difference_in_seconds = (
        answer_time_iama_host_converted_for_subtraction -
        comment_time_converted_for_subtraction).total_seconds()

    return time_difference_in_seconds

# Checks whether the thread host has answered a given question


def check_if_comment_is_answer_from_thread_author(author_of_thread, comment_acutal_id, comments_cursor):

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
            if (
                    check_if_comment_is_not_from_thread_author(
                        author_of_thread,
                        actual_comment_author) == False) and (
                    check_comment_parent_id == comment_acutal_id):

                dict_to_be_returned["question_Answered_From_Host"] = True
                dict_to_be_returned[
                    "time_Stamp_Answer"] = collection.get("created_utc")

                return dict_to_be_returned
            else:
                return dict_to_be_returned
        else:
            return dict_to_be_returned

    # This is the case whenever a comment has not a single thread
    return dict_to_be_returned

# Checks whether the postet comment is not from the thread creator


def check_if_comment_is_not_from_thread_author(author_of_thread, comment_author):

    if author_of_thread != comment_author:
        return True
    else:
        return False

# Could be expanded later on, if checking for question mark is not enough


def check_if_comment_is_a_question(given_string):

    if "?" in given_string:
        return True
    else:
        return False

# Calculates some values for later correlation checking between thread creation date, upvote and answer possibility


def calculate_answered_question_upvote_correlation(id_of_thread, author_of_thread, thread_creation_date):

    # Makes the global comments instance locally available here
    global mongo_DB_Comments_Instance_2009

    comments_collection = mongo_DB_Comments_Instance_2009[id_of_thread]
    comments_cursor = comments_collection.find()

    amount_of_results = []

    amount_of_tier_any_questions = 0
    amount_of_tier_any_questions_answered = 0

    # Iterates over every comment within that thread
    for collection in comments_cursor:

        # Whenever the iterated comment was created by user "AutoModerator"
        # skip it
        if (collection.get("author")) != "AutoModerator":

            # References the text of the comment
            comment_text = collection.get("body")
            comment_author = collection.get("author")
            comment_parent_id = collection.get("parent_id")
            comment_acutal_id = collection.get("name")
            comment_time_stamp = collection.get("created_utc")
            comment_upvotes = collection.get("ups")
            # A dictionary containing the results necessary for the calculation here
            dict_result = {
                "id_thread": id_of_thread,
                "id_question": comment_acutal_id,
                "question_ups": comment_upvotes,
                "time_since_thread_started": 0,
                "question_answered": bool
            }

            # Whenever some values are not None.. (Values can be null / None, whenever they have been deleted)
            if comment_text is not None \
                    and comment_author is not None \
                    and comment_parent_id is not None:

                # Calculation of time since thread has been started can only happen here, because of previous checks
                dict_result["time_since_thread_started"] = \
                    calculate_time_difference(thread_creation_date, comment_time_stamp),

                bool_comment_is_question = check_if_comment_is_a_question(comment_text)

                bool_comment_is_not_from_thread_author = check_if_comment_is_not_from_thread_author(
                    author_of_thread, comment_author)

                # If the posted comment is a question and is not from the thread author
                if bool_comment_is_question \
                        and bool_comment_is_not_from_thread_author:

                    amount_of_tier_any_questions += 1

                    # Check whether that iterated comment is answered by the host
                    answer_is_from_thread_author = check_if_comment_is_answer_from_thread_author(
                        author_of_thread, comment_acutal_id, comments_cursor)

                    # Whenever the answer to that comment is from the author
                    if answer_is_from_thread_author["question_Answered_From_Host"] is True:

                        amount_of_tier_any_questions_answered += 1

                        # Whenever the question has been answered by the iAMA-Host
                        dict_result["question_answered"] = True
                        dict_result = collections.OrderedDict(sorted(dict_result.items()))
                        amount_of_results.append(dict_result)

                    # Whenever the question has not been answered by the iAMA-Host
                    else:
                        dict_result["question_answered"] = False
                        dict_result = collections.OrderedDict(sorted(dict_result.items()))
                        amount_of_results.append(dict_result)

                # Skip that comment
                else:
                    continue

            # Whenever a comment has been deleted or has, somehow, null values in it.. do not process it
            else:
                continue

    # Whenever there were some questions aksed at alland those questions have been answered by the iAMA host on any tier
    if amount_of_tier_any_questions != 0 and amount_of_tier_any_questions_answered != 0:

        # Returns the arithmetic mean of answer time by the iAMA host
        return amount_of_results

    # Whenever no questions have been asked at all
    else:
        print(
            "Thread '" +
            str(id_of_thread) +
            "' will not be included in the calculation because there are no questions asked on any tier")
        return None


# Generates the data which will be analyzed later on


def generate_data_to_analyze():
    for j, val in enumerate(mongo_DB_Thread_Collection_2009):

        # Skips the system.indexes-table which is automatically created by
        # mongodb itself
        if not val == "system.indexes":
            # References the actual iterated thread
            temp_thread = mongo_DB_Threads_Instance_2009[val]

            # Gets the authors name of the iterated thread
            temp_thread_author = temp_thread.find()[0].get("author")

            # Gets the creation date of the iterated thread
            temp_thread_creation_date = temp_thread.find()[0].get("created_utc")

            # Gets the title of that iterated thread
            temp_thread_title = temp_thread.find()[0].get("title")

            # removes iAMA-Requests out of our selection
            if "request" in temp_thread_title.lower() \
                    and "as requested" not in temp_thread_title.lower() \
                    and "by request" not in temp_thread_title.lower() \
                    and "per request" not in temp_thread_title.lower() \
                    and "request response" not in temp_thread_title.lower():
                continue

            returned_value = calculate_answered_question_upvote_correlation(
                val, temp_thread_author, temp_thread_creation_date

            )

            # Value could be none if it has i.E. no values
            if returned_value is not None:
                list_To_Be_Plotted.append(returned_value)

# Prepares the data which will be plotted later. (Does some sorting)


def prepare_data_to_be_plotted():

    # Will contain all comments later on
    all_comments = []

    # Defines the amount of the top 100 questions (by upvotes) which have not been answered
    amount_of_questions_not_answered = 0

    # Iterates over every ordered list
    for i, val in enumerate(list_To_Be_Plotted):

        # Iterates over the sub elements within that iterated object
        for j, val_2 in enumerate(val):

            # breaks comment hierarchy und creates a flat list of all comments
            all_comments.append(val_2)

    # Creates a "sorted" which contains all comments of that year, sorted by upvotes in descending order
    new_list = sorted(all_comments, key=lambda k: k['question_ups'], reverse=True)

    # Iterates over that generated sorted and counts the amount of questions which have not been answered
    for item in new_list[0:100]:
        if item.get("question_answered") is False:
            amount_of_questions_not_answered += 1

    print(amount_of_questions_not_answered)












# Generates the data which will be plotted later on
generate_data_to_analyze()

# Plots the generated data
prepare_data_to_be_plotted()
