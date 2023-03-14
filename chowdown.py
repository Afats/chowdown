import time
import random
from copy import deepcopy

#----------- local imports -------------
from global_module.game_state import GameState
from scraper_module.setup_scrape import *
from helper_module.helper import *
from scraper_module.battle_logs import *
from teambuilding_module.teambuilder import *
from teambuilding_module.test_teambuilder import *
from ui_module.ui import *
#---------------------------------------
      
    

# chowdown every 4-7 seconds
def chowdown(game_state):
    print("Scraping...\n")
    get_players()
    game_state.set_battle_logs(scrape_battle_logs())
    game_state.set_curr_game_turn(get_curr_game_turn_from_logs(game_state.get_battle_logs()))
    game_state.set_action_logs(scrape_action_logs())
    game_state.set_team(update_teams(game_state))
    print("Team states: ", game_state.get_team())
    
    while True:
        # all_battle_logs = get_all_battle_logs()
        # curr_game_turn = get_curr_game_turn(all_battle_logs)
        # scrape_battle_logs(curr_turn, curr_game_turn)
        # pick a random value between x and y seconds
        time_to_wait = random.SystemRandom().uniform(4.1,8.3)
        time.sleep(time_to_wait)
        

def main():
    # set initial game state before chowing down
    #game_state = GameState()
    #chowdown(game_state)

    init_state = init_game_state()
    game_state = deepcopy(init_state)
    update_teams(game_state)

main()



# Business logic:
# ----------------
# NOTE: spectator always sees from challenger's perspective
# spectator scrape (only works when both players send out their starting pokemon for now -- write seperate setup code for battle factory):
    # 0. get battle link/code
    # 0.5. get battle type (random battle, battle factory, etc.)
    # 1. get both player names
    # 1.5: ask user if they're challenger or acceptor
    # 2. get all_battle_logs so far
    # 3. curr_game_turn: get the curr turn being played from end of all_battle_logs (Ex. if turn 6 is curr_game_turn, then the battle is currently on turn 6 and is yet to finish)
    # 4. scrape the battle logs for each curr_turn, where curr_turn <= curr_game_turn. currr_turn is initially 0 (Turn 0 is pokemon being sent out). 
        # 4.1. for turn 0, assign starting pokemon to each player (based on near/far trainer and starting pokemon text order)
        # 4.2. for [turn 1, curr_game_turn-1] (inclusive), compare turn logs with battle logs to get:
        #   4.2.1 the pokemon that was sent out and assign to either challenger or acceptor
        #   4.2.2 get moves used in the turn and assign to either challenger's pokemon or acceptor pokemon (max 4 moves per pokemon)
        #   4.2.3 add metadata to each pokemon object (Ex. type, moves, etc.) / update accordingly
                # get pokemon speed range from pokeapi
                # get pokemon type from pokeapi
                # get pokemon type/s weaknesses from pokeapi
                # get pokemon type/s resistances from pokeapi
                # get pokemon type/s immunities from pokeapi
                # get pokemon move counts, type and category from pokeapi
    
    # 5. for current game turn:
        # display the current game turn
        # display both player's revealed pokemon, and moves used
        # display the current game state: 
            #  challenger's pokemon, acceptor's pokemon
            #  challenger's pokemon's moves, acceptor's pokemon's moves under 2 adjacent columns
            #  highlight pokemon w faster speed w lightining bolt emoji / some color
            #  highlight pokemon w a type/s matchup advantage w a star emoji / color
            #  highlight moves w a type/s 2x matchup advantage w a star emoji / color
            #  highlight moves w a type/s 4x matchup advantage w a skull emoji / color
            #  highlight moves w a type/s 0x matchup advantage (immunity to it) w a 0 emoji / color
            #  highlight moves w a type/s 0.5x matchup advantage (resistance to it) w a 1/2 emoji / color
        # display recommended move/s for each pokemon
            # if no 4x/2x/neutral moves available, recommended withdrawing/status?




     




    

        

