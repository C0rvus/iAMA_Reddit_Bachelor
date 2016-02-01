import praw




reddit_Instance                     =               praw.Reddit(user_agent = "University_Regensburg_iAMA_Crawler_0.001")                # main reddit functionality
user = reddit_Instance.get_redditor('C0rvuss')

reddit_Chosen_Subreddit             =               reddit_Instance.get_subreddit("iAma")                                               # the subreddit, which is to be crawled
reddit_Amount_Of_Threads_To_Crawl   =               2                                                                                 # the amount of threads during crawling
# reddit_Metric_Of_Crawling           =               reddit_Chosen_Subreddit.get_hot(limit = reddit_Amount_Of_Threads_To_Crawl)          # the used metric of crawling.. See foled comment for options

# submission_Thread = reddit_Instance.get_submission(submission_id='42zc3w')


# Source: https://www.reddit.com/r/redditdev/comments/3lo4gn/praw_and_timestamp_searches/
posts = reddit_Instance.search('',subreddit='iAMA',sort='new',limit=None,syntax='cloudsearch',params={'timestamp':'1420027200..1420070400'})

print (posts)