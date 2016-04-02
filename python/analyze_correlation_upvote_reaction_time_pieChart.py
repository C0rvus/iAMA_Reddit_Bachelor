# Tutorials used within this class:
# 1. (13.03.2016 @ 15:41) -
# https://stackoverflow.com/questions/19428029/how-to-get-correlation-of-two-vectors-in-python
# 2. (13.03.2016 @ 16.11) -
# https://stackoverflow.com/questions/13964872/pyplot-tab-character

import copy                             # Necessary to copy value of the starting year
import matplotlib.pyplot as plt         # Necessary to plot graphs with the data calculated
import datetime                         # Necessary to do time calculation
import sys                              # Necessary to use script arguments

import numpy as np
from pymongo import MongoClient         # Necessary to make use of MongoDB
from scipy.stats.stats import pearsonr  # Necessary for correlation calculation


def check_script_arguments():
    """Checks if enough and correct arguments have been given to run this script adequate

    1. It checks in the first instance if enough arguments have been given
    2. Then necessary variables will be filled with appropriate values

    Args:
        -
    Returns:
        -
    """

    global argument_year_beginning, argument_year_ending, argument_tier_in_scope, argument_plot_time_unit, \
        argument_plot_x_limiter

    # Whenever not enough arguments were given
    if len(sys.argv) <= 4:
        print("Not enough arguments were given...")
        print("Terminating script now!")
        sys.exit()
    else:
        # Parses the first argument to the variable
        argument_year_beginning = int(sys.argv[1])
        argument_year_ending = int(sys.argv[2])
        argument_tier_in_scope = str(sys.argv[3]).lower()
        argument_plot_time_unit = str(sys.argv[4]).lower()
        argument_plot_x_limiter = int(sys.argv[5])


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
    """Starts the data processing by swichting through the years

    1. Triggers the data generation process and moves forward within the years
        1.1. By moving through the years a csv file will be created for every year
        1.2. Additionally an interactive chart will be plotted

    Args:
        -
    Returns:
        -
    """

    global argument_year_beginning, data_to_give_plotly, year_actually_in_progress, global_thread_list, \
        list_To_Be_Plotted

    # Copies the value of the beginning year, because it will be changed due to moving forward within the years
    year_actually_in_progress = int(copy.copy(argument_year_beginning))

    data_to_give_plotly.append(["SHITSHITFUCKFUCK", str(argument_tier_in_scope)])

    # As long as the ending year has not been reached
    while year_actually_in_progress != argument_year_ending:

        # Starts retrieving and checking that data
        generate_data_to_be_analyzed()
        print_data_to_commandline(list_To_Be_Plotted)
        add_list_to_global_list(list_To_Be_Plotted)
        list_To_Be_Plotted = []

        # Progresses in the year, necessary for onward year calculation
        year_actually_in_progress += 1

        # Reinitializes the mongodb with new year parameter here
        initialize_mongo_db_parameters(year_actually_in_progress)

    # Will be entered whenever the last year is beeing processed
    if year_actually_in_progress == argument_year_ending:

        # Starts retrieving and checking that data
        generate_data_to_be_analyzed()
        print_data_to_commandline(list_To_Be_Plotted)
        add_list_to_global_list(list_To_Be_Plotted)
        list_To_Be_Plotted = []

    year_actually_in_progress = "ALL"
    print_data_to_commandline(global_thread_list)


def generate_data_to_be_analyzed():
    """Generates the data which will be analyzed

    1. This method iterates over every thread
        1.1. It filters if that iterated thread is an iAMA-request or not
            1.1.1. If yes: this thread gets skipped and the next one will be processed
            1.1.2. If no: this thread will be processed
    2. If the thread gets processed it will receive the arithmetic mean of answer time
    3. This value will be added to a global list and will be plotted later on
    Args:
        -
    Returns:
        -
    """

    print("Generating data for year " + str(year_actually_in_progress) + " now...")

    # noinspection PyTypeChecker
    for j, val in enumerate(mongo_DB_Thread_Collection):

        # Skips the system.indexes-table which is automatically created by
        # mongodb itself
        if not val == "system.indexes":
            # References the actual iterated thread
            temp_thread = mongo_DB_Threads_Instance[val]

            # Gets the creation date of that iterated thread
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

            returned_value = calculate_comment_upvotes_and_response_time_by_host(val, temp_thread_author)

            # Value could be none if it has i.E. no values
            if returned_value is not None:
                list_To_Be_Plotted.append(returned_value)


def add_list_to_global_list(list_to_append):

    global global_thread_list

    for item in list_to_append:
        global_thread_list.append(item)


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


def check_if_comment_is_answer_from_thread_author(author_of_thread, comment_acutal_id, comments_cursor):
    """Checks whether both strings are equal or not

    1. A dictionary containing flags whether that a question is answered by the host with the appropriate timestamp will
        be created in the beginning.
    2. Then the method iterates over every comment within that thread
        1.1. Whenever an answer is from the iAMA hosts and the processed comments 'parent_id' matches the iAMA hosts
            comments (answers) id, the returned dict will contain appropriate values and will be returned
        1.2. If this is not the case, it will be returned in its default condition

    Args:
        author_of_thread (str) : The name of the thread author (iAMA-Host)
        comment_acutal_id (str) : The id of the actually processed comment
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
            if (check_if_comment_is_not_from_thread_author(
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


def calculate_comment_upvotes_and_response_time_by_host(id_of_thread, author_of_thread):
    """Calculates the arithmetic mean of the answer time by the iama host in minutes

    In dependence of the given tier argument (second argument) the processing of tiers will be filtered

    Args:
        id_of_thread (str): The id of the thread which is actually processed. (Necessary for checking if a question
            lies on tier 1 or any other tier)
        author_of_thread (str): The name of the thread author. (Necessary for checking if a given answer is from the
            iama host or not)
    Returns:
        Whenever there was a minimum of 1 question asked and 1 answer from the iama host:
            amount_of_upvotes_reaction_time (int) : The amount of the arithmetic mean time of
        Whenever there no questions have been asked for that thread / or no answers were given /
            or all values in the database were null:
            None:   Returns an empty object of the type None
    """

    global mongo_DB_Comments_Instance

    comments_collection = mongo_DB_Comments_Instance[id_of_thread]
    comments_cursor = comments_collection.find()

    amount_of_upvotes_reaction_time = []

    amount_of_questions = 0
    amount_of_questions_answered = 0

    # Iterates over every comment within that thread
    for collection in comments_cursor:

        # Whenever the iterated comment was created by user "AutoModerator" skip it
        if (collection.get("author")) != "AutoModerator":

            # References the text of the comment
            comment_text = collection.get("body")
            comment_author = collection.get("author")
            comment_parent_id = collection.get("parent_id")
            comment_acutal_id = collection.get("name")
            comment_time_stamp = collection.get("created_utc")
            comment_upvotes = collection.get("ups")

            # Whenever some values are not None.. (Values can be null / None, whenever they have been deleted)
            if comment_text is not None \
                    and comment_author is not None \
                    and comment_parent_id is not None:

                bool_comment_is_question = check_if_comment_is_a_question(comment_text)

                bool_comment_is_question_on_tier_1 = check_if_comment_is_on_tier_1(comment_parent_id)

                bool_comment_is_not_from_thread_author = check_if_comment_is_not_from_thread_author(
                    author_of_thread, comment_author)

                # Whenever the scope lies on the first tier
                if argument_tier_in_scope == "1":

                    if bool_comment_is_question \
                            and bool_comment_is_question_on_tier_1 \
                            and bool_comment_is_not_from_thread_author:

                        amount_of_questions += 1

                        # Check whether that iterated comment is answered by the host
                        answer_is_from_thread_author = check_if_comment_is_answer_from_thread_author(
                            author_of_thread, comment_acutal_id, comments_cursor)

                        # Whenever the answer to that comment is from the author
                        if answer_is_from_thread_author["question_Answered_From_Host"] is True:

                            answer_time_stamp_iama_host = answer_is_from_thread_author["time_Stamp_Answer"]

                            # Adds the calculated answer time to a local list
                            answer_time_iama_host_in_seconds = calculate_time_difference(
                                comment_time_stamp,
                                answer_time_stamp_iama_host
                            )

                            # Contains the amount of upvotes of a question which has been answered by the iama host
                            # with the reaction time of the iama host in seconds
                            dict_upvotes_response_time = {
                                "comment_upvotes": comment_upvotes,
                                "answer_time_host": answer_time_iama_host_in_seconds
                            }

                            amount_of_upvotes_reaction_time.append(dict_upvotes_response_time)

                            amount_of_questions_answered += 1

                    # Skip that comment
                    else:
                        continue

                # Whenever the scope lies on any other tier except tier 1
                elif argument_tier_in_scope == "x":

                    # If the posted comment is a question and is not from the thread author and is not on Tier 1
                    if bool_comment_is_question \
                            and bool_comment_is_question_on_tier_1 is False \
                            and bool_comment_is_not_from_thread_author is True:

                        amount_of_questions += 1

                        # Check whether that iterated comment is answered by the host
                        answer_is_from_thread_author = check_if_comment_is_answer_from_thread_author(
                            author_of_thread, comment_acutal_id, comments_cursor)

                        # Whenever the answer to that comment is from the author
                        if answer_is_from_thread_author["question_Answered_From_Host"] is True:

                            answer_time_stamp_iama_host = answer_is_from_thread_author["time_Stamp_Answer"]

                            # Adds the calculated answer time to a local list
                            answer_time_iama_host_in_seconds = calculate_time_difference(
                                comment_time_stamp,
                                answer_time_stamp_iama_host
                            )

                            # Contains the amount of upvotes of a question which has been answered by the iama host
                            # with the reaction time of the iama host in seconds
                            dict_upvotes_response_time = {
                                "comment_upvotes": comment_upvotes,
                                "answer_time_host": answer_time_iama_host_in_seconds
                            }

                            amount_of_upvotes_reaction_time.append(dict_upvotes_response_time)

                            amount_of_questions_answered += 1

                    # Skip that comment
                    else:
                        continue

                # Whenever the scope lies on all tiers (any tier)
                else:

                    if bool_comment_is_question and bool_comment_is_not_from_thread_author is True:

                        amount_of_questions += 1

                        # Check whether that iterated comment is answered by the host
                        answer_is_from_thread_author = check_if_comment_is_answer_from_thread_author(
                            author_of_thread, comment_acutal_id, comments_cursor)

                        # Whenever the answer to that comment is from the author
                        if answer_is_from_thread_author["question_Answered_From_Host"] is True:
                            answer_time_stamp_iama_host = answer_is_from_thread_author["time_Stamp_Answer"]

                            # Adds the calculated answer time to a local list
                            answer_time_iama_host_in_seconds = calculate_time_difference(
                                comment_time_stamp,
                                answer_time_stamp_iama_host
                            )

                            # Contains the amount of upvotes of a question which has been answered by the iama host
                            # with the reaction time of the iama host in seconds
                            dict_upvotes_response_time = {
                                "comment_upvotes": comment_upvotes,
                                "answer_time_host": answer_time_iama_host_in_seconds
                            }

                            amount_of_upvotes_reaction_time.append(dict_upvotes_response_time)

                            amount_of_questions_answered += 1

                    # Skip that comment
                    else:
                        continue

            # Whenever a comment has been deleted or has, somehow, null values in it.. do not process it
            else:
                continue

    # Whenever some questions have been asked and they have received an answer
    if amount_of_questions != 0 and amount_of_questions_answered != 0:

        # Returns the dictionary containing uptimes of comments and the hosts response time
        return amount_of_upvotes_reaction_time

    # Whenever no questions have been asked at all !
    else:
        return None


def print_data_to_commandline(list_to_be_processed):
    answer_time_host_all_questions = []
    answer_time_host_only_positive_questions_with_0 = []
    answer_time_host_only_negative_questions = []

    comments_votes_score_all_questions = []
    comments_votes_score_only_positive_questions_with_0 = []
    comments_votes_score_only_negative_questions = []

    amount_all_questions = 0
    amount_only_positive_questions_with_0 = 0
    amount_only_negative_questions = 0

    for i, val in enumerate(list_to_be_processed):
        for j, val_2 in enumerate(val):

            answer_time_host_all_questions.append(float((val_2.get("answer_time_host"))))
            comments_votes_score_all_questions.append(float((val_2.get("comment_upvotes"))))
            amount_all_questions += 1

            if (int(val_2.get("comment_upvotes"))) >= 0:
                answer_time_host_only_positive_questions_with_0.append(float((val_2.get("answer_time_host"))))
                comments_votes_score_only_positive_questions_with_0.append(float((val_2.get("comment_upvotes"))))
                amount_only_positive_questions_with_0 += 1

            if (int(val_2.get("comment_upvotes"))) < 0:
                answer_time_host_only_negative_questions.append(float((val_2.get("answer_time_host"))))
                comments_votes_score_only_negative_questions.append(float((val_2.get("comment_upvotes"))))
                amount_only_negative_questions += 1

    print("-- >>> " + str(year_actually_in_progress) + " on tier" + str(argument_tier_in_scope))
    print("-- ALL QUESTIONS --")
    print("Amount of answered questions, by iama host, in total: " + str(amount_all_questions))
    print("Average response time iAMA host in seconds: " + str(np.mean(answer_time_host_all_questions)))
    print("Average answered question vote score: " + str(np.mean(comments_votes_score_all_questions)))
    print("Pearson Ro correlation upvotes <-> response time iAMA host: " +
                                    str(pearsonr(
                                        answer_time_host_all_questions, comments_votes_score_all_questions)[0]))
    print("P-value correlation upvotes <-> response time iAMA host: " +
                                    str(pearsonr(
                                        answer_time_host_all_questions, comments_votes_score_all_questions)[1]))
    print("-----------")

    print("-- ONLY POSITIVE QUESTIONS with 0 --")
    print("Amount of answered questions, by iama host, in total: " + str(amount_only_positive_questions_with_0))
    print("Average response time iAMA host in seconds: " +
                                    str(np.mean(answer_time_host_only_positive_questions_with_0)))
    print("Average answered question vote score: " + str(np.mean(comments_votes_score_only_positive_questions_with_0)))
    print("Pearson Ro correlation upvotes <-> response time iAMA host: " +
                                    str(pearsonr(answer_time_host_only_positive_questions_with_0,
                                                 comments_votes_score_only_positive_questions_with_0)[0]))
    print("P-value correlation upvotes <-> response time iAMA host: " +
                                    str(pearsonr(answer_time_host_only_positive_questions_with_0,
                                                 comments_votes_score_only_positive_questions_with_0)[1]))
    print("-----------")

    print("-- ONLY NEGATIVE QUESTIONS --")
    print("Amount of answered questions, by iama host, in total: " + str(amount_only_negative_questions))
    print("Average response time iAMA host in seconds: " +
                                    str(np.mean(answer_time_host_only_negative_questions)))
    print("Average answered question vote score: " + str(np.mean(comments_votes_score_only_negative_questions)))
    print("Pearson Ro correlation upvotes <-> response time iAMA host: " +
                                    str(pearsonr(answer_time_host_only_negative_questions,
                                                 comments_votes_score_only_negative_questions)[0]))
    print("P-value correlation upvotes <-> response time iAMA host: " +
                                    str(pearsonr(answer_time_host_only_negative_questions,
                                                 comments_votes_score_only_negative_questions)[1]))
    print("-----------")
    print("-----------")
    print("")


def plot_generated_data():
    """Plots the data which is to be generated

    1. This method plots the data which has been calculated before by using 'matplotlib.pyplot-library'
    2. In dependence of the chosen time unit the values will be seperated in either minutes or hours

    Args:
        -
    Returns:
        -
    """

    # Contains all answered questions with their upvotes and response time by the iama host
    # This is also the y axis limiter of the graph, which is to be plotted

    # Defines the highest y value so the y axis gets scaled correctly
    highest_y_value = 0

    x_values = []
    y_values = []

    text_pearson = 'Pearson-Korrelationskoeffizient: \t \t'.expandtabs()
    text_p_value = ' p-Wert: \t \t \t \t \t \t \t'.expandtabs()

    # Whenever the given time argument is minutes..
    if argument_plot_time_unit.lower() in "minutes" or argument_plot_time_unit.lower() in "minuten":

        for i, val in enumerate(list_To_Be_Plotted):
            for j, val_2 in enumerate(val):

                temp_answer_time_host = val_2.get("answer_time_host") / 60
                temp_amount_upvotes = val_2.get("comment_upvotes")

                x_values.append(temp_answer_time_host)
                y_values.append(temp_amount_upvotes)

                if val_2.get("comment_upvotes") > highest_y_value:
                    highest_y_value = val_2.get("comment_upvotes")

        plt.title('Zusammenhang zwischen der Voteanzahl einer Frage und dessen Antwortzeit' +
                  ' durch den iAMA Host in Minuten' +
                  ' auf der Ebene "' +
                  str(argument_tier_in_scope) +
                  '"' +
                  '\n' +
                  '\n' +
                  text_pearson +
                  "%.4f" % pearsonr(x_values, y_values)[0] +
                  '\n' +
                  text_p_value +
                  "%.4f" % pearsonr(x_values, y_values)[1]
                  )
        plt.xlabel('Antworzeit in Minuten')

    else:
        for i, val in enumerate(list_To_Be_Plotted):
            for j, val_2 in enumerate(val):

                temp_answer_time_host = val_2.get("answer_time_host") / 3600
                temp_amount_upvotes = val_2.get("comment_upvotes")

                x_values.append(temp_answer_time_host)
                y_values.append(temp_amount_upvotes)

                if val_2.get("comment_upvotes") > highest_y_value:
                    highest_y_value = val_2.get("comment_upvotes")

        plt.title('Zusammenhang zwischen der Voteanzahl einer Frage und dessen Antwortzeit' +
                  'durch den iAMA Host in Stunden' +
                  ' auf der Ebene "' +
                  str(argument_tier_in_scope) +
                  '"' +
                  '\n' +
                  '\n' +
                  text_pearson +
                  "%.4f" % pearsonr(x_values, y_values)[0] +
                  '\n' +
                  text_p_value +
                  "%.4f" % pearsonr(x_values, y_values)[1]
                  )
        plt.xlabel('Antworzeit in Stunden')

    if argument_plot_x_limiter == 0:
        plt.xlim(0, len(y_values))
    else:
        plt.xlim(0, argument_plot_x_limiter)
        plt.ylim(0, highest_y_value)

    # Plots the appropriate bar within the graph
    plt.ylabel('Anzahl Votes pro beantworteter Frage')
    plt.plot(x_values, y_values, 'ro')
    plt.show()


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Necessary variables and scripts are here

# Contains the year which is given as an argument
argument_year_beginning = 0

# Contains the year which will be processed at the moment
year_actually_in_progress = 0

# Contains the year which is given as argument
argument_year_ending = 0

# Contains the tiers which will be in scope for the calculation
argument_tier_in_scope = ""

# Contains the time unit in which the graphs will be plotted later on
argument_plot_time_unit = ""

# Contains the amount of x elements the plotted graph should be limited to
argument_plot_x_limiter = 0

# The mongo client, necessary to connect to mongoDB
mongo_DB_Client_Instance = None

# The data base instance for the threads
mongo_DB_Threads_Instance = None

# Contains all collection names of the thread database
mongo_DB_Thread_Collection = None

# The data base instance for the comments
mongo_DB_Comments_Instance = None

# Will contain all analyzed time information for threads & comments
list_To_Be_Plotted = []
# SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSHIT
global_thread_list = []

# Data which will be given to plotly bar chart library
data_to_give_plotly = []

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Methods which are to be called are here

# Executes necessary checks
check_script_arguments()

# Initializes the mongoDB with the arguments given via command line
initialize_mongo_db_parameters(argument_year_beginning)

# Starts the data generation process, writes csv files and plots that processed data
start_data_generation_for_analysis()

# Plots a pie chart containing the tier question distribution
# plot_generated_data()
