console.log("Preent dropdown script successfully loaded");

$('.dropdown-menu input, .dropdown-menu label, .dropdown-menu select').click(function(e) {

    console.log("script executed !!!");

    e.stopPropagation();
});