import collections                  # Necessary to sort collections alphabetically
import matplotlib.pyplot as plt     # Necessary to plot graphs with the data calculated
from pymongo import MongoClient     # Necessary to make use of MongoDB
import numpy as np               # Necessary for mean calculation

# The mongo client, necessary to connect to mongoDB
mongo_DB_Client_Instance = MongoClient('localhost', 27017)

# The data base instance for the threads
mongo_DB_Threads_Instance_2012 = mongo_DB_Client_Instance.iAMA_Reddit_Threads_2012

# Contains all collection names of the thread database
mongo_DB_Thread_Collection_2012 = mongo_DB_Threads_Instance_2012.collection_names()

# The data base instance for the comments
mongo_DB_Comments_Instance_2012 = mongo_DB_Client_Instance.iAMA_Reddit_Comments_2012

# Will contain all analyzed time information for threads & comments
list_To_Be_Plotted = []

# Calculates how many tier X questions have been answered


def calculate_percentage_distribution(
        amount_of_tier_x_questions,
        amount_of_tier_x_questions_answered):

    percentage_tier_x_answered = (
        amount_of_tier_x_questions_answered / amount_of_tier_x_questions) * 100
    percentage_tier_x_not_answered = (100 - percentage_tier_x_answered)

    dict_to_be_returned = {
        "percentage_tier_x_answered": percentage_tier_x_answered,
        "percentage_tier_x_not_answered": percentage_tier_x_not_answered
    }

    return dict_to_be_returned

# Checks whether the thread host has answered a given question


def check_if_comment_is_answer_from_thread_author(
        author_of_thread, comment_acutal_id, comments_cursor):

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
                return True
            else:
                return False
        else:
            return False

# Checks whether the postet comment is not from the thread creator


def check_if_comment_is_not_from_thread_author(
        author_of_thread, comment_author):

    if author_of_thread != comment_author:
        return True
    else:
        return False

# Checks wether the question is on Tier-1 Hierarchy or not


def check_if_comment_is_on_tier_1(comment_parent_id):

    if "t3_" in comment_parent_id:
        return True
    else:
        return False

# Could be expanded later on, if checking for question mark is not enough


def check_if_comment_is_a_question(given_string):

    if "?" in given_string:
        return True
    else:
        return False

# Calculates the amount of questions on tier x which have been answered by
# the iAMA host


def amount_of_tier_x_questions_answered_by_host(
        id_of_thread, author_of_thread):
    # print ("Processsing : " + str(id_of_thread) + " ... author: " + str(author_of_thread))

    # Makes the global comments instance locally available here
    global mongo_DB_Comments_Instance_2012

    comments_collection = mongo_DB_Comments_Instance_2012[id_of_thread]
    comments_cursor = comments_collection.find()

    amount_of_tier_x_questions = 0
    amount_of_tier_x_questions_answered = 0

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

            # Whenever some values are not None.. (Values can be null / None,
            # whenever they have been deleted)
            if comment_text is not None \
                    and comment_author is not None \
                    and comment_parent_id is not None:

                bool_comment_is_question = check_if_comment_is_a_question(
                    comment_text)
                bool_comment_is_question_on_tier_1 = check_if_comment_is_on_tier_1(
                    comment_parent_id)
                bool_comment_is_not_from_thread_author = check_if_comment_is_not_from_thread_author(
                    author_of_thread, comment_author)

                # If the posted comment is a question and is not from the
                # thread author and is on Tier X
                if bool_comment_is_question \
                        and bool_comment_is_question_on_tier_1 is False \
                        and bool_comment_is_not_from_thread_author is True:

                    amount_of_tier_x_questions += 1

                    # Check whether that iterated comment is answered by the
                    # host
                    answer_is_from_thread_author = check_if_comment_is_answer_from_thread_author(
                        author_of_thread, comment_acutal_id, comments_cursor)

                    # Whenever the answer to that comment is from the author
                    # (boolean == True)
                    if answer_is_from_thread_author:
                        amount_of_tier_x_questions_answered += 1

                # Skip that comment
                else:
                    continue

            # Whenever a comment has been deleted or has, somehow, null values
            # in it.. do not process it
            else:
                continue

    # Checks if there has been done some calculation or not
    if amount_of_tier_x_questions != 0:

        dict_to_be_returned_percentage_answered_questions = calculate_percentage_distribution(
            amount_of_tier_x_questions, amount_of_tier_x_questions_answered)
        dict_to_be_returned_percentage_answered_questions = collections.OrderedDict(
            sorted(dict_to_be_returned_percentage_answered_questions.items()))
        return dict_to_be_returned_percentage_answered_questions

    # Whenever there were no tier X questions asked.. so all questions
    # remained on tier 1
    else:
        print(
            "Thread '" +
            str(id_of_thread) +
            "' will not be included in the calculation because there are no questions asked on tier X")
        return None


# Generates the data which will be analyzed later on
def generate_data_to_analyze():
    for j, val in enumerate(mongo_DB_Thread_Collection_2012):

        # Skips the system.indexes-table which is automatically created by
        # mongodb itself
        if not val == "system.indexes":
            # References the actual iterated thread
            temp_thread = mongo_DB_Threads_Instance_2012[val]

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

            returned_value = amount_of_tier_x_questions_answered_by_host(
                val, temp_thread_author)

            # Value could be none if it has i.E. no values
            if returned_value is not None:
                list_To_Be_Plotted.append(returned_value)

# Plots the data of the question distribution for that year


def plot_the_generated_data_percentage_mean():

    # Will contain the amount of questions which are not tier x questions
    list_of_tier_x_answered_questions = []

    # Iterates over every value and gets the tier_X value
    for i, val in enumerate(list_To_Be_Plotted):
        list_of_tier_x_answered_questions.append(
            val.get("percentage_tier_x_answered"))

    # Contains the amount of questions which have been answered by the
    # iAMA-Host an tier x in percentage
    percentage_mean_of_tier_x_answered_questions = np.mean(
        list_of_tier_x_answered_questions)

    # Prints the average percentage amount of Tier X questions
    print("Percentage of questions answered by iAMA-Host on Tier_X: " +
          str(percentage_mean_of_tier_x_answered_questions) + " %")
    print("Percentage of questions NOT answered by iAMA-Host on on Tier_X: " +
          str(100 - percentage_mean_of_tier_x_answered_questions) + " %")

    plt.figure()

    # The slices will be ordered and plotted counter-clockwise.
    labels = ['Beantwortet', 'Unbeantwortet']
    colors = ['yellowgreen', 'gold']
    values = [percentage_mean_of_tier_x_answered_questions,
              100 - percentage_mean_of_tier_x_answered_questions]

    patches, texts = plt.pie(values, colors=colors, startangle=90, shadow=True)
    plt.pie(values, colors=colors, autopct='%.2f%%')

    plt.legend(patches, labels, loc="upper right")
    plt.title(
        'iAMA 2012 - Ø Quote von beantworteten Fragen auf Ebene X durch iAMA-Host')

    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

# Generates the data which will be plotted later on
generate_data_to_analyze()

# Plots a pie chart containing the tier x question distribution
plot_the_generated_data_percentage_mean()
