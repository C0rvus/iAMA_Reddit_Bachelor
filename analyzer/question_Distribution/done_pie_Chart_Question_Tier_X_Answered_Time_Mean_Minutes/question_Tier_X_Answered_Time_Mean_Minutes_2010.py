import matplotlib.pyplot as plt         # Necessary to plot graphs with the data calculated
import datetime                         # Necessary to do time calculation
from pymongo import MongoClient         # Necessary to make use of MongoDB
import numpy as np               # Necessary for mean calculation

# The mongo client, necessary to connect to mongoDB
mongo_DB_Client_Instance = MongoClient('localhost', 27017)

# The data base instance for the threads
mongo_DB_Threads_Instance_2010 = mongo_DB_Client_Instance.iAMA_Reddit_Threads_2010

# Contains all collection names of the thread database
mongo_DB_Thread_Collection_2010 = mongo_DB_Threads_Instance_2010.collection_names()

# The data base instance for the comments
mongo_DB_Comments_Instance_2010 = mongo_DB_Client_Instance.iAMA_Reddit_Comments_2010

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


def check_if_comment_is_answer_from_thread_author(
        author_of_thread, comment_acutal_id, comments_cursor):

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


def check_if_comment_is_not_from_thread_author(
        author_of_thread, comment_author):

    if author_of_thread != comment_author:
        return True
    else:
        return False

# Checks whether the question is on Tier-1 Hierarchy or not


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


def calculate_ar_mean_answer_time_for_tier_x_questions(
        id_of_thread, author_of_thread):
    # print ("Processsing : " + str(id_of_thread) + " ... author: " + str(author_of_thread))

    # Makes the global comments instance locally available here
    global mongo_DB_Comments_Instance_2010

    comments_collection = mongo_DB_Comments_Instance_2010[id_of_thread]
    comments_cursor = comments_collection.find()

    amount_of_answer_times = []

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
            comment_time_stamp = collection.get("created_utc")

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
                        and bool_comment_is_question_on_tier_1 is False \
                        and bool_comment_is_not_from_thread_author is True:

                    amount_of_tier_x_questions += 1

                    # Check whether that iterated comment is answered by the
                    # host
                    answer_is_from_thread_author = check_if_comment_is_answer_from_thread_author(
                        author_of_thread, comment_acutal_id, comments_cursor)

                    # Whenever the answer to that comment is from the author
                    # (boolean == True)
                    if answer_is_from_thread_author[
                            "question_Answered_From_Host"] is True:
                        answer_time_stamp_iama_host = answer_is_from_thread_author[
                            "time_Stamp_Answer"]

                        # Adds the calculated answer time to a local list
                        amount_of_answer_times.append(
                            calculate_time_difference(
                                comment_time_stamp,
                                answer_time_stamp_iama_host))

                        amount_of_tier_x_questions_answered += 1

                # Skip that comment
                else:
                    continue

            # Whenever a comment has been deleted or has, somehow, null values
            # in it.. do not process it
            else:
                continue

    # Whenever there were some questions aksed on tier X and those questions
    # have been answered by the iAMA host on tier X
    if amount_of_tier_x_questions != 0 and amount_of_tier_x_questions_answered != 0:

        # Returns the arithmetic mean of answer time by the iAMA host
        return np.mean(amount_of_answer_times)

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
    for j, val in enumerate(mongo_DB_Thread_Collection_2010):

        # Skips the system.indexes-table which is automatically created by
        # mongodb itself
        if not val == "system.indexes":
            # References the actual iterated thread
            temp_thread = mongo_DB_Threads_Instance_2010[val]

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

            returned_value = calculate_ar_mean_answer_time_for_tier_x_questions(
                val, temp_thread_author)

            # Value could be none if it has i.E. no values
            if returned_value is not None:
                list_To_Be_Plotted.append(returned_value)

# Plots the data of the question distribution for that year


def plot_the_generated_data_percentage_mean():

    # The dictionary which is necessary to count the amount of response times
    # in Minutes
    dict_time_amount_counter = {
        "0_To_5": 0,
        "5_To_15": 0,
        "15_To_30": 0,
        "30_To_60": 0,
        "60_To_120": 0,
        "greater_Than_120": 0,
    }

    # Iterates over every value and fills the dict_time_amount_counter
    # appropriate
    for i, val in enumerate(list_To_Be_Plotted):

        if 0 < (val / 60) <= 5:
            dict_time_amount_counter["0_To_5"] += 1

        elif 5 < (val / 60) <= 15:
            dict_time_amount_counter["5_To_15"] += 1

        elif 15 < (val / 60) <= 30:
            dict_time_amount_counter["15_To_30"] += 1

        elif 30 < (val / 60) <= 60:
            dict_time_amount_counter["30_To_60"] += 1

        elif 60 < (val / 60) <= 120:
            dict_time_amount_counter["60_To_120"] += 1

        elif (val / 60) > 120:
            dict_time_amount_counter["greater_Than_120"] += 1

    plt.figure()

    # The slices will be ordered and plotted counter-clockwise.
    labels = [
        '0 bis 5 min',
        '5 bis 15 min',
        '15 bis 30 min',
        '30 bis 60 min',
        '60 bis 120 min',
        '> 120 min']
    colors = [
        'yellowgreen',
        'gold',
        'lightskyblue',
        'lightcoral',
        'mediumpurple',
        'orange']
    values = [dict_time_amount_counter['0_To_5'],
              dict_time_amount_counter['5_To_15'],
              dict_time_amount_counter['15_To_30'],
              dict_time_amount_counter['30_To_60'],
              dict_time_amount_counter['60_To_120'],
              dict_time_amount_counter['greater_Than_120']]

    patches, texts = plt.pie(values, colors=colors, startangle=90, shadow=True)
    plt.pie(values, colors=colors, autopct='%.2f%%')

    plt.legend(patches, labels, loc="lower right", bbox_to_anchor=(1.2, 0.25))
    plt.title(
        'iAMA 2010 - Ø Reaktionszeit des iAMA-Host auf Fragen auf Ebene X in Minuten')

    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

# Generates the data which will be plotted later on
generate_data_to_analyze()

# Plots a pie chart containing the tier X question distribution
plot_the_generated_data_percentage_mean()
