import praw
from datetime import datetime



reddit_Instance                     =               praw.Reddit(user_agent = "University_Regensburg_iAMA_Crawler_0.001")                # main reddit functionality
reddit_Chosen_Subreddit             =               reddit_Instance.get_subreddit("iAma")                                               # the subreddit, which is to be crawled
reddit_Amount_Of_Threads_To_Crawl   =               2                                                                                 # the amount of threads during crawling
# reddit_Metric_Of_Crawling           =               reddit_Chosen_Subreddit.get_hot(limit = reddit_Amount_Of_Threads_To_Crawl)          # the used metric of crawling.. See foled comment for options

submission_Thread = reddit_Instance.get_submission(submission_id='42zc3w')

print (dir(submission_Thread))

print (submission_Thread.created_utc)

# Source: https://www.reddit.com/r/botwatch/comments/21ui81/praw_help_finding_age_of_a_reddit_acccount/
temp_time = str(datetime.fromtimestamp(submission_Thread.created_utc))
print (datetime.fromtimestamp(submission_Thread.created_utc))

print (temp_time[:4])


#for submission in submission_Thread(0, 3):

	#print(dir(submission))

	#print (submission.selftext_html)

	#print (submission.comments)
	#for idx, val in enumerate(submission.comments):
#		print (idx, val.created_utc)
		#print (idx, val.body)
		#print ("------------------\n")


