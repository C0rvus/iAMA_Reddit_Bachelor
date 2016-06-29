# Sources used within this class:
# 1. (25.05.2016 @ 16:27) -
# http://www.adamburvill.com/2015/04/debugging-flask-app-with-pycharm.html
# 2. (29.06.2016 @ 13:56) -
# https://stackoverflow.com/a/11774434

from flask import Flask
from flask.ext.cors import CORS
from flask import request
import time

from r_rest_Calculate_Data import r_rest_Calculate_Data
from r_rest_Login_Behaviour import r_rest_Login_Behaviour


app = Flask(__name__)
CORS(app)
nPanel = r_rest_Calculate_Data()
iLogin = r_rest_Login_Behaviour()
username_to_return = None


@app.route('/calculate_data/'
           '<string:thread_id>_'
           '<string:un_filter_tier>_'
           '<string:un_filter_score_equals>_<string:un_filter_score_numeric>_'
           '<string:un_sorting_direction>_<string:un_sorting_type>__'
           '<string:an_filter_tier>_'
           '<string:an_filter_score_equals>_<string:an_filter_score_numeric>_'
           '<string:an_sorting_direction>_<string:an_sorting_type>',
           methods=['GET'])
# Refreshes the notification panel of the dashboard
def notification_panel(thread_id,

                       un_filter_tier, un_filter_score_equals, un_filter_score_numeric,
                       un_sorting_direction, un_sorting_type,

                       an_filter_tier, an_filter_score_equals, an_filter_score_numeric,
                       an_sorting_direction, an_sorting_type
                       ):

    return nPanel.main_method(thread_id,

                              un_filter_tier, un_filter_score_equals, un_filter_score_numeric,
                              un_sorting_direction, un_sorting_type,

                              an_filter_tier, an_filter_score_equals, an_filter_score_numeric,
                              an_sorting_direction, an_sorting_type)


# Whenever the user initially logs on
@app.route('/login/')
def login_behaviour_open_page():
    global username_to_return

    # Necessary to empty that username, otherwise user would automatically be redirected to index.html whenever he
    # refreshes login.html page
    username_to_return = None

    iLogin.go_to_login_page()

    # Return anything so no errors appear here
    # Returned value is only visible within console.log
    return "SEPP"


@app.route('/authorize_callback/')
def use_signin_key():
    global username_to_return

    sign_key = request.args.get('code')

    # Whenever the user clicked the OAUTH2 button on the reddit page
    if sign_key is not None:

        username_to_return = iLogin.sign_in_with_returned_key(sign_key)

        iLogin.start_iama_experience()

        return "User is signed in"
    else:
        return "User not yet signed in"


@app.route('/get_username/')
def get_user_name():

    # Whenever the user has already logged on
    if username_to_return is not None:

        # iLogin.start_iama_experience()

        return username_to_return

    # Whenever the username has not yet been retrieved (because user has not logged on yet)
    else:
        return "Sorry, user has not logged yet"


# Necessary to run the script on the local host
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
