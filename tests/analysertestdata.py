import datetime, unittest, copy
######################################## Analyser test data ############################################################
templatedata = {
    'home': [
                {  
                    'away_first_half_goals':0,
                    'home_first_half_goals':1,
                    'away_match_goals':0,
                    'date':datetime.date(2018,
                    3,
                    16    ),
                    'home_second_half_goals':0,
                    'home_team':'Liefering',
                    'away_second_half_goals':0,
                    'time':datetime.time(18,
                    30    ),
                    'home_match_goals':1,
                    'away_team':'FAC Wien'
                },
                {  
                    'away_first_half_goals':3,
                    'home_first_half_goals':0,
                    'away_match_goals':3,
                    'date':datetime.date(2018,
                    3,
                    9    ),
                    'home_second_half_goals':0,
                    'home_team':'FAC Wien',
                    'away_second_half_goals':0,
                    'time':datetime.time(18,
                    30    ),
                    'home_match_goals':0,
                    'away_team':'Neustadt'
                },
                {  
                    'away_first_half_goals':0,
                    'home_first_half_goals':0,
                    'away_match_goals':1,
                    'date':datetime.date(2018,
                    2,
                    23    ),
                    'home_second_half_goals':1,
                    'home_team':'Ried',
                    'away_second_half_goals':1,
                    'time':datetime.time(18,
                    30    ),
                    'home_match_goals':1,
                    'away_team':'FAC Wien'
                },
                {  
                    'away_first_half_goals':0,
                    'home_first_half_goals':0,
                    'away_match_goals':1,
                    'date':datetime.date(2018,
                    1,
                    16    ),
                    'home_second_half_goals':1,
                    'home_team':'Austria Vienna',
                    'away_second_half_goals':1,
                    'time':datetime.time(14,
                    30    ),
                    'home_match_goals':1,
                    'away_team':'FAC Wien'
                },
                {  
                    'away_first_half_goals':1,
                    'home_first_half_goals':1,
                    'away_match_goals':2,
                    'date':datetime.date(2017,
                    12,
                    1    ),
                    'home_second_half_goals':0,
                    'home_team':'Hartberg',
                    'away_second_half_goals':1,
                    'time':datetime.time(18,
                    30    ),
                    'home_match_goals':1,
                    'away_team':'FAC Wien'
                }
    ],
    'away': [
                {  
                    'away_first_half_goals':2,
                    'home_first_half_goals':0,
                    'away_match_goals':4,
                    'date':datetime.date(2018,
                    3,
                    20    ),
                    'home_second_half_goals':1,
                    'home_team':'Kapfenberg',
                    'away_second_half_goals':2,
                    'time':datetime.time(18,
                    30    ),
                    'home_match_goals':1,
                    'away_team':'BW Linz'
                },
                {  
                    'away_first_half_goals':0,
                    'home_first_half_goals':0,
                    'away_match_goals':0,
                    'date':datetime.date(2018,
                    3,
                    16    ),
                    'home_second_half_goals':0,
                    'home_team':'Kapfenberg',
                    'away_second_half_goals':0,
                    'time':datetime.time(18,
                    30    ),
                    'home_match_goals':0,
                    'away_team':'Neustadt'
                },
                {  
                    'away_first_half_goals':2,
                    'home_first_half_goals':2,
                    'away_match_goals':2,
                    'date':datetime.date(2018,
                    3,
                    12    ),
                    'home_second_half_goals':1,
                    'home_team':'Wattens',
                    'away_second_half_goals':0,
                    'time':datetime.time(18,
                    30    ),
                    'home_match_goals':3,
                    'away_team':'Kapfenberg'
                },
                {  
                    'away_first_half_goals':1,
                    'home_first_half_goals':0,
                    'away_match_goals':1,
                    'date':datetime.date(2018,
                    3,
                    9    ),
                    'home_second_half_goals':3,
                    'home_team':'A. Lustenau',
                    'away_second_half_goals':0,
                    'time':datetime.time(18,
                    30    ),
                    'home_match_goals':3,
                    'away_team':'Kapfenberg'
                },
                {  
                    'away_first_half_goals':1,
                    'home_first_half_goals':1,
                    'away_match_goals':1,
                    'date':datetime.date(2017,
                    12,
                    1    ),
                    'home_second_half_goals':0,
                    'home_team':'Wacker Innsbruck',
                    'away_second_half_goals':0,
                    'time':datetime.time(18,
                    30    ),
                    'home_match_goals':1,
                    'away_team':'Kapfenberg'
                }
    ],
    'mutual': [
        {  
           'away_first_half_goals':0,
           'home_first_half_goals':2,
           'away_match_goals':1,
           'date':datetime.date(2017,
           10,
           31   ),
           'home_second_half_goals':2,
           'home_team':'Kapfenberg',
           'away_second_half_goals':1,
           'time':datetime.time(18,
           30   ),
           'home_match_goals':4,
           'away_team':'FAC Wien'
        },
        {  
           'away_first_half_goals':2,
           'home_first_half_goals':0,
           'away_match_goals':3,
           'date':datetime.date(2017,
           8,
           18   ),
           'home_second_half_goals':0,
           'home_team':'FAC Wien',
           'away_second_half_goals':1,
           'time':datetime.time(18,
           30   ),
           'home_match_goals':0,
           'away_team':'Kapfenberg'
        },
        {  
           'away_first_half_goals':0,
           'home_first_half_goals':2,
           'away_match_goals':1,
           'date':datetime.date(2017,
           5,
           26   ),
           'home_second_half_goals':1,
           'home_team':'FAC Wien',
           'away_second_half_goals':1,
           'time':datetime.time(19,
           30   ),
           'home_match_goals':3,
           'away_team':'Kapfenberg'
        },
        {  
           'away_first_half_goals':0,
           'home_first_half_goals':0,
           'away_match_goals':1,
           'date':datetime.date(2017,
           4,
           8   ),
           'home_second_half_goals':0,
           'home_team':'Kapfenberg',
           'away_second_half_goals':1,
           'time':datetime.time(16,
           0   ),
           'home_match_goals':0,
           'away_team':'FAC Wien'
        },
        {  
           'away_first_half_goals':0,
           'home_first_half_goals':0,
           'away_match_goals':1,
           'date':datetime.date(2016,
           11,
           18   ),
           'home_second_half_goals':0,
           'home_team':'FAC Wien',
           'away_second_half_goals':1,
           'time':datetime.time(18,
           30   ),
           'home_match_goals':0,
           'away_team':'Kapfenberg'
        },
        {  
           'away_first_half_goals':0,
           'home_first_half_goals':0,
           'away_match_goals':0,
           'date':datetime.date(2016,
           9,
           13   ),
           'home_second_half_goals':2,
           'home_team':'Kapfenberg',
           'away_second_half_goals':0,
           'time':datetime.time(18,
           30   ),
           'home_match_goals':2,
           'away_team':'FAC Wien'
        }
    ]
}

# we use the above data as template data from which we can define generators that will dynamically give us the test 
# that we need
qualifiedov = {'home': [], 'away': [], 'mutual': []}

def looper(template_list, home_score, away_score, home_placebo=None, away_placebo=None, limit=None):
    # dict list is the template dctionary lists,
    # while the target_list is the qualified series of lists
    def inloop(template, home_score, away_score, limit=limit, home_placebo=home_placebo, away_placebo=away_placebo):
        if limit is None: limit = len(template)
        target = []
        for diction in template[:limit]:
            #create a copy of the same and then modify the dictionary in the copy
            _dict = copy.deepcopy(diction)
            _dict['home_match_goals'] = home_score
            _dict['away_match_goals'] = away_score
            target.append(_dict)
        for diction in template[limit:len(template)]:
            _dict = copy.deepcopy(diction)
            _dict['home_match_goals'] = home_placebo
            _dict['away_match_goals'] = away_placebo
            target.append(_dict)
        return target
    return inloop(template_list, home_score, away_score)

qualifiedov['home'] = looper(templatedata['home'], 3, 0)
qualifiedov['away'] = looper(templatedata['away'], 3, 0)
qualifiedov['mutual'] = looper(templatedata['mutual'], 3, 0)

qualifiedun = {'home': [], 'away': [], 'mutual': []}
qualifiedun['home'] = looper(templatedata['home'], 2, 0)
qualifiedun['away'] = looper(templatedata['away'], 2, 0)
qualifiedun['mutual'] = looper(templatedata['mutual'], 2, 0)

qualifiedgg = {'home': [], 'away': [], 'mutual': []}
qualifiedgg['home'] = looper(templatedata['home'], 1, 1)
qualifiedgg['away'] = looper(templatedata['away'], 1, 1)
qualifiedgg['mutual'] = looper(templatedata['mutual'], 1, 1)

qualifiedng = {'home': [], 'away': [], 'mutual': []}
qualifiedng['home'] = looper(templatedata['home'], 1, 0)
qualifiedng['away'] = looper(templatedata['away'], 1, 0)
qualifiedng['mutual'] = looper(templatedata['mutual'], 1, 0)

        ################just above threshhold###################

abovethreshov = {'home': [], 'away': [], 'mutual': []}
abovethreshov['home'] = looper(templatedata['home'], 3, 0, 2, 0, 4)
abovethreshov['away'] = looper(templatedata['away'], 3, 0, 2, 0, 4)
abovethreshov['mutual'] = looper(templatedata['mutual'], 3, 0, 2, 0, 5)

belowthreshov = {'home': [], 'away': [], 'mutual': []}
belowthreshov['home'] = looper(templatedata['home'], 3, 0, 2, 0, 3)
belowthreshov['away'] = looper(templatedata['away'], 3, 0, 2, 0, 3)
belowthreshov['mutual'] = looper(templatedata['mutual'], 3, 0, 2, 0, 4)

abovethreshun = {'home': [], 'away': [], 'mutual': []}
abovethreshun['home'] = looper(templatedata['home'], 2, 0, 3, 0, 4)
abovethreshun['away'] = looper(templatedata['away'], 2, 0, 3, 0, 4)
abovethreshun['mutual'] = looper(templatedata['mutual'], 2, 0, 3, 0, 5)

belowthreshun = {'home': [], 'away': [], 'mutual': []}
belowthreshun['home'] = looper(templatedata['home'], 2, 0, 3, 0, 3)
belowthreshun['away'] = looper(templatedata['away'], 2, 0, 3, 0, 3)
belowthreshun['mutual'] = looper(templatedata['mutual'], 2, 0, 3, 0, 4)

abovethreshgg = {'home': [], 'away': [], 'mutual': []}
abovethreshgg['home'] = looper(templatedata['home'], 1, 1, 1, 0, 4)
abovethreshgg['away'] = looper(templatedata['away'], 1, 1, 1, 0, 4)
abovethreshgg['mutual'] = looper(templatedata['mutual'], 1, 1, 1, 0, 5)

abovethreshng = {'home': [], 'away': [], 'mutual': []}
abovethreshng['home'] = looper(templatedata['home'], 1, 0, 1, 1, 4)
abovethreshng['away'] = looper(templatedata['away'], 1, 0, 1, 1, 4)
abovethreshng['mutual'] = looper(templatedata['mutual'], 1, 0, 1, 1, 5)

belowthreshgg = {'home': [], 'away': [], 'mutual': []}
belowthreshgg['home'] = looper(templatedata['home'], 1, 1, 1, 0, 3)
belowthreshgg['away'] = looper(templatedata['away'], 1, 1, 1, 0, 3)
belowthreshgg['mutual'] = looper(templatedata['mutual'], 1, 1, 1, 0, 4)

belowthreshng = {'home': [], 'away': [], 'mutual': []}
belowthreshng['home'] = looper(templatedata['home'], 1, 0, 1, 1, 3)
belowthreshng['away'] = looper(templatedata['away'], 1, 0, 1, 1, 3)
belowthreshng['mutual'] = looper(templatedata['mutual'], 1, 0, 1, 1, 4)

def display(dictionary):
    # for debugging purposes, will print the computed scores of the above derived dictionaries
    for key, value in dictionary.items():
        for diction in value:
            print(diction['home_match_goals'], diction['away_match_goals'])

######################################## End of anayleser test data ##################################################

#should test this funtion here, we dont want to use faulted testdata, there is no worser tragedy.
                
class LooperTest(unittest.TestCase):
    
    def assertThings(self, dictionary, home_score, away_score):
        """structure of dictionary as parameter, with keys and values as lists"""
        for key, value in dictionary.items():
                for diction in value:
                    self.assertEqual(diction['home_match_goals'], home_score)
                    self.assertEqual(diction['away_match_goals'], away_score)
                    
    def test_looper_function_used_above(self):
        """the looper function used to automate the creation of testdata"""
        self.assertThings(qualifiedov, 3, 0)
        self.assertThings(qualifiedun, 2, 0)
        self.assertThings(qualifiedgg, 1, 1)
        self.assertThings(qualifiedng, 1, 0)
        
    def test_looper_functin_does_not_have_side_effects_on_template_data(self):
        """Ensures that the template data remains unchanged in the course of the looper function"""
        home_scores_list = []
        away_scores_list = []
        mutual_scores_list = []
        
        def render_scores(template_list, target_list):
            for diction in template_list[0:3]:
                target_list.extend([diction['home_match_goals'], diction['away_match_goals']])
                
        render_scores(templatedata['home'], home_scores_list)
        render_scores(templatedata['away'], away_scores_list)
        render_scores(templatedata['mutual'], mutual_scores_list)
        self.assertListEqual(home_scores_list, [1, 0, 0, 3, 1, 1])
        self.assertListEqual(away_scores_list, [1, 4, 0, 0, 3, 2])
        self.assertListEqual(mutual_scores_list, [4, 1, 0, 3, 3, 1])
        