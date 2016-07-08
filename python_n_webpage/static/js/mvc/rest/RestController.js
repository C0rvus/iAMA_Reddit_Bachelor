/**
 *  @class RestController
 *  The RestController is necessary to
 *  - access reddit live api
 *  - interact with locally installed mongo db
 */
IAMA_Extension.RestController = function () {
    var that = {},

        body,
        mongoDBConnector = null,

        /**
         * Triggers data from MongoDBConnector to UIThreadOverview - class (UI)
         * @param {event} event kind of event which is to be triggered
         * @param {[]} data contains data about all threads the author ever created
         */
        _giveThreadOverViewToMainController = function (event, data){
            $(body).trigger('Rest_To_Main_ThreadOverview', data);
        },

        /**
         * Triggers data from MongoDBConnector to UIStatsOverview - class (UI)
         * @param {event} event kind of event which is to be triggered
         * @param {[]} data contains information about the statistics on the left side of the page
         */
        _giveStatisticsPanelToMainController = function (event, data){
            $(body).trigger('Rest_To_Main_StatisticsPanel', data);
        },

        /**
         * Triggers data from MongoDBConnector to UITopBar - class (UI)
         * @param {event} event kind of event which is to be triggered
         * @param {[]} data contains some stats data about the clicked thread
         *  thread_amount_questioners = {Integer}
         *  thread_amount_unanswered_questions = {Integer}
         *  thread_downs = {Integer}
         *  thread_duration = {Integer}
         *  thread_new_question_every_x_sec = {Integer}
         *  thread_ups = {Integer}
         */
        _giveTopPanelToMainController = function (event, data){
            $(body).trigger('Rest_To_Main_TopPanel', data);
        },

        /**
         * Triggers data from MongoDBConnector to UIAnsweredQuestions - class (UI)
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
        _giveAnsweredQuestionsToMainController = function (event, dataArray){
            $(body).trigger('Rest_To_Main_AnsweredQuestions', [dataArray]);
        },

        /**
         * Triggers data from MongoDBConnector to UIUnansweredQuestions - class (UI)
         * @param {event} event kind of event which is to be triggered
         * @param {[]} dataArray contains information about questions which have to be answered by the iama host
         * Each question gets represented by an array containing following information:
         * question_author = "" {String} Information about the question author
         * question_id = "" {String}    The id of the question
         * question_text = "" {String}  The question text itself
         * question_timestamp = "" {String} The (already prepared) timestamp
         * question_upvote_score = {Integer} The amount of upvotes
         * @private
         */
        _giveUnansweredQuestionsToMainController= function (event, dataArray){
            $(body).trigger('Rest_To_Main_UnansweredQuestions', [dataArray]);
        },

        /**
         * Triggers data from UIThreadOverview to MongoDBConnector - class (REST)
         *
         * Initially retrieves data from within the database in combination with reddit live access
         *
         * @param {event} event kind of event which is to be triggered
         * @param {[]} dataArray data necessary for rest retrieval
         * [0] {String} threadid
         * [1] {Array}  Filter / Sorting settings for unanswered questions
         * [2] {Array}  Filter / Sorting settings for answered questions
         * @private
         */
        _getThreadDataFromDB = function (event, dataArray) {
            body.trigger('rest_Get_Data_From_DB', [dataArray]);
        },
        
        /**
         * Triggers data from UIUnansweredQuestions to MongoDBConnector - class (UI)
         *
         * Whenever the user pressed the "send" button, the answer text and the regarding question id, will be triggered
         * to the MongoDBConnector to post that on reddit.
         *
         * @param {event} event which fires that trigger
         * @param {[]} dataArray consists of following data for the answered question:
         * [0]  id_of_question {String}     The id of the question the answer text belongs to
         * [1]  answer_text {String}        The answer text itself
         * @private
         *
         */
        _givePostMessageToMongoDBConnector = function (event, dataArray){
            body.trigger('rest_Post_Message_To_Reddit', [dataArray]);
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
         * @private
         */
        _giveInitialThreadOverViewToMainController = function (event, dataArray) {
            body.trigger('Rest_To_Main_Thread_Overview_Initial', [dataArray]);
        },

        /**
         * Triggers data from MongoDBConnector to UIUnansweredQuestions - class (UI)
         *
         * Whenever the upload of a posted answer (by the iAMA host) was successful, this method gets executed.
         * It will refresh the (un)answered questions panel - by requesting new data from reddit.
         *
         * @param {event} event which fires that trigger
         * @param {String} data contains "SUCCESS"
         * @private
         */
        _givePostSuccessMessageToMainController = function (event, data){
            $(body).trigger('Rest_To_Main_Post_Sucess', data);
        },

        /**
         * Initializes all "trigger" events the rest controller should listen to
         * @private
         */
        _initEvents = function () {

            // UIThreadOverview -> UIController -> MainController -> RestController
            body.on('rest_Thread_Selected', _getThreadDataFromDB);

            // MongoDBConnector -> RestController -> MainController -> UIController -> UIThreadOverview
            body.on('rest_Thread_Overview_Array', _giveThreadOverViewToMainController);

            // MongoDBConnector -> RestController -> MainController -> UIController -> UIStatsOverview
            body.on('rest_Statistics_Panel_Array', _giveStatisticsPanelToMainController);

            // MongoDBConnector -> RestController -> MainController -> UIController -> UITopBar
            body.on('rest_Top_Panel_Array', _giveTopPanelToMainController);

            // MongoDBConnector -> RestController -> MainController -> UIController -> UIAnsweredQuestions
            body.on('rest_Answered_Questions_Array', _giveAnsweredQuestionsToMainController);

            // MongoDBConnector -> RestController -> MainController -> UIController -> UIUnansweredQuestions
            body.on('rest_Unanswered_Questions_Array', _giveUnansweredQuestionsToMainController);

            // UI(Un)AnsweredQuestions -> UIController -> MainController -> RestController -> MongoDBConnector
            body.on('Main_To_Rest_Refresh', _getThreadDataFromDB);

            // MongoDBConnector -> RestController -> MainController -> UIController -> UIThreadOverview
            body.on('rest_Initial_Thread_Overview_Array', _giveInitialThreadOverViewToMainController);

            // UIUnansweredQuestions -> UIController -> MainController -> RestController -> MongoDBConnector
            body.on('Main_To_Rest_Post_To_Reddit', _givePostMessageToMongoDBConnector);

            // MongoDBConnector -> RestController -> MainController -> UIController -> UIUnansweredQuestions
            body.on('Rest_To_Unanswered_Posting_Success', _givePostSuccessMessageToMainController);
        },

        /**
         * Initializes all necessary, underlying REST components to work with.
         * MongoDBConnector : necessary to interact with local mongodb database
         */
        _initModules = function () {
            mongoDBConnector = IAMA_Extension.MongoDBConnector.init();
        },

        /**
         * Initializes necessary variables to work with.
         * Which is just the body document
         * @private
         */
        _initVars = function () {
            body = $(document.body);
        };

    /**
     * Initializes this MainController itself
     *
     * @returns {object} RestController object
     * @public
     */
    that.init = function () {

        _initVars();
        _initEvents();
        _initModules();


        return that;
    };
    return that;
}();