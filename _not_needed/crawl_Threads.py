# TODO: Get comments to work (py using that tutorial [comments are stored as tree] https://praw.readthedocs.org/en/stable/pages/comment_parsing.html

#   Tutorials used within this class:
#   1. (28.01.2016 @ 12:28) - http://pythonforengineers.com/build-a-reddit-bot-part-1/
#   2. (31.01.2016 @ 12:02) - https://www.reddit.com/r/redditdev/comments/2e2q2l/praw_downvote_count_always_zero/

# necessary for sorting dictionaries
import collections
from datetime import datetime
class crawl_Threads:
	def __init__(self):
		print ("...Initializing iAMA-Thread-Crawler...")

	# Crawls thread data, checks whether it has already been crawled / it is up to date and acts appropriately
	def main_Method(self, mongo_DB_Client_Instance, reddit_Instance, reddit_Metric_Of_Crawling):

		# Removes the 'not static' warning
		self.is_Not_Used()

		for submission in reddit_Metric_Of_Crawling:    # Iterates of every thread found in "reddit_Metric_Of_Crwaling"

			# Whenever the thread is already stored in mongoDB and up2date      (True)
			if self.check_If_Coll_In_DB_Already_Exists_Up2Date(mongo_DB_Client_Instance, submission):
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

	# Checks whether a thread already exists within the database
	def check_If_Coll_In_DB_Already_Exists_Up2Date(self, mongo_DB_Client_Instance, submission):
		# Had to use "self" here to circumvent the "may not be static" warning
		self

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
			if ( cursor[0].get("author") != str(submission.author) )\
					or ( cursor[0].get("num_Comments") != str(submission.num_comments) )\
					or ( cursor[0].get("selftext") != str(submission.selftext) )\
					or ( cursor[0].get("title") != str(submission.title) )\
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

	# Necessary to remove static warning in __init__ method
	def is_Not_Used(self):                                                  # Necessary to remove 'not static' warning
		pass