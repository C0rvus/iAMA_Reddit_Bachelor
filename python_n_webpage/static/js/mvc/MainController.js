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
         * @param {[]} givenData contains data about all threads the author ever created
         */
        _onThreadOverviewToUIController = function(event, givenData) {
            $(body).trigger('Main_To_UI_Thread_Overview', givenData);
        },

        /**
         * Triggers data from MainController to UIStatsOverview - class (UI)
         * @param {event} event kind of event which is to be triggered
         * @param {[]} givenData contains following information about the statistics on the left side of the page:
         *
         * thread_amount_questions {Integer}
         * thread_amount_questions_tier_1 {Integer}
         * thread_amount_questions_tier_x {Integer}
         * thread_amount_unanswered_questions {Integer}
         * thread_average_question_score {String}
         * thread_average_reaction_time_host {String}
         * thread_new_question_every_x_sec {String}
         * thread_question_top_score {Integer}
         * thread_time_stamp_last_question {Integer}
         */
        _onStatisticsPanelToUIController = function(event, givenData) {
            $(body).trigger('Main_To_UI_Statistics_Panel', givenData);
        },

        /**
         * Triggers data from MainController to UITopBar - class (UI)
         * @param {event} event kind of event which is to be triggered
         * @param {[]} givenData contains some stats data about the clicked thread
         *  thread_amount_questioners = {Integer}
         *  thread_amount_unanswered_questions = {Integer}
         *  thread_downs = {Integer}
         *  thread_duration = {Integer}
         *  thread_new_question_every_x_sec = {Integer}
         *  thread_ups = {Integer}
         */
        _onTopPanelToUIController = function(event, givenData) {
            $(body).trigger('Main_To_UI_Topbar', givenData);
        },

        /**
         * Triggers data from MainController to UIAnsweredQuestions - class (UI)
         * @param {event} event kind of event which is to be triggered
         * @param {[]} dataArray contains arrays containg the following values:
         *
         * answer_id = "" {String}          The id of the answer
         * answer_text = "" {String}        The answer text itself
         * answer_timestamp = "" {String}   The timestamp of the given answer
         * answer_upvote_score = {Integer}  The score of the single answer
         * question_author = "" {String}    The name of the question author
         * question_id = "" {String}        The id of the question being asked
         * question_text = "" {String}      The text of the question being askex
         * question_timestamp = "" {String} The timestamp of the question
         * question_upvote_score = {Integer} The upvote score of the appropriate question
         */
        _onAnsweredQuestionsToUIController = function(event, dataArray) {
            $(body).trigger('Main_To_UI_Answered_Questions', [dataArray]);
        },

        /**
         * Triggers data from MainController to UIUnansweredQuestions - class (UI)
         * @param {event} event kind of event which is to be triggered
         * @param {[]} dataArray contains information about questions which have to be answered by the iama host
         * Each question gets represented by an array containing following information:
         * question_author = "" {String} Information about the question author
         * question_id = "" {String}    The id of the question
         * question_text = "" {String}  The question text itself
         * question_timestamp = "" {String} The (already prepared) timestamp
         * question_upvote_score = {Integer} The amount of upvotes
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
         * @param {event} event which fires this trigger
         * @param {[]} givenData data which contains information about what kind of thread on the left side has been
         * selected
         *
         * 0 = "" {String} id of thread
         * [1] = Information about unanswered questions
         * [1] = Information about answered questions
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
         * @param {[]} dataArray contains all filtering / sorting information for un & answered questions
         * [0] (unanswered questions) [1] {answered questions}, both containing the values below:
         * 0 = "" {String}  {Question filtering tier: all / 1 / x)
         * 1 = "" {String}  (Question filtering compare: eql / grt / lrt)
         * 2 = {Integer}    {Question score compare: any integer)
         * 3 = "" {String}  {Question sorting type /author / creation / score / random}
         * 4 = "" {String}  {Question sorting direction /asc / desc}
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
         * @param {event} event which fires that trigger
         * @param {[]} dataArray consists of following data:
         * [0]
         *      amount_answered = "" {Integer}
         *      amount_of_questions = "" {Integer}
         *      duration = "" {String}
         *      thread_id = "" {String}
         *      title = "" {String}
         * [1], etc... (depends on the amount of threads on the left side panel)
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