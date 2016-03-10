import collections               # Necessary to sort collections alphabetically
import matplotlib.pyplot as plt  # Necessary to plot graphs with the data calculated
from pymongo import MongoClient  # Necessary to make use of MongoDB
import numpy as np               # Necessary for mean calculation

# The mongo client, necessary to connect to mongoDB
mongo_DB_Client_Instance = MongoClient('localhost', 27017)

# The data base instance for the threads
mongo_DB_Threads_Instance_2016 = mongo_DB_Client_Instance.iAMA_Reddit_Threads_2016

# Contains all collection names of the thread database
mongo_DB_Thread_Collection_2016 = mongo_DB_Threads_Instance_2016.collection_names()

# The data base instance for the comments
mongo_DB_Comments_Instance_2016 = mongo_DB_Client_Instance.iAMA_Reddit_Comments_2016

# Will contain all analyzed time information for threads & comments
list_To_Be_Plotted = []

# Calculates the distribution of tier 1 questions in contrast to questions
# which are not tier 1 in percent


def calculate_percentage_distribution(
        amount_of_tier_1_questions,
        amount_of_tier_x_questions):

    full_percent = amount_of_tier_1_questions + amount_of_tier_x_questions
    percentage_tier_1 = (amount_of_tier_1_questions / full_percent) * 100
    percentage_tier_x = 100 - percentage_tier_1

    dict_to_be_returned = {
        "percentage_tier_1": percentage_tier_1,
        "percentage_tier_x": percentage_tier_x
    }

    return dict_to_be_returned

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

# Calculates the amount of Tier 1 questions in contrast to the other Tiers


def amount_of_tier_1_questions_percentage(id_of_thread, author_of_thread):
    # print ("Processsing : " + str(id_of_thread) + " ... author: " + str(author_of_thread))

    # Makes the global comments instance locally available here
    global mongo_DB_Comments_Instance_2016

    comments_collection = mongo_DB_Comments_Instance_2016[id_of_thread]
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
                # thread author and is on Tier 1
                if bool_comment_is_question \
                        and bool_comment_is_question_on_tier_1 \
                        and bool_comment_is_not_from_thread_author:

                    amount_of_tier_1_questions += 1

                # If the postet comment is a question and is not from the from
                # the thread author and is on any other level except Tier 1
                elif bool_comment_is_question \
                        and bool_comment_is_not_from_thread_author:

                    amount_of_tier_x_questions += 1

            # Whenever a comment has been deleted or has, somehow, null values
            # in it.. do not process it
            else:
                continue

    # Checks if there has been done some calculation or not
    if (amount_of_tier_x_questions != 0) \
            and (amount_of_tier_1_questions != 0):

        dict_to_be_returned_percentage_time = calculate_percentage_distribution(
            amount_of_tier_1_questions, amount_of_tier_x_questions)
        dict_to_be_returned_percentage_time = collections.OrderedDict(
            sorted(dict_to_be_returned_percentage_time.items()))
        return dict_to_be_returned_percentage_time

    # Whenever there were no tier X questions asked.. so all questions
    # remained on tier 1
    else:
        print(
            "Thread '" +
            str(id_of_thread) +
            "' will not be included in the calculation because there are no questions on any tier greater than tier 1")
        return None

# Generates the data which will be analyzed later on


def generate_data_to_analyze():
    for j, val in enumerate(mongo_DB_Thread_Collection_2016):

        # Skips the system.indexes-table which is automatically created by
        # mongodb itself
        if not val == "system.indexes":
            # References the actual iterated thread
            temp_thread = mongo_DB_Threads_Instance_2016[val]

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

# Plots the data of the question distribution for that year


def plot_the_generated_data_percentage_mean():

    # Will contain the amount of questions which are not tier 1 questions
    list_of_tier_x_values = []

    # Iterates over every value and gets the tier_X value
    for i, val in enumerate(list_To_Be_Plotted):
        list_of_tier_x_values.append(val.get("percentage_tier_x"))

    # Contains the amount of questions which are asked, but not on tier 1
    percentage_mean_of_tier_x = np.mean(list_of_tier_x_values)

    # Prints the average percentage amount of Tier X questions
    print("Percentage of questions on Tier_1: " +
          str(100 - percentage_mean_of_tier_x) + " %")
    print("Percentage of questions on Tier_X: " +
          str(percentage_mean_of_tier_x) + " %")

    plt.figure()

    # The slices will be ordered and plotted counter-clockwise.
    labels = ['Ebene 1', 'Andere Ebene']
    colors = ['yellowgreen', 'gold']
    values = [100 - percentage_mean_of_tier_x, percentage_mean_of_tier_x]

    patches, texts = plt.pie(values, colors=colors, startangle=90, shadow=True)
    plt.pie(values, colors=colors, autopct='%.2f%%')

    plt.legend(patches, labels, loc="upper right")
    plt.title('iAMA 2016 - Ø Verteilung von Fragen in Threadhierarchie')

    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

# Generates the data which will be plotted later on
generate_data_to_analyze()

# Plots a pie chart containing the tier 1 question distribution
plot_the_generated_data_percentage_mean()
