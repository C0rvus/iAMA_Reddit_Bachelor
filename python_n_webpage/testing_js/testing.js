// https://stackoverflow.com/a/10857447

console.log("FUCKFUCKFUCK");


var data_to_send = '{'
    +'"text" : "Raj",'
    +'"age"  : 32,'
    +'"married" : false'
    +'}';

var obj = new Object();
obj.text = "Raj";


_onSuccess = function () {
  console.log("I am successful");
};

var data = { "text" : "I am an idiot!! \n \n Yes i AM" };
$.ajax({
    type: "POST",
    url: "http://127.0.0.1:5000/post_to_reddit/?c_id=1234567",
    processData: false,
    contentType: 'application/json',
    data: JSON.stringify(data),
    success: function(r) {
        console.log("SUCCCESSSS")
    }});