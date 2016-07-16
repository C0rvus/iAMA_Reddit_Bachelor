/**
 * @class UIThreadOverview
 * This class handles all the information about all threads the author created on the left side of the window
 *  -
 *  Sources used within this class:
 *  1.(11.06.2016 @ 11:15) - https://api.jquery.com/each/
 */
IAMA_Extension.UIThreadOverview = function () {
    var that = {},
        body,
        overview_Container = null,
        
        /**
         * Assigns an individual click listener per thread id ( <li> DOM - Element within ThreadOverview )
         * The click listener assigns the class "thread_selected" to show the user the active thread
         * And it does a REST-Call to load data from that thread into the page
         * @private
         */
        _assignIndividualClickListener = function () {

            // Iterates over every thread possibility adding unique click listener
            //noinspection JSValidateTypes
            $(overview_Container).children('li').each(function () {

                // Click listener for every iterated item
                $(this).click(function () {

                    // Triggers to write meta data text file
                    _sendUsageMetaData("ThreadOverview: clicked '" + "'" + $(this).attr('id'));

                    // Removes "thread_selected" - class from every element
                    (overview_Container).children('li').each(function () {
                        $(this).removeClass("thread_selected");
                    });

                    // Assigns the "thread_selected" - class to the clicked element
                    // And additionally does a REST-CALL do load up some information
                    if ($(this).hasClass("thread_selected") !== true) {

                        $(this).addClass("thread_selected");

                        // Triggers event -> UIController -> MainController -> RestController ->...
                        // This will load thread specific data to the website
                        $(this).trigger('thread_Clicked_To_Load', [[$(this).attr('id'), [null], [null]]]);

                        // Shows a short warning message to prevent user interaction while receiving data
                        //noinspection JSCheckFunctionSignatures
                        BootstrapDialog.show({
                            title: 'Fetching data from data base',
                            message: 'Please wait a few seconds until the newly loaded data arrives...',
                            type: BootstrapDialog.TYPE_WARNING,
                            closable: false});
                    }

                });

            });

        },

        /**
         * Assigns an initial thread data to the webpage.
         * Whenever the webpage gets fired up, this method will be executed assigning data to the left side of the
         * panel
         *
         * @params {event} event causes this method to fire
         * @params {[]} data consists of following values, containing information about the actual selected thread
         *      amount_answered =  {Integer}
         *      amount_of_questions =  {Integer}
         *      duration = "" {String}
         *      thread_id = "" {String}
         *      title = "" {String}
         * @private
         *
         */
        _assignThreadDataToPanel_Initial = function (event, data) {
            overview_Container.find("> li").remove();
            // Iterates over every array within the received data object
            $.each(data['threads_information'], function (key, value) {

                var title = value['title'],
                    amount_answered = value['amount_answered'],
                    amount_of_questions = value['amount_of_questions'],
                    duration = value['duration'],
                    thread_id = value['thread_id'];

                var t_uber_li_element = $("<li id='" + thread_id + "'>" + "</li>"),
                    thread_title = $("<i class='fa fa-th fa-fw'></i>" + title + "<br>"),
                    answer_ratio = $("<i class='fa fa-question-circle fa-fw'></i>" + amount_answered + "/" + amount_of_questions + " answered" + "<br>"),
                    thread_duration = $("<i class='fa fa-clock-o fa-fw'></i>" + duration + "<br>");

                thread_title.appendTo(t_uber_li_element);
                answer_ratio.appendTo(t_uber_li_element);
                thread_duration.appendTo(t_uber_li_element);

                t_uber_li_element.appendTo(overview_Container);
                
            });

            // Reassign click listener after filling thread panel data on the left side of the window panel
            _assignIndividualClickListener();
            // Now fake click the first entry to start the iAMA experience
            $("#iAMA_Thread_Overview").find("li").first().click();

        },

        /**
         * Assigns thread data to the left panel, whenever a thread has been selected
         *
         * @params {event} event causes this method to fire
         * @params {[]} data consists of following values, containing information about the actual selected thread
         *      thread_title =  {Integer}
         *      thread_amount_answered_questions =  {Integer}
         *      thread_amount_questions = "" {Integer}
         *      thread_duration = "" {Integer}
         *      thread_id = "" {String}
         * @private
         *
         */
        _assignThreadDataToPanel = function (event, data) {

            $.each(overview_Container.find("> li"), function () {

                // Updates the subelements of the actually seleted thread (on the left side panel)
                if ($(this).hasClass("thread_selected") === true) {

                    $(this).empty();

                    var title = data['thread_title'],
                        amount_answered = data['thread_amount_answered_questions'],
                        amount_of_questions = data['thread_amount_questions'],
                        duration = data['thread_duration'],
                        thread_id = data['thread_id'];

                    var thread_title = $("<i class='fa fa-th fa-fw'></i>" + title + "<br>"),
                        answer_ratio = $("<i class='fa fa-question-circle fa-fw'></i>" + amount_answered + "/" + amount_of_questions + " answered" + "<br>"),
                        thread_duration = $("<i class='fa fa-clock-o fa-fw'></i>" + duration + " days ago" + "<br>");

                    thread_title.appendTo($(this));
                    answer_ratio.appendTo($(this));
                    thread_duration.appendTo($(this));

                }
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
         * Initializes all UI elements to get / receive data from
         * @private
         */
        _initUI = function () {
            overview_Container = $("#iAMA_Thread_Overview");
            body = $(document.body);

        },

        /**
         * Initializes all trigger listeners this class should use
         * @private
         */
        _initEvents = function () {
            $(body).on('UI_To_Thread_Overview', _assignThreadDataToPanel);
            $(body).on('UI_To_Thread_Overview_Initial', _assignThreadDataToPanel_Initial);
        };

    /**
     * Initializes this UIThreadOverview class
     *
     * @returns {object} UIThreadOverview object
     */
    that.init = function () {
        _initUI();
        _initEvents();
    };
    return that;
}();