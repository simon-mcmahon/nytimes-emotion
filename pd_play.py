import pandas as pd
import datetime
df = pd.read_csv('nytimes_dash_output.csv')

# print(df.head())

# x  = pd.concat([df['query_time']]*4,1)
# y = df.ix[:,['fb_10_pol','twitter_10_pol','email_10_pol','viewed_10_pol']]
# print(y.head())


time_string = '%Y-%m-%d %H:%M:%S'

#Do the calculations required for the time slider

time_string = '%Y-%m-%d %H:%M:%S'

time_min = df['query_time'].min()
time_min = datetime.datetime.strptime(time_min, time_string)

time_max = df['query_time'].max()
time_max = datetime.datetime.strptime(time_max, time_string)

diff = time_max - time_min

days_recorded = diff.days

timevalue = 4

time_dict = {5: 1, 4: 3, 3: 7, 2: 14, 1: 30}
days_display = time_dict[timevalue]

if days_display > days_recorded:
    days_display = days_recorded

cutoff_date = time_max - datetime.timedelta(days=days_display)

binary_plot = lambda x: (datetime.datetime.strptime(x, time_string) >= cutoff_date )

plot = df[ df['query_time'].map(binary_plot) ]

plot.head()