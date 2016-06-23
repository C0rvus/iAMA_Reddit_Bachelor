// Source: http://stackoverflow.com/questions/759887/how-to-create-a-dom-node-as-an-object
// http://stackoverflow.com/questions/5076466/javascript-replace-n-with-br

IAMA_Extension.UIAnsweredQuestions = function () {
    var that = {},
        body,

        answer_Panel = null,

    // Assigns necessary thread data to the top panel
        _onAnswersToDOM = function (event, data) {

            console.log("BIN HIER DRINANSASDNDANSDANSSDAN");

            // Removes the first example answer here
            $( "#iAMA_Answer_Panel").find("> li" ).remove();

            // Iterates over every q&a combination and patches the DOM elements together
            $.each( data, function( key, value ) {

                var answer_id = value['answer_id'],
                    answer_text = value['answer_text'].replace(new RegExp('\r?\n','g'), '<br>'),
                    answer_timestamp = value['answer_timestamp'],
                    answer_upvote_score = value['answer_upvote_score'],

                    question_author = value['question_author'],
                    question_id = value['question_id'],
                    question_text = value['question_text'].replace(new RegExp('\r?\n','g'), '<br>'),
                    question_timestamp = value['question_timestamp'],
                    question_upvote_score = value['question_upvote_score'],

                    li_top = null;

                // Mini logic to correctly format the timestamp here
                if (answer_upvote_score == 1) {
                    answer_upvote_score = answer_upvote_score.toString() + " upvote";
                } else {
                    answer_upvote_score = answer_upvote_score.toString() + " upvotes"
                }

                // Mini logic to correctly format the timestamp here
                if (question_upvote_score == 1) {
                    question_upvote_score = question_upvote_score.toString() + " upvote";
                } else {
                    question_upvote_score = question_upvote_score.toString() + " upvotes"
                }

                // Necessary for different messaging color
                if (key % 2 === 0 || key === 0) {
                    li_top = $("<li class='left clearfix chat-message-0' id='" + answer_id + "'" + "> </li>");

                } else {
                    li_top = $("<li class='left clearfix chat-message-1' id='" + answer_id + "'" + "> </li>");
                }

                // Defining DOM Elements here
                var separator_q_n_a = $("<hr class='ruler-answered-questions'>"),

                    // Building question containers here
                    q_uber_container = $("<div class='left clearfix'></div>"),
                    q_header = $("<div class='header'></div>"),

                    // Question elements are defined here
                    q_p_username = $("<p class='pull-left primary-font strong'>" + question_author + "</p>"),
                    q_p_posting_time = $("<p class='pull-right text-muted small chat-answered-questions'>" + question_timestamp + "<i class='fa fa-clock-o fa-fw'></i> </p> <br>"),
                    q_p_score = $("<p class='pull-right text-muted small chat-answered-questions'>" + question_upvote_score + "<i class='fa fa-bullseye fa-fw'> </i> </p> <br>"),
                    q_p_question_id = $("<p class='pull-right text-muted small chat-answered-questions'>" + question_id + "<i class='fa fa-bookmark fa-fw'> </i> </p> <br> <br>"),
                    q_p_text = $("<p class='chat-alignment-left'>" + question_text + "</p>"),

                    a_uber_container = $("<div class='right clearfix'></div>"),
                    a_header = $("<div class='header'></div>"),
                    a_p_username = $("<p class='pull-right primary-font strong'>" + "You" + "</p><br>"),
                    a_p_posting_time = $("<p class='pull-left text-muted small chat-answered-questions'><i class='fa fa-clock-o fa-fw'></i>" + answer_timestamp + "</p><br>"),
                    a_p_score = $("<p class='pull-left text-muted small chat-answered-questions'><i class='fa fa-bullseye fa-fw'></i>" + answer_upvote_score + "</p><br>"),
                    a_p_answer_id = $("<p class='pull-left text-muted small chat-answered-questions'><i class='fa fa-bookmark fa-fw'></i>" + answer_id + "</p><br><br>"),
                    a_p_text = $("<p class='chat-alignment-right'>" + answer_text + "</p>");

                // Chains the question objects all together
                q_header.appendTo(q_uber_container);
                q_p_username.appendTo(q_header);
                q_p_posting_time.appendTo(q_header);
                q_p_score.appendTo(q_header);
                q_p_question_id.appendTo(q_header);
                q_p_text.appendTo(q_header);

                // Chains the answer objects all together
                a_header.appendTo(a_uber_container);
                a_p_username.appendTo(a_header);
                a_p_posting_time.appendTo(a_header);
                a_p_score.appendTo(a_header);
                a_p_answer_id.appendTo(a_header);
                a_p_text.appendTo(a_header);

                // Appends all container objects to the top level DOM <li> element
                q_uber_container.appendTo(li_top);
                separator_q_n_a.appendTo(li_top);
                a_uber_container.appendTo(li_top);

                // Adds that combination to the answer panel
                answer_Panel.append(li_top);
            });
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