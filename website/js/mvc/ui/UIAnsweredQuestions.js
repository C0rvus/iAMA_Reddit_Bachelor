// Source: https://api.jquery.com/each/

IAMA_Extension.UIAnsweredQuestions = function () {
    var that = {},
        body,

        unanswered_Q = null,
        questioners = null,
        upvotes = null,
        new_Q_Every_X = null,
        duration_D = null,

    // Assigns necessary thread data to the top panel
        _onAnswersToDOM = function (event, data) {
            console.log("CORRRRRRRRRRRRRRRRRRECT");
        },

    // References UI elements in here
        _initUI = function () {

            body = $(document.body);

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