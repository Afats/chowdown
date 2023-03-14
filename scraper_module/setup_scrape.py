from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent 
from global_module.game_state import GameState



# parse input battle link
def parse_battle_link(battle_link):
    # remove leading and trailing whitespace
    battle_link = battle_link.strip()
    # if link doesn't start with https, add https://play.pokemonshowdown.com/
    if not battle_link.startswith("https://play.pokemonshowdown.com/"):
        battle_link = "https://play.pokemonshowdown.com/" + battle_link

    return battle_link


# get challenger and acceptor usernames
def get_players():
    global challenger
    global acceptor
    global team
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


# globals for chromedriver usage

# create a random real user agent to act as a spectator - avoids 0 users and no logs showing when scraping
ua = UserAgent()
userAgent = ua.random
# print(userAgent)

options = Options()
options.add_argument(f'user-agent={userAgent}')
options.add_experimental_option("detach", True)

game_state = GameState()
# battle_link = input("Insert battle link or code (only after turn 1 has been played): ")
# battle_link = parse_battle_link(battle_link)
# driver = webdriver.Chrome(options=options)
# driver.get(battle_link)
# game_state.set_battle_link(battle_link)
# # initally wait min. seconds for js in page to load
# driver.implicitly_wait(10)