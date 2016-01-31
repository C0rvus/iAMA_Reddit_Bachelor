# TODO: Implement posting answer mechanism by using the following tutorial: https://github.com/shantnu/RedditBot (in Part 2)
# TODO: Get comments to work (py using that tutorial [comments are stored as tree] https://praw.readthedocs.org/en/stable/pages/comment_parsing.html
# TODO: Parse all that stuff into the mongoDB with an appropriate logic to reduce redundancy
# TODO: Rework data to make it all int, bool and string
# TODO: Spezifischen Thread parsen und dort auf MoreComment-Object checken (das dort erstmal modulweise testen!)
# TODO: IF Exist crawled Thread in DB

import collections                                      # necessary for sorting dictionaries

class crawl_Threads:
	def __init__(self):
		print ("...Initializing iAMA-Thread-Crawler...")

	def main_Method(self, mongo_DB_Reddit, reddit_Instance, reddit_Metric_Of_Crawling):
		self.is_Not_Used()                              # Removes the 'not static' warning

		for submission in reddit_Metric_Of_Crawling:    # Iterates of every thread found in "reddit_Metric_Of_Crwaling"

			# Source        : https://www.reddit.com/r/redditdev/comments/2e2q2l/praw_downvote_count_always_zero/
			# Accessed on   : 31.01.2016 @ 12:02

			ratio = reddit_Instance.get_submission(submission.permalink).upvote_ratio
			total_Votes = int(round((ratio*submission.score)/(2*ratio - 1)) if ratio != 0.5 else round(submission.score/2))
			downs = total_Votes - submission.score

			# noinspection PyTypeChecker
			data_To_Write_Into_DB = dict({
				'author'        : str(submission.author),
				'downs'         : int(downs),
				'num_comments'  : str(submission.num_comments),
				'selftext'      : str(submission.selftext),
				'title'         : str(submission.title),
				'total_Votes'   : int(total_Votes),
				'ups'           : int(submission.ups),
				'url'           : str(submission.url)
			})

			data_To_Write_Into_DB = collections.OrderedDict(sorted(data_To_Write_Into_DB.items()))              # Sorts that dictionary alphabetically ordered

			collection = mongo_DB_Reddit[str(submission.id)]
			collection.insert_one(data_To_Write_Into_DB)             # write it now

		#Tutorials used:
	#   1. (28.01.2015 @ 12:28) - http://pythonforengineers.com/build-a-reddit-bot-part-1/







	# Iterate every thread here
	# for submission in subreddit.get_hot(limit = 4):

	# com

	## Testing with the Grammy Thread, because it contains lots of comments
	#
	# print (dir(submission))                                       # <<<<<<- (object)  not necessary any more.. showed the amount of possible anchorpoints for accessing data

	# print ("Approved_by: ", submission.approved_by)               # <<<<<<- (object)  not necessary to be known by us.
	# print ("Author_flair_text: ", submission.author_flair_text)   # <<<<<<- (object)  not necessary to be known by us.
	# print ("Clicked: ", submission.clicked)                       # <<<<<<- (bool)    not necessary because this will be handled via javascript later on
	# print ("domain: ", submission.domain)                         # <<<<<<- (string)  not necessary because domain is always iAMA
	# print ("from_api_response: ", submission.from_api_response)   # <<<<<<- (?)       not necessary because of error message
	# print ("saved: ", submission.saved)                           # <<<<<<- (bool)    retrieves boolean whether it is saved under the used user_agent
	# print ("upvote: ", submission.upvote)                         # <<<<<<- (?)       not necessary because of error message
	# print ("permalink: ", submission.permalink)                   # <<<<<<- (string)  not necessary because it's the same as url
	# print ("user_reports: ", submission.user_reports)             # <<<<<<- (array)   not necessary because it returns an empty list
	# print ("sticky: ", submission.sticky)                         # <<<<<<- (?)       not necessary because of error message
	# print ("thumbnail: ", submission.thumbnail)                   # <<<<<<- (object)  not necessary because it returns 'self'
	# print ("visited: ", submission.visited)                       # <<<<<<- (bool)    not necessary because this will be handled via javascript later on
	# print ("vote: ", submission.vote)                             # <<<<<<- (?)       not necessary because of error message






	# expands all (!!!) comments.. takes about 5 minutes for 4 threads
	#submission.replace_more_comments(limit=None, threshold=0)
	#all_comments = submission.comments




	# # Iterates every top comment
	# for idx, val in enumerate(submission.comments):
	# 	print (idx, val.id)
	# 	print (idx, val.name)
	# 	print (idx, val.parent_id)
	#
	# 	print ("AUSGABE TYPE")
	# 	print (idx, type(val))
	#
	# 	print (idx, val.author)             # Funzt ned, wenn man auf ein "More Comments" object stoesst !!!
	# 	print (idx, val.downs)
	# 	print (idx, val.score)
	# 	print (idx, val.created_utc)
	# 	print (idx, val.body)                               # <<<<<<- (string)  the full comment post
	# 	# print (idx, val.json_dict)
	# 	# print (idx, dir(val))
	#
	#
	# 	#print (val.replies) #<<< contains subobjects, which needs to be parsed additionally
	# 	print ("------------------\n")

	def is_Not_Used(self):                                                  # Necessary to remove 'not static' warning
		pass



