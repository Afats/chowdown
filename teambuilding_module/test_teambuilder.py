from teambuilding_module.teambuilder import GameState

# py file to test teambuilder.py, without having to waste time scraping

def init_game_state():
    game_state = GameState()
    game_state.set_battle_link("https://play.pokemonshowdown.com/battle-gen8randombattle-129325")
    game_state.set_challenger("brubbby")
    game_state.set_acceptor("afats")
    game_state.set_curr_challenger_pokemon("Challenger's Pokemon")
    game_state.set_curr_acceptor_pokemon("Acceptor's Pokemon")
    game_state.set_curr_turn(0)
    game_state.set_curr_game_turn(5)
    game_state.set_battle_logs(['Turn 0', '☆brubbby and ☆afats joined', 'Format:\n[Gen 9] Random Battle', 'Species Clause: Limit one of each Pokémon', 'HP Percentage Mod: HP is shown in percentages', 'Sleep Clause Mod: Limit one foe put to sleep', 'Battle started between brubbby and afats!', 'Go! Toxtricity (Toxtricity-Low-Key)!', 'afats sent out Volcanion!', 'Turn 1', 'Toxtricity used Overdrive!', "It's super effective!", '(The opposing Volcanion lost 85% of its health!)', 'Toxtricity lost some of its HP!', 'The opposing Volcanion used Sludge Bomb!', "It's not very effective...", '(Toxtricity lost 18% of its health!)', 'Turn 2', 'Toxtricity used Toxic Spikes!', 'Poison spikes were scattered on the ground all around the opposing team!', 'The opposing Volcanion used Sludge Bomb!', "It's not very effective...", '(Toxtricity lost 16% of its health!)', 'Turn 3', '☆afats: /save replay', 'Toxtricity used Toxic Spikes!', 'Poison spikes were scattered on the ground all around the opposing team!', 'The opposing Volcanion used Flame Charge!', '(Toxtricity lost 27% of its health!)', "The opposing Volcanion's Speed rose!", 'Turn 4', 'The opposing Volcanion used Flame Charge!', '(Toxtricity lost 26% of its health!)', "The opposing Volcanion's Speed rose!", 'Toxtricity used Overdrive!', "It's super effective!", '(The opposing Volcanion lost 15% of its health!)', 'The opposing Volcanion fainted!', 'Toxtricity lost some of its HP!', 'Toxtricity fainted!', 'Go! Altaria!', 'afats sent out Brambleghast!', 'The opposing Brambleghast was badly poisoned!', 'Turn 5'])
    game_state.set_action_logs(['Turn 0', 'Toxtricity-Low-Key', 'Volcanion', 'Turn 1', 'Overdrive', 'Sludge Bomb', 'Turn 2', 'Toxic Spikes', 'Sludge Bomb', 'Turn 3', 'Toxic Spikes', 'Flame Charge', 'Turn 4', 'Flame Charge', 'Overdrive', 'Altaria', 'Brambleghast', 'Turn 5'])
    return game_state

def test_teambuilder(game_state):
    update_teams(game_state)
