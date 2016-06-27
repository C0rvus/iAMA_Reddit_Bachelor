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
        _getThreadDataFromDB = function (event, clickedThreadID) {
            body.trigger('rest_Get_Data_From_DB', clickedThreadID);

        },

        _getThreadDataFromDBWithFilteringNSorting = function (event, data) {
            console.log("Checking Array data here.. need to gather information for answered also");
            console.log([data]);
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

            body.on('Main_To_Rest_UnansweredQuestions_Refresh', _getThreadDataFromDBWithFilteringNSorting);

        },

    // Initializes necessary modules
        _initModules = function () {
            console.log("RestController: _initModules");
            mongoDBConnector = IAMA_Extension.MongoDBConnector.init();
        },

    // Initializes remaining variables
        _initVars = function () {
            console.log("RestController: _initVars");
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