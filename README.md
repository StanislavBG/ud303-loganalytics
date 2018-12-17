Log Analytics UDD303
=============

Provide summary statistics of usage and errors 
from application-logs data from a web blog. 

To set-up the project fist initialize a psql schema
psql -d news -f newsdata.sql

Then execute the summary python program to generate summary
python3 logAnalytics.py

