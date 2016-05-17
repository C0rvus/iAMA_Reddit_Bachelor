import praw                      # Necessary to receive live data from reddit
import datetime                  # Necessary for calculating time differences
import time                      # Necessary to do some time calculations

from pymongo import MongoClient  # Necessary to make use of MongoDB

# Instanciates a reddit Instance
reddit_Instance = praw.Reddit(user_agent="University_Regensburg_iAMA_Crawler_0.001")  # main reddit functionality

reddit_submission = None


# Defines the year which will be used for correct database looking
database_year = 0

# Refers to the thread creation date
thread_created_utc = 0

# Left side panel information will be stored here
thread_title = ""                           #
thread_amount_questions = 0
thread_amount_unanswered_questions = 0
thread_duration = 0
thread_id = ""                              #

# Top panel
thread_ups = 0                              #
thread_downs = 0                            #

# Notification Panel
thread_time_stamp_last_question = 0
thread_average_question_Score = 0
thread_average_reaction_time_host = 0
thread_new_question_every_x_sec = 0
thread_amount_questions_tier_1 = 0
thread_amount_questions_tier_x = 0
thread_question_top_score = 0

# Middle of screen
thread_unanswered_questions = []
thread_answered_questions = []



# noinspection PyPep8Naming
class r_rest_Notification_Panel:

    def main_method(self):

        # Assigns the submission to a submission object
        self.get_thread_submission()

        # Assigns the thread created_utc data
        self.fill_misc_thread_data()

        # Assigns data to left and top panel
        self.fill_left_n_top_panel_data(self)

        # The value which is to be returned!
        return "At the moment I have no data for you!"



    @staticmethod
    def get_thread_submission():
        global reddit_submission

        print("<< in method get_thread_submission() >>")

        reddit_submission = reddit_Instance.get_submission(submission_id='4jlhq7')

    @staticmethod
    def fill_misc_thread_data():
        global thread_created_utc

        print("<< in method get_thread_submission() >>")

        thread_created_utc = reddit_submission.created_utc

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

    @staticmethod
    def init_DB():

        print("<< in method init_DB() >>")

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

        temp_time_now_converted_2 = datetime.datetime.fromtimestamp(
            temp_time_now_converted_1).strftime('%d-%m-%Y %H:%M:%S')

        time_diff = (temp_time_now_converted_2 - temp_creation_date_of_thread_converted_2).total_seconds()

        print("Time Difference: " + str(time_diff))

        ## Time difference muss ich separat berechnen !!!! in ner Sandbox !! #









