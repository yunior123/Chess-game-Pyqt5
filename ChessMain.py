
from chess import Board, Move, QUEEN, BB_SQUARES, SQUARE_NAMES, PAWN, BISHOP, KNIGHT, KING, ROOK
# We are importing our generated python file .py
from chess.engine import *
from youtube_ui import *
from engine_ui import *
from PyQt5.QtCore import (QTimer, QThread, QRunnable, QThreadPool)
# We are using time for the splash screen in action
from PyQt5.QtCore import (QFileInfo)
from PyQt5.QtGui import (QImage)
from PyQt5.QtCore import (QByteArray, QDataStream, QIODevice, QMimeData,
                          QPoint, Qt)
from PyQt5.QtGui import QColor, QDrag, QPainter, QPixmap
from PyQt5.QtWidgets import QFrame, QLabel, QMessageBox
import time
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication
import random


def timer(func):
    def inner(*args, **kwargs):
        t1 = time.time()
        f = func(*args, **kwargs)
        t2 = time.time()
        print('Runtime took {0} seconds'.format(t2 - t1))
        # main.stockfish_move()
        return f
    return inner


class MainWindow(QMainWindow, Ui_MainWindow, QFrame):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        note_icon = QIcon("note.png")
        note = QSystemTrayIcon(note_icon, self)
        menu = QMenu()
        restore = QAction("Restore", self)
        close = QAction("Close", self)
        menu.addActions([restore, close])
        note.setContextMenu(menu)
        note.show()
        note.showMessage("Welcome to my channel", "Feel free to give it the like in order to support it ")

        self.engine_configuration_window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow_Engine()
        self.side_turn = False
        self.time_clockh_stop = False
        self.time_clockc_stop = False
        self.create_board()
        self.switch = 0
        self.board_analysis = Board()
        self.mainline = []
        self.text_list = []
        self.board = Board()
        self.promotion = [None]
        self.move_f = 0
        self.move_t = 0
        self.current_score = 1600
        self.url = []
        self.skill_level = [20]
        self.elo = [2800]
        self.depth = [40]
        self.threads = [20]
        self.hash = [80]
        self.undo_move = False
        self.redo_move = False
        self.redo_move_list = []
        self.undo_count = 0
        self.update_remainingtime_c = 0
        self.update_remainingtime_h = 0
        # self.thread = QThread()
        # self.runnable = QRunnable.create(self.pron)
        # s.run()
        # self.thread_pool = QThreadPool()
        # self.thread_pool.start(self.runnable)
        # self.thread_pool.cancel(self.runnable)
        # self.thread_pool.cancel(self.runnable)
        # self.threadpool.setExpiryTimeout(10)

        self.time.timeout.connect(self.stockfish_move)
        self.time.start(1000)

        # CLOCKS
        self.time_show.timeout.connect(self.show_time)
        self.time_show.start(1)

        # Engine analysis
        # self.time_analysis = QTimer()
        self.time_analysis.timeout.connect(self.engine_analysis)

        # Computer
        self.time_5min_clock = QTimer()
        # Human
        self.time_5min_clock_h = QTimer()
        self.clock_started = False

        self.setWindowTitle('CHESS GAME')
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        # self.setMinimumSize(200, 200)
        self.square_initial_selected = []
        self.board_mainline = Board()
        self.text_score = []
        self.BACKRANKS = [0, 1, 2, 3, 4, 5, 6, 7, 63, 62, 61, 60, 59, 58, 57, 56]

        self.actionnew.triggered.connect(self.reset_board_pieces)
        self.actionLong_Game.triggered.connect(self.flipping_the_board)
        self.actionLevels.triggered.connect(self.flipping_the_board)
        self.actionPosition_Setup.triggered.connect(self.flipping_the_board)
        self.actionDataBase.triggered.connect(self.flipping_the_board)
        self.actionFlip_Board.triggered.connect(self.flipping_the_board)
        self.actionLong_Game.triggered.connect(self.flipping_the_board)
        self.actionEngine_Configuration.triggered.connect(self.engine_configuration)
        self.actionOpen_Engine.triggered.connect(self.add_engine)
        self.actionUndo.triggered.connect(self.undo)
        self.actionRedo.triggered.connect(self.redo)
        self.actionBlitz_Game.triggered.connect(self.flipping_the_board)
        self.actionResign.triggered.connect(self.resign)
        self.actionAdd_Engine.triggered.connect(self.add_engine)

        self.check_box.stateChanged.connect(self.promote_to_queen)
        self.check_box1.stateChanged.connect(self.promote_to_bishop)
        self.check_box2.stateChanged.connect(self.promote_to_knight)
        self.check_box3.stateChanged.connect(self.promote_to_rook)

        self.dictionary_flip = {(self.list_values_x[7], self.list_values_y[7]): '{}'.format(SQUARE_NAMES[56]),
                                (self.list_values_x[6], self.list_values_y[7]): '{}'.format(SQUARE_NAMES[57]),
                                (self.list_values_x[5], self.list_values_y[7]): '{}'.format(SQUARE_NAMES[58]),
                                (self.list_values_x[4], self.list_values_y[7]): '{}'.format(SQUARE_NAMES[59]),
                                (self.list_values_x[3], self.list_values_y[7]): '{}'.format(SQUARE_NAMES[60]),
                                (self.list_values_x[2], self.list_values_y[7]): '{}'.format(SQUARE_NAMES[61]),
                                (self.list_values_x[1], self.list_values_y[7]): '{}'.format(SQUARE_NAMES[62]),
                                (self.list_values_x[0], self.list_values_y[7]): '{}'.format(SQUARE_NAMES[63]),
                                (self.list_values_x[7], self.list_values_y[6]): '{}'.format(SQUARE_NAMES[48]),
                                (self.list_values_x[6], self.list_values_y[6]): '{}'.format(SQUARE_NAMES[49]),
                                (self.list_values_x[5], self.list_values_y[6]): '{}'.format(SQUARE_NAMES[50]),
                                (self.list_values_x[4], self.list_values_y[6]): '{}'.format(SQUARE_NAMES[51]),
                                (self.list_values_x[3], self.list_values_y[6]): '{}'.format(SQUARE_NAMES[52]),
                                (self.list_values_x[2], self.list_values_y[6]): '{}'.format(SQUARE_NAMES[53]),
                                (self.list_values_x[1], self.list_values_y[6]): '{}'.format(SQUARE_NAMES[54]),
                                (self.list_values_x[0], self.list_values_y[6]): '{}'.format(SQUARE_NAMES[55]),
                                (self.list_values_x[7], self.list_values_y[5]): '{}'.format(SQUARE_NAMES[40]),
                                (self.list_values_x[6], self.list_values_y[5]): '{}'.format(SQUARE_NAMES[41]),
                                (self.list_values_x[5], self.list_values_y[5]): '{}'.format(SQUARE_NAMES[42]),
                                (self.list_values_x[4], self.list_values_y[5]): '{}'.format(SQUARE_NAMES[43]),
                                (self.list_values_x[3], self.list_values_y[5]): '{}'.format(SQUARE_NAMES[44]),
                                (self.list_values_x[2], self.list_values_y[5]): '{}'.format(SQUARE_NAMES[45]),
                                (self.list_values_x[1], self.list_values_y[5]): '{}'.format(SQUARE_NAMES[46]),
                                (self.list_values_x[0], self.list_values_y[5]): '{}'.format(SQUARE_NAMES[47]),
                                (self.list_values_x[7], self.list_values_y[4]): '{}'.format(SQUARE_NAMES[32]),
                                (self.list_values_x[6], self.list_values_y[4]): '{}'.format(SQUARE_NAMES[33]),
                                (self.list_values_x[5], self.list_values_y[4]): '{}'.format(SQUARE_NAMES[34]),
                                (self.list_values_x[4], self.list_values_y[4]): '{}'.format(SQUARE_NAMES[35]),
                                (self.list_values_x[3], self.list_values_y[4]): '{}'.format(SQUARE_NAMES[36]),
                                (self.list_values_x[2], self.list_values_y[4]): '{}'.format(SQUARE_NAMES[37]),
                                (self.list_values_x[1], self.list_values_y[4]): '{}'.format(SQUARE_NAMES[38]),
                                (self.list_values_x[0], self.list_values_y[4]): '{}'.format(SQUARE_NAMES[39]),
                                (self.list_values_x[7], self.list_values_y[3]): '{}'.format(SQUARE_NAMES[24]),
                                (self.list_values_x[6], self.list_values_y[3]): '{}'.format(SQUARE_NAMES[25]),
                                (self.list_values_x[5], self.list_values_y[3]): '{}'.format(SQUARE_NAMES[26]),
                                (self.list_values_x[4], self.list_values_y[3]): '{}'.format(SQUARE_NAMES[27]),
                                (self.list_values_x[3], self.list_values_y[3]): '{}'.format(SQUARE_NAMES[28]),
                                (self.list_values_x[2], self.list_values_y[3]): '{}'.format(SQUARE_NAMES[29]),
                                (self.list_values_x[1], self.list_values_y[3]): '{}'.format(SQUARE_NAMES[30]),
                                (self.list_values_x[0], self.list_values_y[3]): '{}'.format(SQUARE_NAMES[31]),
                                (self.list_values_x[7], self.list_values_y[2]): '{}'.format(SQUARE_NAMES[16]),
                                (self.list_values_x[6], self.list_values_y[2]): '{}'.format(SQUARE_NAMES[17]),
                                (self.list_values_x[5], self.list_values_y[2]): '{}'.format(SQUARE_NAMES[18]),
                                (self.list_values_x[4], self.list_values_y[2]): '{}'.format(SQUARE_NAMES[19]),
                                (self.list_values_x[3], self.list_values_y[2]): '{}'.format(SQUARE_NAMES[20]),
                                (self.list_values_x[2], self.list_values_y[2]): '{}'.format(SQUARE_NAMES[21]),
                                (self.list_values_x[1], self.list_values_y[2]): '{}'.format(SQUARE_NAMES[22]),
                                (self.list_values_x[0], self.list_values_y[2]): '{}'.format(SQUARE_NAMES[23]),
                                (self.list_values_x[7], self.list_values_y[1]): '{}'.format(SQUARE_NAMES[8]),
                                (self.list_values_x[6], self.list_values_y[1]): '{}'.format(SQUARE_NAMES[9]),
                                (self.list_values_x[5], self.list_values_y[1]): '{}'.format(SQUARE_NAMES[10]),
                                (self.list_values_x[4], self.list_values_y[1]): '{}'.format(SQUARE_NAMES[11]),
                                (self.list_values_x[3], self.list_values_y[1]): '{}'.format(SQUARE_NAMES[12]),
                                (self.list_values_x[2], self.list_values_y[1]): '{}'.format(SQUARE_NAMES[13]),
                                (self.list_values_x[1], self.list_values_y[1]): '{}'.format(SQUARE_NAMES[14]),
                                (self.list_values_x[0], self.list_values_y[1]): '{}'.format(SQUARE_NAMES[15]),
                                (self.list_values_x[7], self.list_values_y[0]): '{}'.format(SQUARE_NAMES[0]),
                                (self.list_values_x[6], self.list_values_y[0]): '{}'.format(SQUARE_NAMES[1]),
                                (self.list_values_x[5], self.list_values_y[0]): '{}'.format(SQUARE_NAMES[2]),
                                (self.list_values_x[4], self.list_values_y[0]): '{}'.format(SQUARE_NAMES[3]),
                                (self.list_values_x[3], self.list_values_y[0]): '{}'.format(SQUARE_NAMES[4]),
                                (self.list_values_x[2], self.list_values_y[0]): '{}'.format(SQUARE_NAMES[5]),
                                (self.list_values_x[1], self.list_values_y[0]): '{}'.format(SQUARE_NAMES[6]),
                                (self.list_values_x[0], self.list_values_y[0]): '{}'.format(SQUARE_NAMES[7]),
                                }
        self.dictionary = {(self.list_values_x[0], self.list_values_y[0]): '{}'.format(SQUARE_NAMES[56]),
                           (self.list_values_x[1], self.list_values_y[0]): '{}'.format(SQUARE_NAMES[57]),
                           (self.list_values_x[2], self.list_values_y[0]): '{}'.format(SQUARE_NAMES[58]),
                           (self.list_values_x[3], self.list_values_y[0]): '{}'.format(SQUARE_NAMES[59]),
                           (self.list_values_x[4], self.list_values_y[0]): '{}'.format(SQUARE_NAMES[60]),
                           (self.list_values_x[5], self.list_values_y[0]): '{}'.format(SQUARE_NAMES[61]),
                           (self.list_values_x[6], self.list_values_y[0]): '{}'.format(SQUARE_NAMES[62]),
                           (self.list_values_x[7], self.list_values_y[0]): '{}'.format(SQUARE_NAMES[63]),
                           (self.list_values_x[0], self.list_values_y[1]): '{}'.format(SQUARE_NAMES[48]),
                           (self.list_values_x[1], self.list_values_y[1]): '{}'.format(SQUARE_NAMES[49]),
                           (self.list_values_x[2], self.list_values_y[1]): '{}'.format(SQUARE_NAMES[50]),
                           (self.list_values_x[3], self.list_values_y[1]): '{}'.format(SQUARE_NAMES[51]),
                           (self.list_values_x[4], self.list_values_y[1]): '{}'.format(SQUARE_NAMES[52]),
                           (self.list_values_x[5], self.list_values_y[1]): '{}'.format(SQUARE_NAMES[53]),
                           (self.list_values_x[6], self.list_values_y[1]): '{}'.format(SQUARE_NAMES[54]),
                           (self.list_values_x[7], self.list_values_y[1]): '{}'.format(SQUARE_NAMES[55]),
                           (self.list_values_x[0], self.list_values_y[2]): '{}'.format(SQUARE_NAMES[40]),
                           (self.list_values_x[1], self.list_values_y[2]): '{}'.format(SQUARE_NAMES[41]),
                           (self.list_values_x[2], self.list_values_y[2]): '{}'.format(SQUARE_NAMES[42]),
                           (self.list_values_x[3], self.list_values_y[2]): '{}'.format(SQUARE_NAMES[43]),
                           (self.list_values_x[4], self.list_values_y[2]): '{}'.format(SQUARE_NAMES[44]),
                           (self.list_values_x[5], self.list_values_y[2]): '{}'.format(SQUARE_NAMES[45]),
                           (self.list_values_x[6], self.list_values_y[2]): '{}'.format(SQUARE_NAMES[46]),
                           (self.list_values_x[7], self.list_values_y[2]): '{}'.format(SQUARE_NAMES[47]),
                           (self.list_values_x[0], self.list_values_y[3]): '{}'.format(SQUARE_NAMES[32]),
                           (self.list_values_x[1], self.list_values_y[3]): '{}'.format(SQUARE_NAMES[33]),
                           (self.list_values_x[2], self.list_values_y[3]): '{}'.format(SQUARE_NAMES[34]),
                           (self.list_values_x[3], self.list_values_y[3]): '{}'.format(SQUARE_NAMES[35]),
                           (self.list_values_x[4], self.list_values_y[3]): '{}'.format(SQUARE_NAMES[36]),
                           (self.list_values_x[5], self.list_values_y[3]): '{}'.format(SQUARE_NAMES[37]),
                           (self.list_values_x[6], self.list_values_y[3]): '{}'.format(SQUARE_NAMES[38]),
                           (self.list_values_x[7], self.list_values_y[3]): '{}'.format(SQUARE_NAMES[39]),
                           (self.list_values_x[0], self.list_values_y[4]): '{}'.format(SQUARE_NAMES[24]),
                           (self.list_values_x[1], self.list_values_y[4]): '{}'.format(SQUARE_NAMES[25]),
                           (self.list_values_x[2], self.list_values_y[4]): '{}'.format(SQUARE_NAMES[26]),
                           (self.list_values_x[3], self.list_values_y[4]): '{}'.format(SQUARE_NAMES[27]),
                           (self.list_values_x[4], self.list_values_y[4]): '{}'.format(SQUARE_NAMES[28]),
                           (self.list_values_x[5], self.list_values_y[4]): '{}'.format(SQUARE_NAMES[29]),
                           (self.list_values_x[6], self.list_values_y[4]): '{}'.format(SQUARE_NAMES[30]),
                           (self.list_values_x[7], self.list_values_y[4]): '{}'.format(SQUARE_NAMES[31]),
                           (self.list_values_x[0], self.list_values_y[5]): '{}'.format(SQUARE_NAMES[16]),
                           (self.list_values_x[1], self.list_values_y[5]): '{}'.format(SQUARE_NAMES[17]),
                           (self.list_values_x[2], self.list_values_y[5]): '{}'.format(SQUARE_NAMES[18]),
                           (self.list_values_x[3], self.list_values_y[5]): '{}'.format(SQUARE_NAMES[19]),
                           (self.list_values_x[4], self.list_values_y[5]): '{}'.format(SQUARE_NAMES[20]),
                           (self.list_values_x[5], self.list_values_y[5]): '{}'.format(SQUARE_NAMES[21]),
                           (self.list_values_x[6], self.list_values_y[5]): '{}'.format(SQUARE_NAMES[22]),
                           (self.list_values_x[7], self.list_values_y[5]): '{}'.format(SQUARE_NAMES[23]),
                           (self.list_values_x[0], self.list_values_y[6]): '{}'.format(SQUARE_NAMES[8]),
                           (self.list_values_x[1], self.list_values_y[6]): '{}'.format(SQUARE_NAMES[9]),
                           (self.list_values_x[2], self.list_values_y[6]): '{}'.format(SQUARE_NAMES[10]),
                           (self.list_values_x[3], self.list_values_y[6]): '{}'.format(SQUARE_NAMES[11]),
                           (self.list_values_x[4], self.list_values_y[6]): '{}'.format(SQUARE_NAMES[12]),
                           (self.list_values_x[5], self.list_values_y[6]): '{}'.format(SQUARE_NAMES[13]),
                           (self.list_values_x[6], self.list_values_y[6]): '{}'.format(SQUARE_NAMES[14]),
                           (self.list_values_x[7], self.list_values_y[6]): '{}'.format(SQUARE_NAMES[15]),
                           (self.list_values_x[0], self.list_values_y[7]): '{}'.format(SQUARE_NAMES[0]),
                           (self.list_values_x[1], self.list_values_y[7]): '{}'.format(SQUARE_NAMES[1]),
                           (self.list_values_x[2], self.list_values_y[7]): '{}'.format(SQUARE_NAMES[2]),
                           (self.list_values_x[3], self.list_values_y[7]): '{}'.format(SQUARE_NAMES[3]),
                           (self.list_values_x[4], self.list_values_y[7]): '{}'.format(SQUARE_NAMES[4]),
                           (self.list_values_x[5], self.list_values_y[7]): '{}'.format(SQUARE_NAMES[5]),
                           (self.list_values_x[6], self.list_values_y[7]): '{}'.format(SQUARE_NAMES[6]),
                           (self.list_values_x[7], self.list_values_y[7]): '{}'.format(SQUARE_NAMES[7]),
                           }


    def redo(self):
        print('redo')
        if self.undo_count > 0:
            print('move', self.redo_move_list[-1])
            if self.redo_move_list:
                redo_value = self.redo_move_list[-self.undo_count]
                self.undo_count -= 1
                dictionary = self.dictionary if self.side_turn is False else self.dictionary_flip
                print(redo_value, self.undo_count, 'redo and undo_count', self.redo_move_list)
                position = self.get_keys_for_value(dictionary, str(redo_value)[0:2])
                forward_position = self.get_keys_for_value(dictionary, str(redo_value)[2:4])
                child_to_delete = self.childAt(forward_position[0][0], forward_position[0][1])
                if type(child_to_delete) == QLabel:
                    child_to_delete.close()
                child_forward = self.childAt(position[0][0], position[0][1])
                child_forward.move(forward_position[0][0], forward_position[0][1])

    def undo(self):
        if self.mainline:
            if not self.redo_move_list:
                self.redo_move_list = self.mainline.copy()
            self.undo_count += 1
            self.undo_move = True
            self.mainline.pop()
            # print(self.board.turn)
            dictionary = self.dictionary if self.side_turn is False else self.dictionary_flip
            move = self.board.pop()
            print(move)
            position = self.get_keys_for_value(dictionary, str(move)[2: 4])
            previous_position = self.get_keys_for_value(dictionary, str(move)[0:2])

            print(position)
            # print(str(self.board.pop())[4:6])
            child_to_delete = self.childAt(position[0][0], position[0][1])
            print(type(child_to_delete))
            if type(child_to_delete) == QLabel:
                child_to_delete.close()

            # print(self.board.piece_type_at(Move.from_uci(str(move)).from_square))
            if self.board.piece_type_at(Move.from_uci(str(move)).from_square) == PAWN and self.board.turn is False:
                self._undo_new_pieces(previous_position, color='black', type_p='pawn')
            elif self.board.piece_type_at(Move.from_uci(str(move)).from_square) == PAWN and self.board.turn is True:
                self._undo_new_pieces(previous_position, color='white', type_p='pawn')
            elif self.board.piece_type_at(Move.from_uci(str(move)).from_square) == KNIGHT and self.board.turn is False:
                self._undo_new_pieces(previous_position, color='black', type_p='knight')
            elif self.board.piece_type_at(Move.from_uci(str(move)).from_square) == KNIGHT and self.board.turn is True:
                self._undo_new_pieces(previous_position, color='white', type_p='knight')
            elif self.board.piece_type_at(Move.from_uci(str(move)).from_square) == BISHOP and self.board.turn is False:
                self._undo_new_pieces(previous_position, color='black', type_p='bishop')
            elif self.board.piece_type_at(Move.from_uci(str(move)).from_square) == BISHOP and self.board.turn is True:
                self._undo_new_pieces(previous_position, color='white', type_p='bishop')
            elif self.board.piece_type_at(Move.from_uci(str(move)).from_square) == KING and self.board.turn is False:
                self._undo_new_pieces(previous_position, color='black', type_p='king')
            elif self.board.piece_type_at(Move.from_uci(str(move)).from_square) == KING and self.board.turn is True:
                self._undo_new_pieces(previous_position, color='white', type_p='king')
            elif self.board.piece_type_at(Move.from_uci(str(move)).from_square) == QUEEN and self.board.turn is False:
                self._undo_new_pieces(previous_position, color='black', type_p='queen')
            elif self.board.piece_type_at(Move.from_uci(str(move)).from_square) == QUEEN and self.board.turn is True:
                self._undo_new_pieces(previous_position, color='white', type_p='queen')
            elif self.board.piece_type_at(Move.from_uci(str(move)).from_square) == ROOK and self.board.turn is False:
                self._undo_new_pieces(previous_position, color='black', type_p='rook')
            elif self.board.piece_type_at(Move.from_uci(str(move)).from_square) == ROOK and self.board.turn is True:
                self._undo_new_pieces(previous_position, color='white', type_p='rook')
            if self.board.piece_type_at(Move.from_uci(str(move)).to_square) == PAWN and self.board.turn is True:
                self._undo_new_pieces(position, color='black', type_p='pawn')
            if self.board.piece_type_at(Move.from_uci(str(move)).to_square) == PAWN and self.board.turn is False:
                self._undo_new_pieces(position, color='white', type_p='pawn')
            if self.board.piece_type_at(Move.from_uci(str(move)).to_square) == BISHOP and self.board.turn is True:
                self._undo_new_pieces(position, color='black', type_p='bishop')
            if self.board.piece_type_at(Move.from_uci(str(move)).to_square) == BISHOP and self.board.turn is False:
                self._undo_new_pieces(position, color='white', type_p='bishop')
            if self.board.piece_type_at(Move.from_uci(str(move)).to_square) == KNIGHT and self.board.turn is True:
                self._undo_new_pieces(position, color='black', type_p='knight')
            if self.board.piece_type_at(Move.from_uci(str(move)).to_square) == KNIGHT and self.board.turn is False:
                self._undo_new_pieces(position, color='white', type_p='knight')
            if self.board.piece_type_at(Move.from_uci(str(move)).to_square) == QUEEN and self.board.turn is True:
                self._undo_new_pieces(position, color='black', type_p='queen')
            if self.board.piece_type_at(Move.from_uci(str(move)).to_square) == QUEEN and self.board.turn is False:
                self._undo_new_pieces(position, color='white', type_p='queen')
            if self.board.piece_type_at(Move.from_uci(str(move)).to_square) == KING and self.board.turn is True:
                self._undo_new_pieces(position, color='black', type_p='king')
            if self.board.piece_type_at(Move.from_uci(str(move)).to_square) == KING and self.board.turn is False:
                self._undo_new_pieces(position, color='white', type_p='king')
            if self.board.piece_type_at(Move.from_uci(str(move)).to_square) == ROOK and self.board.turn is True:
                self._undo_new_pieces(position, color='black', type_p='rook')
            if self.board.piece_type_at(Move.from_uci(str(move)).to_square) == ROOK and self.board.turn is False:
                self._undo_new_pieces(position, color='white', type_p='rook')
            if self.board.has_queenside_castling_rights(True) and str(move) == "e1c1":
                child_castling_e1c1 = self.childAt(self.get_keys_for_value(dictionary, 'd1')[0][0],
                                                   self.get_keys_for_value(dictionary, 'd1')[0][1])
                if type(child_castling_e1c1) == QLabel:
                    child_castling_e1c1.move(self.get_keys_for_value(dictionary, 'a1')[0][0],
                                             self.get_keys_for_value(dictionary, 'a1')[0][1])
            if self.board.has_kingside_castling_rights(True) and str(move) == "e1g1":
                child_castling_e1g1 = self.childAt(self.get_keys_for_value(dictionary, "f1")[0][0],
                                                   self.get_keys_for_value(dictionary, "f1")[0][1])
                if type(child_castling_e1g1) == QLabel:
                    child_castling_e1g1.move(self.get_keys_for_value(dictionary, 'h1')[0][0],
                                             self.get_keys_for_value(dictionary, 'h1')[0][1])
            if self.board.has_queenside_castling_rights(False) and str(move) == "e8c8":
                child_castling_e8c8 = self.childAt(self.get_keys_for_value(dictionary, 'd8')[0][0],
                                                   self.get_keys_for_value(dictionary, 'd8')[0][1])
                if type(child_castling_e8c8) == QLabel:
                    child_castling_e8c8.move(self.get_keys_for_value(dictionary, 'a8')[0][0],
                                             self.get_keys_for_value(dictionary, 'a8')[0][1])
            if self.board.has_kingside_castling_rights(False) and str(move) == "e8g8":
                child_castling_e8g8 = self.childAt(self.get_keys_for_value(dictionary, 'f8')[0][0],
                                                   self.get_keys_for_value(dictionary, 'f8')[0][1])
                if type(child_castling_e8g8) == QLabel:
                    child_castling_e8g8.move(self.get_keys_for_value(dictionary, 'h8')[0][0],
                                             self.get_keys_for_value(dictionary, 'h8')[0][1])

    def _undo_new_pieces(self, previous_position, color, type_p):
        root = QFileInfo(__file__).absolutePath()
        print(root + '/iconos/' + '{}'.format(color)+'_'+type_p+'.png')
        image_white_pawn = QImage(root + '/iconos/' + '{}'.format(color)+'_'+type_p+'.png')
        print(image_white_pawn)
        # white_pawn.png
        self.new_pawn = QtWidgets.QLabel(self)
        self.new_pawn.setGeometry(QtCore.QRect(0, 0, 71, 71))
        self.new_pawn.setPixmap(
            QPixmap.fromImage(image_white_pawn).scaled(70, 70, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        self.new_pawn.adjustSize()
        self.new_pawn.move(previous_position[0][0], previous_position[0][1])
        self.new_pawn.show()
        self.new_pawn.setAttribute(Qt.WA_DeleteOnClose)
        self.undo_move = True

    def engine_configuration(self):
        print("engine configuration")
        self.ui.setupUi(self.engine_configuration_window)
        self.engine_configuration_window.show()
        self.ui.toolButton.clicked.connect(self.new_engine_values)

    def new_engine_values(self):
        # print('new engine values')
        # print(self.ui.lineEdit.text())
        # print(self.ui.lineEdit.text() == "")
        if not self.ui.lineEdit.text() == "":
            self.hash.insert(0, int(self.ui.lineEdit.text()))
        # print(self.ui.lineEdit_2.text())
        if not self.ui.lineEdit_2.text() == "":
            self.skill_level.insert(0, int(self.ui.lineEdit_2.text()))
        # print(self.ui.lineEdit_3.text())
        if not self.ui.lineEdit_3.text() == "":
            self.elo.insert(0, int(self.ui.lineEdit_3.text()))
        # print(self.ui.lineEdit_4.text())
        if not self.ui.lineEdit_4.text() == "":
            self.depth.insert(0, int(self.ui.lineEdit_4.text()))
        # print(self.ui.lineEdit_5.text())
        if not self.ui.lineEdit_5.text() == "":
            self.threads.insert(0, int(self.ui.lineEdit_5.text()))

    def add_engine(self):
        print('engine add')
        open_engine = QFileDialog.getOpenFileUrl(self, caption='Open New Engine')
        print(open_engine)
        print(open_engine[0].toString()[8:])
        self.url.insert(0, open_engine[0].toString()[8:])
        # print(str(QDir.toNativeSeparators( open_engine[0].toString()[8:])))

    def resign(self):
        self.stop_clock()
        self.stop_clock_human()
        # self.update_remainingtime_c = 0
        QMessageBox.warning(self, "You resigned", "Your score will get down -20")
        self.lcdNumber_2.display(self.current_score - 20)

    def reset_board_pieces(self):
        self.undo_move = False
        self.update_remainingtime_h = 0
        self.update_remainingtime_c = 0
        self.clock_started = False
        for child in self.children():
            if (type(child)) == QLabel:
                # print(child)
                child.deleteLater()
        self.board.reset()
        self.board_mainline.reset()
        self.mainline = []
        self.create_board()
        # print(self.side_turn,'side turn')
        if self.side_turn is True:
            self.flip_board_icons()
            self.time_5min_clock.start(300000)

    def promote_to_queen(self):
        # print('checked', self.check_box.isChecked())
        self.promote_piece(QUEEN, 'queen')

    def promote_to_knight(self):
        self.promote_piece(QUEEN, 'knight')

    def promote_to_bishop(self):
        self.promote_piece(QUEEN, 'bishop')

    def promote_to_rook(self):
        self.promote_piece(QUEEN, 'rook')

    def promote_piece(self, type_piece, str_piece):
        color = 'white'
        if self.board.turn is False:
            color = 'black'
        print('checked', self.check_box.isChecked())
        # self.check_box.setChecked(True)
        # self.check_box.stateChanged()
        if self.promotion[0] is not None and self.check_box.isChecked():
            print('somefunction', self.board.promoted, self.promotion[0])
            position = self.get_keys_for_value(self.dictionary, '{}'.format(SQUARE_NAMES[self.promotion[0]]))
            print(position)
            child = self.childAt(position[0][0], position[0][1])

            if (type(child)) != QWidget:
                # print(child)
                child.close()

            # Move.from_uci(move_from + move_to).to_square == any(BACKRANK for BACKRANK in BACKRANKS)
            if self.move_t != 0:
                print(self.move_f, self.move_t, 'moves from and to')
                if any(BACKRANK == Move.from_uci(str(self.move_f + self.move_t)).to_square for BACKRANK in self.BACKRANKS):
                    if self.board.piece_type_at(Move.from_uci(str(self.move_f + self.move_t)).from_square) == PAWN:
                        from_s = Move.from_uci(str(self.move_f + self.move_t)).from_square
                        to_s = Move.from_uci(str(self.move_f + self.move_t)).to_square
                        # to_s = 61
                        print('promotion', bin(BB_SQUARES[Move.from_uci(str(self.move_f + self.move_t)).to_square]))
                        print(self.check_box.text().upper())
                        promotion_move = Move(from_s, to_s, promotion=type_piece)
                        # promotion_value = True
                        self.board.push(promotion_move)
                        self.mainline.append("{}".format(promotion_move))
                        print(promotion_move)
                        self.move_t = 0
                        self.move_f = 0
                        # QMessageBox.information(self, "promotion", "Select a piece ")
            root = QFileInfo(__file__).absolutePath()
            image = QImage(root + '/iconos/' + '{}'.format(color) + '_' + '{}'.format(str_piece) + '.png')
            new_icon = QtWidgets.QLabel(self)
            new_icon.setGeometry(QtCore.QRect(position[0][0], position[0][1], 71, 71))
            new_icon.setPixmap(
                QPixmap.fromImage(image).scaled(70, 70, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
            new_icon.adjustSize()
            new_icon.move(position[0][0], position[0][1])
            new_icon.show()
            new_icon.setAttribute(Qt.WA_DeleteOnClose)
            self.promotion.insert(0, None)

    keyPressed = pyqtSignal(int)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Space:
            # self.close()
            main.stockfish_move()
            self.keyPressed.emit(Qt.Key(e.key()))

    def flipping_the_board(self):
        self.board_mainline.reset()
        self.label_3.setText("")
        self.undo_move = False
        self.mainline.clear()
        self.clock_started = False
        if self.switch == 0:
            self.update_remainingtime_h = 0
            self.update_remainingtime_c = 0
            self.time_5min_clock.start(300000)
            for child in self.children():
                if (type(child)) == QLabel:
                    # print(child)
                    child.deleteLater()
            self.create_board()
            self.flip_board_icons()
            self.side_turn = True
            self.board.reset()
            self.switch = 1
        elif self.switch == 1:
            self.update_remainingtime_h = 0
            self.update_remainingtime_c = 0
            for child in self.children():
                if (type(child)) == QLabel:
                    # print(child)
                    child.deleteLater()
            self.create_board()
            self.side_turn = False
            self.board.reset()
            self.switch = 0

    @staticmethod
    def get_keys_for_value(dictionary, value):
        return [key for key in dictionary if dictionary[key] == value]

    def dragEnterEvent(self, event):
        self.setCursor(Qt.ClosedHandCursor)
        if event.mimeData().hasFormat('iconos/x-white_pawn'):
            if event.source() == self:
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()

    dragMoveEvent = dragEnterEvent

    def mousePressEvent(self, event):
        self.setCursor(Qt.ClosedHandCursor)
        child = self.childAt(event.pos())
        if not child:
            return
        if (type(child)) != QWidget and (type(child)) != QCheckBox and (type(child)) != QToolButton:
            square_initial = self.target_square(event.pos())
            self.square_initial_selected.insert(0, square_initial)
            if not child:
                return
            pixmap = QPixmap(child.pixmap())

            item_data = QByteArray()
            data_stream = QDataStream(item_data, QIODevice.WriteOnly)
            data_stream << pixmap << QPoint(event.pos() - child.pos())

            mime_data = QMimeData()
            mime_data.setData('iconos/x-white_pawn', item_data)

            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos() - child.pos())

            temp_pixmap = QPixmap(pixmap)
            painter = QPainter()
            painter.begin(temp_pixmap)
            painter.fillRect(pixmap.rect(), QColor(127, 127, 127, 127))
            painter.end()

            child.setPixmap(temp_pixmap)
            if drag.exec_(Qt.CopyAction | Qt.MoveAction, Qt.CopyAction) == Qt.MoveAction:
                child.close()
            else:
                child.show()
                child.setPixmap(pixmap)
        else:
            if (type(child)) == QCheckBox:
                # child.setChecked(False)
                event.ignore()
                event.accept()

    @timer
    def dropEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        if self.update_remainingtime_c == 0:
            self.time_5min_clock.start(300000)
            self.time_clockc_stop = False
        if self.update_remainingtime_c != 0:
            self.time_5min_clock.start(self.update_remainingtime_c)
            self.time_clockc_stop = False
        if self.clock_started is True:
            remain_time = self.time_5min_clock_h.remainingTime()
            self.update_remainingtime_h = remain_time
            self.stop_clock_human()
        self.update_remainingtime_c = self.time_5min_clock.remainingTime()

        item_data = event.mimeData().data('iconos/x-white_pawn')
        data_stream = QDataStream(item_data, QIODevice.ReadOnly)
        square_t = self.target_square(event.pos())
        selected = self.square_initial_selected[0]
        same_move = 0
        dictionary = self.dictionary if self.board.turn is True else self.dictionary_flip

        move_from = "{}".format(dictionary[(selected[0], selected[1])])
        move_to = "{}".format(dictionary[(square_t[0], square_t[1])])
        child = self.childAt(event.pos())
        # print(self.board.promoted)
        self.BACKRANKS = [0, 1, 2, 3, 4, 5, 6, 7, 63, 62, 61, 60, 59, 58, 57, 56]
        if not(move_from == move_to):
            if (type(child)) != QWidget and (Move.from_uci(move_from + move_to) in self.board.legal_moves):
                # print(child)
                child.close()
        if move_from == move_to:
            print('here')
            same_move = 1
            pixmap = QPixmap()
            offset = QPoint()
            data_stream >> pixmap >> offset
            newicon = QLabel(self)
            newicon.setPixmap(pixmap)
            newicon.move(event.pos() - offset)
            newicon.adjustSize()
            newicon.move(square_t[0], square_t[1])
            newicon.show()
            newicon.setAttribute(Qt.WA_DeleteOnClose)
            event.setDropAction(Qt.MoveAction)
            event.accept()
        if same_move == 0:
            if any(BACKRANK == Move.from_uci(move_from + move_to).to_square for BACKRANK in self.BACKRANKS):
                if self.board.piece_type_at(Move.from_uci(move_from + move_to).from_square) == PAWN:
                    # from_s = Move.from_uci(move_from + move_to).from_square
                    to_s = Move.from_uci(move_from + move_to).to_square
                    # to_s = 61
                    print('promotion', bin(BB_SQUARES[Move.from_uci(move_from + move_to).to_square]))
                    print(self.check_box.text())
                    # promotion_move = Move(from_s, to_s, promotion=QUEEN)
                    # promotion_value = True
                    self.move_f = move_from
                    self.move_t = move_to
                    print(self.move_f, self.move_t, 'at the drop event')
                    print(self.board.promoted)
                    self.promotion.insert(0, to_s)
                    event.setDropAction(Qt.MoveAction)
                    event.accept()
                    QMessageBox.information(self, "promotion", "Select a piece ")
        if self.promotion[0] is None and same_move == 0:
            if event.mimeData().hasFormat('iconos/x-white_pawn') and self.board.turn is not self.side_turn:
                # print('here', move_from, move_to)
                if Move.from_uci(move_from + move_to) in self.board.legal_moves:
                    move = Move.from_uci(move_from + move_to)
                    # print(self.board.is_en_passant(move))
                    if self.board.is_en_passant(move):
                        diff = 70 if self.board.turn is True else -70
                        child_remove = self.childAt(square_t[0], square_t[1]+diff)
                        if (type(child_remove)) != QWidget:
                            # print(child)
                            child_remove.close()
                    # print(move, 'move')
                    complete_move = move_from + move_to

                    if self.board.has_queenside_castling_rights(True) and complete_move == "e1c1":
                        child_castling_e1c1 = self.childAt(self.get_keys_for_value(dictionary, 'a1')[0][0],
                                                           self.get_keys_for_value(dictionary, 'a1')[0][1])
                        if type(child_castling_e1c1) == QLabel:
                            child_castling_e1c1.move(self.get_keys_for_value(dictionary, 'd1')[0][0],
                                                     self.get_keys_for_value(dictionary, 'd1')[0][1])
                        self.board.castling_shredder_fen()
                    if self.board.has_kingside_castling_rights(True) and complete_move == "e1g1":
                        child_castling_e1g1 = self.childAt(self.get_keys_for_value(dictionary, 'h1')[0][0],
                                                           self.get_keys_for_value(dictionary, 'h1')[0][1])
                        if type(child_castling_e1g1) == QLabel:
                            child_castling_e1g1.move(self.get_keys_for_value(dictionary, "f1")[0][0],
                                                     self.get_keys_for_value(dictionary, "f1")[0][1])
                        self.board.castling_shredder_fen()
                    if self.board.has_queenside_castling_rights(False) and complete_move == "e8c8":
                        child_castling_e8c8 = self.childAt(self.get_keys_for_value(dictionary, 'a8')[0][0],
                                                           self.get_keys_for_value(dictionary, 'a8')[0][1])
                        if type(child_castling_e8c8) == QLabel:
                            child_castling_e8c8.move(self.get_keys_for_value(dictionary, 'd8')[0][0],
                                                     self.get_keys_for_value(dictionary, 'd8')[0][1])
                        self.board.castling_shredder_fen()
                    if self.board.has_kingside_castling_rights(False) and complete_move == "e8g8":
                        child_castling_e8g8 = self.childAt(self.get_keys_for_value(dictionary, 'h8')[0][0],
                                                           self.get_keys_for_value(dictionary, 'h8')[0][1])
                        if type(child_castling_e8g8) == QLabel:
                            child_castling_e8g8.move(self.get_keys_for_value(dictionary, 'f8')[0][0],
                                                     self.get_keys_for_value(dictionary, 'f8')[0][1])
                        self.board.castling_shredder_fen()

                    self.board.push(move)
                    self.mainline.append("{}".format(move))

                    pixmap = QPixmap()
                    offset = QPoint()
                    data_stream >> pixmap >> offset
                    newicon = QLabel(self)
                    newicon.setPixmap(pixmap)
                    newicon.move(event.pos() - offset)
                    newicon.adjustSize()
                    newicon.move(square_t[0], square_t[1])
                    newicon.show()
                    newicon.setAttribute(Qt.WA_DeleteOnClose)

                    if event.source() == self:
                        event.setDropAction(Qt.MoveAction)
                        event.accept()
                    else:
                        event.acceptProposedAction()
            else:
                event.ignore()
                event.accept()
        else:
            if self.promotion[0] is None:
                event.ignore()
                event.accept()
        if self.board.is_game_over():
            self.stop_clock_human()
            self.stop_clock()
            QMessageBox.information(self, 'Game Over', 'The game is over')

    def target_square(self, position):
        val_x = 0
        val_y = 0

        for first_value in self.list_values_x:
            second_value = first_value + 71
            if first_value < position.x() < second_value:
                val_x = first_value
                break

        for first_value_y in self.list_values_y:
            second_value_y = first_value_y + 71
            if first_value_y < position.y() < second_value_y:
                val_y = first_value_y
                break

        return [val_x, val_y, 71, 71]

    def stockfish_move(self):

        _translate = QtCore.QCoreApplication.translate
        text_mainline = self.board_mainline.variation_san([Move.from_uci(main_v) for main_v in self.mainline])
        # print(text_mainline[-3:])
        self.label_3.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-weight:600;\"> " +
                                        "{}".format(text_mainline) +
                                        "</span> Standard Notation</p></body></html>"))
        # self.label_3.setText(text_mainline)

        # print(self.board.result)
        # self.undo_move = False
        if not self.board.is_game_over() and not self.undo_move:
            t1 = time.time()
            self.undo_move = False
            if (self.board.turn and self.side_turn) or (self.board.turn is False and self.side_turn is False):
                dictionary = self.dictionary if self.board.turn is False else self.dictionary_flip
                limit = Limit(time=0.2, depth=self.depth[0])
                # print(engine.options)
                root = QFileInfo(__file__).absolutePath()
                # location = root + '/stockfish-11-win/Windows/stockfish_20011801_x64.exe'
                location = root + '/Stockfish-NNUE/sf-nnue-avx2.exe'
                if self.url:
                    if self.url[0] != "":
                        location = self.url[0]
                        print(location, 'location', type(location))

                engine = SimpleEngine.popen_uci(location)
                engine.configure({"Skill level": self.skill_level[0]})
                engine.configure({"UCI_Elo": self.elo[0]})
                engine.configure({"Hash": self.hash[0]})
                engine.configure({"Threads": self.threads[0]})
                move_engine = engine.play(board=self.board, limit=limit).move
                # print(engine.options)
                # ponder = True
                split = ("{}".format(move_engine))
                if self.board.is_game_over() is False:
                    if self.board.is_en_passant(move_engine):
                        diff = 70 if self.board.turn is True else -70
                        square_b = self.get_keys_for_value(self.dictionary, '{}'.format(SQUARE_NAMES[move_engine[2:4]]))
                        child_remove = self.childAt(square_b[0][0], square_b[0][1] + diff)
                        if (type(child_remove)) != QWidget:
                            # print(child)
                            child_remove.deleteLater()

                get_child_from = self.get_keys_for_value(dictionary, '{}'.format(split[0:2]))[0]
                get_child_to = self.get_keys_for_value(dictionary, '{}'.format(split[2:4]))[0]
                child_two = self.childAt(get_child_to[0], get_child_to[1])
                if (type(child_two)) == QLabel:
                    child_two.close()
                child_one = self.childAt(get_child_from[0], get_child_from[1])
                child_one.move(get_child_to[0], get_child_to[1])
                child_one.show()
                child_one.setAttribute(Qt.WA_DeleteOnClose)
                # child_one.deleteLater()

                if any(BACKRANK == Move.from_uci(str(move_engine)).to_square for BACKRANK in self.BACKRANKS):
                    if self.board.piece_type_at(Move.from_uci(str(move_engine)).from_square) == PAWN:
                        child_one.deleteLater()
                        new_promotion = QtWidgets.QLabel(self)
                        new_promotion.setGeometry(QtCore.QRect(80, 20, 71, 71))
                        new_promotion.setObjectName("promotion")
                        image_b = 0
                        image_w = 0
                        # Black queen
                        if move_engine.promotion == 5:
                            image_w = QImage(root + '/iconos/white_queen.png')
                            image_b = QImage(root + '/iconos/black_queen.png')
                        elif move_engine.promotion == 4:
                            image_w = QImage(root + '/iconos/white_rook.png')
                            image_b = QImage(root + '/iconos/black_rook.png')
                        elif move_engine.promotion == 3:
                            image_w = QImage(root + '/iconos/white_bishop.png')
                            image_b = QImage(root + '/iconos/black_bishop.png')
                        elif move_engine.promotion == 2:
                            image_w = QImage(root + '/iconos/white_knight.png')
                            image_b = QImage(root + '/iconos/black_knight.png')
                        print(move_engine.promotion, 'promotion move engine')
                        new_promotion.setPixmap(
                            QPixmap.fromImage(image_b if self.board.turn is False
                                              else image_w).scaled(70,
                                                                   70, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
                        new_promotion.adjustSize()
                        new_promotion.move(get_child_to[0], get_child_to[1])
                        new_promotion.show()
                        new_promotion.setAttribute(Qt.WA_DeleteOnClose)

                if self.board.has_queenside_castling_rights(True) and str(move_engine) == "e1c1":
                    child_castling_e1c1 = self.childAt(self.get_keys_for_value(dictionary, 'a1')[0][0],
                                                       self.get_keys_for_value(dictionary, 'a1')[0][1])
                    if type(child_castling_e1c1) == QLabel:
                        child_castling_e1c1.move(self.get_keys_for_value(dictionary, 'd1')[0][0],
                                                 self.get_keys_for_value(dictionary, 'd1')[0][1])
                    self.board.castling_shredder_fen()
                if self.board.has_kingside_castling_rights(True) and str(move_engine) == "e1g1":
                    child_castling_e1g1 = self.childAt(self.get_keys_for_value(dictionary, 'h1')[0][0],
                                                       self.get_keys_for_value(dictionary, 'h1')[0][1])
                    if type(child_castling_e1g1) == QLabel:

                        child_castling_e1g1.move(self.get_keys_for_value(dictionary, "f1")[0][0],
                                                 self.get_keys_for_value(dictionary, "f1")[0][1])
                    self.board.castling_shredder_fen()
                if self.board.has_queenside_castling_rights(False) and str(move_engine) == "e8c8":
                    child_castling_e8c8 = self.childAt(self.get_keys_for_value(dictionary, 'a8')[0][0],
                                                       self.get_keys_for_value(dictionary, 'a8')[0][1])
                    if type(child_castling_e8c8) == QLabel:
                        child_castling_e8c8.move(self.get_keys_for_value(dictionary, 'd8')[0][0],
                                                 self.get_keys_for_value(dictionary, 'd8')[0][1])
                    self.board.castling_shredder_fen()
                if self.board.has_kingside_castling_rights(False) and str(move_engine) == "e8g8":
                    child_castling_e8g8 = self.childAt(self.get_keys_for_value(dictionary, 'h8')[0][0],
                                                       self.get_keys_for_value(dictionary, 'h8')[0][1])
                    if type(child_castling_e8g8) == QLabel:
                        child_castling_e8g8.move(self.get_keys_for_value(dictionary, 'f8')[0][0],
                                                 self.get_keys_for_value(dictionary, 'f8')[0][1])
                    self.board.castling_shredder_fen()

                self.board.push(Move.from_uci(str(move_engine)))
                self.mainline.append("{}".format(move_engine))

                # my_thread = threading.Thread(target=analysis_engine)
                # my_thread.daemon = True
                # if my_thread.is_alive() is True:
                    # my_thread.join()
                # my_thread.start()

                # Clocks
                # print(self.update_remainingtime_h)
                if self.update_remainingtime_h == 0:
                    self.time_5min_clock_h.start(300000)
                    self.time_clockh_stop = False
                    self.clock_started = True
                if self.update_remainingtime_h != 0:
                    self.time_5min_clock_h.start(self.update_remainingtime_h)
                    self.time_clockh_stop = False
                self.update_remainingtime_h = self.time_5min_clock_h.remainingTime()
                self.update_remainingtime_c = self.time_5min_clock.remainingTime()

                t2 = time.time()
                print(f'{t2 - t1} time')
                engine.quit()
                self.time_analysis.start(100)
                # self.engine_analysis()
                self.stop_clock()
                if self.board.is_game_over():
                    QMessageBox.information(self, 'Game Over', 'The game is over')
                    # print('Game Over')

            # Show Analysis

            if self.text_list:
                text = random.choice(self.text_list)
                self.label_4.setText("{}".format(str(text)))

    def show_time(self):

        text_c = self.time_5min_clock.remainingTime()
        text_h = self.time_5min_clock_h.remainingTime()
        self.lcdNumber_3.setNumDigits(8)
        self.lcdNumber.setNumDigits(8)
        if self.time_clockh_stop is True:
            text_h = self.update_remainingtime_h
        if self.time_clockc_stop is True:
            text_c = self.update_remainingtime_c
        text_c = str(text_c)
        text_h = str(text_h)

        minutes = str(int(text_c) // 60000)
        seconds = str((int(text_c) % 60000)//1000)
        miliseconds = str(int(text_c) % 60000)
        text_c = minutes + ':' + seconds + ':' + miliseconds[2:4]

        minutes_h = str(int(text_h) // 60000)
        seconds_h = str((int(text_h) % 60000) // 1000)
        miliseconds_h = str(int(text_h) % 60000)
        text_h = minutes_h + ':' + seconds_h + ':' + miliseconds_h[2:4]

        if self.update_remainingtime_h == 0:
            text_h = '5:00:00'
        if self.update_remainingtime_c == 0:
            text_c = '5:00:00'
        if self.board.is_game_over():
            self.stop_clock()
            self.stop_clock_human()

        self.lcdNumber_3.display(str(text_c))
        self.lcdNumber.display(str(text_h))

    def stop_clock(self):
        self.time_5min_clock.stop()
        self.time_clockc_stop = True

    def stop_clock_human(self):
        self.time_5min_clock_h.stop()
        self.time_clockh_stop = True

    # Analysis
    def engine_analysis(self):
        limit = Limit(time=0.2, depth=self.depth[0])
        root = QFileInfo(__file__).absolutePath()
        location = root + '/Stockfish-NNUE/sf-nnue-avx2.exe'
        if self.url:
            if self.url[0] != "":
                location = self.url[0]
                print(location, 'location', type(location))
        print('error')
        engine = SimpleEngine.popen_uci(location)
        self.time_analysis.stop()
        with engine.analysis(self.board, multipv=4, limit=limit) as analysis:
            self.text_list = []
            for info in analysis:
                # print(info.get("score"), info.get("pv"))
                data_collect = []
                if info.get("pv") is not None:
                    # print(len(info.get("pv")))
                    if len(info.get("pv")) > 6:
                        for data in info.get("pv"):
                            data = str(data)
                            data_collect.append(data)
                if data_collect:
                    text_variation = self.board.variation_san([Move.from_uci(m) for m in data_collect])
                    text_score = str(info.get("score"))
                    self.text_list.append(str(text_variation) + "  Score  " + text_score)

                # Arbitrary stop condition.
                if info.get("seldepth", 0) > 20:
                    break
                if info.get("pv") is None:
                    break
        engine.quit()


app = QApplication(sys.argv)
main = MainWindow()
app.setWindowIcon(QIcon("icon.ico"))
app.setStyle('Fusion')
splash_image = QPixmap("Tul.jpg")
splash = QSplashScreen(splash_image)
splash.show()
time.sleep(2)
main.show()
splash.finish(main)
# app.exec_()
# pyinstaller -D -F -n Youtube -w -i "C:\Youtube\favicon.ico" youtube.py
# pyuic5.exe youtube.ui -o youtube_ui.py
# pyrcc5.exe C:\Youtube\iconos\icons.qrc -o icons_rc.py
# pyuic5.exe example.ui -o example_ui.py
sys.exit(app.exec_())
