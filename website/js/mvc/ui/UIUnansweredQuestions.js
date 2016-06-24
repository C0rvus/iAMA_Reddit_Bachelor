// Source: http://stackoverflow.com/questions/759887/how-to-create-a-dom-node-as-an-object
// http://stackoverflow.com/questions/5076466/javascript-replace-n-with-br

IAMA_Extension.UIUnansweredQuestions = function () {
    var that = {},
        body,

        question_Panel = null,

    // Assigns necessary thread data to the top panel
        _onQuestionsToDOM = function (event, data) {

            console.log("Ich bin hier drinnen !!!", data);

            // Removes the first example answer here
            $("#iAMA_Question_Panel").find("> li" ).remove();

            // Iterates over every q&a combination and patches the DOM elements together
            $.each( data, function( key, value ) {

                var question_author = value['question_author'],
                    question_id = value['question_id'],
                    question_text = value['question_text'].replace(new RegExp('\r?\n','g'), '<br>'),
                    question_timestamp = value['question_timestamp'],
                    question_upvote_score = value['question_upvote_score'],

                    li_top = null;

                // Mini logic to correctly format the timestamp here
                if (question_upvote_score == 1) {
                    question_upvote_score = question_upvote_score.toString() + " upvote";
                } else {
                    question_upvote_score = question_upvote_score.toString() + " upvotes"
                }

                // Necessary for different messaging color
                if (key % 2 === 0 || key === 0) {
                    li_top = $("<li class='left clearfix chat-message-0' id='" + question_id + "'" + "> </li>");

                } else {
                    li_top = $("<li class='left clearfix chat-message-1' id='" + question_id + "'" + "> </li>");
                }

                // Building question containers here
                var q_image = $("<span class='chat-img pull-left'><img src='/../website/img/question_mark_little.png'" +
                    " alt='Q-Image'class='img-circle'/></span>"),

                    q_uber_container = $("<div class='chat-body clearfix'></div>"),
                    q_header = $("<div class='header'></div>"),

                    // Question elements are defined here
                    q_p_username = $("<p class='primary-font strong'>" + question_author + "</p>"),
                    q_p_posting_time = $("<p class='pull-right text-muted small'>" + question_timestamp + "<i class='fa fa-clock-o fa-fw'></i> </p> <br>"),
                    q_p_score = $("<p class='pull-right text-muted small'>" + question_upvote_score + "<i class='fa fa-bullseye fa-fw'> </i> </p> <br>"),
                    q_p_question_id = $("<p class='pull-right text-muted small'>" + question_id + "<i class='fa fa-bookmark fa-fw'> </i> </p>"),
                    q_p_text = $("<br> <p>" + question_text + "</p>"),
                    
                    q_answer_uber_container = $("<div class='chat-body'></div>"),
                    q_answer_text_area = $("<textarea class='custom_chat' id='btn-input_y' rows='3'>Type your answer here...</textarea>"),
                    
                    q_answer_buttons_uber_container = $("<div class='input-group-btn'> </div>"),
                    q_answer_buttons_template_container = $("<div class='chat_template_button'>"),
                    q_answer_buttons_template_button = $("<button class='btn btn-warning btn-sm dropdown-toggle' id='btn-template_1' data-toggle='dropdown'>Already answered <i class='fa fa-check fa-fw'></i></button>"),

                    q_answer_buttons_send_container = $("<div class='chat_send_button'></div>"),
                    q_answer_buttons_send_button = $("<button class='btn btn-warning btn-sm'>Send</button>");

                // Chains the question objects all together
                q_header.appendTo(q_uber_container);
                q_p_username.appendTo(q_header);
                q_p_posting_time.appendTo(q_header);
                q_p_score.appendTo(q_header);
                q_p_question_id.appendTo(q_header);
                q_p_text.appendTo(q_header);

                // Chains answer possibilities together here
                q_answer_text_area.appendTo(q_answer_uber_container);

                // Appends single dom elements to answer button template
                q_answer_buttons_template_container.appendTo(q_answer_buttons_uber_container);
                q_answer_buttons_template_button.appendTo(q_answer_buttons_template_container);

                q_answer_buttons_template_container.appendTo(q_answer_uber_container);

                // Builds together the send button
                q_answer_buttons_send_button.appendTo(q_answer_buttons_send_container);
                q_answer_buttons_send_container.appendTo(q_answer_uber_container);


                // Appends all container objects to the top level DOM <li> element
                q_image.appendTo(li_top);
                q_uber_container.appendTo(li_top);
                q_answer_uber_container.appendTo(li_top);

                // Adds that combination to the answer panel
                question_Panel.append(li_top);
            });
        },

    // References UI elements in here
        _initUI = function () {

            body = $(document.body);
            question_Panel = $('#iAMA_Question_Panel');

        },

    // References misc listeners here
        _initEvents = function () {
            $(body).on('unanswered_Questions_To_DOM', _onQuestionsToDOM);
        };


    that.init = function () {
        _initUI();
        _initEvents();
    };
    return that;
}();