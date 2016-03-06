import collections                                                                                              # Necessary to sort collections alphabetically

import matplotlib.pyplot as plt                                                                                 # Necessary to plot graphs with the data calculated
from pymongo import MongoClient                                                                                 # Necessary to make use of MongoDB
from functools import reduce
from scipy import stats as scistats

# How to check wether it is a question or not
# TODO: ? am Ende eines Satze4s
# TODO: Filterung nach Tier / Hierarchie der Frage möglich?

# 1. Wenn im Commentar ein Fragezeichen drin ist && der Author nicht der iAMA-Ersteller ist --> Frage (und merke dir die commentar_id, und die utc)

# 2. Durchsuche alle Comments, die jene commentar_id als parent_id haben (und wenn die Länge aller Kommentare größer 1 ist)

#   2.1. Wenn es einen entsprechenden Folgekommentar gibt und der Author der iAMA-Ersteller ist --> Antwort

#          2.1.1. Dann merke dir die UTC des iAMA-Hosts-Kommentars
#          2.1.2. Berechne die Difference seit Frage-Erstellung mit Antwort-Erstellung des Hosts (dadurch können wir die Response-Time berechnen)
#          2.1.3. Counte hoch, dass HOST geantwortet hat

#   2.2. Wenn nach allen Iterationen kein Folgekommentar des iAMA-Erstellers gefunden werden kann, welcher sich auf jenen Kommentar bezieht, dann counte hoch, dass Host NICHT geantwortet hat.

# Was können wir dadurch insgesamt berechnen?

# 1.1. Die allgemeine Reaktionszeit des iAMA-Erstellers
# 1.2. Das Verhältnis zu gestellten Fragen und Antworten hierauf durch den iAMA-Host
# 1.3. Das Verhältnis gestellter Fragen zu restlichen (Tier 1 gegen Rest)


# Host Response time

mongo_DB_Client_Instance                =               MongoClient('localhost', 27017)                         # The mongo client, necessary to connect to mongoDB
mongo_DB_Threads_Instance_2009          =               mongo_DB_Client_Instance.iAMA_Reddit_Threads_2009       # The data base instance for the threads
mongo_DB_Thread_Collection_2009         =               mongo_DB_Threads_Instance_2009.collection_names()       # Contains all collection names of the thread database
mongo_DB_Comments_Instance_2009         =               mongo_DB_Client_Instance.iAMA_Reddit_Comments_2009      # The data base instance for the comments
list_To_Be_Plotted                      =               []                                                      # Will contain all analyzed time information for threads & comments

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
	global mongo_DB_Comments_Instance_2009

	comments_Collection = mongo_DB_Comments_Instance_2009[id_Of_Thread]
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
		print ("Thread '" + str(id_Of_Thread) + "' will not be included in the calculation because there are no questions on any Tier greater Tier 1")
		return None

def generate_Data_To_Analyze():
	for j, val in enumerate(mongo_DB_Thread_Collection_2009):

		# Skips the system.indexes-table which is automatically created by mongodb itself
		if not val == "system.indexes":
			# References the actual iterated thread
			temp_Thread = mongo_DB_Threads_Instance_2009[val]

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
				# Continue skips processing of those elements which are requests here
				# print ("ID of Thread : " + str(val) + "  || Title description: " + str(temp_Thread_Title) ) # won't be printed yet, but if we would switch this line with continue, we would see which ID is a request
				continue

			returned_Value = amount_Of_Tier_1_Questions_Percentage(val, temp_Thread_Author)

			if returned_Value is not None:
				list_To_Be_Plotted.append(returned_Value)










# <editor-fold desc="Plots the data of the geometric mean for that threads">
# Plotts the arithmetic mean - extrema are not filtered here
# </editor-fold>
def plot_The_Generated_Data_Percentage_Mean():

	list_Of_X_Tier_Values = []

	for i, val in enumerate(list_To_Be_Plotted):
		list_Of_X_Tier_Values.append(val.get("percentage_Tier_1"))

	print (list_Of_X_Tier_Values)

	geomean = lambda n: reduce(lambda x,y: x*y, list_Of_X_Tier_Values) ** (1.0 / len(list_Of_X_Tier_Values))
	print (geomean)

	# 35.9407537813 - tier X
	# 56.8270911005 - tier 1

	print (str(scistats.gmean(list_Of_X_Tier_Values)))

	print ((reduce(lambda x, y: x*y, list_Of_X_Tier_Values))**(1.0/len(list_Of_X_Tier_Values)))


	plt.figure()
	# The slices will be ordered and plotted counter-clockwise.
	labels = ['0 bis 1 d', '1 bis 3 d', '3 bis 7 d', '7 bis 14 d', '> 14 d']
	colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'orange']
	values = []

	patches, texts = plt.pie(values, colors=colors, startangle=90, shadow=True)
	plt.pie(values, colors=colors, autopct='%.2f%%')

	plt.legend(patches, labels, loc="best")
	plt.title('iAMA 2009 - Ø Lebensspanne eines Threads in Tagen')

	# Set aspect ratio to be equal so that pie is drawn as a circle.
	plt.axis('equal')
	plt.tight_layout()
	plt.show()












generate_Data_To_Analyze()

plot_The_Generated_Data_Percentage_Mean()