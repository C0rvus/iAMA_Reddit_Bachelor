/**
 * @class UIGenericMethods
 * This class contains several, generic methods for correct UI behaviour of the website (i.E. correct resizing, etc.)
 * -
 * Sources used within this class:
 *  1.(14.06.2016 @ 12:11) - http://stackoverflow.com/questions/759887/how-to-create-a-dom-node-as-an-object
 *  2.(48.06.2016 @ 13:21) - http://stackoverflow.com/questions/5076466/javascript-replace-n-with-br
 */
IAMA_Extension.UIGenericMethods = function () {
    var that = {},

        body,

        /**
         * This method adapts the panels according to the used display height
         * Otherwise they wouldn't be resized on window resize
         * @private
         */
        _initResizeViewDependingOnScreenRes = function () {
            var setElementHeight = function () {
                // 225 has been manually chosen here
                // The choice was necessary because the template is a little bit inconsistent to use
                var height = $(window).height() - 230;
                $('.chat-panel .panel-body').css('height', (height));
            };

            // Whenever this
            $(window).on("resize", function () {
                setElementHeight();
            }).resize();
        },

        /**
         * This method forces all dropdown windows (filtering / sorting) to not hide whenever a single option has
         * been clicked
         * @private
         */
        _initLetDropDownStay = function () {
            $('.dropdown-menu input, .dropdown-menu label, .dropdown-menu select').click(function (e) {
                e.stopPropagation();
            });
        },

        /**
         * Simply initializes the body of the website document here
         * @private
         */
        _initUI = function () {

            body = $(document.body);

        };

    /**
     * Initializes this UIGenericMethod class
     *
     * @returns {object} UIGenericMethod object
     */
    that.init = function () {
        _initUI();
        _initResizeViewDependingOnScreenRes();
        _initLetDropDownStay();
    };
    return that;
}();