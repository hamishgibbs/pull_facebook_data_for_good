#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 11:11:56 2020

@author: hamishgibbs
"""


import unittest
import datetime
from colocation import get_file_dates, combine_url, get_urls

class TestColocation(unittest.TestCase):
    
    def setUp(self):
        
        self.date1 = datetime.datetime(2020, 1, 1, 8)
        self.date2 = datetime.datetime(2020, 1, 1, 16)
    
    def test_get_file_dates(self):
        
        self.assertIsInstance(get_file_dates(), list)
        self.assertIsInstance(get_file_dates()[0], datetime.datetime)
    
    def test_combine_url(self):
        
        self.assertIsInstance(combine_url(self.date1, 'url'), str)
    
    def test_get_urls(self):
        
        self.assertIsInstance(get_urls('url', get_file_dates()), list)
        self.assertIsInstance(get_urls('url', get_file_dates())[0], str)