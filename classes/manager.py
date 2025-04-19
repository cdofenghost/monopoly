from .player import Player
from random import randint
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

class GameManager():
    def __init__(self, game):
        self.game_session = game

    def start_game(self):
        self.next_turn()
        popup = self.show_button_popup(content_text="Hello", button_text="Click", button_action=lambda: print("boop"))
        popup.show()

    def next_turn(self):
        pass

    def roll_dice(self):
        dice1 = randint(1, 6)
        dice2 = randint(1, 6)

        return dice1 + dice2

    def end_game(self):
        pass

    def file_bankruptcy(self):
        pass

    def show_button_popup(self, content_text: str, button_text: str, button_action):
        popup = OverlayWidget(content_text="Оверлей", button_text="Ок", button_action=lambda: print("boop"), parent=self.game_session)

        return popup

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
        self.label.setStyleSheet("""
            background-color: rgba(0, 0, 0, 180);
            color: white;
            border-radius: 10px;
            padding: 20px;
            font-size: 16px;
        """)
        self.button = QPushButton(self.button_text)
        self.button.setStyleSheet('background-color: #35B797; color: #F3F3F3;')
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