import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# Carregando o dataset
Data_path = os.path.join('..', '..', 'data', 'dataset.csv')
# Adicione estas linhas de depuração no seu train.py

print("--- INÍCIO DA DEPURAÇÃO DE CAMINHO ---")

# O caminho para o próprio script
local_do_script = os.path.dirname(__file__)
print(f"O script acredita que está em: {local_do_script}")

# O caminho que você está construindo
Data_path = os.path.join(local_do_script, '..', '..', 'data', 'dataset.csv')
print(f"Caminho relativo construído para o CSV: {Data_path}")

# Vamos ver a versão "absoluta" desse caminho
caminho_absoluto = os.path.abspath(Data_path)
print(f"Tentando carregar o arquivo de: {caminho_absoluto}")

# Verifique se o arquivo realmente existe nesse caminho absoluto
print(f"O arquivo existe neste caminho? -> {os.path.exists(caminho_absoluto)}")

print("--- FIM DA DEPURAÇÃO DE CAMINHO ---")

# A linha original que carrega o CSV (pode deixar como estava ou usar o caminho absoluto)
df = pd.read_csv(Data_path)


print("Tudo ocorreu certo", df.head())

x = df.drop('player_victory', axis=1)
y = df['player_victory']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

print("Dados dividos")

model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(x_train, y_train)

y_pred = model.predict(x_test)

accuracy = accuracy_score(y_test, y_pred)
print("Acurácia:", accuracy)
print("\nRelatório de classificação:")

print(classification_report(y_test, y_pred))

model_save_path = os.path.join('..', '..', 'models')

os.makedirs(model_save_path, exist_ok=True)

joblib.dump(model, os.path.join(model_save_path, 'combat_model.joblib'))
print(f"\nModelo salvo em: {model_save_path}/combat_model.joblib")  