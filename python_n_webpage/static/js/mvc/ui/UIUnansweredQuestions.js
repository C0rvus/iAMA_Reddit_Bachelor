// Source: http://stackoverflow.com/questions/759887/how-to-create-a-dom-node-as-an-object
// http://stackoverflow.com/questions/5076466/javascript-replace-n-with-br
// http://stackoverflow.com/questions/24678799/how-to-unbind-keyup-event
// http://stackoverflow.com/questions/1927593/cant-update-textarea-with-javascript-after-writing-to-it-manualy
// http://stackoverflow.com/questions/17414034/change-mouse-cursor-in-javascript-or-jquery
// https://learn.jquery.com/using-jquery-core/faq/how-do-i-get-the-text-value-of-a-selected-option/

IAMA_Extension.UIUnansweredQuestions = function () {
    var that = {},

        body,
        top_Bar = null,
        thread_Overview = null,
        unanswered_Uber_Div = null,
        answered_Uber_Div = null,

        question_Panel = null,

        unanswered_Filter_Button = null,
        unanswered_Sorting_Button = null,
        unanswered_Refresh_Button = null,

        unanswered_Filter_Settings_Tier = null,
        unanswered_Filter_Settings_Score_Compare = null,
        unanswered_Filter_Settings_Score_Value = null,
        unanswered_Sorting_Settings_Type = null,
        unanswered_Sorting_Settings_Asc_Des = null,

        answered_Filter_Settings_Tier = null,
        answered_Filter_Settings_Score_Compare = null,
        answered_Filter_Settings_Score_Value = null,
        answered_Sorting_Settings_Type = null,
        answered_Sorting_Settings_Asc_Des = null,

        _closeBootStrapDialog = function () {
            BootstrapDialog.closeAll()
        },

        _getThreadID = function () {

            var id_Of_Actual_Selected_Thread = null;

            $('#iAMA_Thread_Overview').find('li').each(function () {

                // Iterates over all threads trying to find the selected / highlighted one
                if ($(this).hasClass("thread_selected") === true) {
                    id_Of_Actual_Selected_Thread = $(this).attr('id');

                }
            });

            return id_Of_Actual_Selected_Thread;

        },

        _getDataForAnsweredQuestionsFromWebSite = function () {

            var sorting_Selection_Answered_Found = null;

            answered_Filter_Settings_Tier = $('#iAMA_Answered_Filtering_Tier_Selection').val();
            answered_Filter_Settings_Score_Compare = $('#iAMA_Answered_Filtering_Score_Selection').val();


            // Settings score will be defined here (whenever nothing has been input)
            if ($('#iAMA_Answered_Filtering_Score_Concrete').val() === "" || $('#iAMA_Answered_Filtering_Score_Concrete').val() === null) {
                answered_Filter_Settings_Score_Value = -99999;
                answered_Filter_Settings_Score_Compare = "grt";
            } else {
                answered_Filter_Settings_Score_Value = $('#iAMA_Answered_Filtering_Score_Concrete').val();
            }


            // Iterates over every elements and checks whether it has been selected or not!
            $('#iAMA_Answered_Sorting').find('li').each(function () {

                // Whenever a highlighted sorting has been found apply that value into an appropriate variable
                if ($(this).hasClass("sorting_Selected") === true) {

                    sorting_Selection_Answered_Found = ($.trim($(this).text()));
                }
            });


            // Correctly converts the "Settings Type" value into REST compatible information
            switch(sorting_Selection_Answered_Found) {

                case null:
                    answered_Sorting_Settings_Type = "random";
                    answered_Sorting_Settings_Asc_Des = "asc"; // Setting it to asc or desc here does not matter, because it's random
                    break;

                case "Random":
                    answered_Sorting_Settings_Type = "random";
                    answered_Sorting_Settings_Asc_Des = "asc"; // Setting it to asc or desc here does not matter, because it's random
                    break;

                case "Author name ascending":
                    answered_Sorting_Settings_Type = "author";
                    answered_Sorting_Settings_Asc_Des = "asc";
                    break;

                case "Author name descending":
                    answered_Sorting_Settings_Type = "author";
                    answered_Sorting_Settings_Asc_Des = "des";
                    break;

                case "Creation time ascending":
                    answered_Sorting_Settings_Type = "creation";
                    answered_Sorting_Settings_Asc_Des = "asc";
                    break;

                case "Creation time descending":
                    answered_Sorting_Settings_Type = "creation";
                    answered_Sorting_Settings_Asc_Des = "des";
                    break;

                case "Score ascending":
                    answered_Sorting_Settings_Type = "score";
                    answered_Sorting_Settings_Asc_Des = "asc";
                    break;

                case "Score descending":
                    answered_Sorting_Settings_Type = "score";
                    answered_Sorting_Settings_Asc_Des = "des";
                    break;

                default:
                    answered_Sorting_Settings_Type = "random";
                    answered_Sorting_Settings_Asc_Des = "asc"; // Setting it to asc or desc here does not matter, because it's random
            }

            return [answered_Filter_Settings_Tier, answered_Filter_Settings_Score_Compare, answered_Filter_Settings_Score_Value,
                answered_Sorting_Settings_Type, answered_Sorting_Settings_Asc_Des]

        },

        _getDataForUnansweredQuestionsFromWebSite = function () {
            unanswered_Filter_Settings_Tier = $('#iAMA_Unanswered_Filtering_Tier_Selection').val();
            unanswered_Filter_Settings_Score_Compare = $('#iAMA_Unanswered_Filtering_Score_Selection').val();

            // Settings score will be defined here (whenever nothing has been input)
            if ($('#iAMA_Unanswered_Filtering_Score_Concrete').val() === "" || ($('#iAMA_Unanswered_Filtering_Score_Concrete').val() === null)) {
                unanswered_Filter_Settings_Score_Value = -99999;
                unanswered_Filter_Settings_Score_Compare = "grt";
            } else {
                unanswered_Filter_Settings_Score_Value = $('#iAMA_Unanswered_Filtering_Score_Concrete').val();
            }

            // Correctly converts the "Settings Type" value into REST compatible information
            switch(unanswered_Sorting_Settings_Type) {
                case null:
                    unanswered_Sorting_Settings_Type = "random";
                    unanswered_Sorting_Settings_Asc_Des = "asc"; // Setting it to asc or desc here does not matter, because it's random
                    break;

                case "Random":
                    unanswered_Sorting_Settings_Type = "random";
                    unanswered_Sorting_Settings_Asc_Des = "asc"; // Setting it to asc or desc here does not matter, because it's random
                    break;

                case "Author name ascending":
                    unanswered_Sorting_Settings_Type = "author";
                    unanswered_Sorting_Settings_Asc_Des = "asc";
                    break;

                case "Author name descending":
                    unanswered_Sorting_Settings_Type = "author";
                    unanswered_Sorting_Settings_Asc_Des = "des";
                    break;

                case "Creation time ascending":
                    unanswered_Sorting_Settings_Type = "creation";
                    unanswered_Sorting_Settings_Asc_Des = "asc";
                    break;

                case "Creation time descending":
                    unanswered_Sorting_Settings_Type = "creation";
                    unanswered_Sorting_Settings_Asc_Des = "des";
                    break;

                case "Score ascending":
                    unanswered_Sorting_Settings_Type = "score";
                    unanswered_Sorting_Settings_Asc_Des = "asc";
                    break;

                case "Score descending":
                    unanswered_Sorting_Settings_Type = "score";
                    unanswered_Sorting_Settings_Asc_Des = "des";
                    break;

                default:
                    unanswered_Sorting_Settings_Type = "random";
                    unanswered_Sorting_Settings_Asc_Des = "asc"; // Setting it to asc or desc here does not matter, because it's random
            }

            return [unanswered_Filter_Settings_Tier, unanswered_Filter_Settings_Score_Compare, unanswered_Filter_Settings_Score_Value,
                unanswered_Sorting_Settings_Type, unanswered_Sorting_Settings_Asc_Des];
        },

        _appendOnClickListenerForSendButton = function(dom_Element, id_of_question) {

            return dom_Element.click("click", function () {

                var data = { "text" : $("#" + id_of_question + "_answer_box").val() };

                console.log("Ausgabe text von input field !!", $("#" + id_of_question + "_answer_box").val());
                console.log("id_of_question", id_of_question);


                BootstrapDialog.show({
                    title: 'Sending data to to reddit now...',
                    message: 'Your answer is beeing uploaded to reddit right now. Please wait a few seconds..',
                    type: BootstrapDialog.TYPE_WARNING,
                    closable: false});

                $.ajax({
                    type: "POST",
                    url: "http://127.0.0.1:5000/post_to_reddit/?c_id=" + id_of_question,
                    processData: false,
                    contentType: 'application/json',
                    data: JSON.stringify(data),
                    success: function() {

                        // Whenever post -> REST -> Successful
                        // Close Dialog
                        // Refresh data

                        console.log("SUCCCESSSS");
                        _closeBootStrapDialog();
                        // Fakeclick refresh button
                        unanswered_Refresh_Button.click();



                    }});


            });

        },

    // Appends an onclick listener to the "already answered" button
        _appendOnClickListenerForAlreadyAnswered = function (dom_Element, id_Of_Question) {

            var id_of_actual_selected_thread = "";

            // Iterates over all list elements checking which has the class "thread_selected"
            $("#iAMA_Thread_Overview").children('li').each(function () {

                if ($(this).hasClass("thread_selected") === true) {
                    id_of_actual_selected_thread = $(this).attr('id')
                }

            });


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
                                    "https://www.reddit.com/r/Gigan/comments/" + id_of_actual_selected_thread + "/-/" + this.id);

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

            _closeBootStrapDialog();
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
                var q_image = $("<span class='chat-img pull-left'><img src='img/question_mark_little.png'" +
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
                    q_answer_buttons_template_button = $("<button class='btn btn-warning btn-sm dropdown-toggle' data-toggle='dropdown'>Already answered <i class='fa fa-check fa-fw'></i></button>"),

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

                // Appends an onclick listener for the send button
                //noinspection JSUnusedAssignment
                q_answer_buttons_send_button = _appendOnClickListenerForSendButton(q_answer_buttons_send_button, question_id);


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
            unanswered_Refresh_Button.click(function () {

                // Defines two arrays which will contain information about the various statemenets
                // Necessary to also get information for the answered questions, due to the way the REST mechanism was
                // built
                var information_Unanswered_Questions = _getDataForUnansweredQuestionsFromWebSite(),
                    information_Answered_Questions = _getDataForAnsweredQuestionsFromWebSite(),
                    selected_Thread_ID = _getThreadID();

                $(body).trigger('Refresh_To_UI',[[selected_Thread_ID, [information_Unanswered_Questions],[information_Answered_Questions]]]);

                // Shows a short warning message to prevent user interaction while receiving data
                BootstrapDialog.show({
                    title: 'Fetching data from data base',
                    message: 'Please wait a few seconds until the newly loaded data arrives...',
                    type: BootstrapDialog.TYPE_WARNING,
                    closable: false});

            });
        },

    // Whenever the filter button has been clicked
        _onFilterClicked = function () {

            // Defines the click listener for tier selection
            $('#iAMA_Unanswered_Filtering_Tier_Selection').click(function () {
                unanswered_Filter_Settings_Tier = $(this).find('option:selected').text();
            });

            // Defines the click listener for score comparison selection
            $('#iAMA_Unanswered_Filtering_Score_Selection').click(function () {
                unanswered_Filter_Settings_Score_Compare = $(this).find('option:selected').text();
            });

            // Defines the concrete numeric value to be input into the score field
            $('#iAMA_Unanswered_Filtering_Score_Concrete').click(function () {

                // Whenever nothing has been initially selected
                if ($(this).val() === null || $(this).val() === "") {
                    // Setting the values to these high values prevents unexpected user behaviour and prevents
                    // that the original setting "eql 0" gets triggered (which will display no data..)
                    
                    unanswered_Filter_Settings_Score_Compare = "grt";
                    unanswered_Filter_Settings_Score_Value = "-9999999";

                } else {
                    unanswered_Filter_Settings_Score_Value = $(this).val();
                }
                
            });

            // Defines the reset button for filtering methods
            $('#iAMA_Unanswered_Filtering_Reset').click(function () {

                // Reset the values within the code to null here
                unanswered_Filter_Settings_Tier = null;
                unanswered_Filter_Settings_Score_Compare = null;
                unanswered_Filter_Settings_Score_Value = null;

                // Reset the frontend changes previously made
                $('#iAMA_Unanswered_Filtering_Tier_Selection').val("all");
                $('#iAMA_Unanswered_Filtering_Score_Selection').val("eql");
                $('#iAMA_Unanswered_Filtering_Score_Concrete').val(null);

            });
        },

    // Whenever the sorting button has been clicked
        _onSortingClicked = function () {
            // Appends a click listener for every dom element
            unanswered_Sorting_Button.find("li").each(function () {
                $(this).click(function () {

                    // 1st. Remove the class "sorting_Selected" from every element
                    // 2nd. Add that class to the selected element
                    unanswered_Sorting_Button.find("li").each(function () {
                        $(this).removeClass("sorting_Selected");
                    });

                    $(this).addClass("sorting_Selected");

                    var text_Of_Clicked_Element = $.trim($(this).text());
                    if (text_Of_Clicked_Element !== "Close dropdown") {
                        unanswered_Sorting_Settings_Type = text_Of_Clicked_Element;
                    }
                })
            })
        },

    // References UI elements in here
        _initUI = function () {

            body = $(document.body);

            top_Bar = $('#iAMA_Top_Bar_Div');
            thread_Overview = $('#iAMA_Thread_Overview');
            unanswered_Uber_Div = $('#iAMA_Unanswered_Uber_Div');
            answered_Uber_Div = $('#iAMA_Answered_Uber_Div');

            question_Panel = $('#iAMA_Question_Panel');

            unanswered_Filter_Button = $('#iAMA_Unanswered_Filter');
            _onFilterClicked();

            unanswered_Sorting_Button = $('#iAMA_Unanswered_Sorting');
            _onSortingClicked();

            unanswered_Refresh_Button = $('#iAMA_Unanswered_Refresh');
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