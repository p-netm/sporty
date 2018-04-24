import unittest
from .analysertestdata import *
from app.gears.analyser import ov, un, gg, ng

class AnalyserTests(unittest.TestCase):

    def test_ov_function_with_full_data(self):
        """"all dictionary fields are well supplied with the required data"""
        self.assertTrue(ov(qualifiedov))

    def test_un_function_with_full_data(self):
        """"all dictionary fields are well supplied with the required data"""
        self.assertTrue(un(qualifiedun))
        
    def test_gg_function_with_full_data(self):
        """"all dictionary fields are well supplied with the required data"""
        self.assertTrue(gg(qualifiedgg))

    def test_ng_function_with_full_data(self):
        """"all dictionary fields are well supplied with the required data"""
        self.assertTrue(ng(qualifiedng))

    def test_recent_evaluator(self):
        """"the abstraction"""
        pass
    
    def test_basic_threshhold_limit_for_ov(self):
        """"""
        self.assertTrue(ov(abovethreshov))
        self.assertFalse(ov(belowthreshov))
        
    def test_basic_threshhold_limit_for_un(self):
        """"""
        self.assertTrue(un(abovethreshun))
        self.assertFalse(un(belowthreshun))
        
    def test_basic_threshhold_limit_for_gg(self):
        self.assertTrue(gg(abovethreshgg))
        self.assertFalse(gg(belowthreshgg))
        
    def test_basic_threshhold_limit_for_ng(self):
        self.assertTrue(ng(abovethreshng))
        self.assertFalse(ng(belowthreshng))