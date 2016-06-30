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

# TODO: Set debugging to false, which starts the iama page just once

app = Flask(__name__, static_url_path='')
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
    iLogin.go_to_login_page()
    app.run(host="0.0.0.0", debug=True)

