import praw
from pymongo import MongoClient                         # necessary to interact with MongoDB
import json
import collections                                      # necessary for sorting dictionaries


# TODO: This method is necessary whenever a thread gets parsed for the very first time!

client = MongoClient('localhost', 27017)
db = client['iAMA_Reddit']
collection = db['42zc3w_comments']



user_agent = "University_Regensburg_iAMA_Crawler_0.001"

r = praw.Reddit(user_agent = user_agent, cache_timeout=0)

## Testing with the Grammy Thread, because it contains lots of comments
## Link: https://www.reddit.com/r/IAmA/comments/42zc3w/i_am_grammy_awardnominated_composer_producer/?limit=500
## https://www.reddit.com/r/IAmA/comments/42zc3w/i_am_grammy_awardnominated_composer_producer/comments.json

submission = r.get_submission(submission_id='42zc3w')

# Expands all comments here -> extreme time consuming (but afterwards there are no MoreComment - Errors)


submission.replace_more_comments(limit=None, threshold=0)
flat_comments = praw.helpers.flatten_tree(submission.comments)

# all_comments = submission.comments

for idx, val in enumerate(flat_comments):
	returned_JSON_Data = []    # Creates an list with fixed length

	# noinspection PyTypeChecker
	returned_JSON_Data = dict({
		'author' : str(val.author),
		'body' : str(val.body),
		'created_utc' : int(val.created_utc),
	    'name' : str(val.name),
	    'parent_id': str(val.parent_id),
	    'score' : int(val.score)
	})

	returned_JSON_Data = collections.OrderedDict(sorted(returned_JSON_Data.items()))              # Sorts that dictionary alphabetically ordered

	collection.insert_one(returned_JSON_Data)             # write it now