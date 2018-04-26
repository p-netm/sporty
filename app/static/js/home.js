/**
 * Created by Sudo Pnet on 26/04/2018.
 */
$(document).ready(main);

function main(){
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