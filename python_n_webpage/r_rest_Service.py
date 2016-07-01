# Sources used within this class:
# 1. (25.05.2016 @ 16:27) -
# http://www.adamburvill.com/2015/04/debugging-flask-app-with-pycharm.html
# 2. (29.06.2016 @ 13:56) -
# https://stackoverflow.com/a/11774434
# https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
import os
from flask import Flask, send_from_directory
from flask.ext.cors import CORS
from flask import request

from r_rest_Calculate_Data import r_rest_Calculate_Data
from r_rest_Login_Behaviour import r_rest_Login_Behaviour
from r_rest_Thread_Overview import r_rest_Thread_Overview

app = Flask(__name__, static_url_path='')
CORS(app)
cData = r_rest_Calculate_Data()
iLogin = r_rest_Login_Behaviour()
tOverview = r_rest_Thread_Overview()

# username_to_return = None
username_to_return = "uni_r_test_acc_1"


@app.route('/crawl_n_calculate/')
def crawl_n_calculate_data():
    extracted_author_name = request.args.get('an')
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

    # print("Given Username: " + str(extracted_author_name))
    # print("Given ThreadID: " + str(extracted_thread_id))
    # print("Given extracted_un_filter_tier: " + str(extracted_un_filter_tier))
    # print("Given extracted_un_filter_score_equals: " + str(extracted_un_filter_score_equals))
    # print("Given extracted_un_filter_score_numeric: " + str(extracted_un_filter_score_numeric))
    # print("Given extracted_un_sorting_direction: " + str(extracted_un_sorting_direction))
    # print("Given extracted_un_sorting_type: " + str(extracted_un_sorting_type))
    # print("Given extracted_an_filter_tier: " + str(extracted_an_filter_tier))
    # print("Given extracted_an_filter_score_equals: " + str(extracted_an_filter_score_equals))
    # print("Given extracted_an_filter_score_numeric: " + str(extracted_an_filter_score_numeric))
    # print("Given extracted_an_sorting_direction: " + str(extracted_an_sorting_direction))
    # print("Given extracted_an_sorting_type: " + str(extracted_an_sorting_type))

    # Whenever the index html gets initially loaded
    if extracted_thread_id == "" \
            or extracted_thread_id is None \
            or extracted_thread_id == "None":

        # Simply crawl author information (threads n comments of them) into the appropriate databases
        cData.get_n_write_author_information(str(username_to_return))

        return tOverview.get_n_return_thread_data(str(username_to_return))

    else:

        return cData.main_method(username_to_return,
                                                 extracted_thread_id,

                                                 extracted_un_filter_tier, extracted_un_filter_score_equals,
                                                 extracted_un_filter_score_numeric,
                                                 extracted_un_sorting_direction, extracted_un_sorting_type,

                                                 extracted_an_filter_tier, extracted_an_filter_score_equals,
                                                 extracted_an_filter_score_numeric, extracted_an_sorting_direction,
                                                 extracted_an_sorting_type)


# Route for reddit programming api callback
@app.route('/authorize_callback/')
def use_signin_key():
    global username_to_return

    # Extracts the username sign in key from the url
    # This allows us to do posts etc on the page
    sign_key = request.args.get('code')

    # Whenever the user clicked the OAUTH2 - 'allow' button on the reddit page
    if sign_key is not None:

        username_to_return = iLogin.sign_in_with_returned_key(sign_key)

        return app.send_static_file('index.html')

    else:
        return "User not yet signed in"


# Routes for flask behaving as web server
# Route for returning js files
@app.route('/authorize_callback/js/<path:js_file>')
def return_js_files(js_file):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'python_n_webpage/static/js'), js_file)


# Route for returning css files
@app.route('/authorize_callback/css/<path:css_file>')
def return_css_files(css_file):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'python_n_webpage/static/css'), css_file)


# Route for returning img files
@app.route('/authorize_callback/img/<path:img_file>')
def return_img_files(img_file):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'python_n_webpage/static/img'), img_file)


# Route for returning additional img files
# Route is necessary due to a unknown bug, where the page wants .png files from another directory
@app.route('/website/img/<path:img_file>')
def return_img_files_wrongly_directed(img_file):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'python_n_webpage/static/img'), img_file)


# Route for returning font files
@app.route('/authorize_callback/fonts/<path:font_file>')
def return_font_files(font_file):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'python_n_webpage/static/fonts'), font_file)


# Necessary to run the script on the local host
if __name__ == '__main__':
    # iLogin.go_to_login_page()
    app.run(host="0.0.0.0", debug=True)
# TODO: Set debugging to false, which starts the iama page just once
