import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime
import re
import sys
import time as Time


def stringify(a):
    if len(str(a)) == 1:
        return '0' + str(a)
    return str(a)


def scrap_for_mutual_matches(url):
    """
    {
        "time": 12321321331,
        "home_team":"team_name",
        "away_team": "team_name",
        "result": "2-5",
        "first_half_score": "2-2",
        "second_half_score": "0-5",
        "past_home": [
            {
                "time": 12321321331,
                "home_team":"team_name",
                "away_team": "team_name",
                "result": "2 - 5",
                "first_half_score": "2-2",
                "second_half_score": "0-5"
            },
            {
                "time": 12321321331,
                "home_team":"team_name",
                "away_team": "team_name",
                "result": "2 - 5",
                "first_half_score": "2-2",
                "second_half_score": "0-5"
            }
            ]
        "past_away":[
            {
                "time": 12321321331,
                "home_team":"team_name",
                "away_team": "team_name",
                "result": "2 - 5",
                "first_half_score": "2-2",
                "second_half_score": "0-5"
            },
            {
                "time": 12321321331,
                "home_team":"team_name",
                "away_team": "team_name",
                "result": "2 - 5",
                "first_half_score": "2-2",
                "second_half_score": "0-5"
            }
            ]
        "mutual": [
            {
                "time": 12321321331,
                "home_team":"team_name",
                "away_team": "team_name",
                "result": "2 - 5",
                "first_half_score": "2-2",
                "second_half_score": "0-5"
            },
            {
                "time": 12321321331,
                "home_team":"team_name",
                "away_team": "team_name",
                "result": "2 - 5",
                "first_half_score": "2-2",
                "second_half_score": "0-5"
            },
            {
                "time": 12321321331,
                "home_team":"team_name",
                "away_team": "team_name",
                "result": "2 - 5",
                "first_half_score": "2-2",
                "second_half_score": "0-5"
            }
        ]
    }
    """

    webpage_text = requests.get(url).text
    soup = BeautifulSoup(webpage_text, 'html.parser')
    main_div = soup.find_all(id='pos_62')[0]
    # main_div contains a div with the table that holds the match records
    tbody_list = main_div.find_all('tbody')
    td_list = list()  # will hold the td tags that hold the href with the #odds
    for tag in tbody_list:
        td_list.extend(tag.find_all('a', class_='tabOdds'))

    all_hrefs = list()
    for link in td_list:
        all_hrefs.append(link.get('href'))

    for index in range(len(all_hrefs)):
        link = all_hrefs[index]
        # run the scrapper functions here for mutual matches and past matches here


def splitter(scores):
    """ returns the scores in the desired integer format"""
    scores = scores.split('-')
    home_goals = int(scores[0])
    away_goals = int(scores[1])
    return {'home_goals': home_goals, 'away_goals': away_goals}


def check_over(scores_diction):
    """ input scores, output either 1 or 0"""
    # if result is equal or greater than 3; then increment over counter else increment under counter
    if scores_diction['home_goals'] + scores_diction['away_goals'] >= 3:
        return 1
    elif scores_diction['home_goals'] + scores_diction['away_goals'] <= 2:
        return 0


def one_x_2(scores):

    # if home goals scored are more than the
    # away goals increment home_counter else, draw or away_counter
    if scores['home_goals'] > scores['away_goals']:
        return 1
    elif scores['home_goals'] < scores['away_goals']:
        return 0
    else:
        return 'x'


def relative_win(scores, home_team, away_team):
    """if one_teams goals are always above the others increment a counter too..."""
    home_goals = scores['home_goals']
    away_goals = scores['away_goals']
    if home_goals > away_goals:
        return home_team
    elif home_goals < away_goals:
        return away_team


def start_conveyer(match_dict):
    # we first deal with over and under 25 patterns from mutual matches only, we
    # will take the simplest approach
    our_list = match_dict['mutual']
    if our_list is None:
        return None
    over_counter = 0
    home_win_counter = 0
    draw_counter = 0
    away_win_counter = 0
    home_team_counter = 0
    away_team_counter = 0
    overall = 0

    for diction in our_list:
        home_team_name = diction['home_team']
        away_team_name = diction['away_team']
        full_time_score = diction['full_time_score']
        refactored_scores = splitter(full_time_score)

        if full_time_score is not None:
            over_counter += check_over(refactored_scores)
            if one_x_2(refactored_scores) == 1:
                home_win_counter += 1
            elif one_x_2(refactored_scores) == 'x':
                draw_counter += 1
            elif one_x_2(refactored_scores) == 0:
                away_win_counter +=1
            else:
                raise Exception('Unrecognized returned Value for 1 x 2')

            if relative_win(refactored_scores, home_team_name, away_team_name) == home_team_name:
                home_team_counter += 1
            elif relative_win(refactored_scores, home_team_name, away_team_name) == away_team_name:
                away_team_counter += 1
            overall += 1

    over_25_percentage = round(over_counter / overall * 100, 2)
    under_25_percentage = round(100 - over_25_percentage, 2)
    home_win_percentage = round(home_win_counter / overall * 100, 2)
    draw_percentage = round(draw_counter / overall * 100, 2)
    away_win_percentage = round(away_win_counter / overall * 100, 2)
    home_team_percentage = round(home_team_counter / overall * 100, 2)
    away_team_percentage = round(away_team_counter / overall * 100, 2)

    # now the question remains how do we report the findings, below is a rudimentary way of how
    # i will be doing it for now, i will improve on this model later
    over_string = under_string = string1 = string2 = string3 = string4 = string5 = ''
    full_string = None

    checker = False


def get_specific_match_details(url):
    url = 'http://www.sportstats.com' + url
    full_page = requests.get(url)
    match_dict = dict()
    insoup = BeautifulSoup(full_page.text, 'html.parser')
    country_league = insoup.find_all(id='center')
    country_league = country_league[0].find_all('div', class_='bread')
    country_league = country_league[0].find_all('a')
    league = country_league[len(country_league) - 1].get_text()
    country = country_league[len(country_league) - 2].get_text()

    match_dict['country'] = country
    match_dict['league'] = league

    teams = insoup.find('h1', class_='hidden').get_text()
    home_team = teams.split(' - ')[0]
    away_team = teams.split(' - ')[1]

    match_dict['home_team'] = home_team
    match_dict['away_team'] = away_team

    main_divs_info = insoup.find_all('div', class_='event-header-wrapper')
    for div in main_divs_info:
        home_logo_url = div.find_all('div', class_='home-logo')
        home_logo_src = home_logo_url[0].img.get('src')
        match_dict['home_logo_src'] = home_logo_src
        away_logo_url = div.find_all('div', class_='away-logo')
        away_logo_src = away_logo_url[0].img.get('src')
        match_dict['away_logo_src'] = away_logo_src

        result = parse_scores_for_match(insoup)
        match_dict.update(result)

        div_date_time_string = div.find_all('span', class_='datet')[0].get_text()
        experimental_string = div_date_time_string
        date_of_play = date_from_string(experimental_string)
        tarehe = date_of_play
        match_dict['time'] = tarehe.timestamp()

    return match_dict


def date_from_string(string):
    # example : Today, 26 Jun 2017, 00:00++++
    date_pattern = r'(\d+ \S+ \d{4})'
    time_pattern = r'(\d+:\d+)'
    # first confirm that the patterns match
    siku = re.findall(date_pattern, string)
    if len(siku) > 0:
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
        siku = siku[0].split(' ')
        _day = int(siku[0])
        _month = str(siku[1])
        _year = int(siku[2])
        for month in months:
            if str(_month) in month:
                _month = int(months.index(month)) + 1
    else:
        raise Exception('Unparsable date day format, please recheck that the website has not changed its date format.')

    saa = re.findall(time_pattern, string)
    if len(saa) > 0:
        tym = saa[0].split(':')
        _hour = int(tym[0])
        _minute = int(tym[1])
    else:
        raise Exception('Unparsable date time format, please check that the website has not changed its time format.')
    # we now create the  final object that we send back
    date_of_play = datetime(_year, _month, _day, _hour, _minute)
    return date_of_play


def retrieve_scores(insoup):
    # there are three cases that this function should deal with
    main_divs_info = insoup.find_all('div', class_='event-header-wrapper')
    div = main_divs_info[0]
    div_date_time_string = div.find_all('span', class_='datet')[0].get_text()
    experimental_string = div_date_time_string
    date_of_play = date_from_string(experimental_string).timestamp()

    if Time.time() < date_of_play:
        # means future match and those no scores
        return None
    if date_of_play > (Time.time() - (2 * 60 *60)) and date_of_play < Time.time():
        # means the game is currently in play
        return None
    # here we standardise the format regardless of the page display, follow the pattern [(]\d-\d , \d-\d[)]
    event_header_wrapper = insoup.find_all('div', class_='event-header-wrapper')[0]
    full_score_info_div = event_header_wrapper.find_all('div', class_='full')[1]
    # now we format
    full_score_info = full_score_info_div.p.get_text()
    full_score_info = re.findall(r'\S-\S', full_score_info)
    full_score_info = "(" + " , ".join(full_score_info) + ")"
    if len(full_score_info) <= 2:
        return  None
    return full_score_info


def parse_scores_for_match(insoup):
    """creates a proper representation of a goals scored before half tym and at full tym
    returns a dictionary containing the full_time, first_half and second_half scores."""
    # input is a div tag that holds the results
    event_header_wrapper = insoup.find_all('div', class_='event-header-wrapper')[0]
    event_header_score = event_header_wrapper.find_all('div', class_='event-header-score')[0]
    full_time_score = event_header_score.span.get_text()
    full_time_score = full_time_score.split(' - ')
    full_time_score = '-'.join(full_time_score)

    # now for the half time and full time results
    full_score_info = retrieve_scores(insoup)

    # validation of score data

    pattern = r'[(]\d-\d , \d-\d[)]'
    if full_score_info is not None:
        if len(re.findall(pattern, full_score_info)) == 1:
            scores = re.findall(pattern, full_score_info)[0]
            first_half_scores_pattern = r'[(](\d-\d) , \d-\d[)]'
            first_half_scores = re.findall(first_half_scores_pattern, scores)[0]
            second_half_scores_pattern = r'[(]\d-\d , (\d-\d)[)]'
            second_half_scores = re.findall(second_half_scores_pattern, scores)[0]
        else:
            raise Exception('The score format for half time , full time seems to have changed')

    else:
        return {'full_time_score': None, 'first_half_score': None,
                'second_half_score': None}
    # how about a little validation. we do so by checking that the scores equal to full-time scores
    # validate only when full_tim_score is length is 1

    if len(full_time_score) == 3:
        score_validated = score_validator(first_half_scores, second_half_scores, full_time_score)
    else:
        return {'full_time_score': full_time_score, 'first_half_score': first_half_scores,
                'second_half_score': second_half_scores}
    if score_validated:
        # return the data in a parsable format
        return {'full_time_score': full_time_score, 'first_half_score': first_half_scores,
                'second_half_score': second_half_scores}
    else:
        raise Exception('Problem validating the Scores.')


def score_validator(first_score, second_score, full_score):
    if not isinstance(first_score, str) or not isinstance(second_score, str) or not isinstance(full_score,str):
        raise TypeError('One of the argument scores is in an unrecognizable format')
    else:
        if len(first_score) != 3 and len(second_score) != 3 and len(full_score) != 3:
            raise Exception('There was a problem ')
    full = (full_score.split('-'))
    first = (first_score.split('-'))
    second = (second_score.split('-'))
    if int(first[0]) + int(second[0]) == int(full[0]) and int(first[1]) + int(second[1]) == int(full[1]):
        return True
    else:
        return False


def retrieve_mutual_matches_data(url):
    """input the link as the get specific content function does
    output: a dictionary of a single mutual_matches key with a list of dictionaries"""

    if not isinstance(url, str):
        raise Exception('Url should be string format, to be parsed')
    else:
        if 'http://www.sportstats.com' in url:
            url = url
        else:
            url = 'http://www.sportstats.com' + url
    full_page = requests.get(url)
    soup = BeautifulSoup(full_page.text, 'html.parser')
    sub_content = soup.find_all(id='subContent_0')[0]
    mutual_block = sub_content.find_all(id='pos_21')[0]
    maintainable_content = mutual_block.find_all(id='LS_maintableContent')[0]
    try:
        table = maintainable_content.find_all(id='maintable_0')[0]
    except IndexError as maintainable_error:
        return {'mutual': None}
    links_list = table.find_all('a',  class_='tabOdds')
    all_hrefs = list()
    for link in links_list:
        href_text = link.get('href')
        all_hrefs.append(href_text)

    all_mutual_matches = list()
    for href in all_hrefs:
        mutual_match_instance = get_specific_match_details(href)
        all_mutual_matches.append(mutual_match_instance)
    # create a dictionary to be returned

    mutual_diction = {'mutual': all_mutual_matches}

    return mutual_diction

def ignite_after(date_string):
    # sleep until the time stated in the above string is reached
    # get fed in details => 13/07/2013 00:57
    dt = datetime.strptime(date_string, "%d/%m/%y %H:%M")
    # infinitely sleep through intervals of 5 seconds until the time is equal to that given in the string, then
    # call another function that will infinitely sleep for 2 hours and another that will do the same for a full day
    while True:
        Time.sleep(5)
        now = datetime.now()
        # first of all you must check that the time given is in the future
        if now.timestamp() > dt.timestamp():
            raise Exception('Start time is in the past')
        if now.timestamp() in range(dt.timestamp(), dt.timestamp() + 10):
            # should the above evaluate to true then that would mean its the day that we want
            # call the daily function first here then the hourly
            scheduled()


def scheduled():
    """daily checkers: database upgrade, flag checks
     hourly checkers database modification-> scores input"""
    while True:
        current = datetime.now()
        daily_step = 24 * 60 * 60
        hourly_step = 2 * 60 * 60
        Time.sleep()  #**********

# i need this application to work for all functions  once and be abble to retrieve and perform all the checks
