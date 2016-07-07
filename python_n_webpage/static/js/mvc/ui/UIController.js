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
         * @param {[]} data contains following information about the statistics on the left side of the page:
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
        _giveStatsToStatsPanel = function (event, data) {
            $(body).trigger("stats_Data_To_DOM", data);
        },

        /**
         * Triggers data from MongoDBConnector to UITopBar - class (UI)
         *
         * @param {event} event kind of event which is to be triggered
         * @param {[]} data contains some stats data about the clicked thread
         *  thread_amount_questioners = {Integer}
         *  thread_amount_unanswered_questions = {Integer}
         *  thread_downs = {Integer}
         *  thread_duration = {Integer}
         *  thread_new_question_every_x_sec = {Integer}
         *  thread_ups = {Integer}
         */
        _giveMiniStatsToTopBar = function (event, data) {
            $(body).trigger("top_Data_To_DOM", data);
        },

        /**
         * Triggers data from MongoDBConnector to UIUnansweredQuestions - class (UI)
         *
         * @param {event} event kind of event which is to be triggered
         * @param {[]} dataArray contains information about questions which have to be answered by the iama host
         * Each question gets represented by an array containing following information:
         * question_author = "" {String} Information about the question author
         * question_id = "" {String}    The id of the question
         * question_text = "" {String}  The question text itself
         * question_timestamp = "" {String} The (already prepared) timestamp
         * question_upvote_score = {Integer} The amount of upvotes
         */
        _giveUnansweredQuestionsToUnansweredPanel = function (event, dataArray) {
            $(body).trigger("unanswered_Questions_To_DOM", [dataArray]);

        },

        /**
         * Triggers data from MongoDBConnector to UIAnsweredQuestions - class (UI)
         *
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
        _giveAnsweredQuestionsToAnsweredPanel = function (event, dataArray) {
            $(body).trigger("answered_Questions_To_DOM", [dataArray]);
        },

        /**
         * Triggers data from UI(Un)AnsweredQuestions to MongoDBConnector - class (REST)
         *
         * Whenever a refresh button on the (un)answered question panel gets clicked, this method will be triggered
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
        _refreshQuestionPanels = function (event, dataArray) {
            $(body).trigger("UI_To_Main_Refresh", [dataArray]);
        },

        /**
         * Triggers data from UIThreadOverview to MongoDBConnector - class (REST)
         *
         * Whenever a thread within the overview has been clicked this trigger gets fired up
         *
         * @param {event} event which fires this trigger
         * @param {[]} dataArray data which contains information about what kind of thread on the left side has been
         * selected
         *
         * 0 = "" {String} id of thread
         * [1] = Information about unanswered questions
         * [1] = Information about answered questions
         */
        _onThreadClicked = function (event, dataArray) {
            $(body).trigger('thread_Selected', [dataArray]);
        },

        /**
         * Triggers data from MongoDBConnector to UIThreadOverview - class (UI)
         *
         * Whenever the website gets loaded for the first time this method will be executed
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
        _giveInitialThreadInformationToThreadOverView = function (event, dataArray) {
            $('body').trigger('UI_To_Thread_Overview_Initial', [dataArray]);
        },

    // TODO: printing of thread data here --> weiter triggern

        /**
         * Triggers data from MongoDBConnector to UIThreadOverview - class (UI)
         *
         * Whenever the refresh button got clicked or a thread got loaded the panel data will be refreshed
         *
         * @param {event} event which fires that trigger
         * @param {[]} dataArray consists of following data for the selected thread:
         * [0]
         *      thread_amount_questions = "" {Integer}
         *      thread_amount_unanswered_questions = "" {Integer}
         *      thread_duration = "" {String}
         *      thread_id = "" {String}
         *      thread_title = "" {String}
         */
        _giveThreadInformationToThreadOverview = function (event, data) {
            console.log(data);
            $(body).trigger('UI_To_Thread_Overview', data);
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
            body.on('Main_To_UI_Thread_Overview', _giveThreadInformationToThreadOverview);

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