/**
 *  @class UIAnswered Questions
 *  This class handles the behaviour of the questions within the answered questions panel, which are the abilities
 *  - to select a answer from the "already answered" button within the unanswered questions panel
 *  - to sort the questions
 *  - to filter the questions
 *  Sources used within this class:
 *  1.(22.06.2016 @ 17:32) - http://stackoverflow.com/questions/759887/how-to-create-a-dom-node-as-an-object
 *  2.(24.06.2016 @ 16:15) - http://stackoverflow.com/questions/5076466/javascript-replace-n-with-br
 */

IAMA_Extension.UIAnsweredQuestions = function () {
    var that = {},
        body,

        answer_Panel = null,

        answered_Filter_Button = null,
        answered_Sorting_Button = null,
        answered_Refresh_Button = null,

        answered_Filter_Settings_Tier = null,
        answered_Filter_Settings_Score_Compare = null,
        answered_Filter_Settings_Score_Value = null,
        answered_Sorting_Settings_Type = null,
        answered_Sorting_Settings_Asc_Des = null,

        unanswered_Filter_Settings_Tier = null,
        unanswered_Filter_Settings_Score_Compare = null,
        unanswered_Filter_Settings_Score_Value = null,
        unanswered_Sorting_Settings_Type = null,
        unanswered_Sorting_Settings_Asc_Des = null,
        
        /**
         * Retrieves the thread id of the thread which is actually in work.
         * This is necessary for correct REST calling behaviour.
         *
         * @returns id_Of_Actual_Selected_Thread {String} the ID of the acutally selected thread
         * from the left panel
         *
         * @private
         */
        _getThreadID = function () {

            var id_Of_Actual_Selected_Thread = null;

            // Iterates over all threads within the left thread panel
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


            // Correctly converts the "Settings Type" value into REST compatible information
            switch(sorting_Selection_Answered_Found) {

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
            if ($('#iAMA_Unanswered_Filtering_Score_Concrete').val() === "" || ($('#iAMA_Unanswered_Filtering_Score_Concrete').val() === null )) {
                unanswered_Filter_Settings_Score_Value = -99999;
                unanswered_Filter_Settings_Score_Compare = "grt";
            } else {
                unanswered_Filter_Settings_Score_Value = $('#iAMA_Unanswered_Filtering_Score_Concrete').val();
            }

            // Correctly converts the "Settings Type" value into REST compatible information
            switch(unanswered_Sorting_Settings_Type) {
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
         * Handles the behaviour of the refresh button for the answered questions..
         *
         * @private
         */
        _onRefreshClicked = function () {
            answered_Refresh_Button.click(function () {

                // Triggers to write meta data text file
                _sendUsageMetaData("Refresh(answered): clicked");

                // Defines two arrays which will contain information about the various statemenets
                // Necessary to also get information for the answered questions, due to the way the REST mechanism was
                // built
                var information_Unanswered_Questions = _getDataForUnansweredQuestionsFromWebSite(),
                    information_Answered_Questions = _getDataForAnsweredQuestionsFromWebSite(),
                    selected_Thread_ID = _getThreadID();


                $(body).trigger('Refresh_To_UI',[[selected_Thread_ID, [information_Unanswered_Questions],[information_Answered_Questions]]]);

                // Shows a short warning message to prevent user interaction while receiving data
                //noinspection JSCheckFunctionSignatures
                BootstrapDialog.show({
                    title: 'Fetching data from data base',
                    message: 'Please wait a few seconds until the newly loaded data arrives...',
                    type: BootstrapDialog.TYPE_WARNING,
                    closable: false});

            });
        },

        /**
         * Whenever the sorting button on the answered questions panel has been clicked, the appropriate selected
         * element will be selected and then highlighted
         * @private
         */
        _onSortingClicked = function () {

            // Defines the click listener for the generic sorting button
            $('#iAMA_Answered_Sorting_Opening_Button').click(function () {

                // Triggers to write meta data text file
                _sendUsageMetaData("Sorting(answered): Clicked sorting Button");

            });

            // Appends a click listener for every dom element
            answered_Sorting_Button.find("li").each(function () {
                $(this).click(function () {

                    // 1st. Remove the class "sorting_Selected" from every element
                    // 2nd. Add that class to the selected element
                    answered_Sorting_Button.find("li").each(function () {
                        $(this).removeClass("sorting_Selected");
                    });

                    $(this).addClass("sorting_Selected");

                    var text_Of_Clicked_Element = $.trim($(this).text());

                    // Triggers to write meta data text file
                    _sendUsageMetaData("Sorting(answered): selected: " + text_Of_Clicked_Element);

                    if (text_Of_Clicked_Element !== "Close dropdown") {
                        answered_Sorting_Settings_Type = text_Of_Clicked_Element;
                    }
                })
            })
        },

        /**
         * This method contains logic for clicking 'filter' button within answered questions.
         * @private
         */
        _onFilterClicked = function () {

            // Appends a click listener to the generic filtering button
            $('#iAMA_Answered_Filtering_Opening_Button').click(function () {

                // Triggers to write meta data text file
                _sendUsageMetaData("Filtering(answered): Clicked filtering Button");

            });

            // Defines the click listener for tier selection
            $('#iAMA_Answered_Filtering_Tier_Selection').click(function () {
                answered_Filter_Settings_Tier = $(this).find('option:selected').text();

                // Triggers to write meta data text file
                _sendUsageMetaData("Filtering(answered): Filter selected: " + answered_Filter_Settings_Tier);
            });

            // Defines the click listener for score comparison selection
            $('#iAMA_Answered_Filtering_Score_Selection').click(function () {
                answered_Filter_Settings_Score_Compare = $(this).find('option:selected').text();

                // Triggers to write meta data text file
                _sendUsageMetaData("Filtering(answered): Score compare selected: " + answered_Filter_Settings_Score_Compare);
            });

            // Defines the concrete numeric value to be input into the score field
            $('#iAMA_Answered_Filtering_Score_Concrete').click(function () {
                // Whenever nothing has been initially selected
                if ($(this).val() === null || $(this).val() === "") {
                    // Setting the values to these high values prevents unexpected user behaviour and prevents
                    // that the original setting "eql 0" gets triggered (which will display no data..)

                    answered_Filter_Settings_Score_Compare = "grt";
                    answered_Filter_Settings_Score_Value = "-9999999";

                } else {
                    answered_Filter_Settings_Score_Value = $(this).val();

                    // Triggers to write meta data text file
                    _sendUsageMetaData("Filtering(answered): Score concrete input: " + answered_Filter_Settings_Score_Value);
                }
            });

            // Whenever the value input changes it will be written down into a text file
            //noinspection JSJQueryEfficiency
            $('#iAMA_Answered_Filtering_Score_Concrete').on('input', function () {

                // Triggers to write meta data text file
                _sendUsageMetaData("Filtering(answered): Score concrete input: " + $('#iAMA_Answered_Filtering_Score_Concrete').val());

            });

            
            // Defines the reset button for filtering methods
            $('#iAMA_Answered_Filtering_Reset').click(function () {

                // Triggers to write meta data text file
                _sendUsageMetaData("Filtering(answered): Reset");

                // Reset the values within the code to null here
                answered_Filter_Settings_Tier = null;
                answered_Filter_Settings_Score_Compare = null;
                answered_Filter_Settings_Score_Value = null;

                // Reset the frontend changes previously made
                $('#iAMA_Answered_Filtering_Tier_Selection').val("all");
                $('#iAMA_Answered_Filtering_Score_Selection').val("eql");
                $('#iAMA_Answered_Filtering_Score_Concrete').val(null);

            });

            // Whenever the filtering dropdown menu gets closed protocol that
            $('#iAMA_Answered_Filtering_Close_Dropdown').click(function () {

                // Triggers to write meta data text file
                _sendUsageMetaData("Filtering(answered): Closed Dropdown");
            });

        },

        /**
         * Builds DOM elements out of the given Q&A combination and appends them to the answered questions panel
         *
         * @param {event} event which causes this method to fire
         * @param {[]} data array containing following information about the answered questions with answers
         * 
         *  "question_id":
         *  "question_author":
         *  "question_timestamp":
         *  "question_upvote_score":
         *  "question_text":
         *  "answer_id":
         *  "answer_timestamp":
         *  "answer_upvote_score":
         *  "answer_text":
         *  
         * @private
         */
        _onAnswersToDOM = function (event, data) {

            // Removes the first example answer here
            $("#iAMA_Answer_Panel").find("> li" ).remove();
            $("#iAMA_Answer_Panel").find("> hr" ).remove();

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
                    question_upvote_score = value['question_upvote_score'];

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


                // Defining DOM Elements here
                var separator_q_n_a = $("<hr class='ruler-answered-questions'>"),

                    li_top = $("<li class='left clearfix' id='" + answer_id + "'" + "> </li>"),

                    // Building question containers here
                    q_uber_container = $("<div class='left clearfix chat-message-question'></div>"),
                    q_header = $("<div class='header'></div>"),

                    // Question elements are defined here
                    q_p_username = $("<p class='pull-left primary-font strong'>" + question_author + "</p>"),
                    q_p_posting_time = $("<p class='pull-right text-muted small chat-answered-questions'>" + question_timestamp + "<i class='fa fa-clock-o fa-fw'></i> </p> <br>"),
                    q_p_score = $("<p class='pull-right text-muted small chat-answered-questions'>" + question_upvote_score + "<i class='fa fa-bullseye fa-fw'> </i> </p> <br>"),
                    q_p_text = $("<p class='chat-alignment-left'>" + question_text + "</p>"),

                    a_uber_container = $("<div class='right clearfix chat-message-answer'></div>"),
                    a_header = $("<div class='header'></div>"),
                    a_p_username = $("<p class='pull-right primary-font strong'>" + "You" + "</p><br>"),
                    a_p_posting_time = $("<p class='pull-left text-muted small chat-answered-questions'><i class='fa fa-clock-o fa-fw'></i>" + answer_timestamp + "</p><br>"),
                    a_p_score = $("<p class='pull-left text-muted small chat-answered-questions'><i class='fa fa-bullseye fa-fw'></i>" + answer_upvote_score + "</p><br>"),
                    a_p_text = $("<p class='chat-alignment-right'>" + answer_text + "</p>");

                // Chains the question objects all together
                q_header.appendTo(q_uber_container);
                q_p_username.appendTo(q_header);
                q_p_posting_time.appendTo(q_header);
                q_p_score.appendTo(q_header);
                q_p_text.appendTo(q_header);

                // Chains the answer objects all together
                a_header.appendTo(a_uber_container);
                a_p_username.appendTo(a_header);
                a_p_posting_time.appendTo(a_header);
                a_p_score.appendTo(a_header);
                a_p_text.appendTo(a_header);

                // Appends all container objects to the top level DOM <li> element
                q_uber_container.appendTo(li_top);
                a_uber_container.appendTo(li_top);

                // Adds that combination to the answer panel
                answer_Panel.append(li_top);
                separator_q_n_a.appendTo(answer_Panel);
            });
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
            answer_Panel = $('#iAMA_Answer_Panel');

            answered_Filter_Button = $('#iAMA_Answered_Filter');
            _onFilterClicked();

            answered_Sorting_Button = $('#iAMA_Answered_Sorting');
            _onSortingClicked();

            answered_Refresh_Button = $('#iAMA_Answered_Refresh');
            _onRefreshClicked();
        },

        /**
         * Initializes all trigger listeners this class should use
         * @private
         */
        _initEvents = function () {
            $(body).on('answered_Questions_To_DOM', _onAnswersToDOM);
        };

    /**
     * Initializes this UIAnsweredQuestions Panel
     *
     * @returns {object} UIAnsweredQuestions object
     */
    that.init = function () {
        _initUI();
        _initEvents();
    };
    return that;
}();