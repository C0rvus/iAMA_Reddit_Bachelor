# TODO: Create HTTP-Server containing test site with refresh button to start PRAW-Gathering
# TODO: Create REST-Server with FLASK for that stuf


from pymongo        import MongoClient                                                                                                  # necessary to interact with MongoDB
from crawl_Threads  import crawl_Threads                                                                                                # necessary for crawling threads
import praw


client                              =               MongoClient('localhost', 27017)                                                     # the mongo client, necessary to connect to mongoDB
mongo_DB_Reddit                     =               client.iAMA_Reddit                                                                  # the collection (table), in which reddit information will be stored
mongo_DB_Test_Row                   =               {}                                                                                  # will be modified by generate_DataSet_To_Be_Written_To_DB()


reddit_Instance                     =               praw.Reddit(user_agent = "University_Regensburg_iAMA_Crawler_0.001")                # main reddit functionality
reddit_Chosen_Subreddit             =               reddit_Instance.get_subreddit("iAma")                                                        # the subreddit, which is to be crawled
reddit_Amount_Of_Threads_To_Crawl   =               8                                                                                   # the amount of threads during crawling
reddit_Metric_Of_Crawling           =               reddit_Chosen_Subreddit.get_hot(limit = reddit_Amount_Of_Threads_To_Crawl)          # the used metric of crawling.. See foled comment for options

# <editor-fold desc="Possible metric variants of reddit are defined inside here">
# get_controversial
# get_controversial_from_all
# get_controversial_from_day
# get_controversial_from_hour
# get_controversial_from_month
# get_controversial_from_week
# get_controversial_from_year
# get_hot
# get_random_submission
# get_rising
# get_new
# get_edited            ( << only works while logged in)
# get_spam              ( << only works while logged in)
# get_top
# get_top_from_all
# get_top_from_day
# get_top_from_hour
# get_top_from_month
# get_top_from_week
# get_top_from_year
# </editor-fold>

cr_T = crawl_Threads()                              # defines the method for creation of the extra table 'arrest'




# <editor-fold desc="Writes test data into the database iAMA_Reddit">
# Writes some data into the collection "example_Table"
# </editor-fold>
def test_Write_DB_Test_Data():
	global mongo_DB_Test_Row                       # references the global variable to make use of it locally
	global mongo_DB_Reddit                         # references the global variable to make use of it locally
	# noinspection PyTypeChecker

	mongo_DB_Test_Row = dict({
		"column_1" :   "Hans_1",
		"column_2" :   "Hans_2"
	})

	mongo_Collection_To_Be_Written_Into = mongo_DB_Reddit["example_Table"]
	mongo_Collection_To_Be_Written_Into.insert_one(mongo_DB_Test_Row)

	print('Test data has been successfully written into example_Table')

# <editor-fold desc="Tests, whether the reddit settings are still correct">
# Simply fetches a few threads from within the iAMA-Subreddit and iterates over them
# </editor-fold>
def test_Reddit_Settings():
	global reddit_Chosen_Subreddit                                              # references the global variable to make use of it locally
	global reddit_Metric_Of_Crawling                                           # references the global variable to make use of it locally

	for submission in reddit_Metric_Of_Crawling:

		print(submission.id, submission.url)                                                    # prints the id of the iterated thread

# <editor-fold desc="Crawls threads and stores them inside the mongoDB">
# Crawls a few threads and stores them inside the mongoDB "iAMA" called colelction
# </editor-fold>
def crawl_Threads():
	global mongo_DB_Reddit                                                      # references the global variable to make use of it locally
	global reddit_Chosen_Subreddit                                              # references the global variable to make use of it locally

	return cr_T.main_Method(mongo_DB_Reddit, reddit_Instance, reddit_Metric_Of_Crawling)






# test_Write_DB_Test_Data()                           # Writes test data into the database, to check whether the connection is working or not
# test_Reddit_Settings()                              # Tests some basic reddit settings

crawl_Threads()                                       # Crawls threads and writes them into the database


