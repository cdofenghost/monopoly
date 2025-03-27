from abc import abstractmethod
from .player import Player

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
        self.name: str = "Taxes"

    def on_stepping_in(self):
        from random import randint

        print(f"DEBUG: You have to pay ${randint(200, 1500)} taxes.")


class Jail(Field):
    def __init__(self):
        self.name: str = "Jail"

    def on_stepping_in(self):
        print(f"DEBUG: You have to go to Jail.")


class PoliceDepartment(Field):
    def __init__(self):
        self.name: str = "Police Department"

    def on_stepping_in(self):
        print(f"DEBUG: You visited the Police Department.")


class Casino(Field):
    def __init__(self):
        self.name: str = "Casino"

    def on_stepping_in(self):
        print(f"DEBUG: You went to Casino to gamble!!")


class Start(Field):
    def __init__(self):
        self.name: str = "Start"

    def on_stepping_in(self):
        print(f"DEBUG: You went back to Start.")


class Chance(Field):
    def __init__(self):
        self.name: str = "Chance"

    def on_stepping_in(self):
        print(f"DEBUG: You stepped on a field 'Chance'.")


class Property(Field):
    def __init__(self):
        self.name: str
        self.__payment: int
        self.owner: Player | None

    def buy_field(self):
        pass

    def auction_field(self):
        pass

    def pledge_field(self):
        pass

    def get_payment(self) -> int:
        return self.__payment
    
    def set_payment(self, new_payment: int):
        self.__payment = new_payment


class GameBusiness(Property):
    def __init__(self):
        self.name: str = "Game Business"
        self.__payment: int

    def on_stepping_in(self):
        print(f"DEBUG: Do you want to buy Game Business?")


class Company(Property):
    def __init__(self, name: str, type):
        self.name: str = "Company"
        self.__payment: int

    def on_stepping_in(self):
        print(f"DEBUG: Do you want to buy Company?")

    def build_branch(self):
        pass


class CarBusiness(Property):
    def __init__(self):
        self.name: str = "Car Business"
        self.__payment: int

    def on_stepping_in(self):
        print(f"DEBUG: Do you want to buy Game Business?")






