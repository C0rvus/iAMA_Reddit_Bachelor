import praw

user_agent = "University_Regensburg_iAMA_Crawler_0.001"

r = praw.Reddit(user_agent = user_agent)

## Testing with the Grammy Thread, because it contains lots of comments
## Link: https://www.reddit.com/r/IAmA/comments/42zc3w/i_am_grammy_awardnominated_composer_producer/?limit=500
submission = r.get_submission(submission_id='42zc3w')

# Expands all comments here -> extreme time consuming (but afterwards there are no MoreComment - Errors)
submission.replace_more_comments(limit=None, threshold=0)
all_comments = submission.comments


# Iterates every top comment
for idx, val in enumerate(all_comments):
	print (idx, val.id)
	print (idx, val.name)
	print (idx, val.parent_id)                          # <<<<<<- necessary for hierarchy creation

	print (idx, val.body)                               # <<<<<<- (string)  the full comment post


	print ("AUSGABE TYPE")
	print (idx, type(val))

	if type(val) == praw.objects.MoreComments:
		print ("ICH BIN EIN MORECOMMENTS")
		# Expand MoireComments Object here



	print (idx, val.author)             # Funzt ned, wenn man auf ein "More Comments" object stoesst !!!
	print (idx, val.downs)
	print (idx, val.score)
	print (idx, val.created_utc)


	print ("AUSGABE TYPE replies")
	print (idx, type(val.replies))          #<<< gibt eine List zurueck
	print (val.replies)                     #<<< contains subobjects, which needs to be parsed additionally
	print ("------------------\n")

