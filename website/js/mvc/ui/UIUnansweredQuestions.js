// Source: http://stackoverflow.com/questions/759887/how-to-create-a-dom-node-as-an-object
// http://stackoverflow.com/questions/5076466/javascript-replace-n-with-br
// http://stackoverflow.com/questions/24678799/how-to-unbind-keyup-event
// http://stackoverflow.com/questions/1927593/cant-update-textarea-with-javascript-after-writing-to-it-manualy
// http://stackoverflow.com/questions/17414034/change-mouse-cursor-in-javascript-or-jquery

IAMA_Extension.UIUnansweredQuestions = function () {
    var that = {},

        body,
        top_Bar = null,
        thread_Overview = null,
        unanswered_Uber_Div = null,
        answered_Uber_Div = null,

        question_Panel = null,

        filter_Button = null,

        filter_Settings = null,
        sorting_Settings = null,

        sorting_Button = null,
        refresh_Button = null,

    // Appends an onclick listener to the "already answered" button
        _appendOnClickListenerForAlreadyAnswered = function (dom_Element, id_Of_Question) {
            return dom_Element.click(function () {

                //noinspection JSCheckFunctionSignatures
                BootstrapDialog.show({
                    title: 'Important information',
                    message: 'To refer to an answer you have already made simply click "Pick answer" and select the appropriate answer' +
                    ' from the expanded "Answered Questions" by clicking on it. \n\n After the selection the link to the given answer will be applied' +
                    ' to text input field. Additionally the "Unanswered Questions" panel will be restored',
                    buttons: [{
                        icon: 'glyphicon glyphicon-send',
                        label: 'Pick answer',
                        cssClass: 'btn-primary',
                        autospin: true,
                        action: function (dialogRef) {

                            //noinspection JSCheckFunctionSignatures
                            dialogRef.enableButtons(false);
                            dialogRef.setClosable(false);
                            dialogRef.getModalBody().html('Loading up necessary javascripts...');

                            // Fades out some DOM Elements for having better overview while selecting answers
                            top_Bar.fadeToggle();
                            thread_Overview.fadeToggle();
                            unanswered_Uber_Div.fadeToggle();

                            // Changes the class for expanded view at full screen width here
                            answered_Uber_Div.removeClass("col-lg-4");
                            answered_Uber_Div.addClass("col-lg-12");

                            // Turns the cursor into a crosshair for letting the user know to select a post now
                            body.css('cursor','crosshair');

                            // On click (answer selection) behaviour for all child elements <li> of the answer panel
                            $('#iAMA_Answer_Panel').find('> li').on('click', function () {

                                // Fade the, previously hidden, elements back
                                top_Bar.fadeToggle();
                                thread_Overview.fadeToggle();
                                unanswered_Uber_Div.fadeToggle();

                                // Reset the view for a better behaviour
                                answered_Uber_Div.removeClass("col-lg-12");
                                answered_Uber_Div.addClass("col-lg-4");

                                // Reverts the cursor behaviour back to normal
                                body.css('cursor','default');

                                // Appends the clicked id to the regarding answer text box
                                //noinspection JSJQueryEfficiency
                                $('#' + id_Of_Question + '_answer_box').val($('#' + id_Of_Question + '_answer_box').val() + "\n" +
                                    "https://www.reddit.com/r/iama/comments/catch_Thread_ID_Here/-/" + this.id);

                                // Whenever the click has been set, unbind that given behaviour
                                $('#iAMA_Answer_Panel').find('> li').unbind("click");

                            });

                            // Whenever ESC has been pressed revert to original view
                            $(document).on('keyup', function (e) {
                                if (e.keyCode === 27) {

                                    $('#iAMA_Answer_Panel').find('> li').unbind("click");

                                    // Fade the, previously hidden, elements back
                                    top_Bar.fadeIn();
                                    thread_Overview.fadeIn();
                                    unanswered_Uber_Div.fadeIn();

                                    // Reset the view for a better behaviour
                                    answered_Uber_Div.removeClass("col-lg-12");
                                    answered_Uber_Div.addClass("col-lg-4");

                                    // Reverts the cursor behaviour back to normal
                                    body.css('cursor','default');

                                }
                            });

                            // Defines a little timeout to let the user think something great is going to happen...
                            setTimeout(function () {
                                dialogRef.close();
                            }, 2000);
                        }
                    }, {
                        // Defines the closing button (behaviour) here
                        label: 'Close',
                        action: function (dialogRef) {
                            dialogRef.close();
                        }
                    }]
                });

            });

        },

    // Assigns necessary thread data to the top panel
        _onQuestionsToDOM = function (event, data) {

            console.log("Ich bin hier drinnen !!!", data);

            // Removes the first example answer here
            $("#iAMA_Question_Panel").find("> li").remove();

            // Iterates over every q&a combination and patches the DOM elements together
            $.each(data, function (key, value) {

                var question_author = value['question_author'],
                    question_id = value['question_id'],
                    question_text = value['question_text'].replace(new RegExp('\r?\n', 'g'), '<br>'),
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
                        " alt='Q-Image' class='img-circle'/></span>"),

                    q_uber_container = $("<div class='chat-body clearfix'></div>"),
                    q_header = $("<div class='header'></div>"),

                // Question elements are defined here
                    q_p_username = $("<p class='primary-font strong'>" + question_author + "</p>"),
                    q_p_posting_time = $("<p class='pull-right text-muted small'>" + question_timestamp + "<i class='fa fa-clock-o fa-fw'></i> </p> <br>"),
                    q_p_score = $("<p class='pull-right text-muted small'>" + question_upvote_score + "<i class='fa fa-bullseye fa-fw'> </i> </p> <br>"),
                    q_p_question_id = $("<p class='pull-right text-muted small'>" + question_id + "<i class='fa fa-bookmark fa-fw'> </i> </p>"),
                    q_p_text = $("<br> <p>" + question_text + "</p>"),

                    q_answer_uber_container = $("<div class='chat-body'></div>"),
                    q_answer_text_area = $("<textarea class='custom_chat' id=" + question_id + "_answer_box" + " rows='3'>Type your answer here...</textarea>"),

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

                // Appends an onclick listener to the "already answered button here"
                //noinspection JSUnusedAssignment
                q_answer_buttons_template_container = _appendOnClickListenerForAlreadyAnswered(q_answer_buttons_template_container, question_id);

                // Appends all container objects to the top level DOM <li> element
                q_image.appendTo(li_top);
                q_uber_container.appendTo(li_top);
                q_answer_uber_container.appendTo(li_top);

                // Adds that combination to the answer panel
                question_Panel.append(li_top);
            });
        },

    // Whenever the refresh button has been clicked
        _onRefreshClicked = function () {
            refresh_Button.click(function () {
                console.log("On refresh clicked");
            });
        },

    // Whenever the filter button has been clicked
        _onFilterClicked = function () {
            filter_Button.click(function () {
                console.log("On filter clicked...");
            });
        },

    // Whenever the sprtomg button has been clicked
        _onSortingClicked = function () {
            sorting_Button.click(function () {
                console.log("On sorting clicked...");
            });
        },

    // References UI elements in here
        _initUI = function () {

            body = $(document.body);

            top_Bar = $('#iAMA_Top_Bar_Div');
            thread_Overview = $('#iAMA_Thread_Overview');
            unanswered_Uber_Div = $('#iAMA_Unanswered_Uber_Div');
            answered_Uber_Div = $('#iAMA_Answered_Uber_Div');

            question_Panel = $('#iAMA_Question_Panel');

            filter_Button = $('#iAMA_Unanswered_Filter');
            _onFilterClicked();

            sorting_Button = $('#iAMA_Unanswered_Sorting');
            _onSortingClicked();

            refresh_Button = $('#iAMA_Unanswered_Refresh');
            _onRefreshClicked();

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