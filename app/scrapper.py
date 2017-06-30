import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime
from .dataModel import Team, BASE
import re
import time as Time

def scrap_for_mutual_science(url):
    """
    {
        "time": 12321321331,
        "home_team":"team_name",
        "away_team": "team_name",
        "result": "2-5",
        "first_half_score": "2-2",
        "second_half_score": "0-5",
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
    full_webpage = requests.get(url)
    webpage_text = full_webpage.text
    soup = BeautifulSoup(webpage_text, 'html.parser')
    main_div = soup.find_all(id='pos_62')[0]
    # main_div contains a div with the table that holds the match records

    tbody_list = main_div.find_all('tbody')
    td_list = list()  # will hold the td tags that hold the href with the #odds
    for tag in tbody_list:
        td_list.extend(tag.find_all('a', class_='tabOdds'))

    all_hrefs = list()
    money_list = list()
    flag_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                 'files', 'flagged', str(int(Time.time())) + '.txt'))

            # create a txt file and add the name of the team
    file_handler = open(flag_dir, 'w')
    file_handler.write(" \n".join(money_list))
    file_handler.close()

    for link in td_list:
        all_hrefs.append(link.get('href'))

    for link in all_hrefs:
        home_and_away = get_specific_match_details(link)  # returns a list containing the home team details in the first
        # index
        home = home_and_away[0]
        away = home_and_away[1]

        # a record that has not yet been analyzed
        home_probs = start_conveyer(home['team'])
        away_probs = start_conveyer(away['team'])
        # if home_probs['score_prob'] > 60 or home_probs['concede_prob'] > 60:
        #     home_team.flagged = 1
        # elif home_probs['score_prob'] <40 or home_probs['concede_prob'] <40:
        #     home_team.flagged = -1
        # if away_probs['score_prob'] > 60 or away_probs['concede_prob'] > 60:
        #     away_team.flagged = 1
        # elif away_probs['score_prob'] <40 or away_probs['concede_prob'] <40:
        #     away_team.flagged = -1

def start_conveyer(team_name):
    num_of_records = 5
    def _check(goals):
        if goals > 5 :
            weight = 5
        elif goals > 4:
            weight = 4
        elif goals > 3:
            weight = 3
        elif goals < 2:
            weight = 1
        return weight
    # first iteration is for each respective teams goals scored
    def cumulative_goals(team):
        team_goals_scored = 0
        team_goals_conceded = 0
        match_scores = 0
        for a, b, c in team: # do the same for away_team
            team_goals_scored += b
            team_goals_conceded += c
            match_scores += b + c

        return {'total_scored': team_goals_scored, 'total_conceded': team_goals_conceded, 'total': match_scores}
    # average = divide the sums by the number of records specified in the query offset
    # team_goal_scored_spread = cumulative_goals(team)['total_scored'] / num_of_records
    # team_goal_conceded_spread = cumulative_goals(team)['total_conceded'] / num_of_records
    # match_scores_spread = cumulative_goals(team)['total'] / (num_of_records * 2)

    def first_check(home_score, home_concede, home_total, away_score, away_concede, away_total):
        average_home_score = _check(home_score)
        average_home_concede = _check(home_concede)
        average_home_total = _check(home_total)
        record = {'score_prob' : average_home_score / 5 *100,
                  'concede_prob': average_home_concede / 5 * 100,
                  'over_prob': average_home_total / 5 * 100,
        }
        # the decisive part
        return record
    # to check for mutual encounters you could possibly go through the #odds link and extract the data.
    # in retrieving the data you could read team records for home team and away team that have the same timestamp



def get_specific_match_details(url):
    url = 'http://www.sportstats.com' + url
    full_page = requests.get(url)
    home_dict = dict()
    away_dict = dict()
    insoup = BeautifulSoup(full_page.text, 'html.parser')
    country_league = insoup.find_all(id='center')
    country_league = country_league[0].find_all('div', class_='bread')
    country_league = country_league[0].find_all('a')
    # country_league now contains 4 links, the first contains the website link, the
    # second contains the game_type, third contains the country while the last contains the league
    league = country_league[len(country_league) - 1].get_text()
    country = country_league[len(country_league) - 2].get_text()
    home_dict['country'] = away_dict['country'] = country
    home_dict['league'] = away_dict['league'] = league
    teams = insoup.find('h1', class_='hidden').get_text()
    home_team = teams.split(' - ')[0]
    away_team = teams.split(' - ')[1]
    home_dict['team'] = home_team
    away_dict['team'] = away_team
    main_divs_info = insoup.find_all('div', class_='event-header-wrapper')
    sub_div_info = list()
    for div in main_divs_info:
        home_logo_url = div.find_all('div', class_='home-logo')
        # get img tag in above
        home_logo_src = home_logo_url[0].img.get('src')
        home_dict['home_logo_src'] = home_logo_src
        away_logo_url = div.find_all('div', class_='away-logo')
        away_logo_src = away_logo_url[0].img.get('src')
        away_dict['away_logo_src'] = away_logo_src


        scores_div = div.find_all('div', class_='event-header-score')[0]

        result = parse_scores_for_match(insoup)

        div_date_time_string = div.find_all('span', class_='datet')[0].get_text()
        # how the string looks Today, 26 Jun 2017, 00:00++++
        experimental_string = div_date_time_string
        # i think the best solution is to employ regular expressions
        date_of_play = date_from_string(experimental_string)
        tarehe = date_of_play
        # ??????*** try and convert tarehe to a timestamp ????*****
        home_dict['timestamp'] = tarehe.timestamp()
        away_dict['timestamp'] = tarehe.timestamp()

    return [home_dict, away_dict]

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
        print(_month)
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
        raise Exception('Unparsable date time format, please check that the wensite has not changed its time format.')

    # we now create the  final object that we send back
    date_of_play = datetime(_year, _month, _day, _hour, _minute)
    return date_of_play

def parse_scores_for_match(insoup):
    """creates a proper representation of a goals scored before half tym and at full tym
    returns a dictionary containing the full_time, first_half and second_half scores."""
    # input is a div tag that holds the results
    event_header_wrapper = insoup.find_all('div', class_='event-header-wrapper')[0]
    event_header_score = event_header_wrapper.find_all('div', class_='event_header-score')[0]
    full_time_score = event_header_score.span.get_text()

    # now for the half time and full time results
    full_score_info_div = event_header_wrapper.find_all('div', class_='full')
    for div in full_score_info_div:
        if len(div.find_all('p', class_='event_header_date')) == 0:
            full_score_info t= div.get_text()

    # validation of score data
    pattern = r'[(]\d-\d , \d-\d[)]'
    if len(re.find_all(pattern, full_score_info)) == 1:
        scores = re.findall(pattern, full_score_info)[0]
        first_half_scores_pattern = r'[(](\d-\d) , \d-\d[)]'
        first_half_scores = re.findall(first_half_scores_pattern, scores)[0]
        second_half_scores_pattern = r'[(]\d-\d , (\d-\d)[)]'
        second_half_scores = re.findall(second_half_scores_pattern, scores)[0]
    else:
        raise Exception('The score format for half time , full time seems to have changed')

    # how about a little validation. we do so by checking that the scores equal to full-time scores
    score_validated  = score_validator(first_half_scores, second_half_scores, full_time_score)
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
    full = int(full_score.split(' - '))
    first = int(first_score.split('-'))
    second = int(second_score.split('-'))
    if first[0] + second[0] == full[0] and first[1] + second[1] == full[1]:
        return True
    else:
        return False

