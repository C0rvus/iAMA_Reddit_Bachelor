from flask import Flask
from r_rest_Notification_Panel import r_rest_Notification_Panel

app = Flask(__name__)
nPanel = r_rest_Notification_Panel()


@app.route('/refreshNotificationPanel')
# Refreshes the notification panel of the dashboard
def notification_panel():
    return nPanel.main_method()

# Necessary to run the script on the local host
if __name__ == '__main__':
    app.run(debug=True)
