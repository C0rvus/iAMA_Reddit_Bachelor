#   Tutorials used within this class:
#   1. (27.02.2016 @ 14:10) - http://www.ast.uct.ac.za/~sarblyth/pythonGuide/PythonPlottingBeginnersGuide.pdf
#   2. (27.02.2016 @ 14:22) - https://stackoverflow.com/questions/20214497/annoying-white-space-in-bar-chart-matplotlib-python
#   3. (27.02.2016 @ 16:30) - http://www.programiz.com/python-programming/break-continue
#   This script is developed with PRAW 3.3.0


from pymongo import MongoClient                                                                                 # Necessary to make use of MongoDB
import datetime                                                                                                 # Necessary to do time calculation
import numpy as np                                                                                              # Necessary to do further time calculation
import collections                                                                                              # Necessary to sort collections alphabetically
import matplotlib.pyplot as plt                                                                                 # Necessary to plot graphs with the data calculated
import plotly.plotly as py
import plotly.graph_objs as go



mongo_DB_Client_Instance                =               MongoClient('localhost', 27017)                         # The mongo client, necessary to connect to mongoDB
mongo_DB_Threads_Instance_2009          =               mongo_DB_Client_Instance.iAMA_Reddit_Threads_2009       # The data base instance for the threads
mongo_DB_Thread_Collection_2009         =               mongo_DB_Threads_Instance_2009.collection_names()       # Contains all collection names of the thread database
mongo_DB_Comments_Instance_2009         =               mongo_DB_Client_Instance.iAMA_Reddit_Comments_2009      # The data base instance for the comments
list_To_Be_Plotted                      =               []                                                      # Will contain all analyzed time information for threads & comments


# <editor-fold desc="Analyses data of threads and comments in terms of time">
# Calculates the average & medan comment time, the thread livespan, and the timespan after which the first comment is submitted
# </editor-fold>
def calculate_Time_Difference(id_Of_Thread, creation_Date_Of_Thread):
	# Makes the global comments instance locally available here
	global mongo_DB_Comments_Instance_2009

	comments_Collection = mongo_DB_Comments_Instance_2009[id_Of_Thread]
	comments_Cursor = comments_Collection.find()

	# Contains the creation date of every comment in epoch time format
	time_List = []

	# Contains the time difference between every comment in seconds
	time_Difference = []

	# This gets used, whenever there is a thread with no comments in it (i.E. all values are null)
	are_Comments_Null = bool

	# The dictionary which will be returned later on, containing all necessary and analyzed time data
	dict_To_Be_Returned = {
		"first_Comment_After_Thread_Started"    :   0,                  # The time between thread creation date and the first comment submitted to it
		"thread_Livespan"                       :   0,                  # The difference between thread creation date and the timestamp of the last comment -> live span
		"arithmetic_Mean_Response_Time"         :   0,                  # The arithmetic mean response time between the comments
		"median_Response_Time"                  :   0,                  # The median response time between the comments
		"id"                                    :   str(id_Of_Thread),  # The thread id. Not really necessary but perhaps interesting for postprocessing threads (i.E. looking up, which threads have most comments)
		"thread_Num_Comments"                   :   0                   # The amount of comments for the iterated thread
	}

	# Iterates over every time stamp and writes it into time_List
	# Additionally comments from AutoModerator-Bot are beeing ingored because they skew our statistics and would be created with the same timestamp like the thread itself
	for collection in comments_Cursor:

		# Whenever the iterated comment was created by user "AutoModerator" skip it
		if (collection.get("author")) != "AutoModerator":
			time_List.append(collection.get("created_utc"))

	# Whenever only "Automoderator" responded and no real comments were given, return an empty dictionary, which will be discarded later on
	if len(time_List) == 0: return dict_To_Be_Returned

	# This sorts the time in an ascending way
	time_List.sort()

	# Calculate the time difference within here
	for i, time_Value in enumerate(time_List):

		# Whenever the comments are not null (comments could be null / NoneType when there is not a single comment created for that thread..)
		if time_Value is None:

			are_Comments_Null = True

		# Whenever a thread contains more than one comment and that comment is not null
		else:
			# Convert the time_Value into float, otherwise it could not be converted...
			time_Value_Current = float(time_Value)
			current_Time_Converted = datetime.datetime.fromtimestamp(time_Value_Current).strftime('%d-%m-%Y %H:%M:%S')
			current_Time_Converted_For_Subtraction = datetime.datetime.strptime(current_Time_Converted, '%d-%m-%Y %H:%M:%S')


			# Whenever a thread only has one single comment which is not null
			if len(time_List) == 1:
				# Converts the thread creation date into a comparable time format
				temp_Creation_Date_Of_Thread = float(creation_Date_Of_Thread)
				temp_Creation_Date_Of_Thread_Converted = datetime.datetime.fromtimestamp(temp_Creation_Date_Of_Thread).strftime('%d-%m-%Y %H:%M:%S')

				# Subtracts the comment creation time from the thread creation time
				temp_Thread_Time = datetime.datetime.strptime(temp_Creation_Date_Of_Thread_Converted, '%d-%m-%Y %H:%M:%S')

				# Add the difference between those two times, in seconds, to that list
				time_Difference.append((current_Time_Converted_For_Subtraction - temp_Thread_Time).total_seconds())
				dict_To_Be_Returned["thread_Livespan"] = int(((current_Time_Converted_For_Subtraction - temp_Thread_Time).total_seconds()))

			# Whenever the last list object is iterated over skip anything because there will be no future object
			elif i != len(time_List) - 1:
				# Convers the next time_Value into float
				time_Value_Next = float(time_List[i + 1])
				next_Time_Converted = datetime.datetime.fromtimestamp(time_Value_Next).strftime('%d-%m-%Y %H:%M:%S')
				next_Time_Converted_For_Subtraction = datetime.datetime.strptime(next_Time_Converted, '%d-%m-%Y %H:%M:%S')

				# Whenever the first commented gets iterated over, build the difference between thread and 1st comment creation date
				if i == 0:
					# Converts the thread creation date into a comparable time format
					temp_Creation_Date_Of_Thread = float(creation_Date_Of_Thread)
					temp_Creation_Date_Of_Thread_Converted = datetime.datetime.fromtimestamp(temp_Creation_Date_Of_Thread).strftime('%d-%m-%Y %H:%M:%S')

					# Subtracts the comment creation time from the thread creation time
					temp_Thread_Time = datetime.datetime.strptime(temp_Creation_Date_Of_Thread_Converted, '%d-%m-%Y %H:%M:%S')

					# Add the difference between those two times, in seconds, to that list
					time_Difference.append((current_Time_Converted_For_Subtraction - temp_Thread_Time).total_seconds())

				else:
					# Add the difference between the time of the current and next comment into the time_Difference variable
					time_Difference.append((next_Time_Converted_For_Subtraction - current_Time_Converted_For_Subtraction).total_seconds())

			# Whenever the last comment time stamp gets iterated over -> calculate the time difference between thread creation date and that last comment (seconds)
			else:
				# Converts the thread creation date into a comparable time format
				temp_Creation_Date_Of_Thread = float(creation_Date_Of_Thread)
				temp_Creation_Date_Of_Thread_Converted = datetime.datetime.fromtimestamp(temp_Creation_Date_Of_Thread).strftime('%d-%m-%Y %H:%M:%S')

				# Subtracts the comment creation time from the thread creation time
				temp_Thread_Time = datetime.datetime.strptime(temp_Creation_Date_Of_Thread_Converted, '%d-%m-%Y %H:%M:%S')

				# Write the time difference (seconds) between the time the thread has been created and the time the last comment was created
				dict_To_Be_Returned["thread_Livespan"] = int(((current_Time_Converted_For_Subtraction - temp_Thread_Time).total_seconds()))


	# Whenever not a single comment was null.. concrete: Whenever everything is normal and the thread contains answers
	if not are_Comments_Null == True:
		dict_To_Be_Returned["first_Comment_After_Thread_Started"] = int(time_Difference[0])

		# Resorts the time_Difference - List , which is necessary to correctly calculate the median of it
		time_Difference.sort()

		dict_To_Be_Returned["arithmetic_Mean_Response_Time"] = float(np.mean(time_Difference))
		dict_To_Be_Returned["median_Response_Time"] = float(np.median(time_Difference))
		dict_To_Be_Returned["thread_Num_Comments"] = len(time_List)

		# Sorts that dictionary so the dictionary structure is standardized
		dict_To_Be_Returned = collections.OrderedDict(sorted(dict_To_Be_Returned.items()))

	# Return that processed dictionary
	return dict_To_Be_Returned

# <editor-fold desc="Generates data which is about to be plotted later on">
# 1. The creation date of a thread gets determined
# 2. Then the comments will be iterated over, creating a dictionary which is structured as follows:
#   {
#       ('first_Comment_After_Thread_Started', int),
#		('thread_Livespan', int),
#		('arithmetic_Mean_Response_Time', int),
#		('median_Response_Time', int),
#		('id')
#   }
# 3. That returned dictionary will be appended to a global list
# 4. That List will be iterated later on and the appropriate graph will be plotted
# </editor-fold>
def generate_Data_To_Be_Plotted():
	for j, val in enumerate(mongo_DB_Thread_Collection_2009):

		# Skips the system.indexes-table which is automatically created by mongodb itself
		if not val == "system.indexes":
			# References the actual iterated thread
			temp_Thread = mongo_DB_Threads_Instance_2009[val]

			# Gets the creation date of that iterated thread
			temp_Thread_Creation_Time = temp_Thread.find()[0].get("created_utc")


			# printe mir hier alles wo request im Selftext drinsteht
			temp_Thread_Title = temp_Thread.find()[0].get("title")

			# removes iAMA-Requests out of our selection
			if "request" in temp_Thread_Title.lower() \
					and not "as requested" in temp_Thread_Title.lower() \
					and not "by request" in temp_Thread_Title.lower() \
					and not "per request" in temp_Thread_Title.lower() \
					and not "request response" in temp_Thread_Title.lower():
				# Continue skips processing of those elements which are requests here
				# print ("ID of Thread : " + str(val) + "  || Title description: " + str(temp_Thread_Title) ) # won't be printed yet, but if we would switch this line with continue, we would see which ID is a request
				continue

			# Will contain information about time calculation methods
			returned_Dict = calculate_Time_Difference(val, temp_Thread_Creation_Time)

			# Whenever the thread has only one comment, or null comments, or is somehow faulty it won't be added to the global list which is to be plotted later on
			if returned_Dict.get("median_Response_Time") == 0 \
				or returned_Dict.get("first_Comment_After_Thread_Started") == 0 \
				or returned_Dict.get("thread_Livespan") == 0 \
				or returned_Dict.get("arithmetic_Mean_Response_Time") == 0 :

				print ("Thread '" + val + "' will not be added to global list. Therefore it won't be in the plotted graph.")
			else:
				# Add that analyzed data dictionary to the global list which will be plotted later on
				list_To_Be_Plotted.append(returned_Dict)

# <editor-fold desc="Plots the data of the arithmetic mean for that threads">
# Plotts the arithmetic mean - extrema are not filtered here
# </editor-fold>
def plot_The_Generated_Data_Arithmetic_Mean():

	# The dictionary which is necessary to count the amount of response times
	dict_Time_Amount_Counter = {
		"0_To_1"    :   0,
		"1_To_5"    :   0,
		"5_To_10"   :   0,
		"10_To_15"  :   0,
		"15_To_30"  :   0,
		"greater_Than_30": 0
	}

	# Iterates over every element and checks if that value is between some given values
	for i, val in enumerate(list_To_Be_Plotted):
		if (val.get("arithmetic_Mean_Response_Time") / 60) <= 1:
			dict_Time_Amount_Counter["0_To_1"] += 1

		elif ((val.get("arithmetic_Mean_Response_Time") / 60) > 1) and ((val.get("arithmetic_Mean_Response_Time") / 60) <= 5):
			dict_Time_Amount_Counter["1_To_5"] += 1

		elif ((val.get("arithmetic_Mean_Response_Time") / 60) > 5) and ((val.get("arithmetic_Mean_Response_Time") / 60) <= 10):
			dict_Time_Amount_Counter["5_To_10"] += 1

		elif ((val.get("arithmetic_Mean_Response_Time") / 60) > 10) and ((val.get("arithmetic_Mean_Response_Time") / 60) <= 15):
			dict_Time_Amount_Counter["10_To_15"] += 1

		elif ((val.get("arithmetic_Mean_Response_Time") / 60) > 15) and ((val.get("arithmetic_Mean_Response_Time") / 60) <= 30):
			dict_Time_Amount_Counter["15_To_30"] += 1

		elif (val.get("arithmetic_Mean_Response_Time") / 60) > 30:
			dict_Time_Amount_Counter["greater_Than_30"] += 1

	plt.figure()
	# The slices will be ordered and plotted counter-clockwise.
	labels = ['0 bis 1 Min', '1 bis 5 Min', '5 bis 10 Min', '10 bis 15 Min', '15 bis 30 Min', '> 30 Min']
	colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'mediumpurple', 'orange']
	values = [dict_Time_Amount_Counter['0_To_1'],
	         dict_Time_Amount_Counter['1_To_5'],
	         dict_Time_Amount_Counter['5_To_10'],
	         dict_Time_Amount_Counter['10_To_15'],
	         dict_Time_Amount_Counter['15_To_30'],
	         dict_Time_Amount_Counter['greater_Than_30']]

	patches, texts = plt.pie(values, colors=colors, startangle=90, shadow=True)
	plt.pie(values, colors=colors, autopct='%.2f%%')

	plt.legend(patches, labels, loc="best")
	plt.title('iAMA 2009 - Verteilung Ø Antwortzeit per Thread in Minuten')

	# Set aspect ratio to be equal so that pie is drawn as a circle.
	plt.axis('equal')
	plt.tight_layout()
	plt.show()

# Generates the data which will be plotted later on
generate_Data_To_Be_Plotted()

# Filters extrema in minutes
plot_The_Generated_Data_Arithmetic_Mean()