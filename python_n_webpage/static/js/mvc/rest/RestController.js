IAMA_Extension.RestController = function () {
    var that = {},

        body,
        mongoDBConnector = null,

        _giveThreadOverViewToMainController = function (event, dataArray){
            $(body).trigger('Rest_To_Main_ThreadOverview', dataArray);
        },
        _giveStatisticsPanelToMainController = function (event, dataArray){
            $(body).trigger('Rest_To_Main_StatisticsPanel', dataArray);
        },
        _giveTopPanelToMainController = function (event, dataArray){
            $(body).trigger('Rest_To_Main_TopPanel', dataArray);
        },
        _giveAnsweredQuestionsToMainController = function (event, dataArray){
            $(body).trigger('Rest_To_Main_AnsweredQuestions', [dataArray]);
        },
        _giveUnansweredQuestionsToMainController= function (event, dataArray){
            $(body).trigger('Rest_To_Main_UnansweredQuestions', [dataArray]);
        },

        // Starts a REST call to receive that data from within the database
    //TODO : der Threadoverview muss überarbeitet werden, da jener nur nen String une ned String + Array + Array schickt

        _getThreadDataFromDB = function (event, data) {
            body.trigger('rest_Get_Data_From_DB', [data]);
        },

        _giveInitialThreadOverViewToMainController = function (event, data) {
            body.trigger('Rest_To_Main_Thread_Overview_Initial', [data]);
        },



    // Initializes custom events the UI controllers listens to
        _initEvents = function () {
            // UIThreadOverview -> UIController -> MainController -> RestController
            body.on('rest_Thread_Selected', _getThreadDataFromDB);

            // MongoDBConnector -> here
            body.on('rest_Thread_Overview_Array', _giveThreadOverViewToMainController);
            body.on('rest_Statistics_Panel_Array', _giveStatisticsPanelToMainController);
            body.on('rest_Top_Panel_Array', _giveTopPanelToMainController);
            body.on('rest_Answered_Questions_Array', _giveAnsweredQuestionsToMainController);
            body.on('rest_Unanswered_Questions_Array', _giveUnansweredQuestionsToMainController);

            // UI(Un)AnsweredQuestions -> UIController -> MainController -> RestController
            body.on('Main_To_Rest_Refresh', _getThreadDataFromDB);

            // MongoDBConnector -> RestController -> MainController -> UIController -> ThreadOverview
            body.on('rest_Initial_Thread_Overview_Array', _giveInitialThreadOverViewToMainController);



        },

    // Initializes necessary modules
        _initModules = function () {
            mongoDBConnector = IAMA_Extension.MongoDBConnector.init();
        },

    // Initializes remaining variables
        _initVars = function () {
            body = $(document.body);
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