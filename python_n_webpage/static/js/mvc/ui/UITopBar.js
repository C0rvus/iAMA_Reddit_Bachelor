// Source: https://api.jquery.com/each/

IAMA_Extension.UITopBar = function () {
    var that = {},
        body,

        unanswered_Q = null,
        questioners = null,
        upvotes = null,
        new_Q_Every_X = null,
        duration_D = null,

        // Assigns necessary thread data to the top panel
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

    // References UI elements in here
        _initUI = function () {

            unanswered_Q = $("#iAMA_Top_Unanswered_Q");
            questioners = $("#iAMA_Top_Amount_Q");
            upvotes = $("#iAMA_Top_Upvotes");
            new_Q_Every_X = $("#iAMA_Top_New_Q_Every_X");
            duration_D = $("#iAMA_Top_Duration_D");

            body = $(document.body);

        },

    // References misc listeners here
        _initEvents = function () {
            $(body).on('top_Data_To_DOM', _onTopToDOM);

        };


    that.init = function () {
        _initUI();
        _initEvents();
    };
    return that;
}();