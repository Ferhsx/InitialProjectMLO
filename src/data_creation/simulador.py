import random
from dataclasses import dataclass
from pathlib import Path
from tqdm import tqdm
import pandas as pd
import argparse

@dataclass
class Entidade:
    hp: int
    ac: int
    atk_bonus: int
    avg_damage: int
    is_alive: bool = True

    def take_damage(self, damage: int):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False

    def attack(self, target: "Entidade") -> int:
        roll = random.randint(1, 20)
        # nat1 miss
        if roll == 1:
            return 0

        # damage variability (simple d6 + bias)
        base_die = 6
        damage_roll = random.randint(1, base_die)
        bias = max(0, self.avg_damage - (base_die // 2))
        damage = damage_roll + bias + (self.atk_bonus // 2)

        # nat20 crit
        if roll == 20:
            damage *= 2

        # check hit
        if roll == 20 or (roll + self.atk_bonus) >= target.ac:
            target.take_damage(damage)
            return damage
        return 0


def simular_batalha(player_list, enemy_list, max_rounds=1000, shuffle_init=True):
    combatentes = list(player_list) + list(enemy_list)
    if shuffle_init:
        random.shuffle(combatentes)

    rounds = 0
    players_alive = [p for p in player_list if p.is_alive]
    enemies_alive = [e for e in enemy_list if e.is_alive]

    while players_alive and enemies_alive and rounds < max_rounds:
        for ent in combatentes:
            if not ent.is_alive:
                continue

            if ent in player_list:
                targets = [e for e in enemy_list if e.is_alive]
            else:
                targets = [p for p in player_list if p.is_alive]

            if not targets:
                break

            target = random.choice(targets)
            ent.attack(target)

        players_alive = [p for p in player_list if p.is_alive]
        enemies_alive = [e for e in enemy_list if e.is_alive]
        rounds += 1

    # outcome: 1 win, 0 loss, 0.5 draw
    if players_alive and not enemies_alive:
        outcome = 1.0
    elif enemies_alive and not players_alive:
        outcome = 0.0
    elif not players_alive and not enemies_alive:
        outcome = 0.5
    else:
        outcome = 0.5

    summary = {
        "outcome": outcome,
        "rounds": rounds,
        "player_hp_left": sum(p.hp for p in player_list),
        "enemy_hp_left": sum(e.hp for e in enemy_list),
        "player_kills": sum(1 for e in enemy_list if not e.is_alive),
        "enemy_kills": sum(1 for p in player_list if not p.is_alive)
    }
    return summary


def gerar_dataset(n_sim=100000, seed=42, out_path='data/dataset.csv'):
    random.seed(seed)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    results = []

    for _ in tqdm(range(n_sim)):
        num_player = random.randint(1, 10)
        level_players = random.randint(1, 20)
        num_enemy = random.randint(1, 20)
        level_enemies = random.randint(1, 20)

        players = []
        for _ in range(num_player):
            hp = 8 + (level_players * 2) + (level_players * 5)
            ac = 13 + (level_players // 3)
            prof = 2 + (level_players - 1) // 4
            main = 2 + (level_players // 4)
            atk = prof + main
            avg_dmg = 5 + main
            players.append(Entidade(hp, ac, atk, avg_dmg))

        enemies = []
        for _ in range(num_enemy):
            hp = 8 + (level_enemies * 2) + (level_enemies * 5)
            ac = 13 + (level_enemies // 3)
            prof = 2 + (level_enemies - 1) // 4
            main = 2 + (level_enemies // 4)
            atk = prof + main
            avg_dmg = 5 + main
            enemies.append(Entidade(hp, ac, atk, avg_dmg))

        initial_player_hp = sum(p.hp for p in players)
        initial_enemy_hp = sum(e.hp for e in enemies)

        res = simular_batalha(players, enemies, max_rounds=1000)

        row = {
            'num_player': num_player,
            'level_players': level_players,
            'total_player_hp': initial_player_hp,
            'avg_player_ac': sum(p.ac for p in players)/num_player,
            'total_player_atk': sum(p.atk_bonus for p in players),
            'total_player_damage': sum(p.avg_damage for p in players),

            'num_enemy': num_enemy,
            'level_enemies': level_enemies,
            'total_enemy_hp': initial_enemy_hp,
            'avg_enemy_ac': sum(e.ac for e in enemies)/num_enemy,
            'total_enemy_atk': sum(e.atk_bonus for e in enemies),
            'total_enemy_damage': sum(e.avg_damage for e in enemies),

            'player_victory': res['outcome']
        }

        results.append(row)

    df = pd.DataFrame(results)
    df.to_csv(out_path, index=False)
    return df


if __name__ == '__main__':
    import time
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=100000)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--out', type=str, default='data/dataset.csv')
    args = parser.parse_args()

    t0 = time.time()
    df = gerar_dataset(n_sim=args.n, seed=args.seed, out_path=args.out)
    print('Dataset salvo em', args.out)
    print('Linhas:', len(df))
    print('Tempo:', time.time() - t0)