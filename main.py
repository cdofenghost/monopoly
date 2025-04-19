from PyQt6.QtGui import QIcon, QFont, QMouseEvent
from PyQt6.QtCore import QSize, Qt, QRect
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
)

from .widgets import (
    Menu,
    GamemodeSettings, 
    Game, 
    GameSetupFriends,
    ViaLANChoice,
)

from .classes.manager import GameManager
from .classes.player import Player

import sys
import logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Monopoly")

        # Windows
        self.menu_container = Menu()
        self.gamemodes_container = GamemodeSettings()
        self.friends_setup_container = GameSetupFriends()
        self.via_lan_container = ViaLANChoice()
        self.game_container = None

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.menu_container)
        self.stacked_widget.addWidget(self.gamemodes_container)
        self.stacked_widget.addWidget(self.via_lan_container)
        self.stacked_widget.addWidget(self.friends_setup_container)
        self.stacked_widget.setStyleSheet('background-color: #272A2E')

        # Labels
        

        # Buttons
        self.menu_container.games_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        self.gamemodes_container.vialan_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.gamemodes_container.withfriends_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.gamemodes_container.withbots_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.gamemodes_container.tomenu_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        self.friends_setup_container.player_amount_combobox.currentIndexChanged.connect(self.friends_setup_container.update_player_list)
        self.friends_setup_container.start_button.clicked.connect(self.start_game_session)

                
        # Setup actions
        self.friends_setup_container.update_player_list(0)
        self.setCentralWidget(self.stacked_widget)

    def start_game_session(self):
        self.players_list: list[Player] = []
        row_amount = self.friends_setup_container.player_list.rowCount()

        for row in range(row_amount):
            hbox = self.friends_setup_container.player_list.itemAt(row).layout()
            player_color = hbox.itemAt(0).widget().color()
            player_name = hbox.itemAt(2).widget().text()

            self.players_list.append(Player(name=player_name, color=player_color))

        if not self.game_container is None:
            self.game_container.deleteLater()
            self.update()

        self.game_container = Game(player_list=self.players_list)
        self.game_container.quit_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.stacked_widget.addWidget(self.game_container)
        self.stacked_widget.setCurrentIndex(4)


        #GameManager.start_game(player i need to some how get them)

app = QApplication([])

window = MainWindow()
window.show()   

app.exec()