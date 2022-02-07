# dataparse
A script to convert and aggregate tab-delimited potentiostat data from EC-Lab into a single csv file

# Problem Statement
The proprietary lab software used by the potentiostat only allowed data to be dumped into tab-delimited files.

# Description
This was an old script I wrote while working at a startup research company.
We were performing differential pulse voltammetry and cyclic voltammetry experiments with a potentiostat.
When the potentiostat would reach the end of the experiment, it would simply dump all the data into a tab-delimited file.
This script would aggregate all of the data files into a format that could be imported into Postgres.
