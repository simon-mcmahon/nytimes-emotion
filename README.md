# nytimes-emotion

A project intending to take the emotions from the nytime most popular page and display the result of the trending page over time.

## Website

The project is now live on a heroku app which is available to view [here](https://nytimes-emotion.herokuapp.com/).

## Structure
The script uses beautiful soup and APscheduler to run a call every 15 minutes to extract the 10 top headlines and article text and store it in an sqlite3 database. This database is then modified and parsed through a sentiment analysis machine learning model using Textblob and NLTK. The script is then parsed through the `output_csv.py` script to trim the text down into a reasonably sized `.csv` file for deplymemt on heroku.

The webapp side is written in a Dash app built on top of plotly and flask. gunicorn is used for deployment.

I have the scaper.py function running on a t2.nano ec2 instance (AWS).

It runs in python 3.6.

## To do

* Add in live updating graphs. ATM the csv is static in the github repo. The database is still continually updated in the t2.nano instance but needs manual processing and deployment.

* Add in another set of checkboxes in order to allow people to show or hide each set of data.

* Add in a 2-way time shift slider so people can adjut their view to 1 week, 2 weeks etc.

* make a controller script to streamline the database processing:
  * copy database from ec2
  * run sentiment analysis
  * output_csv to get csv
  * push to dev branch of nytimes-emotion

* Adding sentiment analysis functionality for something like the 5 emotions

* Graph smoothing to make the graphs more readable

* CSS sheet design to make the app more mobile friendly and wide monitor friendly
