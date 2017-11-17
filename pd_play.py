import pandas as pd

df = pd.read_csv('nytimes_dash_output.csv')

# print(df.head())

x  = pd.concat([df['query_time']]*4,1)
y = df.ix[:,['fb_10_pol','twitter_10_pol','email_10_pol','viewed_10_pol']]
print(y.head())