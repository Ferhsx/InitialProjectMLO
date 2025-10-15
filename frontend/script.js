document.addEventListener('DOMContentLoaded', () =>{
    const combatForm = document.getElementById('combat-form');
    const resultContainer = document.getElementById('result-container');
    const difficultyResult = document.getElementById('difficulty-result');
    const probabilityResult = document.getElementById('probability-result');

    combatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const combatData = {
            num_player: parseInt(document.getElementById('num_player').value),
            num_level_players: parseInt(document.getElementById('num_level_players').value),
            total_player_hp: parseInt(document.getElementById('total_player_hp').value),
            avg_player_ac: parseFloat(document.getElementById('avg_player_ac').value),
            total_player_atk: parseInt(document.getElementById('total_player_atk').value),
            num_enemy: parseInt(document.getElementById('num_enemy').value),
            total_enemy_hp: parseInt(document.getElementById('total_enemy_hp').value),
            avg_enemy_ac: parseFloat(document.getElementById('avg_enemy_ac').value),
            total_enemy_atk: parseInt(document.getElementById('total_enemy_atk').value),
        }

        try{
            const response = await fetch('http://localhost:8000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(combatData),
            });

            if(!response.ok){
                throw new Error('Erro na requisição');
            }

            const data = await response.json();
            difficultyResult.textContent = data.difficulty;
            probabilityResult.textContent = data.player_victory_probability;
            resultContainer.classList.remove('hidden');

        }catch(error){
            console.error('Erro ao prever a dificuldade:', error);
            alert('Erro ao prever a dificuldade. Tente novamente.');
        }
    })
})