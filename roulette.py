from collections import defaultdict
import random

# green_number = [0] 
red_number = [1, 3, 5, 7, 9, 19, 21, 23, 25, 27, 12, 14, 16, 18, 30, 32, 36] 
black_number = [2, 4, 6, 8, 10, 20, 22, 24, 26, 28, 34, 11, 13, 15, 17, 29, 31, 33, 35]

roulette_options = [(0, 'GREEN')]
roulette_options += [(x, 'RED') for x in red_number]
roulette_options += [(x, 'BLACK') for x in black_number]

class Consts:
    ROULETTE_TYPE = 'roulette'
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    MIN_PLAYERS = {
        'roulette': 2,
    }
    GAME_OPTIONS = {
        'roulette' : roulette_options
    }
    GAME_STATUSES = {
        'roulette' :[
            'collecting_bets',
            'spinning',
            'distributing_rewards'
        ]
    }

# singleton this
#list of game tables and their statuses
class Casino(object):

    def __init__(self, gameTables):
        self.gameTables = []        

    def add_table(self):
        pass

    def activate_table(self):
        pass
    
    def deactivate_table(self):
        pass

    def remove_table(self):
        pass
    
    #seperate threads for each table
    def run_tables(self):
        pass


# class Games:
    
#     def roulette()


class GameTable(object):

    def __init__(self, type_):
        #initialize players
        self.min_players = Consts.MIN_PLAYERS[type_]
        self.players = []
        self.status = Consts.ACTIVE

    def add_player(self, player):
        self.players.append(player)
    
    def remove_player(self, player):
        self.players.remove(player)
    
    def activate_table(self):
        self.status = Consts.ACTIVE
    
    def deactivate_table(self):
        self.status = Consts.INACTIVE
    
    @classmethod
    def active_table_required(cls, func):
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
        return wrapper


class Roulette(GameTable):
    
    def __init__(self):
        self.status_types = Consts.GAME_STATUSES[Consts.ROULETTE_TYPE]
        self.status = self.status_types[0] #collecting bets
        self.options = Consts.GAME_OPTIONS[Consts.ROULETTE_TYPE]
        self.bets = defaultdict(lambda: [])
        self.rewards = defaultdict(lambda: [])
        super(Roulette, self).__init__(Consts.ROULETTE_TYPE)
    
    def two_players_required(func): #len(self.players)>=2
        def wrapper():
            func()
        return wrapper

    #require player in self.players
    #require status placing bets
    @GameTable.active_table_required
    def place_bet(self, player, bet):
        amount = bet['amount']
        if player.balance >= amount:
            self.bets[player].append(bet)
            player.deduct(amount)
    
    #change status
    def close_bets(self):
        pass
        
    #require active
    #require status spinning
    @GameTable.active_table_required
    def spin(self): #random number output
        #change status to next 
        self.winner = random.choice(self.options)

    # (1, 'RED')
    def bet_result(self, bet, winning_bet):# x2, x11, x35, x0
        if bet['type'] == 'color':
            if winning_bet[1] == bet['value']:
                return 2
        elif bet['type'] == 'single':
            if winning_bet[0] == bet['value']:
                return 35
        elif bet['type'] == 'pair':
            if winning_bet[0] in bet['value']:
                return 11
        return 0

    def bet_results(self):
        for player in self.bets:
            for bet in self.bets[player]:
                res = self.bet_result(bet, self.winner)
                if res != 0:
                    self.rewards[player].append(res*bet['amount'])


    #require active
    #loop through players to give them profits
    #require status distributing rewards
    @GameTable.active_table_required
    def reward_players(self):
        for player in self.rewards:
            for reward in self.rewards[player]:
                player.win(reward)


class Player(object):
    
    def __init__(self, balance, name):
        # self.tables = []
        self.balance = balance
        self.name = name
        self.table_id = False
    
    def win(self, amount):
        if amount > 0:
            self.balance += amount

    def deduct(self, amount):
        if amount > 0:
            self.balance -= amount
    
    

    
