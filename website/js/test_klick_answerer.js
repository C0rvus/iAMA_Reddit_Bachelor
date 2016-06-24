// Source: https://nakupanda.github.io/bootstrap3-dialog/

$( "#btn-template_1" ).click(function() {

    BootstrapDialog.show({
        title: 'Important information',
        message: 'To refer to an answer you have already made simply click "Pick answer" and select the appropriate answer' +
        ' from the expanded "Answered Questions" by clicking on it. \n\n After the selection the link to the given answer will be applied' +
        ' to text input field. Additionally the "Unanswered Questions" panel will be restored',
        buttons: [{
            icon: 'glyphicon glyphicon-send',
            label: 'Pick answer',
            cssClass: 'btn-primary',
            autospin: true,
            action: function(dialogRef){
                dialogRef.enableButtons(false);
                dialogRef.setClosable(false);
                dialogRef.getModalBody().html('Loading up necessary javascripts...');

                $("#iAMA_Unanswered_Uber_Div").fadeToggle();

                $("#iAMA_Answered_Uber_Div").removeClass("col-lg-4");
                $("#iAMA_Answered_Uber_Div").addClass("col-lg-12");

                $('#iAMA_Answer_Panel > li' ).on('click', function () {
                    alert(this.id);

                    $("#iAMA_Unanswered_Uber_Div").fadeToggle();

                    $("#iAMA_Answered_Uber_Div").removeClass("col-lg-12");
                    $("#iAMA_Answered_Uber_Div").addClass("col-lg-4");

                    $("#btn-input_y").text($("#btn-input_y").val() + "  " + this.id);

                    $('#iAMA_Answer_Panel > li').unbind( "click" );

                });


                setTimeout(function(){
                    dialogRef.close();
                }, 2000);
            }
        }, {
            label: 'Close',
            action: function(dialogRef){
                dialogRef.close();
            }
        }]
    });


});

//TODO: die Questions hiden