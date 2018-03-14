import requests
from bs4 import BeautifulSoup
import datetime
import re
import time as Time
from urllib.parse import urlparse, urljoin
from errors import *


def _run_(url="""http://www.sportstats.com/soccer/matches/"""):
    """The project manager, his main job will to motivate the other functions and  then consolidate their
    work into the last meaningful required product.
    :parameters: wil have an optional url of a certain soccer page from which to pull data from
    """
    all_main_links = scrap_all_links(url)
    all_dictions_lists = []
    for each_link in all_main_links:
        full_page = requests.get(url)
        insoup = BeautifulSoup(full_page.text, 'html.parser')
        diction = get_specific_match_details(insoup)
        diction.update(retrieve_mutual_matches_data(insoup))
        all_dictions_lists.append(diction)
    return {"full_data": all_dictions_lists}


def scrap_all_links(url):
    """
    :parameter: the specific url that contains the data of interest
        :defaults to the current day soccer url
    :returns: A list of all the links that href to a specific matches' details
    """
    if os.environ.get('CONFIGURATION') == "testing":
        # we are loading file from disk,
        with open(url) as handler:
            webpage_text = handler.read()
    else:
        full_webpage = requests.get(url)
        webpage_text = full_webpage.text
    soup = BeautifulSoup(webpage_text, 'html.parser')
    main_div = soup.find_all(id='pos_62')[0]
    # main_div contains a div with the table that holds the match records

    tbody_list = main_div.find_all('tbody') # tbody tags: sample rendering: Avai0 - 1 Hercilio Luz1.334.307.76
    td_list = [] # will hold the td tags that hold the href with the #odds
    for tag in tbody_list:
        td_list.extend(tag.find_all('a', class_='tabOdds'))

    all_hrefs = []
    for link in td_list:
        all_hrefs.append(link.get('href'))
        
    refatored_hrefs = [urljoin('''http://www.sportstats.com''', urlparse(a).path) for a in all_hrefs]
    return refactored_hrefs


def get_specific_match_details(insoup):
    """:parameter: a beautiful soup object of the specific matches' details page
    :return: a dictionary with data pertaining to the ollowing keys:
    country, league, home_team, away_team, home_logo-url, away_logo_url,
    first_half_home_goals, first_half_away_goals, full_time_home-goals, 
    full_time_away_goals, date, time
    """
    match_dict = dict()
    country_league = insoup.find_all(id='center')
    country_league = country_league[0].find_all('div', class_='bread')
    country_league = country_league[0].find_all('a')
    league = country_league[len(country_league) - 1].get_text()
    country = country_league[len(country_league) - 2].get_text()

    match_dict['country'] = country
    match_dict['league'] = league

    teams = insoup.find('h1', class_='hidden').get_text()
    home_team = teams.split('-')[0].strip()
    away_team = teams.split('-')[1].strip()

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
        match_dict['date'], match_dict['time'] = date_from_string(experimental_string)  # unpack returned values

    return match_dict


def date_from_string(string):
    """Takes a string; then uses reqular expresiions to parse the correct needed parts of the string.
    After that we use the str formatting methods to recreate proper date and time objects from the 
    matched strings
    :parameter: strings
    :returns: a tuple containing two objects with the date object as the first index and time object as 
    the later
    """
    # example : Today, 26 Jun 2017, 00:00++++
    date_pattern = r'(\d+ \S+ \d{4})'
    time_pattern = r'(\d+:\d+)'
    # first confirm that the patterns match
    _day = re.findall(date_pattern, string)
    if len(_day) > 0:
        stringed_date = _day[0]
        day_of_play = datetime.datetime.strptime(stringed_date, '%d %b %Y')
    else:
        raise PatternMatchError('Unparsable date day format, please recheck that the website has not changed its date format.')

    _time = re.findall(time_pattern, string)
    if len(_time) > 0:
        stringed_time = _time[0]
        time_of_play = datetime.datetime.strptime(stringed_time, '%H:%M')
    else:
        raise PatternMatchError('Unparsable date time format, please check that the website has not changed its time format.')
        
    return day_of_play, time_of_play


def retrieve_scores(div):
    """:parameter: is a beautiful soup section of the website
    :returns: the hometeams half and full goals as well as those  of the awayteam's"""
    # there are three cases that this function should deal with
    full_score_info_div = div.find_all('div', class_='full')[1]
    # now we format
    full_score_info = full_score_info_div.p.get_text()
    full_score_info = re.findall(r'\S-\S', full_score_info)
    first_half_scores = full_score_info[0]
    second_half_scores = full_score_info[1]
    score_pattern = r'\d+'
    home_team_first_half_goals, away_team_first_half_goals = re.findall(score_pattern, first_half_scores)[0], re.findall(score_pattern, first_half_scores)[0]
    home_team_second_half_goals, away_team_second_half_goals = re.findall(score_pattern, second_half_scores)[0], re.findall(score_pattern, second_half_scores)[1]
    return home_team_first_half_goals, away_team_first_half_goals, home_team_second_half_goals, away_team_second_half_goals


def parse_scores_for_match(div):
    """creates a proper representation of a goals scored before half tym and at full tym
    returns a dictionary containing the full_time, first_half and second_half scores.
    :parameter: is a beautiful soup section of the website"""
    # input is a div tag that holds the results
    event_header_score = div.find_all('div', class_='event-header-score')[0]
    full_time_score = event_header_score.span.get_text()
    # if we have a valid full time score then we can be sure that we have the scores otherwise nope.
    pattern = r'\d+'
    result = re.findall(pattern, full_time_score)
    if len(result) == 2:
        # we have valid scores ladies and gemtlemen, proceed
        home_goals = result[0]
        away_goals = result[1]

        # now for the half time and full time results
        home_first_half_goals, away_first_half_goals, home_second_half_goals, away_second_half_goals = retrieve_scores(div)
    else:
        home_first_half_goals, away_first_half_goals, home_second_half_goals, away_second_half_goals = None, None, None, None
    
    return{
        'home_match_goals': home_goals,
        'away_match_goals': away_goals,
        'home_first_half_goals': home_first_half_goals,
        'away_first_half_goals': away_first_half_goals,
        'home_second_half_goals': home_second_half_goals,
        'away_second_half_goals': away_second_half_goals
    }


def retrieve_mutual_matches_data(soup):
    """
    :parameter: a beatiful soup object of the specific matches' details page
    :returns: a dictionary of a single mutual_matches key with a list of dictionaries
    """
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
