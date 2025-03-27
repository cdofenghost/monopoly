from .player import Player

class GameManager():
    def __init__(self):
        self.players_list: list[Player]
        pass

    @classmethod
    def start_game(self, players_list: list[Player]):
        pass

    @classmethod
    def end_game(self):
        pass

    @classmethod
    def file_bankruptcy(self, player: Player):
        pass