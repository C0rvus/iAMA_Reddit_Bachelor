# Tutorials used within this class:
# 1. (27.02.2016 @ 14:10) -
#       http://www.ast.uct.ac.za/~sarblyth/pythonGuide/PythonPlottingBeginnersGuide.pdf
# 2. (27.02.2016 @ 14:22) -
#       https://stackoverflow.com/questions/20214497/annoying-white-space-in-bar-chart-matplotlib-python
# 3. (27.02.2016 @ 16:30) -
#       http://www.programiz.com/python-programming/break-continue
# This script has been developed with PRAW 3.3.0

from pymongo import MongoClient     # Necessary to make use of MongoDB
import datetime                     # Necessary to do time calculation
import numpy as np                  # Necessary to do further time calculation
import collections                  # Necessary to sort collections alphabetically
import matplotlib.pyplot as plt     # Necessary to plot graphs with the data calculated

# The mongo client, necessary to connect to mongoDB
mongo_DB_Client_Instance = MongoClient('localhost', 27017)

# The data base instance for the threads
mongo_DB_Threads_Instance_2009 = mongo_DB_Client_Instance.iAMA_Reddit_Threads_2009

# Contains all collection names of the thread database
mongo_DB_Thread_Collection_2009 = mongo_DB_Threads_Instance_2009.collection_names()

# The data base instance for the comments
mongo_DB_Comments_Instance_2009 = mongo_DB_Client_Instance.iAMA_Reddit_Comments_2009

# Will contain all analyzed time information for threads & comments
list_To_Be_Plotted = []


# <editor-fold desc="Analyses data of threads and comments in terms of time">
# Calculates the average & medan comment time, the thread livespan,
# and the timespan after which the first comment is submitted
# </editor-fold>
def calculate_time_difference(id_of_thread, creation_date_of_thread):

    # Makes the global comments instance locally available here
    global mongo_DB_Comments_Instance_2009

    comments_collection = mongo_DB_Comments_Instance_2009[id_of_thread]
    comments_cursor = comments_collection.find()

    # Contains the creation date of every comment in epoch time format
    time_list = []

    # Contains the time difference between every comment in seconds
    time_difference = []

    # This gets used, whenever there is a thread with no comments in it (i.E. all values are null)
    are_comments_null = bool

    # The dictionary which will be returned later on, containing all necessary and analyzed time data
    dict_to_be_returned = {
        # The time between thread creation date and the first comment submitted to it
        "first_Comment_After_Thread_Started": 0,

        # The difference between thread creation date and the timestamp of the last comment -> live span
        "thread_Livespan": 0,

        # The arithmetic mean response time between the comments
        "arithmetic_Mean_Response_Time": 0,

        # The median response time between the comments
        "median_Response_Time": 0,

        # The thread id. Not really necessary but perhaps interesting for postprocessing threads
        # (i.E. looking up, which threads have most comments)
        "id": str(id_of_thread),

        # The amount of comments for the iterated thread
        "thread_Num_Comments": 0
    }

    # Iterates over every time stamp and writes it into time_list. Additionally comments from AutoModerator-Bot
    # are beeing ingored because they skew our statistics and would be created with the same timestamp like the thread
    # itself
    for collection in comments_cursor:
        # Whenever the iterated comment was created by user "AutoModerator" skip it
        if (collection.get("author")) != "AutoModerator":
            time_list.append(collection.get("created_utc"))

    # Whenever only "Automoderator" responded and no real comments were given, return an empty dictionary,
    # which will be discarded later on
    if len(time_list) == 0:
        return dict_to_be_returned

    # This sorts the time in an ascending way
    time_list.sort()

    # Calculate the time difference within here
    for i, time_value in enumerate(time_list):
        # Whenever the comments are not null (comments could be null / NoneType when there is not a single comment
        # created for that thread..)
        if time_value is None:
            are_comments_null = True

        # Whenever a thread contains more than one comment and that comment is not null
        else:
            # Convert the time_value into float, otherwise it could not be converted...
            time_value_current = float(time_value)
            current_time_converted = datetime.datetime.fromtimestamp(
                time_value_current).strftime('%d-%m-%Y %H:%M:%S')
            current_time_converted_for_subtraction = datetime.datetime.strptime(
                current_time_converted, '%d-%m-%Y %H:%M:%S')

            # Whenever a thread only has one single comment which is not null
            if len(time_list) == 1:
                # Converts the thread creation date into a comparable time format
                temp_creation_date_of_thread = float(creation_date_of_thread)

                temp_creation_date_of_thread_converted = datetime.datetime.fromtimestamp(
                    temp_creation_date_of_thread).strftime('%d-%m-%Y %H:%M:%S')

                # Subtracts the comment creation time from the thread creation time
                temp_thread_time = datetime.datetime.strptime(
                    temp_creation_date_of_thread_converted, '%d-%m-%Y %H:%M:%S')

                # Add the difference between those two times, in seconds, to
                # that list
                time_difference.append((current_time_converted_for_subtraction - temp_thread_time).total_seconds())
                dict_to_be_returned["thread_Livespan"] = int(
                    ((current_time_converted_for_subtraction - temp_thread_time).total_seconds()))

            # Whenever the last list object is iterated over skip anything because there will be no future object
            elif i != len(time_list) - 1:

                # Converts the next time_value into float
                time_value_next = float(time_list[i + 1])

                next_time_converted = datetime.datetime.fromtimestamp(
                    time_value_next).strftime('%d-%m-%Y %H:%M:%S')

                next_time_converted_for_subtraction = datetime.datetime.strptime(
                    next_time_converted, '%d-%m-%Y %H:%M:%S')

                # Whenever the first commented gets iterated over, build the difference between thread and 1st
                # comment creation date
                if i == 0:
                    # Converts the thread creation date into a comparable time format
                    temp_creation_date_of_thread = float(
                        creation_date_of_thread)
                    temp_creation_date_of_thread_converted = datetime.datetime.fromtimestamp(
                        temp_creation_date_of_thread).strftime('%d-%m-%Y %H:%M:%S')

                    # Subtracts the comment creation time from the thread creation time
                    temp_thread_time = datetime.datetime.strptime(
                        temp_creation_date_of_thread_converted, '%d-%m-%Y %H:%M:%S')

                    # Add the difference between those two times, in seconds, to that list
                    time_difference.append(
                        (current_time_converted_for_subtraction -
                         temp_thread_time).total_seconds())

                else:
                    # Add the difference between the time of the current and next comment into the time_difference
                    # variable
                    time_difference.append(
                        (next_time_converted_for_subtraction -
                         current_time_converted_for_subtraction).total_seconds())

            # Whenever the last comment time stamp gets iterated over ->
            # calculate the time difference between thread creation date and that last comment (seconds)
            else:
                # Converts the thread creation date into a comparable time format
                temp_creation_date_of_thread = float(creation_date_of_thread)
                temp_creation_date_of_thread_converted = datetime.datetime.fromtimestamp(
                    temp_creation_date_of_thread).strftime('%d-%m-%Y %H:%M:%S')

                # Subtracts the comment creation time from the thread creation time
                temp_thread_time = datetime.datetime.strptime(
                    temp_creation_date_of_thread_converted, '%d-%m-%Y %H:%M:%S')

                # Write the time difference (seconds) between the time the thread has been created and the time the
                # last comment was created
                dict_to_be_returned["thread_Livespan"] = int(
                    ((current_time_converted_for_subtraction - temp_thread_time).total_seconds()))

    # Whenever not a single comment was null.. concrete: Whenever everything is normal and the thread contains answers
    if are_comments_null is not True:
        dict_to_be_returned["first_Comment_After_Thread_Started"] = int(time_difference[0])

        # Resorts the time_difference - List , which is necessary to correctly calculate the median of it
        time_difference.sort()

        dict_to_be_returned["arithmetic_Mean_Response_Time"] = float(np.mean(time_difference))
        dict_to_be_returned["median_Response_Time"] = float(np.median(time_difference))
        dict_to_be_returned["thread_Num_Comments"] = len(time_list)

        # Sorts that dictionary so the dictionary structure is standardized
        dict_to_be_returned = collections.OrderedDict(sorted(dict_to_be_returned.items()))

    # Return that processed dictionary
    return dict_to_be_returned

# <editor-fold desc="Generates data which is about to be plotted later on">
# 1. The creation date of a thread gets determined
# 2. Then the comments will be iterated over, creating a dictionary which is structured as follows:
#   {
#       ('first_Comment_After_Thread_Started', int),
#       ('thread_Livespan', int),
#       ('arithmetic_Mean_Response_Time', int),
#       ('median_Response_Time', int),
#       ('id')
#   }
# 3. That returned dictionary will be appended to a global list
# 4. That List will be iterated later on and the appropriate graph will be plotted
# </editor-fold>


def generate_data_to_be_plotted():
    for j, val in enumerate(mongo_DB_Thread_Collection_2009):
        # Skips the system.indexes-table which is automatically created by mongodb itself
        if not val == "system.indexes":
            # References the actual iterated thread
            temp_thread = mongo_DB_Threads_Instance_2009[val]

            # Gets the creation date of that iterated thread
            temp_thread_creation_time = temp_thread.find()[0].get("created_utc")

            # Gets the title of that iterated thread
            temp_thread_title = temp_thread.find()[0].get("title")

            # Removes iAMA-Requests out of our selection
            if "request" in temp_thread_title.lower() \
                    and "as requested" not in temp_thread_title.lower() \
                    and "by request" not in temp_thread_title.lower() \
                    and "per request" not in temp_thread_title.lower() \
                    and "request response" not in temp_thread_title.lower():
                # Continue skips processing of those elements which are requests here
                continue

            # Will contain information about time calculation methods
            returned_dict = calculate_time_difference(val, temp_thread_creation_time)
            # Whenever the thread has only one comment, or null comments, or is
            # somehow faulty it won't be added to the global list which is to be plotted later on
            if returned_dict.get("median_Response_Time") == 0 \
                    or returned_dict.get("first_Comment_After_Thread_Started") == 0 \
                    or returned_dict.get("thread_Livespan") == 0 \
                    or returned_dict.get("arithmetic_Mean_Response_Time") == 0:
                print("Thread '" + val +
                      "' will not be added to global list. Therefore it won't be in the plotted graph.")
            else:
                # Add that analyzed data dictionary to the global list which
                # will be plotted later on
                list_To_Be_Plotted.append(returned_dict)

# <editor-fold desc="Plots the data of the arithmetic mean for that threads">
# Plotts the arithmetic mean - extrema are not filtered here
# </editor-fold>


def plot_the_generated_data_arithmetic_mean(extrema_filter_value):
    # Contains the arithmetic_Mean_Response_Time
    y = []

    # Defines the highest y value so the y axis gets scaled correctly
    highest_y_value = 0

    # Iterates over every value within the list and calculates the arithmetic mean response time in minutes
    for i, val in enumerate(list_To_Be_Plotted):
        if val.get("arithmetic_Mean_Response_Time") / 60 < extrema_filter_value:
            y.append(val.get("arithmetic_Mean_Response_Time") / 60)

            if (val.get("arithmetic_Mean_Response_Time") / 60) > highest_y_value:
                highest_y_value = (val.get("arithmetic_Mean_Response_Time") / 60)

    # Contains the number of elements, which is necessary for correct horizontal graph scaling
    n = len(y)
    x = range(n)

    # The type of graph which is to be plotted..
    plt.title(
        'iAMA 2009 - Ø Antwortzeit per Thread in Minuten' + '\n' + 'Filterung: Extrema mit über ' +
        str(extrema_filter_value) + ' Minuten Antwortzeit')

    plt.xlabel('Threadnummer')
    plt.ylabel('Ø Antworzeit (min)')

    # Necessary to remove annyoing white space on the right side of the graph
    plt.xlim(0, len(y))
    plt.ylim(0, highest_y_value)

    # Plots the appropriate bar within the graph
    plt.bar(x, y, 1, color="green", edgecolor="none")

    print("Durchschnittliche Antwortzeit : " + str(sum(y) / float(len(y))) + " Minuten")

    # Show that plotted graph
    plt.show()

# Generates the data which will be plotted later on
generate_data_to_be_plotted()

# Filters extrema in minutes
plot_the_generated_data_arithmetic_mean(18000)