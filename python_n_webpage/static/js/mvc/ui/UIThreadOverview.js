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


                        // $(this).trigger('thread_Clicked_To_Load', $(this).attr('id'));
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

    // References UI elements in here
        _initUI = function () {
            overview_Container = $("#iAMA_Thread_Overview");
            body = $(document.body);

        },

    // References misc listeners here
        _initListeners = function () {
            _assignIndividualClickListener();
        };


    that.init = function () {
        _initUI();
        _initListeners();
    };
    return that;
}();