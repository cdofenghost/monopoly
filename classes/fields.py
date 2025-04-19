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
        self.popup_text: str
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
        self.popup_text: str = f"Вы должны заплатить налог государству размером ${randint(200, 1500)}."

class Jail(Field):
    def __init__(self):
        self.name: str = "Тюрьма"

    def on_stepping_in(self):
        self.popup_text: str = f"Вы отправляетесь в тюрьму за отмывание денег."


class PoliceDepartment(Field):
    def __init__(self):
        self.name: str = "Полицейский Участок"

    def on_stepping_in(self):
        self.popup_text: str = f"Вы посетили полицейский участок."


class Casino(Field):
    def __init__(self):
        self.name: str = "Казино"

    def on_stepping_in(self):
        self.popup_text: str = f"Вы зашли в поиграть в Казино.\nВы можете поставить $1000 на одну из сторон кубика и выиграть $6000."


class Start(Field):
    def __init__(self):
        self.name: str = "Старт"

    def on_stepping_in(self):
        self.popup_text: str = f'Вы попали на поле "Старт".'


class Chance(Field):
    def __init__(self):
        self.name: str = "Шанс"

    def on_stepping_in(self):
        self.popup_text: str = f'Вы попали на поле "Шанс".'


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
        self.popup_text: str = f'Вы попали на поле {self.name}.'


class Company(Property):
    def __init__(self, name: str, type: str, price: int, rent: int, rent_sheet: dict[int, int]):
        super().__init__(name, type, price, rent)

        self.rent_sheet = rent_sheet
        self.current_rent = rent_sheet[0]

    def on_stepping_in(self):
        self.popup_text: str = f'Вы попали на поле {self.name}.'

    def build_branch(self):
        pass


class CarBusiness(Property):
    def __init__(self, name: str, price: int, rent: int):
        super().__init__(name=name, price=price, rent=rent, type="Машины")


    def on_stepping_in(self):
        self.popup_text: str = f'Вы попали на поле {self.name}.'






