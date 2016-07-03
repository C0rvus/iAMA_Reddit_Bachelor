import praw  # Necessary to receive live data from reddit



# url_auth = r.get_authorize_url('uniqueKey', 'identity', True)


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

        # r = praw.Reddit(user_agent="University_Regensburg_iAMA_Crawler_0.001")
        #
        # r.set_oauth_app_info(client_id='NIo65YvpxR_XFw',
        #                      client_secret='k8tXNifRHXqOebTBhEwuU-RNvbw',
        #                      redirect_uri='http://127.0.0.1:5000/authorize_callback')

        # access_information = r.get_access_information(signin_key)
        # r.set_access_credentials(**access_information)
        # authenticated_user = r.get_me()

        # Allows us to fully operate on reddit
        # r.refresh_access_information(str(refresh_token))

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