# [nytimes-emotion](https://nytimes-emotion.herokuapp.com/)

## Status

This project is not being updated due to changed on the NYTimes website which do not make the Top 10 articles by platform available in real time.

## Purpose

A personal coding project which monitored the trending NYTimes article by social media platform at [http://www.nytimes.com/most-popular.html](http://www.nytimes.com/most-popular.html) until it was deprecated in December 2017. The refresh time of the webpage and data was 15 minutes.

The article text and headline were then fed into the [NTLK](http://www.nltk.org/) sentiment analysis engine where values for polarity and subjectivity were calculated.

## Website

The project is now live on a heroku app which is available to view [here](https://nytimes-emotion.herokuapp.com/).

**(Note: The load time for the web app will be around 15-20 seconds on first refresh as it is hosted on heroku's free tier which does not provide 24hr hosting.)**

## Design

The `scraper.py` script uses beautiful soup and APscheduler to run a call every 15 minutes to extract the 10 top headlines and article text for each platform (facebook, twitter, email and on website). This is then stored in an sqlite database. 

This database is then parsed through a sentiment analysis machine learning model using [Textblob](https://textblob.readthedocs.io/en/dev/) and [NTLK](http://www.nltk.org/). The database is then parsed through the `output_csv.py` script to output a reasonably sized `.csv` file for deplymemt as a webapp heroku.

The webapp side is written in [Dash by Plotly](https://dash.plot.ly/) (built on top of flask). [Gunicorn](https://gunicorn.org/) is used for deployment of the app to [Heroku](https://www.heroku.com/).

The `scraper.py` function runs on a t2.nano ec2 instance (AWS).

It was built on python 3.6 but should run in python 3.X. This has not been tested.

## Installation instructions

Clone this repository:

`git clone https://github.com/simon-mcmahon/nytimes-emotion`

Install the dependencies:

`pip install -r requirements.txt`

Setting up automatic deployment with Gunicorn and Heroku:

[Tutorial](https://github.com/datademofun/heroku-basic-flask)
