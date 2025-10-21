#carregamos aqui o dataset em dataframe do pandas
import pandas as pd
import os

#carregamos o dataset
dataset = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'dataset.csv'))

print(dataset.head())
print(dataset.info())
print(dataset.describe())

#conta quantas vitorias e quantas derotas
print(dataset[dataset['player_victory'] == 1].value_counts())
print(dataset[dataset['player_victory'] == 0].value_counts())
