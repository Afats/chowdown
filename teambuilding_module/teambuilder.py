from global_module.game_state import GameState
from helper_module.helper import *
from scraper_module.battle_logs import *
from scraper_module.setup_scrape import *
from ui_module.ui import *


# 0 actions: both pokemon flinch/paralyzed, etc. and are unable to make a move
# 1 actions: 1 pokemon flinches/paralyzed, etc. and is unable to make a move
# 2 actions: both pokemon make a move
# 3 actions: 1 pokemon faints
# 4 actions: 2 pokemon faint
# 5+ actions: multi-hit moves 
# find the number of actions per turn
def find_num_moves_per_turn(curr_turn, action_logs):
    x = 0
    y = 0

    for i in range(len(action_logs)):
        if get_turn_string(curr_turn) in action_logs[i]:
            x = i
            break

    for i in range(x, len(action_logs)):
        if get_turn_string(curr_turn+1) in action_logs[i]:
            y = i
            break

    return (x,y)


# create/update teams based on battle_logs and action_logs
def update_teams(game_state):

    try:
        # unpack game_state
        battle_logs = game_state.get_battle_logs()
        action_logs = game_state.get_action_logs()
        team = game_state.get_team()
        challenger = game_state.get_challenger()
        acceptor = game_state.get_acceptor()
        curr_turn = game_state.get_curr_turn()
        curr_game_turn = game_state.get_curr_game_turn()
        curr_challenger_pokemon = game_state.get_curr_challenger_pokemon()
        curr_acceptor_pokemon = game_state.get_curr_acceptor_pokemon()

        print("Battle logs: ", battle_logs)
        print()
        print("Action logs: ", action_logs)
        print()


        # TODO !: only 1 action max per turn in usual - one pokemon fliches/paralyzed, etc.
        # !!: only 2 actions max per turn in usual - move/switch poke, and move/switch poke (note: move itself may have multiple actions)
        # !!!!: 3-4 actions max per turn if 1 or both pokemon faint
        # scrape b/w curr_turn and curr_game_turn
    
        for turn in range(curr_turn, curr_game_turn):
            # set starting challenger and acceptor pokemon
            print("Curr turn being processed: ", turn)
           
            # for turn 0, set challenger and acceptor pokemon -- always 2 pokemon
            if (turn == 0):
                try: 
                    print("Turn 0: Setting challenger and acceptor starting pokemon...") 
                    for j in range(1,3):
               
                        if j == 1:
                            # challenger's pokemon
                            # print("Challenger's starting pokemon to parse:", action_logs[j])
                            pokemon = get_pokemon_info(action_logs[j])
                            team[challenger] = {}
                            team[challenger][pokemon.name] = {}
                            team[challenger][pokemon.name]['pokemon_info'] = pokemon
                            curr_challenger_pokemon = pokemon.name
                            # print("Team state:", team)

                        else:
                            # acceptor's pokemon
                            # print("Acceptors's starting pokemon to parse:", action_logs[j])
                            pokemon = get_pokemon_info(action_logs[j])
                            team[acceptor] = {}
                            team[acceptor][pokemon.name] = {}
                            team[acceptor][pokemon.name]['pokemon_info'] = pokemon
                            curr_acceptor_pokemon = pokemon.name
                            # print("Team state:", team)

                except Exception as e:
                    print("Error in parsing challenger and acceptor starting pokemon: ", e)
                    break

                else:
                    # update game state
                    # print("!!!! Starting pokemon set! Updating game state...")
                    game_state.update_battle_state(team, curr_challenger_pokemon, curr_acceptor_pokemon)
                    game_state.update_logs(battle_logs, action_logs)
                    print("Chall pokemon in play:", game_state.get_curr_challenger_pokemon())
                    print("Accep pokemon in play:", game_state.get_curr_acceptor_pokemon())
            

            # for all other turns, parse the actions as moves/switches
            else:

                (x,y) = find_num_moves_per_turn(turn, action_logs)
                # Ex. "Turn 5, Parsing actions from Turn 5 to Turn 6..."
                print("Turn", turn, ": Parsing actions from", action_logs[x], "to" , action_logs[y], "...")

                for j in range(x+1,y):
                    
                    is_move = False
                    try:
                        pokemon = str(action_logs[j]).strip()
                        # pypokedex object
                        pokemon = get_pokemon_info(pokemon)
                        # to silence a weird error where pokemon object would equal to -1 even though it is a pokemon object
                        if type(pokemon) == int:
                            raise Exception("Pokemon not found")

                        # find pokemon in the sentence "Go! Pokemon!" in battle logs: challenger made a switch
                        # find acceptor name and pokemon in battle logs: acceptor made a switch
                        for log in battle_logs:
                            if "Go! " in log and pokemon.name in log:
                                # challenger made a switch 
                                # print("Challenger switch log: ", log)
                                if pokemon.name in team[challenger]:
                                    curr_challenger_pokemon = pokemon.name
                                    

                                else:   
                                    team[challenger][pokemon.name] = {}
                                    team[challenger][pokemon.name]['pokemon_info'] = pokemon
                                    curr_challenger_pokemon = pokemon.name
                                    
                                    
                                battle_logs = battle_logs[battle_logs.index(log)+1:]
                                print("Challenger's curr pokemon:", game_state.get_curr_challenger_pokemon())
                                # print("Team state:", team)
                                # print("Battle logs post-mod.:", battle_logs)
                                break
                            
                            elif acceptor in log and pokemon.name in log:
                                # acceptor made a switch
                                
                                # print("Acceptor switch log: ", log)
                                if pokemon.name in team[acceptor]:
                                    curr_acceptor_pokemon = pokemon.name

                                else:   
                                    team[acceptor][pokemon.name] = {}
                                    team[acceptor][pokemon.name]['pokemon_info'] = pokemon
                                    curr_acceptor_pokemon = pokemon.name
                                    
                                    
                                battle_logs = battle_logs[battle_logs.index(log)+1:]
                                print("Acceptor's curr pokemon:", curr_acceptor_pokemon)
                                # print("Team state:", team)
                                # print("Battle logs post-mod.:", battle_logs)
                                break

                    except:
                        # action is not a pokemon
                        print(action_logs[j], "is not a pokemon, so it's probably a move.")
                        is_move = True

                    else:     
                        # update game state
                        # print("!!!! Pokemon found! Updating game state...")
                        game_state.update_battle_state(team, curr_challenger_pokemon, curr_acceptor_pokemon)
                        game_state.update_logs(battle_logs, action_logs)
                        print("Chall pokemon in play:", game_state.get_curr_challenger_pokemon())
                        print("Accep pokemon in play:", game_state.get_curr_acceptor_pokemon())

                    
                    # if the above didn't happen, action is a move
                    # find first instance of action and challenger's current pokemon in a modified battle_logs
                        # add move to challenger's current pokemon
                    # else find first instance of action and acceptor's current pokemon in a modified battle_logs
                        # add move to acceptor's current pokemon

                    # can't have moves w/o pokemon having played them
                    if (is_move):
                        try:
                            move_added = False
                            move = str(action_logs[j]).strip()
                            # print("Assuming", move, "is a move.")

                            # find first instance of move and challenger's current pokemon in a modified battle_logs
                            for log in battle_logs:

                                # in case it has been changed ???
                                curr_challenger_pokemon = game_state.get_curr_challenger_pokemon()
                                curr_acceptor_pokemon = game_state.get_curr_acceptor_pokemon()

                                # if pokemon has hyphen in name (e.g. Toxtricity-Low-Key), remove hyphen and results in Toxtricity to match w logs
                                if "-" in curr_challenger_pokemon:
                                    challenger_pokemon_search = curr_challenger_pokemon.split("-")[0]

                                else:
                                    challenger_pokemon_search = curr_challenger_pokemon


                                # print("Checking if", move, "and", curr_challenger_pokemon, "is in", log, "...")

                                if move in log and challenger_pokemon_search in log:
                                    # add move to challenger's current pokemon
                                    print("Adding", move, "to", curr_challenger_pokemon, "for", challenger, "...")
                                    # check if 'moves' key exists
                                    if 'moves' not in team[challenger][curr_challenger_pokemon]:
                                        team[challenger][curr_challenger_pokemon]['moves'] = []
                                    # avoid duplicate moves
                                    if move not in team[challenger][curr_challenger_pokemon]['moves']:
                                        team[challenger][curr_challenger_pokemon]['moves'].append(move)
                                    # remove all logs up to and including the move
                                    battle_logs = battle_logs[battle_logs.index(log)+1:]
                                    # print("Team state:", team)
                                    # print("Battle logs post-mod.:", battle_logs)
                                    move_added = True
                                    break
                                
                                # print("Checking if", move, "and", curr_acceptor_pokemon, "is in", log, "...")

                                if "-" in curr_acceptor_pokemon:
                                    acceptor_pokemon_search = curr_acceptor_pokemon.split("-")[0] 
                                else:
                                    acceptor_pokemon_search = curr_acceptor_pokemon

                                if move in log and acceptor_pokemon_search in log:
                                    # add move to acceptor's current pokemon
                                    print("Adding", move, "to", curr_acceptor_pokemon, "for", acceptor, "...")
                                    # check if 'moves' key exists
                                    if 'moves' not in team[acceptor][curr_acceptor_pokemon]:
                                        team[acceptor][curr_acceptor_pokemon]['moves'] = []
                                    

                                    if move not in team[acceptor][curr_acceptor_pokemon]['moves']:
                                        team[acceptor][curr_acceptor_pokemon]['moves'].append(move)
                                    # remove all logs up to and including the move
                                    battle_logs = battle_logs[battle_logs.index(log)+1:]
                                    # print("Team state:", team)
                                    # print("Battle logs post-mod.:", battle_logs)
                                    move_added = True
                                    break
                                
                        except Exception as e:
                            print("Error in move parsing: ", e)

                        else:
                            if move_added:
                                # update game state
                                # print("!!!! Move found! Updating game state...")
                                game_state.update_battle_state(team, curr_challenger_pokemon, curr_acceptor_pokemon)
                                game_state.update_logs(battle_logs, action_logs)
                                print("Chall pokemon in play: ", game_state.get_curr_challenger_pokemon())
                                print("Accep pokemon in play: ", game_state.get_curr_acceptor_pokemon())
                            else:
                                print("Move not added:", move)

    except Exception as e:
        print("Error in update_teams: ", e)
        return 0
    
    else:
        print("Teams updated successfully.")
        print("Challenger's team:", team[challenger])
        print("Acceptor's team:", team[acceptor])
        print("---------------------------------")
        return 1