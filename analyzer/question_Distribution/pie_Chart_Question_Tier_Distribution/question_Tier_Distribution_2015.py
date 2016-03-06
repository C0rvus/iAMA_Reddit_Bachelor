import collections                                                                                              # Necessary to sort collections alphabetically
import matplotlib.pyplot as plt                                                                                 # Necessary to plot graphs with the data calculated
from pymongo import MongoClient                                                                                 # Necessary to make use of MongoDB
import numpy as np

mongo_DB_Client_Instance                =               MongoClient('localhost', 27017)                         # The mongo client, necessary to connect to mongoDB
mongo_DB_Threads_Instance_2015          =               mongo_DB_Client_Instance.iAMA_Reddit_Threads_2015       # The data base instance for the threads
mongo_DB_Thread_Collection_2015         =               mongo_DB_Threads_Instance_2015.collection_names()       # Contains all collection names of the thread database
mongo_DB_Comments_Instance_2015         =               mongo_DB_Client_Instance.iAMA_Reddit_Comments_2015      # The data base instance for the comments
list_To_Be_Plotted                      =               []                                                      # Will contain all analyzed time information for threads & comments

# Calculates the distribution of tier 1 questions in contrast to questions which are not tier 1 in percent
def calculate_Percentage_Distribution(amount_Of_Tier_1_Questions, amount_Of_Tier_X_Questions):

	full_Percent = amount_Of_Tier_1_Questions + amount_Of_Tier_X_Questions
	percentage_Tier_1 = (amount_Of_Tier_1_Questions / full_Percent) * 100
	percentage_Tier_X = 100 - percentage_Tier_1

	dict_To_Be_Returned = {
		"percentage_Tier_1" :   percentage_Tier_1,
		"percentage_Tier_X" :   percentage_Tier_X
	}

	return dict_To_Be_Returned

# Checks whether the postet comment is not from the thread creator
def check_If_Comment_Is_From_Thread_Author(author_Of_Thread, comment_Author):

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
def amount_Of_Tier_1_Questions_Percentage(id_Of_Thread, author_Of_Thread):
	# print ("Processsing : " + str(id_Of_Thread) + " ... author: " + str(author_Of_Thread))

	# Makes the global comments instance locally available here
	global mongo_DB_Comments_Instance_2015

	comments_Collection = mongo_DB_Comments_Instance_2015[id_Of_Thread]
	comments_Cursor = comments_Collection.find()

	# Contains the amount of questions done on the first level of a thread
	amount_Of_Tier_1_Questions = 0

	# Contains the amount of questions done on every sublevel, except on tier 1
	amount_Of_Tier_X_Questions = 0

	# Iterates over every comment within that thread
	for collection in comments_Cursor:

		# Whenever the iterated comment was created by user "AutoModerator" skip it
		if (collection.get("author")) != "AutoModerator":

			# References the text of the comment
			comment_Text = collection.get("body")
			comment_Author = collection.get("author")
			comment_Parent_Id = collection.get("parent_id")

			# Whenever some values are not None.. (Values can be null / None, whenever they have been deleted)
			if comment_Text is not None \
				and comment_Author is not None \
				and comment_Parent_Id is not None :

				bool_Comment_Is_Question = check_If_Comment_Is_A_Question(comment_Text)
				bool_Comment_Is_Question_On_Tier_1 = check_If_Comment_Is_On_Tier_1(comment_Parent_Id)
				bool_Comment_Is_Not_From_Thread_Author = check_If_Comment_Is_From_Thread_Author(author_Of_Thread, comment_Author)

				# If the posted comment is a question and is not from the thread author and is on Tier 1
				if (bool_Comment_Is_Question == True) \
					and (bool_Comment_Is_Question_On_Tier_1 == True) \
					and (bool_Comment_Is_Not_From_Thread_Author == True):

					amount_Of_Tier_1_Questions += 1

				# If the postet comment is a question and is not from the from the thread author and is on any other level except Tier 1
				elif (bool_Comment_Is_Question == True) \
					and (bool_Comment_Is_Not_From_Thread_Author == True):

					amount_Of_Tier_X_Questions += 1

			# Whenever a comment has been deleted or has, somehow, null values in it.. do not process it
			else:
				# print ("Thread '" + str(id_Of_Thread) + "' will not be included in the calculation due to null values")
				continue



	# Checks if there has been done some calculation or not
	if (amount_Of_Tier_X_Questions != 0) \
		and (amount_Of_Tier_1_Questions != 0):

		dict_To_Be_Returned_Percentage_Time = calculate_Percentage_Distribution(amount_Of_Tier_1_Questions, amount_Of_Tier_X_Questions)
		dict_To_Be_Returned_Percentage_Time = collections.OrderedDict(sorted(dict_To_Be_Returned_Percentage_Time.items()))
		return dict_To_Be_Returned_Percentage_Time

	# Whenever there were no tier X questions asked.. so all questions remained on tier 1
	else:
		print ("Thread '" + str(id_Of_Thread) + "' will not be included in the calculation because there are no questions on any tier greater than tier 1")
		return None

# Generates the data which will be analyzed later on
def generate_Data_To_Analyze():
	for j, val in enumerate(mongo_DB_Thread_Collection_2015):

		# Skips the system.indexes-table which is automatically created by mongodb itself
		if not val == "system.indexes":
			# References the actual iterated thread
			temp_Thread = mongo_DB_Threads_Instance_2015[val]

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

			returned_Value = amount_Of_Tier_1_Questions_Percentage(val, temp_Thread_Author)

			# Value could be none if it has i.E. no values
			if returned_Value is not None:
				list_To_Be_Plotted.append(returned_Value)

# Plots the data of the question distribution for that year
def plot_The_Generated_Data_Percentage_Mean():

	# Will contain the amount of questions which are not tier 1 questions
	list_Of_Tier_X_Values = []

	# Iterates over every value and gets the tier_X value
	for i, val in enumerate(list_To_Be_Plotted):
		list_Of_Tier_X_Values.append(val.get("percentage_Tier_X"))

	# Contains the amount of questions which are asked, but not on tier 1
	percentage_Mean_Of_Tier_X = np.mean(list_Of_Tier_X_Values)

	# Prints the average percentage amount of Tier X questions
	print ("Percentage of questions on Tier_1: " + str(100 - percentage_Mean_Of_Tier_X) + " %")
	print ("Percentage of questions on Tier_X: " + str(percentage_Mean_Of_Tier_X) + " %")

	plt.figure()

	# The slices will be ordered and plotted counter-clockwise.
	labels = ['Rang 1', 'Andere Ränge']
	colors = ['yellowgreen', 'gold']
	values = [100 - percentage_Mean_Of_Tier_X, percentage_Mean_Of_Tier_X]

	patches, texts = plt.pie(values, colors=colors, startangle=90, shadow=True)
	plt.pie(values, colors=colors, autopct='%.2f%%')

	plt.legend(patches, labels, loc="upper right")
	plt.title('iAMA 2015 - Ø Verteilung von Fragen in Threadhierarchie')

	# Set aspect ratio to be equal so that pie is drawn as a circle.
	plt.axis('equal')
	plt.tight_layout()
	plt.show()

# Generates the data which will be plotted later on
generate_Data_To_Analyze()

# Plots a pie chart containing the tier 1 question distribution
plot_The_Generated_Data_Percentage_Mean()