import praw
import pprint
from pymongo import MongoClient                         # necessary to interact with MongoDB

# Sources: http://alan-wright.com/programming/tutorial/python/2014/03/09/praw-tutorial/
# https://m.reddit.com/r/RequestABot/comments/42lmgv/need_a_bot_that_can_pull_all_users_and_account/
# https://github.com/alanwright/RedditBots/blob/master/scripts/UserGoneWild.py

client = MongoClient('localhost', 27017)

reddit_Instance = praw.Reddit(user_agent="University_Regensburg_iAMA_Crawler_0.001")
# user_name = "_Daimon_"


user_name = "TonyYounMD"
# amount_of_comments_total = 0

# TODO: 1. Sortieren der time stamp arrays
# TODO: 2. Berechnen der Diffs zwischen den time stamps
# TODO: 3. Den Wert korrekt in eine CSV reinschreiben (siehe bisherige Scripte)
# TODO: 4. Korrekt kommentieren und Datei sauber anpassen
# TODO: 5. Dieses Script analog den anderen Crawlern aufbauen und in der Readme.MD hinterlegen
# TODO: 6. Diese Sachen alle auswerten

# (y) Amount comments except iAMA
# (y) Amount comments in iAMA only
# (y) Amount threads created in submission except iAMA
# (y) Amount threads created within iAMA
# (y) Date of Birth (Account)
# (y) Amount of Karma per Thread created
# (y) Amount of Kerma per Comment
# Time date of thread creation ----> Kann man Aktivität herauslesen (wie "aktiv" ist ein Redditor)
# ^^ Zahl aller Zeitstempel der Threads speichern und dann die Diffs dazwischen berechnen
# ^^ Zahl aller Zeitstempel der Kommentare speichern und dann die Diffs dazwischen berechnen


reddit_Thread_Host = reddit_Instance.get_redditor(user_name)

# Amount of comments the redditor every made in total
amount_of_comments_except_iama = 0
amount_of_comments_iama = 0

# Amount of threads the host created
amount_creation_iama_threads = 0
amount_creation_other_threads = 0

# The birthdate of the account in utc epoch time format
author_birtday = reddit_Thread_Host.refresh().created_utc

# Amount of comment karma
author_comment_karma_amount = reddit_Thread_Host.refresh().comment_karma

# Amount of link / thread karma
author_link_karma_amount = reddit_Thread_Host.refresh().link_karma

# Timestamps of every single link / thread created by the author
timestamps_threads = []

# Timestamps of every single comment created by the author
timestamps_comments = []

# Contains all submissions of the thread creator
submitted = reddit_Thread_Host.get_submitted(limit=None)

# Contains all comments of the thread creator
comments = reddit_Thread_Host.get_comments(limit=None)

# <editor-fold desc="Retrieves all comments per author">
for comment in comments:

    # Checks for submission of that comment (i.e. plasticsurgerybeauty)
    name_of_subreddit_the_host_commented_to = comment.subreddit.display_name.lower()

    comment_creation_date = comment.created_utc

    timestamps_comments.append(comment_creation_date)

    # Whenever the author contributed an comment to iama
    if name_of_subreddit_the_host_commented_to == "iama":

        amount_of_comments_iama += 1

    # Whenever he did not
    else:
        amount_of_comments_except_iama += 1

print("Anzahl Kommentare innerhalb von iAMA: " + str(amount_of_comments_iama))
print("Anzahl Kommentare ausserhalb von iAMA: " + str(amount_of_comments_except_iama))

# </editor-fold>

# <editor-fold desc="Retrieves all threads created per author">
for link in submitted:

    subreddit = link.subreddit.display_name.lower()
    link_creation_date = link.created_utc

    timestamps_threads.append(link_creation_date)

    if subreddit == "iama":
        amount_creation_iama_threads += 1
    else:
        amount_creation_other_threads += 1

print("Anzahl erstellter Threads in iAMA: " + str(amount_creation_iama_threads))
print("Anzahl erstellter Threads nicht in iAMA: " + str(amount_creation_other_threads))
# </editor-fold>

print(timestamps_threads)
print(timestamps_comments)
