/**
 * Created by Sudo Pnet on 26/04/2018.
 */
$(document).ready(main());

function populate_stats(){
    alert('i was clicked');
}

function withData(data){
    alert('Data is currently being displayed');
    console.log(data);
}
function setDatesNavigation(alist){
    //populate the dates navigation with the correct data, bind the required event listeners
    var anchorTags = $('#dates li a time')
    for (var forCounter = 0; forCounter < alist.length; forCounter++){
        //get the anchor tag modify the 
    }
    
}

function main(){
    (function (){
        //get all the data and render
        $.ajax(window.location.href,
            {
                data: {
                    requestData: 'full'
                },
                method: "POST"
            }
            ).done(function (data){
            withData(data);
        });
    })();
    
    //form
    $('#subscription-form').on('submit', function(event){
        event.preventDefault();
        //email verification code here
        pattern = /\s|\d+@\s\.com/;
        email_data = {
            email: $('#subscription-form').val()
        }
        $.ajax(window.location.href,
            {
                data: email_data,
                method: "POST"
            }
            ).done(function(data){
                //display if error
        });
    });
    (function(){
        //asynchronous ajax requests for the pills
    })();
}