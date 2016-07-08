# Sources used within this class:
# 1. (19.05.2016 @ 15:43) -
# https://stackoverflow.com/questions/17474211/how-to-sort-python-list-of-strings-of-numbers
# 2. (24.05.2016 @ 16:29) -
# https://stackoverflow.com/a/73465
# 3. (24.05.2016 @ 18:32) -
# http://stackoverflow.com/questions/497426/deleting-multiple-elements-from-a-list
# 4. (25.05.2016 @ 15:26) -
# https://stackoverflow.com/a/29988426

import praw                 # Necessary to receive live data from reddit
import copy                 # Necessary to copy value of the starting year - needed for correct csv file name
import math                 # Necessary to check for nan values
import datetime             # Necessary for calculating time differences
import time                 # Necessary to do some time calculations
import numpy as np          # Necessary for mean calculation
import sys                  # Necessary to print out unicode console logs
import collections          # Necessary to sort the dictionary before they will be appended to a list
import operator             # Necessary for correct dictionary sorting
import json                 # Necessary for creating json objects
from pymongo import MongoClient  # Necessary to make use of MongoDB


# Instanciates necessary database instances
mongo_db_client_instance = MongoClient('localhost', 27017)

mongo_db_author_fake_iama_instance = mongo_db_client_instance['fake_iAMA_Reddit_Authors']
mongo_db_author_fake_iama_collection_names = mongo_db_author_fake_iama_instance.collection_names()

mongo_db_author_comments_instance = mongo_db_client_instance['fake_iAMA_Reddit_Comments']
mongo_db_author_comments_collection = mongo_db_author_comments_instance.collection_names()

# Instanciates a reddit instance
reddit_instance = praw.Reddit(user_agent="University_Regensburg_iAMA_Crawler_0.001")  # Main reddit functionality

# The necessary reddit submission
reddit_submission = None

# Refers to the thread creation date
thread_created_utc = 0  # Value received by (Reddit API - live)
thread_author = ""  # Value received by (Reddit API - live)

# Various thread information are defined here
thread_title = ""  # Value received by (Reddit API - live)
thread_amount_questions = 0  # Value received by (MongoDB - offline)
thread_amount_unanswered_questions = 0  # Value received by (MongoDB - offline)
thread_duration = 0  # Value received by (Reddit API - live)
thread_id = ""  # Value received by (Reddit API - live)
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

# All (un)answreed questions will reside here
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


# noinspection PyPep8Naming
class r_rest_Crawl_N_Calculate_Data:

    def main_method(self,

                    author_name,
                    id_thread,

                    un_filter_tier, un_filter_score_equals, un_filter_score_numeric,
                    un_sorting_direction, un_sorting_type,

                    an_filter_tier, an_filter_score_equals, an_filter_score_numeric,
                    an_sorting_direction, an_sorting_type):

        """Defines the main method which will be called by listening on a certain REST-Interface

        Args:
            self:   Self representation of the class [necessary to use methods within the class itself]

            author_name(str): The name of the author who currently processed threads

            id_thread(str): The ID of the thread which will be searched for within the database


            un_filter_tier(str) : The kind of tier for which the questions will be filtered accordingly (all / 1 / x)
             for unanswered questions
            un_filter_score_equals(str) : The kind of comparison the questions will be filtered on (eql / grt / lrt)
             for unanswered questions
            un_filter_score_numeric(str): The "number" of score / upvote which will be used to filter the questions
             (int)for unanswered questions
            un_sorting_direction(str): The direction the questions will be filtered after (asc / desc)
             for unanswered questions
            un_sorting_type(str): The type of information the questions will be filtered after
             (author, creation, score, random) for unanswered questions

            an_filter_tier(str) : The kind of tier for which the questions will be filtered accordingly (all / 1 / x)
             for answered questions
            an_filter_score_equals(str) : The kind of comparison the questions will be filtered on (eql / grt / lrt)
             for answered questions
            an_filter_score_numeric(str): The "number" of score / upvote which will be used to filter the questions
             (int) for answered questions
            an_sorting_direction(str): The direction the questions will be filtered after (asc / desc)
             for answered questions
            an_sorting_type(str): The type of information the questions will be filtered after
            (author, creation, score, random) for answered questions

        Returns:
            create_json_object (json): A complex json object containing

                1. Information about various, thread related statistics
                2. All (un)answered questions (& answers) sorted and filtered according to the parameters given

        """

        # Crawl and write that author information (threads + comments from it) into the various databases
        self.get_n_write_author_information(author_name)

        # Clears all variables to not return objects / questions twice
        self.clear_variables()

        # Assigns the reddit thread submission to an appropriate object
        self.get_thread_submission(str(id_thread))

        # Assigns the thread created_utc data
        self.fill_misc_thread_data()

        # Assigns data to left and top panel
        self.fill_left_n_top_panel_data(self)

        # Assigns data to the right panel
        self.fill_right_panel_data(self, str(id_thread))

        # Calculates necessary question statistics
        self.calculate_question_stats(self)

        # Processes the unanswered questions depending on the information given
        self.sort_n_filter_questions(thread_unanswered_questions, str(un_filter_tier), str(un_filter_score_equals),
                                     str(un_filter_score_numeric), str(un_sorting_direction), str(un_sorting_type))

        # Processes the answered questions depending on the information given
        self.sort_n_filter_questions(thread_answered_questions, str(an_filter_tier), str(an_filter_score_equals),
                                     str(an_filter_score_numeric), str(an_sorting_direction), str(an_sorting_type))

        # This method merges answered questions and their respective answers in a way to easen the display in the page
        self.build_list_containing_q_n_a(self)

        # Prepares the unanswered questions for JSON transport and removes unncessary data, which was necessary
        # before due to calculation of stats
        self.prepare_unanswered_questions(self)

        # Builds the JSON object for correct return
        self.create_json_object()

        # The value which is to be returned (JSON-Object)
        if json_object_to_return != "" or json_object_to_return is not None:
            return json_object_to_return
        else:
            return "At the moment I have no data for you!"

    @staticmethod
    def get_n_write_author_information(name_of_author):
        """Crawls data from the author into the mongodb

            At first all previously stored data will be dropped and then the new one will be crawled.
            This may be slow at some times but it enables us to give the user a better iAMA experience, because
            he will immediately receive new data upon posting / requesting.

        Args:
            name_of_author (str): The name of the author whose data is to be crawled

        Returns:
            -

        """

        # Necessary to wait 5 seconds, before we try to receive data from reddit
        # This is because a real reddit live experience is not possible...
        # Whenever you try to receive data directly after you have posted something on reddit, you will receive
        # the old data.. (reddit is not that fast).. therefore we will wait a few seconds.
        # time.sleep(5)

        # Anonymous inner method to write comments into the database
        def write_comments_into_db(id_of_thread):
            """Writes all comments for all threads, the iAMA host created into the database.

                Storing comments into the database instead of always crawling them live, when demanded, allows faster
                retrieval and a better reactivity of the website

            Args:
                id_of_thread (str): The id of the thread whose comments are to be stored into the database.

            Returns:
                -

            """

            # Drop comments collections here, before they will be recrawled
            mongo_db_client_instance['fake_iAMA_Reddit_Comments'].drop_collection(id_of_thread)

            # Retrieves the submission object from reddit
            submission = reddit_instance.get_submission(submission_id=id_of_thread)

            # Breaks up comments hierarchy
            submission.replace_more_comments(limit=None, threshold=0)
            flat_comments = praw.helpers.flatten_tree(submission.comments)

            # Whenever no comments have been made at all yet!
            if len(flat_comments) == 0:
                # noinspection PyTypeChecker
                returned_json_data = dict({
                    'author': None,
                    'body': None,
                    'created_utc': None,
                    'name': None,
                    'parent_id': None,
                    'ups': None
                })

                # Sorts the dictionary alphabetically correct
                returned_json_data = collections.OrderedDict(sorted(returned_json_data.items()))

                # Defines the position where the calculated information should be written into
                collection = mongo_db_author_comments_instance[str(id_of_thread)]

                # Writes that information into the database
                collection.insert_one(returned_json_data)

            else:
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
        mongo_db_client_instance['fake_iAMA_Reddit_Authors'].drop_collection(str(name_of_author))

        # The instance of the thread iama host
        reddit_thread_host = reddit_instance.get_redditor(name_of_author)

        # Contains all submissions of the thread creator
        submitted = reddit_thread_host.get_submitted(limit=None)

        # Iterates over every submission the author made
        for link in submitted:

            # Truncate the thread id (removes 't3_' on top of the thread)
            threads_id = str(link.name)[3:]
            amount_of_threads.append(threads_id)

            # Write comments into the database
            write_comments_into_db(threads_id)

        # Sorts the list in alphabetically order
        amount_of_threads.sort()

        # The dict to be returned
        dict_to_be_returned = {
            "threads": amount_of_threads,
        }

        # Select the collection into which the data will be written
        collection_to_write = mongo_db_author_fake_iama_instance[str(name_of_author)]

        # Write that data into the mongo db right now!
        collection_to_write.insert_one(dict_to_be_returned)

    @staticmethod
    def clear_variables():
        """Resets all variables, to not return duplicate objects.
            Because the REST-Service won't destruct the objects by it self we have to reset them manually here

        Args:
            -

        Returns:
            -
        """

        global mongo_db_client_instance
        global mongo_db_author_fake_iama_instance
        global mongo_db_author_fake_iama_collection_names
        global mongo_db_author_comments_instance
        global mongo_db_author_comments_collection
        global reddit_instance
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

        # Resets the mongoclient instance
        mongo_db_client_instance = MongoClient('localhost', 27017)

        # Resets the author db - instance and collection
        mongo_db_author_fake_iama_instance = mongo_db_client_instance['fake_iAMA_Reddit_Authors']
        mongo_db_author_fake_iama_collection_names = mongo_db_author_fake_iama_instance.collection_names()

        # Resets the comments db - instance and collection
        mongo_db_author_comments_instance = mongo_db_client_instance['fake_iAMA_Reddit_Comments']
        mongo_db_author_comments_collection = mongo_db_author_comments_instance.collection_names()

        # Instanciates a reddit instance
        reddit_instance = praw.Reddit(user_agent="University_Regensburg_iAMA_Crawler_0.001")
        reddit_submission = None

        # Refers to the thread creation date
        thread_created_utc = 0
        thread_author = ""

        # Left side panel information will be stored here
        thread_title = ""
        thread_amount_questions = 0
        thread_amount_unanswered_questions = 0
        thread_duration = 0
        thread_ups = 0
        thread_downs = 0

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

    @staticmethod
    def get_thread_submission(id_of_thread):
        """Receives the thread information live from Reddit via the Reddit-API

        Args:
            id_of_thread (str): The id of the thread whose data are to be retrieved and stored globally

        Returns:
            -

        """

        global reddit_submission

        reddit_submission = reddit_instance.get_submission(submission_id=id_of_thread)

    @staticmethod
    def fill_misc_thread_data():
        """Retrieves the creation time stamp and the thread author from the submission

        Args:
            -

        Returns:
            -

        """

        global thread_created_utc
        global thread_author

        thread_created_utc = float(reddit_submission.created_utc)
        thread_author = str(reddit_submission.author)

    @staticmethod
    def fill_left_n_top_panel_data(self):
        """Fills data to the left and the top panel

        Args:
            self:   Self representation of the class [necessary to use methods within the class itself]

        Returns:
            -

        """

        global thread_title
        global thread_duration
        global thread_id
        global thread_ups
        global thread_downs

        thread_title = reddit_submission.title
        thread_id = reddit_submission.id
        thread_ups = reddit_submission.ups

        # Calls external methods for calculation purpose
        thread_downs = self.calculate_down_votes()
        thread_duration = self.calculate_time_difference(thread_created_utc, int(time.time()))

    @staticmethod
    def fill_right_panel_data(self, id_of_thread):
        """Calculates various statistics for the left panel of the page

        Args:
            self:   Self representation of the class [necessary to use methods within the class itself]

            id_of_thread: The id of the thread which is to be processed

        Returns:
            -
        """

        global thread_amount_questions
        global thread_amount_unanswered_questions
        global thread_time_stamp_last_question
        global thread_average_question_score
        global thread_average_reaction_time_host
        global thread_new_question_every_x_sec
        global thread_amount_questions_tier_1
        global thread_amount_questions_tier_x
        global thread_question_top_score
        global thread_unanswered_questions
        global thread_answered_questions

        # Needs to get reinitialized because of previous deleting / recrawling behaviour
        comments_collection = mongo_db_client_instance['fake_iAMA_Reddit_Comments'][id_of_thread]
        comments_cursor = list(comments_collection.find())
        cursor_copy = copy.copy(comments_cursor)

        # Iterates over every comment within that thread
        for i, val in enumerate(comments_cursor):

            comment_text = val.get("body")
            comment_author = val.get("author")
            comment_parent_id = val.get("parent_id")
            comment_timestamp = val.get("created_utc")
            comment_id = val.get("name")
            comment_ups = val.get("ups")

            # Whenever the comment text, the author and the comments' parent_id is not None
            if comment_text is not None and comment_author is not None and comment_parent_id is not None:

                bool_comment_is_question = self.checker_comment_is_question(comment_text)
                bool_comment_is_question_on_tier_1 = self.checker_comment_is_question_on_tier_1(comment_parent_id)
                bool_comment_is_not_from_thread_author = self.checker_comment_is_not_from_thread_author(
                    thread_author, comment_author)

                # Checks for question and tier behaviour
                if bool_comment_is_question is True and bool_comment_is_not_from_thread_author is True:

                    thread_amount_questions += 1

                    # Tier 1 checking
                    if bool_comment_is_question_on_tier_1 is True:
                        thread_amount_questions_tier_1 += 1

                    # Tier X checking
                    elif bool_comment_is_question_on_tier_1 is False:
                        thread_amount_questions_tier_x += 1

                    # Check whether that iterated comment is answered by the host
                    comment_has_been_answered_by_thread_author = \
                        self.check_if_comment_has_been_answered_by_thread_author(
                            self, thread_author, comment_id, comment_timestamp, cursor_copy
                        )

                    # Fills necessary data of the question here
                    dict_question = {
                        "question_id": comment_id,
                        "question_author": comment_author,
                        "question_timestamp": comment_timestamp,
                        "question_answer_time_host":
                            comment_has_been_answered_by_thread_author["question_host_reaction_time"],
                        "question_upvote_score": comment_ups,
                        "question_on_tier_1": bool_comment_is_question_on_tier_1,
                        "question_text": comment_text,
                        "question_answered_by_host":
                            comment_has_been_answered_by_thread_author["question_answered_from_host"]
                    }

                    # Whenever the answer to that comment is from the author
                    if comment_has_been_answered_by_thread_author["question_answered_from_host"] is True:

                        # Append it to the answered questions list
                        dict_question = collections.OrderedDict(sorted(dict_question.items()))
                        thread_answered_questions.append(dict_question)

                    elif comment_has_been_answered_by_thread_author["question_answered_from_host"] is False:

                        # Append it to the unanswered questions list
                        dict_question = collections.OrderedDict(sorted(dict_question.items()))
                        thread_unanswered_questions.append(dict_question)
                        thread_amount_unanswered_questions += 1

                    else:
                        # Nothing to do here
                        pass

                        # reaction time host berechnen

                # Skip that reaction (comment / question)
                else:
                    continue

                # Reassigns the comment ups
                if thread_question_top_score < comment_ups:
                    thread_question_top_score = comment_ups

                # Fills the value of the last question posted
                if float(comment_timestamp) > float(thread_time_stamp_last_question):
                    thread_time_stamp_last_question = float(comment_timestamp)

            # Whenever a comment has been deleted or has, somehow, null values in it.. do not process it
            else:
                continue

    @staticmethod
    def calculate_question_stats(self):
        """Calculates remaining question statistics, like average question score, reaction time and question creation
            interval in seconds

        Args:
            self:   Self representation of the class [necessary to use methods within the class itself]
        Returns:
            -
        """

        global thread_average_question_score
        global thread_average_reaction_time_host
        global thread_new_question_every_x_sec
        global thread_amount_questioners

        # Will contain all scores of every question
        question_scores = []
        # Will contain the reaction time of the iama host
        question_host_reaction_time = []
        # Will contain the timestamps of every question, beginning with the thread creation date
        question_every_x_sec_timestamp_holder = [thread_created_utc]
        # Will contain the actual concrete time difference in seconds
        question_every_x_sec = []

        # Will contain questioners of every question
        questioner_holder = []

        # Iterates over the unanswered questions
        for i, val in enumerate(thread_unanswered_questions):
            question_scores.append(val['question_upvote_score'])

            question_author = str(val['question_author'])

            # Whenever the author is not yet listed within the list add him to it
            if question_author not in questioner_holder:
                questioner_holder.append(question_author)
            else:
                pass

            # noinspection PyTypeChecker
            question_every_x_sec_timestamp_holder.append(float(val['question_timestamp']))

        # Iterates over the answered questions
        for i, val in enumerate(thread_answered_questions):
            question_scores.append(val['question_upvote_score'])

            question_author = str(val['question_author'])

            # Whenever the author is not yet listed within the list add him to it
            if question_author not in questioner_holder:
                questioner_holder.append(question_author)
            else:
                pass

            # noinspection PyTypeChecker
            question_every_x_sec_timestamp_holder.append(float(val['question_timestamp']))

            if val['question_answer_time_host'] != 0:
                question_host_reaction_time.append(val['question_answer_time_host'])

        # Sorts the questions for every x seconds the reverse way !
        question_every_x_sec_timestamp_holder.sort(key=float, reverse=True)

        # Iterates over every question
        for i in range(0, len(question_every_x_sec_timestamp_holder)):

            # Avoids index out of bounds error message
            if i != len(question_every_x_sec_timestamp_holder) - 1:
                # Calculates time difference here
                question_every_x_sec.append(
                    self.calculate_time_difference(question_every_x_sec_timestamp_holder[i + 1],
                                                   question_every_x_sec_timestamp_holder[i]))

        # Assigns necessary values for correct calculation
        if len(question_scores) == 0:
            thread_average_question_score = 0
        else:
            thread_average_question_score = np.mean(question_scores)

        # Whenever the host has not yet reacted (made no comment or whatsoever)(
        if len(question_host_reaction_time) == 0:
            # Prevents some errors during mean creation
            thread_average_reaction_time_host = 0
        else:
            thread_average_reaction_time_host = np.mean(question_host_reaction_time)

        # Whenever no question has been posted at all
        if len(question_every_x_sec) == 0:
            thread_new_question_every_x_sec = 0
        else:
            thread_new_question_every_x_sec = np.mean(question_every_x_sec)

        thread_amount_questioners = len(questioner_holder)

        # Prevention of nAn declaration (could mess up JSON Parsing for javascript)
        if math.isnan(thread_average_reaction_time_host):
            thread_average_reaction_time_host = 0
        else:
            pass

        # Prevention of nAn declaration (could mess up JSON Parsing for javascript)
        if math.isnan(thread_new_question_every_x_sec):
            thread_new_question_every_x_sec = 0
        else:
            pass

    @staticmethod
    def calculate_down_votes():
        """Calculates the amount of down votes of a thread

            This is actually not necessary anymore but will be left inside, whenever downvotes will be reimplemented
            to the website.

        Args:
            -

        Returns:
            object (int): The amount of time difference between two values in seconds

        """

        # Because down votes are not accessable via reddit API, we have calculated it by our own here
        ratio = reddit_instance.get_submission(reddit_submission.permalink).upvote_ratio

        # Calculates the total score amount
        total_votes = int(round((ratio * reddit_submission.score) / (2 * ratio - 1))
                          if ratio != 0.5 else round(reddit_submission.score / 2))

        return total_votes - reddit_submission.score

    @staticmethod
    def calculate_time_difference(time_value_1, time_value_2):
        """Calculates the time difference between two floats in epoch style and returns seconds

        Args:
            time_value_1 (float): The first time value to be used for calculation
            time_value_2 (float): The second time value to be used for calculation
        Returns:
            time_diff_seconds (int): The amount of time difference in seconds
        """

        # Converts the the first time unit into a comparable format
        temp_time_value_1 = float(time_value_1)

        temp_time_value_1_converted_1 = datetime.datetime.fromtimestamp(
            temp_time_value_1).strftime('%d-%m-%Y %H:%M:%S')

        # Reformatation of time string
        temp_time_value_1_converted_2 = datetime.datetime.strptime(
            temp_time_value_1_converted_1, '%d-%m-%Y %H:%M:%S')

        # Converts the current time into a comparable time format
        temp_time_value_2 = float(time_value_2)

        temp_time_value_2_converted_1 = datetime.datetime.fromtimestamp(
            temp_time_value_2).strftime('%d-%m-%Y %H:%M:%S')

        # Reformatation of time string
        temp_time_value_2_converted_2 = datetime.datetime.strptime(
            temp_time_value_2_converted_1, '%d-%m-%Y %H:%M:%S')

        # Contains the amount of time units (minutes)
        time_diff_seconds = (temp_time_value_2_converted_2 - temp_time_value_1_converted_2).total_seconds()

        return time_diff_seconds

    # Checker methods below here for correct data calculation
    @staticmethod
    def checker_comment_is_question(string_to_check):
        """Simply checks whether a given string is a question or not

        1. This method simply checks wether a question mark exists within that string or not..
            This is just that simple because messing around with natural processing kits to determine the semantic sense
            would blow up my bachelor work...

        Args:
            string_to_check (str) : The string which will be checked for a question mark

        Returns:
            True (bool): Whenever the given string is a question
            False (bool): Whenever the given string is not a question

        """

        if "?" in string_to_check:
            return True
        else:
            return False

    @staticmethod
    def checker_comment_is_question_on_tier_1(string_to_check):
        """Simply checks whether a given string is a question posted on tier 1 or not

        1. This method simply checks whether a question has been posted on tier 1 by looking whether the given
            string contains the substring "t3_" or not

        Args:
            string_to_check (str): The string which will be checked for "t3_" appearance in it

        Returns:
            -

        """

        if "t3_" in string_to_check:
            return True
        else:
            return False

    @staticmethod
    def checker_comment_is_not_from_thread_author(author_of_thread, comment_author):
        """Checks whether both strings are equal or not

        1. This method simply checks wether both strings match each other or not.
            I have built this extra method to have a better overview in the main code..

        Args:
            author_of_thread (str) : The name of the thread author (iAMA-Host)
            comment_author (str) : The name of the comments author

        Returns:
            True (bool): Whenever the strings do not match
            False (bool): Whenever the strings do match that given question

        """

        if author_of_thread != comment_author:
            return True
        else:
            return False

    @staticmethod
    def check_if_comment_has_been_answered_by_thread_author(self, author_of_thread, comment_acutal_id,
                                                            comment_timestamp, comments_cursor):
        """Checks whether both strings are equal or not

        1. A dictionary containing flags whether that a question is answered by the host with the appropriate timestamp
            will be created in the beginning.
        2. Then the method iterates over every comment within that thread
            1.1. Whenever an answer is from the iAMA hosts and the processed comments 'parent_id' matches the iAMA hosts
                comments (answers) id, the returned dict will contain appropriate values and will be returned
            1.2. If this is not the case, it will be returned in its default condition

        Args:
            self:   Self representation of the class [necessary to use methods within the class itself]
            author_of_thread (str) : The name of the thread author (iAMA-Host)
            comment_acutal_id (str) : The id of the actually processed comment
            comment_timestamp (float): The timestamp of the currently processed comment
            comments_cursor (Cursor) : The cursor which shows to the amount of comments which can be iterated

        Returns:
            True (bool): Whenever the strings do not match
            False (bool): Whenever the strings do match

        """

        # Necessary to refer to this variable, to add the answers to it
        global thread_answers_of_host

        dict_to_be_returned = {
            "question_answered_from_host": False,
            "question_host_reaction_time": 0
        }

        # Iterates over every comment
        for i, val in enumerate(comments_cursor):

            check_comment_parent_id = val.get("parent_id")
            actual_comment_author = val.get("author")

            # Whenever the iterated comment is from the iAMA-Host and that comment has the question as parent_id
            if (self.checker_comment_is_not_from_thread_author(str(author_of_thread), actual_comment_author) is False) \
                    and (check_comment_parent_id == comment_acutal_id):
                dict_to_be_returned["question_answered_from_host"] = True

                # The difference between timestamp of the hosts answer and the questions timestamp
                dict_to_be_returned["question_host_reaction_time"] = self.calculate_time_difference(
                    comment_timestamp, val.get("created_utc"))

                # A dict containing the answer, the host made
                dict_to_add_to_answers_of_host_list = {
                    "answer_text": val.get("body"),
                    "created_utc": val.get("created_utc"),
                    "ups": val.get("ups"),
                    "id_of_answer": val.get("name"),
                    "id_of_related_q": val.get("parent_id")
                }

                thread_answers_of_host.append(dict_to_add_to_answers_of_host_list)

                return dict_to_be_returned

        # This is the case whenever a comment has not a single thread or the comment / question has not been answered
        return dict_to_be_returned

    @staticmethod
    def sort_n_filter_questions(questions_to_be_sorted, filter_tier, filter_score_equals, filter_score_numeric,
                                sorting_direction, sorting_type):
        """Sorts and filters given question lists depending on parameters received via REST call

        Args:
            questions_to_be_sorted (list): Contains all questions which will be processed later on

            filter_tier (str): Contains the information, which questions, depending on the tier, will be sorted out
                (all / 1 / X)
            filter_score_equals(str): Contains the information to filter a tier depending on a special score
                (eql [equal] / grt [greather than] / lrt [lesser than])
            filter_score_numeric(str): The upvote score which will be used for filtering

            sorting_direction(str): The direction which will be used for sorting the questions
                (asc [ascending] / des [descending])
            sorting_type(str): The kind of type which will be used for sorting
                (author / creation / score / random)

        Returns:
            -

        """

        # Contains the index numbers of questions which are to be deleted later on
        indices_to_be_deleted = []

        # Iterates over every question and filtering them depending on the settings given
        for i, val in enumerate(questions_to_be_sorted):

            # Whenever the tier filter '1' has been selected
            if filter_tier == "1" and (filter_score_numeric != "" or filter_score_numeric is not None):

                if val["question_on_tier_1"] is False:
                    indices_to_be_deleted.append(i)

                elif filter_score_equals == "eql" and (val["question_upvote_score"] != int(filter_score_numeric)):
                    indices_to_be_deleted.append(i)

                elif filter_score_equals == "grt" and (val["question_upvote_score"] < int(filter_score_numeric)):
                    indices_to_be_deleted.append(i)

                elif filter_score_equals == "lrt" and (val["question_upvote_score"] > int(filter_score_numeric)):
                    indices_to_be_deleted.append(i)

                else:
                    pass

            # Whenever the tier filter 'x' has been selected
            elif filter_tier == "x" and (filter_score_numeric != "" or filter_score_numeric is not None):

                if val["question_on_tier_1"] is True:
                    indices_to_be_deleted.append(i)

                elif filter_score_equals == "eql" and (val["question_upvote_score"] != int(filter_score_numeric)):
                    indices_to_be_deleted.append(i)

                elif filter_score_equals == "grt" and (val["question_upvote_score"] < int(filter_score_numeric)):
                    indices_to_be_deleted.append(i)

                elif filter_score_equals == "lrt" and (val["question_upvote_score"] > int(filter_score_numeric)):
                    indices_to_be_deleted.append(i)

                else:
                    pass

            # Whenever the tier filter 'all' has been selected
            elif filter_tier == "all" and (filter_score_numeric != "" or filter_score_numeric is not None):

                if filter_score_equals == "eql" and (val["question_upvote_score"] != int(filter_score_numeric)):
                    indices_to_be_deleted.append(i)

                elif filter_score_equals == "grt" and (val["question_upvote_score"] < int(filter_score_numeric)):
                    indices_to_be_deleted.append(i)

                elif filter_score_equals == "lrt" and (val["question_upvote_score"] > int(filter_score_numeric)):
                    indices_to_be_deleted.append(i)

                else:
                    pass

            else:
                pass

        # Kicks the indices out of the question list.. beginning with the highest index number
        for i in sorted(indices_to_be_deleted, reverse=True):
            # Removes messages from the original question list, which have been "flagged" before
            del questions_to_be_sorted[i]

        # Whenever the questions should be sorted the ascending way
        if str(sorting_direction) == "asc":

            if str(sorting_type) == "author":
                questions_to_be_sorted.sort(key=operator.itemgetter('question_author'), reverse=False)

            elif str(sorting_type) == "creation":
                questions_to_be_sorted.sort(key=operator.itemgetter('question_timestamp'), reverse=False)

            elif str(sorting_type) == "score":
                questions_to_be_sorted.sort(key=operator.itemgetter('question_upvote_score'), reverse=False)

            else:
                pass
        # Whenever the questions should be sorted the descending way
        elif str(sorting_direction) == "des":

            if str(sorting_type) == "author":
                questions_to_be_sorted.sort(key=operator.itemgetter('question_author'), reverse=True)

            elif str(sorting_type) == "creation":
                questions_to_be_sorted.sort(key=operator.itemgetter('question_timestamp'), reverse=True)

            elif str(sorting_type) == "score":
                questions_to_be_sorted.sort(key=operator.itemgetter('question_upvote_score'), reverse=True)
        # Do as nothing would have happened
        else:
            pass

        # Shuffle all questions if 'random' has been selected on the website
        if str(sorting_type) == "random":

            np.random.shuffle(questions_to_be_sorted)

        # Otherwise do nothing here
        else:
            pass

    @staticmethod
    def convert_epoch_to_time(timeAsString):

        time_to_days = int(int(timeAsString) / 60 / 60 / 24)
        time_to_hours = int(int(timeAsString) / 60 / 60)
        value_to_return = None

        if time_to_days == 1:
            value_to_return = str(time_to_days) + " day ago"

        elif time_to_days >= 2:
            value_to_return = str(time_to_days) + " days ago"

        # happened within 24 h
        elif time_to_days <= 0:

            if time_to_hours <= 1:
                value_to_return = "recently"
            else:
                value_to_return = str(time_to_hours) + " hours ago"

        else:
            pass

        return value_to_return

    @staticmethod
    def build_list_containing_q_n_a(self):
        """Prepares data for display in the "answered questions" panel

            This method iterates over all answered questions and all answers the host made.
            Furthermore it merges them together into pairs for a easy display of it on the website

        Args:
            self : Self reference - necessary to use methods within this class

        Returns:
            -

        """

        global thread_questions_n_answers

        # Iterates over every answered question and subiterates its answers
        for i, val_1 in enumerate(thread_answered_questions):

            # Will contain the question (1st place) and the answer to it (2nd place)
            temp_list_q_n_a = {
                "question_id": val_1.get("question_id")[3:],
                "question_author": val_1.get("question_author"),
                "question_timestamp": self.convert_epoch_to_time
                (self.calculate_time_difference(val_1.get('question_timestamp'), int(time.time()))),
                "question_upvote_score": val_1.get("question_upvote_score"),
                "question_text": val_1.get("question_text"),

                "answer_id": None,
                "answer_timestamp": None,
                "answer_upvote_score": None,
                "answer_text": None
            }

            # Iterates over every answer of the host
            for j, val_2 in enumerate(thread_answers_of_host):

                # Whenever the answer of a given question has been found append them to the q_n_a - list
                if val_2.get('id_of_related_q') == val_1.get('question_id'):

                    # Refers to necessary variables
                    temp_list_q_n_a["answer_id"] = val_2.get('id_of_answer')[3:]
                    temp_list_q_n_a["answer_timestamp"] = self.convert_epoch_to_time(self.calculate_time_difference
                                                                                     (val_2.get('created_utc'),
                                                                                      int(time.time())))
                    temp_list_q_n_a["answer_upvote_score"] = val_2.get('ups')
                    temp_list_q_n_a["answer_text"] = val_2.get('answer_text')

                    # Append that q & a combination to the global list
                    thread_questions_n_answers.append(temp_list_q_n_a)

                else:
                    pass

    @staticmethod
    def prepare_unanswered_questions(self):
        """Re-prepares the unanswered questions for correct display on the website

            It is necessary to re-prepare and strip down information from the questions.
            If we would not do this there would be huge overhead in JSON - rest-transfer..
            (i.E. the website does not flags like "answered_by_host" == true, etc..)

        Args:
            self : Self reference - necessary to use methods within this class

        Returns:
            -

        """

        # Iterates over all unanswered questions and assigns necessary values
        for i, val in enumerate(thread_unanswered_questions):
            dict_to_append = {
                "question_id": val['question_id'][3:],
                "question_author": val['question_author'],
                "question_timestamp": self.convert_epoch_to_time(self.calculate_time_difference(
                    val['question_timestamp'], int(time.time()))),
                "question_upvote_score": val['question_upvote_score'],
                "question_text": val['question_text']
            }

            thread_unanswered_questions_converted.append(dict_to_append)

    # noinspection PyUnresolvedReferences
    @staticmethod
    def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
        """This method is also for debugging purpose only. It helps printing out questions which can not be printed out
            the normal way because of errors displaying unicode characters (Windows has some problems with it...)

        Args:
            *objects(object) : The kind of object, which will be used for printing
            sep(str) : The seperator to seperated the printed text
            end(str) : Defines whenever the printing should stop
            file(object) : Defines where to print that object to

        Returns:
            -

        """

        enc = file.encoding
        if enc == 'UTF-8':
            # noinspection PyArgumentList
            print(*objects, sep=sep, end=end, file=file)
        else:
            def f(x):
                str(x).encode(enc, errors='backslashreplace').decode(enc)

            print(*map(f, objects), sep=sep, end=end, file=file)

    @staticmethod
    def test_calculated_values():
        """This method is for debugging purpose only. It shows if all values have been calculated the correct way.

        Args:
            -

        Returns:
            -

        """

        print("Creation time stamp: " + str(thread_created_utc))
        print("Thread_Author: " + str(thread_author))
        print("Thread Title: " + str(thread_title))
        print("Thread_amount_questions: " + str(thread_amount_questions))
        print("Thread_amount_unanswered:" + str(thread_amount_unanswered_questions))
        print("thread_duration: " + str(thread_duration))
        print("thread_id: " + str(thread_id))
        print(str(thread_ups), str(thread_downs))
        print("thread_time_stamp_last_question: " + str(thread_time_stamp_last_question))
        print("thread_average_question_score: " + str(thread_average_question_score))
        print("thread_average_reaction_time_host: " + str(thread_average_reaction_time_host))
        print("thread_new_question_every_x_sec: " + str(thread_new_question_every_x_sec))
        print("thread_amount_questions_tier_1: " + str(thread_amount_questions_tier_1))
        print("thread_amount_questions_tier_x: " + str(thread_amount_questions_tier_x))
        print("thread_question_top_score: " + str(thread_question_top_score))
        print("Ausgabe Laenge un_answered questions: " + str(len(thread_unanswered_questions)))
        print("Ausgabe Laenge answered questions: " + str(len(thread_answered_questions)))
        print("------")
        print("Ausgabe antworten Laenge-Host: " + str(len(thread_answers_of_host)))
        print("------")

    @staticmethod
    def create_json_object():
        """Builds a JSON object consisting of all values which have been previously calculated

          Args:
              -

          Returns:
              -

          """

        global json_object_to_return

        data = {}

        returned_json_thread_overview = [{
            "thread_title": thread_title,
            "thread_amount_questions": thread_amount_questions,
            "thread_amount_answered_questions": thread_amount_questions - thread_amount_unanswered_questions,
            "thread_duration": int(thread_duration / 86400),
            "thread_id": thread_id
        }]

        returned_json_top_panel = [{
            "thread_ups": thread_ups,
            "thread_downs": thread_downs,
            "thread_duration": int(thread_duration / 86400),
            "thread_new_question_every_x_sec": int(thread_new_question_every_x_sec),
            "thread_amount_questioners": thread_amount_questioners,
            "thread_amount_unanswered_questions": thread_amount_unanswered_questions
        }]

        returned_json_statistics_panel = [{
            "thread_time_stamp_last_question": thread_time_stamp_last_question,
            "thread_average_question_score": "%.2f" % thread_average_question_score,
            "thread_average_reaction_time_host": "%.2f" % thread_average_reaction_time_host,
            "thread_new_question_every_x_sec": "%.2f" % thread_new_question_every_x_sec,
            "thread_amount_questions_tier_1": thread_amount_questions_tier_1,
            "thread_amount_questions_tier_x": thread_amount_questions_tier_x,
            "thread_question_top_score": thread_question_top_score,
            "thread_amount_questions": thread_amount_questions,
            "thread_amount_unanswered_questions": thread_amount_unanswered_questions,
        }]

        data["thread_overview"] = returned_json_thread_overview
        data["top_panel"] = returned_json_top_panel
        data["statistics_panel"] = returned_json_statistics_panel
        data["question_n_answers"] = thread_questions_n_answers
        data["open_questions"] = thread_unanswered_questions_converted

        # Dumps that data into JSON
        json_data = json.dumps(data)

        # Assign the json data to the generic object
        json_object_to_return = json_data
