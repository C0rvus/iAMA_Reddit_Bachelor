# Sources used within this class:
# 1. (25.05.2016 @ 16:27) -
# http://www.adamburvill.com/2015/04/debugging-flask-app-with-pycharm.html
# 2. (29.06.2016 @ 13:56) -
# https://stackoverflow.com/a/11774434
# 3. (01.07.2016 @ 12:48) -
# https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask

import os                                       # Necessary to define paths for files to be returned via web
from flask import Flask, send_from_directory    # Necessary to be able to return requested files
from flask.ext.cors import CORS                 # Necessary to reduce "cross origin" errors during REST requests
from flask import request                       # Necessary to handle REST requests


from r_rest_Crawl_N_Calculate_Data import r_rest_Crawl_N_Calculate_Data     # Ability to crawl and calculate data
from r_rest_Thread_Overview import r_rest_Thread_Overview   # Ability to give back thread stats for better overview

from r_rest_Login_Behaviour import r_rest_Login_Behaviour   # Ability to handle the login behaviour
from r_rest_Post_Behaviour import r_rest_Post_Behaviour     # Ability to be able to post things on reddit


app = Flask(__name__, static_url_path='')       # Defines the flask service it self
CORS(app)                                       # Removes cross origin problems from within the app

cData = r_rest_Crawl_N_Calculate_Data()         # Crawls and calculates Data
tOverview = r_rest_Thread_Overview()            # Overview for thread information

iLogin = r_rest_Login_Behaviour()               # The login behaviour is handled here
pBehaviour = r_rest_Post_Behaviour()            # Ability to post things on reddit

username_actually_logged_in = ""                # The name, with which you have authorized yourself via OAuth2 on reddit
thread_actually_used = ""                       # The actually selected thread (necessary for calculation / retrieval)
r_object = None                                 # The PRAW (r)-object, which allows authorization and posting


# REST: Crawl author data and prepare Q&A
@app.route('/crawl_n_calculate/', methods=['GET'])
def crawl_n_calculate_data():
    """Generates the data which will be written into csv and plotted later on

        This route is active, whenever the user
        - clicked the refresh button on the (un)answered panel
        - initially selected a thread on the left side panel

        This route processes (sorting / filtering) settings for (un)answered questions panel

    Args:
        request.args.get('t_id')  : The id of the thread being processed
        request.args.get('u_f_t') : The selected tier - filter for unanswered questions (all / 1 / X)
        request.args.get('u_s_e') : The selected score comparison - filter for unanswered questions (eql / grt / lrt)
        request.args.get('u_s_n') : The selected score value used for filter for unanswered questions(any int)
        request.args.get('u_s_d') : The selected sorting direction for unanswered questions (asc / des)
        request.args.get('u_s_t') : The selected type to sort the data to (author / creation / score / random)

        request.args.get('a_f_t') : The selected tier - filter for answered questions (all / 1 / X)
        request.args.get('a_s_e') : The selected score comparison - filter for answered questions (eql / grt / lrt)
        request.args.get('a_s_n') : The selected score value used for filter for answered questions(any int)
        request.args.get('a_s_d') : The selected sorting direction for answered questions (asc / des)
        request.args.get('a_s_t') : The selected type to sort the data to (author / creation / score / random)

    Returns:
        1. thread_over_view_data (whenever if will be entered) (dict):

            'title': (str)                 [The written title of the thread]
            'amount_answered': (str)       [The amount of questions already answered]
            'amount_of_questions': (str)   [The overall amount of questions]
            'duration': (str)              [The duration of the thread (in hours / days) depending on internal calc]
            'thread_id': (str)             [The id of the thread]

        2. (un)answered question information sorted / filtered (dict):

            'extracted_an_filter_score_equals': (str)       [Answered q: The score comparison (eql / grt / lrt)]
            'extracted_an_filter_score_numeric': (str)      [Answered q: The score value (int)]
            'extracted_an_filter_tier': (str)               [Answered q: The tier - filter (all / 1 / Xx]
            'extracted_an_sorting_direction': (str)         [Answered q: The sorting direction (asc / des)]
            'extracted_an_sorting_type': (str)              [Answered q: The sorting type
                                                            (author / creation / score / random)]

            'extracted_thread_id': (str)                    [The ID of the processed thread]

            'extracted_un_filter_score_equals': (str)       [Unanswered q: The score comparison (eql / grt / lrt)]
            'extracted_un_filter_score_numeric': (str)      [Unanswered q: The score value (int)]
            'extracted_un_filter_tier': (str)               [Unanswered q: The tier - filter (all / 1 / Xx]
            'extracted_un_sorting_direction': (str)         [Unanswered q: The sorting direction (asc / des)]
            'extracted_un_sorting_type': (str)              [Unanswered q: The sorting type
                                                            (author / creation / score / random)]

    """

    global thread_actually_used

    extracted_thread_id = request.args.get('t_id')

    extracted_un_filter_tier = request.args.get('u_f_t')
    extracted_un_filter_score_equals = request.args.get('u_s_e')
    extracted_un_filter_score_numeric = request.args.get('u_s_n')
    extracted_un_sorting_direction = request.args.get('u_s_d')
    extracted_un_sorting_type = request.args.get('u_s_t')

    extracted_an_filter_tier = request.args.get('a_f_t')
    extracted_an_filter_score_equals = request.args.get('a_s_e')
    extracted_an_filter_score_numeric = request.args.get('a_s_n')
    extracted_an_sorting_direction = request.args.get('a_s_d')
    extracted_an_sorting_type = request.args.get('a_s_t')

    # Whenever the 'index.html' gets initially loaded
    if extracted_thread_id == "" \
            or extracted_thread_id is None \
            or extracted_thread_id == "None":

        # Simply crawl author information (threads n comments of them) into the appropriate databases
        cData.get_n_write_author_information(str(username_actually_logged_in))

        # Returns an overview of all author threads, with appropriate thread statistics
        return tOverview.get_n_return_thread_data(str(username_actually_logged_in))

    # Whenever the user clicked on a thread (left side panel) or he clicked one of the 'refresh' buttons on the
    # according (un)answered questions panel
    else:
        # Makes the id of the actually processed thread globally available (necessary for a working posting behaviour)
        thread_actually_used = extracted_thread_id

        # Returns (un) + answered questions the way the user wanted them to be sorted / filtered
        return cData.main_method(username_actually_logged_in,
                                                 extracted_thread_id,

                                                 extracted_un_filter_tier, extracted_un_filter_score_equals,
                                                 extracted_un_filter_score_numeric,
                                                 extracted_un_sorting_direction, extracted_un_sorting_type,

                                                 extracted_an_filter_tier, extracted_an_filter_score_equals,
                                                 extracted_an_filter_score_numeric, extracted_an_sorting_direction,
                                                 extracted_an_sorting_type)


# <editor-fold desc="Explanation of route inside here">
# This route is active, whenever the user clicks the "send" button within the unanswered questions panel
# It works the following way:
#
# 1. A REST-POST message, with the text inside its body to be uploaded to reddit will retreived
#   1.1. That post will be uploaded to reddit
#
# 2. The new information will be crawled from reddit and written into the database
#   Crawling it live from reddit instead of directly writing it into the database is more precise (i.E. in cases of utc)
# ----
# This route processes (sorting / filtering) settings for (un)answered questions panel
# </editor-fold>
@app.route('/post_to_reddit/', methods=['POST'])
def post_comment_to_reddit():

    # Extracts the text of the REST-POST body
    json_text = str(request.json['text'])

    # Extracts the id of the question the author replied to
    id_of_comment_replied_to = request.args.get('c_id')

    # 1. Post that comment onto reddit
    pBehaviour.post_comment_on_reddit(r_object, thread_actually_used, id_of_comment_replied_to, json_text)

    # 2. Recrawl all information from reddit
    cData.get_n_write_author_information(str(username_actually_logged_in))

    # Returns the following question ("success"). Which will trigger a "/crawl_n_calculate/" on JS side for correct
    # display of the newly posted message
    return "Processed your posting request"


# <editor-fold desc="Explanation of route inside here">
# Whenever the user is on the "authorize" Website and clicks "allow", he will be redirected to this route.
# The redirection to this route is defined within the reddits app setting
# </editor-fold>
@app.route('/authorize_callback/', methods=['GET'])
def use_signin_key():
    global username_actually_logged_in
    global r_object

    # Extracts the username sign in key from the url
    # This allows us to do posts etc on the page
    sign_key = request.args.get('code')

    # Whenever the user clicked the OAUTH2 - 'allow' button on the reddit page
    if sign_key is not None:

        dict_with_values = iLogin.sign_in_with_returned_key(sign_key)
        username_actually_logged_in = dict_with_values['username']
        r_object = dict_with_values['r_object']

        # Send the index.html file to the browser window
        return app.send_static_file('index.html')

    else:
        return "User not yet signed in"


# <editor-fold desc="Webserver: Returns font - files">
# This route returns font files the webpage requested
# </editor-fold>
@app.route('/authorize_callback/fonts/<path:font_file>', methods=['GET'])
def return_font_files(font_file):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'python_n_webpage/static/fonts'), font_file)


# <editor-fold desc="Webserver: Returns .js - files">
# This route returns .js files the webpage requested
# </editor-fold>
@app.route('/authorize_callback/js/<path:js_file>', methods=['GET'])
def return_js_files(js_file):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'python_n_webpage/static/js'), js_file)


# <editor-fold desc="Webserver: Returns .css - files">
# This route returns .css files the webpage requested
# </editor-fold>
@app.route('/authorize_callback/css/<path:css_file>', methods=['GET'])
def return_css_files(css_file):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'python_n_webpage/static/css'), css_file)


# <editor-fold desc="Webserver: Returns image - files">
# This route returns image files the webpage requested
# </editor-fold>
@app.route('/authorize_callback/img/<path:img_file>', methods=['GET'])
def return_img_files(img_file):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'python_n_webpage/static/img'), img_file)


# <editor-fold desc="Webserver: Returns image - files">
# This route returns image files the webpage requested.
# But this route here is a bug preventation, because the website requests an image from that path, even
# it is defined at no place, neither in html / js - code, to get image files from that location
# </editor-fold>
@app.route('/website/img/<path:img_file>', methods=['GET'])
def return_img_files_wrongly_directed(img_file):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'python_n_webpage/static/img'), img_file)


# Necessary to run the script on the local host
if __name__ == '__main__':
    # iLogin.go_to_login_page()
    app.run(host="0.0.0.0", debug=True)
