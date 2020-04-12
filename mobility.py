#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 20:40:40 2020

@author: hamishgibbs
"""


from datetime import datetime
from datetime import timedelta

def get_file_dates(earliest_date):
    
    data_dates = []
    date = earliest_date
    while date < datetime.now():
        data_dates.append(date)
        date = date + timedelta(hours=8)
        
    # need to add %200000' with proper time value at 3rd position to end of url
        
    return(data_dates)

def get_url_end(date):
    return('%20' + '{0:02d}'.format(date.hour) + '00') #'{:<03d}'

def combine_url(date, url):
    
    return(url + str(date).split(' ')[0] + get_url_end(date))

def get_urls(base_url, data_dates):
    
    return(list(map(lambda x:combine_url(x, base_url), data_dates)))

