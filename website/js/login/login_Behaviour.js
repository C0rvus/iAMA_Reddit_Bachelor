// Source: https://stackoverflow.com/a/5052661

function _onRetryGettingUsername() {

    (function worker() {
        console.log("Starting AJAX Call again!");
        $.ajax({
            type: "GET",
            url: "http://127.0.0.1:5000/get_username/",
            success: function(response) {
                console.log("Print out AJAX repeat username data : " + response);

                if (response === "Sorry, user has not logged yet") {
                    console.log("user has not logged on yet \n");
                    setTimeout(worker, 5000);

                } else {
                    console.log("User has finally logged on !!!");
                    // TODO: In index.html on load do trigger REST call here (go get data out of userbase)
                    // window.location.href = "http://localhost:63342/website/pages/index.html";
                }
            }
        });
    })();


}
var login_Behaviour = {

    login_button : null,

    _onLoginClick: function () {
        this.login_button.click(function () {
            console.log("!I HAVE BEEN CLICKED WOOWOWOWO");

            // Triggers a REST-CALL for OAUTH2
            $.ajax({
                type: "GET",
                url: "http://127.0.0.1:5000/login/",

                // Hier switcht er zu keiner site
                success: function() {
                    console.log("Login: Ich bin im Success drinnen -- woop woop");
                    // _onRetryGettingUsername();
                },

                error: function(){
                    alert("Could not load the logon page, I am very sorry! REST is down !!");
                }

            });

        })
    },

    _initUI: function () {
        console.log("Logon: init UI");
        this.login_button = $('#iAMA_Login_Button');
    },

    init: function () {
        console.log("Logon: I have been executed!!");
        this._initUI();
        this._onLoginClick();
    }
};