// Sources used within this class:
// 1. (13.06.2016) -
// https://stackoverflow.com/a/18559967


var setElementHeight = function () {
    // 225 has been manually chosen here
    // The choice was necessary because the template is a little bit inconsistent to use
    var height = $(window).height() - 230;
    $('.chat-panel .panel-body').css('height', (height));
};

$(window).on("resize", function () {
    setElementHeight();
}).resize();

