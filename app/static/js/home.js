/**
 * Created by Sudo Pnet on 26/04/2018.
 */
$(document).ready(main);

function populate_stats(){
    alert('i was clicked');
}

function main(){
    (function (){
        //get all the data and render
        $.ajax(window.location.href,
            {
                data: 'full-data',
                method: "POST"
            }
            ).done(function(data){
                //display if error
            var today = new Date();
            var anchor_arrays, marketsArray = [];
            $('#dates').children().each(function(index, element){
                //for each child we need to bind the ajax function, and populate the time data
                console.log(index);
                console.log(element);
                anchor_arrays.push(element.children[0]);
            });
            console.log(anchor_arrays);
            for (var index = 0; index < anchor_arrays.length; index++){
                anchor_arrays[index].onclick(populate_stats());
                var time_tag = anchor_arrays[index];
                time_tag.attr('datetime', data.dates_nav[index]);
                let _this_date = new Date(data.dates_nav[index]);
                time_tag.html(data.dates_nav[index])
                if (_this_date.getDate() === today.getDate() && _this_date.getMonth === today.getMonth()){
                    time_tag.html('today');
                }
                
            }
            $('#markets').children().each(function(index, element){
                anchor_arrays.push(element.children[0]);
            });
            for (var counter = 0; counter < marketsArray.length; counter++){
                marketsArray[index].onclick(populate_stats());
                marketsArray[index].html(data.markets[index])
                
            }
            
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