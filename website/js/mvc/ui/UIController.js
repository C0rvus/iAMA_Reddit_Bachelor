IAMA_Extension.UIController = function () {
    var that = {},

        body,
        topbar,
        thread_Overview,
        stats_Overview,
        unanswered_Questions,
        answered_Questions,
        ui_Generic_Methods,

        //
        _giveStatsToStatsPanel = function (event, data) {
            $(body).trigger("stats_Data_To_DOM", data);
        },

        _giveTopBar = function (event, data) {
            $(body).trigger("top_Data_To_DOM", data);
        },

        _giveUnansweredQuestionsToUnansweredPanel = function (event, dataArray) {
            $(body).trigger("unanswered_Questions_To_DOM", [dataArray]);

        },

        _giveAnsweredQuestionsToUnansweredPanel = function (event, dataArray) {
            $(body).trigger("answered_Questions_To_DOM", [dataArray]);
        },

        _giveThreadInformationToThreadPanel = function (event, data) {

        },

        // Whenever refresh within the unanswered question panel has been clicked
        _refreshQuestionPanels = function (event, dataArray) {
            $(body).trigger("UI_To_Main_Refresh", [dataArray]);
        },

        // Triggers the clicked event to the MainController
        _onThreadClicked = function (event, data) {
            $('body').trigger('thread_Selected', [data]);
        },

    // Initializes custom events the UI controllers listens to
        _initEvents = function () {


            thread_Overview.on('thread_Clicked_To_Load', _onThreadClicked);

            body.on('Main_To_UI_Topbar', _giveTopBar);

            body.on('Main_To_UI_ThreadSingular', _giveThreadInformationToThreadPanel);

            body.on('Main_To_UI_Statistics_Panel', _giveStatsToStatsPanel);

            body.on('Main_To_UI_Unanswered_Questions', _giveUnansweredQuestionsToUnansweredPanel);

            body.on('Main_To_UI_Answered_Questions', _giveAnsweredQuestionsToUnansweredPanel);

            body.on('Refresh_To_UI', _refreshQuestionPanels);

        },

    // Initializes necessary modules
        _initModules = function () {

            topbar = IAMA_Extension.UITopBar.init();
            thread_Overview = IAMA_Extension.UIThreadOverview.init();
            stats_Overview = IAMA_Extension.UIStatsOverview.init();
            answered_Questions = IAMA_Extension.UIAnsweredQuestions.init();
            unanswered_Questions = IAMA_Extension.UIUnansweredQuestions.init();
            ui_Generic_Methods = IAMA_Extension.UIGenericMethods.init();

        },

    // Initializes remaining variables
        _initVars = function () {

            body = $(document.body);

            topbar = $('#iAMA_Topbar');
            thread_Overview = $('#iAMA_Thread_Overview');
            stats_Overview = $('#iAMA_Stats');
            unanswered_Questions = $('#iAMA_Unanswered_Questions');
            answered_Questions = $('#iAMA_Answered_Questions');
        };

    // Initializes the UI Controller
    that.init = function () {

        _initVars();
        _initEvents();
        _initModules();

        return that;
    };
    return that;
}();