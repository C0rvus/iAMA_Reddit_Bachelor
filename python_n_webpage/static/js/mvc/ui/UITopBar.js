/**
 *  @class UITopBar
 *  The UITopbar is necessary to display important information about the actually selected thread
 *  -
 *  Sources used within this class:
 *  1. (15.06.2016 @ 13:15) - https://api.jquery.com/each/
  */
IAMA_Extension.UITopBar = function () {
    var that = {},
        body,

        open_Q = null,
        questioners = null,
        votes = null,
        new_Q_Every_X = null,
        new_A_Every_X = null,
        duration_D = null,
        /**
         * Assigns information from the given "data" element to appropriate UI elements
         * @param {event} event kind of event which is to be triggered
         * @param {[]} data contains some stats data about the clicked thread
         *  thread_amount_questioners = {Integer}
         *  thread_amount_unanswered_questions = {Integer}
         *  thread_downs = {Integer}
         *  thread_duration = {Integer}
         *  thread_new_question_every_x_sec = {Integer}
         *  thread_ups = {Integer}
         */
        _onTopToDOM = function (event, data) {

            var thread_amount_unanswered_questions = data['thread_amount_unanswered_questions'],
                thread_amount_questions = data['thread_amount_questions'],
                thread_new_question_every_x = data['thread_new_question_per_hour'],
                thread_new_answer_every_x = data['thread_new_answer_per_hour'],
                thread_duration = data['thread_duration'],
                thread_downs = data['thread_downs'],
                thread_ups = data['thread_ups'],
                thread_amount_questioners = data['thread_amount_questioners'];

            open_Q.text(thread_amount_questions - thread_amount_unanswered_questions + " / " + thread_amount_questions);
            questioners.text(thread_amount_questioners);

            // Because the up- / downvotes element is rather complex we have to create it dynamically here
            var votes_dom_element = $("<i class='fa fa-thumbs-o-up'></i> " + thread_ups + " / " + thread_downs + " <i class='fa fa-thumbs-o-down'></i>");
            votes.empty();
            votes.append(votes_dom_element);

            var answers_per_hour_dom_element = $("<i class='fa fa-check'></i> "),
                questions_per_hour_dom_element = $("<i class='fa fa-question'></i> ");

            // Empty the "answers per hours" element
            //noinspection JSJQueryEfficiency
            $('#iAMA_Top_New_A_Every_X').empty();
            //noinspection JSJQueryEfficiency
            answers_per_hour_dom_element.appendTo($('#iAMA_Top_New_A_Every_X'));
            //noinspection JSJQueryEfficiency
            $('#iAMA_Top_New_A_Every_X').append(" " + thread_new_answer_every_x);

            // Empty the "questions per hours" element
            //noinspection JSJQueryEfficiency
            $('#iAMA_Top_New_Q_Every_X').empty();
            //noinspection JSJQueryEfficiency
            questions_per_hour_dom_element.appendTo($('#iAMA_Top_New_Q_Every_X'));
            //noinspection JSJQueryEfficiency
            $('#iAMA_Top_New_Q_Every_X').append(" " + thread_new_question_every_x);

            duration_D.text(thread_duration);
        },

    /**
     * Refers to the single UI elements within the topbar
     */
        _initUI = function () {

            open_Q = $("#iAMA_Top_Open_Q");
            questioners = $("#iAMA_Top_Amount_Q");
            votes = $("#iAMA_Votes_Score");
            new_Q_Every_X = $("#iAMA_Top_New_Q_Every_X");
            new_A_Every_X = $("#iAMA_Top_New_A_Every_X");
            duration_D = $("#iAMA_Top_Duration_D");

            body = $(document.body);

        },

        /**
         * Initializes all "trigger" events the UITopBar should listen to
         */
        _initEvents = function () {
            $(body).on('top_Data_To_DOM', _onTopToDOM);
        };

    /**
     * Initializes the UITopBar class itself
     *
     * @returns {object} UITopBar
     */
    that.init = function () {
        _initUI();
        _initEvents();
    };
    return that;
}();