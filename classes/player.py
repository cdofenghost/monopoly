from typing import Self

class Player():
    def __init__(self, name):
        self.name: str = name
        self.color: str
        self.__money: int
        self.owned_fields: list
        self.pledged_fields: list

    def offer(self, player: Self):
        pass

    def set_money(self, new_money: int):
        self.__money = new_money

    def get_money(self) -> int:
        return self.__money