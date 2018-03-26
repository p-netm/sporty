import datetime
import copy
saverdata = {  
   "home_team":"Corinthians",
   "home_logo_src":"http://i.sportstats.com/EJjZAohQ-4GpinQcR.png",
   "time":datetime.time(0, 0),
   "away_logo_src":"http://i.sportstats.com/ObzPomjQ-S2oksqYj.png",
   "away_first_half_goals":0,
   "away_match_goals":0,
   "league":"Campeonato Paulista",
   "home_first_half_goals":2,
   "country":"Brazil",
   "away_team":"Bragantino",
   "date":datetime.date(2018, 3, 23),
   "home_match_goals":2,
   "away_second_half_goals":0,
   "home_second_half_goals":0
}
saverdatadeformed = {  
   "home_team":"Corinthians",
   "home_logo_src":"http://i.sportstats.com/EJjZAohQ-4GpinQcR.png",
   "time":datetime.time(0, 0),
   "away_logo_src":"http://i.sportstats.com/ObzPomjQ-S2oksqYj.png",
   "away_first_half_goals":0,
   "away_match_goals":0,
   "league":"Campeonato Paulista",
   "home_first_half_goals":2,
   "country":"Brazil",
   "away_team":"Bragantino",
   "home_match_goals":2,
   "away_second_half_goals":0,
   "home_second_half_goals":0
}
saverdatadeformed1 = {  
   "home_team":"Corinthians",
   "home_logo_src":"http://i.sportstats.com/EJjZAohQ-4GpinQcR.png",
   "time":datetime.time(0, 0),
   "away_logo_src":"http://i.sportstats.com/ObzPomjQ-S2oksqYj.png",
   "away_first_half_goals":0,
   "away_match_goals":0,
   "league":"Campeonato Paulista",
   "home_first_half_goals":2,
   "away_team":"Bragantino",
   "date":datetime.date(2018, 3, 23),
   "home_match_goals":2,
   "away_second_half_goals":0,
   "home_second_half_goals":0
}
saverdatadeformed2 = {  
   "home_team":"Corinthians",
   "home_logo_src":"http://i.sportstats.com/EJjZAohQ-4GpinQcR.png",
   "time":datetime.time(0, 0),
   "away_logo_src":"http://i.sportstats.com/ObzPomjQ-S2oksqYj.png",
   "away_first_half_goals":0,
   "away_match_goals":0,
   "home_first_half_goals":2,
   "country":"Brazil",
   "away_team":"Bragantino",
   "date":datetime.date(2018, 3, 23),
   "home_match_goals":2,
   "away_second_half_goals":0,
   "home_second_half_goals":0
}
saverdatacountry= {  
   'away_first_half_goals':1,
   'home_team':'Boca Unidos',
   'time':datetime.time(0, 0),
   'away_team':'Club Atletico Mitre',
   'home_first_half_goals':0,
   'country':'Brazil',
   'home_match_goals':1,
   'away_logo_src':'http://i.sportstats.com/fkdoMcoh-OSNzaEMG.png',
   'away_second_half_goals':1,
   'away_match_goals':2,
   'home_logo_src':'http://i.sportstats.com/IRUMW9WE-Sl6NCk6r.png',
   'home_second_half_goals':1,
   'league':'Primera B Nacional',
   'date':datetime.date(2018, 3, 26)
}
saverdataleague= {  
   'away_first_half_goals':1,
   'home_team':'Boca Unidos',
   'time':datetime.time(0, 0),
   'away_team':'Club Atletico Mitre',
   'home_first_half_goals':0,
   'country':'Argentina',
   'home_match_goals':1,
   'away_logo_src':'http://i.sportstats.com/fkdoMcoh-OSNzaEMG.png',
   'away_second_half_goals':1,
   'away_match_goals':2,
   'home_logo_src':'http://i.sportstats.com/IRUMW9WE-Sl6NCk6r.png',
   'home_second_half_goals':1,
   "league":"Campeonato Paulista",
   'date':datetime.date(2018, 3, 26)
}
save = copy.deepcopy(saverdata)
saveflagged = {  
   'away_first_half_goals':None,
   'home_team':'Portugal',
   'time':datetime.time(20, 30),
   'away_team':'Netherlands',
   'home_first_half_goals':None,
   'country':'World',
   'home_match_goals':None,
   'away_logo_src':'http://i.sportstats.com/hM4ITqUE-hfYFp0jk.png',
   'away_second_half_goals':None,
   'away_match_goals':None,
   'home_logo_src':'http://i.sportstats.com/nFK0QOCK-OS1AyatK.png',
   'home_second_half_goals':None,
   'league':'Friendly International',
   'date':datetime.date(2018, 3, 26)
}

{  
   "mutual":[  
      {  
         "home_team":"Corinthians",
         "home_logo_src":"http://i.sportstats.com/EJjZAohQ-4GpinQcR.png",
         "time":datetime.time(0, 0),
         "away_logo_src":"http://i.sportstats.com/ObzPomjQ-S2oksqYj.png",
         "away_first_half_goals":0,
         "away_match_goals":0,
         "league":"Campeonato Paulista",
         "home_first_half_goals":2,
         "country":"Brazil",
         "away_team":"Bragantino",
         "date":datetime.date(2018, 3, 23),
         "home_match_goals":2,
         "away_second_half_goals":0,
         "home_second_half_goals":0
      },
      {  
         "home_team":"Corinthians",
         "home_logo_src":"http://i.sportstats.com/EJjZAohQ-4GpinQcR.png",
         "time":datetime.time(0, 0),
         "away_logo_src":"http://i.sportstats.com/ObzPomjQ-S2oksqYj.png",
         "away_first_half_goals":0,
         "away_match_goals":0,
         "league":"Campeonato Paulista",
         "home_first_half_goals":2,
         "country":"Brazil",
         "away_team":"Bragantino",
         "date":datetime.date(2018, 3, 23),
         "home_match_goals":2,
         "away_second_half_goals":0,
         "home_second_half_goals":0
      },
      {  
         "home_team":"Corinthians",
         "home_logo_src":"http://i.sportstats.com/EJjZAohQ-4GpinQcR.png",
         "time":datetime.time(0, 0),
         "away_logo_src":"http://i.sportstats.com/ObzPomjQ-S2oksqYj.png",
         "away_first_half_goals":0,
         "away_match_goals":0,
         "league":"Campeonato Paulista",
         "home_first_half_goals":2,
         "country":"Brazil",
         "away_team":"Bragantino",
         "date":datetime.date(2018, 3, 23),
         "home_match_goals":2,
         "away_second_half_goals":0,
         "home_second_half_goals":0
      },
      {  
         "home_team":"Corinthians",
         "home_logo_src":"http://i.sportstats.com/EJjZAohQ-4GpinQcR.png",
         "time":datetime.time(0, 0),
         "away_logo_src":"http://i.sportstats.com/ObzPomjQ-S2oksqYj.png",
         "away_first_half_goals":0,
         "away_match_goals":0,
         "league":"Campeonato Paulista",
         "home_first_half_goals":2,
         "country":"Brazil",
         "away_team":"Bragantino",
         "date":datetime.date(2018, 3, 23),
         "home_match_goals":2,
         "away_second_half_goals":0,
         "home_second_half_goals":0
      },
      {  
         "home_team":"Corinthians",
         "home_logo_src":"http://i.sportstats.com/EJjZAohQ-4GpinQcR.png",
         "time":datetime.time(0, 0),
         "away_logo_src":"http://i.sportstats.com/ObzPomjQ-S2oksqYj.png",
         "away_first_half_goals":0,
         "away_match_goals":0,
         "league":"Campeonato Paulista",
         "home_first_half_goals":2,
         "country":"Brazil",
         "away_team":"Bragantino",
         "date":datetime.date(2018, 3, 23),
         "home_match_goals":2,
         "away_second_half_goals":0,
         "home_second_half_goals":0
      },
      {  
         "home_team":"Corinthians",
         "home_logo_src":"http://i.sportstats.com/EJjZAohQ-4GpinQcR.png",
         "time":datetime.time(0, 0),
         "away_logo_src":"http://i.sportstats.com/ObzPomjQ-S2oksqYj.png",
         "away_first_half_goals":0,
         "away_match_goals":0,
         "league":"Campeonato Paulista",
         "home_first_half_goals":2,
         "country":"Brazil",
         "away_team":"Bragantino",
         "date":datetime.date(2018, 3, 23),
         "home_match_goals":2,
         "away_second_half_goals":0,
         "home_second_half_goals":0
      }
   ]
}