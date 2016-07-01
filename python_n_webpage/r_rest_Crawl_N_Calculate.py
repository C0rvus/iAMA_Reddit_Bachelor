# Sources used within this class:
# 1. (19.05.2016 @ 15:43) -
# https://stackoverflow.com/questions/17474211/how-to-sort-python-list-of-strings-of-numbers
# 2. (24.05.2016 @ 16:29) -
# https://stackoverflow.com/a/73465
# 3. (24.05.2016 @ 18:32) -
# http://stackoverflow.com/questions/497426/deleting-multiple-elements-from-a-list
# 4. (25.05.2016 @ 15:26) -
# https://stackoverflow.com/a/29988426


import praw  # Necessary to receive live data from reddit
import copy  # Necessary to copy value of the starting year - needed for correct csv file name
import math  # Necessary to check for nan values
import datetime  # Necessary for calculating time differences
import time  # Necessary to do some time calculations
import numpy as np  # Necessary for mean calculation
import sys  # Necessary to print out unicode console logs
import collections  # Necessary to sort the dictionary before they will be appended to a list
import operator  # Necessary for correct dictionary sorting
import json      # Necessary for creating json objects
from pymongo import MongoClient  # Necessary to make use of MongoDB

# Instanciates necessary database instances
mongo_DB_Client_Instance = MongoClient('localhost', 27017)

mongo_DB_Threads_Instance = None
mongo_DB_Thread_Collection = None

mongo_DB_Comments_Instance = None
mongo_DB_Comments_Collection = None

# Instanciates a reddit instance
reddit_Instance = praw.Reddit(user_agent="University_Regensburg_iAMA_Crawler_0.001")  # Main reddit functionality
reddit_submission = None

# Refers to the thread creation date
thread_created_utc = 0  # Value received by (Reddit API - live)
thread_author = ""  # Value received by (Reddit API - live)

# Left side panel information will be stored here
thread_title = ""  # Value received by (Reddit API - live)
thread_amount_questions = 0  # Value received by (MongoDB - offline)
thread_amount_unanswered_questions = 0  # Value received by (MongoDB - offline)
thread_duration = 0  # Value received by (Reddit API - live)
thread_id = ""  # Value received by (Reddit API - live)

# Top panel
thread_ups = 0  # Value received by (Reddit API - live)
thread_downs = 0  # Value received by (Reddit API - live)

# Left (stats) panel
thread_time_stamp_last_question = 0  # Value received by (MongoDB - offline)

thread_average_question_score = 0  # Value received by (MongoDB - offline)
thread_average_reaction_time_host = 0  # Value received by (MongoDB - offline)
thread_new_question_every_x_sec = 0  # Value received by (MongoDB - offline)

thread_amount_questions_tier_1 = 0  # Value received by (MongoDB - offline)
thread_amount_questions_tier_x = 0  # Value received by (MongoDB - offline)
thread_question_top_score = 0  # Value received by (MongoDB - offline)
thread_amount_questioners = 0   # Value received by (MongoDB - offline)

# Middle of screen
thread_unanswered_questions = []  # Value received by (MongoDB - offline)
thread_answered_questions = []  # Value received by (MongoDB - offline)

# Contains the answers the author made.. Will be merged later with the answers done on
thread_answers_of_host = []  # Value received by (MongoDB - offline)

# Contains all questions and the appropriate answers to it
# I have to do this separately because otherwise this whole script would be needed to be reworked then..
thread_questions_n_answers = []  # Value received by (MongoDB - offline)

# Contains the unanswered questions prepared
# Prepared means 1. removal of unnecessary values for return and 2. timestamp conversion
# I have to do this separately because otherwise this whole script would be needed to be reworked then..
thread_unanswered_questions_converted = []  # Value received by (MongoDB - offline)

# Object to return (JSON)
json_object_to_return = []


class r_rest_Crawl_N_Calculate:
    def main_method(self,

                    id_thread,

                    un_filter_tier, un_filter_score_equals, un_filter_score_numeric,
                    un_sorting_direction, un_sorting_type,

                    an_filter_tier, an_filter_score_equals, an_filter_score_numeric,
                    an_sorting_direction, an_sorting_type):

        self.clear_variables()

        @staticmethod
        def clear_variables():
            """Resets all variables, to not return duplicated objects.
                Because the REST-Service won't destruct the objects by it self we have to do it manually

            Args:
                -
            Returns:
                -
            """

            global mongo_DB_Client_Instance
            global mongo_DB_Threads_Instance
            global mongo_DB_Thread_Collection
            global mongo_DB_Comments_Instance
            global mongo_DB_Comments_Collection
            global reddit_Instance
            global reddit_submission
            global thread_created_utc
            global thread_author
            global thread_title
            global thread_amount_questions
            global thread_amount_unanswered_questions
            global thread_duration
            global thread_ups
            global thread_downs
            global thread_time_stamp_last_question
            global thread_average_question_score
            global thread_average_reaction_time_host
            global thread_new_question_every_x_sec
            global thread_amount_questions_tier_1
            global thread_amount_questions_tier_x
            global thread_question_top_score
            global thread_answers_of_host
            global thread_questions_n_answers
            global thread_unanswered_questions_converted
            global thread_unanswered_questions
            global thread_answered_questions
            global thread_amount_questioners
            global json_object_to_return

            mongo_DB_Client_Instance = MongoClient('localhost', 27017)

            mongo_DB_Threads_Instance = None
            mongo_DB_Thread_Collection = None

            mongo_DB_Comments_Instance = None
            mongo_DB_Comments_Collection = None

            # Instanciates a reddit instance
            reddit_Instance = praw.Reddit(user_agent="University_Regensburg_iAMA_Crawler_0.001")
            reddit_submission = None

            # Refers to the thread creation date
            thread_created_utc = 0
            thread_author = ""

            # Left side panel information will be stored here
            thread_title = ""
            thread_amount_questions = 0
            thread_amount_unanswered_questions = 0
            thread_duration = 0
            # thread_id = ""

            # Top panel
            thread_ups = 0
            thread_downs = 0

            # Right (stats) panel
            thread_time_stamp_last_question = 0

            thread_average_question_score = 0
            thread_average_reaction_time_host = 0
            thread_new_question_every_x_sec = 0

            thread_amount_questions_tier_1 = 0
            thread_amount_questions_tier_x = 0
            thread_question_top_score = 0
            thread_amount_questioners = 0

            # Middle of screen
            thread_unanswered_questions = []
            thread_answered_questions = []
            thread_answers_of_host = []
            thread_questions_n_answers = []
            thread_unanswered_questions_converted = []

            # Object which is to be returned (JSON)
            json_object_to_return = []
