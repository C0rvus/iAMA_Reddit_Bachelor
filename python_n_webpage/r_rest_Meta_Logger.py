# Sources used within this class
# 1. (09.07.2016 @ 15:48) -
# https://stackoverflow.com/questions/10640804/how-to-add-lines-to-existing-file-using-python
# 2. (09.07.2016 @ 15:48) -
# http://www.cyberciti.biz/faq/howto-get-current-date-time-in-python/

import time             # Necessary to do some time calculation
import datetime         # Necessary to do some time calculation


# noinspection PyPep8Naming
class r_rest_Meta_Logger:

    @staticmethod
    def write_data_into_file(user, usage_text):
        """The mechanism to create text files containing usage data is defined here

            Whenever the user clicks something on the webpage it will be written down into a text file.
            That text file will be analyzed by a seperate method, which is not yet defined here

            This class works as described below:

            1. It receives the submission object for the given thread_id at first.
            2. Now it crawls all comments from reddit, by breaking up the hierarchy
            3. It iterates over all comments. Whenever the iterated comments id matches the one the author replied to:
                Post the answer of the author to reddit.

        Args:
            user (str): The name of the author who has clicked something
            usage_text (str): The name of the behaviour he clicked / did

        Returns:
            -

        """

        time_variable = datetime.datetime.now()
        text_to_write = "" + str(time_variable.day) +\
                        "." + str(time_variable.month) +\
                        "." + str(time_variable.year) +\
                        " @ " + time.strftime("%H:%M:%S") +\
                        " ;;; " + user +\
                        " ;;; " + usage_text

        # open mode "a" means append lines
        file = open(user + ".txt", "a")
        file.write(text_to_write + "\n")
        file.close()
