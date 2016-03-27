# Tutorials used within this class:
# 1. (12.03.2016 @ 16:53) -
# https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-values-of-the-dictionary-in-python
# 2. (26.03.2016 @ 15:40) -
# https://stackoverflow.com/questions/14693646/writing-to-csv-file-python
# 3. (26.03.2016 @ 18:03) -
# https://stackoverflow.com/questions/12400256/python-converting-epoch-time-into-the-datetime
# 4. (26.03.2016 @ 18:43) -
# http://effbot.org/pyfaq/how-do-i-copy-an-object-in-python.htm
# 5. (27.03.2016 @ 15:28) -
# http://matplotlib.org/examples/pylab_examples/alignment_test.html
# 6. (27.03.2016 @ 16:54) -
# https://stackoverflow.com/questions/12750355/python-matplotlib-figure-title-overlaps-axes-label-when-using-twiny
# 7. (27.03.2016 @ 17:51) -
# https://stackoverflow.com/questions/14737599/mongoengine-serverstatus
# 8. (27.03.2016 @ 19:13) -
# https://stackoverflow.com/questions/33661080/python-matplotlib-plot-text-will-not-align-left
# 9. (27.03.2016 @ 19:50) -
# https://stackoverflow.com/questions/1093322/how-do-i-check-what-version-of-python-is-running-my-script

import collections                  # Necessary to sort collections alphabetically
import datetime                     # Necessary to create the year out of the thread utc
import matplotlib.pyplot as plt     # Necessary to plot graphs with the data calculated
import sys                          # Necessary to use script arguments
import csv                          # Necessary to write data to csv files
import os                           # Necessary to get the name of currently processed file
import copy                         # Necessary to copy value of the starting year - needed for correct csv file name
import time                         # Necessary to calculate the current time
from pymongo import MongoClient     # Necessary to make use of MongoDB
import pymongo                      # Necessary to get information about the database


def initialize_mongo_db_parameters():
    """Instantiates all necessary variables for the correct usage of the mongoDB-Client

    Args:
        -
    Returns:
        -
    """

    global mongo_DB_Client_Instance
    global mongo_DB_Threads_Instance
    global mongo_DB_Thread_Collection
    global mongo_DB_Comments_Instance

    mongo_DB_Client_Instance = MongoClient('localhost', 27017)
    mongo_DB_Threads_Instance = mongo_DB_Client_Instance['iAMA_Reddit_Threads_' + str(argument_year_beginning)]
    mongo_DB_Thread_Collection = mongo_DB_Threads_Instance.collection_names()
    mongo_DB_Comments_Instance = mongo_DB_Client_Instance['iAMA_Reddit_Comments_' + str(argument_year_beginning)]


def check_script_arguments():
    """Checks if enough and correct arguments have been given to run this script adequate

    1. It checks in the first instance if enough arguments have been given
    2. Afterwards it fills 'argument_year_beginning' with the first argument (str) and 'argument_sorting' with
        a boolean value, by previously parsing and checking that value.

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
    time_difference_in_seconds = int((
        answer_time_iama_host_converted_for_subtraction -
        comment_time_converted_for_subtraction
    ).total_seconds())

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


def generate_data_now():
    """Generates the data which will be analyzed later on

    1. This method iterates over every thread
        1.1. It filters if that iterated thread is an iAMA-request or not
            1.1.1. If yes: this thread gets skipped and the next one will be processed
            1.1.2. If no: this thread will be processed
    2. If the thread gets processed it will receive an ordered dictionary containing information about every question
        whether it has been answered or not
    3. This ordered dictionary will be appended to a global list, which will be processed afterwards for the generation
        of plots

    Args:
        -
    Returns:
        -
    """

    print("Generating data for year " + str(argument_year_beginning) + " now...")
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
                list_To_Be_Plotted.append(returned_value)


def start_data_generation_for_analysis():
    """Starts the data processing by swichting through the years

    1. Triggers the data generation process and moves forward within the years

    Args:
        -
    Returns:
        -
    """

    global argument_year_beginning

    # Copies the value of the beginning year, because it will be changed due to moving forward within the years
    temp_starting_year = copy.copy(argument_year_beginning)

    while argument_year_beginning != argument_year_ending:
        generate_data_now()
        argument_year_beginning += 1
        initialize_mongo_db_parameters()

    if argument_year_beginning == argument_year_ending:
        generate_data_now()
        argument_year_beginning += 1
        initialize_mongo_db_parameters()

    # After all operations have finished reset the starting year - this is necessary to have a correct and
    # not progressional file name
    argument_year_beginning = temp_starting_year


def prepare_and_print_data_to_be_plotted():
    """Prepares data and prints data into the command line

    1. This method prepares the data, in kind of sorting and counting amount of questions not being answered
    2. Afterwards it executes the write_csv_and_count_unanswered - method to write an csv file containing the top /
        worst amount of questions (parsed as arguments)
    3. Then it returns the number of unanswered questions, necessary for graph plotting

    Args:
        -
    Returns:
        write_csv_and_count_unanswered (int) : The amount of questions which have not been answered
    """

    # Will contain all comments later on
    all_comments = []

    # Iterates over every ordered list
    for i, val in enumerate(list_To_Be_Plotted):

        # Iterates over the sub elements within that iterated object
        for j, val_2 in enumerate(val):

            # breaks comment hierarchy und creates a flat list of all comments
            all_comments.append(val_2)

    # Creates a "sorted" which contains all comments of that year, sorted by upvotes in descending order
    # In dependence of given sort parameter..
    new_list = sorted(all_comments, key=lambda k: k['question_ups'], reverse=argument_sorting)

    # Defines the amount of the top X questions (by upvotes) which have not been answered
    return write_csv_and_count_unanswered(new_list)


def write_csv_and_count_unanswered(list_with_comments):
    """Creates a csv file containing all necessary information and calculates the amount of unanswered questions

    1. This method iterates over the top / worst X comments
        1.1. By iterating: all necessary information will be written into the csv file
        1.2. By iterating: the amount of unanswered questions will be counted
    2. After iterating the amount of unanswered questions will be returned, which is necessary for graph plotting

    Args:
        list_with_comments (list): Contains all comments from the year
    Returns:
        write_csv_and_count_unanswered (int) : The amount of questions which have not been answered
    """

    print("---- Writing top / worst " + str(argument_amount_of_top_quotes) + " comments now")

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
                    '.csv'

    with open(file_name_csv, 'w', newline='') as fp:
        csv_writer = csv.writer(fp, delimiter=',')

        # The heading of the csv file.. sep= is needed, otherwise Microsoft Excel would not recognize seperators..
        data = [['sep=,'],
                ['Year',
                 'Has question been answered?',
                 'Thread-ID',
                 'Question-ID',
                 'Question-Upvotes',
                 'Thread lifespan (seconds)',
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


def plot_generated_data(amount_of_questions_not_answered):
    """Plots the data which is to be generated

    1. This method plots the data which has been calculated before by using 'matplotlib.pyplot-library'

    Args:
        amount_of_questions_not_answered (int): The amount of questions which have not been answered.
    Returns:
        -
    """

    # Connect to admin (internal) mongoDB for mongoDB-Server information
    mongo_db_admin_database = mongo_DB_Client_Instance.admin

    mono = {'family' : 'monospace'}

    plt.figure(figsize=(10, 6))
    labels = ['Nicht beantwortet', 'Beantwortet']
    colors = ['indianred', 'yellowgreen']
    values = [amount_of_questions_not_answered, argument_amount_of_top_quotes - amount_of_questions_not_answered]

    # The absolute amount of numbers
    absolute_amount = [values[0], values[1]]

    patches, texts = plt.pie(values, colors=colors, startangle=90, shadow=True)
    plt.pie(values, labels=absolute_amount, colors=colors, autopct='%.2f%%')

    plt.legend(patches, labels, loc="upper right")

    if argument_sorting is True:
        plt.title('Beantwortung der TOP ' +
                  str(argument_amount_of_top_quotes) +
                  ' iAMA Fragen von' +
                  '\n ' +
                  str(argument_year_beginning) +
                  ' bis ' +
                  str(argument_year_ending),
                  bbox={'facecolor': '0.8', 'pad': 5},
                  y=1.08
                  )
    else:
        plt.title('Beantwortung der WORST ' +
                  str(argument_amount_of_top_quotes) +
                  ' iAMA Fragen von' +
                  '\n ' +
                  str(argument_year_beginning) +
                  ' bis ' +
                  str(argument_year_ending),
                  bbox={'facecolor': '0.8', 'pad': 5},
                  y=1.08
                  )

    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    plt.tight_layout()

    time_now_date = time.strftime("%d.%m.%Y")
    time_now_time = time.strftime("%H:%M:%S")

    text_to_print_box_1 = "MongoDB connection:" + "\n" + \
                "MongoDB version:" + "\n" + \
                "MongoDB storage engine:" + "\n" + \
                "\n" + \
                "IAMA-db creation date:" + "\n" + \
                "\n" + \
                "Python version:" + "\n" + \
                "Pymongo version:" + "\n" + \
                "\n" + \
                "Plot creation date:" + "\n" + \
                "Plot creation time:"

    text_to_print_box_2 = str(MongoClient.HOST) + ":" + str(MongoClient.PORT) + "\n" + \
                str(mongo_db_admin_database.command("serverStatus")["version"]) + "\n" + \
                str(mongo_db_admin_database.command("serverStatus")["storageEngine"]['name']) + "\n" + \
                "\n" + \
                "17.02.2016" + "\n" + \
                "\n" + \
                str(sys.version[:5]) + "\n" + \
                str(pymongo.version) + "\n" + \
                "\n" + \
                time_now_date + "\n" + \
                time_now_time

    ax = plt.gca()

    plt.text(0.0, 0.0, text_to_print_box_1, transform=ax.transAxes, fontsize=8, fontdict=mono, ha='left', va='bottom')
    plt.text(0.25, 0.0, text_to_print_box_2, transform=ax.transAxes, fontsize=8, fontdict=mono, ha='right', va='bottom')

    plt.show()


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Necessary variables and scripts are here

# Contains the year which is given as an argument
argument_year_beginning = 0

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

# Will contain all analyzed time information for threads & comments
list_To_Be_Plotted = []


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Methods which are to be called are here

# Executes necessary checks
check_script_arguments()

# Initializes the mongoDB with the arguments given via command line
initialize_mongo_db_parameters()

# Generates the data which will be plotted later on
start_data_generation_for_analysis()

# Sorts, prepares the data and finally plots it
plot_generated_data(prepare_and_print_data_to_be_plotted())
