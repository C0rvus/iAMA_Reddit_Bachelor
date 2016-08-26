# Sources used within this class:
# 1. (27.02.2016 @ 14:22) -
# https://stackoverflow.com/questions/20214497/annoying-white-space-in-bar-chart-matplotlib-python
# 2. (27.02.2016 @ 16:30) -
# http://www.programiz.com/python-programming/break-continue
# 3. (26.03.2016 @ 18:03) -
# https://stackoverflow.com/questions/12400256/python-converting-epoch-time-into-the-datetime

import collections               # Necessary to sort collections alphabetically
import copy                      # Necessary to copy value of the starting year - needed for correct csv file name
import csv                       # Necessary to write data to csv files
import datetime                  # Necessary for calculating time differences
import numpy as np               # Necessary for mean calculation
import os                        # Necessary to get the name of currently processed file
import sys                       # Necessary to use script arguments
from pymongo import MongoClient  # Necessary to make use of MongoDB
# noinspection PyUnresolvedReferences
from PlotlyBarChart_5_Bars import PlotlyBarChart5Bars


def check_script_arguments():
    """Checks if enough and correct arguments have been given to run this script adequate

    1. It checks in the first instance if enough arguments have been given
    2. Then necessary variables will be filled with appropriate values

    Args:
        -
    Returns:
        -
    """

    global argument_year_beginning, argument_year_ending, argument_calculation, argument_plot_time_unit

    # Whenever not enough arguments were given
    if len(sys.argv) <= 3:
        print("Not enough arguments were given...")
        print("Terminating script now!")
        sys.exit()
    else:
        # Writes necessary values into the variables
        argument_year_beginning = int(sys.argv[1])
        argument_year_ending = int(sys.argv[2])
        argument_calculation = str(sys.argv[3])
        argument_plot_time_unit = str(sys.argv[4]).lower()


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


def start_data_generation_for_analysis():
    """Starts the data processing by swichting through the years

    1. Triggers the data generation process and moves forward within the years
        1.1. By moving through the years a csv file will be created for every year
        1.2. Additionally an interactive chart will be plotted

    Args:
        -
    Returns:
        -
    """

    global argument_year_beginning, data_to_give_plotly, year_actually_in_progress, global_thread_list, \
        list_with_currents_year_infos, temp_time_difference_list

    # Copies the value of the beginning year, because it will be changed due to moving forward within the years
    year_actually_in_progress = copy.copy(argument_year_beginning)

    if argument_calculation == "lifespan":
        data_to_give_plotly.append(["t_life_span", str(argument_plot_time_unit)])
    else:
        data_to_give_plotly.append(["t_comment_time", str(argument_plot_time_unit)])

    # As long as the ending year has not been reached
    while year_actually_in_progress != argument_year_ending:

        # Starts retrieving and checking that data
        generate_data_to_be_analyzed()

        # Writes a csv file for the actually processed year
        write_csv(list_with_currents_year_infos)

        if argument_calculation == "lifespan":

            # Iterates over every item within the list and adds them to a gobal list..
            # This is necessary for printing out a global list containing appropriate information about threads, etc.
            add_thread_list_to_global_list(list_with_currents_year_infos)

            # Prepares data for graph / chart plotting later on
            dict_thread_life_span = prepare_data_for_graph_life_span()

            data_to_give_plotly.append([
                int(year_actually_in_progress),
                dict_thread_life_span["first"],
                dict_thread_life_span["second"],
                dict_thread_life_span["third"],
                dict_thread_life_span["fourth"],
                dict_thread_life_span["fifth"],
            ])

        # Whenever the average comment reaction time will be calculated
        else:

            # Iterates over every item within the list and adds them to a gobal list..
            # This is necessary for printing out a global list containing appropriate information about threads, etc.
            add_thread_list_to_global_list(list_with_currents_year_infos)

            # Calculates the average mean comment reaction time of users within that actually processed year
            dict_mean_comment_time = prepare_data_for_comment_time()

            # Append data to plotly object
            data_to_give_plotly.append([
                int(year_actually_in_progress),
                dict_mean_comment_time["first"],
                dict_mean_comment_time["second"],
                dict_mean_comment_time["third"],
                dict_mean_comment_time["fourth"],
                dict_mean_comment_time["fifth"],
            ])

            # Empty that time list so there is space for new values
            temp_time_difference_list = []

        # Empty that list, so new values have room
        list_with_currents_year_infos = []

        # Progresses in the year, necessary for onward year calculation
        year_actually_in_progress += 1

        # Reinitializes the mongodb with new year parameter here
        # noinspection PyTypeChecker
        initialize_mongo_db_parameters(year_actually_in_progress)

    # Will be entered whenever the last year is beeing processed
    if year_actually_in_progress == argument_year_ending:

        # Starts retrieving and checking that data
        generate_data_to_be_analyzed()

        # Writes a csv file for the actually processed year
        write_csv(list_with_currents_year_infos)

        if argument_calculation == "lifespan":

            # Iterates over every item within the list and adds them to a gobal list..
            # This is necessary for printing out a global list containing appropriate information about threads, etc.
            add_thread_list_to_global_list(list_with_currents_year_infos)

            # Prepares data for graph / chart plotting later on
            dict_thread_life_span = prepare_data_for_graph_life_span()

            # Append data to plotly object
            data_to_give_plotly.append([
                int(year_actually_in_progress),
                dict_thread_life_span["first"],
                dict_thread_life_span["second"],
                dict_thread_life_span["third"],
                dict_thread_life_span["fourth"],
                dict_thread_life_span["fifth"],
            ])

        else:

            # Iterates over every item within the list and adds them to a gobal list..
            # This is necessary for printing out a global list containing appropriate information about threads, etc.
            add_thread_list_to_global_list(list_with_currents_year_infos)

            # Calculates the average mean comment reaction time of users within that actually processed year
            dict_mean_comment_time = prepare_data_for_comment_time()

            # Append data to plotly object
            data_to_give_plotly.append([
                int(year_actually_in_progress),
                dict_mean_comment_time["first"],
                dict_mean_comment_time["second"],
                dict_mean_comment_time["third"],
                dict_mean_comment_time["fourth"],
                dict_mean_comment_time["fifth"],
            ])

            # Empty that time list so there is space for new values
            temp_time_difference_list = []

        # Empty that list, so new values have room
        list_with_currents_year_infos = []

        # Value setting is necessary for correct file writing
        year_actually_in_progress = "ALL"

    # Writes a global csv file containing information about all threads
    write_csv(global_thread_list)

    # Plots the graph
    plot_generated_data()


def prepare_data_for_graph_life_span():
    """Calculates the distribution of single values regarding the chosen time argument

    Args:
        -
    Returns:
        -
    """

    dict_time_amount_counter = {
        "first": 0,
        "second": 0,
        "third": 0,
        "fourth": 0,
        "fifth": 0
    }

    # Minutes
    if argument_plot_time_unit == "minutes":
        divider = 60

        # Iterates over every element and checks if that value is between some given values
        for i, val in enumerate(list_with_currents_year_infos):

            value = val.get("Thread_life_span")

            if (value / divider) <= 14:
                dict_time_amount_counter["first"] += 1

            elif ((value / divider) > 14) \
                    and ((value / 60) <= 29):
                dict_time_amount_counter["second"] += 1

            elif ((value / divider) > 29) \
                    and ((value / 60) <= 59):
                dict_time_amount_counter["third"] += 1

            elif ((value / divider) > 59) \
                    and ((value / 60) <= 119):
                dict_time_amount_counter["fourth"] += 1

            elif (value / divider) >= 120:
                dict_time_amount_counter["fifth"] += 1

    # Hours
    elif argument_plot_time_unit == "hours":
        divider = 3600

        # Iterates over every element and checks if that value is between some given values
        for i, val in enumerate(list_with_currents_year_infos):

            value = val.get("Thread_life_span")

            if (value / divider) <= 1:
                dict_time_amount_counter["first"] += 1

            elif ((value / divider) > 1) \
                    and ((value / divider) <= 5):
                dict_time_amount_counter["second"] += 1

            elif ((value / divider) > 5) \
                    and ((value / divider) <= 10):
                dict_time_amount_counter["third"] += 1

            elif ((value / divider) > 10) \
                    and ((value / divider) <= 23):
                dict_time_amount_counter["fourth"] += 1

            elif (value / divider) >= 24:
                dict_time_amount_counter["fifth"] += 1

    # Days
    else:
        divider = 86400

        # Iterates over every element and checks if that value is between some given values
        for i, val in enumerate(list_with_currents_year_infos):

            value = val.get("Thread_life_span")

            if (value / divider) <= 1:
                dict_time_amount_counter["first"] += 1

            elif ((value / divider) > 1) and \
                    ((value / divider) <= 4):
                dict_time_amount_counter["second"] += 1

            elif ((value / divider) > 4) and \
                    ((value / divider) <= 8):
                dict_time_amount_counter["third"] += 1

            elif ((value / divider) > 8) and \
                    ((value / divider) <= 13):
                dict_time_amount_counter["fourth"] += 1

            elif (value / divider) >= 14:
                dict_time_amount_counter["fifth"] += 1

    return dict_time_amount_counter


def prepare_data_for_comment_time():
    """Prepares the average mean comment time per thread

    Args:
        -
    Returns:
        -
    """
    global temp_time_difference_list, data_to_give_plotly

    temp_amount_counter = 0

    dict_time_amount_counter = {
        "first": 0,
        "second": 0,
        "third": 0,
        "fourth": 0,
        "fifth": 0
    }

    for item in temp_time_difference_list:
        for i in item:
            temp_amount_counter += i

        temp_amount_counter /= len(item)

        # Minutes
        if argument_plot_time_unit == "minutes":
            divider = 60

            value = temp_amount_counter

            if (value / divider) <= 14:
                dict_time_amount_counter["first"] += 1

            elif ((value / divider) > 14) \
                    and ((value / 60) <= 29):
                dict_time_amount_counter["second"] += 1

            elif ((value / divider) > 29) \
                    and ((value / 60) <= 59):
                dict_time_amount_counter["third"] += 1

            elif ((value / divider) > 59) \
                    and ((value / 60) <= 119):
                dict_time_amount_counter["fourth"] += 1

            elif (value / divider) >= 120:
                dict_time_amount_counter["fifth"] += 1

        # Hours
        elif argument_plot_time_unit == "hours":
            divider = 3600

            # Iterates over every element and checks if that value is between some given values

            value = temp_amount_counter

            if (value / divider) <= 1:
                dict_time_amount_counter["first"] += 1

            elif ((value / divider) > 1) \
                    and ((value / divider) <= 5):
                dict_time_amount_counter["second"] += 1

            elif ((value / divider) > 5) \
                    and ((value / divider) <= 10):
                dict_time_amount_counter["third"] += 1

            elif ((value / divider) > 10) \
                    and ((value / divider) <= 23):
                dict_time_amount_counter["fourth"] += 1

            elif (value / divider) >= 24:
                dict_time_amount_counter["fifth"] += 1

        # Days
        else:
            divider = 86400

            value = temp_amount_counter

            if (value / divider) <= 1:
                dict_time_amount_counter["first"] += 1

            elif ((value / divider) > 1) and \
                    ((value / divider) <= 4):
                dict_time_amount_counter["second"] += 1

            elif ((value / divider) > 4) and \
                    ((value / divider) <= 8):
                dict_time_amount_counter["third"] += 1

            elif ((value / divider) > 8) and \
                    ((value / divider) <= 13):
                dict_time_amount_counter["fourth"] += 1

            elif (value / divider) >= 14:
                dict_time_amount_counter["fifth"] += 1

        # Resets the value
        temp_amount_counter = 0

    return dict_time_amount_counter


def generate_data_to_be_analyzed():
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

    print("Generating data for year " + str(year_actually_in_progress) + " now...")

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
            if returned_dict.get("Median_Response_Time") == 0 \
                    or returned_dict.get("First_comment_after_thread_started") == 0 \
                    or returned_dict.get("Thread_life_span") == 0 \
                    or returned_dict.get("Arithmetic_mean_response_time") == 0:

                continue

            else:
                # Add that analyzed data dictionary to the global list which will be plotted later on
                list_with_currents_year_infos.append(returned_dict)


def calculate_time_difference(id_of_thread, creation_date_of_thread):
    """Calculates the difference between thread creation date and the last comment found in that thread

    1. The creation date of a thread gets determined
    2. Then the comments will be iterated over, creating a dictionary which is structured as follows:
      {
          ('first_Comment_After_Thread_Started', int),
          ('thread_life_span', int),
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
    global mongo_DB_Comments_Instance, temp_time_difference_list

    comments_collection = mongo_DB_Comments_Instance[id_of_thread]
    comments_cursor = list(comments_collection.find())

    temp_thread = mongo_DB_Threads_Instance[id_of_thread]
    temp_thread_ups = temp_thread.find()[0].get("ups")
    temp_thread_downs = temp_thread.find()[0].get("downs")

    # Contains the creation date of every comment in epoch time format
    time_list = []

    # Contains the time difference between every comment in seconds
    time_difference = []

    # This gets used, whenever there is a thread with no comments in it (i.E.  all values are null)
    are_comments_null = bool

    # The dictionary which will be returned later on, containing all necessary and analyzed time data
    dict_to_be_returned = {

        # The time between thread creation date and the first comment submitted to it
        "First_comment_after_thread_started": 0,

        # The difference between thread creation date and the timestamp of the last comment -> live span
        "Thread_life_span": 0,

        # The amount of upvotes a thread received
        "Thread_ups": temp_thread_ups,

        # The amount of downvotes a thread received
        "Thread_downs": temp_thread_downs,

        # The arithmetic mean response time between the comments
        "Arithmetic_mean_response_time": 0,

        # The median response time between the comments
        "Median_Response_Time": 0,

        # The thread id. Not really necessary but perhaps interesting for postprocessing threads
        # (i.E. looking up, which threads have most comments)
        "Thread_id": str(id_of_thread),

        # The amount of comments for the iterated thread
        "Thread_num_comments": 0,

        # Appends the year, actually in progress
        "Year": year_actually_in_progress
    }

    # Iterates over every time stamp and writes it into time_list
    # Additionally comments from AutoModerator-Bot are beeing ingored because
    # they skew our statistics and would be created with the same timestamp
    # like the thread itself
    for i, val in enumerate(comments_cursor):

        # Whenever the iterated comment was created by user "AutoModerator" skip it
        if (val.get("author")) != "AutoModerator":
            time_list.append(val.get("created_utc"))

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

                # Subtracts the comment creation time from the thread creation time
                temp_thread_time = datetime.datetime.strptime(
                    temp_creation_date_of_thread_converted, '%d-%m-%Y %H:%M:%S')

                # Add the difference between those two times, in seconds, to that list
                time_difference.append(
                    (current_time_converted_for_subtraction - temp_thread_time).total_seconds())

                dict_to_be_returned["Thread_life_span"] = int(
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
                # The substraction method only returns ints and no floats
                dict_to_be_returned["Thread_life_span"] = int(
                    ((current_time_converted_for_subtraction - temp_thread_time).total_seconds()))

    # Whenever not a single comment was null.. concrete: Whenever everything is normal and the thread contains answers
    if are_comments_null is not True:
        dict_to_be_returned["First_comment_after_thread_started"] = int(time_difference[0])

        # Resorts the time_difference - List , which is necessary to correctly calculate the median of it
        time_difference.sort()

        # Adds the list containing all response time information to a global list.. necessary for correct csv writing
        # and graph plotting
        temp_time_difference_list.append(time_difference)

        dict_to_be_returned["Arithmetic_mean_response_time"] = int(np.mean(time_difference))
        dict_to_be_returned["Median_Response_Time"] = float(np.median(time_difference))
        dict_to_be_returned["Thread_num_comments"] = len(time_list)

        # Sorts that dictionary so the dictionary structure is standardized
        dict_to_be_returned = collections.OrderedDict(sorted(dict_to_be_returned.items()))

    # Return that processed dictionary
    return dict_to_be_returned


def write_csv(list_with_information):
    """Creates a csv file containing all necessary information about the life span of a thread and various information
        about comments

    Args:
        list_with_information (list) : Contains various information about thread and comment time
    Returns:
        -
    """
    global global_thread_list

    print("---- Writing csv containing all thread life spans for year " + str(year_actually_in_progress) + " now")
    # Empty print line here for a more beautiful console output
    print("")

    file_name_csv = str(os.path.basename(__file__))[0:len(os.path.basename(__file__)) - 3] + \
                    '_' + \
                    str(argument_year_beginning) + \
                    '_until_' + \
                    str(argument_year_ending) + \
                    '_' + \
                    "thread_n_comment" + \
                    '_' + \
                    str(year_actually_in_progress) + \
                    '.csv'

    with open(file_name_csv, 'w', newline='') as fp:
        csv_writer = csv.writer(fp, delimiter=',')

        data = [['Year',
                 'Thread id',
                 'Thread ups',
                 'Thread downs',
                 'Thread comments',
                 'Thread life span (sec) to last reaction of anyone',
                 'Thread average mean comment reaction time (sec)',
                 'Thread median comment reaction time (sec)',
                 'Link to Thread']]

        # Iterates over that generated sorted and counts the amount of questions which have not been answered
        for item in list_with_information:
            temp_list = [str(item.get("Year")),
                         str(item.get("Thread_id")),
                         str(item.get("Thread_ups")),
                         str(item.get("Thread_downs")),
                         str(item.get("Thread_num_comments")),
                         str(item.get("Thread_life_span")),
                         str(item.get("Arithmetic_mean_response_time")),
                         str(item.get("Median_Response_Time")),
                         'https://www.reddit.com/r/IAma/' + str(item.get("Thread_id"))
                         ]
            data.append(temp_list)

        # Writes data into the csv file
        csv_writer.writerows(data)


def add_thread_list_to_global_list(list_to_append):
    """Adds all elements of for the current year into a global list. This global list will be written into a csv file
    later on

    1. This method simply checks wether both strings match each other or not.
        I have built this extra method to have a better overview in the main code..

    Args:
        list_to_append (list) : The list which will be iterated over and which elements will be added to the global list
    Returns:
        -
    """

    global global_thread_list

    for item in list_to_append:
        global_thread_list.append(item)


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
        for i, val in enumerate(list_with_currents_year_infos):

            value = val.get("Arithmetic_mean_response_time")

            if (value / divider) <= 1:
                dict_time_amount_counter["first"] += 1

            elif ((value / divider) > 1) \
                    and ((value / 60) <= 5):
                dict_time_amount_counter["second"] += 1

            elif ((value / divider) > 5) \
                    and ((value / 60) <= 10):
                dict_time_amount_counter["third"] += 1

            elif ((value / divider) > 10) \
                    and ((value / 60) <= 15):
                dict_time_amount_counter["fourth"] += 1

            elif ((value / divider) > 15) \
                    and ((value / 60) <= 30):
                dict_time_amount_counter["fifth"] += 1

            elif (value / divider) > 30:
                dict_time_amount_counter["sixth"] += 1

    # hours
    elif argument_plot_time_unit == "hours":
        divider = 3600

        # Iterates over every element and checks if that value is between some given values
        for i, val in enumerate(list_with_currents_year_infos):

            value = val.get("Arithmetic_mean_response_time")

            if (value / divider) <= 1:
                dict_time_amount_counter["first"] += 1

            elif ((value / divider) > 1) \
                    and ((value / divider) <= 6):
                dict_time_amount_counter["second"] += 1

            elif ((value / divider) > 6) \
                    and ((value / divider) <= 12):
                dict_time_amount_counter["third"] += 1

            elif ((value / divider) > 12) \
                    and ((value / divider) <= 24):
                dict_time_amount_counter["fourth"] += 1

            elif ((value / divider) > 24) \
                    and ((value / divider) <= 48):
                dict_time_amount_counter["fifth"] += 1

            elif (value / divider) > 48:
                dict_time_amount_counter["sixth"] += 1

    # days
    else:
        divider = 86400

        # Iterates over every element and checks if that value is between some given values
        for i, val in enumerate(list_with_currents_year_infos):

            value = val.get("Arithmetic_mean_response_time")

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


def plot_generated_data():
    """Plots the data which is to be generated

    1. This method plots the data which has been calculated before by using Pltoly-Framework within a self written class

    Args:
        -
    Returns:
        -
    """

    PlotlyBarChart5Bars().main_method(data_to_give_plotly)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Necessary variables and scripts are here

# Contains the year which is given as an argument
argument_year_beginning = 0

# Contains information what data you want to be calculated
argument_calculation = ""

# Contains the year which is given as an argument
argument_year_ending = 0

# Contains the year which will be processed at the moment
year_actually_in_progress = 0

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

# Contains all questions of the actually processed year
global_thread_list = []

# Contains every single time difference_value for the currently processed year
temp_time_difference_list = []

# Will contain all analyzed time information for threads & comments
list_with_currents_year_infos = []


# Contains the data which are necessary for plotly
# <editor-fold desc="Description of data object plotly needs">
# Structure as follows:
# [ "analyze_type", "analyze_time_setting"},
#  [year, first values, second values, third values, fourth values, fifth values],
#  ... ]
# Values can be the amount of minutes between a defined interval..
# i.e. [["t_life_span", "minutes"],
#       [2009, 32, 21, 48, 102, 4787],
#       [...],
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
