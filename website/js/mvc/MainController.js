IAMA_Extension.MainController = function () {

    var that = {},

        body,
        uiController = null,
        restController = null,

        _onThreadOverviewToUIController = function(event, givenData) {
            $(body).trigger('Main_To_UI_Thread_Overview', givenData);
        },

        _onStatisticsPanelToUIController = function(event, givenData) {
            $(body).trigger('Main_To_UI_Statistics_Panel', givenData);
        },

        _onTopPanelToUIController = function(event, givenData) {
            $(body).trigger('Main_To_UI_Topbar', givenData);
        },

        _onAnsweredQuestionsToUIController = function(event, givenData) {
            $(body).trigger('Main_To_UI_Answered_Questions', givenData);
        },

        _onUnansweredQuestionsToUIController = function(event, givenData) {
            $(body).trigger('Main_To_UI_Unanswered_Questions', givenData);
        },

        // Triggers the refresh functionality for unanswered questions to the rest controller
        _onThreadSelected = function (event, givenData) {
            $(body).trigger('rest_Thread_Selected', givenData);
        },

        // Triggers logout functionality for that website
        _onLogOut = function (event, givenData) {
            $(body).trigger('misc_Log_Out', givenData);
        },



    //Initializes custom events the MainControllers listenes to
        _initEvents = function () {
            // UIThreadOverview -> UIController -> MainController
            body.on('thread_Selected', _onThreadSelected);

            body.on('Rest_To_Main_ThreadOverview', _onThreadOverviewToUIController);
            body.on('Rest_To_Main_StatisticsPanel', _onStatisticsPanelToUIController);
            body.on('Rest_To_Main_TopPanel', _onTopPanelToUIController);
            body.on('Rest_To_Main_AnsweredQuestions', _onAnsweredQuestionsToUIController);
            body.on('Rest_To_Main_UnansweredQuestions', _onUnansweredQuestionsToUIController);

            body.on('log_Out', _onLogOut);

        },

    //Initializes necessary modules
        _initModules = function () {
            console.log("Maincontroller: _initModules");
            uiController = IAMA_Extension.UIController.init();
            restController = IAMA_Extension.RestController.init();
        },

    //Initializes remaining variables
        _initVars = function () {
            console.log("Maincontroller: _initVars");
            body = $(document.body);
        };

    // Initializes the MainController
    that.init = function () {

        _initVars();
        _initEvents();
        _initModules();

        body.trigger('pageLoaded');

        return that;
    };

    return that;
}();