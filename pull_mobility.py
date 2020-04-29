#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 20:48:26 2020

@author: hamishgibbs
"""

import sys
import pandas as pd
from utils import download_data, move_most_recent_files
from mobility import get_file_dates, get_urls
from datetime import datetime
from getpass import getpass

def main(_args):
    '''
    download colocation data
    
    Parameters
    ----------
    _args : listx
        Arg list secret_key, username and pass dir, csv file specifying download countries and ids, outdir.

    Returns
    -------
    None.

    '''
    
    
    username = input("Username: ")
        
    password = getpass()
    
    keys = [username, password]
    
    #read target datasets
    data_target = pd.read_csv(_args[3])
    
    for i, dataset_id in enumerate(data_target['id']):
            
        base_url = 'https://www.facebook.com/geoinsights-portal/downloads/vector/?id=' + str(dataset_id) + '&ds='
    
        earliest_date = datetime(int(data_target.loc[i, 'year']), int(data_target.loc[i, 'month']), int(data_target.loc[i, 'day']), int(data_target.loc[i, 'hour']))    
        
        data_dates = get_file_dates(earliest_date)
        urls = get_urls(base_url, data_dates)
        
        download_data(urls, keys)
        
    
        move_most_recent_files(_args[len(_args) - 1] + "/" + data_target.loc[i, 'country'] + '_mobility', urls)
    
    print('Success.')

if __name__ == "__main__":
    
    _args = sys.argv
    print(_args)
    main(_args)