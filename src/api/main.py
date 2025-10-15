from fastapi import FastAPI
import pandas as pd
import joblib
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Oráculo de combate API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_path = os.path.join(os.path.dirname(__file__), "..", "..","models", 'combat_model.joblib')
model = joblib.load(model_path)

class CombatData(BaseModel):
    num_player: int
    num_level_players: int
    total_player_hp: int
    avg_player_ac: float
    total_player_atk: int
    num_enemy: int
    total_enemy_hp: int
    avg_enemy_ac: float
    total_enemy_atk: int

@app.post("/predict")
async def predict(data: CombatData):
    input_df = pd.DataFrame([data.dict()])

    features_order = [
        'num_player',
        'num_level_players',
        'total_player_hp',
        'avg_player_ac',
        'total_player_atk',
        'num_enemy',
        'total_enemy_hp',
        'avg_enemy_ac',
        'total_enemy_atk'
    ]

    input_df = input_df[features_order]

    prediction_proba = model.predict_proba(input_df)

    player_victory_probability = prediction_proba[0][1]

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

    return{
        "difficulty": difficulty,
        "player_victory_probability": f"{player_victory_probability:.2%}"
    }