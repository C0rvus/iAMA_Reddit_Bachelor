// Source: https://stackoverflow.com/a/5225641
// https://xuad.net/artikel/vom-einfachen-ajax-request-zum-komplexen-objektaustausch-mit-json-mittels-jquery/

IAMA_Extension.MongoDBConnector = function () {
    var that = {},
        body,

        _onSuccess = function(content) {
            // console.log(content);

            // BootstrapDialog.closeAll();

            // Parses the JSON response into an java script accessable object
            var response = $.parseJSON(content);

            // Whenever the response received is valid
            if(!response.result) {
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

        // Whenever a thread has been clicked on the left side panel
    // TODO: Hier reinschreiben, wie denn das, zu übergebende Objekt eigentlich aussieht....
        // [ String [ Arr ] [ Arr ] ]
        _getThreadDataFromDB = function(event, data) {
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

                // url: "http://127.0.0.1:5000/calculate_data/" + threadID + "_all_grt_-99999_asc_random__all_grt_-99999_asc_random",

                url: "http://127.0.0.1:5000/calculate_data/" + threadID +
                "_" + unanswered_Filter_Settings_Tier +
                "_" + unanswered_Filter_Settings_Score_Compare +
                "_" + unanswered_Filter_Settings_Score_Value +
                "_" + unanswered_Sorting_Settings_Asc_Des +
                "_" + unanswered_Sorting_Settings_Type +
                "_" +
                "_" + answered_Filter_Settings_Tier +
                "_" + answered_Filter_Settings_Score_Compare +
                "_" + answered_Filter_Settings_Score_Value +
                "_" + answered_Sorting_Settings_Asc_Des +
                "_" + answered_Sorting_Settings_Type,
                // data: { get_param: 'value' },
                // dataType: 'json',
                success: _onSuccess,
                error: function(){
                    alert("Thread not found in database.. Please check ID of thread and DB consistency!");
                },
                timeout: 25000 // Throws an error after 15 seconds of inactivity
            });


        },

        // Initializes necessary variables for triggering
        _initVars = function () {
            body = $(document.body);
        },


    // References misc listeners here
        _initEvents = function () {
            body.on('rest_Get_Data_From_DB', _getThreadDataFromDB);
        };


    that.init = function () {
        _initVars();
        _initEvents();
    };
    return that;
}();