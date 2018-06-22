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
    thisTimeTag = $(this);
    dateString = thisTimeTag.attr("datetime");
    market = $('#markets li a.active').val();
    $.ajax(window.location.href, {
        method : "POST",
        data : {
            date: dateString,
            market: market
        }
    }).done(function (data){
        // place data in the table
        $('#dates li a.active').removeClass("active");
        thisTimeTag.parent().addClass("active");
        tabulateData(data.tips);
    });
}

function populateStatsForMarkets(){
    console.log(this, 'market was clicked');
    thisMarketTag = $(this);
    market = thisMarketTag.val();
    dateString = $('#dates li a.active time').attr('datetime');
    $.ajax(window.location.href, {
        method : "POST",
        data : {
            date: dateString,
            market: market
        }
    }).done(function (data){
        // place data in the table
        //toggle the active class
        console.log(data);
        tabulateData(data.tips);
    });
}

function withData(data){
    datesNavigation = data.dates_nav;
    marketNavigation = data.markets;
    setDatesNavigation(datesNavigation);
    setMarketsNavigation(marketNavigation);
}

function setDatesNavigation(alist){
    // populate the dates navigation with the correct data, bind the required event listeners
    var anchorTags = $('#dates li a time');
    $.each(anchorTags, function(index, value){
        $(value).html(alist[index]);
        $(value).attr('datetime', alist[index]);
        $(value).on("click", populateStatsForDates);
    });

}

function setMarketsNavigation(alist){
    var anchorTags = $('#markets li a');
    $.each(anchorTags, function(index, value){
        $(value).html(alist[index]);
        $(value).on("click", populateStatsForMarkets);
    });
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