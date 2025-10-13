#carregamos aqui o dataset em dataframe do pandas
import pandas as pd

#carregamos o dataset
dataset = pd.read_csv('dataset.csv')

print(dataset.head())
print(dataset.info())
print(dataset.describe())

