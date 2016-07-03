import praw  # Necessary to receive live data from reddit

class r_rest_Post_Behaviour:

    @staticmethod
    def post_comment_on_reddit(r_object, iama_thread_id, id_to_reply_to, comment_text):

        print("-- inside post comment")
        print(r_object)
        print(iama_thread_id)
        print(id_to_reply_to)
        print(comment_text)
        print("-- inside post comment")

        r = r_object

        submission = r.get_submission(submission_id=iama_thread_id)
        submission.replace_more_comments(limit=None, threshold=0)
        flat_comments = praw.helpers.flatten_tree(submission.comments)

        # Iterates over all comments trying to find the related one
        for idx, val in enumerate(flat_comments):
            commment_id = val.name[3:]

            if commment_id == id_to_reply_to:
                val.reply(comment_text)
            else:
                pass
