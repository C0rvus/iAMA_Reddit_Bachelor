import praw, time, collections
from pymongo        import MongoClient                                                                                                  # necessary to interact with MongoDB

from datetime import datetime, timedelta

mongo_DB_Client_Instance            =               MongoClient('localhost', 27017)                                                     # the mongo client, necessary to connect to mongoDB
reddit_Instance                     =               praw.Reddit(user_agent = "University_Regensburg_iAMA_Crawler_0.001")                # main reddit functionality

# TODO: IM kleineren Intervall (12h) nochmal drüber gehen mit höherem limit


#   Tutorials used within this class:
#   1. (06.02.2016 @ 15:23) - http://www.esqsoft.com/javascript_examples/date-to-epoch.htm
#   2. (06.02.2016 @ 15:48) - https://www.reddit.com/r/redditdev/comments/2zdyy2/praw_continue_getting_posts_after_given_post_id/
#   3. (06.02.2016 @ 16:20) - https://www.linuxquestions.org/questions/programming-9/python-datetime-to-epoch-4175520007/
#   4. (06.02.2016 @ 16:30) - https://stackoverflow.com/questions/11743019/convert-python-datetime-to-epoch-with-strftime

hours_To_Move_On    = 96                    # Defines the crawling time frame in hours
# x                   = 1243469026            # Starting time of the first iAMA post of Reddit [ 2009-05-28 02:03:46 ]

x = 1291881086

# <editor-fold desc="Description of y inside here">
# 1. At first 8 hours are added to the epoch format of x
#   1.1. At this step epoch gets converted to String
# 2. String gets converted back to epoch time
#   2.1. Due to conversion the time is in float format [1201907536.0]
# 3. Converts float to int while rounding it
#   3.1. Rounding does not the numbers in front of the comma [1201907536]
# </editor-fold>
y                   = int(round(time.mktime((datetime.fromtimestamp(x) + timedelta(hours=hours_To_Move_On)).timetuple())))


def crawlwholedb():
	global x, y

	# added_8_Hours_To_X = datetime.fromtimestamp(x) + timedelta(hours=8)     # Adds 4 hours to epoch time and converts it to string (2008-02-01 20:12:16)
	# y = time.mktime(added_8_Hours_To_X.timetuple())                                     # Converts the string back to epoch time

	posts = reddit_Instance.search('timestamp:' + str(x) + '..' + str(y), subreddit='iAMA', sort="new", limit=900, syntax="cloudsearch")
	for submission in posts:
		# print (submission.id, submission.created_utc, datetime.fromtimestamp(submission.created_utc))

		if check_If_Coll_In_DB_Already_Exists_Up2Date(submission):
			print ("++ Thread " + str(submission.id) + " already exists in mongoDB and is up2date")

			# Whenever the thread does not exist within the mongoDB (anymore)   (False)
		else:
			print ("    -- Thread " + str(submission.id) + " will be created now")

			# Because down votes are no accessable via reddit API, we have calculated it by our own here
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
				#'total_Votes'   : int(total_Votes),    # not necessary to write it into the database, because we can add 'ups' and 'downs' ourselfes
				'ups'           : int(submission.ups)   #,
				#'url'           : str(submission.url)  # not necessary to crawl that url, because we can build it by using the id
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

			# Write it now !
			collection.insert_one(data_To_Write_Into_DB)

	print ("------------ completed crawling data for " + str(hours_To_Move_On) + " hours.. Continuing to the next time frame now")

	x = int(round(time.mktime((datetime.fromtimestamp(x) + timedelta(hours=hours_To_Move_On)).timetuple())))         # Shifts x with "hours_To_Move_On" hours into the future
	y = int(round(time.mktime((datetime.fromtimestamp(y) + timedelta(hours=hours_To_Move_On)).timetuple())))         # Shifts y with "hours_To_Move_On" hours into the future


	# Whenever the destination time (y) to be crawled is newer than the current time:   set y to the current time
	if y > int(time.time()):
		y = int(time.time())

	# Whenever the starting time (x) to be crawled is newer than the current time:      end this method here
	elif x > int(time.time()):
		return

	# Continue crawling
	else:
		crawlwholedb() # with locally defined x it won't work i think


def check_If_Coll_In_DB_Already_Exists_Up2Date(submission):
	# Had to use "self" here to circumvent the "may not be static" warning

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


crawlwholedb()



