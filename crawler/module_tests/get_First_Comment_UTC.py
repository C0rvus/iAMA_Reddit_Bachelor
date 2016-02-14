import praw
from datetime import datetime
import sys



reddit_Instance                     =               praw.Reddit(user_agent = "University_Regensburg_iAMA_Crawler_0.001")                # main reddit functionality
reddit_Chosen_Subreddit             =               reddit_Instance.get_subreddit("iAma")                                               # the subreddit, which is to be crawled
reddit_Amount_Of_Threads_To_Crawl   =               2                                                                                 # the amount of threads during crawling
# reddit_Metric_Of_Crawling           =               reddit_Chosen_Subreddit.get_hot(limit = reddit_Amount_Of_Threads_To_Crawl)          # the used metric of crawling.. See foled comment for options

submission = reddit_Instance.get_submission(submission_id='vg1og')
submission.replace_more_comments(limit=None, threshold=0)


def get_comments_depth_n(comments, n, depth=0):
    # First check the end condition: reaching the desired depth
    # Return the comments list, which will be merged with other comment lists
    if depth == n:
        return comments

    # Otherwise continue to recur through the comment tree
    n_comments = list()         # List to store result comments
    for comment in comments:
        # Recur the method and get the result: a list of comments at the desired depth
        result = get_comments_depth_n(comment.replies, n, depth+1)
        # Store these comments with the rest of 'em
        n_comments.extend(result)

    return n_comments




print (get_comments_depth_n(submission.comments, 10))










# print (dir(submission))
# print ("Ausgabe clicked: " + str(submission.clicked))
# print ("Ausgabe distinguish: " + str(submission.distinguish))
# print ("Ausgabe distinguished: " + str(submission.distinguished))
# print ("Ausgabe domain: " + str(submission.domain))
# print ("Ausgabe from_id: " + str(submission.from_id))
# print ("Ausgabe from_api_response: " + str(submission.from_api_response))
# print ("Ausgabe gild: " + str(submission.gild))
# print ("Ausgabe gilded: " + str(submission.gilded))
# print ("Ausgabe id: " + str(submission.id))
# print ("Ausgabe link_flair_text: " + str(submission.link_flair_text))
# print ("Ausgabe media: " + str(submission.media))
# print ("Ausgabe reddit_session: " + str(submission.reddit_session))
# print ("Ausgabe set_flair: " + str(submission.set_flair))
# print ("Ausgabe short_link: " + str(submission.short_link))
# print ("Ausgabe subreddit: " + str(submission.subreddit))
# print ("Ausgabe subreddit_id: " + str(submission.subreddit_id))






sys.exit()


# Source: https://www.reddit.com/r/botwatch/comments/21ui81/praw_help_finding_age_of_a_reddit_acccount/
# temp_time = str(datetime.fromtimestamp(submission.created_utc))
# print (datetime.fromtimestamp(submission.created_utc))

# print (temp_time[:4])


#for submission in submission(0, 3):

	#print(dir(submission))

	#print (submission.selftext_html)

	#print (submission.comments)
	#for idx, val in enumerate(submission.comments):
#		print (idx, val.created_utc)
		#print (idx, val.body)
		#print ("------------------\n")


