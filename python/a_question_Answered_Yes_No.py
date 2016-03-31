# Tutorials used within this class:
# 1. (12.03.2016 @ 16:53) -
# https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-values-of-the-dictionary-in-python
# 2. (26.03.2016 @ 15:40) -
# https://stackoverflow.com/questions/14693646/writing-to-csv-file-python
# 3. (26.03.2016 @ 18:03) -
# https://stackoverflow.com/questions/12400256/python-converting-epoch-time-into-the-datetime
# 4. (26.03.2016 @ 18:43) -
# http://effbot.org/pyfaq/how-do-i-copy-an-object-in-python.htm


import collections                  # Necessary to sort collections alphabetically
import datetime                     # Necessary to create the year out of the thread utc
import sys                          # Necessary to use script arguments
import csv                          # Necessary to write data to csv files
import os                           # Necessary to get the name of currently processed file
import copy                         # Necessary to copy value of the starting year - needed for correct csv file name
from pymongo import MongoClient     # Necessary to make use of MongoDB
# noinspection PyUnresolvedReferences
from PlotlyBarChart import PlotlyBarChart   # Necessary to plot the data into a stacked bar chart


def initialize_mongo_db_parameters(actually_processed_year):
    """Instantiates all necessary variables for the correct usage of the mongoDB client

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


def check_script_arguments():
    """Checks if enough and correct arguments have been given to run this script adequate

    1. It checks in the first instance if enough arguments have been given
    2. Afterwards it will fill the instance variables ap

    Args:
        -
    Returns:
        -
    """

    global argument_year_beginning, argument_year_ending, argument_sorting, argument_amount_of_top_quotes

    # Whenever not enough arguments were given
    if len(sys.argv) <= 4:
        print("Not enough arguments were given...")
        print("Terminating script now!")
        sys.exit()

    else:
        # Simple bool checker
        bool_checker = ['top', 'best']

        # Parses the first argument to the variable
        argument_year_beginning = int(sys.argv[1])
        argument_year_ending = int(sys.argv[2])

        # Whenever the second argument is in the bool_checker list
        if sys.argv[3] in bool_checker:
            argument_sorting = True
        else:
            argument_sorting = False

        argument_amount_of_top_quotes = int(sys.argv[4])


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
    time_difference_in_seconds = int((answer_time_iama_host_converted_for_subtraction -
                                      comment_time_converted_for_subtraction).total_seconds())

    return time_difference_in_seconds


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


def process_answered_questions_within_thread(id_of_thread, author_of_thread, thread_creation_date):
    """ Checks whether an iterated question has been answered by the iama host or not

    1. This method checks at first whether an iterated comment contains values (e.g. is not none)
        1.1. If not: That comment will be skipped / if no comment is remaining None will be returned
        1.2. If yes: That comment will be processed
    2. Now it will be checked whether that iterated comment is a question or not
    3. Afterwards it will be checked wether that comment is a comment from the iAMA Host or not
        3.1. If this is not the case the next comment will be processed
    4. Whenever that processed comment is a question and not (!!) from the thread author:
        amount_of_tier_any_questions (int) will be increased by one
    5. Now it will be checked whether that comment has a comment ( answer ) below it which is from the iAMA-host
        5.1. If yes: amount_of_tier_any_questions_answered (int) will be increased by one and the dictionary, which
            is to be returned will be filled with values
        5.2. If no: the dictionary, which is to be returned will be filled with values

    Args:
        id_of_thread (str) : Contains the id of the thread which is to be iterated
        author_of_thread (str) : Contains the name of the thread author
        thread_creation_date (str): Contains the time
    Returns:
        amount_of_questions_not_answered (int) : The amount of questions which have not been answered
    """

    # Makes the global comments instance locally available here
    global mongo_DB_Comments_Instance

    comments_collection = mongo_DB_Comments_Instance[id_of_thread]
    comments_cursor = comments_collection.find()

    amount_of_results = []

    amount_of_tier_any_questions = 0
    amount_of_tier_any_questions_answered = 0

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

            # A dictionary containing the results necessary for the calculation here
            dict_result = {
                "year": 0,
                "id_thread": str(id_of_thread),
                "id_question": comment_acutal_id,
                "question_ups": comment_upvotes,
                "time_since_thread_started": 0,
                "question_answered": bool
            }

            # Whenever some values are not None.. (Values can be null / None, whenever they have been deleted)
            if comment_text is not None \
                    and comment_author is not None \
                    and comment_parent_id is not None:

                # Converts the timestamp to float, parses it to strings and cut anything away except the last 4 chars
                floated_time = float(comment_time_stamp)
                converted_time = datetime.datetime.fromtimestamp(floated_time).strftime('%c')
                converted_time_length = len(converted_time)
                converted_time_length -= 4

                dict_result["year"] = converted_time[converted_time_length:]

                # Calculation of time since thread has been started can only happen here, because of previous checks
                dict_result["time_since_thread_started"] = \
                    calculate_time_difference(thread_creation_date, comment_time_stamp)

                bool_comment_is_question = check_if_comment_is_a_question(comment_text)

                bool_comment_is_not_from_thread_author = check_if_comment_is_not_from_thread_author(
                    author_of_thread, comment_author)

                # If the posted comment is a question and is not from the thread author
                if bool_comment_is_question and bool_comment_is_not_from_thread_author:

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
        return None


def start_data_generation_for_analysis():
    """Starts the data processing by swichting through the years

    1. Triggers the data generation process and moves forward within the years
        1.1. By moving through the years a csv file will be created for every year
        1.2. At the end a csv file will be generated containing all questions of all years, sorted
        1.3. Additionally an interactive chart will be plotted

    Args:
        -
    Returns:
        -
    """

    global argument_year_beginning, data_to_give_plotly, year_actually_in_progress, question_information_list

    # Copies the value of the beginning year, because it will be changed due to moving forward within the years
    year_actually_in_progress = copy.copy(argument_year_beginning)

    # Contains the summary / total amount of all questions for all years..
    # This is necessary to print out a csv file containing all (!) questions within
    all_years_whole_list = []

    # If checking is necessary for correct list formatation
    if argument_sorting is True:
        data_to_give_plotly.append(["q_answered_y_n", "top"])
    else:
        data_to_give_plotly.append(["q_answered_y_n", "worst"])

    # As long as the ending year has not been reached
    while year_actually_in_progress != argument_year_ending:

        # Starts retrieving and checking that data
        generate_data_now()

        # Sorts the questions corresponding to the sorting parameters given
        list_of_sorted_questions = sort_questions(question_information_list)

        # Contains the contains for every year
        all_years_whole_list.append(list_of_sorted_questions)

        # Due writing a csv file for that actually processed year the amount of not answered questions will be answered
        amount_of_unanswered_questions = write_csv_and_count_unanswered(list_of_sorted_questions)

        data_to_give_plotly.append([year_actually_in_progress,
                                    argument_amount_of_top_quotes - amount_of_unanswered_questions,
                                    amount_of_unanswered_questions])

        # Removes the values to be able to generate the csv file for every year
        question_information_list = []

        # Progresses in the year, necessary for onward year calculation
        year_actually_in_progress += 1

        # Reinitializes the mongodb with new year parameter here
        initialize_mongo_db_parameters(year_actually_in_progress)

    # Will be entered whenever the last year is beeing processed
    if year_actually_in_progress == argument_year_ending:

        # Starts retrieving and checking that data
        generate_data_now()

        # Sorts the questions corresponding to the sorting parameters given
        list_of_sorted_questions = sort_questions(question_information_list)

        # Contains the contains for every year
        all_years_whole_list.append(list_of_sorted_questions)

        # Due writing a csv file for that actually processed year the amount of not answered questions will be answered
        amount_of_unanswered_questions = write_csv_and_count_unanswered(list_of_sorted_questions)

        data_to_give_plotly.append([year_actually_in_progress,
                                    argument_amount_of_top_quotes - amount_of_unanswered_questions,
                                    amount_of_unanswered_questions])

        # Removes the values to be able to generate the csv file for every year
        question_information_list = []

    # Creates an csv file with questions for all years.. so all years are compacted into a single file!
    create_question_list_containing_all_years(all_years_whole_list)

    # Plots the graph
    plot_generated_data()


def generate_data_now():
    """Generates the data which will be written into csv and plotted later on

    1. This method iterates over every thread
        1.1. It filters if that iterated thread is an iAMA-request or not
            1.1.1. If yes: this thread gets skipped and the next one will be processed
            1.1.2. If no: this thread will be processed
    2. If the thread gets processed it will receive an ordered dictionary containing information about every question
        whether it has been answered or not
    3. This ordered dictionary will be appended to a global list, which will be processed afterwards for the generation
        of plots and csv files

    Args:
        -
    Returns:
        -
    """

    print("Generating data for year " + str(year_actually_in_progress) + " now...")
    # noinspection PyTypeChecker
    for j, val in enumerate(mongo_DB_Thread_Collection):
        # Skips the system.indexes-table which is automatically created by mongodb itself
        if not val == "system.indexes":
            # References the actual iterated thread
            temp_thread = mongo_DB_Threads_Instance[val]

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

            returned_value = process_answered_questions_within_thread(
                val, temp_thread_author, temp_thread_creation_date
            )

            # Value could be none if it has i.E. no values
            if returned_value is not None:
                question_information_list.append(returned_value)


def sort_questions(list_which_is_to_be_sorted):
    """Sorts a list of questions for a year, depending on the upvotes

    1. This method prepares the data, in kind of sorting and counting amount of questions not being answered
    2. It also returns the number of unanswered questions, necessary for chart plotting

    Args:
        list_which_is_to_be_sorted (list) : The list you want to sort regarding the sorting arguments give on execution
    Returns:
        questions_sorted (list) : The amount of questions, sorted on upvotes
    """

    # Will contain all comments later on
    all_comments = []

    # Iterates over every ordered list
    for i, val in enumerate(list_which_is_to_be_sorted):

        # Iterates over the sub elements within that iterated object
        for j, val_2 in enumerate(val):

            # breaks comment hierarchy und creates a flat list of all comments
            all_comments.append(val_2)

    # Creates a "sorted" which contains all comments of that year, sorted by upvotes in descending order
    # In dependence of given sort parameter..
    questions_sorted = sorted(all_comments, key=lambda k: k['question_ups'], reverse=argument_sorting)

    # Defines the amount of the top X questions (by upvotes) which have not been answered
    return questions_sorted


def create_question_list_containing_all_years(list_with_comments_per_years):
    global year_actually_in_progress

    # Overwrites the variable, because the final csv file gets written
    year_actually_in_progress = "ALL"

    # List will be sorted here, so we do not have to sort it within excel or some other software
    whole_list_of_years_sorted = sort_questions(list_with_comments_per_years)

    # This variable is senseless, because we won't use it, but the execution of the method creates the csv we want!
    # noinspection PyUnusedLocal
    senseless_number = write_csv_and_count_unanswered(whole_list_of_years_sorted)


def write_csv_and_count_unanswered(list_with_comments):
    """Creates a csv file containing all necessary information and calculates the amount of unanswered questions

    1. This method iterates over the top / worst X comments
        1.1. By iterating: all necessary information will be written into the csv file
        1.2. By iterating: the amount of unanswered questions will be counted
    2. After iterating the amount of unanswered questions will be returned, which is necessary for graph plotting

    Args:
        list_with_comments (list): Contains all comments from the year
    Returns:
        amount_of_questions_not_answered (int) : The amount of questions which have not been answered
    """

    print("---- Writing top / worst " + str(argument_amount_of_top_quotes) + " comments now")
    # Empty print line here for a more beautiful console output
    print("")

    amount_of_questions_not_answered = 0

    file_name_csv = str(os.path.basename(__file__))[0:len(os.path.basename(__file__)) - 3] + \
                    '_' + \
                    str(argument_year_beginning) + \
                    '_until_' + \
                    str(argument_year_ending) + \
                    '_' + \
                    str(sys.argv[3]) + \
                    '_' + \
                    str(argument_amount_of_top_quotes) + \
                    '_' + \
                    str(year_actually_in_progress) + \
                    '.csv'

    with open(file_name_csv, 'w', newline='') as fp:
        csv_writer = csv.writer(fp, delimiter=',')

        # The heading of the csv file.. sep= is needed, otherwise Microsoft Excel would not recognize seperators..
        data = [['sep=,'],
                ['Year',
                 'Has question been answered?',
                 'Thread id',
                 'Question id',
                 'Question ups',
                 'Question birth time since thread started (sec)',
                 'Link to Thread']]

        # Iterates over that generated sorted and counts the amount of questions which have not been answered
        for item in list_with_comments[0:argument_amount_of_top_quotes]:
            temp_list = [str(item.get("year")),
                         str(item.get("question_answered")),
                         str(item.get("id_thread")),
                         str(item.get("id_question")),
                         str(item.get("question_ups")),
                         str(item.get("time_since_thread_started")),
                         'https://www.reddit.com/r/IAma/' + str(item.get("id_thread"))
                         ]
            data.append(temp_list)

            # Additionally checks whether a question has been answered or not
            if item.get("question_answered") is False:
                amount_of_questions_not_answered += 1

        # Writes data into the csv file
        csv_writer.writerows(data)

    return amount_of_questions_not_answered


def plot_generated_data():
    """Plots the data which is to be generated

    1. This method plots the data which has been calculated before by using Pltoly-Framework within a self written class

    Args:
        -
    Returns:
        -
    """

    PlotlyBarChart().main_method(data_to_give_plotly)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Necessary variables and scripts are here

# Contains the year which is given as an argument
argument_year_beginning = 0

# Contains the year which will be processed at the moment
year_actually_in_progress = 0

# Contains the year which is given as argument
argument_year_ending = 0

# Contains the information wether the first top X (highest upvotes) or the last X (lowest upvotes [negative]
# should be calculated
argument_sorting = bool

# Contains the amount of questions you will be having respected in plotting your graph and writing the csv data
argument_amount_of_top_quotes = 0


# The mongo client, necessary to connect to mongoDB
mongo_DB_Client_Instance = None

# The data base instance for the threads
mongo_DB_Threads_Instance = None

# Contains all collection names of the thread database
mongo_DB_Thread_Collection = None

# The data base instance for the comments
mongo_DB_Comments_Instance = None


# Will contain temporarily contain all analyzed question information
question_information_list = []

# Contains the data which are necessary for plotly
# <editor-fold desc="Description of data object plotly needs">
# Structure as follows:
# [ "analyze_type", "analyze_setting"}, [year, answered, unanswered], [year, answered, unanswered], ... ]
# i.e. [["q_answered_y_n", "top"],
#       [2009, 900, 1536],
#       [2010, 500, 500],
#       [2011, 300, 700]
#       ]
# </editor-fold>
data_to_give_plotly = []


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Methods which are to be called are here

# Executes necessary checks
check_script_arguments()

# Initializes the mongoDB with the arguments given via command line
initialize_mongo_db_parameters(argument_year_beginning)

# Starts the data generation process, writes csv files and plots that processed data
start_data_generation_for_analysis()
