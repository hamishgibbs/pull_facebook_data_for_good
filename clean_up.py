import os
import glob
import pandas as pd


def remove_empty_files(outdir: str):
    """
    Function to remove files with 0 rows
    """

    # Get all files that have been downloaded
    downloaded_files = glob.glob(outdir + '/*.csv')

    # For each downloaded file
    for file in downloaded_files:

        # Open file with pandas
        data = pd.read_csv(file)

        # If file has no rows, delete it
        if len(data.index) == 0:

            os.remove(file)
