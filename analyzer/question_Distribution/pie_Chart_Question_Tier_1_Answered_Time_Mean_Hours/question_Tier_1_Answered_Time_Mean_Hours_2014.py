import matplotlib.pyplot as plt                                                                                 # Necessary to plot graphs with the data calculated
import datetime                                                                                                 # Necessary to do time calculation
from pymongo import MongoClient                                                                                 # Necessary to make use of MongoDB
import numpy as np

mongo_DB_Client_Instance                =               MongoClient('localhost', 27017)                         # The mongo client, necessary to connect to mongoDB
mongo_DB_Threads_Instance_2014          =               mongo_DB_Client_Instance.iAMA_Reddit_Threads_2014       # The data base instance for the threads
mongo_DB_Thread_Collection_2014         =               mongo_DB_Threads_Instance_2014.collection_names()       # Contains all collection names of the thread database
mongo_DB_Comments_Instance_2014         =               mongo_DB_Client_Instance.iAMA_Reddit_Comments_2014      # The data base instance for the comments
list_To_Be_Plotted                      =               []                                                      # Will contain all analyzed time information for threads & comments

def calculate_Time_Difference(comment_Time_Stamp, answer_Time_Stamp_IAMA_Host):

	# Converts the time_Value into float, otherwise it could not be processed any further...
	comment_Time_Value = float(comment_Time_Stamp)
	comment_Time_Converted = datetime.datetime.fromtimestamp(comment_Time_Value).strftime('%d-%m-%Y %H:%M:%S')
	comment_Time_Converted_For_Subtraction = datetime.datetime.strptime(comment_Time_Converted, '%d-%m-%Y %H:%M:%S')

	# Converts the time_Value into float, otherwise it could not be processed any further...
	answer_Time_IAMA_Host = float(answer_Time_Stamp_IAMA_Host)
	answer_Time_IAMA_Host_Converted = datetime.datetime.fromtimestamp(answer_Time_IAMA_Host).strftime('%d-%m-%Y %H:%M:%S')
	answer_Time_IAMA_Host_Converted_For_Subtraction = datetime.datetime.strptime(answer_Time_IAMA_Host_Converted, '%d-%m-%Y %H:%M:%S')

	# Calculates the time difference between the comment and the iAMA hosts answer
	time_Difference_In_Seconds = (answer_Time_IAMA_Host_Converted_For_Subtraction - comment_Time_Converted_For_Subtraction).total_seconds()

	return time_Difference_In_Seconds

# Calculates the distribution of tier 1 questions in contrast to questions which are not tier 1 in percent
def calculate_Percentage_Distribution(amount_Of_Tier_1_Questions, amount_Of_Tier_1_Questions_Answered):

	percentage_Tier_1_Answered      = (amount_Of_Tier_1_Questions_Answered / amount_Of_Tier_1_Questions) * 100
	percentage_Tier_1_Not_Answered  = (100 - percentage_Tier_1_Answered)

	dict_To_Be_Returned = {
		"percentage_Tier_1_Answered"    :   percentage_Tier_1_Answered,
		"percentage_Tier_1_Not_Answered":   percentage_Tier_1_Not_Answered
	}

	return dict_To_Be_Returned

# Checks whether the thread host has answered a given question
def check_If_Comment_Is_Answer_From_Thread_Author(author_Of_Thread, comment_Acutal_Id, comments_Cursor):

	dict_To_Be_Returned = {
		"question_Answered_From_Host"   :   False,
		"time_Stamp_Answer"             :   0
	}

	# Iterates over every comment
	for collection in comments_Cursor:

		# Whenever the iterated comment was created by user "AutoModerator" skip it
		if (collection.get("author")) != "AutoModerator":
			check_Comment_Parent_Id = collection.get("parent_id")
			actual_Comment_Author = collection.get("author")

			# Whenever the iterated comment is from the iAMA-Host and that comment has the question as parent_id
			if (check_If_Comment_Is_Not_From_Thread_Author(author_Of_Thread, actual_Comment_Author) == False) \
					and (check_Comment_Parent_Id == comment_Acutal_Id):

				dict_To_Be_Returned["question_Answered_From_Host"] = True
				dict_To_Be_Returned["time_Stamp_Answer"] = collection.get("created_utc")

				return dict_To_Be_Returned
			else:
				return dict_To_Be_Returned
		else:
			return dict_To_Be_Returned

	# This is the case whenever a comment has not a single thread
	return dict_To_Be_Returned

# Checks whether the postet comment is not from the thread creator
def check_If_Comment_Is_Not_From_Thread_Author(author_Of_Thread, comment_Author):

	if author_Of_Thread != comment_Author:
		return True
	else:
		return False

# Checks wether the question is on Tier-1 Hierarchy or not
def check_If_Comment_Is_On_Tier_1(comment_Parent_Id):

	if "t3_" in  comment_Parent_Id:
		return True
	else:
		return False

# Could be expanded later on, if checking for question mark is not enough
def check_If_Comment_Is_A_Question(given_String):

	if "?" in given_String:
		return True
	else:
		return False

# Calculates the amount of Tier 1 questions in contrast to the other Tiers
def calculate_Ar_Mean_Answer_Time_For_Tier_1_Questions(id_Of_Thread, author_Of_Thread):
	# print ("Processsing : " + str(id_Of_Thread) + " ... author: " + str(author_Of_Thread))

	# Makes the global comments instance locally available here
	global mongo_DB_Comments_Instance_2014

	comments_Collection = mongo_DB_Comments_Instance_2014[id_Of_Thread]
	comments_Cursor = comments_Collection.find()

	amount_Of_Answer_Times = []

	amount_Of_Tier_1_Questions = 0
	amount_Of_Tier_1_Questions_Answered = 0


	# Iterates over every comment within that thread
	for collection in comments_Cursor:

		# Whenever the iterated comment was created by user "AutoModerator" skip it
		if (collection.get("author")) != "AutoModerator":

			# References the text of the comment
			comment_Text = collection.get("body")
			comment_Author = collection.get("author")
			comment_Parent_Id = collection.get("parent_id")
			comment_Acutal_Id = collection.get("name")
			comment_Time_Stamp = collection.get("created_utc")

			# Whenever some values are not None.. (Values can be null / None, whenever they have been deleted)
			if comment_Text is not None \
				and comment_Author is not None \
				and comment_Parent_Id is not None :

				bool_Comment_Is_Question = check_If_Comment_Is_A_Question(comment_Text)
				bool_Comment_Is_Question_On_Tier_1 = check_If_Comment_Is_On_Tier_1(comment_Parent_Id)
				bool_Comment_Is_Not_From_Thread_Author = check_If_Comment_Is_Not_From_Thread_Author(author_Of_Thread, comment_Author)

				# If the posted comment is a question and is not from the thread author and is on Tier 1
				if (bool_Comment_Is_Question == True) \
					and (bool_Comment_Is_Question_On_Tier_1 == True) \
					and (bool_Comment_Is_Not_From_Thread_Author == True):

					amount_Of_Tier_1_Questions += 1

					# Check whether that iterated comment is answered by the host
					answer_Is_From_Thread_Author = check_If_Comment_Is_Answer_From_Thread_Author(author_Of_Thread, comment_Acutal_Id, comments_Cursor)

					# Whenever the answer to that comment is from the author (boolean == True)
					if answer_Is_From_Thread_Author["question_Answered_From_Host"] is True:
						answer_Time_Stamp_IAMA_Host = answer_Is_From_Thread_Author["time_Stamp_Answer"]

						# Adds the calculated answer time to a local list
						amount_Of_Answer_Times.append(calculate_Time_Difference(comment_Time_Stamp, answer_Time_Stamp_IAMA_Host))
						
						amount_Of_Tier_1_Questions_Answered += 1

				# Skip that comment
				else:
					continue

			# Whenever a comment has been deleted or has, somehow, null values in it.. do not process it
			else:
				# print ("Thread '" + str(id_Of_Thread) + "' will not be included in the calculation due to null values")
				continue

	# Whenever there were some questions aksed on tier 1 and those questions have been answered by the iAMA host on tier 1
	if amount_Of_Tier_1_Questions != 0 and amount_Of_Tier_1_Questions_Answered != 0:

		# Returns the arithmetic mean of answer time by the iAMA host
		return np.mean(amount_Of_Answer_Times)

	#Whenever there were no tier X questions asked.. so all questions remained on tier 1
	else:
		print ("Thread '" + str(id_Of_Thread) + "' will not be included in the calculation because there are no questions asked on tier 1")
		return None


# Generates the data which will be analyzed later on
def generate_Data_To_Analyze():
	for j, val in enumerate(mongo_DB_Thread_Collection_2014):

		# Skips the system.indexes-table which is automatically created by mongodb itself
		if not val == "system.indexes":
			# References the actual iterated thread
			temp_Thread = mongo_DB_Threads_Instance_2014[val]

			# Gets the creation date of that iterated thread
			temp_Thread_Author = temp_Thread.find()[0].get("author")

			# Gets the title of that iterated thread
			temp_Thread_Title = temp_Thread.find()[0].get("title")

			# removes iAMA-Requests out of our selection
			if "request" in temp_Thread_Title.lower() \
					and not "as requested" in temp_Thread_Title.lower() \
					and not "by request" in temp_Thread_Title.lower() \
					and not "per request" in temp_Thread_Title.lower() \
					and not "request response" in temp_Thread_Title.lower():
				continue

			returned_Value = calculate_Ar_Mean_Answer_Time_For_Tier_1_Questions(val, temp_Thread_Author)

			# Value could be none if it has i.E. no values
			if returned_Value is not None:
				list_To_Be_Plotted.append(returned_Value)

# Plots the data of the question distribution for that year
def plot_The_Generated_Data_Percentage_Mean():

	# The dictionary which is necessary to count the amount of response times in Minutes
	dict_Time_Amount_Counter = {
		"0_To_1"    :   0,
		"1_To_6"    :   0,
		"6_To_12"   :   0,
		"12_To_24"  :   0,
		"24_To_48"  :   0,
		"greater_Than_48": 0
	}

	# Iterates over every value and fills the dict_Time_Amount_Counter appropriate
	for i, val in enumerate(list_To_Be_Plotted):

		if 0 < (val / 3600) <= 1:
			dict_Time_Amount_Counter["0_To_1"] += 1

		elif 1 < (val / 3600) <= 6:
			dict_Time_Amount_Counter["1_To_6"] += 1

		elif 6 < (val / 3600) <= 12:
			dict_Time_Amount_Counter["6_To_12"] += 1

		elif 12 < (val / 3600) <= 24:
			dict_Time_Amount_Counter["12_To_24"] += 1

		elif 24 < (val / 3600) <= 48:
			dict_Time_Amount_Counter["24_To_48"] += 1

		elif (val / 3600) > 48:
			dict_Time_Amount_Counter["greater_Than_48"] += 1


	plt.figure()

	# The slices will be ordered and plotted counter-clockwise.
	labels = ['0 bis 1 h', '1 bis 6 h', '6 bis 12 h', '12 bis 24 h', '24 bis 48 h', '> 48 h']
	colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'mediumpurple', 'orange']
	values = [dict_Time_Amount_Counter['0_To_1'],
	         dict_Time_Amount_Counter['1_To_6'],
	         dict_Time_Amount_Counter['6_To_12'],
	         dict_Time_Amount_Counter['12_To_24'],
	         dict_Time_Amount_Counter['24_To_48'],
	         dict_Time_Amount_Counter['greater_Than_48']]

	patches, texts = plt.pie(values, colors=colors, startangle=90, shadow=True)
	plt.pie(values, colors=colors, autopct='%.2f%%')

	plt.legend(patches, labels, loc="upper left")
	plt.title('iAMA 2014 - Ø Reaktionszeit des iAMA-Host auf Fragen auf Ebene 1 in Stunden')

	# Set aspect ratio to be equal so that pie is drawn as a circle.
	plt.axis('equal')
	plt.tight_layout()
	plt.show()

# Generates the data which will be plotted later on
generate_Data_To_Analyze()

# Plots a pie chart containing the tier 1 question distribution
plot_The_Generated_Data_Percentage_Mean()