import praw  # Necessary to receive live data from reddit
import webbrowser

r = praw.Reddit(user_agent="University_Regensburg_iAMA_Crawler_0.001")

r.set_oauth_app_info(client_id='NIo65YvpxR_XFw',
                     client_secret='k8tXNifRHXqOebTBhEwuU-RNvbw',
                     redirect_uri='http://127.0.0.1:5000/authorize_callback')

# url_auth = r.get_authorize_url('uniqueKey', 'identity', True)
url_auth = r.get_authorize_url('uniqueKey', ['identity', 'submit'], True)


class r_rest_Login_Behaviour:

    @staticmethod
    def go_to_login_page():
        webbrowser.open(url_auth)

    @staticmethod
    def sign_in_with_returned_key(sign_key):

        # noinspection PyUnusedLocal
        # This statement needs to be set otherwise we can not operate with the users name
        access_information = r.get_access_information(sign_key)

        # Refreshes the access token to be valid for 60 minutes
        # noinspection PyUnusedLocal
        access_information.get('refresh_token')

        r.set_access_credentials(**access_information)
        authenticated_user = r.get_me()

        # noinspection PyTypeChecker
        dict_to_return = dict({
            'username': authenticated_user.name,
            'r_object': r
        })

        return dict_to_return
