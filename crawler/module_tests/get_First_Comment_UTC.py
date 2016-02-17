import praw
# from datetime import datetime
import sys



reddit_Instance                     =               praw.Reddit(user_agent = "University_Regensburg_iAMA_Crawler_0.001")                # main reddit functionality
reddit_Chosen_Subreddit             =               reddit_Instance.get_subreddit("iAma")                                               # the subreddit, which is to be crawled
reddit_Amount_Of_Threads_To_Crawl   =               2                                                                                 # the amount of threads during crawling
# reddit_Metric_Of_Crawling           =               reddit_Chosen_Subreddit.get_hot(limit = reddit_Amount_Of_Threads_To_Crawl)          # the used metric of crawling.. See foled comment for options

# submission = reddit_Instance.get_submission(submission_id='vg1og')
# submission.replace_more_comments(limit=None, threshold=0)


# submission = reddit_Instance.get_submission(submission_id='vg1og')

comment = reddit_Instance.get_submission('http://www.reddit.com/r/redditdev/comments/10msc8/')

print (comment)









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