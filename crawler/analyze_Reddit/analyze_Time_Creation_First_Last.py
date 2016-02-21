# Calculation polarity / subjectivity
# print (TextBlob("Textblob is amazingly simple to use. What great fun!").sentiment)
# TODO: Textlänge, Wortkategorisierung, Erkennung ob Frage oder Satz / Antwort
# TODO: 4. Die Durchschnittsdauer der Antworten berechnen
# TODO: Datentyp aufbau [erster Comment, letzer Comment, Durchschnittsantwortszeit, Mean-Antwortszeit]
# TODO: Dict noch sortieren, damit es echt einheitlich ist !

from pymongo import MongoClient
import datetime
import numpy as np
import collections
import matplotlib.pyplot as plt

client                                  =               MongoClient('localhost', 27017)                                                     # the mongo client, necessary to connect to mongoDB


# Gets the time of the created thread
def get_Creation_Time_Of_Thread():
	threads_Mongo_DB_Reddit             =               client.iAMA_Reddit_Threads_2016
	threads_Collection                  =               threads_Mongo_DB_Reddit["3z1jf4"]
	threads_Cursor                      =               threads_Collection.find()

	# print (threads_Cursor[0].get("created_utc"))
	# print ("Zeit von Thread umgewandelt: " + datetime.datetime.fromtimestamp(1451673724).strftime('%Y-%m-%d %H:%M:%S.%f'))
	# print ("Zeit von Thread umgewandelt: " + datetime.datetime.fromtimestamp(1451673724).strftime('%d-%m-%Y %H:%M:%S'))



def calculate_Time_Difference(creation_Date_Of_Thread):
	comments_Mongo_DB_Reddit             =               client.iAMA_Reddit_Comments_2016
	comments_Collection                  =               comments_Mongo_DB_Reddit["3z1jf4"]
	comments_Cursor                      =               comments_Collection.find()

	# Contains the creation date of every comment
	time_List = []

	# Contains the time difference between every comment in seconds
	time_Difference = []

	dict_To_Be_Returned = {
		"first_Comment_After_Thread_Started"    :   0,
		"last_Comment_After_Thread_Started"     :   0,
		"arithmetic_Mean_Response_Time"         :   0,
		"median_Response_Time"                  :   0
	}

	# Iterates over every time stamp and writes it into time_List
	# Additionally comments from AutoModerator-Bot are beeing ingored because they skew our statistics and would be created with the same timestamp like the thread itself
	for collection in comments_Cursor:
		# Whenever the iterated comment was created by user "AutoModerator" skip it
		if (collection.get("author")) != "AutoModerator":
			time_List.append(collection.get("created_utc"))


	# This sorts the time in an ascending way
	time_List.sort()

	# Calculate the time difference within here
	for i, time_Value in enumerate(time_List):

		# Convert the time_Value into float, otherwise it could not be converted...
		time_Value_Current = float(time_Value)
		current_Time_Converted = datetime.datetime.fromtimestamp(time_Value_Current).strftime('%d-%m-%Y %H:%M:%S')
		current_Time_Converted_For_Subtraction = datetime.datetime.strptime(current_Time_Converted, '%d-%m-%Y %H:%M:%S')

		# Whenever the last list object is iterated over skip anything because there will be no future object
		if i != len(time_List) - 1:
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
				#print ("Momentane Zeit fuer Subtract: " + str(current_Time_Converted_For_Subtraction) + " ||||| " + "Zeit fuer naechsten Thread: " + str(next_Time_Converted_For_Subtraction))
				time_Difference.append((next_Time_Converted_For_Subtraction - current_Time_Converted_For_Subtraction).total_seconds())

		# Whenever the last comment time stamp gets iterated over -> calculate the time difference between thread creation date and that last comment (seconds)
		else:
			# Converts the thread creation date into a comparable time format
			temp_Creation_Date_Of_Thread = float(creation_Date_Of_Thread)
			temp_Creation_Date_Of_Thread_Converted = datetime.datetime.fromtimestamp(temp_Creation_Date_Of_Thread).strftime('%d-%m-%Y %H:%M:%S')

			# Subtracts the comment creation time from the thread creation time
			temp_Thread_Time = datetime.datetime.strptime(temp_Creation_Date_Of_Thread_Converted, '%d-%m-%Y %H:%M:%S')

			# Write the time difference (seconds) between the time the thread has been created and the time the last comment was created
			dict_To_Be_Returned["last_Comment_After_Thread_Started"] = int(((current_Time_Converted_For_Subtraction - temp_Thread_Time).total_seconds()))



	print (time_Difference)
	dict_To_Be_Returned["first_Comment_After_Thread_Started"] = int(time_Difference[0])

	# Resorts the time_Difference - List , which is necessary to correctly calculate the median of it
	time_Difference.sort()

	dict_To_Be_Returned["arithmetic_Mean_Response_Time"] = int(np.mean(time_Difference))
	dict_To_Be_Returned["median_Response_Time"] = int(np.median(time_Difference))

	# Sorts that dictionary so the dictionary structure is standardized
	dict_To_Be_Returned = collections.OrderedDict(sorted(dict_To_Be_Returned.items()))


	print (dict_To_Be_Returned)

# This method plots a graph to show the graphical distribution
def draw_Graph():
	# Source: http://www.scipy-lectures.org/intro/matplotlib/matplotlib.html#bar-plots
	# Source: https://plot.ly/matplotlib/bar-charts/

	print ("ICH BIN DA")
	y = [3, 10, 7, 5, 3, 4.5, 6, 8.1]
	N = len(y)
	x = range(N)
	width = 1/1.5
	plt.bar(x, y, width, color="blue")
	#Y2 = (1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)

	#plt.bar(X, +Y1, facecolor='#9999ff', edgecolor='white')
	#plt.bar(X, -Y2, facecolor='#ff9999', edgecolor='white')

	#for x, y in zip(X, Y1):
	#    plt.text(x + 0.4, y + 0.05, '%.2f' % y, ha='center', va='bottom')

	# plt.ylim(0, +1.25)


	plt.show()


get_Creation_Time_Of_Thread()
calculate_Time_Difference(str(1451673724))
draw_Graph()