# Sources used within this class:
# 1. (30.06.2016 @ 13:21) -
# https://praw.readthedocs.io/en/stable/
# 2. (03.07.2016 @ 12:21) -
# https://www.reddit.com/r/redditdev/comments/2t32fg/praw_getting_oauthscoperequired_error/


import praw             # Necessary to receive live data from reddit
import webbrowser       # Necessary to open up the OAUTH2 - reddit - webpage

# Instanciates the reddit instace for crawling / logon behaviour
r = praw.Reddit(user_agent="University_Regensburg_iAMA_Crawler_0.001")

# Sets the secret key for our reddit app here.. (not secret anymore now, I know...)
r.set_oauth_app_info(client_id='NIo65YvpxR_XFw',
                     client_secret='k8tXNifRHXqOebTBhEwuU-RNvbw',
                     redirect_uri='http://127.0.0.1:5000/authorize_callback')

# <editor-fold desc="Contains information necessary to be geathered from reddit">
# Defines the information to be gathered.. The most important ones are the scopes:
# ['identity']  : To be able to logon and get user information
# ['submit']    : To be able to post something on reddit later on
# </editor-fold>
url_auth = r.get_authorize_url('uniqueKey', ['identity', 'submit'], True)


# noinspection PyPep8Naming
class r_rest_Login_Behaviour:

    @staticmethod
    def go_to_login_page():
        """Whenever the REST - service gets initially started this method will be executed

            This method opens an authentification webpage, which will redirect to the route
            '/authorize_callback/' where the sign in key will be getting extracted and logon / posting behaviour
            will be received

        Args:
            -

        Returns:
            -

        """

        webbrowser.open(url_auth)

    @staticmethod
    def sign_in_with_returned_key(sign_key):
        """Logs on the user to reddit via using the transmitted sign_key.

            Additionally some user information gets extracted and the ability to post comments on reddit will be
            achieved in here

        Args:
            sign_key (str): The key which will be extracted from the authentification url callback

        Returns:
            dict_to_return (dict) : Contains the extracted username and the PRAW (r) object, which is going to be used
             within 'r_rest_Post_Behaviour' - class

            dict({
                'username': authenticated_user.name,
                'r_object': r
            })

        """

        # noinspection PyUnusedLocal
        # This statement needs to be set otherwise we can not operate with the users name
        access_information = r.get_access_information(sign_key)

        # noinspection PyUnusedLocal
        # Refreshes the access token to be valid for 60 minutes
        access_information.get('refresh_token')

        # Set logon credentials to be able to fully operate on reddit
        r.set_access_credentials(**access_information)

        # Extracts the user name out of the given sign key information
        authenticated_user = r.get_me()

        # noinspection PyTypeChecker
        dict_to_return = dict({
            'username': authenticated_user.name,
            'r_object': r
        })

        return dict_to_return
