#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 13:07:41 2020

@author: hamishgibbs
"""

#update unittests


import os
import sys
from getpass import getpass
from utils import get_download_variables
from pull_mobility import pull_mobility
from pull_colocation import pull_colocation
from pull_population import pull_population

def main():
    
    argv = sys.argv 
    
    #access user credential
    try:
        import dotenv
        
        dotenv.load_dotenv()
        
        username = os.getenv("FB_USERNAME")
        password = os.getenv("FB_PASSWORD")
        outdir = os.getenv("FB_OUTDIR")
        
        if username is None or password is None:
            raise ValueError('File .env is missing credentials FB_USERNAME and/or FB_PASSWORD.')
            
        else:
            print('Using credentials in .env file.')
            
            
    except:
        
        print('No credentials found. You can configure the FB_USERNAME, FB_PASSWORD, and FB_OUTDIR variables in a .env file.')
        
        username = input("Username: ")
            
        password = getpass()
        
        outdir = input("Output directory: ")
    
    keys = [username, password]
    
    if argv[2] not in ['TilePopulation', 'TileMovement', 'AdminMovement', 'Colocation']:
        raise ValueError("Dataset type not recognized. Currently supporting 'TilePopulation', 'TileMovement', and 'Colocation' datasets")
    
    dl_variables = get_download_variables(argv[1], argv[2])
    
    update = input("Updating an existing data collection? (y/n): ")
    
    if update == 'y':
        
            update = True
            
    elif update == 'n':
        
        update = False
        
    else:
        
        raise ValueError('Unknown update input. Choose "y", "n".')
    
    if argv[2] in ['TileMovement', 'AdminMovement']:
    
        pull_mobility(outdir, keys, argv[1], dl_variables, update, argv[2])
    
    elif argv[2] == 'Colocation':
        
        pull_colocation(outdir, keys, argv[1], dl_variables, update)
    
    elif argv[2] == 'TilePopulation':
        
        pull_population(outdir, keys, argv[1], dl_variables, update, argv[2])

if __name__ == '__main__':
    main()





