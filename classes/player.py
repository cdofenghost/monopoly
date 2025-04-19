from typing import Self

class Player():
    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color
        self.money = 15000
        self.owned_fields: list
        self.pledged_fields: list
        self.position = 0
        self.in_jail: bool = False

    def offer(self, player: Self):
        pass