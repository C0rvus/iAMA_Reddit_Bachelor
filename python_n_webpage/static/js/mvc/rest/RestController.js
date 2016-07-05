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
         * @param {??} data data which is to be triggered
         */
        _giveThreadOverViewToMainController = function (event, data){
            $(body).trigger('Rest_To_Main_ThreadOverview', data);
        },

        /**
         * Triggers data from MongoDBConnector to UIStatsOverview - class (UI)
         * @param {event} event kind of event which is to be triggered
         * @param {??} data data which is to be triggered
         */
        _giveStatisticsPanelToMainController = function (event, data){
            $(body).trigger('Rest_To_Main_StatisticsPanel', data);
        },

        /**
         * Triggers data from MongoDBConnector to UITopBar - class (UI)
         * @param {event} event kind of event which is to be triggered
         * @param {??} data data which is to be triggered
         */
        _giveTopPanelToMainController = function (event, data){
            $(body).trigger('Rest_To_Main_TopPanel', data);
        },

        /**
         * Triggers data from MongoDBConnector to UIAnsweredQuestions - class (UI)
         * @param {event} event kind of event which is to be triggered
         * @param {??} dataArray data which is to be triggered
         */
        _giveAnsweredQuestionsToMainController = function (event, dataArray){
            $(body).trigger('Rest_To_Main_AnsweredQuestions', [dataArray]);
        },

        /**
         * Triggers data from MongoDBConnector to UIUnansweredQuestions - class (UI)
         * @param {event} event kind of event which is to be triggered
         * @param {??} dataArray data which is to be triggered
         */
        _giveUnansweredQuestionsToMainController= function (event, dataArray){
            $(body).trigger('Rest_To_Main_UnansweredQuestions', [dataArray]);
        },

    //TODO : der Threadoverview muss überarbeitet werden, da jener nur nen String une ned String + Array + Array schickt
        /**
         * Triggers data from UIThreadOverview to MongoDBConnector - class (REST)
         *
         * Initially retrieves data from within the database in combination with reddit live access
         *
         * @param {event} event kind of event which is to be triggered
         * @param {??} dataArray data which is to be triggered
         */
        _getThreadDataFromDB = function (event, dataArray) {
            body.trigger('rest_Get_Data_From_DB', [dataArray]);
        },
        
        /**
         * Triggers data from MongoDBConnector to UIThreadOverview - class (UI)
         *
         * Gives thread data which will be initially received from the database straight to the thread overview
         *
         * @param {event} event kind of event which is to be triggered
         * @param {??} dataArray data which is to be triggered
         */
        _giveInitialThreadOverViewToMainController = function (event, dataArray) {
            body.trigger('Rest_To_Main_Thread_Overview_Initial', [dataArray]);
        },

        /**
         * Initializes all "trigger" events the rest controller should listen to
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
         */
        _initVars = function () {
            body = $(document.body);
        };

    /**
     * Initializes this MainController itself
     *
     * @returns {object} RestController object
     */
    that.init = function () {

        _initVars();
        _initEvents();
        _initModules();


        return that;
    };
    return that;
}();