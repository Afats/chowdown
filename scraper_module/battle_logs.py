from scraper_module.setup_scrape import *
from helper_module.helper import *

# TODO: condense multi-hit moves into 1 action in scrape_action_logs()

# scrape the turn number
def scrape_turn(i):
    try: 
        turn = driver.find_element(By.XPATH, f"//div[@class='inner message-log']/h2[@class='battle-history'][{i}]")
        return get_turn_num(turn.text)
    except:
        print("no turn found")
        return 0

# get all battle logs from the start of the battle to the current turn in play
def scrape_battle_logs():
    try:
        battle_logs_scraped = driver.find_elements(By.XPATH, "//div[@class='inner message-log']/*[self::div or self::h2][not(@class='spacer battle-history')]")
        battle_logs = []
        for log in battle_logs_scraped:
            battle_logs.append(log.text)

        battle_logs.insert(0, "Turn 0")
        print("Battle logs scraped: ", battle_logs)
        print()
        return battle_logs
    except Exception as e:
        print("Error in scrape_battle_logs: ", e)
        return 0
    

# scrape keywords from battle logs
def scrape_action_logs():
    try:
        action_logs_scraped = driver.find_elements(By.XPATH, "//div[@class='inner message-log']//div[@class='battle-history']/strong[1] | //div[@class='inner message-log']//h2[@class='battle-history']")
        action_logs = []
        
        for log in action_logs_scraped:
            action_logs.append(log.text)

        # !! todo: condense multi-hit moves into 1 action

        action_logs.insert(0, "Turn 0")
        print("Actions scraped: ", action_logs)
        print()
        return action_logs

    except Exception as e:
        print("Error in scrape_action_logs: ", e)
        return 0