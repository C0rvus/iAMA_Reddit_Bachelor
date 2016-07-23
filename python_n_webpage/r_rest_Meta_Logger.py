# Sources used within this class
# 1. (09.07.2016 @ 15:48) -
# https://stackoverflow.com/questions/10640804/how-to-add-lines-to-existing-file-using-python
# 2. (09.07.2016 @ 15:48) -
# http://www.cyberciti.biz/faq/howto-get-current-date-time-in-python/
# 3. (23.07.2016 @ 11:30) -
# https://wiki.python.org/moin/HandlingExceptions

import time             # Necessary to do some time calculation
import datetime         # Necessary to do some time calculation
import csv              # Necessary to do some csv operations
import os               # Necessary to get the correct path for the file
import pandas as pd     # Necessary for line checking

timestamp = None            # Timestamp to be written into the csv file
user = None                 # The user who is actually logged in
object_clicked_text = None  # The object which has been clicked
file_name_csv = None        # The path to the csv file which will contain the clicked information (meta data)


# noinspection PyPep8Naming
class r_rest_Meta_Logger:

    def write_data_into_file(self, given_user_name, given_usage_text):
        """The mechanism to create text files containing usage data is defined here

            Whenever the user clicks something on the webpage it will be written down into a text file.
            That text file will be analyzed by a seperate method, which is not yet defined here

            This class works as described below:

            1. It receives the submission object for the given thread_id at first.
            2. Now it crawls all comments from reddit, by breaking up the hierarchy
            3. It iterates over all comments. Whenever the iterated comments id matches the one the author replied to:
                Post the answer of the author to reddit.

        Args:
            self:   Self representation of the class [necessary to use methods within the class itself]
            given_user_name (str): The name of the author who has clicked something
            given_usage_text (str): The name of the behaviour he clicked / did

        Returns:
            -

        """

        self.set_global_variables(given_user_name, given_usage_text)
        self.logic_behaviour()

    @staticmethod
    def set_global_variables(username, text_of_object_clicked):
        """This method makes the given parameters globally available

            Because passing al those parameters into the single methods would mess up the code, I have decided
            to make them globally available to improve the readability of the code.

        Args:
            username:   The name of the author who has clicked something
            text_of_object_clicked (str): The text of the object which has been clicked
            text_of_question (str): The text of the question the user is actually processing

        Returns:
            -

        """

        global file_name_csv
        global timestamp
        global user
        global object_clicked_text
        global question_text

        time_variable = datetime.datetime.now()
        timestamp = "" + str(time_variable.day) +\
                        "." + str(time_variable.month) +\
                        "." + str(time_variable.year) +\
                        " @ " + time.strftime("%H:%M:%S")

        user = username
        object_clicked_text = text_of_object_clicked

        file_name_csv = str(os.path.basename(__file__))[0:len(os.path.basename(__file__)) - 3] + '_' + user + '.csv'

    def logic_behaviour(self):
        """Contains the logical behaviour of the class itself

            Depending of the existence of the file, a new text file will be created.
            Otherwise the given meta data ewill be appended to the already existing text file

        Args:
            self:   Self representation of the class [necessary to use methods within the class itself]

        Returns:
            -

        """

        # If the file, which is to be created, already exists, check for the first line
        if os.path.isfile(file_name_csv):

            # noinspection PyBroadException
            try:
                data_columns = pd.read_csv(file_name_csv, nrows=1).columns

                # Whenever the file has already been created and the columns are correct
                if ("Timestamp" and "User" and "What has been clicked") in data_columns:
                    self.append_meta_data_to_file()

                # Whenever the file has been created, but does not yet contain any line
                else:
                    self.initially_create_file()
                    self.append_meta_data_to_file()

            except:
                print("Csv (logging) data seems destroyed. Creating new one now...")
                self.initially_create_file()
                self.append_meta_data_to_file()

        # If the file has not been created at all
        else:
            self.initially_create_file()
            self.append_meta_data_to_file()

    # Creates the text file for the very first time
    @staticmethod
    def initially_create_file():
        """Initially creates the text file in here

            Whenever the text file does not exist this method will be executed

        Args:
            -

        Returns:
            -

        """

        # noinspection PyTypeChecker
        with open(file_name_csv, 'w', newline='') as fp:
            csv_writer = csv.writer(fp, delimiter=',')
            data = [['Timestamp',
                     'User',
                     'What has been clicked']]
            csv_writer.writerows(data)

    # Appends additional data to the given text file
    @staticmethod
    def append_meta_data_to_file():
        """Appends meta data to the already existing text file

            Whenever the text file aready exists this method will be executed and the globally stored data
            will be appended to it

        Args:
            -

        Returns:
            -

        """

        # noinspection PyTypeChecker
        with open(file_name_csv, 'a', newline='') as fp:
            csv_writer = csv.writer(fp, delimiter=',')
            data = [[timestamp, user, object_clicked_text]]
            csv_writer.writerows(data)
