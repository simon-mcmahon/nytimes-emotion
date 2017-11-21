from textblob import TextBlob

import sqlite3

#Connect to the database and add the sentiment columns if they do not exist

db = sqlite3.connect('data/nytimes.sqlite')

cursor = db.cursor()

link_table_data = cursor.execute('PRAGMA table_info(link)')
link_cols = []
#Get the column names for the table links
for d in link_table_data:
    link_cols += [d[1]]

if 'polarity' not in link_cols:
    print('making polarity')

    cursor.execute('''
    ALTER TABLE link
        ADD polarity REAL;
        ''')

if 'subjectivity' not in link_cols:
    print('making subjectivity')

    cursor.execute('''
    ALTER TABLE link
        ADD subjectivity REAL;
        ''')

db.commit()

# Query the link table and execute the sentiment analysis on each article and assign the output to the database.

article_query = cursor.execute('SELECT link_id,article,polarity,subjectivity FROM link;').fetchall()

count = 0

for d in article_query:
    count = count + 1
    if (d[2] is None) and (d[3] is None):
        print('adding polarity and subjectivity ' + str(count) + ' out of ' + str(len(article_query)))
        article_id = d[0]
        article_text = TextBlob(d[1])
        article_polarity = article_text.sentiment.polarity
        article_subjectivity = article_text.sentiment.subjectivity
        cursor.execute('UPDATE link SET polarity = {0}, subjectivity  = {1} WHERE link_id = {2};'.format(article_polarity,article_subjectivity,article_id))
        db.commit()
    else:
        print('already added')
        continue

