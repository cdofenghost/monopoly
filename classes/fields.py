from abc import abstractmethod
from .player import Player

from random import randint

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
    def on_stepping_in(self, manager):
        '''
        Description of a method.
        '''
        pass

class Taxes(Field):
    def __init__(self):
        self.name: str = "Налоги"

    def on_stepping_in(self, manager):
        from random import randint
        self.tax_price = randint(200, 1500)
        self.popup_text: str = f"Вы должны заплатить налог государству размером ${self.tax_price}."

        manager.show_popup_2b(content_text=self.popup_text,
                              button_text1="Оплатить налог",
                              button_text2="Обанкротиться",
                              button_action1=lambda: self.pay_taxes(manager),
                              button_action2=lambda: self.file_for_bankruptcy(manager))
        
    def pay_taxes(self, manager):
        manager.current_player.money -= self.tax_price
        manager.log_message(f"<span style='color: {manager.current_player.color}'>{manager.current_player.name}</span> оплатил налог размером ${self.tax_price}")
        manager.next_turn()
        manager.game_session.players_stats.update_box()

    def file_for_bankruptcy(self, manager):
        manager.file_bankruptcy(manager.current_player)
        manager.log_message(f"<span style='color: {manager.current_player.color}'>{manager.current_player.name}</span> стал банкротом.")
        manager.next_turn()
        manager.game_session.players_stats.update_box()

class Jail(Field):
    def __init__(self):
        self.name: str = "Тюрьма"

    def on_stepping_in(self, manager):
        self.popup_text: str = f"Вы отправляетесь в тюрьму за отмывание денег."

        manager.show_popup(content_text=self.popup_text,
                           button_text="В тюрьму",
                           button_action=lambda: self.move_player(manager))

    def move_player(self, manager):
        
        manager.log_message(f"<span style='color: {manager.current_player.color}'>{manager.current_player.name}</span> отправляется в тюрьму за отмывание денег.")
        manager.current_player.in_jail = True
        manager.move_player(10, on_step=False)
        manager.next_turn()
        manager.game_session.players_stats.update_box()


class PoliceDepartment(Field):
    def __init__(self):
        self.name: str = "Полицейский Участок"

    def on_stepping_in(self, manager):
        if manager.current_player.in_jail is False:
            self.popup_text: str = f"Вы посетили полицейский участок."
            manager.show_popup(content_text=self.popup_text,
                            button_text="ОК",
                            button_action=lambda: self.next_turn(manager))

    def next_turn(self, manager):
        manager.log_message(f"<span style='color: {manager.current_player.color}'>{manager.current_player.name}</span> посещает полицейский участок с экскурсией.")
        manager.next_turn()
        manager.game_session.players_stats.update_box()

class Casino(Field):
    def __init__(self):
        self.name: str = "Казино"

    def on_stepping_in(self, manager):
        self.popup_text: str = f"Вы зашли в поиграть в Казино.\nВы можете поставить $1000 на одну из сторон кубика и выиграть $6000."
        manager.show_popup(content_text=self.popup_text,
                           button_text="ОК",
                           button_action=lambda: self.next_turn(manager))

    def next_turn(self, manager):
        manager.next_turn()
        manager.game_session.players_stats.update_box()

class Start(Field):
    def __init__(self):
        self.name: str = "Старт"

    def on_stepping_in(self, manager):
        self.popup_text: str = f'Вы попали на поле "Старт".'
        manager.show_popup(content_text=self.popup_text,
                           button_text="ОК",
                           button_action=lambda: self.add_1000_bucks(manager))

    def add_1000_bucks(self, manager):
        manager.log_message(f"<span style='color: {manager.current_player.color}'>{manager.current_player.name}</span> зашел на поле 'Старт' и получил дополнительные $1000.")
        manager.current_player.money += 1000
        manager.next_turn()
        manager.game_session.players_stats.update_box()


class Chance(Field):
    def __init__(self):
        self.name: str = "Шанс"
        self.chance_texts = {
            1: "отправляется в путешествие",
            2: "потратил $500 на распродаже",
            3: "нашел на улице $500",
            4: "забыл выключить утюг дома. В следующем ходу он будет перемещаться в обратном направлении",
        }
        self.chance_actions = {
            1: self.chance1,
            2: self.chance2,
            3: self.chance3,
            4: self.chance4,
        }

    def on_stepping_in(self, manager):
        self.popup_text: str = f'Вы попали на поле "Шанс".'
        manager.show_popup(content_text=self.popup_text,
                           button_text="ОК",
                           button_action=lambda: self.game_action(manager))

    def game_action(self, manager):
        chance_number = randint(1, 4)

        self.chance_actions[chance_number](manager)

        manager.log_message(f"<span style='color: {manager.current_player.color}'>{manager.current_player.name}</span> {self.chance_texts[chance_number]}")
        manager.next_turn()
        manager.game_session.players_stats.update_box()

    def chance1(self, manager):
        manager.move_player(manager.current_player.position + randint(-12, 12), on_step=False)

    def chance2(self, manager):
        manager.current_player.money -= 500

    def chance3(self, manager):
        manager.current_player.money += 500

    def chance4(self, manager):
        pass

class Property(Field):
    def __init__(self, name: str, type: str, price: int, rent: int):
        self.name = name
        self.type = type
        self.type_color = PROPERTY_TYPE_COLORS[type]

        self.price = price
        self.rent = rent

        # Pledge attributes
        self.pledge_price = price // 2
        self.from_pledge_price = self.pledge_price * 1.2
        self.pledged = False

        self.owner: Player | None = None

    def buy_field(self, player: Player):
        player.money -= self.price
        self.owner = player
        player.owned_fields.append(self)


    def auction_field(self):
        pass

    def pledge_field(self):
        self.pledged = True
        self.owner.money += self.pledge_price


class GameBusiness(Property):
    def __init__(self, name: str, type: str, price: int, rent: int, multiplier: float):
        super().__init__(name=name, price=price, rent=rent, type="Игры")
        self.multiplier = multiplier

    def on_stepping_in(self, manager):
        if self.owner is None:
            buy_button_enabled = manager.current_player.money >= self.price
            self.popup_text: str = f'Вы попали на поле {self.name}.'
            manager.show_popup_2b(content_text=self.popup_text,
                                button_text1="Купить",
                                button_text2="Отменить",
                                button1_enabled=buy_button_enabled,
                                button_action1=lambda: self.buying_action(manager),
                                button_action2=lambda: self.next_turn(manager))
        else:
            if not self.owner is manager.current_player:
                buy_button_enabled = manager.current_player.money >= self.rent
                self.popup_text: str = f'Вы попали на поле {self.name}, которым владеет <span style="color: {self.owner.color}">{self.owner.name}</span>.\nВы обязаны заплатить владельцу ${self.rent}.'
                manager.show_popup_2b(content_text=self.popup_text,
                                    button_text1="Заплатить",
                                    button_text2="Обанкротиться",
                                    button1_enabled=buy_button_enabled,
                                    button_action1=lambda: self.pay_rent(manager),
                                    button_action2=lambda: self.file_for_bankruptcy(manager))
            else:
                manager.log_message(f'<span style="color: {self.owner.color}">{self.owner.name}</span> попадает на свое поле')
                manager.next_turn()

    def pay_rent(self, manager):
        manager.current_player.money -= self.rent
        self.owner.money += self.rent
        manager.next_turn()
        manager.game_session.players_stats.update_box()

    def file_for_bankruptcy(self, manager):
        manager.file_bankruptcy(manager.current_player)
        manager.log_message(f"<span style='color: {manager.current_player.color}'>{manager.current_player.name}</span> стал банкротом.")
        manager.next_turn()
        manager.game_session.players_stats.update_box()

    def buying_action(self, manager):
        self.buy_field(manager.current_player)
        manager.log_message(f"<span style='color: {manager.current_player.color}'>{manager.current_player.name}</span> купил компанию {self.name} за ${self.price}.")

        index = manager.current_player.position

        if index in range(20, 31):
            index = 30 - (index - 20)
        elif index in range(31, 40):
            index = 39 - (index - 31)

        field = manager.game_session.fields[index]
        field.button.setStyleSheet(f"background-color: {manager.current_player.color}")
        field.rent_label.setText(f"${self.rent}")
        manager.next_turn()
        manager.game_session.players_stats.update_box()

    def next_turn(self, manager):
        manager.next_turn()
        manager.game_session.players_stats.update_box()

class Company(Property):
    def __init__(self, name: str, type: str, price: int, rent: int, rent_sheet: dict[int, int]):
        super().__init__(name, type, price, rent)

        self.rent_sheet = rent_sheet
        self.current_rent = rent_sheet[1]

    def on_stepping_in(self, manager):
        if self.owner is None:
            buy_button_enabled = manager.current_player.money >= self.price
            self.popup_text: str = f'Вы попали на поле {self.name}.'
            manager.show_popup_2b(content_text=self.popup_text,
                                button_text1="Купить",
                                button_text2="Отменить",
                                button1_enabled=buy_button_enabled,
                                button_action1=lambda: self.buying_action(manager),
                                button_action2=lambda: self.next_turn(manager))
        else:
            if not self.owner is manager.current_player:
                buy_button_enabled = manager.current_player.money >= self.rent
                self.popup_text: str = f'Вы попали на поле <span style="color: {self.type_color}">{self.name}</span>, которым владеет <span style="color: {self.owner.color}">{self.owner.name}</span>.\nВы обязаны заплатить владельцу ${self.rent}.'
                manager.show_popup_2b(content_text=self.popup_text,
                                    button_text1="Заплатить",
                                    button_text2="Обанкротиться",
                                    button1_enabled=buy_button_enabled,
                                    button_action1=lambda: self.pay_rent(manager),
                                    button_action2=lambda: self.file_for_bankruptcy(manager))
            else:
                manager.log_message(f'<span style="color: {self.owner.color}">{self.owner.name}</span> попадает на свое поле')
                manager.next_turn()

    def build_branch(self):
        pass

    def pay_rent(self, manager):
        manager.current_player.money -= self.rent
        self.owner.money += self.rent
        manager.next_turn()
        manager.game_session.players_stats.update_box()

    def file_for_bankruptcy(self, manager):
        manager.file_bankruptcy(manager.current_player)
        manager.log_message(f"<span style='color: {manager.current_player.color}'>{manager.current_player.name}</span> стал банкротом.")
        manager.next_turn()
        manager.game_session.players_stats.update_box()

    def buying_action(self, manager):
        self.buy_field(manager.current_player)
        manager.log_message(f"<span style='color: {manager.current_player.color}'>{manager.current_player.name}</span> купил компанию <span style='color: {self.type_color}'>{self.name}</span> за ${self.price}.")

        index = manager.current_player.position

        if index in range(20, 31):
            index = 30 - (index - 20)
        elif index in range(31, 40):
            index = 39 - (index - 31)

        field = manager.game_session.fields[index]
        field.button.setStyleSheet(f"background-color: {manager.current_player.color}")
        field.rent_label.setText(f"${self.rent}")
        manager.next_turn()
        manager.game_session.players_stats.update_box()
        

    def next_turn(self, manager):
        manager.next_turn()
        manager.game_session.players_stats.update_box()


class CarBusiness(Property):
    def __init__(self, name: str, price: int, rent: int):
        super().__init__(name=name, price=price, rent=rent, type="Машины")


    def on_stepping_in(self, manager):
        if self.owner is None:
            buy_button_enabled = manager.current_player.money >= self.price
            self.popup_text: str = f'Вы попали на поле {self.name}.'
            manager.show_popup_2b(content_text=self.popup_text,
                                button_text1="Купить",
                                button_text2="Отменить",
                                button1_enabled=buy_button_enabled,
                                button_action1=lambda: self.buying_action(manager),
                                button_action2=lambda: self.next_turn(manager))
        else:
            if not self.owner is manager.current_player:
                buy_button_enabled = manager.current_player.money >= self.rent
                self.popup_text: str = f'Вы попали на поле <span style="color: {self.type_color}">{self.name}</span>, которым владеет <span style="color: {self.owner.color}">{self.owner.name}</span>.\nВы обязаны заплатить владельцу ${self.rent}.'
                manager.show_popup_2b(content_text=self.popup_text,
                                    button_text1="Заплатить",
                                    button_text2="Обанкротиться",
                                    button1_enabled=buy_button_enabled,
                                    button_action1=lambda: self.pay_rent(manager),
                                    button_action2=lambda: self.file_for_bankruptcy(manager))
            else:
                manager.log_message(f'<span style="color: {self.owner.color}">{self.owner.name}</span> попадает на свое поле')
                manager.next_turn()
                
    def pay_rent(self, manager):
        manager.current_player.money -= self.rent
        self.owner.money += self.rent
        manager.next_turn()
        manager.game_session.players_stats.update_box()

    def file_for_bankruptcy(self, manager):
        manager.file_bankruptcy(manager.current_player)
        manager.log_message(f"<span style='color: {manager.current_player.color}'>{manager.current_player.name}</span> стал банкротом.")
        manager.next_turn()
        manager.game_session.players_stats.update_box()

    def buying_action(self, manager):
        self.buy_field(manager.current_player)
        manager.log_message(f"<span style='color: {manager.current_player.color}'>{manager.current_player.name}</span> купил компанию <span style='color: {self.type_color}'>{self.name}</span> за ${self.price}.")

        index = manager.current_player.position

        if index in range(20, 31):
            index = 30 - (index - 20)
        elif index in range(31, 40):
            index = 39 - (index - 31)

        field = manager.game_session.fields[index]
        field.button.setStyleSheet(f"background-color: {manager.current_player.color}")
        field.rent_label.setText(f"${self.rent}")
        manager.next_turn()
        manager.game_session.players_stats.update_box()

    def next_turn(self, manager):
        manager.next_turn()
        manager.game_session.players_stats.update_box()





