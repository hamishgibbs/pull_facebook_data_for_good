#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 09:20:30 2020

@author: hamishgibbs
"""


import sys
import pandas as pd
from utils import download_data, move_most_recent_files, get_update_date
from population import get_file_dates, get_urls
from datetime import datetime
from getpass import getpass
from itertools import compress

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
    
    #check if updating or downloading full ts
    update = input("Update datasets? (y/n): ")
    
    if update == 'y':
        update = True
    elif update == 'n':
        update = False
    else:
        sys.exit('Unknown update input. Choose "y", "n". Exiting.')
    
    #read target datasets
    data_target = pd.read_csv(_args[1])
    
    for i, dataset_id in enumerate(data_target['id']):
        
        country_output = _args[len(_args) - 1] + "/" + data_target.loc[i, 'country'] + '_population'
            
        base_url = 'https://www.facebook.com/geoinsights-portal/downloads/raster/?id=' + str(dataset_id) + '&ds='
    
        earliest_date = datetime(int(data_target.loc[i, 'year']), int(data_target.loc[i, 'month']), int(data_target.loc[i, 'day']), int(data_target.loc[i, 'hour']))    
        
        data_dates = get_file_dates(earliest_date)
                
        if update:
            data_dates = list(compress(data_dates, [x > get_update_date(country_output) for x in data_dates]))
        
        if len(data_dates) == 0:
            sys.exit('No datasets to download. Exiting.')
            
        urls = get_urls(base_url, data_dates)
        
        start_time = download_data(urls, keys)
    
        move_most_recent_files(country_output, urls, start_time)
    
    print('Success.')

if __name__ == "__main__":
    
    _args = sys.argv
    print(_args)
    main(_args)