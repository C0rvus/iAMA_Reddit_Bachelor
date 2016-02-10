from pymongo        import MongoClient                                                                                                  # necessary to interact with MongoDB
from datetime       import datetime
import praw                                                                                                                             # necessary for praw usage
import collections
                                                                                                          # Necessary to calculate time shifting windows for onward crawling

mongo_DB_Client_Instance            =               MongoClient('localhost', 27017)                                                     # the mongo client, necessary to connect to mongoDB

mongo_DB_Threads_Instance_2009      =              mongo_DB_Client_Instance.iAMA_Reddit_Threads_2009                                                # the collection (table), in which reddit information will be stored _ for test cases
mongo_DB_Thread_Collection_2009     =              mongo_DB_Threads_Instance_2009.collection_names()


mongo_DB_Comments_Instance_2009     =               mongo_DB_Client_Instance.iAMA_Reddit_Comments_2009                                                # the collection (table), in which reddit information will be stored _ for test cases
mongo_DB_Comments_Collection_2009   =               mongo_DB_Comments_Instance_2009.collection_names()

#vice versa, also in beide Richtungen machen !


def crawl_Missing_Collection_Into_Comments_Database(name_Of_Missing_Collection):
	reddit_Instance                     =               praw.Reddit(user_agent = "University_Regensburg_diff_Crawler_0.001")                # main reddit functionality
	submission_Thread = reddit_Instance.get_submission(submission_id='' + name_Of_Missing_Collection)

	# Replaces the objects of Type praw.MoreComments with comments (i.e. iterates their tree to the end / expands all comments)
	submission_Thread.replace_more_comments(limit=None, threshold=0)

	# Breaks the tree hierarchy and returns a plain straight aligned list containing all fulltext comments
	flat_comments = praw.helpers.flatten_tree(submission_Thread.comments)

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
	else:

		# Iterates over every single comment within the thread
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

			print ("    +++++ Finished writing " + str(name_Of_Missing_Collection) + " into " + "iAMA_Reddit_Comments_" + temp_Submission_Creation_Year + "\n")


def check_If_Collection_Is_Missing_In_Comments_Database():

	for j in range (0, len(mongo_DB_Thread_Collection_2009)):

		#Whenever a collection which is in the threads database does not exist within the comments database
		if not mongo_DB_Thread_Collection_2009[j] in mongo_DB_Comments_Collection_2009:
			print ("The following collection is missing in iAMA_Reddit_Comments_2009 : " + mongo_DB_Thread_Collection_2009[j])
			crawl_Missing_Collection_Into_Comments_Database(str(mongo_DB_Thread_Collection_2009[j]))


check_If_Collection_Is_Missing_In_Comments_Database()