"""
 Home Page: typersi.com Areas of interests
    best 5 tipster picks
    picks from tipsters with the best efficiency -> high precedence
    Tipsters ranking
    Efficiency from 10 to 20 tips
    Efficiency above 20 tips -> optionally
    Efficiency 100%
 Each Tipster respective page: Areas of interest:
    main middle table records
    other points of interest fields are duplicates from the main web-page
 """
import requests
from bs4 import BeautifulSoup
import re
import sys
import os
from datetime import datetime


def get_home_page(text=False):
    """returns either a soup object or string object as per the given arguments
     soup_object by default"""
    home_url = 'http://www.typersi.com'
    index_html = requests.get(home_url).text
    if text:
        # return a text reponse
        return index_html
    soup = BeautifulSoup(index_html, 'html.parser')
    return soup

def get_top_picks(soup):
    """Isolates the first category: best 5 tipster picks, input: soup object representation of the full site
        output: list of tuples containing the sections data"""
    # there are theree tables that share the same class so i thought best to refer to
    # to these elements  through what surrounds them.
    h2_string = 'Best 5 tipsters picks'
    if len(re.findall(h2_string, str(soup))):
        best_5_header = soup.find_all('h2', string=h2_string)[0]
    else:
        print("Extreme danger!.. site's relative structure compromised, re-evaluate")
        sys.exit(2)
    desired_table = best_5_header.next_sibling.next_sibling
    #  ??? question how do i at least verify that u have a table and maybe even verify that its the table that you need
    # table has one thead and one tbody. the tbody contains 5 rows. The thead contains the title heads which i plan to use a keys
    # in a dictionary
    only_thead = desired_table.thead
    only_tr = only_thead.tr
    all_ths = only_tr.find_all('th')
    tbody = desired_table.tbody
    tr_list = tbody.find_all('tr')
    data_list = parse_table_rows(tr_list)
    writing_to_disk(stringify_diction_list(data_list), 'Days best Picks')
    return data_list

def get_picks_from_tipsters_with_the_best_efficiency(soup):
    """"""
    h2_string = "Picks from tipsters with the best efficiency"
    h2_string = 'Best 5 tipsters picks'
    if len(re.findall(h2_string, str(soup))):
        best_5_header = soup.find_all('h2', string=h2_string)[0]
    else:
        print("Extreme danger!.. site's relative structure compromised, re-evaluate")
        sys.exit(2)
    desired_table = best_5_header.next_sibling.next_sibling
    # i have jus thought of a way to check if the desired table is indeed what we are looking
    # for, well at least to some point, like say what if we had a way of accessing its attributes
    # and asserting what we know should be present is in-fact present
    thead = desired_table.thead # returns single thead with the table headings
    tbody = desired_table.tbody
    tr_list = tbody.find_all('tr')
    data_list = parse_table_rows(tr_list)
    writing_to_disk(stringify_diction_list(data_list), 'Picks from the best efficiency')
    return data_list

def parse_table_rows(tr_list):
    return_list = list()
    for tr in tr_list:
        temp_diction = {}
        td_list = tr.find_all('td')
        """
                <tr>
                    <td class="toolTyp"
                        title="22:00  |  Valur (Ice)  - Ventspils (Lat)   |   1    |  1.66   |  Totolotek   |  Soccer">
                        <a href="typer,marcom12,30761.html">marcom12</a>&nbsp;<img alt="+" src="template/img/plus.jpg"/>
                    </td>
                    <td>18:45</td>
                    <td>FK Liepaja (Lat) - Crusaders (Nir)</td>
                    <td><a class="toolTypek" href="#Totolotek"
                           onclick="javascript:openUrl('https://www.totolotek.pl?section=47&amp;place=24')"> 1 </a></td>
                    <td>30.00</td>
                    <td><a class="toolTypek" href="#Totolotek"
                           onclick="javascript:openUrl('https://www.totolotek.pl?section=47&amp;place=24')">1.56</a>
                    </td>
                    <td><a class="tableTypeBuk" style="color: " href="#888.com"
                           onclick="javascript:openUrl('http://www.888sport.com/bet?lang=en&amp;sr=394133&amp;flag=0000')"><img
                            class="bukImg" alt="888.com" src="logo/16.jpg"/></a></td>
                    <td><a rel="nofollow" href="art,7,Scores.html">Soccer</a></td>
                    <td></td>
                </tr>
                """
        # validating the number of tds in that we have just captured
        if len(td_list) != 9:
            raise Exception('Problem getting the table data')
        #tipster details in the first td
        first_td = td_list[0]
        tipster_url = first_td.a.get('href')
        tipster_name = first_td.a.get_text()
        # timing functionalities
        second_td =td_list[1]
        time_as_string = second_td.get_text()
        time_as_list = time_as_string.split(':')
        hour = int(time_as_list[0])
        minute = int(time_as_list[1])
        today = datetime.today()
        time_of_play = datetime(today.year, today.month, today.day, hour, minute)
        # the match including both the home team and the away team
        third_td = td_list[2]
        match = third_td.get_text()
        home_and_away = match.split(' - ')
        home_team = home_and_away[0]
        away_team = home_and_away[1]
        # the pick
        fourth_td = td_list[3]
        if len(re.findall(r'\d', fourth_td.get_text())) > 0:
            pick = str(int(fourth_td.get_text()))
        else:
            pick = str(fourth_td.get_text().strip(' '))
        # the proposed stake
        fifth_td = td_list[4]
        proposed_stake = fifth_td.get_text()
        stake_as_float = float(proposed_stake)
        confidence = stake_as_float / 30.0 * 100
        confidence = str(confidence)
        # now to a very important part to the odds
        sixth_td = td_list[5]
        odds_as_string = sixth_td.get_text()
        odds = float(odds_as_string)
        # as for the results i.e if provided
        results_td = td_list[-2]
        results = results_td.get_text()
        if len(re.findall('\d', results)) == 0:
            # signifies that the there is no digit in the result and thus the score is not yet displayed
            result = None
        temp_diction['tipster_url'] = tipster_url
        temp_diction['tipster_name'] = tipster_name
        temp_diction['time_of_play'] = time_of_play
        temp_diction['home_team'] = home_team
        temp_diction['away_team'] = away_team
        temp_diction['pick'] = pick
        temp_diction['confidence'] = confidence
        temp_diction['odds'] = odds
        return_list.append(temp_diction)
        return return_list

def writing_to_disk(string, parameter):
    """input: not yet defined:
     process: should write a certain string to a certain file in a certain folder provided that some other
     decisive parameter is provided"""
    # typersi will have its own main folder under flagged matches, in this folder it well then create a series of
    # sub-folders in which it will ussually label using the data of creation and within them will lies the compiled
    # files following that day's events
    initial_directory = os.getcwd()
    working_dir = os.path.join(os.path.dirname(__file__), 'files')
    flagging_dir = os.path.join(working_dir, 'flagged')
    typersi_dir = os.path.join(flagging_dir, 'typersi')
    if not os.path.exists(typersi_dir):
        # create the path
        os.chdir(flagging_dir)
        os.mkdir('typersi')
    else:
        os.chdir(typersi_dir)
        today = datetime.today()
        try:
            folder_name = 'typersi{}{}{}'.format(today.day, today.month, today.year)
            os.mkdir(folder_name)
        except OSError:  # check that the folder is already existing
            os.chdir(os.path.join(typersi_dir, folder_name))
            file_handler = open(parameter + '.txt', 'w')
            file_handler.write(string)
            file_handler.close()

    os.chdir(initial_directory)

def get_optimum_three(soup):
    """I think there is a side of this that i think we are not considering,.. instead of randomly picking
    matches whose odds are going to line up with our target how about picking these matches from a more specialised
    pool. A pool that we have also filtered through"""
    # input is from the tipsters with the best efficiency
    list = get_picks_from_tipsters_with_the_best_efficiency(soup)

def stringify_diction_list(diction_list):
    """input a dictionary instance of known format that is then parsed into a string so that it can be written to
     a file.
        temp_diction['tipster_url'] = tipster_url
        temp_diction['tipster_name'] = tipster_name
        temp_diction['time_of_play'] = time_of_play
        temp_diction['home_team'] = home_team
        temp_diction['away_team'] = away_team
        temp_diction['pick'] = pick
        temp_diction['confidence'] = confidence
        temp_diction['odds'] = odds
        return_list.append(temp_diction)"""
    string = ''
    for diction in diction_list:
        print(diction)
        for key in diction.keys():
            string += '{} = {}'.format(key, diction[key])
    return string

def get_all_other_tips():
    """ input: soup object representing the full webpage
    process: retrieve the others link and extract all the other remaining tips
    flagging procedure will be based on the tip that appears more than once."""
    pass

soup = get_home_page()
get_picks_from_tipsters_with_the_best_efficiency(soup)