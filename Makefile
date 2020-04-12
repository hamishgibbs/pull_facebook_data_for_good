KEY := ~/Documents/Personal/Cryptography/fb_key.key
USERPASS := ~/Documents/Personal/Scrape
MAINDIR := ~/Documents/Covid-19/covid_facebook_mobility

COLDATASETS := colocation_datsets.csv
MOBDATASETS := mobility_datsets.csv

OUTDIR := ${MAINDIR}/data/Facebook_Data

pull_colocation:
	python pull_colocation.py ${KEY} ${USERPASS} ${COLDATASETS} ${OUTDIR}

pull_mobility:	
	python pull_mobility.py ${KEY} ${USERPASS} ${MOBDATASETS} ${OUTDIR}

test:
	python -m unittest discover