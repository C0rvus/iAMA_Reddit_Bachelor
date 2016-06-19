# Sources used within this class:
# 1. (25.05.2016 @ 16:27) -
# http://www.adamburvill.com/2015/04/debugging-flask-app-with-pycharm.html

from flask import Flask
from flask.ext.cors import CORS

from r_rest_Calculate_Data import r_rest_Calculate_Data

app = Flask(__name__)
CORS(app)
nPanel = r_rest_Calculate_Data()


@app.route('/calculate_data/'
           '<string:thread_id>_'
           '<string:un_filter_tier>_'
           '<string:un_filter_score_equals>_<string:un_filter_score_numeric>_'
           '<string:un_sorting_direction>_<string:un_sorting_type>__'
           '<string:an_filter_tier>_'
           '<string:an_filter_score_equals>_<string:an_filter_score_numeric>_'
           '<string:an_sorting_direction>_<string:an_sorting_type>')
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

# Necessary to run the script on the local host
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
