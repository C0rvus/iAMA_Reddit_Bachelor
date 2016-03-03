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
x                           =       1262300400                                                                  # Starting time of the first iAMA post of Reddit 	[ 2010-01-01 00:00:00 ]
end_Value			        =       1293836400		                                                            # Ending time where crawling should be stopped		[ 2011-01-01 00:00:00 ]

# <editor-fold desc="Description of y inside here">
# 1. At first 8 hours are added to the epoch format of x
#   1.1. At this step epoch gets converted to String
# 2. String gets converted back to epoch time
#   2.1. Due to conversion the time is in float format [1201907536.0]
# 3. Converts float to int while rounding it
#   3.1. Rounding does not the numbers in front of the comma [1201907536]
# </editor-fold>
y                   = int(round(time.mktime((datetime.fromtimestamp(x) + timedelta(hours=hours_To_Move_On)).timetuple())))

# This method crawls the data base for the year 2010
def crawl_Whole_Reddit_For_Threads():
	global x, y

	# Below is the crawl command to search within a dedicated time span from x to y. Time is used in epoch format
	posts = reddit_Instance.search('timestamp:' + str(x) + '..' + str(y), subreddit='iAMA', sort="new", limit=900, syntax="cloudsearch")
	for submission in posts:

		# Whenver the collection already exists in the database             (True)
		if check_If_Coll_In_DB_Already_Exists_Up2Date(submission):
			print ("++ Thread " + str(submission.id) + " already exists in mongoDB and is up2date")

		# Whenever the thread does not exist within the mongoDB (anymore)   (False)
		else:
			print ("    -- Thread " + str(submission.id) + " will be created now")

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

	print ("------------ completed crawling data for " + str(hours_To_Move_On) + " hours.. Continuing to the next time frame...")

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
		crawl_Whole_Reddit_For_Threads()

# This method checks whether a collection already exists in the database or not and updates it if necessary
def check_If_Coll_In_DB_Already_Exists_Up2Date(submission):

	# This is a tolerance factor because Reddit screws the "ups" - value. The "num_comments" - value remains consistent
	tolerance_Factor = 25

	# Converts the unix utc_time into a date format and converts it to string afterwards
	temp_Submission_Creation_Year = str(datetime.fromtimestamp(submission.created_utc))
	temp_Submission_Creation_Year = temp_Submission_Creation_Year[:4]

	# This method says to look into the appropriate database, depending on the year the thread was created
	mongo_DB_Reddit = mongo_DB_Client_Instance["iAMA_Reddit_Threads_" + temp_Submission_Creation_Year]

	# Get all collections within that database
	mongo_DB_Collection = mongo_DB_Reddit.collection_names()

	# If it already exists, check whether it is up to date or not!
	if (str(submission.id)) in mongo_DB_Collection:

		# Select the appropriate collection within the database
		collection = mongo_DB_Reddit[str(submission.id)]
		# And store the selection in a cursor
		cursor = collection.find()

		# Because the amount of comments crawled (comments db) will always differ (due to api restrictions) from the num_comments value
		# we check here wether the num_comments value has changed.. Whenever that is true the comments collection in the comments database gets dropped
		# and has to be crawled anew by using the appropriate diff-crawler script
		if cursor[0].get("num_Comments") != str(submission.num_comments) :

			# Creates a new connect to the mongoDB
			comments_Mongo_DB_Client_Instance = MongoClient('localhost', 27017)

			# References to the appropriate year
			comments_Mongo_DB_Reddit = comments_Mongo_DB_Client_Instance["iAMA_Reddit_Comments_" + temp_Submission_Creation_Year]

			# Tells mongoDB to drop that collection within the comments DB
			comments_Mongo_DB_Reddit.drop_collection(str(submission.id))
			print ("--- Comments for " + str(submission.id) + " have changed and therefore that collection has been dropped from comments DB")

		# Check various details to validate wether there is a need to recreate that collection or not
		if ( cursor[0].get("author") != str(submission.author) ) \
				or ( cursor[0].get("num_Comments") != str(submission.num_comments) ) \
				or ( cursor[0].get("selftext") != str(submission.selftext) ) \
				or ( cursor[0].get("title") != str(submission.title) ) \
				or ( cursor[0].get("ups") + tolerance_Factor < int(submission.ups)) \
				or ( cursor[0].get("ups") - tolerance_Factor > int(submission.ups)) \
				:
			# Delete that collection so that it gets recreated again
			mongo_DB_Reddit.drop_collection(str(submission.id))

			print ("--- Thread " + str(submission.id) + " was not up2date and therefore has been dropped")

			# Because the information in the database were old we dropped it and therefore we return False
			return False

		# Whenever the collection already exists and it is already up to date
		else :
			return True

	# Whenever the collection does not yet exist
	else:
		return False

# Execute the method to crawl all data
crawl_Whole_Reddit_For_Threads()