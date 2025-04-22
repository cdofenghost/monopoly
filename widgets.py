import sys
import socket

from PyQt6.QtGui import QIcon, QFont, QMouseEvent, QColor
from PyQt6.QtCore import QSize, Qt, QRect, pyqtSignal
from PyQt6.QtWidgets import (
    QSizePolicy,
    QSpacerItem,
    QApplication,
    QMainWindow,
    QStackedWidget,
    QDialog,
    QLabel,
    QLineEdit,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
    QComboBox,
    QPushButton,
    QStyle,
    QStyleFactory,
    QCheckBox,
    QMessageBox,
    QTextEdit,
    QColorDialog,
)

from .server import Host
from .client import Client
from .classes.player import Player
from .classes.fields import Field as FieldInGame, Company
from .classes.fields import Property
from .classes.map import Map
from .classes.manager import GameManager

class ViaLANChoice(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Доступные игры: ")
        self.button_host = QPushButton("Создать свою игру")
        self.button_connect = QPushButton("Присоединиться к существующей игре")
        self.button_host.clicked.connect(self.host_a_game)
        self.button_connect.clicked.connect(self.connect_to_a_game)

        self.container = QFormLayout()

        self.container.addRow(self.label)
        self.container.addRow(self.button_host)
        self.container.addRow(self.button_connect)

        self.setLayout(self.container)

    def host_a_game(self):
        host = Host("localhost", 8000)
        host.run()

    def connect_to_a_game(self):
        client = Client("localhost", 8000)
        client.connect()

class GameSetupFriends(QWidget):
    def __init__(self):
        super().__init__()

        self.player_amount_label = QLabel("Количество игроков: ")
        self.player_amount_combobox = QComboBox()

        for i in range(2, 8+1):
            self.player_amount_combobox.addItem(str(i))

        self.player_amount_combobox.setCurrentIndex(0)

        player_amount_layout = QHBoxLayout()
        player_amount_layout.addWidget(self.player_amount_label)
        player_amount_layout.addWidget(self.player_amount_combobox)

        self.container = QFormLayout()
        self.player_list = QFormLayout()

        self.start_button = QPushButton("Начать игру")

        self.container.addRow(player_amount_layout)
        self.container.addRow(self.player_list)
        self.container.addRow(self.start_button)

        self.setLayout(self.container)

    def update_player_list(self, n):
        self.container.removeRow(self.player_list)
        self.player_list = QFormLayout()

        for i in range(n+2):
            color_picker = ColorButton()
            label = QLabel(f"Игрок {i+1}: ")
            textbox = QLineEdit()
            textbox.setPlaceholderText("Имя игрока")
            layout = QHBoxLayout()
            layout.addWidget(color_picker)
            layout.addWidget(label)
            layout.addWidget(textbox)
            self.player_list.addRow(layout)

        self.container.insertRow(1, self.player_list)
            
class Menu(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Монополия")
        self.label.setStyleSheet("QLabel {text-align: center; font: bold 18px;}")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.games_button = QPushButton("Начать игру")
        self.games_button.clicked.connect(lambda: print("DEBUG MESSAGE: Start a Game"))

        self.quit_button = QPushButton("Выйти из игры")
        self.quit_button.clicked.connect(lambda: print("DEBUG MESSAGE: Quitting the game..."))

        menu_box = QVBoxLayout()
        menu_box.addWidget(self.label)
        menu_box.addWidget(self.games_button)
        menu_box.addWidget(self.quit_button)
        self.setLayout(menu_box)

class GamemodeSettings(QWidget):
    def __init__(self):
        super().__init__()

        # Labels
        self.gamemode_label = QLabel("Выбор игрового режима")
        self.gamemode_label.setStyleSheet("QLabel {text-align: center; font: bold 18px;}")
        self.gamemode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Buttons
        self.vialan_button = QPushButton("Играть по LAN")
        self.vialan_button.clicked.connect(lambda: print("DEBUG MESSAGE: Redirecting to page Awaiting Room"))

        self.withfriends_button = QPushButton("Играть с Друзьями")
        self.withfriends_button.clicked.connect(lambda: print("DEBUG MESSAGE: Redirecting to page Game Setup"))

        self.withbots_button = QPushButton("Играть с ботами")
        self.withbots_button.clicked.connect(lambda: print("DEBUG MESSAGE: Redirecting to page Game Setup"))

        self.tomenu_button = QPushButton("Back to Menu")
        self.tomenu_button.clicked.connect(lambda: print("DEBUG MESSAGE: Redirecting to page Menu"))
        
        # Layout
        gamemode_box = QVBoxLayout()
        gamemode_box.addWidget(self.gamemode_label)
        gamemode_box.addWidget(self.vialan_button)
        gamemode_box.addWidget(self.withfriends_button)
        gamemode_box.addWidget(self.withbots_button)
        gamemode_box.addWidget(self.tomenu_button)

        self.setLayout(gamemode_box)

class Game(QWidget):
    def __init__(self, player_list: list[Player]):
        super().__init__()
        self.player_list = player_list

        # Actual Game Items
        self.upper_road = QHBoxLayout()
        self.right_road = QVBoxLayout()
        self.left_road = QVBoxLayout()
        self.middle = QHBoxLayout()

        self.chat = Chat()
        self.chat.message_box.returnPressed.connect(self.chat.send_message)

        self.middle.addItem(self.left_road)
        self.middle.addWidget(self.chat)
        self.middle.addItem(self.right_road)

        self.lower_road = QHBoxLayout()
        self.main_map = Map()
        self.main_map.load_map()
        self.fields: list[Field] = []

        for field in self.main_map.map[:11]: 
            widget = Field(field, self)
            self.upper_road.addWidget(widget)
            self.fields.append(widget)

        for field in self.main_map.map[11:20]: 
            widget = Field(field, self, form_direction='right')
            self.right_road.addWidget(widget)
            self.fields.append(widget)

        for field in self.main_map.map[30:19:-1]: 
            widget = Field(field, self, form_direction='down')
            self.lower_road.addWidget(widget)
            self.fields.append(widget)

        for field in self.main_map.map[40:30:-1]: 
            widget = Field(field, self, form_direction='left')
            self.left_road.addWidget(widget)
            self.fields.append(widget)

        self.chips = []
        self.create_player_chips()

        game_box = QFormLayout()

        game_box.addRow(self.upper_road)
        game_box.addRow(self.middle)
        game_box.addRow(self.lower_road)
        game_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Stats and other Items
        self.players_stats = PlayersBox(player_list=player_list)
        self.quit_button = QPushButton("Покинуть игру")
        self.quit_button.setStyleSheet("background-color: #AA0000; border-radius: 4px; color: #F3F3F3;")

        players_box = QVBoxLayout()
        players_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        players_box.addWidget(self.players_stats)
        players_box.addWidget(self.quit_button)

        layout = QHBoxLayout()

        layout.addItem(QSpacerItem(20, 40, hPolicy=QSizePolicy.Policy.Expanding, vPolicy=QSizePolicy.Policy.Expanding))
        layout.addItem(players_box)
        layout.addItem(game_box)
        layout.addItem(QSpacerItem(20, 40, hPolicy=QSizePolicy.Policy.Expanding, vPolicy=QSizePolicy.Policy.Expanding))

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        # Game Interaction Manager
        self.game_manager = GameManager(self)
        self.game_manager.start_game()

    def create_player_chips(self):
        start_field = self.fields[0]
        field_height = start_field.height()
        field_width = start_field.width()

        player_amount = len(self.player_list)
        count = 0

        for player in self.player_list:
            chip = QWidget(start_field)
            chip_width = int(field_width / (player_amount * 2))
            chip_height = int(field_height / (player_amount * 2))
            chip.setFixedSize(chip_width, chip_height)

            chip.setStyleSheet(f'background-color: {player.color}; border: 2px solid black; border-radius: 4px;')
            chip.move(count * chip_width, 0)

            self.chips.append(chip)
            count += 1


class Chat(QWidget):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(400,400)
        self.setMaximumSize(Field.FIELD_MAX_SIZE[0]*9, 1200)

        self.chat_log = QTextEdit()
        self.chat_log.setReadOnly(True)
        self.chat_log.setStyleSheet("background-color: #F3F3F3; border-radius: 10px;")
        self.message_box = QLineEdit()
        self.message_box.setStyleSheet("background-color: #F3F3F3; border-radius: 4px;")
        self.message_box.setPlaceholderText("Напишите гадости соперникам!")

        layout = QVBoxLayout()
        layout.addWidget(self.chat_log)
        layout.addWidget(self.message_box)

        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

    def send_message(self):
        message = self.message_box.text()

        if message == "/clear":
            self.message_box.setText("")
            self.chat_log.setText("")
            return
        
        self.chat_log.setText(self.chat_log.toHtml() + f"\nИгрок: {message}")
        self.message_box.setText("")

    def log_message(self, message: str):
        self.chat_log.setText(self.chat_log.toHtml() + f"\n{message}")


class Field(QWidget):

    # Attributes
    FIELD_MIN_SIZE = (60, 60)
    FIELD_MAX_SIZE = (100, 120)

    def __init__(self, field: FieldInGame, game: Game, form_direction: str = 'up'):
        # Widget settings
        super().__init__()
        self.setStyleSheet('background-color: #F3F3F3')

        self.field_layout = QFormLayout()
        self.field_layout.setContentsMargins(0, 0, 0, 0)
        self.field_layout.setSpacing(0)
        self.game = game

        self.rent_tag = QWidget()
        self.button = QPushButton(field.name)
        self.button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.button.clicked.connect(lambda: self.show_field_info_popup(field, game.game_manager.current_player))

        if isinstance(field, Property):
            rent_layout = QVBoxLayout()
            rent_layout.setContentsMargins(0, 0, 0, 0)
            rent_layout.setSpacing(0)

            self.rent_label = QLabel(f"${str(field.price)}")
            self.rent_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.rent_label.setStyleSheet('color: white;')

            if form_direction in ['left', 'right']:
                self.rent_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            else:
                self.rent_tag.setMaximumHeight(12)

            rent_layout.addWidget(self.rent_label)

            self.rent_tag.setStyleSheet(f"background-color: {field.type_color}; font-weight: 500")
            self.rent_tag.setLayout(rent_layout)
            self.rent_tag.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        if form_direction == 'up':
            self.field_layout.addRow(self.rent_tag)
            self.field_layout.addRow(self.button)

        if form_direction == 'down':
            self.field_layout.addRow(self.button)
            self.field_layout.addRow(self.rent_tag)

        if form_direction == 'left':
            box = QHBoxLayout()
            box.setContentsMargins(0, 0, 0, 0)
            box.setSpacing(0)

            box.addWidget(self.rent_tag)
            box.addWidget(self.button)

            self.field_layout.addRow(box)

        if form_direction == 'right':
            box = QHBoxLayout()
            box.setContentsMargins(0, 0, 0, 0)
            box.setSpacing(0)

            box.addWidget(self.button)
            box.addWidget(self.rent_tag)

            self.field_layout.addRow(box)

        self.setMinimumSize(*Field.FIELD_MIN_SIZE)  
        self.setMaximumSize(*Field.FIELD_MAX_SIZE)  
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setLayout(self.field_layout)

    def show_field_info_popup(self, field: FieldInGame, player: Player):
        if isinstance(field, Property):
            if isinstance(field, Company):
                content_text = f"Поле: {field.name}<br>Тип: <span style='color: {field.type_color}'>{field.type}</span><br>Цена покупки: {field.price}<br>Базовая рента: {field.rent}<br>Рента филиалов: {field.rent_sheet}<br>Цена залога: ${field.pledge_price}<br>Цена выкупа: ${field.from_pledge_price}"

                if field in player.owned_fields:
                    if not field.pledged:
                        self.popup = OverlayWidget2B(content_text=content_text,
                                                    button_action1=self.hide_popup,
                                                    button_text1='Закрыть',
                                                    button_action2=lambda: self.pledge_field(field, player),
                                                    button_text2="Заложить",
                                                    parent=self.game)
                        self.popup.show()
                    else:
                        self.popup = OverlayWidget2B(content_text=content_text,
                            button_action1=self.hide_popup,
                            button_text1='Закрыть',
                            button_action2=lambda: self.pledge_field(field, player),
                            button_text2="Выкупить",
                            button2_enabled=player.money >= field.from_pledge_price,
                            parent=self.game)
                        self.popup.show()
                else:
                    self.popup = OverlayWidget(content_text=content_text, 
                                        button_text="Закрыть", 
                                        button_action=self.hide_popup, 
                                        parent=self.game)
                    self.popup.show()

    def hide_popup(self):
        if not self.popup is None:
            self.popup.hide()
            self.popup.setParent(None)
            self.popup.deleteLater()
            QApplication.processEvents() 

    def pledge_field(self, field: Property, player: Player):
        field.pledge_field()
        self.button.setStyleSheet(f'background-color: #AAAAAA')
        self.game.chat.log_message(f"<span style='{player.color}'>{player.name}</span> заложил поле <span style='color: {field.type_color}'>{field.name}</span>")
        self.game.players_stats.update_box()
        self.hide_popup()

class PlayersBox(QWidget):
    def __init__(self, player_list: list[Player]):
        super().__init__()
        self.player_list = player_list

        layout = QFormLayout()
        for player in player_list:
            container = QHBoxLayout()
            color_flag = QWidget()
            color_flag.setFixedSize(32, 32)
            color_flag.setStyleSheet(f"background-color: {player.color}; border-radius: 4px; border: 2px solid white;")

            label = QLabel(f"{player.name}: ${player.money}")
            label.setStyleSheet('color: #F3F3F3;')
            container.addWidget(color_flag)
            container.addWidget(label)
            layout.addRow(container)

        self.setLayout(layout)

    def remove_player(self, player_index: int):
        line = self.layout().itemAt(player_index).layout()
        self.layout().removeItem(line)

    def update_box(self):
        for i in range(self.layout().count()):
            line = self.layout().itemAt(i).layout()
            player = line.itemAt(1).widget()
            player.setText(f"{self.player_list[i].name}: ${self.player_list[i].money}")

class ColorButton(QPushButton):
    '''
    Custom Qt Widget to show a chosen color.

    Left-clicking the button shows the color-chooser, while
    right-clicking resets the color to None (no-color).
    '''

    colorChanged = pyqtSignal(object)

    def __init__(self, *args, color=None, **kwargs):
        super().__init__(*args, **kwargs)

        self._color = None
        self._default = color
        self.pressed.connect(self.onColorPicker)

        # Set the initial/default state.
        self.setColor(self._default)

    def setColor(self, color):
        if color != self._color:
            self._color = color
            self.colorChanged.emit(color)

        if self._color:
            self.setStyleSheet("background-color: %s;" % self._color)
        else:
            self.setStyleSheet("")

    def color(self):
        return self._color

    def onColorPicker(self):
        '''
        Show color-picker dialog to select color.

        Qt will use the native dialog by default.

        '''
        dlg = QColorDialog()
        if self._color:
            dlg.setCurrentColor(QColor(self._color))

        if dlg.exec():
            self.setColor(dlg.currentColor().name())

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.RightButton:
            self.setColor(self._default)

        return super().mousePressEvent(e)
    
class OverlayWidget(QWidget):
    def __init__(self, content_text: str, button_text: str, button_action, parent=None):
        super().__init__(parent)

        self.button_text = button_text
        self.button_action = button_action
        self.content_text = content_text
        self.setup_ui()
        
    def setup_ui(self):
        # Убираем рамку и делаем фон полупрозрачным
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Создаем контент оверлея
        self.label = QLabel(self.content_text, self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("""
            background-color: rgba(0, 0, 0, 180);
            color: white;
            border-radius: 10px;
            padding: 20px;
            font-size: 16px;
        """)
        self.button = QPushButton(self.button_text)
        self.button.setStyleSheet('background-color: #35B797; color: #F3F3F3; font-weight: 500;')
        self.button.clicked.connect(self.button_action)
        
        self.setFixedSize(240, 240)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)
        
        # Позиционируем относительно родителя
        self.update_position()
        
    def update_position(self):
        if self.parent():
            # Центрируем относительно родителя
            self.move(self.parent().rect().center())

class OverlayWidget2B(QWidget):
    def __init__(self, content_text: str, button_text1: str, button_text2: str, button_action1, button_action2, button1_enabled=True, button2_enabled=True, parent=None):
        super().__init__(parent)

        self.button_text1 = button_text1
        self.button_action1 = button_action1
        self.button_text2 = button_text2
        self.button_action2 = button_action2
        self.content_text = content_text
        self.button1_enabled = button1_enabled
        self.button2_enabled = button2_enabled
        self.setup_ui()
        
    def setup_ui(self):
        BUTTON_COLORS = {
            True: "#35B797",
            False: "#258772",
        }
        # Убираем рамку и делаем фон полупрозрачным
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Создаем контент оверлея
        self.label = QLabel(self.content_text, self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("""
            background-color: rgba(0, 0, 0, 180);
            color: white;
            border-radius: 10px;
            padding: 20px;
            font-size: 16px;
        """)
        button_layout = QHBoxLayout()


        self.button1 = QPushButton(self.button_text1)
        self.button1.setStyleSheet(f'background-color: {BUTTON_COLORS[self.button1_enabled]}; color: #F3F3F3; font-weight: 500;')
        self.button1.clicked.connect(self.button_action1)
        self.button1.setEnabled(self.button1_enabled)

        self.button2 = QPushButton(self.button_text2)
        self.button2.setStyleSheet(f'background-color: {BUTTON_COLORS[self.button2_enabled]}; color: #F3F3F3; font-weight: 500;')
        self.button2.clicked.connect(self.button_action2)
        self.button2.setEnabled(self.button2_enabled)
        
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)

        self.setFixedSize(240, 240)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addItem(button_layout)
        self.setLayout(layout)
        
        # Позиционируем относительно родителя
        self.update_position()
        
    def update_position(self):
        if self.parent():
            # Центрируем относительно родителя
            self.move(self.parent().rect().center())