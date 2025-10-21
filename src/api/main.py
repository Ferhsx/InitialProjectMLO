from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
import joblib
import pandas as pd
from pathlib import Path

app = FastAPI(title='Oráculo de combate API', version='1.2.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

# Carrega modelo + metadata
BASE = Path(__file__).resolve().parent
MODEL_PATH = BASE.joinpath('..', '..', 'models', 'combat_model.joblib')
if not MODEL_PATH.exists():
    raise RuntimeError(f'Modelo não encontrado em {MODEL_PATH}')

model, metadata = joblib.load(str(MODEL_PATH))
FEATURES_ORDER = metadata['features_order']

class CombatData(BaseModel):
    num_player: int
    level_players: int
    total_player_hp: int
    avg_player_ac: float
    total_player_atk: int
    total_player_damage: int
    num_enemy: int
    level_enemies: int
    total_enemy_hp: int
    avg_enemy_ac: float
    total_enemy_atk: int
    total_enemy_damage: int

    @validator('num_player', 'level_players', 'num_enemy', 'level_enemies', 'total_player_hp', 'total_enemy_hp', 'total_player_atk', 'total_enemy_atk', 'total_player_damage', 'total_enemy_damage')
    def non_negative(cls, v):
        if v is None:
            raise ValueError('Valor obrigatório')
        if v < 0:
            raise ValueError('Valor não pode ser negativo')
        return v

@app.post('/predict')
async def predict(data: CombatData):
    input_df = pd.DataFrame([data.dict()])

    # criar features derivadas na mesma ordem usada no treino
    input_df['hp_ratio'] = input_df['total_player_hp'] / (input_df['total_enemy_hp'] + 1)
    input_df['atk_diff'] = input_df['total_player_atk'] - input_df['total_enemy_atk']
    input_df['ac_diff'] = input_df['avg_player_ac'] - input_df['avg_enemy_ac']
    input_df['num_ratio'] = input_df['num_player'] / (input_df['num_enemy'] + 1)
    input_df['damage_diff'] = input_df['total_player_damage'] - input_df['total_enemy_damage']
    input_df['level_diff'] = input_df.get('level_players', 0) - input_df.get('level_enemies', 0)
    input_df['avg_dmg_per_player'] = input_df['total_player_damage'] / input_df['num_player']
    input_df['avg_dmg_per_enemy'] = input_df['total_enemy_damage'] / input_df['num_enemy']

    # reordena as colunas para corresponder ao treino
    input_df = input_df[FEATURES_ORDER]

    # predicao
    prediction_proba = model.predict_proba(input_df)
    player_victory_probability = prediction_proba[0][1]

    # define dificuldade
    difficulty = "Desconhecida"
    if player_victory_probability >= 0.95:
        difficulty = "Trivial"
    elif player_victory_probability >= 0.75:
        difficulty = "Facil"
    elif player_victory_probability >= 0.5:
        difficulty = "Medio"
    elif player_victory_probability >= 0.25:
        difficulty = "Dificil"
    else:
        difficulty = "Mortal"

    return {
        "difficulty": difficulty,
        "player_victory_probability": f"{player_victory_probability:.2%}"
    }