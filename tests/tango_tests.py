import unittest
from app.gears import *

class TangoTests(unittest.TestCase):
	"""refer: to app.gear.tango.py"""
	def setUp(self):
		pass
	
	def tearDown(self):
		pass
	
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
		pass
	
	def test_saver_worker_function_for_absent_data(self):
		"""remove some expected fields and see how well it handles the deformation"""
		pass
	
	def test_worker_function_for_repeat_countries(self):
		"""can this function detect that we have already added a certain country to our records"""
		pass
	
	def test_worker_function_for_repeat_league(self):
		"""in the same spirit, does worker omit already present league names"""
		pass
	
	def  test_worker_function_for_repeated_match(self):
		"""what about the same match instances, as it will be so often for mutual matches"""
		pass
	
	def test_worker_function_for_flagged_matches(self):
		"""How polymorphic?.. can we also save data to different model with some simmilarities"""
		pass
	