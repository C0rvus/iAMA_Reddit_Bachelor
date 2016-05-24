from flask import Flask
from r_rest_Notification_Panel import r_rest_Notification_Panel

app = Flask(__name__)
nPanel = r_rest_Notification_Panel()


@app.route('/refreshNotificationPanel/'
           '<string:un_filter_tier>_'
           '<string:un_filter_score_equals>_<string:un_filter_score_numeric>_'
           '<string:un_sorting_direction>_<string:un_sorting_type>__'
           '<string:an_filter_tier>_'
           '<string:an_filter_score_equals>_<string:an_filter_score_numeric>_'
           '<string:an_sorting_direction>_<string:an_sorting_type>')
# Refreshes the notification panel of the dashboard
def notification_panel(un_filter_tier, un_filter_score_equals, un_filter_score_numeric,
                       un_sorting_direction, un_sorting_type,

                       an_filter_tier, an_filter_score_equals, an_filter_score_numeric,
                       an_sorting_direction, an_sorting_type
                       ):

    return nPanel.main_method(un_filter_tier, un_filter_score_equals, un_filter_score_numeric,
                              un_sorting_direction, un_sorting_type,

                              an_filter_tier, an_filter_score_equals, an_filter_score_numeric,
                              an_sorting_direction, an_sorting_type)

# Necessary to run the script on the local host
if __name__ == '__main__':
    app.run(debug=True)
