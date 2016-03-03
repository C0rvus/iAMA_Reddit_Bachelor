#   Tutorials used within this class:
#   1. (06.02.2016 @ 15:23) - http://www.esqsoft.com/javascript_examples/date-to-epoch.htm
#   2. (06.02.2016 @ 15:48) - https://www.reddit.com/r/redditdev/comments/2zdyy2/praw_continue_getting_posts_after_given_post_id/
#   3. (06.02.2016 @ 16:20) - https://www.linuxquestions.org/questions/programming-9/python-datetime-to-epoch-4175520007/
#   4. (06.02.2016 @ 16:30) - https://stackoverflow.com/questions/11743019/convert-python-datetime-to-epoch-with-strftime
#   This script is developed with PRAW 3.3.0

import praw, time, collections                                                                                  # Necessary to make use of Reddit-API, time calculation and dictionary sorting
from pymongo  import MongoClient                                                                                # Necessary to interact with MongoDB
from datetime import datetime, timedelta                                                                        # Necessary to calculate time shifting windows for onward crawling


mongo_DB_Client_Instance    =       MongoClient('localhost', 27017)                                             # The mongo client, necessary to connect to mongoDB
reddit_Instance             =       praw.Reddit(user_agent = "University_Regensburg_iAMA_Crawler_0.001")        # The Main reddit functionality
hours_To_Move_On            =       96                                                                          # Defines the crawling time frame in hours
x                           =       1356994800                                                                  # Starting time of the first iAMA post of Reddit 	[ 2013-01-01 00:00:00 ]
end_Value			        =       1388530800		                                                            # Ending time where crawling should be stopped		[ 2014-01-01 00:00:00 ]

# <editor-fold desc="Description of y inside here">
# 1. At first 8 hours are added to the epoch format of x
#   1.1. At this step epoch gets converted to String
# 2. String gets converted back to epoch time
#   2.1. Due to conversion the time is in float format [1201907536.0]
# 3. Converts float to int while rounding it
#   3.1. Rounding does not the numbers in front of the comma [1201907536]
# </editor-fold>
y                   = int(round(time.mktime((datetime.fromtimestamp(x) + timedelta(hours=hours_To_Move_On)).timetuple())))

# This method crawls the data base for the year 2013
def crawl_Whole_Reddit_For_Comments():
	global x, y

	# Below is the crawl command to search within a dedicated time span from x to y. Time is used in epoch format
	posts = reddit_Instance.search('timestamp:' + str(x) + '..' + str(y), subreddit='iAMA', sort="new", limit=1000, syntax="cloudsearch")
	for submission in posts:

		# Whenver the collection already exists in the database                 (True)
		if check_If_Coll_In_DB_Already_Exists_Up2Date(submission):
			print ("++ Comments for " + str(submission.id) + " already exist in mongoDB and is up2date")

		# Whenever the thread does not yet exist within the mongoDB (anymore)   (False)
		else:
			print ("    -- Comments for " + str(submission.id) + " will be created now")

			# Replaces the objects of Type praw.MoreComments with comments (i.e. iterates their tree to the end / expands all comments)
			submission.replace_more_comments(limit=None, threshold=0)

			# Breaks the tree hierarchy and returns a plan straight aligned list containing all fulltext comments
			flat_comments = praw.helpers.flatten_tree(submission.comments)

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
				temp_Submission_Creation_Year = str(datetime.fromtimestamp(submission.created_utc))
				temp_Submission_Creation_Year = temp_Submission_Creation_Year[:4]

				# This method says to look into the appropriate database, depending on the year the thread was created
				mongo_DB_Reddit = mongo_DB_Client_Instance["iAMA_Reddit_Comments_" + temp_Submission_Creation_Year]

				# Writes the crawled information into the mongoDB
				collection = mongo_DB_Reddit[str(submission.id)]

				# Write the dictionary "data_To_Write_Into_DB" into the mongo db right now!
				collection.insert_one(data_To_Write_Into_DB)

	print ("------------ completed crawling data for " + str(hours_To_Move_On) + " hours.. Continuing to the next time frame now")

	# Shifts x with "hours_To_Move_On" hours into the future
	x = int(round(time.mktime((datetime.fromtimestamp(x) + timedelta(hours=hours_To_Move_On)).timetuple())))

	# Shifts y with "hours_To_Move_On" hours into the future
	y = int(round(time.mktime((datetime.fromtimestamp(y) + timedelta(hours=hours_To_Move_On)).timetuple())))


	# Whenever the destination time (y) to be crawled is newer than the defined ending time:      set y to the end_Value
	if y > end_Value:
		y = end_Value

	# Whenever the starting time (x) to be crawled is newer than the defined ending time   :      end this method here
	elif x > end_Value:
		return

	# Continue crawling
	else:
		crawl_Whole_Reddit_For_Comments()

# This method checks whether a collection already exists in the database or not and updates it if necessary
def check_If_Coll_In_DB_Already_Exists_Up2Date(submission):
	# Had to use "self" here to circumvent the "may not be static" warning

	# This is a tolerance factor because Reddit screws the "ups" - value. The "num_comments" - value remains consistent
	# tolerance_Factor = 25

	# Converts the unix utc_time into a date format and converts it to string afterwards
	temp_Submission_Creation_Year = str(datetime.fromtimestamp(submission.created_utc))
	temp_Submission_Creation_Year = temp_Submission_Creation_Year[:4]

	# This method says to look into the appropriate database, depending on the year the thread was created
	mongo_DB_Reddit = mongo_DB_Client_Instance["iAMA_Reddit_Comments_" + temp_Submission_Creation_Year]

	# Get all collections within that database
	mongo_DB_Collection = mongo_DB_Reddit.collection_names()

	# If it already exists, check whether it is up to date or not!
	if (str(submission.id)) in mongo_DB_Collection:

		# There is no proper checking method available to check whether all comments are up to date or not
		# We have to do this sideways by iterating over all threads and whenever a change in the amount of comments
		# is recognized the comments-collection for that thread gets dropped and has to be recrawled.

		return True

	# Whenever the collection does not yet exist
	else:
		return False

# Execute the method to crawl all data
crawl_Whole_Reddit_For_Comments()