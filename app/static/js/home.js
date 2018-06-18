/**
 * Created by Sudo Pnet on 26/04/2018.
 */
$(document).ready(main());

function deactivateNavs(){
    $('.nav-link.active').each(function(index, tag){
        tag.removeClass('active')
    });
}

function tabulateData(data){
    //fill data to the display table, data is a list
}

function populateStatsForDates(){
    console.log(this, 'i was clicked');
    //get the values of the active dates and markets tab and create an ajax request
    dateString = this.attr("datetime");
    market = $('#markets li a.active').val();
    $.ajax(window.location.href, {
        method : "POST",
        data : {
            date: dateString,
            market: market
        }
    }).done(function (data){
        // place data in the table
        console.log(data);
        tabulateData(data.tips);
    });
}

function populateStatsForMarkets(){
    console.log(this, 'market was clicked');
    market = this.val();
    dateString = $('#dates li a.active time').attr('datetime');
    $.ajax(window.location.href, {
        method : "POST",
        data : {
            date: dateString,
            market: market
        }
    }).done(function (data){
        // place data in the table
        console.log(data);
        tabulateData(data.tips);
    });
}

function withData(data){
    alert('Data is currently being displayed');
    datesNavigation = data.dates_nav;
    marketNavigation = data.markets;
    setDatesNavigation(datesNavigation);
    setMarketsNavigation(marketNavigation);
    console.log(data);
}
function setDatesNavigation(alist){
    //populate the dates navigation with the correct data, bind the required event listeners
    var anchorTags = $('#dates li a time')
    for (var forCounter = 0; forCounter < alist.length; forCounter++){
        //modify the datetime attr and the html value
        anchorTags[forCounter].InnerHTML = "asdkada w" ; // `${alist[forCounter]}`;
        anchorTags[forCounter].setAttribute('datetime', alist[forCounter]);
        anchorTags[forCounter].addEventListener("click", populateStatsForDates);
        console.log(anchorTags[forCounter], alist[forCounter]);
    }
}

function setMarketsNavigation(alist){
    var anchorTags = $('#markets li a');
    for (var forCounter = 0; forCounter < alist.length; forCounter++){
        //modify the datetime attr and the html value
        anchorTags[forCounter].innerHTML = '' + alist[forCounter];
        anchorTags[forCounter].addEventListener("click", populateStatsForMarkets);
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