import unittest
from app.gears import *
from app import create_app
from app.models import db, Team, League, Match, Country, Flagged
from app.gears.tango import saver, saver_worker, save_team, save_match, save_league, save_country, save_flagged
from app.gears.scrapper import process_team_name
from .match import *


class TangoTests(unittest.TestCase):
    """refer: to app.gear.tango.py"""

    def setUp(self):
        """setup the test database"""
        app = create_app('testing')
        app_context = app.app_context()
        app_context.push()
        db.drop_all()
        db.create_all()


    def tearDown(self):
        """Teardown the test database"""
        db.session.remove()
        db.drop_all()

    def test_saver_function_with_deformed_url(self):
        """if saver was offered a deformed url what does it do"""
        url = "asfbajsdb gaaf a daugf"
        with self.assertRaises(ValueError):
            saver(url)

    def test_saver_function_with_no_url(self):
        """what happens if tango.saver does not recieve this resource"""
        # it should run and requires a connection to the internet
        # 		self.assertTrue(saver())
        # 		self.assertTrue(Matches.query.all())
        pass

    def test_saver_worker_function(self):
        """see how well it responds to well formed data"""
        self.assertFalse(len(Match.query.all()))
        saver_worker(saverdata)
        self.assertTrue(len(Match.query.all()))
        self.assertEqual(1, len(Match.query.all()))

    def test_saver_worker_function_for_absent_data_mutual(self):
        """remove some expected fields and see how well it handles the deformation"""
        self.assertFalse(len(Match.query.all()))
        saver_worker(saverdata)
        self.assertEqual(1, len(Match.query.all()))

    def test_saver_worker_function_for_absent_data_(self):
        """deformed diction, occurence wil be rare"""
        self.assertFalse(len(Match.query.all()))
        saver_worker(saverdatadeformed) # say no date
        self.assertFalse(len(Match.query.all()))
        saver_worker(saverdatadeformed1) # say no country
        self.assertFalse(len(Match.query.all()))
        saver_worker(saverdatadeformed2) # say no league
        self.assertFalse(len(Match.query.all()))

    def test_worker_function_for_repeat_countries(self):
        """can this function detect that we have already added a certain country to our records"""
        self.assertFalse(len(Match.query.all()))
        saver_worker(saverdata)
        self.assertTrue(len(Match.query.all()))
        saver_worker(saverdatacountry)
        self.assertEqual(len(Match.query.all()), 2)
        self.assertEqual(1, len(Country.query.all()))


    def test_worker_function_for_repeat_league(self):
        """in the same spirit, does worker omit already present league names"""
        self.assertFalse(len(Match.query.all()))
        saver_worker(saverdata)
        self.assertTrue(len(Match.query.all()))
        saver_worker(saverdataleague)
        self.assertEqual(len(Match.query.all()), 2)
        self.assertEqual(2, len(League.query.all())) # leagues can be duplicates but only in different countries and
        # not in the same country
        saverdataleague['Country'] = saverdata['country']
        saver_worker(saverdataleague)
        self.assertEqual(len(Match.query.all()), 2)
        self.assertEqual(2, len(League.query.all()))


    def test_worker_function_for_repeated_match(self):
        """what about the same match instances, as it will be so often for mutual matches"""
        self.assertFalse(len(Match.query.all()))
        saver_worker(saverdata)
        self.assertTrue(len(Match.query.all()))
        saver_worker(saverdata)
        self.assertEqual(1, len(Match.query.all()))

    def test_save_country(self):
        """check to see that the system does save country data as it is supposed to"""
        save_country(save['country'])
        self.assertEqual(len(Country.query.all()), 1)
        self.assertEqual(Country.query.all()[0].country_name, save['country'])

    def test_save_country_duplicate_values(self):
        """save country: resave country"""
        save_country(save['country'])
        self.assertEqual(len(Country.query.all()), 1)
        self.assertFalse(save_country(save['country']))
        self.assertEqual(len(Country.query.all()), 1)

    def test_save_league_optimally(self):
        """does the system save league data the way that it is supposed to"""
        save_country(save['country'])
        save_league(save['country'], save['league'])
        self.assertTrue(len(League.query.all()), 1)
        self.assertEqual(League.query.all()[0].league_name, save['league'])

        # now how about those leagues that belong to the same country
        save_league(save['country'], 'league')
        self.assertEqual(len(League.query.all()), 2)
        # load country and confirm that itholds backrefs to the two added leagues
        country = Country.query.filter_by(country_name=save['country']).first()
        self.assertEqual(len(country.leagues), 2)

    def test_save_duplicate_leagues(self):
        """how does the league saver deal with duplicate league entries"""
        save_country(save['country'])
        save_league(save['country'], save['league'])
        self.assertTrue(len(League.query.all()), 1)
        self.assertFalse(save_league(save['country'], save['league']))
        self.assertTrue(len(League.query.all()), 1)
        country = Country.query.filter_by(country_name=save['country']).first()
        self.assertEqual(len(country.leagues), 1)

    def test_save_team_optimally(self):
        """test expectations"""
        save_country(save['country'])
        save_league(save['country'], 'league')
        self.assertFalse(len(Team.query.all()), 0)
        save_team(save['home_team'], save['home_logo_src'])
        self.assertTrue(len(Team.query.all()), 1)
        # add the same team to different leagues and see the response
        save_team(save['home_logo_src'] + 'asd')
        self.assertTrue(len(Team.query.all()), 2)

    def test_save_team_as_duplicate(self):
        """teams cannot be duplicate in the same league otherwise teams
        are not quaranteed to have unique names in a more global scope"""
        self.assertEqual(len(Team.query.all()), 0)
        save_team(save['home_team'], save['home_logo_src'])
        self.assertEqual(len(Team.query.all()), 1)
        self.assertFalse(save_team(save['home_team'], save['home_logo_src']))
        self.assertTrue(len(Team.query.all()), 1)

    def test_save_match_optimally(self):
        """under normal conditions does the save matches function perform as recomended"""
        self.assertFalse(len(Match.query.all()))
        save_match(save)
        self.assertTrue(len(Match.query.all()))

    def test_save_match_with_duplicate_values(self):
        """am getting tired of writing obvious statements such as this"""
        self.assertFalse(len(Match.query.all()))
        save_match(save)
        self.assertTrue(len(Match.query.all()))
        self.assertFalse(save_match(save))
        self.assertEqual(len(Match.query.all()), 1)

    def test_save_flagged_match_function_optimally(self):
        """And here i find myself again"""
        self.assertFalse(len(Flagged.query.all()))
        save_flagged(saveflagged, 'ov')
        self.assertTrue(len(Flagged.query.all()))
        save_flagged(saveflagged)
        self.assertEqual(len(Flagged.query.all()), 1)
        save_flagged(saveflagged, 'gg')
        self.assertEqual(len(Flagged.query.all()), 1)

    def test_save_flagged_match_with_conflicting_markets(self):
        """some markets are mutually exclusive and saving one should override the former"""
        self.assertFalse(len(Flagged.query.all()))
        save_flagged(saveflagged, '1')
        self.assertTrue(len(Flagged.query.all()))
        save_flagged(saveflagged, '2')
        print(Flagged.query.all())
        self.assertEqual(len(Flagged.query.all()), 1)
        self.assertEqual(1, len(Flagged.query.filter(Flagged._2).all()))
        self.assertEqual(0, len(Flagged.query.filter(Flagged._1).all()))


    def test_save_flagged_match_function_for_duplicate_data(self):
        """and you know the drill right"""
        self.assertEqual(len(Flagged.query.all()), 0)
        save_flagged(saveflagged, 'ng')
        self.assertTrue(len(Flagged.query.all()))
        save_flagged(saveflagged, 'ng')
        self.assertEqual(len(Flagged.query.all()), 1)

        # here am going to add two cases that could have easily gone unnoticed
    def test_save_past_matches_in_past_seasons(self):
        """it so happens that my scrap methods will record the same league more than once
        if it has a prefix or suffice of the season"""
        # add a record from a match and then add a mutual match that was played in a past different season
        # check that the league does not increment and the teams too
        self.assertFalse(len(Match.query.all()))
        save_match(ancestralpageplacebo1)
        self.assertTrue(len(Match.query.all()))
        save_match(ancestralpageplacebo2)
        save_match(ancestralpage)
        self.assertEqual(3, len(Match.query.all()))
        self.assertEqual(1 , len(Country.query.all()))
        print(League.query.all())
        self.assertEqual(2, len(League.query.all()))
    # # never checked if the records added to the database was valid data


class TangoSecondary(unittest.TestCase):
    """we are testing two retrieve functions """

    def setUp(self):
        """set up the database as we create an application instance"""
        app = create_app('testing')
        app_context = app.app_context()
        app_context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        """ destroy the tables """
        db.drop_all()

    def test_teams_constraits(self):
        """av purposely decided to introduce a bug here by adding a unoque constraint to the teams"""
        # cannot add teams withe the same name
        self.assertFalse(len(Team.query.all()))
        save_team('SofaPaka')
        self.assertEqual(1, len(Team.query.all()))
        self.assertFalse(save_team( 'Sofapaka'))
        # save_team('Sofapaka')
        self.assertEqual(1, len(Team.query.all()))
        self.assertEqual(2, League.query.all())
        save_team('chemelil')
        self.assertEqual(2, Team.query.all())

    def test_match_constraints(self):
        """added a unique together constraint"""
        # constraint = date + home_team + away_team
        # what happens if only the country is different
        # what happens only if the league is different
        # what happpens only if the time is different
        # what happens if any combination of the above is different
        pass

    def test_league_constraint(self):
        """added a unique together constraint(league and country) to the Leagues"""
        save_league('Kenya', 'Premier League')
        save_league('Kenya', 'Sportpesa Cup')
        self.assertEqual(2, len(League.query.all()))
        save_league('Ethopia', 'Premier League')
        self.assertEqual(2, len(Country.query.all()))
        self.assertEqual(3, len(League.query.all()))
        save_league('Kenya', 'Premier League')
        self.assertEqual(3, len(League.query.all()))

    def test_overall(self):
        """Make sure that the number of reords save in each relation are verified"""
        for diction in diction_list:
            diction['home_team'] = process_team_name(diction['home_team'])
            diction['away_team'] = process_team_name(diction['away_team'])
            saver_worker(diction)
        self.assertEqual(2, len(Country.query.all()))
        self.assertEqual(3, len(League.query.all()))
        self.assertEqual(11, len(Team.query.all()))
        self.assertEqual(len(Match.query.all()), 32)