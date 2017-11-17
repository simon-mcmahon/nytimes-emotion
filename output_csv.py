
import datetime
import sqlite3
import csv

db = sqlite3.connect('nytimes.sqlite')

cursor = db.cursor()

link_table_data = cursor.execute('PRAGMA table_info(link)')

print(link_table_data.fetchall())

article_query = cursor.execute('SELECT link_id,url,polarity,subjectivity FROM link;').fetchall()
time_query = cursor.execute('SELECT * FROM query;').fetchall()
# fb_query = cursor.execute('SELECT * FROM fb;')
# twitter_query = cursor.execute('SELECT * FROM twitter;')
# email_query = cursor.execute('SELECT * FROM email;')
# viewed_query = cursor.execute('SELECT * FROM viewed;')
length_process = len(time_query)
count = 0
countmax = 5

with open('nytimes_dash_output.csv', 'w+', newline='') as csvfile:
    prefix = ['fb', 'twitter', 'email', 'viewed']
    fieldnames = ['query_id','query_time','fb_1_head','fb_1_pol','fb_1_sub','fb_10_pol','fb_10_sub','twitter_1_head','twitter_1_pol','twitter_1_sub','twitter_10_pol','twitter_10_sub','email_1_head','email_1_pol','email_1_sub','email_10_pol','email_10_sub','viewed_1_head','viewed_1_pol','viewed_1_sub','viewed_10_pol','viewed_10_sub']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for d in time_query:
        count = count+1
        if divmod(count,100)[1]==0:
            print('processed ' + str(count) + ' out of ' + str(length_process))
        #Sanity check print d[0] = query_id , d[1] = unixtime
        query_id = d[0]
        utctime = datetime.datetime.utcfromtimestamp(d[1])
        # print(str(d[0]) + ' ' + str(d[1]))

        prefix = ['fb','twitter','email','viewed']
        output_dict = {}
        output_dict['query_id'] = query_id
        output_dict['query_time'] = utctime

        #Iterate over each media type
        for pre in prefix:

            pre_query = cursor.execute('SELECT * FROM {0} WHERE query_id={1};'.format(pre,query_id)).fetchall()
            pre_tuple = pre_query[0]
            head_pol_sub = []
            #Iterate over all the links in FB
            for e in range(1,len(pre_tuple)):
                head_pol_sub += [cursor.execute('SELECT headline,polarity,subjectivity FROM link WHERE url="{0}";'.format(pre_tuple[e])).fetchone()]

            #Find the top headline
            top_headline = head_pol_sub[0][0]

            #Find the top1 pol and sub and the average top 10 pol and sub
            top1_pol = head_pol_sub[0][1]
            top1_sub = head_pol_sub[0][2]

            average_pol = 0
            average_sub = 0

            for x in range(0,len(head_pol_sub)):
                average_pol = average_pol + head_pol_sub[x][1]
                average_sub = average_sub + head_pol_sub[x][2]
            average_pol = average_pol/len(head_pol_sub)
            average_sub = average_sub/len(head_pol_sub)
            top10_pol = average_pol
            top10_sub = average_sub

            #Make the dict to interface with dictwriter

            output_dict[pre + '_1_head'] = top_headline
            output_dict[pre + '_1_pol'] = top1_pol
            output_dict[pre + '_1_sub'] = top1_sub
            output_dict[pre + '_10_pol'] = top10_pol
            output_dict[pre + '_10_sub'] = top10_sub

        writer.writerow(output_dict)

        # print(head_pol_sub)
        # print(pre_query[0])

#Error checking

# print(cursor.execute('SELECT polarity,subjectivity FROM link WHERE url="{0}";'.format('https://www.nytimes.com/2017/11/05/us/church-shooting-texas.html')).fetchone())


# print(cursor.execute('SELECT polarity,subjectivity FROM link WHERE url="{0}";'.format('https://www.nytimes.com/2017/11/05/us/church-shooting-texas.html')).fetchone())
