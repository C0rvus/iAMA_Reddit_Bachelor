import collections               # Necessary to sort collections alphabetically
import matplotlib.pyplot as plt  # Necessary to plot graphs with the data calculated
import numpy as np               # Necessary for mean calculation
import sys                       # Necessary to use script arguments
from pymongo import MongoClient  # Necessary to make use of MongoDB


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
    2. Then necessary variables will be filled with appropriate values

    Args:
        -
    Returns:
        -
    """

    global argument_year, argument_tier_in_scope

    # Whenever not enough arguments were given
    if len(sys.argv) <= 1:
        print("Not enough arguments were given...")
        print("Terminating script now!")
        sys.exit()
    else:
        # Parses the first argument to the variable
        argument_year = str(sys.argv[1])
        argument_tier_in_scope = str(sys.argv[2]).lower()


def calculate_percentage_distribution(amount_of_questions, amount_of_questions_answered):
    """Checks whether both strings are equal or not

    1. This method simply checks wether both strings match each other or not.
        I have built this extra method to have a better overview in the main code..

    Args:
        amount_of_questions (int) : The amount of questions which have been asked at all
        amount_of_questions_answered (int) : The amount of questions which have been answered
    Returns:
        dict_to_be_returned (dict): A dictionary containing
            1. The amount of questions answered as int
            2. The amount of questions which have not been answered
         answered that given question)
    """

    percentage_answered = (
                              amount_of_questions_answered / amount_of_questions) * 100
    percentage_not_answered = (100 - percentage_answered)

    dict_to_be_returned = {
        "percentage_answered": percentage_answered,
        "percentage_not_answered": percentage_not_answered
    }

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
        comment_actual_id:  (str) : The id of the actually processed comment
        comments_cursor (Cursor) : The cursor which shows to the amount of comments which can be iterated
    Returns:
        True (bool): Whenever the strings do not match
        False (bool): Whenever the strings do match
         answered that given question)
         :param
    """

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
                        check_comment_parent_id == comment_actual_id):
                return True
            else:
                return False
        else:
            return False


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
def amount_of_questions_answered_by_host(id_of_thread, author_of_thread):
    """Generates the data which will be analyzed

    1. It iterates over every comment and
         1.1. checks if the iterated comment is a question
         1.2. checks if the iterated comment has been posted on tier 1 level
         1.3. checks if that comment is from the iAMA-Host himself or not
    2. Now the distribution of questions answered / not answered will be calculated depending on the commited tier level
        3. A dictionary containing the amounts in percentage will be returned

    id_of_thread (str) : Contains the id of the processed thread
    author_of_thread (str) : Contains the iAMA-Hosts name

    Returns:
    dict_to_be_returned_percentage_answered_questions (dict) : Containing the percentage amount of questions
    which have been answered and which have not been answered
     """

    # Makes the global comments instance locally available here
    global mongo_DB_Comments_Instance

    comments_collection = mongo_DB_Comments_Instance[id_of_thread]
    comments_cursor = comments_collection.find()

    amount_of_questions = 0
    amount_of_questions_answered = 0

    # Iterates over every comment within that thread
    for collection in comments_cursor:

        # Whenever the iterated comment was created by user "AutoModerator"
        # skip it
        if (collection.get("author")) != "AutoModerator":

            # References the text of the comment
            comment_text = collection.get("body")
            comment_author = collection.get("author")
            comment_parent_id = collection.get("parent_id")
            comment_actual_id = collection.get("name")

            # Whenever some values are not None.. (Values can be null / None whenever they have been deleted)
            if comment_text is not None \
                    and comment_author is not None \
                    and comment_parent_id is not None:

                bool_comment_is_question = check_if_comment_is_a_question(comment_text)
                bool_comment_is_question_on_tier_1 = check_if_comment_is_on_tier_1(comment_parent_id)
                bool_comment_is_not_from_thread_author = check_if_comment_is_not_from_thread_author(
                    author_of_thread, comment_author)

                # Whenever the scope lies on the first tier
                if argument_tier_in_scope == "1":

                    # If the posted comment is a question and is not from the thread author and is on tier 1
                    if bool_comment_is_question is True \
                            and bool_comment_is_question_on_tier_1 is True \
                            and bool_comment_is_not_from_thread_author is True:

                        amount_of_questions += 1

                        # Check whether that iterated comment is answered by the host
                        answer_is_from_thread_author = check_if_comment_is_answer_from_thread_author(
                            author_of_thread, comment_actual_id, comments_cursor)

                        # Whenever the answer to that comment is from the author
                        if answer_is_from_thread_author is True:
                            amount_of_questions_answered += 1

                    # Skip that comment
                    else:
                        continue

                # Whenever the scope lies on any other tier except tier 1
                elif argument_tier_in_scope == "x":

                    # If the posted comment is a question and is not from the thread author and is on tier 1
                    if bool_comment_is_question is True \
                            and bool_comment_is_question_on_tier_1 is False \
                            and bool_comment_is_not_from_thread_author is True:

                        amount_of_questions += 1

                        # Check whether that iterated comment is answered by the host
                        answer_is_from_thread_author = check_if_comment_is_answer_from_thread_author(
                            author_of_thread, comment_actual_id, comments_cursor)

                        # Whenever the answer to that comment is from the author
                        if answer_is_from_thread_author is True:
                            amount_of_questions_answered += 1

                    # Skip that comment
                    else:
                        continue

                # Whenever the scope lies on all tiers (any tier)
                else:

                    # If the posted comment is a question and is not from the thread author
                    if bool_comment_is_question is True \
                            and bool_comment_is_not_from_thread_author is True:

                        amount_of_questions += 1

                        # Check whether that iterated comment is answered by the host
                        answer_is_from_thread_author = check_if_comment_is_answer_from_thread_author(
                            author_of_thread, comment_actual_id, comments_cursor)

                        # Whenever the answer to that comment is from the author (boolean == True)
                        if answer_is_from_thread_author is True:
                            amount_of_questions_answered += 1

                    # Skip that comment
                    else:
                        continue

            # Whenever a comment has been deleted or has, somehow, null values in it.. do not process it
            else:
                continue

    # Checks if there were questions asked at all...
    if amount_of_questions != 0:

        dict_to_be_returned_percentage_answered_questions = calculate_percentage_distribution(
            amount_of_questions, amount_of_questions_answered)

        dict_to_be_returned_percentage_answered_questions = collections.OrderedDict(
            sorted(dict_to_be_returned_percentage_answered_questions.items()))

        return dict_to_be_returned_percentage_answered_questions

    # Whenever there were no questions asked at all - skip that thread
    else:
        return None


def generate_data_to_be_analyzed():
    """Generates the data which will be analyzed

    1. This method iterates over every thread
        1.1. It filters if that iterated thread is an iAMA-request or not
            1.1.1. If yes: this thread gets skipped and the next one will be processed
            1.1.2. If no: this thread will be processed
    2. If the thread gets processed it will receive the amount of questions answered
    3. This value will be added to a global list and will be plotted later on
    Args:
        -
    Returns:
        -
    """

    print("Generating data now...")

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

            # Removes iAMA-Requests out of our selection
            if "request" in temp_thread_title.lower() \
                    and "as requested" not in temp_thread_title.lower() \
                    and "by request" not in temp_thread_title.lower() \
                    and "per request" not in temp_thread_title.lower() \
                    and "request response" not in temp_thread_title.lower():
                continue

            returned_value = amount_of_questions_answered_by_host(val, temp_thread_author)

            # Value could be none if it has i.E. no values
            if returned_value is not None:
                list_To_Be_Plotted.append(returned_value)


def plot_the_generated_data():
    """Plots the data which is to be generated

    1. This method plots the data which has been calculated before by using 'matplotlib.pyplot-library'
    2. Depending on the committed year and tier scope the title will be adapted appropriate

    Args:
        -
    Returns:
        -
    """

    # Will contain the amount of questions which have been answered
    list_of_tier_any_answered_questions = []

    # Iterates over every value and gets the necessary value
    for i, val in enumerate(list_To_Be_Plotted):
        list_of_tier_any_answered_questions.append(
            val.get("percentage_answered")
        )

    # Contains the amount of questions which have been answered by the iAMA-Host as arithmetic mean
    percentage_mean_of_tier_any_answered_questions = np.mean(
        list_of_tier_any_answered_questions)

    # Prints the average percentage amount questions answered by the iAMA Host
    print("Percentage of questions answered by iAMA-Host: " +
          str(percentage_mean_of_tier_any_answered_questions) + " %")

    print("Percentage of questions NOT answered by iAMA-Host: " +
          str(100 - percentage_mean_of_tier_any_answered_questions) + " %")

    plt.figure()

    # Contains the labels, used for the plot
    labels = [
        'Beantwortet', 'Unbeantwortet'
    ]

    # Contains the colors, used for the plot
    colors = [
        'yellowgreen',
        'gold'
    ]

    # Contains the values, used for the plot
    values = [
        percentage_mean_of_tier_any_answered_questions,
        100 - percentage_mean_of_tier_any_answered_questions
    ]

    # Defines the way the patches and texts will be printed
    patches, texts = plt.pie(
        values,
        colors=colors,
        startangle=90,
        shadow=True
    )

    # Defines what values the pie chart should contain
    plt.pie(
        values,
        colors=colors,
        autopct='%.2f%%'
    )

    # Defines the design of the plots legend
    plt.legend(
        patches,
        labels,
        loc="upper right"
    )

    # Whenever the commited tier is tier 1
    if argument_tier_in_scope == "1":
        plt.title(
            'iAMA ' +
            argument_year +
            ' - Ø Quote beantworteter Fragen durch den iAMA-Host \n' +
            ' auf Ebene ' + str(argument_tier_in_scope)
        )

    # Whenever the commited tier is tier x
    elif argument_tier_in_scope == "x":
        plt.title(
            'iAMA ' +
            argument_year +
            ' - Ø Quote beantworteter Fragen durch den iAMA-Host \n' +
            ' auf allen Ebenen, ausschließlich Ebene 1'
        )

    # Whenever the commited tier neither 1 or x
    else:
        plt.title(
            'iAMA ' +
            argument_year +
            ' - Ø Quote beantworteter Fragen durch den iAMA-Host \n' +
            ' auf allen Ebenen'
        )

    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')

    # Automatically adjusts the subplot params
    plt.tight_layout()

    # Show that plot
    plt.show()


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Necessary variables and scripts are here

# Contains the year which is given as an argument
argument_year = ""

# Contains the tiers which will be in scope for the calculation
argument_tier_in_scope = ""

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
generate_data_to_be_analyzed()

# Plots a pie chart containing a distribution of questions answered by hosts on all tiers
plot_the_generated_data()
