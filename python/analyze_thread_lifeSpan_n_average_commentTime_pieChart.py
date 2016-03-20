#   Tutorials used within this class:
#   1. (27.02.2016 @ 14:10) -
#       http://www.ast.uct.ac.za/~sarblyth/pythonGuide/PythonPlottingBeginnersGuide.pdf
#   2. (27.02.2016 @ 14:22) -
#       https://stackoverflow.com/questions/20214497/annoying-white-space-in-bar-chart-matplotlib-python
#   3. (27.02.2016 @ 16:30) -
#       http://www.programiz.com/python-programming/break-continue

import collections               # Necessary to sort collections alphabetically
import matplotlib.pyplot as plt  # Necessary to plot graphs with the data calculated
import sys                       # Necessary to use script arguments
import numpy as np               # Necessary for mean calculation
import datetime                  # Necessary for calculating time differences
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

    global argument_year, argument_calculation, argument_plot_time_unit

    # Whenever not enough arguments were given
    if len(sys.argv) <= 2:
        print("Not enough arguments were given...")
        print("Terminating script now!")
        sys.exit()
    else:
        # Writes necessary values into the variables
        argument_year = str(sys.argv[1])
        argument_calculation = str(sys.argv[2])
        argument_plot_time_unit = str(sys.argv[3]).lower()


def calculate_time_difference(id_of_thread, creation_date_of_thread):
    """Calculates the difference between thread creation date and the last comment found in that thread

    1. The creation date of a thread gets determined
    2. Then the comments will be iterated over, creating a dictionary which is structured as follows:
      {
          ('first_Comment_After_Thread_Started', int),
          ('thread_Lifespan', int),
          ('arithmetic_Mean_Response_Time', int),
          ('median_Response_Time', int),
          ('id')
      }
    3. That returned dictionary will be appended to a global list
    4. That List will be iterated later on and the appropriate graph will be plotted

    Args:
        id_of_thread (str) : The string which contains the id of the actually processed thread
        creation_date_of_thread (str) : The string which contains the creation date of the thread (in epoch formatation)
    Returns:
        dict_to_be_returned (dict) : Containing information about the time difference

    """

    # Makes the global comments instance locally available here
    global mongo_DB_Comments_Instance

    comments_collection = mongo_DB_Comments_Instance[id_of_thread]
    comments_cursor = comments_collection.find()

    # Contains the creation date of every comment in epoch time format
    time_list = []

    # Contains the time difference between every comment in seconds
    time_difference = []

    # This gets used, whenever there is a thread with no comments in it (i.E.  all values are null)
    are_comments_null = bool

    # The dictionary which will be returned later on, containing all necessary and analyzed time data
    dict_to_be_returned = {

        # The time between thread creation date and the first comment submitted to it
        "first_Comment_After_Thread_Started": 0,

        # The difference between thread creation date and the timestamp of the last comment -> live span
        "thread_Lifespan": 0,

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

    # Iterates over every time stamp and writes it into time_list
    # Additionally comments from AutoModerator-Bot are beeing ingored because
    # they skew our statistics and would be created with the same timestamp
    # like the thread itself
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
    for i, time_Value in enumerate(time_list):

        # Whenever the comments are not null (comments could be null / NoneType
        # when there is not a single comment created for that thread..)
        if time_Value is None:

            are_comments_null = True

        # Whenever a thread contains more than one comment and that comment is not null
        else:
            # Convert the time_Value into float, otherwise it could not be converted...
            time_value_current = float(time_Value)

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

                # Subtracts the comment creation time from the thread creation
                # time
                temp_thread_time = datetime.datetime.strptime(
                    temp_creation_date_of_thread_converted, '%d-%m-%Y %H:%M:%S')

                # Add the difference between those two times, in seconds, to that list
                time_difference.append(
                    (current_time_converted_for_subtraction - temp_thread_time).total_seconds())

                dict_to_be_returned["thread_Lifespan"] = int(
                    ((current_time_converted_for_subtraction - temp_thread_time).total_seconds()))

            # Whenever the last list object is iterated over skip anything because there will be no future object
            elif i != len(time_list) - 1:
                # Convers the next time_Value into float
                time_value_next = float(time_list[i + 1])
                next_time_converted = datetime.datetime.fromtimestamp(
                    time_value_next).strftime('%d-%m-%Y %H:%M:%S')

                next_time_converted_for_subtraction = datetime.datetime.strptime(
                    next_time_converted, '%d-%m-%Y %H:%M:%S')

                # Whenever the first commented gets iterated over, build the
                # difference between thread and 1st comment creation date
                if i == 0:
                    # Converts the thread creation date into a comparable time format
                    temp_creation_date_of_thread = float(creation_date_of_thread)

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
                    # Appends the difference between the time of the current and next comment into the time_difference
                    # variable
                    time_difference.append(
                        (next_time_converted_for_subtraction - current_time_converted_for_subtraction).total_seconds())

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

                # Write the time difference (seconds) between the time the thread has been created and the
                # time the last comment was created
                dict_to_be_returned["thread_Lifespan"] = int(
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


def generate_data_to_be_plotted():
    """Generates the data which will be analyzed

    1. This method iterates over every thread
        1.1. It filters if that iterated thread is an iAMA-request or not
            1.1.1. If yes: this thread gets skipped and the next one will be processed
            1.1.2. If no: this thread will be processed
    2. If the thread gets processed it will receive the life span and other information about the thread as dictionary
    3. This dictionary will be added to a global list and will be plotted later on

    Args:
        -
    Returns:
        -
    """

    print("Generating data now...")

    # noinspection PyTypeChecker
    for j, val in enumerate(mongo_DB_Thread_Collection):

        # Skips the system.indexes-table which is automatically created by  mongodb itself
        if not val == "system.indexes":
            # References the actual iterated thread
            temp_thread = mongo_DB_Threads_Instance[val]

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

            # Whenever the thread has only one comment, or null comments, or is somehow faulty it won't be added
            # to the global list which is to be plotted later on
            if returned_dict.get("median_Response_Time") == 0 \
                    or returned_dict.get("first_Comment_After_Thread_Started") == 0 \
                    or returned_dict.get("thread_Lifespan") == 0 \
                    or returned_dict.get("arithmetic_Mean_Response_Time") == 0:

                continue

            else:
                # Add that analyzed data dictionary to the global list which will be plotted later on
                list_To_Be_Plotted.append(returned_dict)


def prepare_dict_by_time_separation_for_life_span():
    """Restructures the dictionary which is to be plotted for the display of the life span

    1. This method processes the data in dependence of the commited time

    Args:
        -
    Returns:
        -
    """

    # noinspection PyUnusedLocal
    divider = 0

    dict_time_amount_counter = {
        "first": 0,
        "second": 0,
        "third": 0,
        "fourth": 0,
        "fifth": 0,
        "sixth": 0
    }

    # minutes
    if argument_plot_time_unit == "minutes":
        divider = 60

        # Iterates over every element and checks if that value is between some given values
        for i, val in enumerate(list_To_Be_Plotted):

            value = val.get("thread_Lifespan")

            if (value / divider) <= 1:
                dict_time_amount_counter["first"] += 1

            elif ((value / divider) > 1)\
                    and ((value / 60) <= 5):
                dict_time_amount_counter["second"] += 1

            elif ((value / divider) > 5)\
                    and ((value / 60) <= 10):
                dict_time_amount_counter["third"] += 1

            elif ((value / divider) > 10)\
                    and ((value / 60) <= 15):
                dict_time_amount_counter["fourth"] += 1

            elif ((value / divider) > 15)\
                    and ((value / 60) <= 30):
                dict_time_amount_counter["fifth"] += 1

            elif (value / divider) > 30:
                dict_time_amount_counter["sixth"] += 1

    # hours
    elif argument_plot_time_unit == "hours":
        divider = 3600

        # Iterates over every element and checks if that value is between some given values
        for i, val in enumerate(list_To_Be_Plotted):

            value = val.get("thread_Lifespan")

            if (value / divider) <= 1:
                dict_time_amount_counter["first"] += 1

            elif ((value / divider) > 1)\
                    and ((val.get("thread_Lifespan") / divider) <= 6):
                dict_time_amount_counter["second"] += 1

            elif ((value / divider) > 6)\
                    and ((value / divider) <= 12):
                dict_time_amount_counter["third"] += 1

            elif ((value / divider) > 12)\
                    and ((value / divider) <= 24):
                dict_time_amount_counter["fourth"] += 1

            elif ((value / divider) > 24)\
                    and ((value / divider) <= 48):
                dict_time_amount_counter["fifth"] += 1

            elif (value / divider) > 48:
                dict_time_amount_counter["sixth"] += 1

    # days
    else:
        divider = 86400

        # Iterates over every element and checks if that value is between some given values
        for i, val in enumerate(list_To_Be_Plotted):

            value = val.get("thread_Lifespan")

            if (value / divider) <= 1:
                dict_time_amount_counter["first"] += 1

            elif ((value / divider) > 1) and \
                    ((value / divider) <= 3):
                dict_time_amount_counter["second"] += 1

            elif ((value / divider) > 3) and \
                    ((value / divider) <= 7):
                dict_time_amount_counter["third"] += 1

            elif ((value / divider) > 7) and \
                    ((value / divider) <= 14):
                dict_time_amount_counter["fourth"] += 1

            elif (value / divider) > 14 and \
                    ((value / divider) <= 28):
                dict_time_amount_counter["fifth"] += 1

            elif (value / divider) > 28:
                dict_time_amount_counter["sixth"] += 1

    return dict_time_amount_counter


def prepare_dict_by_time_separation_for_comment_time():
    """Restructures the dictionary which is to be plotted for the display of the average mean comment time

    1. This method processes the data in dependence of the commited time

    Args:
        -
    Returns:
        -
    """

    # noinspection PyUnusedLocal
    divider = 0

    dict_time_amount_counter = {
        "first": 0,
        "second": 0,
        "third": 0,
        "fourth": 0,
        "fifth": 0,
        "sixth": 0
    }

    # minutes
    if argument_plot_time_unit == "minutes":
        print("")
        divider = 60

        # Iterates over every element and checks if that value is between some given values
        for i, val in enumerate(list_To_Be_Plotted):

            value = val.get("arithmetic_Mean_Response_Time")

            if (value / divider) <= 1:
                dict_time_amount_counter["first"] += 1

            elif ((value / divider) > 1)\
                    and ((value / 60) <= 5):
                dict_time_amount_counter["second"] += 1

            elif ((value / divider) > 5)\
                    and ((value / 60) <= 10):
                dict_time_amount_counter["third"] += 1

            elif ((value / divider) > 10)\
                    and ((value / 60) <= 15):
                dict_time_amount_counter["fourth"] += 1

            elif ((value / divider) > 15)\
                    and ((value / 60) <= 30):
                dict_time_amount_counter["fifth"] += 1

            elif (value / divider) > 30:
                dict_time_amount_counter["sixth"] += 1

    # hours
    elif argument_plot_time_unit == "hours":
        divider = 3600

        # Iterates over every element and checks if that value is between some given values
        for i, val in enumerate(list_To_Be_Plotted):

            value = val.get("arithmetic_Mean_Response_Time")

            if (value / divider) <= 1:
                dict_time_amount_counter["first"] += 1

            elif ((value / divider) > 1)\
                    and ((value / divider) <= 6):
                dict_time_amount_counter["second"] += 1

            elif ((value / divider) > 6)\
                    and ((value / divider) <= 12):
                dict_time_amount_counter["third"] += 1

            elif ((value / divider) > 12)\
                    and ((value / divider) <= 24):
                dict_time_amount_counter["fourth"] += 1

            elif ((value / divider) > 24)\
                    and ((value / divider) <= 48):
                dict_time_amount_counter["fifth"] += 1

            elif (value / divider) > 48:
                dict_time_amount_counter["sixth"] += 1

    # days
    else:
        divider = 86400

        # Iterates over every element and checks if that value is between some given values
        for i, val in enumerate(list_To_Be_Plotted):

            value = val.get("arithmetic_Mean_Response_Time")

            if (value / divider) <= 1:
                dict_time_amount_counter["first"] += 1

            elif ((value / divider) > 1) and \
                    ((value / divider) <= 3):
                dict_time_amount_counter["second"] += 1

            elif ((value / divider) > 3) and \
                    ((value / divider) <= 7):
                dict_time_amount_counter["third"] += 1

            elif ((value / divider) > 7) and \
                    ((value / divider) <= 14):
                dict_time_amount_counter["fourth"] += 1

            elif (value / divider) > 14 and \
                    ((value / divider) <= 28):
                dict_time_amount_counter["fifth"] += 1

            elif (value / divider) > 28:
                dict_time_amount_counter["sixth"] += 1

    return dict_time_amount_counter


def plot_the_generated_data():
    """Plots the data which is to be generated

    1. This method plots the data which has been calculated before by using 'matplotlib.pyplot-library'
    2. Depending on the committed year the title will be adapted appropriate
    3. Time units will be separated into days, because this gives us the best overview

    Args:
        -
    Returns:
        -
    """

    # noinspection PyUnusedLocal
    labels = []
    plot_title = ""

    # noinspection PyUnusedLocal
    dict_to_be_used = {}

    if argument_calculation == "lifespan":
        # The dictionary which is necessary to count the amount of response times
        dict_to_be_used = prepare_dict_by_time_separation_for_life_span()

        plot_title += 'iAMA ' +\
                      argument_year +\
                      '- Ø Lebensspanne eines Threads in '
    else:
        dict_to_be_used = prepare_dict_by_time_separation_for_comment_time()

        plot_title += 'iAMA ' + \
                      argument_year + \
                      '- Verteilung Ø Antwortzeit per Thread in '

    if argument_plot_time_unit == "minutes":
        plot_title += "Minuten"
        labels = [
            '0 bis 1 min',
            '1 bis 5 min',
            '5 bis 10 min',
            '10 bis 15 min',
            '15 bis 30 min',
            '> 30 min'
        ]

    elif argument_plot_time_unit == "hours":
        plot_title += "Stunden"
        labels = [
            '0 bis 1 h',
            '1 bis 6 h',
            '6 bis 12 h',
            '12 bis 24 h',
            '24 bis 48 h',
            '> 48 h'
        ]

    else:
        plot_title += "Tagen"
        labels = [
            '0 bis 1 d',
            '1 bis 3 d',
            '3 bis 7 d',
            '7 bis 14 d',
            '14 bis 28 d',
            '> 28 d'
        ]

    plt.figure()

    # Contains the colors, used for the plot
    colors = [
        'yellowgreen',
        'gold',
        'lightskyblue',
        'lightcoral',
        'mediumpurple',
        'orange',
    ]

    # Contains the values, used for the plot
    values = [
        dict_to_be_used['first'],
        dict_to_be_used['second'],
        dict_to_be_used['third'],
        dict_to_be_used['fourth'],
        dict_to_be_used['fifth'],
        dict_to_be_used['sixth']
    ]

    # Defines the way the patches and texts will be printed
    patches, texts = plt.pie(
        values,
        colors=colors,
        startangle=90,
        shadow=True
    )

    # Defines the design of the plots legend
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

    plt.title(plot_title)

    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    plt.tight_layout()

    plt.show()


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Necessary variables and scripts are here

# Contains the year which is given as an argument
argument_year = ""

# Contains information what data you want to be calculated
argument_calculation = ""

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

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Methods which are to be called are here


# Executes necessary checks
check_script_arguments()

# Initializes the mongoDB with the arguments given via command line
initialize_mongo_db_parameters()

# Generates the data which will be plotted later on
generate_data_to_be_plotted()

# Plots the data wich has been calculated before
plot_the_generated_data()
