from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent 

# just a py page for ideas, experiemnts and code snippets


# todo: ask user if they are challenger or acceptor 
# todo: scrape from user's session instead of spectator if possible
# todo: write seperate setup code for battle factory
# todo: extract poke stuff on hover over pic??
# todo: use tooltip stats to make better naive predictions
# todo: cool user interface to enter battle link and scrape
# todo: send put request to current battle link as player (instead of just scraping as spectator)
# todo: get ditto's type/s from poke's bar
# endgame todo: keep track of any pokemon type changes from chat - ex. terastallizing, mega evolving, etc.



# rotate through IP addresses to avoid getting banned from pokemon showdown


# add random clicks, scrolls, and mouse movements to make your crawling seem less predictable. 
# also add random delays between actions to make it look more human-like.

# reduce scraping speed

# endgame: use headless chrome to avoid opening a browser window -- see if this works


# create a random real user agent to act as a spectator - avoids 0 users and no logs showing when scraping
ua = UserAgent()
userAgent = ua.random
# print(userAgent)

options = Options()
options.add_argument(f'user-agent={userAgent}')
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

battle_link = "https://play.pokemonshowdown.com/battle-gen9randombattle-1820046302"
driver.get(battle_link)

# initally wait min. seconds for page to load
driver.implicitly_wait(7)


# scrape inner message-log div from battle link
# use until.elementLocated() ?
print("scraping...")


# turns are in h2 tags
print([turn.text for turn in driver.find_elements(By.XPATH, "//div[@class='inner message-log']//h2[@class='battle-history']")])

# get battle log for each turn
# if pokemon is in battle log, it was sent out
# check what poekmon was mentioned in the move and add move to opponent or user dictionary
     # alt. check tooltip for opponent pokemon move deets
print([battle_log.text for battle_log in driver.find_elements(By.XPATH, "//div[@class='inner message-log']//div[@class='battle-history']/strong[1]")])


battle_logs = driver.find_elements(By.XPATH, "//div[@class='inner message-log']/*[self::div or self::h2][not(@class='spacer battle-history')]")
for log in battle_logs:
    print(log.text)

battle_logs.insert(0, "Turn 0")

# usernames in div class "trainer trainer-near" 
# opponent usernames in div class "trainer trainer-far"

# for battle factory/similar (doesn't apply to random battles/similar)
    # afats's team:
        # Yveltal / Rayquaza / Heatran / Magearna / Palkia / Marshadow
    # bruvvvvvvvvvvv's team:
        # Palkia / Landorus / Lunala / Magearna / Ho-Oh / Necrozma-Dusk-Mane
# OR "teamicons" class inside has pokemon names to get pokemon names? 
# active pokemon deets in "controls" and "tooltip tooltip-activepokemon" divs
# active pokemon sent out by user and opponent in div aria-label "Active Pokemon" and 
# all active pokemon deets and type (incl. terra type) in "tooltip tooltip-activepokemon" 
# hover over opponent pokemon to get their deets in "tooltip tooltip-activepokemon" 
# scrape all of my inactive pokemon from "chooseSwitch" button names


# keep track of last turn scraped
# continously scrape the battle link for new messages every 4-7 seconds or until turn x elementLocated
    # if turns have passed, scrape the latest turn
    
    # extract the pokemon names and moves used (usually before an "!" and in bold) OR fom tooltips
    # use pokeapi to get the pokemon types move type and info
    # record the pokemon and move used in 2 dictionaries (user and opponent)
    # print battling pokemon, types and moves used
    # if pokekon has a weak type match-up to opponent, suggest withdrawing pokemon
    # print a recommendation for the next move to use depending on opponent pokemon: super effective, not very effective, neutral, etc.