import random
import pandas as pd
from tqdm import tqdm

# Classes

class entidades:
    def __init__(self, hp, ac, bonus_atk, avg_damage):
        self.hp = hp
        self.ac = ac
        self.bonus_atk = bonus_atk
        self.avg_damage = avg_damage
        self.is_alive = True

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
    
    def attack(self, target):
        atack_roll = random.randint(1, 20)

        if atack_roll + self.bonus_atk >= target.ac:
            target.take_damage(self.avg_damage)


# Funções

def simular_batalha(player, enemy):
    combatentes = player + enemy
    random.shuffle(combatentes)
    rodadas = 0

    while (any(p.is_alive for p in player) and 
           any(e.is_alive for e in enemy) and 
           rodadas < 1000):
        for ent in combatentes:
            if not ent.is_alive:
                continue
                
            # Get a fresh list of alive targets each time
            if ent in player:
                targets = [e for e in enemy if e.is_alive]
            else:
                targets = [p for p in player if p.is_alive]
                
            if not targets:
                break

            target = random.choice(targets)
            ent.attack(target)
        
        rodadas += 1
    
    return 1 if any(p.is_alive for p in player) else 0


# simulação para criar o dataset

simulador_resul = []
numeros_simulacoes = 50000

for _ in tqdm(range(numeros_simulacoes)):
    num_player = random.randint(3, 8)
    num_level_players = random.randint(1, 16)
    
    player = []

    for _ in range(num_player):
        player_hp = 10 + (num_level_players * 8)
        player_ac = 14 + (num_level_players//2)
        player_atk = 4 + num_level_players
        player_avg_damage = 5 + (num_level_players *1.5)
        player.append(entidades(player_hp, player_ac, player_atk, player_avg_damage))

    num_enemy = random.randint(1, 10)

    enemy = []

    for _ in range(num_enemy):
        enemy_hp = random.randint(10,120)
        enemy_ac = random.randint(10,20)
        enemy_atk = random.randint(3,10)
        enemy_avg_damage = random.randint(5,40)
        enemy.append(entidades(enemy_hp, enemy_ac, enemy_atk, enemy_avg_damage))

    player_victory = simular_batalha(player, enemy)


    simulador_data = {
        'num_player': num_player,
        'num_level_players': num_level_players,
        'total_player_hp': sum(p.hp for p in player),
        'avg_player_ac': sum(p.ac for p in player)/num_player,
        'total_player_atk': sum(p.bonus_atk for p in player),

        'num_enemy': num_enemy,
        'total_enemy_hp': sum(e.hp for e in enemy),
        'avg_enemy_ac': sum(e.ac for e in enemy)/num_enemy,
        'total_enemy_atk': sum(e.bonus_atk for e in enemy),

        'player_victory': player_victory
    }

    simulador_resul.append(simulador_data)

dataset = pd.DataFrame(simulador_resul)
dataset.to_csv('dataset.csv', index=False)

print("Dataset criado com sucesso!")