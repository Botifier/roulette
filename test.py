import unittest
import mock
from roulette import (
    Casino,
    GameTable,
    Roulette,
    Player,
    Consts
)


class TestCasino(unittest.TestCase):
    def setUp(self):
        game_table = GameTable(Consts.ROULETTE_TYPE)
        casino = Casino()
    

class TestGameTable(unittest.TestCase):
    def setUp(self):
        self.player = Player(100, 'Kaido')
        self.game_table = GameTable('roulette')        

    def test_add_player(self):
        self.game_table.add_player(self.player)
        self.assertEqual(self.game_table.players, [self.player])

    def test_remove_player(self):
        self.game_table.players = [self.player]
        self.game_table.remove_player(self.player)
        self.assertEqual(self.game_table.players, [])
    
    def test_activate_table(self):
        self.game_table.status = 'inactive'
        self.game_table.activate_table()
        self.assertEqual(self.game_table.status, 'active')

    def test_deactivate_table(self):
        self.game_table.deactivate_table()
        self.assertEqual(self.game_table.status, 'inactive')
        

class TestRoulette(unittest.TestCase):
    def setUp(self):
        self.player = Player(100, 'Kaido')
        self.roulette = Roulette()
        self.bet1 = {
            'type': 'color',
            'value': 'BLACK',
            'amount': 20
        }
        # should be rejected
        self.bet2 = {
            'type': 'color',
            'value': 'RED',
            'amount': 200
        }
        self.bet3 = {
            'type': 'single',
            'value': 1,
            'amount': 30
        }
        self.bet4 = {
            'type': 'pair',
            'value': {1,2},
            'amount': 10
        }
        

    #test only running when state==collecting bets
    # bet:'black', [1], [1,2] : amount
    #only allow bet collection when sufficient funds otherwise reject
    def test_place_bet(self):
        self.roulette.place_bet(self.player, self.bet1)
        self.roulette.place_bet(self.player, self.bet2)
        self.assertEqual(self.player.balance, 80)
        self.assertEqual(self.roulette.bets, {self.player: [self.bet1]})

    # test only running when state==spinning
    #generate random output    
    def test_spin(self):
        with mock.patch('random.choice', return_value=(1, 'RED')):
            self.roulette.spin()
            self.assertEqual(self.roulette.winner, (1, 'RED'))
    
    def test_bet_result(self):
        self.assertEqual(self.roulette.bet_result(self.bet1, (2, 'BLACK')), 2)
        self.assertEqual(self.roulette.bet_result(self.bet2, (2, 'BLACK')), 0)
        self.assertEqual(self.roulette.bet_result(self.bet3, (1, 'RED')), 35)
        self.assertEqual(self.roulette.bet_result(self.bet4, (2, 'BLACK')), 11)

    def test_bet_results(self):
        self.roulette.winner = (2, 'BLACK')
        self.roulette.bets = {self.player: [self.bet1]}
        self.roulette.bet_results()
        self.assertEqual(self.roulette.rewards, {self.player:[40]})
    
    #test only running when state=reward
    #test player balance
    def test_reward_players(self):
        self.roulette.rewards = {self.player:[20, 50]}
        self.roulette.reward_players()
        self.assertEqual(self.player.balance, 100+20+50)

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(100, 'Kaido')
    
    def test_win(self):
        self.player.win(10)
        self.assertEqual(self.player.balance, 110)
    
    def test_deduct(self):
        self.player.deduct(10)
        self.assertEqual(self.player.balance, 90)


if __name__=='__main__':
    unittest.main()

