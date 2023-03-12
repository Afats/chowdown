from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent 
import time
import random
import re


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


battle_link = ""
all_battle_logs = []
team = {}
challenger = ""
acceptor = ""

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
        battle_logs = all_battle_logs

        # only 2 actions max per turn - move/switch poke, and move/switch poke (note: move itself may have multiple actions)
        # scrape b/w curr_turn and curr_game_turn
        x = -3
        y = 0
        for turn in range(curr_turn, curr_game_turn+1):
            # set starting challenger and acceptor pokemon
            x += 3
            y += 3

            # for turn 0, set challenger and acceptor pokemon
            if (x == 0):
                for j in range(x,y):
                    # all turns until current turn parsed
                    if j == x and get_turn_num(action_logs[j]) == curr_game_turn:
                        break    
                    elif j == x+1:
                        # challenger's pokemon
                        team[challenger][action_logs[j]] = {}
                    elif j == x+2:
                        # acceptor's pokemon
                        team[acceptor][action_logs[j]] = {}
            
            # for all other turns, parse the logs as moves/switches
            else:
                # call parse fucntion logic for moves
                    # parse all_battle_logs to remove common english words (except for turn/Turn, playernames and numbers)??
                    # check instance of word in all_battle_logs[i]
                # call parse function logic for switches if moves are not found
                for j in range(x,y):

                    if j == x and get_turn_num(action_logs[j]) == curr_game_turn:
                        break   
                    # figure out if it is a move/pokemon switch
                    # if move assign to right pokemon
                    # if switch assign to right player
                    else: 
                        continue
                        # assume action is a pokemon switch
                        # check if pokemon exists via pokeapi
                        # if pokemon exists, check the mention in battle logs:
                            # if sentence is Go! Pokemon!, challenger made a switch
                                # add pokemon to challenger's team
                            # else acceptor made a switch
                                # add pokemon to acceptor's team

                        # if neither of the above happened, action is a move
                        # find first instance of action and challenger's current pokemon in a modified all_battle_logs
                            # add move to challenger's current pokemon
                        # else find first instance of action and acceptor's current pokemon in a modified all_battle_logs
                            # add move to acceptor's current pokemon

    except:
        print("No turn battle logs found. :(")
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
    


# current turn being scraped
curr_turn = 0
# the current turn in play -- may not contain battle logs
curr_game_turn = 0

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
    
    while True:
        # all_battle_logs = get_all_battle_logs()
        # curr_game_turn = get_curr_game_turn(all_battle_logs)
        # scrape_battle_logs(curr_turn, curr_game_turn)
        # pick a random value between x and y seconds
        time_to_wait = random.SystemRandom().uniform(4.1,8.3)
        time.sleep(time_to_wait)
        

battle_link = input("Insert battle link or code: ")
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




     




    

        

