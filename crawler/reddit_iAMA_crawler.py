import praw


# Tutorials used:
#   1. (28.01.2015 @ 12:28) - http://pythonforengineers.com/build-a-reddit-bot-part-1/

user_agent = "University_Regensburg_iAMA_Crawler_0.001"

r = praw.Reddit(user_agent = user_agent)

subreddit = r.get_subreddit("iAma")

for submission in subreddit.get_hot(limit = 2):
	print (dir(submission))

	# print ("Approved_by: ", submission.approved_by)               # <<<<<<- (object)  not necessary to be known by us.
	# print ("Author_flair_text: ", submission.author_flair_text)   # <<<<<<- (object)  not necessary to be known by us.
	# print ("Clicked: ", submission.clicked)                       # <<<<<<- (bool)    not necessary because this will be handled via javascript later on
	# print ("domain: ", submission.domain)                         # <<<<<<- (string)  not necessary because domain is always iAMA
	# print ("from_api_response: ", submission.from_api_response)   # <<<<<<- (?)       not necessary because of error message
	# print ("saved: ", submission.saved)                           # <<<<<<- (bool)    retrieves boolean whether it is saved under the used user_agent
	# print ("upvote: ", submission.upvote)                         # <<<<<<- (?)       not necessary because of error message
	# print ("permalink: ", submission.permalink)                   # <<<<<<- (string)  not necessary because it's the same as url
	# print ("user_reports: ", submission.user_reports)             # <<<<<<- (array)   not necessary because it returns an empty array
	# print ("sticky: ", submission.sticky)                         # <<<<<<- (?)       not necessary because of error message
	# print ("thumbnail: ", submission.thumbnail)                   # <<<<<<- (object)  not necessary because it returns 'self'
	# print ("visited: ", submission.visited)                       # <<<<<<- (bool)    not necessary because this will be handled via javascript later on
	# print ("vote: ", submission.vote)                             # <<<<<<- (?)       not necessary because of error message



	print ("Author: ",  submission.author)                          # <<<<<<- (string)  the authors name
	print ("Title: ",   submission.title)                           # <<<<<<- (string)  the title of the thread
	print ("comments: ", submission.comments)                       # <<<<<<- (array)   with no content in it ?!
	print ("num_comments: ", submission.num_comments)               # <<<<<<- (int)     the amount of comments done to this thread
	print ("downs: ", submission.downs)                             # <<<<<<- (int)     the amount of downvotes to this thread
	print ("id: ", submission.id)                                   # <<<<<<- (string)  the unique id of that thread.. extremly necessary for writing into the database
	print ("url: ", submission.url)                                 # <<<<<<- (string)  the url to the thread
	print ("score: ", submission.score)                             # <<<<<<- (int)     the score (can be the same like upvotes / downvotes)
	print ("ups: ", submission.ups)                                 # <<<<<<- (int)     the amount of upvotes
	print ("------------------\n")                                  # <<<<<<-           just a simple line break
	print ("Text: ", submission.selftext)                           # <<<<<<- (string) the starting post

