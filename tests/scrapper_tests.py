"""
		Solely test the scrapper functionality
"""
import unittest
import os, BeautifulSoup, datetime
from app.gears.scrapper import scrap_all_urls, date_from_string
from validator import url

def create_file_path(filename):
	"""abstract the path creation to the golden files"""
	base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'files', 'goldenfiles')
	if isinstance(filename, str):
		return os.path.join(base_dir, filename)
	else:
		raise TypeError("Filename is {}, expecting str".format(type(filename)))

class Reckless(unittest.TestCase):
	
	def test_create_file_path(self):
		"""check that any file path returned by the above function exists and that it is a html file"""
		path = create_file_path('nonesense')
		self.assertFalse(os.path.exists(path))
		path = create_file_path('awarded.html')
		self.assertTrue(os.path.exists(path))
	
	

class ScrapperTest(unittest.TestCase):
	""":Focus: the module app.gear.scrapper full functions"""
	def setUp(self):
		pass
	
	def tearDown(self):
		pass
	
	def test_scrap_all_links(self):
		"""See if the scrap dows return the expected number of links and also 
		evaluate how well it handles errors.
		"""
		# here i check only for  the expected number of links
		present_scrap = scrap_all_urls(create_file_path('present_soccer_home.html'))
		self.assertIsInstance(present_scrap, list)
		# each scrapped element is a full blown valid url without the #odds
		self.assertTrue(url(present_scrap[0]))
		self.assertTrue(url(present_scrap[2]))
		# should not have the fragment $odds at the end of the url
		sample_url = present_scrap[0]
		self.assertEqual(sample_url.find('#odds'), -1)
		self.assertEqual(len(present_scrap), 200)
		self.assertEqual(len(scrap_all_urls(create_file_path('past_soccer_home.html'))), 1037)
		self.assertEqual(len(scrap_all_urls(create_file_path('future_soccer_home.html'))), 200)
		
	def test_date_from_string(self):
		"""refer to method declaration"""
		sample_string = 'Today, 26 Jun 2017, 00:00++++'
		deformed_string = 'Today, 26 Jun 207, 00:00++++'
		time_deformed_string = 'Today, 26 Jun 2017, 0:00++++'
		no_effect=' 26 Jun 2017, 00:00++++'
		date = datetime.date(2018, 6, 26)
		time = datetime.time()
		self.assertIsInstance(date_from_string(sample_string), tuple)
		self.assertIsInstance(date_from_string(no_effect), tuple)
		with self.assertRaises(PatternMatchError):
			date_from_string(deformed_string)
			date_from_string(time_deformed_string)
		self.assertIsInstance(date_from_string(sample_string)[0], datetime.date)
		self.assertIsInstance(date_from_string(sample_string)[1], datetime.time)
		
	def test_get_specific_match_details(self):
		"""This is more than a unit test"""
		