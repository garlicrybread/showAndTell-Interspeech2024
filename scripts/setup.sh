#!/bin/bash

# initialize db
echo ---
echo Initializing database...
echo ---
flask --app flaskr/ init db
echo

# Run a Python script that creates the userConditions.csv
echo ---
echo Create user conditions csv...
echo ---
python3 setup.py
echo

# Create Minimal Pair files based on vowels and consonants
echo ---
echo Creating minimal pair files based on vowels and consonants...
echo ---
cd flaskr/data/minimalPairsGeneration
python3 preprocess.py
echo

# Create control, vwl, const, and mirror files
echo ---
echo Create practice files for each of the conditions based on the different orderings
echo ---
cd ..
python3 data_prep.py vwl-info.txt
python3 data_prep.py const-info.txt
python3 data_prep.py control-info.txt
python3 data_prep.py mirror-info.txt
