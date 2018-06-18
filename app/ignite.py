# the launch sequence for normal application functions
# we scrap the matches for the day before and then save those to the database
# we then scrap the matches for today and run the analyser functions for them and save the flagged
import datetime
from .gears.tango import saver  # used for saving past date data
from .gears.analyser import starter  # used for getting the present dates data, analysing and flagging

format = 'http://www.sportstats.com/soccer/matches/20180214/' #yyyymmdd

def recreate_date_query(date_obj):
    """
    :parameter: a date object
    :returns: a string query format
    """
    return date_obj.strftime('%Y%m%d')

def run():
    """takes the yesterday parsed data and saves this to the database ,
    secondaction: analyse todays data and save those that are flagged.
    """
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    
    today_url = 'http://www.sportstats.com/soccer/matches/{}/'.format(recreate_date_query(today))
    yesterday_url = 'http://www.sportstats.com/soccer/matches/{}/'.format(recreate_date_query(yesterday))
    
    saver(yesterday_url)
    starter(today_url)
    
    
def launch():
    # execute the run command at their respective appropriate times
    pass