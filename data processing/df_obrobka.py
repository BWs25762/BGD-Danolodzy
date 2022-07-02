import pandas as pd
from ast import literal_eval

def contains(lista, string):
    if string in lista:
        return True
    else:
        return False

#wypisujemy dane które mergujemy:

df = pd.read_csv('danex1.csv')
df = df.append(pd.read_csv('danex2.csv'), ignore_index = True)
df = df.append(pd.read_csv('danex3.csv'), ignore_index = True)
#df = df.append(pd.read_csv('dane4.csv'), ignore_index = True)


df = df.sort_values(by=['created_utc'])
df = df.reset_index()
df = df.drop(columns=['_id','index', 'level_0'])
df['isbuy'] = 0
df['issell'] = 0
df['posts_count'] = 1
for x in range(df['selftext'].shape[0]):
    df['selftext'].iloc[x] = literal_eval(df['selftext'].iloc[x])
for x in range(df['selftext'].shape[0]):
    if 'buy' in df['selftext'].iloc[x] or 'Buy' in df['selftext'].iloc[x] or 'BUY' in df['selftext'].iloc[x] \
            or 'pump' in df['selftext'].iloc[x] or 'PUMP' in df['selftext'].iloc[x]:
        df['isbuy'].iloc[x] = 1
    if 'sell' in df['selftext'].iloc[x] or 'Sell' in df['selftext'].iloc[x] or 'SELL' in df['selftext'].iloc[x] \
            or 'dump' in df['selftext'].iloc[x] or 'DUMP' in df['selftext'].iloc[x]:
        df['issell'].iloc[x] = 1
df['created_utc'] = pd.to_datetime(df['created_utc'])
df.drop(columns=['selftext'])
df = df.groupby([df['created_utc'].dt.date])['isbuy','issell','posts_count'].sum()
df.to_csv('danepoobrobcetesla.csv', index=True)
print(df)