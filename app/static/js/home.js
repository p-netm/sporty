/**
 * Created by Sudo Pnet on 26/04/2018.
 */
$(document).ready(main());

var dataStore = {};
function sortDataArray(dataArray, sortOrder = "kickoff"){
    /*{away_team: "A. Lustenau", country: "Austria", time: "18:30", home_team: "FAC Wien", league: "Erste Liga", …}*/
    dataArray = Array.from(dataArray);
    function condenseTime(time){
        let hours = time.split(":")[0];
        let minutes = time.split(":")[1];
        return parseFloat(hours) + parseFloat(minutes/60);
    }

    if (sortOrder === "kickoff"){
        // sort based on time, create new array and return the array with the sorted data
        dataArray.sort(function(objA, objB){
            return condenseTime(objA.time) - condenseTime(objB.time);
        });

    }
    if (sortOrder === "league"){
        //sort against the league name and return the results as a new array
        dataArray.sort(function(valueA, valueB){
            if (valueA.league > valueB.league){return 1;}
            else if (valueA.league < valueB.league){return -1;}
            else {return 0;}
        });
    }
    return dataArray;
}

function tabulateData(dataArray, sortOrder){
    //fill data to the display table, dataArray is array, and can be sorted in two ways:
    // by kickoff time, by league title
    dataArray = sortDataArray(dataArray, sortOrder);
    var table = $('#data-table');
    table.empty();
    date_thead = createDateTHead(dataArray[0].date);
    table.append(date_thead);
    var currentLeague;
    $.each(dataArray, function(index, obj){
        if (currentLeague && obj.league === currentLeague){
            table.append(createSingleMatch(obj.home_team, obj.away_team, obj.time));
        }
        else if (currentLeague && obj.league !== currentLeague){
            table.append('</tbody>');
            let breadcrumbs = createBreadcrumbs(obj.country, obj.league);
            currentLeague = obj.league;
            table.append(breadcrumbs);
            table.append('<tbody>');
            table.append(createSingleMatch(obj.home_team, obj.away_team, obj.time));
        }
        else if (!currentLeague){
            //the start
            let breadcrumbs = createBreadcrumbs(obj.country, obj.league);
            currentLeague = obj.league;
            table.append(breadcrumbs);
            table.append('<tbody>');
            table.append(createSingleMatch(obj.home_team, obj.away_team, obj.time));
        }
    });

}

function createDateTHead(dateAsString){
    const tags = '<thead class="date"><tr><td colspan="4">'+ dateAsString + '.</td></tr></thead>';
    return tags
}
function createBreadcrumbs(countryName, leagueName){
    const tags = '<thead class="breadcrumps"><tr><td colspan="4">SOCCER>' + countryName +'>'+ leagueName +'</td></tr></thead>';
    return tags
}
function createSingleMatch(homeTeam, awayTeam, time){
    const tags = '<tr><td> '+ time + '</td><td>'+ homeTeam + '</td><td> - </td><td>'+ awayTeam + '</td></tr>'
    return tags
}

function populateStatsForDates(){
    //get the values of the active dates and markets tab and create an ajax request
    var thisTimeTag = $(this);
    var dateString = thisTimeTag.attr("datetime");
    var market = $('#markets li a.active').val();
    console.log("market:  ",market);
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
        dataStore = data;
        tabulateData(data.tips);
    });
}

function populateStatsForMarkets(){
    var thisMarketTag = $(this);
    var market = thisMarketTag.text();
    var dateString = $('#dates li a.active time').attr('datetime');
    $.ajax(window.location.href, {
        method : "POST",
        data : {
            date: dateString,
            market: market
        }
    }).done(function (data){
        // place data in the table
        //toggle the active class
        incumbent_active = $('#markets li a.active').removeClass('active');
        thisMarketTag.addClass('active');
        dataStore = data;
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
            activeMarket = $('#markets li a.active').trigger('click');
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

    //display-filters
    $(".display-filter a").on('click', function(event){
        event.preventDefault();
        $(".display-filter a.active").removeClass('active');
        $(this).addClass('active');
        sortOrder = $(this).text();
        tabulateData(dataStore.tips, sortOrder);

    });
}