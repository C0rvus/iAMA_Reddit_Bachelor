/**
 *  @class UIController
 *  The UIController is necessary to
 *  - give trigger data to specific UI elements
 *  - give trigger data from UI elements (requests) to mo the MongoDBConnector
 */
IAMA_Extension.UIController = function () {
    var that = {},

        body,
        topbar,
        thread_Overview,
        stats_Overview,
        unanswered_Questions,
        answered_Questions,
        ui_Generic_Methods,

        /**
         * Triggers data from MongoDBConnector to UIStatsOverview - class (UI)
         * @param {event} event kind of event which is to be triggered
         * @param {??} data data which is to be triggered
         */
        _giveStatsToStatsPanel = function (event, data) {
            $(body).trigger("stats_Data_To_DOM", data);
        },

        /**
         * Triggers data from MongoDBConnector to UITopBar - class (UI)
         *
         * @param {event} event kind of event which is to be triggered
         * @param {??} data data which is to be triggered
         */
        _giveMiniStatsToTopBar = function (event, data) {
            $(body).trigger("top_Data_To_DOM", data);
        },

        /**
         * Triggers data from MongoDBConnector to UIUnansweredQuestions - class (UI)
         *
         * @param {event} event kind of event which is to be triggered
         * @param {??} dataArray data which is to be triggered
         */
        _giveUnansweredQuestionsToUnansweredPanel = function (event, dataArray) {
            $(body).trigger("unanswered_Questions_To_DOM", [dataArray]);

        },

        /**
         * Triggers data from MongoDBConnector to UIAnsweredQuestions - class (UI)
         *
         * @param {event} event kind of event which is to be triggered
         * @param {??} dataArray data which is to be triggered
         */
        _giveAnsweredQuestionsToAnsweredPanel = function (event, dataArray) {
            $(body).trigger("answered_Questions_To_DOM", [dataArray]);
        },

        /**
         * Triggers data from UI(Un)AnsweredQuestions to MongoDBConnector - class (REST)
         *
         * Whenever a refresh button on the (un)answered question panel gets clicked, this method will be triggered
         *
         * @param {event} event kind of event which is to be triggered
         * @param {??} dataArray data which is to be triggered
         */
        _refreshQuestionPanels = function (event, dataArray) {
            $(body).trigger("UI_To_Main_Refresh", [dataArray]);
        },

        /**
         * Triggers data from UIThreadOverview to MongoDBConnector - class (REST)
         *
         * Whenever a thread within the overview has been clicked this trigger gets fired up
         *
         * @param {event} event kind of event which is to be triggered
         * @param {??} dataArray data which is to be triggered
         */
        _onThreadClicked = function (event, dataArray) {
            $('body').trigger('thread_Selected', [dataArray]);
        },

        /**
         * Triggers data from MongoDBConnector to UIThreadOverview - class (UI)
         *
         * Whenever the website gets loaded for the first time this method will be executed
         *
         * @param {event} event kind of event which is to be triggered
         * @param {??} dataArray data which is to be triggered
         */
        _giveInitialThreadInformationToThreadOverView = function (event, dataArray) {
            $('body').trigger('UI_To_Thread_Overview_Initial', [dataArray]);
        },

        /**
         * Initializes all "trigger" events the ui controller should listen to
         */
        _initEvents = function () {

            // UIThreadOverview -> UIController -> MainController -> RestController -> MongoDBConnector
            body.on('thread_Clicked_To_Load', _onThreadClicked);

            // MongoDBConnector -> RestController -> MainController -> UIController -> UITopBar
            body.on('Main_To_UI_Topbar', _giveMiniStatsToTopBar);

            // MongoDBConnector -> RestController -> MainController -> UIController -> UIStatsOverview
            body.on('Main_To_UI_Statistics_Panel', _giveStatsToStatsPanel);

            // MongoDBConnector -> RestController -> MainController -> UIController -> UIUnansweredQuestions
            body.on('Main_To_UI_Unanswered_Questions', _giveUnansweredQuestionsToUnansweredPanel);

            // MongoDBConnector -> RestController -> MainController -> UIController -> UIAnsweredQuestions
            body.on('Main_To_UI_Answered_Questions', _giveAnsweredQuestionsToAnsweredPanel);

            // MongoDBConnector -> RestController -> MainController -> UIController -> UIThreadOverview
            body.on('Main_To_UI_Thread_Initial_Load', _giveInitialThreadInformationToThreadOverView);

            // UI(Un)AnsweredQuestions -> UIController -> MainController -> RestController -> MongoDBConnector
            body.on('Refresh_To_UI', _refreshQuestionPanels);

        },

        /**
         * Initializes all ui elements to work with
         * topbar : necessary to give data to the top panel of the website
         * thread_Overview : necessary to give data to the thread overview of the website
         * stats_Overview : necessary to give statistics data to the statistics panel
         * answered_Questions : necessary to interact with the answered questions panel
         * unanswered_Questions : necessary to interact with the unanswered questions panel
         * ui_Generic_Methods : necessary to make use of specific ui scripts (i.E. Resizing behaviour, etc..)
         */
        _initModules = function () {

            topbar = IAMA_Extension.UITopBar.init();
            thread_Overview = IAMA_Extension.UIThreadOverview.init();
            stats_Overview = IAMA_Extension.UIStatsOverview.init();
            answered_Questions = IAMA_Extension.UIAnsweredQuestions.init();
            unanswered_Questions = IAMA_Extension.UIUnansweredQuestions.init();
            ui_Generic_Methods = IAMA_Extension.UIGenericMethods.init();

        },

        /**
         * Initializes necessary variables to work with.
         * Which is just the body document
         */
        _initVars = function () {
            body = $(document.body);
            // TODO: Die Teile hier rausschmeissen ??
        };

    /**
     * Initializes this UIController itself
     *
     * @returns {object} UIController
     */
    that.init = function () {

        _initVars();
        _initEvents();
        _initModules();

        return that;
    };
    return that;
}();