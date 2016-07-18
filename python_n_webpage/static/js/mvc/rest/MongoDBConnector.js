/**
 *  @class MongoDBConnector
 *  The MongoDBConnector triggers appropriate REST-Calls to to the REST-Service.
 *  Those REST calls contain various information about the style the questions have to be sorted and filtered
 *  -
 *  Sources used within this class:
 *  1.(11.06.2016 @ 10:15) - https://stackoverflow.com/a/5225641
 *  2.(13.06.2016 @ 11:01) - https://xuad.net/artikel/vom-einfachen-ajax-request-zum-komplexen-objektaustausch-mit-json-mittels-jquery/
 */
IAMA_Extension.MongoDBConnector = function () {
    var that = {},
        body,

        /**
         *  This breaks MVC in a little way, because this class here directly accesses an open modal window and forces
         *  it to close.. to avoid unnecessary triggering I just simply hardcoded this in here
         */
        _closeBootStrapDialog = function () {
            BootstrapDialog.closeAll()
        },

        /**
         * Whenever the initial REST call to retrieve the thread information data was successful, then that data
         * will be triggered to the thread overview
         **
         * @param {[]} content contains all stats & q&a for the selected thread.. It is structured as following:
         *
         * [thread_overview]
         *  "thread_title":
         *  "thread_id":
         *  "thread_duration":
         *  "thread_amount_unanswered_questions":
         *  "thread_amount_questions":
         *
         * [top_panel]
         *  "thread_amount_questioners":
         *  "thread_ups":
         *  "thread_new_question_every_x_sec":
         *  "thread_downs":
         *  "thread_duration":
         *  "thread_amount_unanswered_questions":
         *
         * [open_questions]
         * {
                  * "question_id":
                  * "question_timestamp":
                  * "question_text":
                  * "question_author":
                  * "question_upvote_score":
         }, etc.

         * [question_n_answers]
         *  "question_id":
         *  "question_author":
         *  "question_timestamp":
         *  "question_upvote_score":
         *  "question_text":
         *  "answer_id":
         *  "answer_timestamp":
         *  "answer_upvote_score":
         *  "answer_text":

         * [statistics_panel]
         *  "thread_amount_unanswered_questions"
         *  "thread_average_question_score"
         *  "thread_new_question_every_x_sec"
         *  "thread_amount_questions_tier_1"
         *  "thread_amount_questions"
         *  "thread_amount_questions_tier_x"
         *  "thread_question_top_score"
         *  "thread_time_stamp_last_question"
         *  "thread_average_reaction_time_host"
         *
         * @private
         */
        _onSuccessInitialCall = function (content) {
            // Closes all open BootStrapDialog dialoges
            _closeBootStrapDialog();
            $(body).trigger('rest_Initial_Thread_Overview_Array', [content]);
        },

        /**
         * Whenever the retrieval of thread data from the mongodb was successful that whole data package will be split
         * up and each part will be triggered individually to the single UI components
         *
         * @param {[]} content contains all stats & q&a for the selected thread.. It is structured as following:
         *
         * [thread_overview]
         *  "thread_title":
         *  "thread_id":
         *  "thread_duration":
         *  "thread_amount_unanswered_questions":
         *  "thread_amount_questions":
         *
         * [top_panel]
         *  "thread_amount_questioners":
         *  "thread_ups":
         *  "thread_new_question_every_x_sec":
         *  "thread_downs":
         *  "thread_duration":
         *  "thread_amount_unanswered_questions":
         *
         * [open_questions]
         * {
                  * "question_id":
                  * "question_timestamp":
                  * "question_text":
                  * "question_author":
                  * "question_upvote_score":
         }, etc.

         * [question_n_answers]
         *  "question_id":
         *  "question_author":
         *  "question_timestamp":
         *  "question_upvote_score":
         *  "question_text":
         *  "answer_id":
         *  "answer_timestamp":
         *  "answer_upvote_score":
         *  "answer_text":

         * [statistics_panel]
         *  "thread_amount_unanswered_questions"
         *  "thread_average_question_score"
         *  "thread_new_question_every_x_sec"
         *  "thread_amount_questions_tier_1"
         *  "thread_amount_questions"
         *  "thread_amount_questions_tier_x"
         *  "thread_question_top_score"
         *  "thread_time_stamp_last_question"
         *  "thread_average_reaction_time_host"
         *
         * @private
         */
        _onSuccess = function (content) {
            // Parses the JSON response into an java script accessable object
            var response = $.parseJSON(content);

            // Whenever the response received is valid
            if (!response.result) {
                var thread_overview = response['thread_overview'][0];
                var statistics_panel = response['statistics_panel'][0];
                var top_panel = response['top_panel'][0];
                var answered_questions = response['question_n_answers'];
                var unanswered_questions = response['open_questions'];

                $(body).trigger('rest_Thread_Overview_Array', thread_overview);
                $(body).trigger('rest_Statistics_Panel_Array', statistics_panel);
                $(body).trigger('rest_Top_Panel_Array', top_panel);
                $(body).trigger('rest_Answered_Questions_Array', [answered_questions]);
                $(body).trigger('rest_Unanswered_Questions_Array', [unanswered_questions]);

            } else {
                BootstrapDialog.closeAll();
                alert("Error receiving JSON! Please fix python data conversion for REST");
            }
        },

        /**
         * Whenever a thread has been selected on the left side of the webpage a REST call containing necessary
         * will be triggered
         *
         * @param {event} event kind of event which is to be triggered
         * @param {??} data gets data from within the database, consisting of
         * [0] {String} threadID
         * [1] {Array} Array containing filtering / sortings settings for answered questions
         * [2] {Array} Array containing filtering / sortings settings for unanswered questions
         *
         * @private
         */
        _getThreadDataFromDB = function (event, data) {
            var threadID = data[0],
                unanswered_Questions_Settings_Array = data[1],
                answered_Questions_Settings_Array = data[2],

                unanswered_Filter_Settings_Tier = null,
                unanswered_Filter_Settings_Score_Compare = null,
                unanswered_Filter_Settings_Score_Value = null,
                unanswered_Sorting_Settings_Type = null,
                unanswered_Sorting_Settings_Asc_Des = null,

                answered_Filter_Settings_Tier = null,
                answered_Filter_Settings_Score_Compare = null,
                answered_Filter_Settings_Score_Value = null,
                answered_Sorting_Settings_Type = null,
                answered_Sorting_Settings_Asc_Des = null;

            // Whenever the unanswered_Questions_Settings_Array is null
            // That means, whenever a thread has been initially clicked
            if (data[1][0] === null) {
                unanswered_Filter_Settings_Tier = "all";
                unanswered_Filter_Settings_Score_Compare = "grt";
                unanswered_Filter_Settings_Score_Value = -99999;
                unanswered_Sorting_Settings_Asc_Des = "asc";
                unanswered_Sorting_Settings_Type = "random";

                answered_Filter_Settings_Tier = "all";
                answered_Filter_Settings_Score_Compare = "grt";
                answered_Filter_Settings_Score_Value = -99999;
                answered_Sorting_Settings_Asc_Des = "asc";
                answered_Sorting_Settings_Type = "random";

                // Whenever the refresh button of the (un)answered questions panel has been clicked
            } else {
                unanswered_Filter_Settings_Tier = unanswered_Questions_Settings_Array[0][0];
                unanswered_Filter_Settings_Score_Compare = unanswered_Questions_Settings_Array[0][1];
                unanswered_Filter_Settings_Score_Value = unanswered_Questions_Settings_Array[0][2];
                unanswered_Sorting_Settings_Type = unanswered_Questions_Settings_Array[0][3];
                unanswered_Sorting_Settings_Asc_Des = unanswered_Questions_Settings_Array[0][4];


                answered_Filter_Settings_Tier = answered_Questions_Settings_Array[0][0];
                answered_Filter_Settings_Score_Compare = answered_Questions_Settings_Array[0][1];
                answered_Filter_Settings_Score_Value = answered_Questions_Settings_Array[0][2];
                answered_Sorting_Settings_Type = answered_Questions_Settings_Array[0][3];
                answered_Sorting_Settings_Asc_Des = answered_Questions_Settings_Array[0][4];

            }

            // The ajax call which gets information through REST from the reddit API and the mongoDB
            $.ajax({
                type: "GET",
                url: "http://127.0.0.1:5000/crawl_n_calculate/" +

                "?an=None" +
                "&t_id=" + threadID +

                "&u_f_t=" + unanswered_Filter_Settings_Tier +
                "&u_s_e=" + unanswered_Filter_Settings_Score_Compare +
                "&u_s_n=" + unanswered_Filter_Settings_Score_Value +
                "&u_s_d=" + unanswered_Sorting_Settings_Asc_Des +
                "&u_s_t=" + unanswered_Sorting_Settings_Type +

                "&a_f_t=" + answered_Filter_Settings_Tier +
                "&a_s_e=" + answered_Filter_Settings_Score_Compare +
                "&a_s_n=" + answered_Filter_Settings_Score_Value +
                "&a_s_d=" + answered_Sorting_Settings_Asc_Des +
                "&a_s_t=" + answered_Sorting_Settings_Type,

                success: _onSuccess,
                error: function () {
                    alert("Thread not found in database.. Please check ID of thread and DB consistency!");
                },
                timeout: 35000 // Throws an error after 25 seconds of inactivity
            });


        },

        /**
         * Whenever the user clicked the "send" button, when he answered a question
         *
         *
         * @param {event} event which fires that trigger
         * @param {[]} dataArray consists of following data for the answered question:
         * [0]  id_of_question {String}     The id of the question the answer text belongs to
         * [1]  answer_text {String}        The answer text itself
         * @private
         */
        _submitDataToReddit = function (event, dataArray) {

            var id_Of_Question = [dataArray][0][0][0],
                text_To_Send = [dataArray][0][1][0];

            $.ajax({
                type: "POST",
                url: "http://127.0.0.1:5000/post_to_reddit/?c_id=" + id_Of_Question,
                processData: false,
                contentType: 'application/json',
                data: text_To_Send, // this text data is already json - stringified
                success: function () {
                    // Triggers a success message to the unanswered questions panel
                    // Which will result in refreshing the data there
                    $(body).trigger('Rest_To_Unanswered_Posting_Success', "SUCCESS");
                },
                error: function () {
                    // Close that previously opened BootStrapDialog dialog
                    _closeBootStrapDialog();

                    //noinspection JSCheckFunctionSignatures
                    BootstrapDialog.show({
                        title: 'Fatal error! Post could not be submitted!',
                        message: 'Your answer could not be submitted to reddit. Please check online connectivity',
                        type: BootstrapDialog.TYPE_WARNING,
                        closable: true
                    });
                }
            });
            
        },
        
        /**
         * Writes data, which is triggered from any UI class to here down into a text file
         *
         * Whenever the user clicked on any UI event within the page it will be trigered to the MongoDBConnector
         * which will write that information into a text file which is to be analyzed later on.
         *
         * @param {event} event which fires that trigger
         * @param {String} data contains Information about the clicked UI element
         * @private
         */
        _writeMetaDataFile = function (event, data) {

            $.ajax({
                type: "POST",
                url: "http://127.0.0.1:5000/write_meta_data/",
                processData: false,
                contentType: 'application/json',
                data: data // this text data is already json - stringified
                // success: function () {
                //     console.log("SUCCESS meta data");
                // },
                // error: function () {
                //     console.log("FAILURE in meta data");
                // }
            });



        },

        /**
         * Initializes necessary variables to work with.
         * Which is just the body document
         * @private
         */
        _initVars = function () {
            body = $(document.body);
        },

        /**
         * Initializes all "trigger" events the MongoDBConnector should listen to
         * @private
         */
        _initEvents = function () {

            // UIThreadOverview -> UIController -> MainController -> RestController
            body.on('rest_Get_Data_From_DB', _getThreadDataFromDB);

            // UIUnansweredQuestions -> UIController -> MainController -> RestController -> MongoDBConnector
            body.on('rest_Post_Message_To_Reddit', _submitDataToReddit);

            // AnyUIClass -> UIController -> MainController -> RestController -> MongoDBConnector
            body.on('rest_Write_MetaData_Into_TextFile', _writeMetaDataFile);
        },

        /**
         * Does THE initial REST-Call to start the iAMA experience and retrieves data from mongoDB and reddit live
         * @private
         */
        _initialRestCall = function () {

            // I know this is bad style here, but before triggering around like hell just get this straight and
            // display an UI element here
            //noinspection JSCheckFunctionSignatures
            BootstrapDialog.show({
                title: 'Fetching data from Reddit and the local data base',
                message: 'Please wait a few seconds until the requested data arrives...',
                type: BootstrapDialog.TYPE_WARNING,
                closable: false
            });

            $.ajax({
                type: "GET",

                // dataType 'json' is necessary here, otherwise arrays wouldn't get loaded
                dataType: "json",

                /**
                 * Because there is no explicit method within the REST-Service to only calculate data explicitly for
                 * the thread overview, I do a generic REST call here, which also includes calculation of other things
                 * which will be discarded
                 */
                url: "http://127.0.0.1:5000/crawl_n_calculate/?an=&t_id=&u_f_t=all&u_s_e=grt&u_s_n=-99999&u_s_d=asc&u_s_t=author&a_f_t=all&a_s_e=grt&a_s_n=-99999&a_s_d=asc&a_s_t=random",
                success: _onSuccessInitialCall,
                error: function () {

                    // Close that previously opened BootStrapDialog dialog
                    _closeBootStrapDialog();

                    //noinspection JSCheckFunctionSignatures
                    BootstrapDialog.show({
                        title: 'Fatal error! thread could not be found',
                        message: 'Thread not found in database.. Please check ID of thread and DB consistency!',
                        type: BootstrapDialog.TYPE_WARNING,
                        closable: true
                    });
                },
                timeout: 30000 // Throws an error after 30 seconds of inactivity
            });

        };

    /**
     * Initializes the MongoDBConnector itself
     *
     * @returns {object} MongoDBConnector object
     * @public
     */
    that.init = function () {

        _initVars();
        _initEvents();
        _initialRestCall();

    };
    return that;
}();