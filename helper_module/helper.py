from scraper_module.setup_scrape import *
import pypokedex

# general helper functions

# get turn number from turn string
def get_turn_num(turn_string):
    try: 
        return int(turn_string.split()[1])
    except:
        print("No turn number found. :(")
        return -1
    
    
# get the current turn in play
def get_curr_game_turn_from_logs(battle_logs):
    try:
        # get the last element in battle_logs, which is the current turn in play
        curr_game_turn = get_turn_num(battle_logs[-1])
        print("Current game turn:", curr_game_turn)
        return curr_game_turn
    except:
        print("No current turn found. :(")
        return 0
    

# helper to get pypokedex object and capitalize pokemon name
def get_pokemon_info(pokemon_name):
    try: 
        pokemon = pypokedex.get(name=pokemon_name.strip())
        pokemon.name = pokemon.name.capitalize()
        return pokemon
    except:
        return -1
    
