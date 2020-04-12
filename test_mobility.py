#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 10:53:31 2020

@author: hamishgibbs
"""

import unittest
import datetime
from mobility import get_file_dates, get_url_end, combine_url, get_urls

class TestMobility(unittest.TestCase):
    
    def setUp(self):
        self.date1 = datetime.datetime(2020, 1, 1, 8)
        self.date2 = datetime.datetime(2020, 1, 1, 16)
    
    def test_get_file_dates(self):
        
        self.assertIsInstance(get_file_dates(), list)
        self.assertIsInstance(get_file_dates()[0], datetime.datetime)
    
    def test_get_url_end(self):
        
        self.assertEqual(len(get_url_end(self.date1)), 7)
        self.assertEqual(len(get_url_end(self.date2)), 7)
        
        self.assertEqual(get_url_end(self.date1), '%200800')
        self.assertEqual(get_url_end(self.date2), '%201600')
        
    def test_combine_url(self):
        self.assertIsInstance(combine_url(self.date1, 'url'), str)

    def test_get_urls(self):
        
        self.assertIsInstance(get_urls('url', get_file_dates()), list)
        self.assertIsInstance(get_urls('url', get_file_dates())[0], str)

        
                