// Source: https://api.jquery.com/each/

IAMA_Extension.UIThreadOverview = function () {
    var that = {},
        body,
        overview_Container = null,

        // Assigns an individual click listener per thread id ( <li> DOM - Element within ThreadOverciew )
        // The click listener assigns the class "thread_selected" to show the user the active thread
        // And it does a REST-Call to load data from that thread into the page
        _assignIndividualClickListener = function () {

            // Iterates over every thread possibility adding unique click listener
            $(overview_Container).children('li').each(function () {

                // Click listener for every iterated item
                $(this).click(function () {

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
                        //TODO: Hier kommentieren, dass man zwei nuller arrays braucht, wegen der einen _getThreadDataFromDB methode
                        $(this).trigger('thread_Clicked_To_Load', [[$(this).attr('id'), [null], [null]]]);

                        // Shows a short warning message to prevent user interaction while receiving data
                        BootstrapDialog.show({
                            title: 'Fetching data from data base',
                            message: 'Please wait a few seconds until the newly loaded data arrives...',
                            type: BootstrapDialog.TYPE_WARNING,
                            closable: false});
                    }

                });

            });

        },

        // Assigns initial thread data overview to panel
        _assignThreadDataToPanel = function (event, data) {
            console.log("_assignThreadDataToPanel", [data]);
            console.log("Initial CALLLING !!!");
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
                    thread_duration = $("<i class='fa fa-clock-o fa-fw'></i>" + duration + "<br>"),
                    id_of_thread = $("<i class='fa fa-tag fa-fw'></i>" + thread_id + "<br>");

                thread_title.appendTo(t_uber_li_element);
                answer_ratio.appendTo(t_uber_li_element);
                thread_duration.appendTo(t_uber_li_element);
                id_of_thread.appendTo(t_uber_li_element);

                t_uber_li_element.appendTo(overview_Container);


            });

            _assignIndividualClickListener();
            // Todo: Den ersten Listeneintrag aktiv anklicken per jQuery - macht das Sinn ?
            $("#iAMA_Thread_Overview").find("li").first().click();
            // $(this).trigger('thread_Clicked_To_Load', [[$(this).attr('id'), [null], [null]]]);


        },

    // References UI elements in here
        _initUI = function () {
            overview_Container = $("#iAMA_Thread_Overview");
            body = $(document.body);

        },

    // References event listeners here
        _initEvents = function () {
            $(body).on('UI_To_Thread_Overview_Initial', _assignThreadDataToPanel);
        };


    that.init = function () {
        _initUI();
        _initEvents();
    };
    return that;
}();