import praw, time
from datetime import datetime, timedelta

reddit_Instance                     =               praw.Reddit(user_agent = "University_Regensburg_iAMA_Crawler_0.001")                # main reddit functionality

#   Tutorials used within this class:
#   1. (06.02.2016 @ 15:23) - http://www.esqsoft.com/javascript_examples/date-to-epoch.htm
#   2. (06.02.2016 @ 15:48) - https://www.reddit.com/r/redditdev/comments/2zdyy2/praw_continue_getting_posts_after_given_post_id/
#   3. (06.02.2016 @ 16:20) - https://www.linuxquestions.org/questions/programming-9/python-datetime-to-epoch-4175520007/
#   4. (06.02.2016 @ 16:30) - https://stackoverflow.com/questions/11743019/convert-python-datetime-to-epoch-with-strftime



x = 1243469026 # Starting time of the first iAMA post of Reddit [ 2009-05-28 02:03:46 ]

# <editor-fold desc="Description of y inside here">
# 1. At first 8 hours are added to the epoch format of x
#   1.1. At this step epoch gets converted to String
# 2. String gets converted back to epoch time
#   2.1. Due to conversion the time is in float format [1201907536.0]
# 3. Converts float to int while rounding it
#   3.1. Rounding does not the numbers in front of the comma [1201907536]
# </editor-fold>
y = int(round(time.mktime((datetime.fromtimestamp(x) + timedelta(hours=8)).timetuple())))


def crawlwholedb():
	global x, y

	# added_8_Hours_To_X = datetime.fromtimestamp(x) + timedelta(hours=8)     # Adds 4 hours to epoch time and converts it to string (2008-02-01 20:12:16)
	# y = time.mktime(added_8_Hours_To_X.timetuple())                                     # Converts the string back to epoch time

	posts = reddit_Instance.search('timestamp:' + str(x) + '..' + str(y), subreddit='iAMA', sort="new", limit=100, syntax="cloudsearch")
	for submission in posts:
		print (submission.id, submission.created_utc, datetime.fromtimestamp(submission.created_utc))
	print ("------------ completed crawling data for 8 hours.. Continuing to the next 8 hours now")

	x = int(round(time.mktime((datetime.fromtimestamp(x) + timedelta(hours=8)).timetuple())))         # Shifts x with 8 hours into the future
	y = int(round(time.mktime((datetime.fromtimestamp(y) + timedelta(hours=8)).timetuple())))         # Shifts y with 8 hours into the future



	# if x oder y größer als jetzt, dann break / setze y auf jetzt

	# X nochmal neu setzen, denn Y zieht oben automatisch nach

	# Whenever the time to be crawled is newer than the current time
	if x > int(time.time()):
		return
	# Continue crawling
	else:
		crawlwholedb() # with locally defined x it won't work i think



crawlwholedb()


