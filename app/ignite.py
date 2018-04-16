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

def launch():
    """the launch populates the database far back from a 30 days from the past"""
    today = datetime.date.today()
