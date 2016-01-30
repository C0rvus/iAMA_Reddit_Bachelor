# TODO: Implement posting answer mechanism by using the following tutorial: https://github.com/shantnu/RedditBot (in Part 2)
# TODO: Get comments to work (py using that tutorial [comments are stored as tree] https://praw.readthedocs.org/en/stable/pages/comment_parsing.html
# TODO: Parse all that stuff into the mongoDB with an appropriate logic to reduce redundancy
# TODO: Rework data to make it all int, bool and string
# TODO: Spezifischen Thread parsen und dort auf MoreComment-Object checken (das dort erstmal modulweise testen!)

# https://www.reddit.com/r/IAmA/comments/42zc3w/i_am_grammy_awardnominated_composer_producer/comments.json
# ^^ Retrieves all Raw comments in the correct hierarchy
import praw


# Tutorials used:
#   1. (28.01.2015 @ 12:28) - http://pythonforengineers.com/build-a-reddit-bot-part-1/

user_agent = "University_Regensburg_iAMA_Crawler_0.001"

r = praw.Reddit(user_agent = user_agent)

subreddit = r.get_subreddit("iAma")

# Iterate every thread here
# for submission in subreddit.get_hot(limit = 4):

# com

## Testing with the Grammy Thread, because it contains lots of comments
for submission in subreddit.get_hot(limit = 4):
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



	print ("Author: ",  submission.author)                          # <<<<<<- (string)  the authors name
	print ("Title: ",   submission.title)                           # <<<<<<- (string)  the title of the thread
	# print ("comments: ", submission.comments)                     # <<<<<<- (list)    the comments, which need to be iterated seperately
	print ("num_comments: ", submission.num_comments)               # <<<<<<- (int)     the amount of comments done to this thread ..... newer goes down, because deleted posts will be kept
	print ("downs: ", submission.downs)                             # <<<<<<- (int)     the amount of downvotes to this thread
	print ("id: ", submission.id)                                   # <<<<<<- (string)  the unique id of that thread.. extremly necessary for writing into the database
	print ("url: ", submission.url)                                 # <<<<<<- (string)  the url to the thread
	print ("score: ", submission.score)                             # <<<<<<- (int)     the score (can be the same like upvotes / downvotes)
	print ("ups: ", submission.ups)                                 # <<<<<<- (int)     the amount of upvotes
	print ("------------------\n")                                  # <<<<<<-           just a simple line break
	# print ("Text: ", type(submission.selftext))                           # <<<<<<- (string)  the starting post


	# expands all (!!!) comments.. takes about 5 minutes for 4 threads
	submission.replace_more_comments(limit=None, threshold=0)
	all_comments = submission.comments




	# Iterates every top comment
	for idx, val in enumerate(submission.comments):
		print (idx, val.id)
		print (idx, val.name)
		print (idx, val.parent_id)

		print ("AUSGABE TYPE")
		print (idx, type(val))

		print (idx, val.author)             # Funzt ned, wenn man auf ein "More Comments" object stoesst !!!
		print (idx, val.downs)
		print (idx, val.score)
		print (idx, val.created_utc)
		print (idx, val.body)                               # <<<<<<- (string)  the full comment post
		# print (idx, val.json_dict)
		# print (idx, dir(val))


		#print (val.replies) #<<< contains subobjects, which needs to be parsed additionally
		print ("------------------\n")





