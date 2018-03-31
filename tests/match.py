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
# placebo1 will hold a mutual match not necessarily in the same league but a league with the season suffix
ancestralpageplacebo1 =

#placebo2 will hold a mutual match that holds the same league but without any prefix or suffix
ancestralpageplacebo2 =
ancestralpage = {
    'home_match_goals': 1,
    'home_logo_src': 'http://i.sportstats.com/SY4Ud7Ot-QerFRpgR.png',
    'away_match_goals': 2,
    'home_second_half_goals': None,
    'league': 'OFB Cup 2010/2011',
    'away_team': 'Kapfenberg',
    'date': datetime.date(2010, 8, 13),
    'home_team': 'FAC Wien',
    'home_first_half_goals': None,
    'away_first_half_goals': None,
    'away_second_half_goals': None,
    'country':'Austria',
    'away_logo_src':'http://i.sportstats.com/CQfdaCiQ-phgpt3Fq.png',
    'time':datetime.time(20, 0)
}  # for the tango test

########################################################################################################################

# fac wien home
links = '''http://www.sportstats.com/soccer/austria/erste-liga/floridsdorfer-ac-wien-neustadt-fNmNoOXm/
http://www.sportstats.com/soccer/austria/erste-liga/floridsdorfer-ac-wien-a-lustenau-2i9pxE4M/
http://www.sportstats.com/soccer/austria/erste-liga/floridsdorfer-ac-wien-bw-linz-OtnaQG5A/
http://www.sportstats.com/soccer/austria/erste-liga/floridsdorfer-ac-wien-fc-liefering-YwEDEJ6b/
http://www.sportstats.com/soccer/austria/erste-liga/floridsdorfer-ac-wien-ried-pfoLCxKD/
http://www.sportstats.com/soccer/austria/erste-liga/floridsdorfer-ac-wien-hartberg-4vj0H05r/
http://www.sportstats.com/soccer/austria/erste-liga/floridsdorfer-ac-wien-wacker-innsbruck-SzUe8NSR/
http://www.sportstats.com/soccer/austria/erste-liga/floridsdorfer-ac-wien-kapfenberg-OrB9dQTF/
#fac wien home from 2012

# fac wien away
http://www.sportstats.com/soccer/austria/erste-liga/fc-liefering-floridsdorfer-ac-wien-UutzqMH6/
http://www.sportstats.com/soccer/austria/erste-liga/ried-floridsdorfer-ac-wien-AcWBhZl3/
http://www.sportstats.com/soccer/world/club-friendly/austria-vienna-floridsdorfer-ac-wien-Aw0IPj0F/
http://www.sportstats.com/soccer/austria/erste-liga/hartberg-floridsdorfer-ac-wien-dfS7gFZd/
http://www.sportstats.com/soccer/austria/erste-liga/wacker-innsbruck-floridsdorfer-ac-wien-llqBNEkT/
# fac wien away from 2012

# kapfenburg away
http://www.sportstats.com/soccer/austria/erste-liga/wattens-kapfenberg-rBUJjDJF/
http://www.sportstats.com/soccer/austria/erste-liga/a-lustenau-kapfenberg-8SWp5CY8/
http://www.sportstats.com/soccer/austria/erste-liga/wacker-innsbruck-kapfenberg-GbkLVBsj/
http://www.sportstats.com/soccer/austria/erste-liga/ried-kapfenberg-2Xp3PzLG/
http://www.sportstats.com/soccer/austria/erste-liga/neustadt-kapfenberg-fmF9Faih/
http://www.sportstats.com/soccer/austria/erste-liga/bw-linz-kapfenberg-b11yFS0s/
# kapfenburg home
http://www.sportstats.com/soccer/austria/erste-liga/kapfenberg-bw-linz-2VuerkRe/
http://www.sportstats.com/soccer/austria/erste-liga/kapfenberg-neustadt-x6qrs0nJ/
http://www.sportstats.com/soccer/austria/erste-liga/kapfenberg-fc-liefering-df6xvzzA/
http://www.sportstats.com/soccer/austria/erste-liga/kapfenberg-hartberg-SEhjSxyb/
http://www.sportstats.com/soccer/austria/erste-liga/kapfenberg-floridsdorfer-ac-wien-GzPX9eLT/
http://www.sportstats.com/soccer/austria/erste-liga/kapfenberg-a-lustenau-8hAkA4FC/

# mutualmatches
http://www.sportstats.com/soccer/austria/erste-liga/kapfenberg-floridsdorfer-ac-wien-GzPX9eLT/
http://www.sportstats.com/soccer/austria/erste-liga/floridsdorfer-ac-wien-kapfenberg-OrB9dQTF/
http://www.sportstats.com/soccer/austria/erste-liga-2016-2017/floridsdorfer-ac-wien-kapfenberg-WrXZ49VD/
http://www.sportstats.com/soccer/austria/erste-liga-2016-2017/kapfenberg-floridsdorfer-ac-wien-CIYKZrK5/
http://www.sportstats.com/soccer/austria/erste-liga-2016-2017/floridsdorfer-ac-wien-kapfenberg-d6Cf6Mgi/
http://www.sportstats.com/soccer/austria/erste-liga-2016-2017/kapfenberg-floridsdorfer-ac-wien-dWJiTRvq/
http://www.sportstats.com/soccer/austria/erste-liga-2015-2016/kapfenberg-floridsdorfer-ac-wien-jguXXEMs/
http://www.sportstats.com/soccer/austria/erste-liga-2015-2016/floridsdorfer-ac-wien-kapfenberg-lSVH1jtn/
#mutualmatches before 2012
http://www.sportstats.com/soccer/austria/ofb-cup-2010-2011/floridsdorfer-ac-wien-kapfenberg-dGx08q4r/'''

diction_list = []