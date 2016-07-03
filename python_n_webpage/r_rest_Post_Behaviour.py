# Sources used within this class:
# 1. (30.06.2016 @ 13:21) -
# https://praw.readthedocs.io/en/stable/

import praw             # Necessary to receive live data from reddit


# noinspection PyPep8Naming
class r_rest_Post_Behaviour:

    @staticmethod
    def post_comment_on_reddit(r_object, iama_thread_id, id_to_reply_to, comment_text):
        """The mechanism to reply to questions on reddit is defined here

            This class works as described below:

            1. It receives the submission object for the given thread_id at first.
            2. Now it crawls all comments from reddit, by breaking up the hierarchy
            3. It iterates over all comments. Whenever the iterated comments id matches the one the author replied to:
                Post the answer of the author to reddit.

        Args:
            r_object (PRAW.object): The prepared r-object, which is necessary to be able to post
            iama_thread_id (str): The thread the iAMA author is currently working on
            id_to_reply_to (str): The question id the author is replying to
            comment_text (str): The text the author has been posted

        Returns:
            -

        """

        # The PRAW (r) object. Which has been prepared within Login_Behaviour - class.
        # It is necessary to use it here, otherwise the user would not be able to post to reddit
        r = r_object

        # Retreives the thread as submission object
        submission = r.get_submission(submission_id=iama_thread_id)

        # Breaks comment hierarchy and flattens them
        submission.replace_more_comments(limit=None, threshold=0)
        flat_comments = praw.helpers.flatten_tree(submission.comments)

        # Iterates over all comments trying to find the related one
        for idx, val in enumerate(flat_comments):

            # Trunactes the comments id (removes 't1_') to match the comment format from the web site
            commment_id = val.name[3:]

            # Whenever the iterated comment's id matches the one the author replied to: post that answer to it
            if commment_id == id_to_reply_to:
                val.reply(comment_text)
            else:
                pass
