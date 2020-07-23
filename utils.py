#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 16:41:48 2020

@author: hamishgibbs
"""

import os
import glob
import shutil
from selenium import webdriver
import time
from datetime import datetime
from progress.bar import Bar
import requests

def try_mkdir_silent(path):
    '''
    Make the target directory or do nothing if it already exists.
    
    Parameters
    ----------
    path : str
        directory to be made.

    Returns
    -------
    None.

    '''
    
    try:
        os.mkdir(path)
    except:
        pass
    
def get_home_dir():
    '''
    Expand user home directory.

    Returns
    -------
    str.

    '''
    
    return(os.path.expanduser("~"))


def download_data(urls: list, keys: list):
    '''
    navigate the facebook login page and access each url

    Parameters
    ----------
    urls : list
        dataset urls.
    keys : list
        login keys username, password.

    Returns
    -------
    Start time of downloads.

    '''
    
    driver = webdriver.Chrome(executable_path='/Applications/chromedriver')
    
    download_start = time.time()
    
    driver.get(urls[0])
    
    driver.find_element_by_xpath('//*[@id="email"]').send_keys(keys[0])
    
    driver.find_element_by_xpath('//*[@id="pass"]').send_keys(keys[1])
    
    driver.find_element_by_xpath('//*[@id="loginbutton"]').click()
    time.sleep(1)
    
    bar = Bar('Downloading', max=len(urls[1:]))
    for url in urls[1:]:
        driver.get(url)
        bar.next()
        time.sleep(1)
    
    bar.finish()
    
    driver.quit()
    
    return(download_start)

def rename_and_move(old_fn: str, old_dir: str, new_fn: str, new_dir: str):
    '''
    rename files and move them to a new directory

    Parameters
    ----------
    old_fn : str
        old filename.
    old_dir : str
        old directory.
    new_fn : str
        new filemane.
    new_dir : str
        new directory.

    Returns
    -------
    None.

    '''
    
    os.rename(old_dir + '/' + old_fn, old_dir + '/' + new_fn) 

    shutil.move(old_dir + '/' + new_fn, new_dir + '/' + new_fn)
    
def get_new_file_name(file: str):
    '''
    parse default filename to reformat as COUNTRY_DATE.csv

    Parameters
    ----------
    file : str
        filename.

    Returns
    -------
    new filename.

    '''
        
    country = file.split('/')[-1].split(" ")[0]
    
    date = file.split('/')[-1].split("_")[-1].split(".")[0].replace('-', '_').replace(' ', '_')
    
    return(country + '_' + date + '.csv')
    
def move_most_recent_files(outdir: str, urls: list, download_start: float):
    '''
    get the most recent files from the download directory, rename them, and put them in the destination directory

    Parameters
    ----------
    outdir : str
        output directory.
    urls : list
        download urls.

    Returns
    -------
    None.

    '''
    
    try_mkdir_silent(outdir)
        
    csv_files = glob.glob(get_home_dir() + '/Downloads/*.csv')
    csv_files = {}
    
    for f in glob.glob(get_home_dir() + '/Downloads/*.csv'):
        csv_files[f] = os.path.getctime(f)
        
    downloaded_files = dict((k, v) for k, v in csv_files.items() if v >= download_start) 
        
    #sorted_files = [f[0] for f in sorted(csv_files.items(), key=operator.itemgetter(1), reverse=True)[:len(urls)]]
    
    new_fns = [get_new_file_name(file) for file in downloaded_files]
    
    for i, f in enumerate(downloaded_files):
        
        rename_and_move(f.split('/')[-1], get_home_dir() + '/Downloads', new_fns[i], outdir)
#%%
def get_update_date(outdir: str):
    '''
    Get the latest date added in the output directory.

    Parameters
    ----------
    outdir : str
        output directory.

    Returns
    -------
    latest date of files added: datetime.datetime.

    '''
    
    latest_addition = []
    
    for i, f in enumerate(glob.glob(outdir + '/*.csv')):
        
        f_date_parse = f.split('/')[-1].split('.')[0].split('_')
        
        year = int(f_date_parse[1])
        month = int(f_date_parse[2])
        day = int(f_date_parse[3])
        
        try:
            hour = int(f_date_parse[4].strip('0'))
        except:
            hour = 0
        
        
        latest_addition.append(datetime(year, month, day, hour))
    
    return(max(latest_addition))
    
    
def get_config():
    '''
    

    Raises
    ------
    SystemExit
        When requests.get() of .config file fails.
    Exception
        A .config file cannot be transformed to a dict.

    Returns
    -------
    dict of .config file data.

    '''
    
    config_url = 'https://raw.githubusercontent.com/hamishgibbs/pull_facebook_data_for_good/master/.config'
    
    try:
        r = requests.get(config_url)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)
    
    try:
        config = dict(x.split("=") for x in r.text.split("\n")[:-1])    
    except:
        raise Exception('Malformed .config file.')
                
    return(config)

def origin_to_datetime(origin: str):
    '''

    Parameters
    ----------
    origin : str
        string of dataset origin in format year_month_day(_hour).

    Raises
    ------
    ValueError
        When date parsing fails.

    Returns
    -------
    datetime.datetime object.

    '''
    
    if origin.count('_') == 3:
        
        origin = datetime.strptime(origin, '%Y_%m_%d_%H')
        
    elif origin.count('_') == 2:
        
        origin = datetime.strptime(origin, '%Y_%m_%d')
        
    else:
        raise ValueError('Unknown date format.')
        
    return(origin) 
    
def get_download_variables(country: str, dataset: str):
    '''

    Parameters
    ----------
    country : str
        Country to be downloaded.
    dataset : str
        Dataset to be downloaded.

    Raises
    ------
    KeyError
        When a country and dataset combination is not in the .config file.

    Returns
    -------
    dict of download parameters (dataset id and origin).

    '''
    
    config = get_config()
    
    try:
        dataset_id = config['_'.join([country, dataset, 'ID'])]
    except:
        raise KeyError('No config value for {}. To add a new dataset, see the Readme.'.format('_'.join([country, dataset, 'ID'])))
        
    try:
        dataset_origin = config['_'.join([country, dataset, 'Origin'])]
    except:
        raise KeyError('No config value for {}.  To add a new dataset, see the Readme.'.format('_'.join([country, dataset, 'Origin'])))
    
    dataset_origin = origin_to_datetime(dataset_origin)
    
    return({'id':dataset_id, 'origin':dataset_origin})
    
def remove_empty_files(country_output: str):
    '''
    

    Parameters
    ----------
    country_output : str
        Country-specific output directory.

    Returns
    -------
    None.

    '''
    fns = [country_output + '/' + fn for fn in os.listdir(country_output)]
    
    size = [os.path.getsize(fn) for fn in fns]
    
    fns = dict(zip(fns, size))
    
    empty_fns = list({k: v for k, v in fns.items() if v == 0 }.keys())
    
    if len(empty_fns) == 0:
        return(None)
    else:
        try:
            
            [os.remove(fn) for fn in empty_fns]
            
            print('Removed {} empty files.'.format(len(empty_fns)))
            
        except Exception as e:
            print(e)
            print('Unable to remove empty files.')
        
    
    
    
    