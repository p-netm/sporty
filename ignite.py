# the launch sequence for normal application functions
# we scrap the matches for the day before and then save those to the database
# we then scrap the matches for today and run the analyser functions for them and save the flagged
import datetime
from app.gears.tango import saver  # used for saving past date data
from app.gears.analyser import starter  # used for getting the present dates data, analysing and flagging

from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()
format = 'http://www.sportstats.com/soccer/matches/20180214/' #yyyymmdd

def recreate_date_query(date_obj):
    """
    :parameter: a date object
    :returns: a string query format
    """
    return date_obj.strftime('%Y%m%d')

def run():
    """takes the yesterday parsed data and saves this to the database ,
    second action: analyse todays data and save those that are flagged.
    """
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    
    today_url = 'http://www.sportstats.com/soccer/matches/{}/'.format(recreate_date_query(today))
    yesterday_url = 'http://www.sportstats.com/soccer/matches/{}/'.format(recreate_date_query(yesterday))
    
    saver(yesterday_url)
    starter(today_url)

@sched.scheduled_job('cron', day_of_week="sun-sat", hour=1)
def scheduled_job():
    run()

sched.start()
