#!/bin/sh

set -ex

date=$1
days=$2
host="the_sanctuary"

# get data from apex controller
wget "http://${host}.local/cgi-bin/datalog.xml?sdate=${date}&days=${days}" -O xml/datalog_${date}_${days}.xml

# convert xml to csv
./xml_to_csv.py xml/datalog_${date}_${days}.xml csv/datalog_${date}_${days}.csv

# append new csv to global datalog
#tail --lines=+2 csv/datalog_${date}_${days}.csv csv/datalog.csv

# plot data
./csv_plot.py csv/datalog_${date}_${days}.csv
#./csv_plot.py csv/datalog.csv