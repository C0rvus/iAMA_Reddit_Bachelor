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

        unanswered_Q = null,
        questioners = null,
        upvotes = null,
        new_Q_Every_X = null,
        duration_D = null,
        //TODO: Daten hier genau angeben
        /**
         * Assigns information from the given "data" element to appropriate UI elements
         * @param {event} event kind of event which is to be triggered
         * @param {??} data data which is to be triggered
         */
        _onTopToDOM = function (event, data) {

            var thread_amount_unanswered_questions = data['thread_amount_unanswered_questions'],
                thread_new_question_every_x_sec = data['thread_new_question_every_x_sec'],
                thread_duration = data['thread_duration'],
                thread_downs = data['thread_downs'],
                thread_ups = data['thread_ups'],
                thread_amount_questioners = data['thread_amount_questioners'];

            unanswered_Q.text(thread_amount_unanswered_questions);
            questioners.text(thread_amount_questioners);
            upvotes.text(thread_ups);
            new_Q_Every_X.text(thread_new_question_every_x_sec);
            duration_D.text(thread_duration);
        },

    /**
     * Refers to the single UI elements within the topbar
     */
        _initUI = function () {

            unanswered_Q = $("#iAMA_Top_Unanswered_Q");
            questioners = $("#iAMA_Top_Amount_Q");
            upvotes = $("#iAMA_Top_Upvotes");
            new_Q_Every_X = $("#iAMA_Top_New_Q_Every_X");
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