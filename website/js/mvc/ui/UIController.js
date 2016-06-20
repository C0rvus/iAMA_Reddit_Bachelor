IAMA_Extension.UIController = function () {
    var that = {},

        body,
        topbar,
        thread_Overview,
        stats_Overview,
        unanswered_Questions,
        answered_Questions,

        //
        _giveStatsToStatsPanel = function (event, data) {
            $(body).trigger("stats_Data_To_DOM", data);
        },

        _giveTopBar = function (event, data) {
            $(body).trigger("top_Data_To_DOM", data);
        },

        _giveUnansweredQuestionsToUnansweredPanel = function (event, data) {

        },

        _giveAnsweredQuestionsToUnansweredPanel = function (event, data) {
            $(body).trigger("answered_Questions_To_DOM", data);
        },

        _giveThreadInformationToThreadPanel = function (event, data) {

        },

        // Triggers the clicked event to the MainController
        _onThreadClicked = function (event, data) {
            console.log("UIController - _onThreadClicked: " + data);
            $('body').trigger('thread_Selected', data);
        },

    // Initializes custom events the UI controllers listens to
        _initEvents = function () {

            console.log("UIcontroller: _initEvents");

            thread_Overview.on('thread_Clicked_To_Load', _onThreadClicked);

            body.on('Main_To_UI_Topbar', _giveTopBar);

            body.on('Main_To_UI_ThreadSingular', _giveThreadInformationToThreadPanel);

            body.on('Main_To_UI_Statistics_Panel', _giveStatsToStatsPanel);

            body.on('Main_To_UI_Unanswered_Questions', _giveUnansweredQuestionsToUnansweredPanel);

            body.on('Main_To_UI_Answered_Questions', _giveAnsweredQuestionsToUnansweredPanel);

        },

    // Initializes necessary modules
        _initModules = function () {
            console.log("UIcontroller: _initModules");

            topbar = IAMA_Extension.UITopBar.init();
            thread_Overview = IAMA_Extension.UIThreadOverview.init();
            stats_Overview = IAMA_Extension.UIStatsOverview.init();
            answered_Questions = IAMA_Extension.UIAnsweredQuestions.init();

        },

    // Initializes remaining variables
        _initOtherVars = function () {
            console.log("UIcontroller: _initOtherVars");

            body = $(document.body);

            topbar = $('#iAMA_Topbar');
            thread_Overview = $('#iAMA_Thread_Overview');
            stats_Overview = $('#iAMA_Stats');
            unanswered_Questions = $('#iAMA_Unanswered_Questions');
            answered_Questions = $('#iAMA_Answered_Questions');
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