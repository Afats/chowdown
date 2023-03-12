from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent 
import time
import random
import re
import pypokedex


# create a random real user agent to act as a spectator - avoids 0 users and no logs showing when scraping
ua = UserAgent()
userAgent = ua.random
# print(userAgent)

options = Options()
options.add_argument(f'user-agent={userAgent}')
options.add_experimental_option("detach", True)

# driver = webdriver.Chrome(options=options)
# battle_link = "https://play.pokemonshowdown.com/battle-gen9randombattle-1820033851"
# driver.get(battle_link)
# # initally wait min. seconds for page to load
# driver.implicitly_wait(7)

# globals
battle_link = ""
all_battle_logs = []
team = {}
challenger = ""
acceptor = ""
curr_challenger_pokemon = ""
curr_acceptor_pokemon = ""
# current turn being scraped
curr_turn = 0
# the current turn in play -- may not contain battle logs
curr_game_turn = 0

#------------------------------------------------------------

# parse input battle link
def parse_battle_link(battle_link):
    # remove leading and trailing whitespace
    battle_link = battle_link.strip()
    # if link doesn't start with https, add https://play.pokemonshowdown.com/
    if not battle_link.startswith("https://play.pokemonshowdown.com/"):
        battle_link = "https://play.pokemonshowdown.com/" + battle_link

    return battle_link
    




# helper function: get turn number from turn string
# Ex. get "x" from "Turn x" using split()
def get_turn_num(turn_string):
    try: 
        return int(turn_string.split()[1])
    except:
        return -1


# helper function: scrape the turn number
def scrape_turn(i):
    try: 
        turn = driver.find_element(By.XPATH, f"//div[@class='inner message-log']/h2[@class='battle-history'][{i}]")
        return get_turn_num(turn.text)
    except:
        print("no turn found")
        return 0
    
# helper to get pypokedex object and capitalize pokemon name
def get_pokemon_info(pokemon_name):
    try: 
        pokemon = pypokedex.get(name=pokemon_name.strip())
        pokemon.name = pokemon.name.capitalize()
        return pokemon
    except:
        return -1
    

# get the current turn in play
def get_curr_game_turn(battle_logs):
    try:
        # get the last element in battle_logs, which is the current turn in play
        curr_game_turn = get_turn_num(battle_logs[-1])
        print("Current game turn:", curr_game_turn)
        return curr_game_turn
    except:
        print("No current turn found. :(")
        return 0



# get challenger and acceptor usernames
def get_players():
    global challenger
    global acceptor
    try:
        # scrape the player's username
        player = driver.find_element(By.XPATH, "//div[@class='trainer trainer-near']")
        challenger = player.text
        print("Challenger:", challenger.strip())
        team[challenger] = {}
        # scrape the opponent's username
        player = driver.find_element(By.XPATH, "//div[@class='trainer trainer-far']")
        acceptor = player.text
        print("Acceptor:", acceptor.strip())
        print()
        team[acceptor] = {}
        return 1
    
    except:
        print("No players found. :(")
        return 0


# scrape until curr_turn is curr_game_turn
def scrape_battle_logs(curr_turn, curr_game_turn):
    global all_battle_logs
    global curr_challenger_pokemon
    global curr_acceptor_pokemon
    global team

    try:
        action_logs_scraped = driver.find_elements(By.XPATH, "//div[@class='inner message-log']//div[@class='battle-history']/strong[1] | //div[@class='inner message-log']//h2[@class='battle-history']")
        action_logs = []
        
        for log in action_logs_scraped:
            action_logs.append(log.text)

        # !! todo: condense multi-hit moves into 1 action

        action_logs.insert(0, "Turn 0")
        print("Actions: ", action_logs)
        print()

        # local battle logs instance
        battle_logs = all_battle_logs.copy()

        # TODO !: only 1 action max per turn in usual - one pokemon fliches/paralyzed, etc.
        # !!: only 2 actions max per turn in usual - move/switch poke, and move/switch poke (note: move itself may have multiple actions)
        # !!!!: 3-4 actions max per turn if 1 or both pokemon faint
        # scrape b/w curr_turn and curr_game_turn
        x_inc = 0
        x = -3
        y = 0
        for turn in range(curr_turn, curr_game_turn+1):
            # set starting challenger and acceptor pokemon
            x += 3 + x_inc
            y += 3
            x_inc = 0

            # for turn 0, set challenger and acceptor pokemon
            if (x == 0):
                print("Turn 0: Setting challenger and acceptor starting pokemon...") 
                for j in range(x,y):
                    # all turns until current turn parsed
                    if j == x and get_turn_num(action_logs[j]) == curr_game_turn:
                        print("All turns until current game turn parsed.")
                        break    
                    elif j == x+1:
                        # challenger's pokemon
                        print("Challenger's starting pokemon to parse:", action_logs[j])
                        pokemon = get_pokemon_info(action_logs[j])
                        team[challenger][pokemon.name] = {}
                        team[challenger][pokemon.name]['pokemon_info'] = pokemon
                        curr_challenger_pokemon = pokemon.name
                        # print("Team state:", team)
                    elif j == x+2:
                        # acceptor's pokemon
                        print("Accpetors's starting pokemon to parse:", action_logs[j])
                        pokemon = get_pokemon_info(action_logs[j])
                        team[acceptor][pokemon.name] = {}
                        team[acceptor][pokemon.name]['pokemon_info'] = pokemon
                        curr_acceptor_pokemon = pokemon.name
                        # print("Team state:", team)
            
            # for all other turns, parse the logs as moves/switches
            else:
                
                # parse all_battle_logs to remove common english words (except for turn/Turn, playernames and numbers)??
                   
                print("Turn", turn, ": Parsing actions from ", action_logs[x], "to " , action_logs[y-1], "...")
                
                # check if action_logs[y] is a turn number -- to deal w 1 or 2 faints per turn
                if get_turn_num(action_logs[y]) == -1:
                    # increment y until get_turn_num(action_logs[y-1]) != -1
                    x_inc = 0
                    while get_turn_num(action_logs[y]) == -1:
                        y += 1
                        x_inc += 1

                for j in range(x,y):

                    if j == x and get_turn_num(action_logs[j]) == curr_game_turn:
                        print("All turns until current game turn parsed, and curr_turn >=1 .")
                        break   

                    elif j == x:
                        continue
                    # figure out if it is a move/pokemon switch
                    # if move assign to right pokemon
                    # if switch assign to right player
                    else: 
                        # assume action is a pokemon (switch)
                        # check ifa pokemon exists via pokeapi
                        # if pokemon exists, check the mention in battle logs:
                            # if sentence is Go! Pokemon!, challenger made a switch
                                # add pokemon to challenger's team
                            # else acceptor made a switch
                                # add pokemon to acceptor's team
                        
                        is_move = False

                        try:
                            pokemon = str(action_logs[j]).strip()
                            # assign pokemon to pypokedex object
                            pokemon = get_pokemon_info(pokemon)
                            print(action_logs[j], ": ", pokemon)

                            # to silence a weird error where pokemon object would equal to -1 even though it is a pokemon object
                            if type(pokemon) == int:
                                print(action_logs[j], "is not a pokemon.")
                                raise Exception("Pokemon not found")

                            # find pokemon in the sentence "Go! Pokemon!" in battle logs: challenger made a switch
                            # find acceptor name and pokemon in battle logs: acceptor made a switch
                            for log in battle_logs:
                                if "Go! " in log and pokemon.name in log:
                                    # challenger made a switch 
                                    print("Challenegr switch Log: ", log)
                                    if pokemon.name in team[challenger]:
                                        curr_challenger_pokemon = pokemon.name

                                    else:   
                                        team[challenger][pokemon.name] = {}
                                        team[challenger][pokemon.name]['pokemon_info'] = pokemon
                                        curr_challenger_pokemon = pokemon.name
                                        
                                        
                                    battle_logs = battle_logs[battle_logs.index(log)+1:]
                                    print("Challenger's curr pokemon:", curr_challenger_pokemon)
                                    print("Team state:", team)
                                    # print("Battle logs post-mod.:", battle_logs)
                                    break
                                
                                elif acceptor in log and pokemon.name in log:
                                    # acceptor made a switch
                                    
                                    print("Acceptor switch Log: ", log)
                                    if pokemon.name in team[acceptor]:
                                        curr_acceptor_pokemon = pokemon.name

                                    else:   
                                        team[acceptor][pokemon.name] = {}
                                        team[acceptor][pokemon.name]['pokemon_info'] = pokemon
                                        curr_acceptor_pokemon = pokemon.name
                                        
                                        
                                    battle_logs = battle_logs[battle_logs.index(log)+1:]
                                    print("Acceptor's curr pokemon:", curr_acceptor_pokemon)
                                    print("Team state:", team)
                                    # print("Battle logs post-mod.:", battle_logs)
                                    break

                        except:
                            # action is not a pokemon
                            print(action_logs[j], "is not a pokemon.")
                            is_move = True
                        
                        # if the above didn't happen, action is a move
                        # find first instance of action and challenger's current pokemon in a modified all_battle_logs
                            # add move to challenger's current pokemon
                        # else find first instance of action and acceptor's current pokemon in a modified all_battle_logs
                            # add move to acceptor's current pokemon

                        if (is_move):
                            try:
                                move = str(action_logs[j]).strip()
                                print("Assuming", move, "is a move.")

                                # find first instance of move and challenger's current pokemon in a modified all_battle_logs
                                for log in battle_logs:
                                    if move in log and curr_challenger_pokemon in log:
                                        # add move to challenger's current pokemon
                                        print("Adding ", move, "to ", curr_challenger_pokemon, "for ", challenger, "...")
                                        # check if 'moves' key exists
                                        if 'moves' not in team[challenger][curr_challenger_pokemon]:
                                            team[challenger][curr_challenger_pokemon]['moves'] = []
                                        # avoid duplicate moves
                                        if move not in team[challenger][curr_challenger_pokemon]['moves']:
                                            team[challenger][curr_challenger_pokemon]['moves'].append(move)
                                        # remove all logs up to and including the move
                                        battle_logs = battle_logs[battle_logs.index(log)+1:]
                                        print("Team state:", team)
                                        # print("Battle logs post-mod.:", battle_logs)
                                        break

                                    if move in log and curr_acceptor_pokemon in log:
                                        # add move to acceptor's current pokemon
                                        print("Adding ", move, "to ", curr_acceptor_pokemon, "for ", acceptor, "...")
                                        # check if 'moves' key exists
                                        if 'moves' not in team[acceptor][curr_acceptor_pokemon]:
                                            team[acceptor][curr_acceptor_pokemon]['moves'] = []
                                        

                                        if move not in team[acceptor][curr_acceptor_pokemon]['moves']:
                                            team[acceptor][curr_acceptor_pokemon]['moves'].append(move)
                                        # remove all logs up to and including the move
                                        battle_logs = battle_logs[battle_logs.index(log)+1:]
                                        print("Team state:", team)
                                        # print("Battle logs post-mod.:", battle_logs)
                                        break
                                   
                            except Exception as e:
                                print("Error in move parsing: ", e)
                                

    except Exception as e:
        print("Error in scrape_battle_logs: ", e)
        return 0
    
      

# get all battle logs from the start of the battle to the current turn in play
def get_all_battle_logs():
    try:
        battle_logs_scraped = driver.find_elements(By.XPATH, "//div[@class='inner message-log']/*[self::div or self::h2][not(@class='spacer battle-history')]")
        # print(battle_logs_scraped.text)
        battle_logs = []
        for log in battle_logs_scraped:
            battle_logs.append(log.text)

        battle_logs.insert(0, "Turn 0")
        print("Battle logs: ", battle_logs)
        print()
        return battle_logs
    except:
        print("No battle logs found. :(")
        return 0
    

# run main function every 4-7 seconds
def main():
    global curr_turn
    global curr_game_turn
    global battle_link
    global all_battle_logs
    
    print("Scraping...\n")
    get_players()
    all_battle_logs = get_all_battle_logs()
    curr_game_turn = get_curr_game_turn(all_battle_logs)
    scrape_battle_logs(curr_turn, curr_game_turn)
    print("Team states: ", team)
    
    while True:
        # all_battle_logs = get_all_battle_logs()
        # curr_game_turn = get_curr_game_turn(all_battle_logs)
        # scrape_battle_logs(curr_turn, curr_game_turn)
        # pick a random value between x and y seconds
        time_to_wait = random.SystemRandom().uniform(4.1,8.3)
        time.sleep(time_to_wait)
        

battle_link = input("Insert battle link or code (curr. after turn 1 ONLY): ")
battle_link = parse_battle_link(battle_link)
driver = webdriver.Chrome(options=options)
driver.get(battle_link)
# initally wait min. seconds for js in page to load
driver.implicitly_wait(7)
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




     




    

        

