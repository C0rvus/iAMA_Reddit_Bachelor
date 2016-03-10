#   This script has been developed with PRAW 3.3.0

from pymongo import MongoClient         # Necessary to interact with MongoDB
from datetime import datetime           # Necessary to create the year out of the thread utc
#  [better than hardcoding the db info here]

import praw                             # Necessary for praw usage
import collections                      # Necessary to sort the dictionary before it will be written into the database


# The mongo client, necessary to connect to mongoDB
mongo_DB_Client_Instance = MongoClient('localhost', 27017)

# The data base instance for the threads
mongo_DB_Threads_Instance_2016 = mongo_DB_Client_Instance.iAMA_Reddit_Threads_2016

# Contains all collection names of the thread database
mongo_DB_Thread_Collection_2016 = mongo_DB_Threads_Instance_2016.collection_names()

# The data base instance for the comments
mongo_DB_Comments_Instance_2016 = mongo_DB_Client_Instance.iAMA_Reddit_Comments_2016

# Contains all collection names of the comments database
mongo_DB_Comments_Collection_2016 = mongo_DB_Comments_Instance_2016.collection_names()


# Retrieves the missing post from reddit and writes its comments into the comments database
def crawl_missing_collection_into_comments_database(name_of_missing_collection):

    # Because crawling could take many hours / days the previously assigned variables
    # could be old and therefore values could be written twice into the database.
    # Therefore we reassign the actual collection name to double check we do
    # not write data twice

    # The mongo client, necessary to connect to mongoDB
    temp_mongo_db_client_instance = MongoClient('localhost', 27017)

    # The data base instance for the comments
    temp_mongo_db_comments_instance_2016 = temp_mongo_db_client_instance.iAMA_Reddit_Comments_2016

    # Contains all collection names of the comments database
    temp_mongo_db_comments_collection_2016 = temp_mongo_db_comments_instance_2016.collection_names()

    # Double checks that data so that not both crawler overwrite each other
    if name_of_missing_collection not in temp_mongo_db_comments_collection_2016:

        # The Main reddit functionality
        reddit_instance = praw.Reddit(user_agent="University_Regensburg_iAMA_Diff_Inverse_0.001")

        # The thread which is to be crawled
        submission_thread = reddit_instance.get_submission(submission_id='' + name_of_missing_collection)

        # Replaces the objects of Type praw.MoreComments with comments (i.e.
        # iterates their tree to the end / expands all comments)
        submission_thread.replace_more_comments(limit=None, threshold=0)

        # Breaks the tree hierarchy and returns a plain straight aligned list containing all fulltext comments
        flat_comments = praw.helpers.flatten_tree(submission_thread.comments)

        # Whenever a thread does not contain a single comment -> create a null
        # entry collection inside the database
        if len(flat_comments) == 0:
            print("    ----- " + str(name_of_missing_collection) +
                  " does not contain single comment. Creation empty collection now")

            # noinspection PyTypeChecker
            data_to_write_into_db = dict({
                'author': None,
                'body': None,
                'created_utc': None,
                'name': None,
                'parent_id': None,
                'ups': None
            })

            # Sorts that dictionary alphabetically ordered
            data_to_write_into_db = collections.OrderedDict(sorted(data_to_write_into_db.items()))

            # Converts the unix utc_time into a date format and converts it to
            # string afterwards
            temp_submission_creation_year = str(datetime.fromtimestamp(submission_thread.created_utc))
            temp_submission_creation_year = temp_submission_creation_year[:4]

            # This method says to look into the appropriate database, depending on the year the thread was created
            mongo_db_reddit = mongo_DB_Client_Instance["iAMA_Reddit_Comments_" + temp_submission_creation_year]

            # Writes the crawled information into the mongoDB
            collection = mongo_db_reddit[str(submission_thread.id)]

            # Write the dictionary "data_to_write_into_db" into the mongo db right now!
            collection.insert_one(data_to_write_into_db)
            print(
                "    +++++ Finished writing " +
                str(name_of_missing_collection) +
                " into " +
                "iAMA_Reddit_Comments_" +
                temp_submission_creation_year +
                "\n")

        # Whenever there were comments / answers within that crawled thread
        else:

            # Iterates over every single comment within the thread [and write it into the
            # appropriate collection in the comments database]
            for idx, val in enumerate(flat_comments):

                # noinspection PyTypeChecker
                data_to_write_into_db = dict({
                    'author': str(val.author),
                    'body': str(val.body),
                    'created_utc': str(val.created_utc),
                    'name': str(val.name),
                    'parent_id': str(val.parent_id),
                    'ups': int(val.ups)
                })

                # Sorts that dictionary alphabetically ordered
                data_to_write_into_db = collections.OrderedDict(sorted(data_to_write_into_db.items()))

                # Converts the unix utc_time into a date format and converts it
                # to string afterwards
                temp_submission_creation_year = str(datetime.fromtimestamp(submission_thread.created_utc))
                temp_submission_creation_year = temp_submission_creation_year[:4]

                # This method says to look into the appropriate database, depending on the year the thread was created
                mongo_db_reddit = mongo_DB_Client_Instance["iAMA_Reddit_Comments_" + temp_submission_creation_year]

                # Writes the crawled information into the mongoDB
                collection = mongo_db_reddit[str(submission_thread.id)]

                # Write the dictionary "data_to_write_into_db" into the mongo db right now!
                collection.insert_one(data_to_write_into_db)

            print(
                "    +++++ Finished writing " +
                str(name_of_missing_collection) +
                " into " +
                "iAMA_Reddit_Comments_2016" +
                "\n")

# Checks whether every collection, which exists in thread database, is also available in the comments database


def check_if_collection_is_missing_in_comments_database():

    # Iterate over every collection within the thread database
    for j in range(0, len(mongo_DB_Thread_Collection_2016)):

        # If that iterated collection does not exist within the comments
        # database - get that data and create that collection
        if not mongo_DB_Thread_Collection_2016[
                            len(mongo_DB_Thread_Collection_2016) - 1 - j] in mongo_DB_Comments_Collection_2016:
            print(
                "The following collection is missing in iAMA_Reddit_Comments_2016 : " +
                mongo_DB_Thread_Collection_2016[len(mongo_DB_Thread_Collection_2016) - 1 - j])

            crawl_missing_collection_into_comments_database(str(
                mongo_DB_Thread_Collection_2016[len(mongo_DB_Thread_Collection_2016) - 1 - j]))


# Retrieves the missing post from reddit and writes its properties into the threads database
def crawl_missing_collection_into_threads_database(name_of_missing_collection):

    # The mongo client, necessary to connect to mongoDB
    temp_mongo_db_client_instance = MongoClient('localhost', 27017)

    # The data base instance for the threads
    temp_mongo_db_threads_instance_2016 = temp_mongo_db_client_instance.iAMA_Reddit_Threads_2016

    # Contains all collection names of the thread database
    temp_mongo_db_thread_collection_2016 = temp_mongo_db_threads_instance_2016.collection_names()

    # Double checks that data so that not both crawler overwrite each other
    if name_of_missing_collection not in temp_mongo_db_thread_collection_2016:

        # The Main reddit functionality
        reddit_instance = praw.Reddit(user_agent="University_Regensburg_iAMA_Crawler_0.001")

        # The thread which is to be crawled
        submission = reddit_instance.get_submission(submission_id='' + name_of_missing_collection)

        # Because down votes are not accessable via reddit API, we have calculated it by our own here
        ratio = reddit_instance.get_submission(submission.permalink).upvote_ratio

        total_votes = int(round((ratio * submission.score) / (2 * ratio - 1))
                          if ratio != 0.5 else round(submission.score / 2))
        downs = total_votes - submission.score

        # noinspection PyTypeChecker
        data_to_write_into_db = dict({
            'author': str(submission.author),
            'created_utc': str(submission.created_utc),
            'downs': int(downs),
            'num_Comments': str(submission.num_comments),
            'selftext': str(submission.selftext),
            'title': str(submission.title),
            'ups': int(submission.ups)
        })

        # Sorts that dictionary alphabetically ordered
        data_to_write_into_db = collections.OrderedDict(sorted(data_to_write_into_db.items()))

        # Converts the unix utc_time into a date format and converts it to
        # string afterwards
        temp_submission_creation_year = str(datetime.fromtimestamp(submission.created_utc))
        temp_submission_creation_year = temp_submission_creation_year[:4]

        # This method says to look into the appropriate database, depending on the year the thread was created
        mongo_db_reddit = mongo_DB_Client_Instance["iAMA_Reddit_Threads_" + temp_submission_creation_year]

        # Writes the crawled information into the mongoDB
        collection = mongo_db_reddit[str(submission.id)]

        # Write the dictionary "data_to_write_into_db" into the mongo db right now!
        collection.insert_one(data_to_write_into_db)

        print(
            "    +++++ Finished writing " +
            str(name_of_missing_collection) +
            " into " +
            "iAMA_Reddit_Threads_" +
            temp_submission_creation_year +
            "\n")

# Checks whether every collection, which exists in comments database, is also available in the threads database


def check_if_collection_is_missing_in_threads_database():

    # Iterate over every collection within the comments database
    for j in range(0, len(mongo_DB_Comments_Collection_2016)):

        # If that iterated collection does not exist within the thread database
        # - get that data and create that collection
        if not mongo_DB_Comments_Collection_2016[
                len(mongo_DB_Comments_Collection_2016) - 1 - j] in mongo_DB_Thread_Collection_2016:
            print(
                "The following collection is missing in iAMA_Reddit_Threads_2016 : " +
                mongo_DB_Comments_Collection_2016[len(mongo_DB_Comments_Collection_2016) - 1 -j])

            crawl_missing_collection_into_threads_database(str(
                mongo_DB_Comments_Collection_2016[len(mongo_DB_Comments_Collection_2016) - 1 - j]))


# Creates missing collections within the comments database
check_if_collection_is_missing_in_comments_database()

# Creates missing collections within the threads database
check_if_collection_is_missing_in_threads_database()
