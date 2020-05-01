#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 10:03:05 2020

@author: hamishgibbs
"""

import os
import shutil
import unittest
import pandas as pd
from datetime import datetime
from utils import try_mkdir_silent, rename_and_move, move_most_recent_files, get_home_dir, get_new_file_name, get_update_date


class TestUtils(unittest.TestCase):
    
    def setUp(self):
        try_mkdir_silent('./tmp1')
        try_mkdir_silent('./tmp2')
        
    def test_get_home_dir(self):
        self.assertTrue('~' not in get_home_dir())
                                  
    def test_try_mkdir_silent(self):
        self.assertTrue(os.path.exists('./tmp1'))
        self.assertTrue(os.path.exists('./tmp2'))
        
    def test_rename_and_move(self):
        
        self.data = pd.DataFrame({'data':[1, 2, 3, 4, 5]})
        self.data.to_csv('./tmp1/test.csv')    
        
        self.assertTrue(os.path.exists('./tmp1/test.csv'))
        rename_and_move('test.csv', './tmp1', 'test_move.csv', './tmp2')
        self.assertTrue(os.path.exists('./tmp2/test_move.csv'))
        
    def test_move_most_recent_files(self):
        
        self.data1 = pd.DataFrame({'data':[1, 2, 3, 4, 5]})
        self.data1.to_csv(get_home_dir() + '/Downloads/test1.csv') 
        
        self.data2 = pd.DataFrame({'data':[1, 2, 3, 4, 5]})
        self.data2.to_csv(get_home_dir() + '/Downloads/Britain Coronavirus Disease Prevention Map Mar 06 2020 Id Id Colocation Map_2020-03-31.csv') 

        self.assertTrue(os.path.exists(get_home_dir() + '/Downloads/test1.csv'))
        self.assertTrue(os.path.exists(get_home_dir() + '/Downloads/Britain Coronavirus Disease Prevention Map Mar 06 2020 Id Id Colocation Map_2020-03-31.csv'))

        move_most_recent_files('./tmp1', ['url'])

        self.assertTrue(os.path.exists(get_home_dir() + '/Downloads/test1.csv'))
        self.assertTrue(os.path.exists('./tmp1/Britain_2020_03_31.csv'))

        
        os.remove(get_home_dir() + '/Downloads/test1.csv')
        
    def test_get_new_file_name(self):
        
        self.colocation_fn = 'Britain Coronavirus Disease Prevention Map Mar 06 2020 Id Id Colocation Map_2020-03-31.csv'
        self.mobility_fn = 'Britain Coronavirus Disease Prevention Map Mar 06 2020 Id Id  Movement between Tiles_2020-03-10 0000.csv'

        self.assertEqual(get_new_file_name(self.colocation_fn), 'Britain_2020_03_31.csv')
        self.assertEqual(get_new_file_name(self.mobility_fn), 'Britain_2020_03_10_0000.csv')
        
    def test_get_update_date(self):
        
        self.data = pd.DataFrame({'data':[1, 2, 3, 4, 5]})
        
        self.assertRaises(ValueError, get_update_date, './tmp1')
        
        self.data.to_csv('./tmp1/test.csv')
        
        self.assertIsInstance(get_update_date('./tmp1'), datetime)
        
        
    def tearDown(self):
        shutil.rmtree('./tmp1')
        shutil.rmtree('./tmp2')

    
