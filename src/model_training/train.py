import os
from pathlib import Path
import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score


def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    # Evita divisão por zero
    df = df.copy()
    df['hp_ratio'] = df['total_player_hp'] / (df['total_enemy_hp'] + 1)
    df['atk_diff'] = df['total_player_atk'] - df['total_enemy_atk']
    df['ac_diff'] = df['avg_player_ac'] - df['avg_enemy_ac']
    df['num_ratio'] = df['num_player'] / (df['num_enemy'] + 1)
    df['damage_diff'] = df['total_player_damage'] - df['total_enemy_damage']
    df['level_diff'] = df.get('level_players', 0) - df.get('level_enemies', 0)
    df['avg_dmg_per_player'] = df['total_player_damage'] / df['num_player']
    df['avg_dmg_per_enemy'] = df['total_enemy_damage'] / df['num_enemy']
    # remova ou converta outcomes flutuantes para binário (0/1) se necessário
    df = df[df['player_victory'].isin([0, 1])]
    return df


def train_and_save(df: pd.DataFrame, model_out: str):
    df = add_derived_features(df)

    target = 'player_victory'
    X = df.drop(columns=[target])
    y = df[target].astype(int)

    # Salva a ordem das features para a API
    features_order = list(X.columns)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        use_label_encoder=False,
        eval_metric='logloss',
        random_state=42
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)

    print('Acurácia:', acc)
    print('AUC:', auc)
    print('\nRelatório de classificação:')
    print(classification_report(y_test, y_pred))

    # metadata com ordem de features e versão
    metadata = {
        'features_order': features_order,
        'version': '1.0.0'
    }

    os.makedirs(os.path.dirname(model_out), exist_ok=True)
    joblib.dump((model, metadata), model_out)
    print('Modelo salvo em', model_out)


if __name__ == '__main__':
    base = Path(__file__).resolve().parent
    data_path = base.joinpath('..', '..', 'data', 'dataset.csv')
    model_out = base.joinpath('..', '..', 'models', 'combat_model.joblib')

    df = pd.read_csv(data_path)
    train_and_save(df, str(model_out))