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
thread_questions_n_answers = []

# Object to return (JSON)
json_object_to_return = []


# noinspection PyPep8Naming
class r_rest_Calculate_Data:
    def main_method(self,

                    id_thread,

                    un_filter_tier, un_filter_score_equals, un_filter_score_numeric,
                    un_sorting_direction, un_sorting_type,

                    an_filter_tier, an_filter_score_equals, an_filter_score_numeric,
                    an_sorting_direction, an_sorting_type):

        """Defines the main method which will be called by listening on a certain REST-Interface

        Args:
            self:   Self representation of the class [necessary to use methods within the class itself]

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
            -
        """

        # Clears all variables to not return objects / questions twice
        self.clear_variables()

        # Assigns the reddit thread submission to an appropriate object
        self.get_thread_submission(str(id_thread))

        # Assigns the thread created_utc data
        self.fill_misc_thread_data()

        # <editor-fold desc="Initializes the database">
        # Initializes the database to get necessary information from
        # Necessary to first get the thread submission, otherwise we could not get the timestamp of the thread
        # That timestamp is necessary to look inside the correct database instance
        # </editor-fold>
        self.init_DB()

        # Assigns data to left and top panel
        self.fill_left_n_top_panel_data(self)

        # Assigns data to the right panel
        self.fill_right_panel_data(self)

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

        # # Creates the first chart data which is to be displayed via high charts
        # self.create_chart_1()
        #
        # # Creates the second chart data which is to be displayed via high charts
        # self.create_chart_2()
        #
        # # Creates the third chart data which is to be displayed via high charts
        # self.create_chart_3()

        # Simple test method for checking the correct assignment of the variables / values
        self.test_calculated_values()

        # Builds the JSON object for correct return
        self.create_json_object()

        # The value which is to be returned (JSON-Object)
        if json_object_to_return != "" or json_object_to_return is not None:
            return json_object_to_return
        else:
            return "At the moment I have no data for you!"

    @staticmethod
    def init_DB():
        """Initializes the database with all necessary instances

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

        # The year as formatted string (dd-mm-yy HH:MM:SS)
        # Converts the thread creation date into a comparable time format
        temp_creation_date_of_thread = float(thread_created_utc)

        temp_creation_date_of_thread_converted_1 = datetime.datetime.fromtimestamp(
            temp_creation_date_of_thread).strftime('%d-%m-%Y %H:%M:%S')

        # Gets the plain naked year here [i.e. 2015]
        thread_year = temp_creation_date_of_thread_converted_1[6:10]

        # Necessary value assignment to variables
        mongo_DB_Threads_Instance = mongo_DB_Client_Instance['iAMA_Reddit_Threads_' + str(thread_year)]
        mongo_DB_Thread_Collection = mongo_DB_Threads_Instance.collection_names()

        mongo_DB_Comments_Instance = mongo_DB_Client_Instance['iAMA_Reddit_Comments_' + str(thread_year)]
        mongo_DB_Comments_Collection = mongo_DB_Comments_Instance.collection_names()

    @staticmethod
    def get_thread_submission(id_of_thread):
        """Receives the thread information live from Reddit via the Reddit-API

        Args:
            -
        Returns:
            -
        """

        global reddit_submission

        reddit_submission = reddit_Instance.get_submission(submission_id=id_of_thread)

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
        # thread_duration = self.calculate_thread_duration_until_now()
        thread_duration = self.calculate_time_difference(thread_created_utc, int(time.time()))

    @staticmethod
    def fill_right_panel_data(self):
        """Calculates various statistics for the right panel of the page

        Args:
            self:   Self representation of the class [necessary to use methods within the class itself]
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

        comments_collection = mongo_DB_Comments_Instance[thread_id]
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
    def calculate_down_votes():
        """Calculates the amount of down votes of a thread

        Args:
            -
        Returns:
            object (int): The amount of time difference between two values in seconds
        """

        # Because down votes are not accessable via reddit API, we have calculated it by our own here
        ratio = reddit_Instance.get_submission(reddit_submission.permalink).upvote_ratio

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
        thread_average_question_score = np.mean(question_scores)
        thread_average_reaction_time_host = np.mean(question_host_reaction_time)
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

    # Checker methods below here for correct data calculation (right information panel of the webpage)
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
            willbe created in the beginning.
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

        # Iterates over every question
        for i, val in enumerate(questions_to_be_sorted):

            # Checks for the given REST parameter
            if filter_tier == "1":

                # Whenever the iterated question is not on tier 1
                if val["question_on_tier_1"] is False:

                    if filter_score_numeric != "" or filter_score_numeric is not None:

                        if filter_score_equals == "eql":
                            if val["question_upvote_score"] != int(filter_score_numeric):
                                indices_to_be_deleted.append(i)

                        elif filter_score_equals == "grt":
                            if val["question_upvote_score"] < int(filter_score_numeric):
                                indices_to_be_deleted.append(i)

                        elif filter_score_equals == "lrt":
                            if val["question_upvote_score"] > int(filter_score_numeric):
                                indices_to_be_deleted.append(i)

                        else:
                            # Continue as if nothing ever happened
                            pass
                    else:
                        indices_to_be_deleted.append(i)
                else:
                    pass

            # Checks for the given REST parameter
            elif filter_tier == "x":

                # Whenever the iterated question is on tier 1
                if val["question_on_tier_1"] is True:

                    # Whenever a numeric filtering score has been given via REST
                    if filter_score_numeric != "" or filter_score_numeric is not None:

                        if filter_score_equals == "eql":
                            if val["question_upvote_score"] != int(filter_score_numeric):
                                indices_to_be_deleted.append(i)

                        elif filter_score_equals == "grt":
                            if val["question_upvote_score"] < int(filter_score_numeric):
                                indices_to_be_deleted.append(i)

                        elif filter_score_equals == "lrt":
                            if val["question_upvote_score"] > int(filter_score_numeric):
                                indices_to_be_deleted.append(i)

                        else:
                            # Continue as if nothing ever happened
                            pass

                    # Whenever no filtering score has been given
                    else:
                        indices_to_be_deleted.append(i)
                else:
                    pass

            # Continue as if nothing ever happened
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

        # Shuffle all questions if selected from the page
        if str(sorting_type) == "random":

            np.random.shuffle(questions_to_be_sorted)

        # Otherwise do nothing here
        else:
            pass

    @staticmethod
    def build_list_containing_q_n_a(self):
        global thread_questions_n_answers

        # Iterates over every answered question and subiterates its answers
        for i, val_1 in enumerate(thread_answered_questions):

            # Will contain the question (1st place) and the answer to it (2nd place)
            temp_list_q_n_a = {
                "question_id": val_1.get("question_id"),
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
                    temp_list_q_n_a["answer_id"] = val_2.get('id_of_answer')
                    temp_list_q_n_a["answer_timestamp"] = self.convert_epoch_to_time\
                        (self.calculate_time_difference(val_2.get('created_utc'), int(time.time())))
                    temp_list_q_n_a["answer_upvote_score"] = val_2.get('ups')
                    temp_list_q_n_a["answer_text"] = val_2.get('answer_text')

                    # Append that q & a combination to the global list
                    thread_questions_n_answers.append(temp_list_q_n_a)

                else:
                    pass


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

        # Object which is to be returned (JSON)
        json_object_to_return = []

    @staticmethod
    def create_json_object():
        """Builds a JSON object consisting of all values which have been calculated

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
            "thread_amount_unanswered_questions": thread_amount_unanswered_questions,
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

        returned_json_questions = [{
            "unanswered_questions": thread_unanswered_questions,
            "answered_questions": thread_questions_n_answers
        }]

        data["thread_overview"] = returned_json_thread_overview
        data["top_panel"] = returned_json_top_panel
        data["statistics_panel"] = returned_json_statistics_panel
        # data["middle_screen"] = returned_json_questions
        data["question_n_answers"] = thread_questions_n_answers
        data["open_questions"] = thread_unanswered_questions

        # Dumps that data into JSON
        json_data = json.dumps(data)

        # Assign the json data to the generic object
        json_object_to_return = json_data
