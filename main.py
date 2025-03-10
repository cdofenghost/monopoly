import sys

from PyQt6.QtGui import QIcon, QFont, QMouseEvent
from PyQt6.QtCore import QSize, Qt, QRect
from PyQt6.QtWidgets import (
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
)

class GameSetupFriends(QWidget):
    def __init__(self):
        super().__init__()

        self.player_amount_label = QLabel("Number of players: ")
        self.player_amount_combobox = QComboBox()

        for i in range(2, 8+1):
            self.player_amount_combobox.addItem(str(i))

        self.player_amount_combobox.setCurrentIndex(0)

        player_amount_layout = QHBoxLayout()
        player_amount_layout.addWidget(self.player_amount_label)
        player_amount_layout.addWidget(self.player_amount_combobox)

        self.container = QFormLayout()
        self.player_list = QFormLayout()

        self.start_button = QPushButton("Start a game")

        self.container.addRow(player_amount_layout)
        self.container.addRow(self.player_list)
        self.container.addRow(self.start_button)

        self.setLayout(self.container)

    def update_player_list(self, n):
        self.container.removeRow(self.player_list)
        self.player_list = QFormLayout()

        for i in range(n+2):
            label = QLabel(f"Player {i+1}: ")
            textbox = QLineEdit()
            layout = QHBoxLayout()
            layout.addWidget(label)
            layout.addWidget(textbox)
            self.player_list.addRow(layout)

        self.container.insertRow(1, self.player_list)
            
class Menu(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Monopoly")
        self.label.setStyleSheet("QLabel {color: #000000; text-align: center; font: bold 18px;}")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.games_button = QPushButton("Start a Game")
        self.games_button.clicked.connect(lambda: print("DEBUG MESSAGE: Start a Game"))

        self.quit_button = QPushButton("Quit")
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
        self.gamemode_label = QLabel("Gamemode Choice")
        self.gamemode_label.setStyleSheet("QLabel {color: #000000; text-align: center; font: bold 18px;}")
        self.gamemode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Buttons
        self.vialan_button = QPushButton("Play via LAN")
        self.vialan_button.clicked.connect(lambda: print("DEBUG MESSAGE: Redirecting to page Awaiting Room"))

        self.withfriends_button = QPushButton("Play with Friends")
        self.withfriends_button.clicked.connect(lambda: print("DEBUG MESSAGE: Redirecting to page Game Setup"))

        self.withbots_button = QPushButton("Play with Bots")
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

    def __init__(self):
        super().__init__()

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
        
        for i in range(11): self.upper_road.addWidget(Field("Field"))
        for i in range(9): self.right_road.addWidget(Field("Field"))
        for i in range(11): self.lower_road.addWidget(Field("Field"))
        for i in range(9): self.left_road.addWidget(Field("Field"))

        game_box = QFormLayout()
        players_box = QHBoxLayout()
        players_box = PlayersBox(4)

        layout = QHBoxLayout()

        game_box.addRow(self.upper_road)
        game_box.addRow(self.middle)
        game_box.addRow(self.lower_road)
        
        layout.addWidget(players_box)
        layout.addItem(game_box)
        self.setLayout(layout)

class Chat(QWidget):
    def __init__(self):
        super().__init__()

        self.sizeHint = (None, None)
        self.width = 200
        self.height = 200
        self.setMinimumSize(200, 200)

        self.chat_log = QTextEdit()
        self.chat_log.setReadOnly(True)
        self.message_box = QLineEdit()
        self.message_box.placeholderText = "Напишите гадости соперникам!"

        layout = QVBoxLayout()
        layout.addWidget(self.chat_log)
        layout.addWidget(self.message_box)

        self.setLayout(layout)

    def send_message(self):
        message = self.message_box.text()

        if message == "/clear":
            self.message_box.setText("")
            self.chat_log.setText("")
            return
        
        self.chat_log.setText(self.chat_log.toPlainText() + f"\nPlayer: {message}")
        self.message_box.setText("")


class Field(QPushButton):
    def __init__(self, text):
        super().__init__(text)

        self.setFixedSize(60, 60)        

class PlayersBox(QWidget):
    def __init__(self, players_amount: int):
        super().__init__()
        
        layout = QVBoxLayout()
        for i in range(players_amount):
            layout.addWidget(QLabel(f"Player {i+1}: 15000$"))

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Monopoly")

        # Windows
        self.menu_container = Menu()
        self.gamemodes_container = GamemodeSettings()
        self.friends_setup_container = GameSetupFriends()
        self.game_container = Game()

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.menu_container)
        self.stacked_widget.addWidget(self.gamemodes_container)
        self.stacked_widget.addWidget(self.friends_setup_container)
        self.stacked_widget.addWidget(self.game_container)

        # Labels
        

        # Buttons
        self.menu_container.games_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        self.gamemodes_container.vialan_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.gamemodes_container.withfriends_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.gamemodes_container.withbots_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.gamemodes_container.tomenu_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        self.friends_setup_container.player_amount_combobox.currentIndexChanged.connect(self.friends_setup_container.update_player_list)
        self.friends_setup_container.start_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))

                
        # Setup actions
        self.friends_setup_container.update_player_list(0)
        self.setCentralWidget(self.stacked_widget)

app = QApplication([])

window = MainWindow()
window.show()

app.exec()