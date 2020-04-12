#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 20:04:22 2020

@author: hamishgibbs
"""

from datetime import datetime
from datetime import timedelta

def get_file_dates(earliest_date):
    '''
    get dates of each dataset

    Returns
    -------
    dataset dates.

    '''
        
    data_dates = []
    date = earliest_date
    while date < datetime.now():
        data_dates.append(date)
        date = date + timedelta(days=7)
        
    return(data_dates)


def get_urls(base_url: str, data_dates: list):
    '''
    combine base url with dates

    Parameters
    ----------
    base_url : str
        base url.
    data_dates : list
        list of dataset dates.

    Returns
    -------
    list of download urls.

    '''
    
    
    return(list(map(lambda x:combine_url(x, base_url), data_dates)))

def combine_url(date: str, url: str):
    '''
    

    Parameters
    ----------
    date : str
        date.
    url : str
        url.

    Returns
    -------
    full url.

    '''
    
    return(url + str(date).split(' ')[0])

