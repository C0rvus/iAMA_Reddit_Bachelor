/**
 *  @class MainController
 *  The MainController is necessary to
 *  - control trigger behaviour
 *  - guarantee overall working functionality
 */
IAMA_Extension.MainController = function () {

    var that = {},

        body,
        uiController = null,
        restController = null,

        /**
         * Triggers data from MainController to UIThreadOverview - class (UI)
         * @param {event} event kind of event which is to be triggered
         * @param {??} givenData data which is to be triggered
         */
        _onThreadOverviewToUIController = function(event, givenData) {
            $(body).trigger('Main_To_UI_Thread_Overview', givenData);
        },

        /**
         * Triggers data from MainController to UIStatsOverview - class (UI)
         * @param {event} event kind of event which is to be triggered
         * @param {??} givenData data which is to be triggered
         */
        _onStatisticsPanelToUIController = function(event, givenData) {
            $(body).trigger('Main_To_UI_Statistics_Panel', givenData);
        },

        /**
         * Triggers data from MainController to UITopBar - class (UI)
         * @param {event} event kind of event which is to be triggered
         * @param {??} givenData data which is to be triggered
         */
        _onTopPanelToUIController = function(event, givenData) {
            $(body).trigger('Main_To_UI_Topbar', givenData);
        },

        /**
         * Triggers data from MainController to UIAnsweredQuestions - class (UI)
         * @param {event} event kind of event which is to be triggered
         * @param {??} dataArray data which is to be triggered
         */
        _onAnsweredQuestionsToUIController = function(event, dataArray) {
            $(body).trigger('Main_To_UI_Answered_Questions', [dataArray]);
        },

        /**
         * Triggers data from MainController to UIUnansweredQuestions - class (UI)
         * @param {event} event kind of event which is to be triggered
         * @param {??} dataArray data which is to be triggered
         */
        _onUnansweredQuestionsToUIController = function(event, dataArray) {
            $(body).trigger('Main_To_UI_Unanswered_Questions', [dataArray]);
        },

        /**
         * Triggers data from MainController to UIThreadOverview - class (UI)
         *
         * This gets executed whenever the user clicked on a thread on the left side panel
         * Then the threads data will be received
         *
         * @param {event} event kind of event which is to be triggered
         * @param {??} givenData data which is to be triggered
         */
        _onThreadSelected = function (event, givenData) {
            $(body).trigger('rest_Thread_Selected', [givenData]);
        },

        /**
         * Triggers data from MainController to RestController - class (UI)
         *
         * Whenever a refresh button has been clicked this method gets triggerd, trying to retrieve
         * data from rest services
         *
         * @param {event} event kind of event which is to be triggered
         * @param {??} dataArray data which is to be triggered
         */
        _onRefreshToRest = function (event, dataArray) {
            $(body).trigger("Main_To_Rest_Refresh", [dataArray]);
        },

        /**
         * Triggers data from MainController to UIThreadOverview - class (UI)
         *
         * Whenever the page gets initially (!) loaded this trigger fires up.
         * This page will initially fire up, after logging on to reddit via OAUTH2
         *
         * @param {event} event kind of event which is to be triggered
         * @param {??} dataArray data which is to be triggered
         */
        _onThreadOverviewInitialToUIController = function (event, dataArray) {
            $(body).trigger("Main_To_UI_Thread_Initial_Load", [dataArray]);
        },

        /**
         * Initializes all "trigger" events the main controller should listen to
         */
        _initEvents = function () {

            // UIThreadOverview -> UIController -> MainController -> RestController -> MongoDBConnector
            body.on('thread_Selected', _onThreadSelected);

            // MongoDBConnector -> RestController -> MainController -> UIController -> UIThreadOverview
            body.on('Rest_To_Main_ThreadOverview', _onThreadOverviewToUIController);

            // MongoDBConnector -> RestController -> MainController -> UIController -> UIStatsOverview
            body.on('Rest_To_Main_StatisticsPanel', _onStatisticsPanelToUIController);

            // MongoDBConnector -> RestController -> MainController -> UIController -> UITopBar
            body.on('Rest_To_Main_TopPanel', _onTopPanelToUIController);

            // MongoDBConnector -> RestController -> MainController -> UIController -> UIAnsweredQuestions
            body.on('Rest_To_Main_AnsweredQuestions', _onAnsweredQuestionsToUIController);

            // MongoDBConnector -> RestController -> MainController -> UIController -> UIUnansweredQuestions
            body.on('Rest_To_Main_UnansweredQuestions', _onUnansweredQuestionsToUIController);

            // MongoDBConnector -> RestController -> MainController -> UIController -> UIThreadOverview
            body.on('Rest_To_Main_Thread_Overview_Initial', _onThreadOverviewInitialToUIController);

            // UI(Un)AnsweredQuestions -> UIController -> MainController -> RestController -> MongoDBConnector
            body.on('UI_To_Main_Refresh', _onRefreshToRest);

        },

        /**
         * Initializes all necessary controllers to work with.
         * uiController : necessary to operate with UI elements
         * restController : necessary to interact with local mongodb database
         */
        _initModules = function () {
            uiController = IAMA_Extension.UIController.init();
            restController = IAMA_Extension.RestController.init();
        },

        /**
         * Initializes necessary variables to work with.
         * Which is just the body document
         */
        _initVars = function () {
            body = $(document.body);
        };

    /**
     * Initializes the MainController itself
     *
     * @returns {object} MainController
     */
    that.init = function () {

        _initVars();
        _initEvents();
        _initModules();

        return that;
    };

    return that;
}();