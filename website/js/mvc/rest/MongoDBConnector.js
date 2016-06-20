// Source: https://stackoverflow.com/a/5225641
// https://xuad.net/artikel/vom-einfachen-ajax-request-zum-komplexen-objektaustausch-mit-json-mittels-jquery/

IAMA_Extension.MongoDBConnector = function () {
    var that = {},
        body,

        _onSuccess = function(content) {
            // console.log(content);

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

                // $.each( answered_questions, function( key, value ) {
                //     console.log( key + ": " + value );
                // });

                // $.response.each(response.statistics_panel, function(k, v) {
                //    console.log(k, v);
                // });


            } else {
                alert("Error receiving JSON! Please fix python data conversion for REST");
            }

        },

        _getThreadDataFromDB = function(event, threadID) {
            // The ajax call which gets information through REST from the reddit API and the mongoDB
            $.ajax({
                type: "GET",
                url: "http://127.0.0.1:5000/calculate_data/" + threadID + "_all_grt_-99999_asc_random__all_grt_-99999_asc_random",
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