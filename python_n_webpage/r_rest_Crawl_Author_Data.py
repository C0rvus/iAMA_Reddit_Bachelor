# Sources used within this class:
# 1. (09.06.2016 @ 18:20) -
# http://alan-wright.com/programming/tutorial/python/2014/03/09/praw-tutorial/
# 2. (09.06.2016 @ 22:30) -
# https://m.reddit.com/r/RequestABot/comments/42lmgv/need_a_bot_that_can_pull_all_users_and_account/
# 3. (09.06.2016 @ 22:42) - https://github.com/alanwright/RedditBots/blob/master/scripts/UserGoneWild.py

import praw                                 # Necessary to access the reddit api
import collections                          # Necessary for dictionary sorting
from pymongo import MongoClient             # Necessary to interact with MongoDB

mongo_db_client_instance = MongoClient('localhost', 27017)

mongo_db_author_fake_iama_instance = mongo_db_client_instance['fake_iAMA_Reddit_Authors']
mongo_db_author_fake_iama_collection_names = mongo_db_author_fake_iama_instance.collection_names()

mongo_db_author_comments_instance = mongo_db_client_instance['fake_iAMA_Reddit_Comments']
mongo_db_author_comments_collection = mongo_db_author_comments_instance.collection_names()

# Instanciates the reddit instace for crawling behaviour
reddit_instance = praw.Reddit(user_agent="University_Regensburg_iAMA_Crawler_0.001")


# noinspection PyPep8Naming
class r_rest_Crawl_Author_Data:
    def start_crawling(self, author_name):

        # Crawl and write that author information (threads + comments from it) into the various databases
        self.get_n_write_author_information(author_name)

    @staticmethod
    def get_n_write_author_information(name_of_author):

        # Anonymous inner method to write comments into the database
        def write_comments_into_db(id_of_thread):

            # Drop comments collections here, before they will be recrawled
            mongo_db_author_comments_instance.drop_collection(id_of_thread)

            # Retrieves the submission object from reddit
            submission = reddit_instance.get_submission(submission_id=id_of_thread)

            # Breaks up comments hierarchy
            submission.replace_more_comments(limit=None, threshold=0)
            flat_comments = praw.helpers.flatten_tree(submission.comments)

            # Iterates over the loosened comments hierarchy
            for idx, val in enumerate(flat_comments):

                # noinspection PyTypeChecker
                returned_json_data = dict({
                    'author': str(val.author),
                    'body': str(val.body),
                    'created_utc': str(val.created_utc),
                    'name': str(val.name),
                    'parent_id': str(val.parent_id),
                    'ups': int(val.score)
                })

                # Sorts the dictionary alphabetically correct
                returned_json_data = collections.OrderedDict(sorted(returned_json_data.items()))

                # Defines the position where the calculated information should be written into
                collection = mongo_db_author_comments_instance[str(id_of_thread)]

                # Writes that information into the database
                collection.insert_one(returned_json_data)

        # Amount of threads created by the author is defined here
        amount_of_threads = []

        # Drop that author collection (recrawl that information anew)
        mongo_db_author_fake_iama_instance.drop_collection(str(name_of_author))

        # The instance of the thread iama host
        reddit_thread_host = reddit_instance.get_redditor(name_of_author)

        # Contains all submissions of the thread creator
        submitted = reddit_thread_host.get_submitted(limit=None)

        # Iterates over every submission the author made
        for link in submitted:

            # Truncate the thread id (removes 't3_' on top of the thread)
            thread_id = str(link.name)[3:]
            amount_of_threads.append(thread_id)

            # Write comments into the database
            write_comments_into_db(thread_id)

        # The dict to be returned
        dict_to_be_returned = {
            "threads": amount_of_threads,
        }

        # Select the collection into which the data will be written
        collection_to_write = mongo_db_author_fake_iama_instance[str(name_of_author)]

        # Write that data into the mongo db right now!
        collection_to_write.insert_one(dict_to_be_returned)
