# Sources used within this class:
# 1. (26.03.2016 @ 18:03) -
# https://stackoverflow.com/questions/12400256/python-converting-epoch-time-into-the-datetime
# 2. (26.03.2016 @ 18:43) -
# http://effbot.org/pyfaq/how-do-i-copy-an-object-in-python.htm
# 3. (26.03.2016 @ 15:40) -
# https://stackoverflow.com/questions/14693646/writing-to-csv-file-python

import datetime                     # Necessary to do time calculation
import sys                          # Necessary to use script arguments
import os                           # Necessary to get the name of currently processed file
import csv                          # Necessary to write data to csv files
import copy                         # Necessary to copy value of the starting year - needed for correct csv file name
from pymongo import MongoClient     # Necessary to make use of MongoDB
import numpy as np                  # Necessary for mean calculation
# noinspection PyUnresolvedReferences
from PlotlyBarChart_5_Bars import PlotlyBarChart5Bars


def check_script_arguments():
    """Checks if enough and correct arguments have been given to run this script adequate

    1. It checks in the first instance if enough arguments have been given
    2. Then necessary variables will be filled with appropriate values

    Args:
        -
    Returns:
        -
    """

    global year_actually_in_progress, argument_year_beginning, argument_year_ending, \
        argument_tier_in_scope, argument_plot_time_unit

    # Whenever not enough arguments were given
    if len(sys.argv) <= 3:
        print("Not enough arguments were given...")
        print("Terminating script now!")
        sys.exit()
    else:
        argument_year_beginning = int(sys.argv[1])
        argument_year_ending = int(sys.argv[2])
        argument_tier_in_scope = str(sys.argv[3])
        argument_plot_time_unit = str(sys.argv[4]).lower()


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

    global year_actually_in_progress, data_to_give_plotly, global_thread_list, list_To_Be_Plotted

    # Copies the value of the beginning year, because it will be changed due to moving forward within the years
    year_actually_in_progress = copy.copy(argument_year_beginning)

    data_to_give_plotly.append(["t_iama_comment_time", argument_plot_time_unit, argument_tier_in_scope])

    # As long as the ending year has not been reached
    while year_actually_in_progress != argument_year_ending:

        generate_data_to_be_analyzed()

        write_csv_data(list_To_Be_Plotted)

        dict_to_add_to_plotly = prepare_data_for_graph()

        data_to_give_plotly.append([
            int(year_actually_in_progress),
            dict_to_add_to_plotly["first"],
            dict_to_add_to_plotly["second"],
            dict_to_add_to_plotly["third"],
            dict_to_add_to_plotly["fourth"],
            dict_to_add_to_plotly["fifth"],
        ])

        add_thread_list_to_global_list(list_To_Be_Plotted)

        list_To_Be_Plotted = []

        year_actually_in_progress += 1

        # Reinitializes the mongodb with new year parameter here
        # noinspection PyTypeChecker
        initialize_mongo_db_parameters(year_actually_in_progress)

    # Will be entered whenever the last year is beeing processed
    if year_actually_in_progress == argument_year_ending:

        generate_data_to_be_analyzed()

        write_csv_data(list_To_Be_Plotted)

        dict_to_add_to_plotly = prepare_data_for_graph()

        data_to_give_plotly.append([
            int(year_actually_in_progress),
            dict_to_add_to_plotly["first"],
            dict_to_add_to_plotly["second"],
            dict_to_add_to_plotly["third"],
            dict_to_add_to_plotly["fourth"],
            dict_to_add_to_plotly["fifth"],
        ])

        add_thread_list_to_global_list(list_To_Be_Plotted)

        list_To_Be_Plotted = []

        # Value setting is necessary for correct file writing
        year_actually_in_progress = "ALL"

    # Writes a global csv file containing information about all threads
    write_csv_data(global_thread_list)

    print(data_to_give_plotly)

    # Plots the graph
    plot_generated_data()


def prepare_data_for_graph():
    """Sorts and prepares data for graph plotting

    Args:
        -
    Returns:
        -
    """

    dict_time_amount_counter = {
        "first": 0,
        "second": 0,
        "third": 0,
        "fourth": 0,
        "fifth": 0
    }

    # Minutes
    if argument_plot_time_unit == "minutes":
        divider = 60

        # Iterates over every element and checks if that value is between some given values
        for i, val in enumerate(list_To_Be_Plotted):

            value = val.get("Thread_iAMA_host_average_comment_time")

            if (value / divider) <= 14:
                dict_time_amount_counter["first"] += 1

            elif ((value / divider) > 14) \
                    and ((value / 60) <= 29):
                dict_time_amount_counter["second"] += 1

            elif ((value / divider) > 29) \
                    and ((value / 60) <= 59):
                dict_time_amount_counter["third"] += 1

            elif ((value / divider) > 59) \
                    and ((value / 60) <= 119):
                dict_time_amount_counter["fourth"] += 1

            elif (value / divider) >= 120:
                dict_time_amount_counter["fifth"] += 1

    # Hours
    elif argument_plot_time_unit == "hours":
        divider = 3600

        # Iterates over every element and checks if that value is between some given values
        for i, val in enumerate(list_To_Be_Plotted):

            value = val.get("Thread_iAMA_host_average_comment_time")

            if (value / divider) <= 1:
                dict_time_amount_counter["first"] += 1

            elif ((value / divider) > 1) \
                    and ((value / divider) <= 5):
                dict_time_amount_counter["second"] += 1

            elif ((value / divider) > 5) \
                    and ((value / divider) <= 10):
                dict_time_amount_counter["third"] += 1

            elif ((value / divider) > 10) \
                    and ((value / divider) <= 23):
                dict_time_amount_counter["fourth"] += 1

            elif (value / divider) >= 24:
                dict_time_amount_counter["fifth"] += 1

    # Days
    else:
        divider = 86400

        # Iterates over every element and checks if that value is between some given values
        for i, val in enumerate(list_To_Be_Plotted):

            value = val.get("Thread_iAMA_host_average_comment_time")

            if (value / divider) <= 1:
                dict_time_amount_counter["first"] += 1

            elif ((value / divider) > 1) and \
                    ((value / divider) <= 4):
                dict_time_amount_counter["second"] += 1

            elif ((value / divider) > 4) and \
                    ((value / divider) <= 8):
                dict_time_amount_counter["third"] += 1

            elif ((value / divider) > 8) and \
                    ((value / divider) <= 13):
                dict_time_amount_counter["fourth"] += 1

            elif (value / divider) >= 14:
                dict_time_amount_counter["fifth"] += 1

    return dict_time_amount_counter


def add_thread_list_to_global_list(list_to_append):
    """Adds all elements of for the current year into a global list. This global list will be written into a csv file
    later on

    1. This method simply checks wether both strings match each other or not.
        I have built this extra method to have a better overview in the main code..

    Args:
        list_to_append (list) : The list which will be iterated over and which elements will be added to the global list
    Returns:
        -
    """

    global global_thread_list

    for item in list_to_append:
        global_thread_list.append(item)


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

            returned_value = calculate_ar_mean_answer_time_for_questions(val, temp_thread_author)

            # Value could be none if it has i.E. no values
            if returned_value is not None:
                list_To_Be_Plotted.append(returned_value)


def calculate_ar_mean_answer_time_for_questions(id_of_thread, author_of_thread):
    """Calculates the arithmetic mean of the answer time by the iama host in minutes

    In dependence of the given tier argument (second argument) the processing of tiers will be filtered

    Args:
        id_of_thread (str): The id of the thread which is actually processed. (Necessary for checking if a question
            lies on tier 1 or any other tier)
        author_of_thread (str): The name of the thread author. (Necessary for checking if a given answer is from the
            iama host or not)
    Returns:
        Whenever there was a minimum of 1 question asked and 1 answer from the iama host:
            amount_of_answer_times (int) : The amount of the arithmetic mean time of
        Whenever there no questions have been asked for that thread / or no answers were given /
            or all values in the database were null:
            None:   Returns an empty object of the type None
    """

    global mongo_DB_Comments_Instance

    comments_collection = mongo_DB_Comments_Instance[id_of_thread]
    comments_cursor = comments_collection.find()

    temp_thread = mongo_DB_Threads_Instance[id_of_thread]
    temp_thread_ups = temp_thread.find()[0].get("ups")
    temp_thread_downs = temp_thread.find()[0].get("downs")

    amount_of_answer_times = []

    amount_of_comments = 0
    amount_of_questions = 0
    amount_of_questions_answered_by_iama_host = 0

    # Iterates over every comment within that thread
    for collection in comments_cursor:
        # Whenever the iterated comment was created by user "AutoModerator" skip it
        if (collection.get("author")) != "AutoModerator":

            # References the text of the comment
            comment_text = collection.get("body")
            comment_author = collection.get("author")
            comment_parent_id = collection.get("parent_id")
            comment_actual_id = collection.get("name")
            comment_time_stamp = collection.get("created_utc")

            # Whenever some values are not None.. (Values can be null / None, whenever they have been deleted)
            if comment_text is not None \
                    and comment_author is not None \
                    and comment_parent_id is not None:

                amount_of_comments += 1
                bool_comment_is_question = check_if_comment_is_a_question(comment_text)

                bool_comment_is_question_on_tier_1 = check_if_comment_is_on_tier_1(comment_parent_id)

                bool_comment_is_not_from_thread_author = check_if_comment_is_not_from_thread_author(
                    author_of_thread, comment_author)

                # Whenever the scope lies on the first tier
                if argument_tier_in_scope == "1":

                    if bool_comment_is_question is True \
                            and bool_comment_is_question_on_tier_1 is True\
                            and bool_comment_is_not_from_thread_author is True:

                        amount_of_questions += 1

                        # Check whether that iterated comment is answered by the host
                        answer_is_from_thread_author = check_if_comment_is_answer_from_thread_author(
                            author_of_thread, comment_actual_id, comments_cursor)

                        # Whenever the answer to that comment is from the author
                        # (boolean == True)
                        if answer_is_from_thread_author["question_Answered_From_Host"] is True:

                            answer_time_stamp_iama_host = answer_is_from_thread_author["time_Stamp_Answer"]

                            # Adds the calculated answer time to a local list
                            amount_of_answer_times.append(
                                calculate_time_difference(
                                    comment_time_stamp,
                                    answer_time_stamp_iama_host)
                            )

                            amount_of_questions_answered_by_iama_host += 1

                    # Skip that comment
                    else:
                        continue

                # Whenever the scope lies on any other tier except tier 1
                elif argument_tier_in_scope == "x":

                    # If the posted comment is a question and is not from the thread author and is not on Tier 1
                    if bool_comment_is_question is True \
                            and bool_comment_is_question_on_tier_1 is False \
                            and bool_comment_is_not_from_thread_author is True:

                        amount_of_questions += 1

                        # Check whether that iterated comment is answered by the host
                        answer_is_from_thread_author = check_if_comment_is_answer_from_thread_author(
                            author_of_thread, comment_actual_id, comments_cursor)

                        # Whenever the answer to that comment is from the author
                        if answer_is_from_thread_author["question_Answered_From_Host"] is True:
                            answer_time_stamp_iama_host = answer_is_from_thread_author["time_Stamp_Answer"]

                            # Adds the calculated answer time to a local list
                            amount_of_answer_times.append(
                                calculate_time_difference(
                                    comment_time_stamp,
                                    answer_time_stamp_iama_host)
                            )

                            amount_of_questions_answered_by_iama_host += 1

                    # Skip that comment
                    else:
                        continue

                # Whenever the scope lies on all tiers
                else:
                    if bool_comment_is_question is True and bool_comment_is_not_from_thread_author is True:

                        amount_of_questions += 1

                        # Check whether that iterated comment is answered by the host
                        answer_is_from_thread_author = check_if_comment_is_answer_from_thread_author(
                            author_of_thread, comment_actual_id, comments_cursor)

                        # Whenever the answer to that comment is from the author
                        if answer_is_from_thread_author["question_Answered_From_Host"] is True:
                            answer_time_stamp_iama_host = answer_is_from_thread_author["time_Stamp_Answer"]

                            # Adds the calculated answer time to a local list
                            amount_of_answer_times.append(
                                calculate_time_difference(
                                    comment_time_stamp,
                                    answer_time_stamp_iama_host)
                            )

                            amount_of_questions_answered_by_iama_host += 1

                    # Skip that comment
                    else:
                        continue

            # Whenever a comment has been deleted or has, somehow, null values in it.. do not process it
            else:
                continue

    # Whenever some questions have been asked and they have received an answer
    if amount_of_questions != 0 and amount_of_questions_answered_by_iama_host != 0:

        dict_to_be_returned = {
            'Year': str(year_actually_in_progress),
            'Thread_id': str(id_of_thread),
            'Thread_author': str(author_of_thread),
            'Thread_ups': temp_thread_ups,
            'Thread_downs': temp_thread_downs,
            'Thread_num_comments': amount_of_comments,
            'Thread_num_questions': amount_of_questions,
            'Thread_amount_questions_answered_by_iAMA_host': amount_of_questions_answered_by_iama_host,
            'Thread_iAMA_host_average_comment_time': np.mean(amount_of_answer_times)
        }

        # Returns the arithmetic mean of answer time by the iAMA host
        return dict_to_be_returned

    # Whenever no questions have been asked at all !
    else:
        return None


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
            if (check_if_comment_is_not_from_thread_author(
                    author_of_thread,
                    actual_comment_author) == False) and (
                        check_comment_parent_id == comment_actual_id):

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


def write_csv_data(list_with_information):
    """Creates a csv file containing all necessary information about the average comment time of the iama host

    Args:
        list_with_information (list) : Contains various information about thread and comment time
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
                    str(argument_tier_in_scope) + \
                    '_' + \
                    str(year_actually_in_progress) + \
                    '.csv'

    with open(file_name_csv, 'w', newline='') as fp:
        csv_writer = csv.writer(fp, delimiter=',')

        # The heading of the csv file.. sep= is needed, otherwise Microsoft Excel would not recognize seperators..
        data = [['sep=,'],
                ['Year',
                 'Thread id',
                 'Thread author',
                 'Thread ups',
                 'Thread downs',
                 'Thread comments',
                 'Thread questions',
                 'Thread questions answered by iAMA host',
                 'Thread average response time from iAMA host (sec)',
                 'Link to Thread']]

        # Iterates over that generated sorted and counts the amount of questions which have not been answered
        for item in list_with_information:

            temp_list = [str(item.get("Year")),
                         str(item.get("Thread_id")),
                         str(item.get("Thread_author")),
                         str(item.get("Thread_ups")),
                         str(item.get("Thread_downs")),
                         str(item.get("Thread_num_comments")),
                         str(item.get("Thread_num_questions")),
                         str(item.get("Thread_amount_questions_answered_by_iAMA_host")),
                         str(item.get("Thread_iAMA_host_average_comment_time")),
                         'https://www.reddit.com/r/IAma/' + str(item.get("Thread_id"))
                         ]
            data.append(temp_list)

        # Writes data into the csv file
        csv_writer.writerows(data)


def plot_generated_data():
    """Plots the data which is to be generated

    1. This method plots the data which has been calculated before by using Pltoly-Framework within a self written class

    Args:
        -
    Returns:
        -
    """

    PlotlyBarChart5Bars().main_method(data_to_give_plotly)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Necessary variables and scripts are here

# Contains the year which is given as an argument
argument_year_beginning = 0

# Contains the year which is given as an argument
year_actually_in_progress = 0

# Contains the year which is given as argument
argument_year_ending = 0

# Contains the tiers which will be in scope for the calculation
argument_tier_in_scope = ""

# Contains the time unit in which the graphs will be plotted later on
argument_plot_time_unit = ""

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

# Contains all questions of the actually processed year
global_thread_list = []

# Contains the data which are necessary for plotly
# <editor-fold desc="Description of data object plotly needs">
# Structure as follows:
# [ "analyze_type", "analyze_time_setting", "analyze_tier_setting"},
#  [year, first values, second values, third values, fourth values, fifth values],
#  ... ]
# Values can be the amount of minutes between a defined interval..
# [["t_iama_comment_time", "days", "any"],
#                     [2009, 1, 2, 3, 4, 5],
#                     [2010, 6, 7, 2, 3, 4],
#                     [2011, 16, 3, 9, 0, 1]]
# </editor-fold>
data_to_give_plotly = []


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Methods which are to be called are here

# Executes necessary checks
check_script_arguments()

# Initializes the mongoDB with the arguments given via command line
initialize_mongo_db_parameters(argument_year_beginning)

# Starts the data generation process, writes csv files and plots that processed data
start_data_generation_for_analysis()
