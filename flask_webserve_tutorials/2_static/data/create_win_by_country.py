import pandas as pd

df_winners = pd.read_json('nwinners.json')

for name, group in df_winners.groupby('country'):
    group.to_json('nwinners_by_country/' + name + '.json', orient='records')

