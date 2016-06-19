IAMA_Extension.UIController = function () {
    var that = {},

        $body,
        $navbar,
        thread_Overview,
        $stats_Overview,
        $unanswered_Questions,
        $answered_Questions,

        // Triggers the clicked event to the MainController
        _onThreadClicked = function (event, data) {
            console.log("UIController - _onThreadClicked: " + data);
            $('body').trigger('thread_Selected', data);
        },

    // Initializes custom events the UI controllers listens to
        _initEvents = function () {
            console.log("UIcontroller: _initEvents");

            $thread_Overview.on('thread_Clicked_To_Load', _onThreadClicked);

        },

    // Initializes necessary modules
        _initModules = function () {
            console.log("UIcontroller: _initModules");

            thread_Overview = IAMA_Extension.UIThreadOverview.init();

        },

    // Initializes remaining variables
        _initOtherVars = function () {
            console.log("UIcontroller: _initOtherVars");

            $body = $('body');
            $navbar = $('#iAMA_Navbar');
            $thread_Overview = $('#iAMA_Thread_Overview');
            $stats_Overview = $('#iAMA_Stats');
            $unanswered_Questions = $('#iAMA_Unanswered_Questions');
            $answered_Questions = $('#iAMA_Answered_Questions');
        };

    // Initializes the UI Controller
    that.init = function () {

        _initOtherVars();
        _initEvents();
        _initModules();


        return that;
    };
    return that;
}();