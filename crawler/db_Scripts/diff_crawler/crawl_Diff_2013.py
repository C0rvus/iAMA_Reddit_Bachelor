from pymongo        import MongoClient                                                                          # Necessary to interact with MongoDB
from datetime       import datetime                                                                             # Necessary to create the year out of the thread utc [better than hardcoding the db info here]
import praw                                                                                                     # Necessary for praw usage
import collections                                                                                              # Necessary to sort the dictionary before it will be written into the database


mongo_DB_Client_Instance            =               MongoClient('localhost', 27017)                             # The mongo client, necessary to connect to mongoDB

mongo_DB_Threads_Instance_2013      =               mongo_DB_Client_Instance.iAMA_Reddit_Threads_2013           # The data base instance for the threads
mongo_DB_Thread_Collection_2013     =               mongo_DB_Threads_Instance_2013.collection_names()           # Contains all collection names of the thread database


mongo_DB_Comments_Instance_2013     =               mongo_DB_Client_Instance.iAMA_Reddit_Comments_2013          # The data base instance for the comments
mongo_DB_Comments_Collection_2013   =               mongo_DB_Comments_Instance_2013.collection_names()          # Contains all collection names of the comments database


# Retrieves the missing post from reddit and write its comments into the comments database
def crawl_Missing_Collection_Into_Comments_Database(name_Of_Missing_Collection):

	# Because crawling could take many hours / days the previously assigned variables could be old and therefore values could be written twice into the database.
	# Therefore we reassign the actual collection name to double check we do not write data twice

	temp_Mongo_DB_Client_Instance            =               MongoClient('localhost', 27017)                             # The mongo client, necessary to connect to mongoDB
	temp_Mongo_DB_Comments_Instance_2013     =               temp_Mongo_DB_Client_Instance.iAMA_Reddit_Comments_2013          # The data base instance for the comments
	temp_Mongo_DB_Comments_Collection_2013   =               temp_Mongo_DB_Comments_Instance_2013.collection_names()     # Contains all collection names of the comments database

	# Double checks that data so that not both crawler overwrite each other
	if not name_Of_Missing_Collection in temp_Mongo_DB_Comments_Collection_2013:

		# The Main reddit functionality
		reddit_Instance = praw.Reddit(user_agent = "University_Regensburg_iAMA_Crawler_0.001")
		# The thread which is to be crawled
		submission_Thread = reddit_Instance.get_submission(submission_id='' + name_Of_Missing_Collection)

		# Replaces the objects of Type praw.MoreComments with comments (i.e. iterates their tree to the end / expands all comments)
		submission_Thread.replace_more_comments(limit=None, threshold=0)

		# Breaks the tree hierarchy and returns a plain straight aligned list containing all fulltext comments
		flat_comments = praw.helpers.flatten_tree(submission_Thread.comments)

		# Whenever a thread does not contain a single comment -> create a null entry collection inside the database
		if len(flat_comments) == 0:
			print ("    ----- " + str(name_Of_Missing_Collection) + " does not contain single comment. Creation empty collection now")

			# noinspection PyTypeChecker
			data_To_Write_Into_DB = dict({
				'author'        : None,
				'body'          : None,
				'created_utc'   : None,
				'name'          : None,
				'parent_id'     : None,
				'ups'           : None
			})

			# Sorts that dictionary alphabetically ordered
			data_To_Write_Into_DB = collections.OrderedDict(sorted(data_To_Write_Into_DB.items()))

			# Converts the unix utc_time into a date format and converts it to string afterwards
			temp_Submission_Creation_Year = str(datetime.fromtimestamp(submission_Thread.created_utc))
			temp_Submission_Creation_Year = temp_Submission_Creation_Year[:4]

			# This method says to look into the appropriate database, depending on the year the thread was created
			mongo_DB_Reddit = mongo_DB_Client_Instance["iAMA_Reddit_Comments_" + temp_Submission_Creation_Year]

			# Writes the crawled information into the mongoDB
			collection = mongo_DB_Reddit[str(submission_Thread.id)]

			# Write the dictionary "data_To_Write_Into_DB" into the mongo db right now!
			collection.insert_one(data_To_Write_Into_DB)
			print ("    +++++ Finished writing " + str(name_Of_Missing_Collection) + " into " + "iAMA_Reddit_Comments_" + temp_Submission_Creation_Year + "\n")

		# Whenever there were comments / answers within that crawled thread
		else:

			# Iterates over every single comment within the thread [and write it into the appropriate collection in the comments database]
			for idx, val in enumerate(flat_comments):

				# noinspection PyTypeChecker
				data_To_Write_Into_DB = dict({
					'author'        : str(val.author),
					'body'          : str(val.body),
					'created_utc'   : str(val.created_utc),
					'name'          : str(val.name),
					'parent_id'     : str(val.parent_id),
					'ups'           : int(val.ups)
				})

				# Sorts that dictionary alphabetically ordered
				data_To_Write_Into_DB = collections.OrderedDict(sorted(data_To_Write_Into_DB.items()))

				# Converts the unix utc_time into a date format and converts it to string afterwards
				temp_Submission_Creation_Year = str(datetime.fromtimestamp(submission_Thread.created_utc))
				temp_Submission_Creation_Year = temp_Submission_Creation_Year[:4]

				# This method says to look into the appropriate database, depending on the year the thread was created
				mongo_DB_Reddit = mongo_DB_Client_Instance["iAMA_Reddit_Comments_" + temp_Submission_Creation_Year]

				# Writes the crawled information into the mongoDB
				collection = mongo_DB_Reddit[str(submission_Thread.id)]

				# Write the dictionary "data_To_Write_Into_DB" into the mongo db right now!
				collection.insert_one(data_To_Write_Into_DB)

			print ("    +++++ Finished writing " + str(name_Of_Missing_Collection) + " into " + "iAMA_Reddit_Comments_2013" + "\n")

# Checks whether every collection, which exists in thread database, is also available in the comments database
def check_If_Collection_Is_Missing_In_Comments_Database():

	# Iterate over every collection within the thread database
	for j in range (0, len(mongo_DB_Thread_Collection_2013)):

		# If that iterated collection does not exist within the comments database - get that data and create that collection
		if not mongo_DB_Thread_Collection_2013[j] in mongo_DB_Comments_Collection_2013:
			print ("The following collection is missing in iAMA_Reddit_Comments_2013 : " + mongo_DB_Thread_Collection_2013[j])
			crawl_Missing_Collection_Into_Comments_Database(str(mongo_DB_Thread_Collection_2013[j]))




# Retrieves the missing post from reddit and write its properties into the threads database
def crawl_Missing_Collection_Into_Threads_Database(name_Of_Missing_Collection):

	# Because crawling could take many hours / days the previously assigned variables could be old and therefore values could be written twice into the database.
	# Therefore we reassign the actual collection name to double check we do not write data twice

	temp_Mongo_DB_Client_Instance            =               MongoClient('localhost', 27017)                             # The mongo client, necessary to connect to mongoDB
	temp_Mongo_DB_Threads_Instance_2013      =               temp_Mongo_DB_Client_Instance.iAMA_Reddit_Threads_2013           # The data base instance for the threads
	temp_Mongo_DB_Thread_Collection_2013     =               temp_Mongo_DB_Threads_Instance_2013.collection_names()      # Contains all collection names of the thread database

	# Double checks that data so that not both crawler overwrite each other
	if not name_Of_Missing_Collection in temp_Mongo_DB_Thread_Collection_2013:

		# The Main reddit functionality
		reddit_Instance = praw.Reddit(user_agent = "University_Regensburg_iAMA_Crawler_0.001")
		# The thread which is to be crawled
		submission = reddit_Instance.get_submission(submission_id='' + name_Of_Missing_Collection)

		# Because down votes are not accessable via reddit API, we have calculated it by our own here
		ratio = reddit_Instance.get_submission(submission.permalink).upvote_ratio
		total_Votes = int(round((ratio*submission.score)/(2*ratio - 1)) if ratio != 0.5 else round(submission.score/2))
		downs = total_Votes - submission.score

		# noinspection PyTypeChecker
		data_To_Write_Into_DB = dict({
			'author'        : str(submission.author),
			'created_utc'   : str(submission.created_utc),
			'downs'         : int(downs),
			'num_Comments'  : str(submission.num_comments),
			'selftext'      : str(submission.selftext),
			'title'         : str(submission.title),
			'ups'           : int(submission.ups)
		})

		# Sorts that dictionary alphabetically ordered
		data_To_Write_Into_DB = collections.OrderedDict(sorted(data_To_Write_Into_DB.items()))

		# Converts the unix utc_time into a date format and converts it to string afterwards
		temp_Submission_Creation_Year = str(datetime.fromtimestamp(submission.created_utc))
		temp_Submission_Creation_Year = temp_Submission_Creation_Year[:4]

		# This method says to look into the appropriate database, depending on the year the thread was created
		mongo_DB_Reddit = mongo_DB_Client_Instance["iAMA_Reddit_Threads_" + temp_Submission_Creation_Year]

		# Writes the crawled information into the mongoDB
		collection = mongo_DB_Reddit[str(submission.id)]

		# Write the dictionary "data_To_Write_Into_DB" into the mongo db right now!
		collection.insert_one(data_To_Write_Into_DB)

		print ("    +++++ Finished writing " + str(name_Of_Missing_Collection) + " into " + "iAMA_Reddit_Threads_" + temp_Submission_Creation_Year + "\n")

# Checks whether every collection, which exists in comments database, is also available in the threads database
def check_If_Collection_Is_Missing_In_Threads_Database():

	# Iterate over every collection within the comments database
	for j in range (0, len(mongo_DB_Comments_Collection_2013)):

		# If that iterated collection does not exist within the thread database - get that data and create that collection
		if not mongo_DB_Comments_Collection_2013[j] in mongo_DB_Thread_Collection_2013:
			print ("The following collection is missing in iAMA_Reddit_Threads_2013 : " + mongo_DB_Comments_Collection_2013[j])
			crawl_Missing_Collection_Into_Threads_Database(str(mongo_DB_Comments_Collection_2013[j]))





# Creates missing collections within the comments database
check_If_Collection_Is_Missing_In_Comments_Database()

# Creates missing collections within the threads database
check_If_Collection_Is_Missing_In_Threads_Database()