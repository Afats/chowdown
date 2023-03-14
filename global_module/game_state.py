import copy
# global class GameState

class GameState:
    def __init__(self):
        self.battle_link = ""
        self.battle_logs = []
        self.action_logs = []
        self.team = {}
        self.challenger = ""
        self.acceptor = ""
        self.curr_challenger_pokemon = ""
        self.curr_acceptor_pokemon = ""
        self.curr_turn = 0 # current turn being scraped
        self.curr_game_turn = 0 # the current turn in play -- may not contain battle logs

    # generate getters and setters for all attributes
    def get_battle_link(self):
        return self.battle_link
    
    def set_battle_link(self, battle_link):
        self.battle_link = battle_link
    
    def get_battle_logs(self):
        return copy.copy(self.battle_logs)
    
    def set_battle_logs(self, battle_logs):
        self.battle_logs = battle_logs
    
    def get_action_logs(self):
        return copy.copy(self.action_logs)
    
    def set_action_logs(self, action_logs):
        self.action_logs = action_logs
    
    def get_team(self):
        return copy.copy(self.team)
    
    def set_team(self, team):
        self.team = team
    
    def get_challenger(self):
        return self.challenger

    def set_challenger(self, challenger):
        self.challenger = challenger
    
    def get_acceptor(self):
        return self.acceptor
    
    def set_acceptor(self, acceptor):
        self.acceptor = acceptor
    
    def get_curr_challenger_pokemon(self):
        return self.curr_challenger_pokemon
    
    def set_curr_challenger_pokemon(self, curr_challenger_pokemon):
        self.curr_challenger_pokemon = curr_challenger_pokemon
    
    def get_curr_acceptor_pokemon(self):
        return self.curr_acceptor_pokemon
    
    def set_curr_acceptor_pokemon(self, curr_acceptor_pokemon):
        self.curr_acceptor_pokemon = curr_acceptor_pokemon
    
    def get_curr_turn(self):
        return self.curr_turn
    
    def set_curr_turn(self, curr_turn):
        self.curr_turn = curr_turn
    
    def get_curr_game_turn(self):
        return self.curr_game_turn
    
    def set_curr_game_turn(self, curr_game_turn):
        self.curr_game_turn = curr_game_turn

    # updating the pokemon in play and team pokemon info
    def update_battle_state(self, team, challenger, acceptor):
        self.set_team(team)
        self.set_challenger(challenger)
        self.set_acceptor(acceptor)

    def update_logs(self, battle_log, action_log):
        self.set_battle_logs(battle_log)
        self.set_action_logs(action_log)

    def update_entire_game_state(self, battle_state):
        self.set_battle_logs(battle_state.get_battle_logs())
        self.set_action_logs(battle_state.get_action_logs())
        self.set_team(battle_state.get_team())
        self.set_challenger(battle_state.get_challenger())
        self.set_acceptor(battle_state.get_acceptor())
        self.set_curr_challenger_pokemon(battle_state.get_curr_challenger_pokemon())
        self.set_curr_acceptor_pokemon(battle_state.get_curr_acceptor_pokemon())
        self.set_curr_turn(battle_state.get_curr_turn())
        self.set_curr_game_turn(battle_state.get_curr_game_turn())
    

