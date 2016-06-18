# Sources used within this class:
# 1. (09.06.2016 @ 18:20) -
# http://alan-wright.com/programming/tutorial/python/2014/03/09/praw-tutorial/
# 2. (09.06.2016 @ 22:30) -
# https://m.reddit.com/r/RequestABot/comments/42lmgv/need_a_bot_that_can_pull_all_users_and_account/
# 3. (09.06.2016 @ 22:42) - https://github.com/alanwright/RedditBots/blob/master/scripts/UserGoneWild.py

import sys                          # Necessary to use script arguments
import csv                          # Necessary to write data to csv files
import os                           # Necessary to get the name of currently processed file
from pymongo import MongoClient     # Necessary to interact with MongoDB


def check_script_arguments():
    """Checks if enough and correct arguments have been given to run this script adequate

    1. It checks in the first instance if enough arguments have been given
    2. Then necessary variables will be filled with appropriate values

    Args:
        -
    Returns:
        -
    """

    global argument_db_to_choose

    # Whenever not enough arguments were given
    if len(sys.argv) <= 1 or len(sys.argv) > 2:
        print("Not enough arguments were given...")
        print("Terminating script now!")
        sys.exit()

    else:
        # Contains the information which database you want to retrieve data from
        if str(sys.argv[1]).lower() == "iama":
            argument_db_to_choose = str(sys.argv[1]).lower()

        elif "rand" in str(sys.argv[1]).lower():
            argument_db_to_choose = "random"

        else:
            print("Please follow the argument syntax!")
            print("Terminating script now!")
            sys.exit()


def initialize_mongo_db_parameters():
    """Instantiates all necessary variables for the correct usage of the mongoDB client

    Args:
        -
    Returns:
        -
    """

    global mongo_db_client_instance, mongo_db_author_instance, mongo_db_author_collection, \
        mongo_db_author_collection_original

    mongo_db_client_instance = MongoClient('localhost', 27017)

    if argument_db_to_choose == "random":

        mongo_db_author_instance = mongo_db_client_instance['iAMA_Reddit_Authors_Random']

    else:

        mongo_db_author_instance = mongo_db_client_instance['iAMA_Reddit_Authors']

    mongo_db_author_collection = mongo_db_author_instance.collection_names()

    # Contains the amount of collection for the original reddit db
    mongo_db_author_collection_original = int(len(mongo_db_client_instance['iAMA_Reddit_Authors'].collection_names()))


def write_csv_data():
    """Gets all information from every collection within 'iAMA_Reddit_Authors*' database and writes it into a csv file

    Args:
        -
    Returns:
        -
    """

    print("Generating author data (csv) now...")

    # The heading of the csv file..
    data = [['amount_creation_iama_threads',
             'amount_creation_other_threads',
             'amount_of_comments_except_iama',
             'amount_of_comments_iama',
             'author_birth_date',
             'author_comment_karma_amount',
             'author_link_karma_amount',
             'author_name',
             'comment_creation_every_x_sec',
             'thread_creation_every_x_sec',
             'time_acc_birth_first_iama_thread',
             'time_diff_acc_creation_n_first_comment',
             'time_diff_acc_creation_n_first_thread']]

    # noinspection PyTypeChecker

    for j, val in enumerate(mongo_db_author_collection):

        # There is a way more beautiful way of checking this, but I am in a hury now, I am sorry!
        if argument_db_to_choose == "random":
            if j > mongo_db_author_collection_original:
                continue
        else:
            pass

        # noinspection PyTypeChecker
        # print(str(j), "/", len(mongo_db_author_collection))

        # Skips the system.indexes-table which is automatically created by mongodb itself
        if not val == "system.indexes":

            # Contains the collection which corresponds to the author name
            temp_author = mongo_db_author_instance[val]

            # A temporary list containing all information from the iterated collection
            temp_list = [str(temp_author.find()[0].get('amount_creation_iama_threads')),
                         str(temp_author.find()[0].get('amount_creation_other_threads')),
                         str(temp_author.find()[0].get('amount_of_comments_except_iama')),
                         str(temp_author.find()[0].get('amount_of_comments_iama')),
                         str(temp_author.find()[0].get('author_birth_date')),
                         str(temp_author.find()[0].get('author_comment_karma_amount')),
                         str(temp_author.find()[0].get('author_link_karma_amount')),
                         str(temp_author.find()[0].get('author_name')),
                         str(temp_author.find()[0].get('comment_creation_every_x_sec')),
                         str(temp_author.find()[0].get('thread_creation_every_x_sec')),
                         str(temp_author.find()[0].get('time_acc_birth_first_iama_thread')),
                         str(temp_author.find()[0].get('time_diff_acc_creation_n_first_comment')),
                         str(temp_author.find()[0].get('time_diff_acc_creation_n_first_thread'))]

            # Appends that temporary list to the data heading section for correct writing of the csv file
            data.append(temp_list)

    # Defines the path and name of the csv file which will be written after the iteration

    if argument_db_to_choose != "random":

        file_name_csv = str(os.path.basename(__file__))[0:len(os.path.basename(__file__)) - 3] + '_iama.csv'

    else:
        file_name_csv = str(os.path.basename(__file__))[0:len(os.path.basename(__file__)) - 3] + '_random.csv'

    # The csv writer gets referenced here
    with open(file_name_csv, 'w', newline='') as fp:

        # Defines the delimiter here for correct csv writing
        csv_writer = csv.writer(fp, delimiter=',')

        # Writes data into the csv file
        csv_writer.writerows(data)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Necessary variables are defined here

# The mongo client, necessary to connect to mongoDB
mongo_db_client_instance = None

# The data base instance for all author information
mongo_db_author_instance = None

# The amount of all collections within the 'iAMA_Reddit_Authors*' - DB
mongo_db_author_collection = None

# Contains the amount of collections within the original 'iAMA_Reddit_Authors' DB
# This is necessary to not crawl write to much data into the .csv file
mongo_db_author_collection_original = 0

# Will contain information whether you want to analyse the iAMA authors of 'iAMA_Reddit_Authors' db
# or random authors from 'iAMA_Reddit_Authors_Random'
argument_db_to_choose = ""


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Methods which are to be called are here


# Initializes the mongoDB with the arguments given via command line
initialize_mongo_db_parameters()

# Starts the data generation process and writes csv files
write_csv_data()
