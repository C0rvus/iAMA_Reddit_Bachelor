/**
 *  @class UIUnansweredQuestions
 *  This class handles the behaviour of the questions within the unanswered questions panel.
 *  Additionally it handles the ability to pick up and refer to already answered questions.
 *  Furthermore it allows you to upload a comment made to reddit.
 *  -
 *  Sources used within this class:
 *  1.(15.06.2016 @ 13:15) - http://stackoverflow.com/questions/759887/how-to-create-a-dom-node-as-an-object
 *  2.(18.06.2016 @ 08:01) - http://stackoverflow.com/questions/5076466/javascript-replace-n-with-br
 *  3.(23.06.2016 @ 13:03) - http://stackoverflow.com/questions/24678799/how-to-unbind-keyup-event
 *  4.(26.06.2016 @ 14:05) - http://stackoverflow.com/questions/1927593/cant-update-textarea-with-javascript-after-writing-to-it-manualy
 *  5.(27.06.2016 @ 17:27) - http://stackoverflow.com/questions/17414034/change-mouse-cursor-in-javascript-or-jquery
 *  6.(27.06.2016 @ 07:29) - https://learn.jquery.com/using-jquery-core/faq/how-do-i-get-the-text-value-of-a-selected-option/
 *  7.(07.07.2016 @ 17:11) - http://stackoverflow.com/questions/7854820/sleep-pause-wait-in-javascript
 *  8.(08.07.2016 @ 22:14) - https://stackoverflow.com/a/16873849
 *
 */
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

        amount_Questions_Left_On_Send = null,

        /**
         * Closes an open BootstrapDialog
         * @private
         */
        _closeBootStrapDialog = function () {
            BootstrapDialog.closeAll()
        },

        /**
         * Iterates over all threads on the thread panel and looks for the class "thread_selected" in them
         *
         * @private
         * @returns {String} id_Of_Actual_Selected_Thread : The id of the thread which is actually selected.
         * The selected threads DOM id === the id of the thread on reddit
         */
        _getThreadID = function () {

            var id_Of_Actual_Selected_Thread = null;

            // Iterates ovver all "li" elements within the iAMA Thread Overview
            $('#iAMA_Thread_Overview').find('li').each(function () {

                // Iterates over all threads trying to find the selected / highlighted one
                if ($(this).hasClass("thread_selected") === true) {
                    id_Of_Actual_Selected_Thread = $(this).attr('id');

                }
            });

            return id_Of_Actual_Selected_Thread;

        },

        /**
         * Catches information about the sorting and filtering settings for the answered questions panel from the website
         * and stores that information into globally available variables
         * @private
         * @returns: {Array} [] containing
         *              - {String} answered_Filter_Settings_Tier
         *              - {String} answered_Filter_Settings_Score_Compare
         *              - {String} answered_Filter_Settings_Score_Value
         *              - {String} answered_Sorting_Settings_Type
         *              - {String} answered_Sorting_Settings_Asc_Des
         */
        _getDataForAnsweredQuestionsFromWebSite = function () {

            var sorting_Selection_Answered_Found = null;

            answered_Filter_Settings_Tier = $('#iAMA_Answered_Filtering_Tier_Selection').val();
            answered_Filter_Settings_Score_Compare = $('#iAMA_Answered_Filtering_Score_Selection').val();

            // Settings score will be defined here (whenever nothing has been input)
            //noinspection JSJQueryEfficiency
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


            // Correctly converts the "Sorting_Settings_Type" value into REST compatible information
            switch (sorting_Selection_Answered_Found) {

                case null:
                    answered_Sorting_Settings_Type = "random";
                    // Setting it to asc or desc here does not matter, because it's random
                    answered_Sorting_Settings_Asc_Des = "asc";
                    break;

                case "Random":
                    answered_Sorting_Settings_Type = "random";
                    // Setting it to asc or desc here does not matter, because it's random
                    answered_Sorting_Settings_Asc_Des = "asc";
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
                    // Setting it to asc or desc here does not matter, because it's random
                    answered_Sorting_Settings_Asc_Des = "asc";
            }

            return [answered_Filter_Settings_Tier, answered_Filter_Settings_Score_Compare, answered_Filter_Settings_Score_Value,
                answered_Sorting_Settings_Type, answered_Sorting_Settings_Asc_Des]

        },

        /**
         * Catches information about the sorting and filtering settings for the answered questions panel from the website
         * and stores that information into globally available variables
         * @private
         * @returns: {Array} [] containing
         *              - {String} unanswered_Filter_Settings_Tier
         *              - {String} unanswered_Filter_Settings_Score_Compare
         *              - {String} unanswered_Filter_Settings_Score_Value
         *              - {String} unanswered_Sorting_Settings_Type
         *              - {String} unanswered_Sorting_Settings_Asc_Des
         */
        _getDataForUnansweredQuestionsFromWebSite = function () {
            unanswered_Filter_Settings_Tier = $('#iAMA_Unanswered_Filtering_Tier_Selection').val();
            unanswered_Filter_Settings_Score_Compare = $('#iAMA_Unanswered_Filtering_Score_Selection').val();

            // Settings score will be defined here (whenever nothing has been input)
            //noinspection JSJQueryEfficiency
            if ($('#iAMA_Unanswered_Filtering_Score_Concrete').val() === "" || ($('#iAMA_Unanswered_Filtering_Score_Concrete').val() === null)) {
                unanswered_Filter_Settings_Score_Value = -99999;
                unanswered_Filter_Settings_Score_Compare = "grt";
            } else {
                unanswered_Filter_Settings_Score_Value = $('#iAMA_Unanswered_Filtering_Score_Concrete').val();
            }

            // Correctly converts the "Settings Type" value into REST compatible information
            switch (unanswered_Sorting_Settings_Type) {
                case null:
                    unanswered_Sorting_Settings_Type = "random";
                    // Setting it to asc or desc here does not matter, because it's random
                    unanswered_Sorting_Settings_Asc_Des = "asc";
                    break;

                case "Random":
                    unanswered_Sorting_Settings_Type = "random";
                    // Setting it to asc or desc here does not matter, because it's random
                    unanswered_Sorting_Settings_Asc_Des = "asc";
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
                    // Setting it to asc or desc here does not matter, because it's random
                    unanswered_Sorting_Settings_Asc_Des = "asc";
            }

            return [unanswered_Filter_Settings_Tier, unanswered_Filter_Settings_Score_Compare, unanswered_Filter_Settings_Score_Value,
                unanswered_Sorting_Settings_Type, unanswered_Sorting_Settings_Asc_Des];
        },

        /**
         * Appends an onClick listener for the send button within the unanswered questions panel, which will trigger
         * an ajax REST call
         *
         * @params: {String} dom_Element send button as DOM-Element
         * @params: {String} id_of_question the id of the question the answer text blongs to
         * @private
         */
        _appendOnClickListenerForSendButton = function (dom_Element, id_of_question, given_Question_Text) {

            return dom_Element.click("click", function () {

                // Triggers to write meta data text file
                //noinspection JSJQueryEfficiency
                _sendUsageMetaData("(unanswered) Clicked SEND Button for question '" + given_Question_Text + "' with following answer: " + $("#" + id_of_question + "_answer_box").val());

                //noinspection JSJQueryEfficiency
                var data = {"text": $("#" + id_of_question + "_answer_box").val()};

                /**
                 *  Iterates over every question within the question panel
                 *  This is necessary for checking the correctness of the returned data, because reddit, sometimes,
                 *  does not refresh its data as fast as we want to be. Because after posting, we recrawl all that
                 *  thread data (but very often reddit does yet only return old data, therefore we do counting checks)
                 */

                // Resets that value to 0
                amount_Questions_Left_On_Send = 0;

                // Iterates over all questions within the question panel
                $('#iAMA_Question_Panel').find('li').each(function () {
                    amount_Questions_Left_On_Send += 1;
                });

                // Subtract by one, because we have posted a message on reddit here
                amount_Questions_Left_On_Send -= 1;

                // $('#' + id_of_question).hide();
                // $('#' + id_of_question).remove();
                $('#' + id_of_question).fadeOut("slow", function() {
                    // Animation complete.
                });

                //noinspection JSCheckFunctionSignatures
                BootstrapDialog.show({
                    title: 'Sending data to to reddit now...',
                    message: 'Your answer is beeing uploaded to reddit right now. Please wait a few seconds..',
                    type: BootstrapDialog.TYPE_WARNING,
                    closable: false
                });

                // Triggesr the id of the question which is to be answered and the appropriate text, already stringified
                // to reddit
                $(body).trigger('Post_To_Reddit', [[[id_of_question], [JSON.stringify(data)]]]);




            });

        },

        /**
         * Appends functionality to pickup already answered question to the template button
         *
         *
         * @param {String} dom_Element the "already answered" button DOM template
         * @param {String} id_Of_Question the id of the question the "already answered" button belongs to
         * @returns {Object} dom_Element the template button which allows the user to pick an answer from the already
         * answered questions
         *
         */
        _appendOnClickListenerForAlreadyAnswered = function (dom_Element, id_Of_Question, text_Of_Selected_Question) {

            var id_of_actual_selected_thread = "";

            // Iterates over all list elements checking which has the class "thread_selected"
            //noinspection JSValidateTypes
            $("#iAMA_Thread_Overview").children('li').each(function () {
                if ($(this).hasClass("thread_selected") === true) {
                    id_of_actual_selected_thread = $(this).attr('id')
                }
            });

            //noinspection JSUnresolvedFunction
            return dom_Element.click(function () {

                // Triggers to write meta data text file
                _sendUsageMetaData("Already answered(unanswered): clicked");


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
                            body.css('cursor', 'crosshair');

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
                                body.css('cursor', 'default');

                                // Appends the clicked id to the regarding answer text box
                                //noinspection JSJQueryEfficiency
                                $('#' + id_Of_Question + '_answer_box').val("Ich habe deine Frage bereits hier beantwortet: " + $('#' + id_Of_Question + '_answer_box').val() + "\n" +
                                    "https://www.reddit.com/r/miregensburg/comments/" + id_of_actual_selected_thread + "/-/" + this.id);

                                // Whenever the click has been set, unbind that given behaviour
                                $('#iAMA_Answer_Panel').find('> li').unbind("click");

                                // Triggers to write meta data text file
                                // _sendUsageMetaData("Already answered(unanswered): selected question_id: " + id_Of_Question);
                                _sendUsageMetaData("Already answered(unanswered): selected question_text: " + text_Of_Selected_Question);

                            });

                            // Whenever ESC has been pressed revert to original view
                            $(document).on('keyup', function (e) {
                                if (e.keyCode === 27) {

                                    // Triggers to write meta data text file
                                    _sendUsageMetaData("Already answered(unanswered): pressed ESC selected question_id: " + id_Of_Question);

                                    $('#iAMA_Answer_Panel').find('> li').unbind("click");

                                    // Fade the, previously hidden, elements back
                                    top_Bar.fadeIn();
                                    thread_Overview.fadeIn();
                                    unanswered_Uber_Div.fadeIn();

                                    // Reset the view for a better behaviour
                                    answered_Uber_Div.removeClass("col-lg-12");
                                    answered_Uber_Div.addClass("col-lg-4");

                                    // Reverts the cursor behaviour back to normal
                                    body.css('cursor', 'default');
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

                            // Triggers to write meta data text file
                            _sendUsageMetaData("Already answered(unanswered): closed selection dialogue");
                        }
                    }]
                });

            });

        },

        /**
         * Builds DOM elements out of the given questions and appends them to the unanswered questions panel
         *
         * @param {event} event
         * @param {[]} data information about every question
         * Each question gets represented by an array containing following information:
         *
         * question_author = "" {String} Information about the question author
         * question_id = "" {String}    The id of the question
         * question_text = "" {String}  The question text itself
         * question_timestamp = "" {String} The (already prepared) timestamp
         * question_upvote_score = {Integer} The amount of upvotes
         * @private
         */
        _onQuestionsToDOM = function (event, data) {

            // Closes all open BootStrapDialog dialogues, whenever the correct amount of questions have been delivered
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
                    // q_p_question_id = $("<p class='pull-right text-muted small'>" + question_id + "<i class='fa fa-bookmark fa-fw'> </i> </p>"),
                    q_p_text = $("<br> <p>" + question_text + "</p>"),

                    q_answer_uber_container = $("<div class='chat-body'></div>"),
                    q_answer_text_area = $("<textarea class='custom_chat' id=" + question_id + "_answer_box" + " rows='3' placeholder='Type your answer here..'></textarea>"),

                    q_answer_buttons_uber_container = $("<div class='input-group-btn'> </div>"),
                    q_answer_buttons_template_container = $("<div class='chat_template_button'>"),
                    q_answer_buttons_template_button = $("<button class='btn btn-warning btn-sm dropdown-toggle' data-toggle='dropdown'>Already answered >> HERE << </button>"),

                    q_answer_buttons_send_container = $("<div class='chat_send_button'></div>"),
                    q_answer_buttons_send_button = $("<button class='btn btn-warning btn-sm'>Answer</button>");

                // Chains the question objects all together
                q_header.appendTo(q_uber_container);
                q_p_username.appendTo(q_header);
                q_p_posting_time.appendTo(q_header);
                q_p_score.appendTo(q_header);
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
                q_answer_buttons_template_container = _appendOnClickListenerForAlreadyAnswered(q_answer_buttons_template_container, question_id, question_text);

                // Appends an onclick listener for the send button
                //noinspection JSUnusedAssignment
                q_answer_buttons_send_button = _appendOnClickListenerForSendButton(q_answer_buttons_send_button, question_id, question_text);


                // Appends all container objects to the top level DOM <li> element
                q_image.appendTo(li_top);
                q_uber_container.appendTo(li_top);
                q_answer_uber_container.appendTo(li_top);

                // Adds that combination to the answer panel
                question_Panel.append(li_top);
            });
        },

        /**
         * Whenever the refresh button of the unanswered questions panel has been clicked gather all
         * filtering / sorting data and trigger them to the MongoDBConnector
         *
         * @private
         */
        _onRefreshClicked = function () {
            unanswered_Refresh_Button.click(function () {

                // Triggers to write meta data text file
                _sendUsageMetaData("Refresh(unanswered): clicked");

                // Defines two arrays which will contain information about the various statemenets
                // Necessary to also get information for the answered questions, due to the way the REST mechanism was
                // built
                var information_Unanswered_Questions = _getDataForUnansweredQuestionsFromWebSite(),
                    information_Answered_Questions = _getDataForAnsweredQuestionsFromWebSite(),
                    selected_Thread_ID = _getThreadID(),
                    amount_Of_Open_BootStrapDialogs = 0;

                // UIUnansweredQuestions -> UIController -> MainController -> RestController -> MongoDBConnector
                $(body).trigger('Refresh_To_UI', [[selected_Thread_ID, [information_Unanswered_Questions], [information_Answered_Questions]]]);

                // Iterates over all open BootStrapDialogWindows, making sure to not generate new windows over the old ones
                // This prevents permanent window recreation and fading effects..
                $.each(BootstrapDialog.dialogs, function () {
                    amount_Of_Open_BootStrapDialogs += 1;
                });

                // Whenever there is no BootStrapDialogue open!
                if (amount_Of_Open_BootStrapDialogs < 1) {
                    // Shows a short warning message to prevent user interaction while receiving data
                    //noinspection JSCheckFunctionSignatures
                    BootstrapDialog.show({
                        title: 'Fetching data from data base',
                        message: 'Please wait a few seconds until the newly loaded data arrives...',
                        type: BootstrapDialog.TYPE_WARNING,
                        closable: false
                    });
                }

            });
        },

        /**
         * This method contains logic for clicking 'filter' button within unanswered questions.
         * @private
         */
        _onFilterClicked = function () {

            // Appends a click listener to the generic filtering button
            $('#iAMA_Unanswered_Filtering_Opening_Button').click(function () {

                // Triggers to write meta data text file
                _sendUsageMetaData("Filtering(unanswered): Clicked filtering Button");

            });

            // Defines the click listener for tier selection
            $('#iAMA_Unanswered_Filtering_Tier_Selection').click(function () {
                unanswered_Filter_Settings_Tier = $(this).find('option:selected').text();

                // Triggers to write meta data text file
                _sendUsageMetaData("Filtering(unanswered): Filter selected: " + unanswered_Filter_Settings_Tier);

            });

            // Defines the click listener for score comparison selection
            $('#iAMA_Unanswered_Filtering_Score_Selection').click(function () {
                unanswered_Filter_Settings_Score_Compare = $(this).find('option:selected').text();

                // Triggers to write meta data text file
                _sendUsageMetaData("Filtering(unanswered): Score compare selected: " + unanswered_Filter_Settings_Score_Compare);
            });

            // Defines the concrete numeric value to be input into the score field
            //noinspection JSJQueryEfficiency
            $('#iAMA_Unanswered_Filtering_Score_Concrete').click(function () {

                // Whenever nothing has been initially selected
                if ($(this).val() === null || $(this).val() === "") {

                    // Setting the values to these high values prevents unexpected user behaviour and prevents
                    // that the original setting "eql 0" gets triggered (which would display no data..)
                    unanswered_Filter_Settings_Score_Compare = "grt";
                    unanswered_Filter_Settings_Score_Value = "-9999999";

                } else {
                    unanswered_Filter_Settings_Score_Value = $(this).val();

                    // Triggers to write meta data text file
                    _sendUsageMetaData("Filtering(unanswered): Score concrete input: " + unanswered_Filter_Settings_Score_Value);
                }

            });

            // Whenever the value input changes it will be written down into a text file
            //noinspection JSJQueryEfficiency
            $('#iAMA_Unanswered_Filtering_Score_Concrete').on('input', function () {

                // Triggers to write meta data text file
                _sendUsageMetaData("Filtering(unanswered): Score concrete input: " + $('#iAMA_Unanswered_Filtering_Score_Concrete').val());

            });

            // Defines the reset button for filtering methods
            $('#iAMA_Unanswered_Filtering_Reset').click(function () {

                // Triggers to write meta data text file
                _sendUsageMetaData("Filtering(unanswered): Reset");

                // Reset the values within the code to null here
                unanswered_Filter_Settings_Tier = null;
                unanswered_Filter_Settings_Score_Compare = null;
                unanswered_Filter_Settings_Score_Value = null;

                // Reset the frontend changes previously made
                $('#iAMA_Unanswered_Filtering_Tier_Selection').val("all");
                $('#iAMA_Unanswered_Filtering_Score_Selection').val("eql");
                $('#iAMA_Unanswered_Filtering_Score_Concrete').val(null);

            });

            // Whenever the filtering dropdown menu gets closed protocol that
            $('#iAMA_Unanswered_Filtering_Close_Dropdown').click(function () {

                // Triggers to write meta data text file
                _sendUsageMetaData("Filtering(unanswered): Closed Dropdown");
            });

        },

        /**
         * Whenever the sorting button on the unanswered questions panel has been clicked, the appropriate selected
         * element will be selected and then highlighted
         * @private
         */
        _onSortingClicked = function () {

            // Defines the click listener for the generic sorting button
            $('#iAMA_Unanswered_Sorting_Opening_Button').click(function () {

                // Triggers to write meta data text file
                _sendUsageMetaData("Sorting(unanswered): Clicked sorting Button");

            });


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

                    // Triggers to write meta data text file
                    _sendUsageMetaData("Sorting(unanswered): selected: " + text_Of_Clicked_Element);

                    if (text_Of_Clicked_Element !== "Close dropdown") {
                        unanswered_Sorting_Settings_Type = text_Of_Clicked_Element;
                    }
                })
            })
        },

        /**
         * Whenever the upload of a comment to reddit was successful this function will be executed, which
         * closes all open BootStrapDialog windows and fakes a refresh click for the unanswered question panel
         * @private
         */
        _fakeClickRefreshButton = function () {

            // Fake clicks the refresh button to trigger retrieval of new data
            unanswered_Refresh_Button.click();

        },

        /**
         * Puts the thread to sleep, to not flood the REST Service whenever the returned amount of questions is
         * incorrect. It can be incorrect at sometimes when the reddit server does not response that fast...
         *
         * @param milliseconds {int} the amount of milliseconds the webpage should be delayed
         * @private
         */
        _sleepNow = function (milliseconds) {
            var start = new Date().getTime();
            for (var i = 0; i < 1e7; i++) {
                if ((new Date().getTime() - start) > milliseconds) {
                    break;
                }
            }
        },

        /**
         * Checks whether the returned amount of questions is correct.
         * This circumvents a bug due to the reddit api limitation. Because, whenever you post a comment via my tool
         * on reddit, our tool immediately tries to recrawl thread and author data.
         * Because the reddit API is not that fast ---> old data will be returned..
         * This could disturb the user, because he would see questions he has already answered..
         * Therefore, before displaying questions, we check if the amount of questions is the same with the amount it
         * should be after the last comment had been posted on reddit.
         *
         * @param {event} event
         * @param {[]} data information about every question
         * Each question gets represented by an array containing following information:
         *
         * question_author = "" {String} Information about the question author
         * question_id = "" {String}    The id of the question
         * question_text = "" {String}  The question text itself
         * question_timestamp = "" {String} The (already prepared) timestamp
         * question_upvote_score = {Integer} The amount of upvotes
         * @private
         */
        _checkIfQuestionRetrievalIsOk = function (event, data) {
            // var temp_Question_Checker = 0;
            //
            // // Iterates over all questions within the received data array
            // $.each(data, function () {
            //     temp_Question_Checker += 1;
            // });
            //
            // // Whenever the amount of received questions is the same as the previously counted amount
            // if ((temp_Question_Checker === amount_Questions_Left_On_Send) ||
            //     (amount_Questions_Left_On_Send === null)) {
            //
            //     // Give the questions to that method and display them on the page!
                _onQuestionsToDOM(event, data);
            //
            //     // By switching between the threads resetting it to null is necessary, otherwise there would be an
            //     // unlimited refresh
            //     amount_Questions_Left_On_Send = null;
            //
            //     // Whenever we have received old data [old questions which have already been answered] request them anew
            // } else {
            //     // Because this else tree gets executed like a while loop (I do not know why) I have included a
            //     // 15 seconds pause to not flood the FLASK REST-Service... But it uses between 5 to 15 seconds randomly.
            //     console.log("BIN in While loop hier !!!");
            //     _sleepNow(30000);
            //     _fakeClickRefreshButton();
            // }

        },

        /**
         * Whenever metadata needs to be written down into a text file
         * @param given_usage_text contains information about the usage context
         * @private
         */
        _sendUsageMetaData = function (given_usage_text) {
            var data_to_send = [JSON.stringify({"text": given_usage_text})];

            // Here -> UIController -> MainController -> RestController -> MongoDBConnector
            $(body).trigger('MetaData_To_File', data_to_send);
        },

        /**
         * Initializes all UI elements to retrieve data from
         *
         * @private
         */
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

        /**
         * Initializes all trigger listeners this class should use
         * @private
         */
        _initEvents = function () {

            // MongoDBConnector -> RestController -> MainController -> UIController -> UIUnansweredQuestions
            $(body).on('unanswered_Questions_To_DOM', _checkIfQuestionRetrievalIsOk);

            // MongoDBConnector -> RestController -> MainController -> UIController -> UIUnansweredQuestions
            $(body).on('UI_To_Unanswered_Questions_Post_Successful', _fakeClickRefreshButton);
        };

    /**
     * Initializes this UIUnansweredQuestions Panel
     *
     * @returns {object} UIUnansweredQuestions object
     */
    that.init = function () {
        _initUI();
        _initEvents();
    };
    return that;
}();