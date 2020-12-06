import os
import glob
import pandas as pd


def remove_empty_files(outdir: str):
    '''
    Function to remove files with 0 rows
    '''

    downloaded_files = glob.glob(outdir)

    for file in downloaded_files:

        data = pd.read_csv(file)

        if len(data.index) == 0:

            os.remove(file)
