// Source: http://stackoverflow.com/questions/759887/how-to-create-a-dom-node-as-an-object
// http://stackoverflow.com/questions/5076466/javascript-replace-n-with-br

IAMA_Extension.UIGenericMethods = function () {
    var that = {},

        body,

    // References UI elements in here
        _initUI = function () {

            body = $(document.body);

        },

    // Expands the (un)answered panels regarding to the screen resolution used.
        _initResizeViewDependingOnScreenRes = function () {
            var setElementHeight = function () {
                // 225 has been manually chosen here
                // The choice was necessary because the template is a little bit inconsistent to use
                var height = $(window).height() - 230;
                $('.chat-panel .panel-body').css('height', (height));
            };

            $(window).on("resize", function () {
                setElementHeight();
            }).resize();
        },

    // The ability to not close the drop down menu whenever an option has been clicked
        _initLetDropDownStay = function () {
            $('.dropdown-menu input, .dropdown-menu label, .dropdown-menu select').click(function (e) {
                e.stopPropagation();
            });
        };


    that.init = function () {
        _initUI();
        _initResizeViewDependingOnScreenRes();
        _initLetDropDownStay();
    };
    return that;
}();