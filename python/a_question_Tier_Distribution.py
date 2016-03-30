# Source: http://stackoverflow.com/questions/33448233/python-write-to-text-file-skip-bad-lines
# http://stackoverflow.com/questions/14630288/unicodeencodeerror-charmap-codec-cant-encode-character-maps-to-undefined


import collections               # Necessary to sort collections alphabetically
import sys                       # Necessary to use script arguments
import unicodecsv as csv         # Necessary to write data to csv files
import os                        # Necessary to get the name of currently processed file
import numpy as np               # Necessary for mean calculation
import copy                      # Necessary to copy value of the starting year - needed for correct csv file name
from pymongo import MongoClient  # Necessary to make use of MongoDB
# noinspection PyUnresolvedReferences
from PlotlyBarChart import PlotlyBarChart   # Necessary to plot the data into a stacked bar chart


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
    if len(sys.argv) <= 1:
        print("Not enough arguments were given...")
        print("Terminating script now!")
        sys.exit()

    else:
        # Parses the first argument to the variable
        # Parses the first argument to the variable
        argument_year_beginning = int(sys.argv[1])
        argument_year_ending = int(sys.argv[2])


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


def calculate_percentages_n_amount(amount_of_tier_1_questions, amount_of_tier_x_questions):
    """Checks whether both strings are equal or not

    1. This method simply checks wether both strings match each other or not.
        I have built this extra method to have a better overview in the main code..

    Args:
        amount_of_tier_1_questions (int) : The amount of questions which have been asked at all
        amount_of_tier_x_questions (int) : The amount of questions which have been answered
    Returns:
        dict_to_be_returned (dict): A dictionary containing
            1. The amount of questions answered as int
            2. The amount of questions which have not been answered
         answered that given question)
    """

    full_percent = amount_of_tier_1_questions + amount_of_tier_x_questions
    percentage_tier_1 = (amount_of_tier_1_questions / full_percent) * 100
    percentage_tier_x = 100 - percentage_tier_1

    dict_to_be_returned = {
        "percentage_tier_1": percentage_tier_1,
        "percentage_tier_x": percentage_tier_x,
        "amount_tier_1_questions": amount_of_tier_1_questions,
        "amount_tier_x_questions": amount_of_tier_x_questions,
    }

    return dict_to_be_returned


def check_if_comment_is_on_tier_1(comment_parent_id):
    """Simply checks whether a given string is a question posted on tier 1 or not

    1. This method simply checks whether a question has been posted on tier 1 by looking whether the given
        string contains the substring "t3_" or not
    Args:
        comment_parent_id (str): The string which will be checked for "t3_" appearance in it
    Returns:
        -
    """

    if "t3_" in comment_parent_id:
        return True
    else:
        return False


def check_if_comment_is_a_question(given_string):
    """Simply checks whether a given string is a question or not

    1. This method simply checks whether a question mark exists within that string or not..
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


# noinspection PyIncorrectDocstring
def amount_of_tier_1_questions_percentage(id_of_thread, author_of_thread):
    """Generates the data which will be analyzed

    1. It iterates over every comment and
         1.1. checks if the iterated comment is a question
         1.2. checks if the iterated comment has been posted on tier 1 level
         1.3. checks if that comment is from the iAMA-Host himself or not

    2. Now the distribution of on the tier levels will be calculated
    3. Then a dict will be returned containing the distribution amount of questions on the tier levels in percentage

    id_of_thread (str) : Contains the id of the processed thread
    author_of_thread (str) : Contains the iAMA-Hosts name

    Returns:
    dict_to_be_returned_percentage_answered_questions (dict) : Containing the percentage amount of questions
    on tier 1 and the other tiers
     """

    # Makes the global comments instance locally available here
    global mongo_DB_Comments_Instance, global_question_list

    comments_collection = mongo_DB_Comments_Instance[id_of_thread]
    comments_cursor = comments_collection.find()

    # Contains the amount of questions done on the first level of a thread
    amount_of_tier_1_questions = 0

    # Contains the amount of questions done on every sublevel, except on tier 1
    amount_of_tier_x_questions = 0

    # Iterates over every comment within that thread
    for collection in comments_cursor:
        # Whenever the iterated comment was created by user "AutoModerator"
        # skip it
        if (collection.get("author")) != "AutoModerator":

            # References the text of the comment
            comment_text = collection.get("body")
            comment_author = collection.get("author")
            comment_parent_id = collection.get("parent_id")
            comment_time_stamp = collection.get("created_utc")
            comment_id = collection.get("name")
            comment_ups = collection.get("ups")

            # Whenever some values are not None.. (Values can be null / None whenever they have been deleted)
            if comment_text is not None \
                    and comment_author is not None \
                    and comment_parent_id is not None:

                bool_comment_is_question = check_if_comment_is_a_question(
                    comment_text)
                bool_comment_is_question_on_tier_1 = check_if_comment_is_on_tier_1(
                    comment_parent_id)
                bool_comment_is_not_from_thread_author = check_if_comment_is_not_from_thread_author(
                    author_of_thread, comment_author)

                # If the posted comment is a question and is not from the thread author and is on Tier 1
                if bool_comment_is_question \
                        and bool_comment_is_question_on_tier_1 \
                        and bool_comment_is_not_from_thread_author:

                    amount_of_tier_1_questions += 1

                    temp_dict = {"year": year_actually_in_progress,
                                 "question_time_stamp": comment_time_stamp, "question_author": comment_author,
                                 "question_id": comment_id, "question_ups": comment_ups,
                                 "parent_id": comment_parent_id, "thread_id": str(id_of_thread),
                                 "thread_author": str(author_of_thread), "tier": "1",
                                 "comment_text": comment_text}

                    # Apply that temp_dict to the global list, so we have all questions of that year within that list
                    global_question_list.append(temp_dict)

                # If the postet comment is a question and is not from the from
                # the thread author and is on any other level except Tier 1
                elif bool_comment_is_question \
                        and bool_comment_is_not_from_thread_author:

                    temp_dict = {"year": year_actually_in_progress,
                                 "question_time_stamp": comment_time_stamp, "question_author": comment_author,
                                 "question_id": comment_id, "question_ups": comment_ups,
                                 "parent_id": comment_parent_id, "thread_id": str(id_of_thread),
                                 "thread_author": str(author_of_thread), "tier": "1",
                                 "comment_text": comment_text}

                    # Apply that temp_dict to the global list, so we have all questions of that year within that list
                    global_question_list.append(temp_dict)

                    amount_of_tier_x_questions += 1

            # Whenever a comment has been deleted or has, somehow, null values in it.. do not process it
            else:
                continue

    # Checks if there has been done some calculation or not
    if (amount_of_tier_x_questions != 0) \
            and (amount_of_tier_1_questions != 0):

        dict_to_be_returned_percentage_time = calculate_percentages_n_amount(
            amount_of_tier_1_questions, amount_of_tier_x_questions)

        dict_to_be_returned_percentage_time = collections.OrderedDict(
            sorted(dict_to_be_returned_percentage_time.items()))

        return dict_to_be_returned_percentage_time

    # Whenever there were no tier X questions asked.. so all questions remained on tier 1
    else:
        return None


def start_data_generation_for_analysis():
    global argument_year_beginning, data_to_give_plotly, year_actually_in_progress, list_To_Be_Plotted, \
        global_question_list

    # Copies the value of the beginning year, because it will be changed due to moving forward within the years
    year_actually_in_progress = copy.copy(argument_year_beginning)

    # Contains the summary / total amount of all questions for all years..
    # This is necessary to print out a csv file containing all (!) questions within

    data_to_give_plotly.append(["q_tier_dist", None])

    # As long as the ending year has not been reached
    while year_actually_in_progress != argument_year_ending:

        # Starts retrieving and checking that data
        generate_data_to_be_analyzed()

        # Writes a csv file for the actually processed year
        write_csv()

        # Prepares data for graph / chart plotting later on
        prepare_data_for_graph()

        # Empty both lists
        list_To_Be_Plotted = []
        global_question_list = []

        # Progresses in the year, necessary for onward year calculation
        year_actually_in_progress += 1

        # Reinitializes the mongodb with new year parameter here
        initialize_mongo_db_parameters(year_actually_in_progress)

    # Will be entered whenever the last year is beeing processed
    if year_actually_in_progress == argument_year_ending:

        # Starts retrieving and checking that data
        generate_data_to_be_analyzed()

        # Writes a csv file for the actually processed year
        write_csv()

        # Prepares data for graph / chart plotting later on
        prepare_data_for_graph()

        # Empty both lists
        list_To_Be_Plotted = []
        global_question_list = []

    # Plots the graph
    plot_generated_data()


def write_csv():

    global global_question_list

    print("---- Writing csv containing all questions for year " + str(year_actually_in_progress) + " now")
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

    # We write the file here in binary mode.. therefore only excel is able to correctly display the csv file
    # We must use binary mode, because some comments contain characters which python on windows is not able to process
    # Because I do not want to leave out the question text of this data, I left the comments in
    with open(file_name_csv, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',', encoding='utf-8')

        # The heading of the csv file.. sep= is needed, otherwise Microsoft Excel would not recognize seperators..
        data = [['sep=,'],
                ['Year',
                 'Thread id',
                 'Thread author',
                 'Question time stamp utc (epoch)',
                 'Question author',
                 'Question id',
                 'Question tier',
                 'Question ups',
                 'Question text',
                 'Parent id',
                 'Link to Thread']]
        # Iterates over that generated sorted and counts the amount of questions which have not been answered
        for item in global_question_list:
            temp_list = [str(item.get("year")),
                         str(item.get("thread_id")),
                         str(item.get("thread_author")),
                         str(item.get("question_time_stamp")),
                         str(item.get("question_author")),
                         str(item.get("question_id")),
                         str(item.get("tier")),
                         str(item.get("question_ups")),
                         str(item.get("comment_text")),
                         str(item.get("parent_id")),
                         'https://www.reddit.com/r/IAma/' + str(item.get("thread_id"))
                         ]
            data.append(temp_list)
        # Writes data into the csv file
        csv_writer.writerows(data)


def prepare_data_for_graph():

    # Will contain the amount of questions which are not tier 1 questions
    amount_of_tier_1_questions = 0
    amount_of_tier_x_questions = 0

    for i, val in enumerate(list_To_Be_Plotted):
        amount_of_tier_1_questions += val.get("amount_tier_1_questions")
        amount_of_tier_x_questions += val.get("amount_tier_x_questions")

    # Appends the information for the year to the global list
    data_to_give_plotly.append([year_actually_in_progress, amount_of_tier_1_questions, amount_of_tier_x_questions])


def generate_data_to_be_analyzed():
    """Generates the data which will be analyzed

    1. This method iterates over every thread
        1.1. It filters if that iterated thread is an iAMA-request or not
            1.1.1. If yes: this thread gets skipped and the next one will be processed
            1.1.2. If no: this thread will be processed
    2. If the thread gets processed it will receive the distribution of questions on the tiers
    3. This value will be added to a global list and will be plotted later on
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

            returned_value = amount_of_tier_1_questions_percentage(
                val, temp_thread_author)

            # Value could be none if it has i.E. no values
            if returned_value is not None:
                list_To_Be_Plotted.append(returned_value)


def plot_generated_data():
    """Plots the data which is to be generated


    Args:
        -
    Returns:
        -
    """

    print(data_to_give_plotly)
    PlotlyBarChart().main_method(data_to_give_plotly)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Necessary variables and scripts are here

# Contains the year which is given as an argument
argument_year_beginning = 0

# Contains the year which will be processed at the moment
year_actually_in_progress = 0

# Contains the year which is given as argument
argument_year_ending = 0


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
global_question_list = []

# Contains the data which are necessary for plotly
# <editor-fold desc="Description of data object plotly needs">
# Structure as follows:
# [ "analyze_type", "analyze_setting"}, [year, tier 1, other tier], [year, tier 1, other tier], ... ]
# i.e. [["q_tier_dist", None],
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

# Generates the data which will be plotted later on
# generate_data_to_be_analyzed()

# Plots a pie chart containing the tier 1 question distribution
# plot_the_generated_data()
