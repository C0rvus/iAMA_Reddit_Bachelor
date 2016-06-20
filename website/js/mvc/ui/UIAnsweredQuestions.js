// Source: http://stackoverflow.com/questions/759887/how-to-create-a-dom-node-as-an-object

IAMA_Extension.UIAnsweredQuestions = function () {
    var that = {},
        body,

        answer_Panel = null,

    // Assigns necessary thread data to the top panel
        _onAnswersToDOM = function (event, data) {
            console.log("CORRRRRRRRRRRRRRRRRRECT");

            console.log(data);

            // Removes the first example answer here
            $( "#iAMA_Answer_Panel").find("> li" ).remove();

            $.each( data, function( key, value ) {

                var answer_id = value['answer_id'],
                    answer_text = value['answer_text'],
                    answer_timestamp = value['answer_timestamp'],
                    answer_upvote_score = value['answer_upvote_score'],

                    question_author = value['question_author'],
                    question_id = value['question_id'],
                    question_text = value['question_text'],
                    question_timestamp = value['question_timestamp'],
                    question_upvote_score = value['question_upvote_score'];

                // TODO : That one here is necessary for different class behaviour
                if (key % 2 === 0 || key === 0) {
                    console.log(key, "Ich bin gerade !! also gleich 0")
                }



                // Hier in jedem Element nochmal drueber gehen
            });



            // TODO: Hier schauen mittels iteration und modulo 2 ob gerade Zahl oder nicht, und das reinbauen
            var li_top = $("<li class='left clearfix chat-message-0'> </li>");

            var separator_q_n_a = $("<hr class='ruler-answered-questions'>");

            var combined = $(li_top).append(separator_q_n_a);


            // Building question containers here
            var q_uber_container = $("<div class='left clearfix'> </div>");
            var q_header = $("<div class='header'> </div>");

            var q_p_username = $("<p class='pull-left primary-font strong'> </p>"); //TODO: Username in here

            var q_p_posting_time = $("<p class='pull-right text-muted small chat-answered-questions'> </p>"); // TODO: Posting time
            var q_i_posting_time_icon = $("<i class='fa fa-clock-o fa-fw'> </i>");

            var break_line = $("<br>");

            var q_p_score = $("<p class='pull-right text-muted small chat-answered-questions'> </p>"); // TODO: Amount of points
            var q_i_score = $("<i class='fa fa-bullseye fa-fw'> </i>");

            var q_p_question_id = $("<p class='pull-right text-muted small chat-answered-questions'> </p>"); // TODO: Amount of points
            var q_i_question_id = $("<i class='fa fa-bullseye fa-fw'> </i>");

            var q_p_text = $("<p class='chat-alignment-left'> </p>"); //TODO Question text in here


            answer_Panel.append(combined);

            // TODO: Das hier testweise mal zusammenbauen!

        },

    // References UI elements in here
        _initUI = function () {

            body = $(document.body);
            answer_Panel = $('#iAMA_Answer_Panel');

        },

    // References misc listeners here
        _initEvents = function () {
            $(body).on('answered_Questions_To_DOM', _onAnswersToDOM);

        };


    that.init = function () {
        _initUI();
        _initEvents();
    };
    return that;
}();