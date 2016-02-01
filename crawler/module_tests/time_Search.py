import praw
reddit_Instance                     =               praw.Reddit(user_agent = "University_Regensburg_iAMA_Crawler_0.001")                # main reddit functionality



# correct utc converter: http://www.esqsoft.com/javascript_examples/date-to-epoch.htm
# https://www.reddit.com/r/redditdev/comments/2zdyy2/praw_continue_getting_posts_after_given_post_id/   <<<<<<<<<<<<<<<<< LOOK AT IT FOR SHIFTING WINDOW !!!! und das dann in ner Loop machen !!!
posts = reddit_Instance.search('timestamp:1295029800..1295116200', \
                      subreddit='iAMA', \
                      sort="new", \
                      limit=100, \
                      syntax="cloudsearch")

for submission in posts:
	print (submission.id)