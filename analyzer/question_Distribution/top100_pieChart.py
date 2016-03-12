# Tutorials used within this class:
# 1. (12.03.2016 @ 16:53) -
# https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-values-of-the-dictionary-in-python

import collections                  # Necessary to sort collections alphabetically
import matplotlib.pyplot as plt     # Necessary to plot graphs with the data calculated
import datetime                     # Necessary to do time calculation
import sys                          # Necessary to use script arguments
from pymongo import MongoClient     # Necessary to make use of MongoDB


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
    mongo_DB_Threads_Instance = mongo_DB_Client_Instance['iAMA_Reddit_Threads_' + argument_year]
    mongo_DB_Thread_Collection = mongo_DB_Threads_Instance.collection_names()
    mongo_DB_Comments_Instance = mongo_DB_Client_Instance['iAMA_Reddit_Comments_' + argument_year]


def check_script_arguments():
    """Checks if enough and correct arguments have been given to run this script adequate

    1. It checks in the first instance if enough arguments have been given
    2. Afterwards it fills 'argument_year' with the first argument (str) and 'argument_sorting' with a boolean value,
        by previously parsing and checking that value.

    Args:
        -
    Returns:
        -
    """

    global argument_year, argument_sorting

    # Whenever not enough arguments were given
    if len(sys.argv) <= 2:
        print("Not enough arguments were given...")
        print("Terminating script now!")
        sys.exit()

    else:

        # Simple bool checker
        bool_checker = ['true', 'True', '1', 'yes', 'Yes', 'ja', 'Ja']

        # Parses the first argument to the variable
        argument_year = str(sys.argv[1])

        # Whenever the second argument is in the bool_checker list
        if sys.argv[2] in bool_checker:
            argument_sorting = True
        else:
            argument_sorting = False


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


def calculate_answered_question_upvote_correlation(id_of_thread, author_of_thread, thread_creation_date):
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

                # Calculation of time since thread has been started can only happen here, because of previous checks
                dict_result["time_since_thread_started"] = \
                    calculate_time_difference(thread_creation_date, comment_time_stamp),

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


def generate_data_to_analyze():
    """Generates the data which will be analyzed

    1. This method iterates over every thread
        1.1. It filters if that iterated thread is an iAMA-request or not
            1.1.1. If yes: this thread gets skipped and the next one will be processed
            1.1.2. If no: this thread will be processed
    2. If the thread gets processed it will receive an ordered dictionary containing information about every question
        whether it has been answered or not
    3. This ordered dictionary will be applied to a global list, which will be processed after wards for the generation
        of plots

    Args:
        -
    Returns:
        -
    """

    print("Generating data now...")
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

            returned_value = calculate_answered_question_upvote_correlation(
                val, temp_thread_author, temp_thread_creation_date
            )

            # Value could be none if it has i.E. no values
            if returned_value is not None:
                list_To_Be_Plotted.append(returned_value)


def prepare_and_print_data_to_be_plotted():
    """Prepares data and prints data into the command line

    1. This method prepares the data, in kind of sorting and counting amount of questions not being answered
    2. Afterwards it prints, in dependency of the second argument given of this script, whether the
        TOP or WORST 100 questions have been answered or not

    Args:
        -
    Returns:
        amount_of_questions_not_answered (int) : The amount of questions which have not been answered
    """

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
    # In dependence of given sort parameter..
    new_list = sorted(all_comments, key=lambda k: k['question_ups'], reverse=argument_sorting)

    print("---- Printing top 100 comments now")

    # Iterates over that generated sorted and counts the amount of questions which have not been answered
    for item in new_list[0:100]:
        print(
            "Has Question been answered ?: " +
            str(item.get("question_answered")) +

            "| ID-Thread: " +
            str(item.get("id_thread")) +

            "| ID-Question: " +
            str(item.get("id_question")) +

            "| Amount of question upvotes: " +
            str(item.get("question_ups")) +

            "| Time (sec) since thread has started: " +
            str(item.get("time_since_thread_started")) +

            "| Link to thread: https://www.reddit.com/r/IAma/" +
            str(item.get("id_thread"))
            )

        if item.get("question_answered") is False:
            amount_of_questions_not_answered += 1

    print("------------------------------")
    return amount_of_questions_not_answered


def plot_generated_data(amount_of_questions_not_answered):
    """Plots the data which is to be generated

    1. This method plots the data which has been calculated before by using 'matplotlib.pyplot-library'

    Args:
        amount_of_questions_not_answered (int): The amount of questions which have not been answered.
    Returns:
        -
    """

    plt.figure()
    labels = ['Nicht beantwortet', 'Beantwortet']
    colors = ['yellowgreen', 'gold']
    values = [amount_of_questions_not_answered, 100 - amount_of_questions_not_answered]

    patches, texts = plt.pie(values, colors=colors, startangle=90, shadow=True)
    plt.pie(values, colors=colors, autopct='%.2f%%')

    plt.legend(patches, labels, loc="upper right")

    if argument_sorting is True:
        plt.title('iAMA ' + argument_year + ' - Beantwortung der TOP 100 Fragen')
    else:
        plt.title('iAMA ' + argument_year + ' - Beantwortung der WORST 100 Fragen')

    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    plt.tight_layout()
    plt.show()


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Necessary variables and scripts are here

# Contains the year which is given as an argument
argument_year = ""

# Contains the information wether the first top 100 (highest upvotes) or the last 100 (lowest upvotes [negative]
# should be calculated
argument_sorting = bool

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
generate_data_to_analyze()

# Sorts, prepares the data and finally plots it
plot_generated_data(prepare_and_print_data_to_be_plotted())
