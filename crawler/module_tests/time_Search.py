import praw
import time
from datetime import datetime, timedelta

reddit_Instance                     =               praw.Reddit(user_agent = "University_Regensburg_iAMA_Crawler_0.001")                # main reddit functionality



# correct utc converter: http://www.esqsoft.com/javascript_examples/date-to-epoch.htm
# https://www.reddit.com/r/redditdev/comments/2zdyy2/praw_continue_getting_posts_after_given_post_id/   <<<<<<<<<<<<<<<<< LOOK AT IT FOR SHIFTING WINDOW !!!! und das dann in ner Loop machen !!!
# https://www.linuxquestions.org/questions/programming-9/python-datetime-to-epoch-4175520007/
# https://stackoverflow.com/questions/11743019/convert-python-datetime-to-epoch-with-strftime


# globales x definieren und dann der Funktion übergreifen
# das gleiche aucvh fuer y machen

#x = 1201878736 # starting time (2008)
# y = 0 # time delta

# print (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1201878736)))
# print (datetime.fromtimestamp(1201878736).strftime('%c'))

#added_Time = datetime.fromtimestamp(1201878736) + timedelta(hours=4)

#print (datetime.fromtimestamp(1201878736) + timedelta(hours=4))

#print (time.mktime(added_Time.timetuple()))


# x = 1201878736 # starting time plus new time ... (2008-02-01 16:12:16)
# y = int(round(time.mktime((datetime.fromtimestamp(x) + timedelta(hours=8)).timetuple())))       # Adds 8 Hours to epoch time -> String.. Converts it back to epoch time (float) 1201907536.0 and rounds it to int (1201907536)


# print (str(x), str(y))

x = 1243469026 # starting time plus new time ... (2008-02-01 16:12:16)
y = int(round(time.mktime((datetime.fromtimestamp(x) + timedelta(hours=8)).timetuple())))       # Adds 8 Hours to epoch time -> String.. Converts it back to epoch time (float) 1201907536.0 and rounds it to int (1201907536)





# 8nron 1243469026.0 2009-05-28 02:03:46 [first iAMA post ever !!]
# first end : 1243469026
def crawlwholedb():
	global x, y



	# added_8_Hours_To_X = datetime.fromtimestamp(x) + timedelta(hours=8)     # Adds 4 hours to epoch time and converts it to string (2008-02-01 20:12:16)
	# y = time.mktime(added_8_Hours_To_X.timetuple())                                     # Converts the string back to epoch time

	posts = reddit_Instance.search('timestamp:' + str(x) + '..' + str(y), subreddit='iAMA', sort="new", limit=100, syntax="cloudsearch")
	for submission in posts:
		print (submission.id, submission.created_utc, datetime.fromtimestamp(submission.created_utc))
	print ("------------ Bin mit allen durch, gehe nun 8 Stunden voran")

	x = int(round(time.mktime((datetime.fromtimestamp(x) + timedelta(hours=8)).timetuple())))         # X adds 8 hours to itself in epochtime
	y = int(round(time.mktime((datetime.fromtimestamp(y) + timedelta(hours=8)).timetuple())))

	# X nochmal neu setzen, denn Y zieht oben automatisch nach
	crawlwholedb() # with locally defined x it won't work i think


# damit es ueberhaupt susgerfuerhr wird...
crawlwholedb()


