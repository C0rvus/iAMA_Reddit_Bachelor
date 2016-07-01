from pymongo import MongoClient     # Necessary to make use of MongoDB
import praw                         # Necessary to access the reddit api
import datetime  # Necessary for calculating time differences
import time  # Necessary to do some time calculations
import json      # Necessary for creating json objects


# Instanciates the reddit instace for crawling behaviour
reddit_instance = praw.Reddit(user_agent="University_Regensburg_iAMA_Crawler_0.001")

mongo_db_client_instance = MongoClient('localhost', 27017)

mongo_db_author_fake_iama_instance = mongo_db_client_instance['fake_iAMA_Reddit_Authors']
mongo_db_author_fake_iama_collection_names = mongo_db_author_fake_iama_instance.collection_names()


# noinspection PyPep8Naming
class r_rest_Thread_Overview:

    @staticmethod
    def get_live_thread_data(thread_id, thread_author_name):

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

        def convert_epoch_to_time(time_as_string):
            time_to_days = int(int(time_as_string) / 60 / 60 / 24)
            time_to_hours = int(int(time_as_string) / 60 / 60)
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

        # Retrieves the submissions object live from reddit
        submission = reddit_instance.get_submission(submission_id=thread_id)

        # Necessary variables are defined here
        thread_title = submission.title
        thread_duration = calculate_time_difference(submission.created_utc, int(time.time()))
        # id_thread = submission.id

        amount_of_questions = 0
        amount_of_questions_answered = 0

        amount_of_questions_made = []
        reactions_of_thread_host = []

        # Getting all comments here -> necessary for live checking
        submission.replace_more_comments(limit=None, threshold=0)
        flat_comments = praw.helpers.flatten_tree(submission.comments)

        # Builds an imaginary dictionary containing all reactions
        for idx, val_2 in enumerate(flat_comments):

            comment_text = str(val_2.body)
            comment_author = str(val_2.author)

            # noinspection PyTypeChecker
            returned_json_data = dict({
                'id'       : str(val_2.name),
                'parent_id': str(val_2.parent_id),
            })

            if comment_author == thread_author_name:
                reactions_of_thread_host.append(returned_json_data)
            else:
                pass

            if "?" in comment_text and comment_author != thread_author_name:
                amount_of_questions_made.append(returned_json_data)
            else:
                pass

        # Iterates over all questions and counts the amount of the (un)answered ones
        for j, val_3 in enumerate(amount_of_questions_made):
            id_of_question_asked = val_3.get('id')

            amount_of_questions += 1

            for l, val_4 in enumerate(reactions_of_thread_host):
                parent_id_of_question_reacted_to = val_4.get('parent_id')

                # Whenever the question has been answered by the thread author
                if parent_id_of_question_reacted_to == id_of_question_asked:
                    amount_of_questions_answered += 1

        # Dict with necessary information for display in the left side panel
        dict_to_be_returned = dict({
            'title': thread_title,
            'amount_answered': amount_of_questions_answered,
            'amount_of_questions': amount_of_questions,
            'duration': convert_epoch_to_time(thread_duration),
            'thread_id': thread_id
        })

        return dict_to_be_returned

    def get_n_return_thread_data(self, author_name):

        author_cursor = list(mongo_db_author_fake_iama_instance [author_name].find())
        amount_of_threads = author_cursor [0].get("threads")

        threads_information_overview = []

        for i, val_1 in enumerate(amount_of_threads):
            thread_information = self.get_live_thread_data(val_1, author_name)

            threads_information_overview.append(thread_information)

        # Hier erstmal noch verjson....
        data = {"threads_information": threads_information_overview}

        json_data = json.dumps(data)

        return json_data
