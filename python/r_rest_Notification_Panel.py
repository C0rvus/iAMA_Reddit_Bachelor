import praw                      # Necessary to receive live data from reddit
import datetime                  # Necessary for calculating time differences
import time                      # Necessary to do some time calculations

from pymongo import MongoClient  # Necessary to make use of MongoDB

# Instanciates necessary database instances
mongo_DB_Client_Instance = MongoClient('localhost', 27017)

mongo_DB_Threads_Instance = None
mongo_DB_Thread_Collection = None

mongo_DB_Comments_Instance = None
mongo_DB_Comments_Collection = None

# Instanciates a reddit instance
reddit_Instance = praw.Reddit(user_agent="University_Regensburg_iAMA_Crawler_0.001")  # main reddit functionality
reddit_submission = None

# Refers to the thread creation date
thread_created_utc = 0                      # Live receive (Reddit API)
thread_author = ""                          # Live receive (Reddit API)

# Left side panel information will be stored here
thread_title = ""                           # Live receive (Reddit API)
thread_amount_questions = 0                 # MongoDB
thread_amount_unanswered_questions = 0      # MongoDB
thread_duration = 0                         # Live receive (Reddit API)
thread_id = ""                              # Live receive (Reddit API)

# Top panel
thread_ups = 0                              # Live receive (Reddit API)
thread_downs = 0                            # Live receive (Reddit API)

# Notification (Right) Panel
thread_time_stamp_last_question = 0         # MongoDB

thread_average_question_Score = 0
thread_average_reaction_time_host = 0
thread_new_question_every_x_sec = 0

thread_amount_questions_tier_1 = 0          # MongoDB
thread_amount_questions_tier_x = 0          # MongoDB
thread_question_top_score = 0               # MongoDB

# Middle of screen
thread_unanswered_questions = []            # MongoDB
thread_answered_questions = []              # MongoDB


# noinspection PyPep8Naming
class r_rest_Notification_Panel:

    def main_method(self):

        # Assigns the submission to a submission object
        self.get_thread_submission()

        # Assigns the thread created_utc data
        self.fill_misc_thread_data()

        # Initializes the database to get necessary information from
        # Necessary to first get the thread submission, otherwise we could not get the timestamp of the thread
        # That timestamp is necessary to look inside the correct database instance
        self.init_DB()

        # Assigns data to left and top panel
        self.fill_left_n_top_panel_data(self)

        # Assigns data to the right panel
        self.fill_right_panel_data(self)

        # The value which is to be returned!
        return "At the moment I have no data for you!"

    @staticmethod
    def init_DB():
        global mongo_DB_Client_Instance

        global mongo_DB_Threads_Instance
        global mongo_DB_Thread_Collection

        global mongo_DB_Comments_Instance
        global mongo_DB_Comments_Collection

        print("<< in method init_DB() >>")

        # The year as formatted string (dd-mm-yy HH:MM:SS)
        # Converts the thread creation date into a comparable time format
        temp_creation_date_of_thread = float(thread_created_utc)

        temp_creation_date_of_thread_converted_1 = datetime.datetime.fromtimestamp(
            temp_creation_date_of_thread).strftime('%d-%m-%Y %H:%M:%S')

        # Gets the plain naked year here
        thread_year = temp_creation_date_of_thread_converted_1[6:10]

        mongo_DB_Threads_Instance = mongo_DB_Client_Instance['iAMA_Reddit_Threads_' + str(thread_year)]
        mongo_DB_Thread_Collection = mongo_DB_Threads_Instance.collection_names()

        mongo_DB_Comments_Instance = mongo_DB_Client_Instance['iAMA_Reddit_Comments_' + str(thread_year)]
        mongo_DB_Comments_Collection = mongo_DB_Comments_Instance.collection_names()

    @staticmethod
    def get_thread_submission():
        global reddit_submission

        print("<< in method get_thread_submission() >>")

        reddit_submission = reddit_Instance.get_submission(submission_id='3zaf18')

    @staticmethod
    def fill_misc_thread_data():
        global thread_created_utc
        global thread_author

        print("<< in method get_thread_submission() >>")

        thread_created_utc = reddit_submission.created_utc
        thread_author = reddit_submission.author

    @staticmethod
    def fill_left_n_top_panel_data(self):
        global thread_title
        global thread_duration
        global thread_id
        global thread_ups
        global thread_downs

        print("<< in method fill_left_panel_data() >>")

        thread_title = reddit_submission.title
        thread_id = reddit_submission.id
        thread_ups = reddit_submission.ups

        # Calls external methods for calculation purpose
        thread_downs = self.calculate_down_votes()
        thread_duration = self.calculate_time_until_now()

        # Unanswered questions will be calculated by fill_righ_panel_data()

    @staticmethod
    def fill_right_panel_data(self):
        global thread_amount_questions
        global thread_amount_unanswered_questions
        global thread_time_stamp_last_question
        global thread_average_question_Score
        global thread_average_reaction_time_host
        global thread_new_question_every_x_sec
        global thread_amount_questions_tier_1
        global thread_amount_questions_tier_x
        global thread_question_top_score
        global thread_unanswered_questions
        global thread_answered_questions

        print("<< in method fill_right_panel_data() >>")

        comments_collection = mongo_DB_Comments_Instance[thread_id]
        comments_cursor = list(comments_collection.find())

        # Iterates over every comment within that thread
        for i, val in enumerate(comments_cursor):

            comment_text = val.get("body")
            comment_author = val.get("author")
            comment_parent_id = val.get("parent_id")
            comment_timestamp = val.get("created_utc")
            comment_id = val.get("name")
            comment_ups = val.get("ups")

            if comment_text is not None and comment_author is not None and comment_parent_id is not None:
                print("do something in here")

                bool_comment_is_question = self.checker_comment_is_question(comment_text)
                bool_comment_is_question_on_tier_1 = self.checker_comment_is_question_on_tier_1(comment_parent_id)
                bool_comment_is_not_from_thread_author = self.checker_is_not_from_thread_author(
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
                            thread_author, comment_id, comments_cursor
                        )

                    # Fills necessary data of the question here
                    dict_question = {
                        "question_id": comment_id,
                        "question_author": comment_author,
                        "question_timestamp": comment_timestamp,
                        "question_upvote_score": comment_ups,
                        "question_on_tier_1": bool_comment_is_question_on_tier_1,
                        "question_text": comment_text,
                        "question_answered_by_host":
                            comment_has_been_answered_by_thread_author["question_Answered_From_Host"]
                    }

                    # Whenever the answer to that comment is from the author
                    if comment_has_been_answered_by_thread_author["question_Answered_From_Host"] is True:

                        # Append it to the answered questions list
                        thread_answered_questions.append(dict_question)

                    elif comment_has_been_answered_by_thread_author["question_Answered_From_Host"] is False:

                        # Append it to the unanswered questions list
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
                if comment_timestamp > thread_time_stamp_last_question:
                    thread_time_stamp_last_question = comment_timestamp

            # Whenever a comment has been deleted or has, somehow, null values in it.. do not process it
            else:
                continue

    @staticmethod
    def calculate_down_votes():

        print("<< in method calculate_down_votes() >>")

        # Because down votes are not accessable via reddit API, we have calculated it by our own here
        ratio = reddit_Instance.get_submission(reddit_submission.permalink).upvote_ratio

        total_votes = int(round((ratio * reddit_submission.score) / (2 * ratio - 1))
                          if ratio != 0.5 else round(reddit_submission.score / 2))

        return total_votes - reddit_submission.score

    @staticmethod
    def calculate_time_until_now():
        global thread_duration

        print("<< in method calculate_time_until_now() >>")

        # Converts the thread creation date into a comparable time format
        temp_creation_date_of_thread = float(thread_created_utc)

        temp_creation_date_of_thread_converted_1 = datetime.datetime.fromtimestamp(
            temp_creation_date_of_thread).strftime('%d-%m-%Y %H:%M:%S')

        # Reformatation of time string
        temp_creation_date_of_thread_converted_2 = datetime.datetime.strptime(
            temp_creation_date_of_thread_converted_1, '%d-%m-%Y %H:%M:%S')

        # Converts the current time into a comparable time format
        time_now = int(time.time())

        temp_time_now = float(time_now)

        temp_time_now_converted_1 = datetime.datetime.fromtimestamp(
            temp_time_now).strftime('%d-%m-%Y %H:%M:%S')

        # Reformatation of time string
        temp_time_now_converted_2 = datetime.datetime.strptime(
            temp_time_now_converted_1, '%d-%m-%Y %H:%M:%S')

        # Contains the amount of time units (minutes)
        time_diff_minutes = (temp_time_now_converted_2 - temp_creation_date_of_thread_converted_2).total_seconds() / 60

        thread_duration = time_diff_minutes

    @staticmethod
    def calculate_question_stats():
        print("<< in method calculate_question_stats() >>")

        

    # Checker methods below here for correct data calculation (notification panel [right])
    @staticmethod
    def checker_comment_is_question(string_to_check):

        print("<< in method checker_comment_is_question() >>")

        if "?" in string_to_check:
            return True
        else:
            return False

    @staticmethod
    def checker_comment_is_question_on_tier_1(string_to_check):

        print("<< in method checker_comment_is_question_on_tier_1() >>")

        if "t3_" in string_to_check:
            return True
        else:
            return False

    @staticmethod
    def checker_is_not_from_thread_author(author_of_thread, comment_author):

        print("<< in method checker_is_not_from_thread_author() >>")

        if author_of_thread != comment_author:
            return True
        else:
            return False

    @staticmethod
    def check_if_comment_has_been_answered_by_thread_author(self, author_of_thread, comment_acutal_id, comments_cursor):

        print("<< in method check_if_comment_has_been_answered_by_thread_author() >>")

        dict_to_be_returned = {
            "question_Answered_From_Host": False,
            "time_Stamp_Answer": 0
        }

        # Iterates over every comment
        for i, val in enumerate(comments_cursor):

            check_comment_parent_id = val.get("parent_id")
            actual_comment_author = val.get("author")

            # Whenever the iterated comment is from the iAMA-Host and that comment has the question as parent_id
            if (self.check_if_comment_is_not_from_thread_author(author_of_thread, actual_comment_author) == False) \
                    and (check_comment_parent_id == comment_acutal_id):

                dict_to_be_returned["question_Answered_From_Host"] = True
                dict_to_be_returned["time_Stamp_Answer"] = val.get("created_utc")

                return dict_to_be_returned

        # This is the case whenever a comment has not a single thread or the comment / question has not been answered
        return dict_to_be_returned
