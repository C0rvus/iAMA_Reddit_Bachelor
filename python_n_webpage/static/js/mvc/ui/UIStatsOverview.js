/**
 * @class UIStatsOverview
 * This class handles the behaviour of the statistics panel on the left side of the window
 */
IAMA_Extension.UIStatsOverview = function () {
    var that = {},
        body,
        statsPanel,
        stats_amount_answered_q,
        stats_q_score,
        stats_react_time,
        stats_new_q_every_x_sec,
        stats_amount_q_tier_1,
        stats_amount_q_tier_x,
        stats_best_q_score,

        /**
         * Appends data, receveived from the statistics data object to the panel of the left side of the webpage
         * @param {event} event
         * @param {[]} data contains information about the actual selected thread (left panel). It consists of following
         * values:
         *
         *  "thread_amount_unanswered_questions"
         *  "thread_average_question_score"
         *  "thread_new_question_every_x_sec"
         *  "thread_amount_questions_tier_1"
         *  "thread_amount_questions"
         *  "thread_amount_questions_tier_x"
         *  "thread_question_top_score"
         *  "thread_time_stamp_last_question"
         *  "thread_average_reaction_time_host"
         *  
         * @private
         * //TODO: stats to dom überarbeiten
         */
        _onStatsToDOM = function (event, data) {
            var thread_amount_questions_tier_x = data['thread_amount_questions_tier_x'],
                thread_average_question_score = data['thread_average_question_score'],
                thread_average_reaction_time_host = data['thread_average_reaction_time_host'],
                thread_amount_questions_tier_1 = data['thread_amount_questions_tier_1'],
                thread_new_question_every_x_sec = data['thread_new_question_every_x_sec'],
                thread_question_top_score = data['thread_question_top_score'],
                thread_amount_questions = data['thread_amount_questions'],
                thread_amount_unanswered_questions = data['thread_amount_unanswered_questions'],
                thread_time_stamp_last_question = data['thread_time_stamp_last_question'];

            stats_amount_answered_q.text(thread_amount_questions - thread_amount_unanswered_questions + " / " + thread_amount_questions);
            stats_q_score.text(thread_average_question_score);
            stats_react_time.text(thread_average_reaction_time_host + " s");
            stats_new_q_every_x_sec.text(thread_new_question_every_x_sec + " s");
            stats_amount_q_tier_1.text(thread_amount_questions_tier_1);
            stats_amount_q_tier_x.text(thread_amount_questions_tier_x);
            stats_best_q_score.text(thread_question_top_score);
        },

        /**
         * Initializes all UI elements to put data into
         * @private
         */
        _initUI = function () {
            body = $(document.body);

            statsPanel = $('#iAMA_Stats');

            stats_amount_answered_q = $('#iAMA_Stats_Answered_Q');
            stats_q_score = $('#iAMA_Stats_Q_Score');
            stats_react_time = $('#iAMA_Stats_React_Time');
            stats_new_q_every_x_sec = $('#iAMA_Stats_New_Q');
            stats_amount_q_tier_1 = $('#iAMA_Stats_Amount_Q_Tier_1');
            stats_amount_q_tier_x = $('#iAMA_Stats_Amount_Q_Tier_X');
            stats_best_q_score = $('#iAMA_Stats_Best_Q_Score');
        },

        /**
         * Initializes all trigger listeners this class should use
         * @private
         */
        _initEvents = function () {
            $(body).on('stats_Data_To_DOM', _onStatsToDOM);

        };

    /**
     * Initializes this UIStatsOverview class
     *
     * @returns {object} UIStatsOverview object
     */
    that.init = function () {
        _initUI();
        _initEvents();
    };
    return that;
}();