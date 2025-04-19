from abc import abstractmethod
from .player import Player

PROPERTY_TYPE_COLORS = {
    'Парфюмерия': '#F678CA',
    'Машины': '#D02A4C',
    'Одежда': '#CCA21C',
    'Социальные сети': '#32DD9C',
    'Игры': '#680C05',
    'Напитки': '#4F95ED',
    'Авиакомпании': '#9CD559',
    'Фастфуд': '#55D6F6',
    'Отели': '#9171E2',
    'Смартфоны': '#646D73',
}
class Field():
    def __init__(self):
        self.name: str
        pass

    @abstractmethod
    def on_stepping_in(self):
        '''
        Description of a method.
        '''
        pass

class Taxes(Field):
    def __init__(self):
        self.name: str = "Налоги"

    def on_stepping_in(self):
        from random import randint

        print(f"DEBUG: You have to pay ${randint(200, 1500)} taxes.")


class Jail(Field):
    def __init__(self):
        self.name: str = "Тюрьма"

    def on_stepping_in(self):
        print(f"DEBUG: You have to go to Jail.")


class PoliceDepartment(Field):
    def __init__(self):
        self.name: str = "Полицейский Участок"

    def on_stepping_in(self):
        print(f"DEBUG: You visited the Police Department.")


class Casino(Field):
    def __init__(self):
        self.name: str = "Казино"

    def on_stepping_in(self):
        print(f"DEBUG: You went to Casino to gamble!!")


class Start(Field):
    def __init__(self):
        self.name: str = "Старт"

    def on_stepping_in(self):
        print(f"DEBUG: You went back to Start.")


class Chance(Field):
    def __init__(self):
        self.name: str = "Шанс"

    def on_stepping_in(self):
        print(f"DEBUG: You stepped on a field 'Chance'.")


class Property(Field):
    def __init__(self, name: str, type: str, price: int, rent: int):
        self.name = name
        self.type = type
        self.type_color = PROPERTY_TYPE_COLORS[type]
        self.price = price
        self.rent = rent

        self.owner: Player | None = None

    def buy_field(self):
        pass

    def auction_field(self):
        pass

    def pledge_field(self):
        pass


class GameBusiness(Property):
    def __init__(self, name: str, type: str, price: int, rent: int, multiplier: float):
        super().__init__(name=name, price=price, rent=rent, type="Игры")
        self.multiplier = multiplier

    def on_stepping_in(self):
        print(f"DEBUG: Do you want to buy Game Business?")


class Company(Property):
    def __init__(self, name: str, type: str, price: int, rent: int, rent_sheet: dict[int, int]):
        super().__init__(name, type, price, rent)

        self.rent_sheet = rent_sheet
        self.current_rent = rent_sheet[0]

    def on_stepping_in(self):
        print(f"DEBUG: Do you want to buy Company?")

    def build_branch(self):
        pass


class CarBusiness(Property):
    def __init__(self, name: str, price: int, rent: int):
        super().__init__(name=name, price=price, rent=rent, type="Машины")


    def on_stepping_in(self):
        print(f"DEBUG: Do you want to buy Game Business?")






