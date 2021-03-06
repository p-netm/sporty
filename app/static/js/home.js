/**
 * Created by Sudo Pnet on 26/04/2018.
 */
$(document).ready(main());

var dataStore = {};
function sortDataArray(dataArray){
    /*{away_team: "A. Lustenau", country: "Austria", time: "18:30", home_team: "FAC Wien", league: "Erste Liga", …}*/
    dataArray = Array.from(dataArray);
    let sortOrder = $('.display-filter a.active').text();
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

function tabulateData(dataArray){ /*   *****   */
    //fill data to the display table, dataArray is array, and can be sorted in two ways:
    // by kickoff time, by league title
    dataArray = sortDataArray(dataArray);
    var table = $('#data-table');
    table.empty();
    date_thead = createDateTHead(dataArray[0].date);
    table.append(date_thead);
    var currentLeague;
    for (let index=0; index < dataArray.length; index++) {
        let obj = dataArray[index];
        if (currentLeague && obj.league === currentLeague) {
            //get the last tbody and append the below match to that
            var lastAddedTbody = $('#data-table tbody:last');
            lastAddedTbody.append(createSingleMatch(obj.home_team, obj.away_team, obj.time));
        }
        else if (currentLeague && obj.league !== currentLeague) {
            let breadcrumbs = createBreadcrumbs(obj.country, obj.league);
            currentLeague = obj.league;
            table.append(breadcrumbs);
            table.append('<tbody>' + createSingleMatch(obj.home_team, obj.away_team, obj.time) + '</tbody>');
        }
        else if (!currentLeague) {
            //the start
            let breadcrumbs = createBreadcrumbs(obj.country, obj.league);
            currentLeague = obj.league;
            table.append(breadcrumbs);
            table.append('<tbody>' + createSingleMatch(obj.home_team, obj.away_team, obj.time) + '</tbody>');
        }
    }
}

function createDateTHead(dateAsString){
    const tags = '<thead class="date"><tr><td colspan="4">'+ dateAsString + '.</td></tr></thead>';
    return tags
}
function createBreadcrumbs(countryName, leagueName){
    const tags = '<thead class="breadcrumps"><tr><td colspan="4">soccer>' + countryName +'>'+ leagueName +'</td></tr></thead>';
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
        var incumbent_active = $('#markets li a.active').removeClass('active');
        thisMarketTag.addClass('active');
        dataStore = data;
        tabulateData(data.tips);
    });
}

function withData(data){
    var datesNavigation = data.dates_nav;
    var marketNavigation = data.markets;
    var topTeams = data.teams_dict_list; // top teams is a dictionary with keys: top_ov[un[gg[ng]]]
    setDatesNavigation(datesNavigation);
    setMarketsNavigation(marketNavigation);
    renderTopTeams(topTeams);
}
function listData(topTeamData, ulElement){
    for (index = 0; index< topTeamData.length; index++){
        ulElement.append('<li><img class="top-team-logo" src=' + topTeamData[index].logo+'><em>' + topTeamData[index].team_name + '</em></li>')
    }
}
function renderTopTeams(diction){
    // get the respective card displays and parse the required data into each display
    var topOv = $('#ov-section ul');
    var topUn = $('#un-section ul');
    var topGg = $('#gg-section ul');
    var topNg = $('#ng-section ul');
    listData(diction.top_ov, topOv);
    listData(diction.top_un, topUn);
    listData(diction.top_gg, topGg);
    listData(diction.top_ng, topNg);
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
        //deactivate the email submit button and set other default html behaviours
        
    })();
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
            $('#markets li a.active').trigger('click');
        });
    })();
    
    //form
    $('#submit').on('click', function(event){
        event.preventDefault();
        var email_data = {
            email: $('#subscription-form').val()
        };
        $.ajax(window.location.href,
            {
                data: email_data,
                method: "POST"
            }
            ).done(function(data){
                //display feedback above the email input field
                $('#subscription-message').html(data["message"]);
                console.log(data);
        });
    });

    //display-filters
    $(".display-filter a").on('click', function(event){
        event.preventDefault();
        $(".display-filter a.active").removeClass('active');
        $(this).addClass('active');
        tabulateData(dataStore.tips);
    });
    
    function emailVerifies(email){
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }

        
    $('#email').on('input', function (){
        let userInput = $(this).val();
        if (!emailVerifies(userInput)){
            //add a dismissable error message above the input tag
            $("#submit").attr("disabled",true);
            $('#subscription-message').empty();
            $('#subscription-message').addClass("error-message");
            $('#subscription-message').html("Invalid Email");
        }
        else{
            //activate the email submit button
            $('#subscription-message').empty();
            $('#subscription-message').removeClass("error-message");
            $("#submit").attr("disabled",false);
        }
    });
    
}