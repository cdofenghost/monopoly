from .player import Player
from random import randint
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QSizePolicy,
)

class GameManager():
    def __init__(self, game):
        self.game_session = game
        self.current_index: int = -1
        self.current_player: Player
        self.popup: OverlayWidget | None = None

    def start_game(self):
        self.next_turn()

    def next_turn(self):
        # Roll Dice
        self.current_index += 1
        self.current_player = self.game_session.player_list[self.current_index]

        self.show_button_popup(content_text=f"<span style='color: {self.current_player.color}'>{self.current_player.name}</span>, ваша очередь бросать кости!", 
                               button_text="Бросить кости", 
                               button_action=self.roll_dice)

    def log_message(self, message: str):
        self.game_session.chat.log_message(message)

    def roll_dice(self):
        dice1 = randint(1, 6)
        dice2 = randint(1, 6)

        self.log_message(f"<span style='color: {self.current_player.color}'>{self.current_player.name}</span> бросил кости - выпало {dice1} и {dice2} ({dice1 + dice2})!")

        self.destroy_popup()

        self.move_player(self.current_player.position + dice1 + dice2)
        return dice1 + dice2

    def move_player(self, pos):
        self.current_player.position = (pos % 40)
        field = self.game_session.fields[self.current_player.position]
        chip = self.game_session.chips[self.current_index]

        chip.setParent(field)
        chip.move(0, 0)
        chip.show()

    def on_stepping_in(self):
        field = self.game_session.main_map.map[self.current_player.position]
        field.on_stepping_in()
        pass


    def end_game(self):
        pass

    def file_bankruptcy(self):
        pass

    def show_button_popup(self, content_text: str, button_text: str, button_action):
        self.popup = OverlayWidget(content_text=content_text, 
                              button_text=button_text, 
                              button_action=button_action, 
                              parent=self.game_session)
        self.popup.show()

    def destroy_popup(self):
        if not self.popup is None:
            self.popup.deleteLater()
            self.game_session.update()

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