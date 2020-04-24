# main menu

import sys
from PyQt5.QtWidgets import QGroupBox, QApplication, QLabel, QWidget, QStackedWidget, QGridLayout, \
    QLineEdit, QPushButton, QVBoxLayout, QBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QCoreApplication
from random import choice


class WordBook(QWidget):

    def __init__(self):
        super().__init__()
        word_file = open('word_list.csv', 'a', encoding='utf-8')
        word_file.close()
        with open('word_list.csv', 'r', encoding='utf-8') as word_file:
            self.word_data = word_file.readlines()
        self.stacked_widget = QStackedWidget()
        self.mean = ''
        self.test_word = QLabel()
        self.edit_table = QTableWidget(self)
        self.init_book()

    # main menu has add button, test button, edit button, exit button
    # add button : add words in the book
    # test button : word test with word in the book
    # edit button : delete or change word in the book
    # exit button : exit
    def init_book(self):
        ### main menu layout
        main_vbox = QVBoxLayout()
        main_box = QBoxLayout(QBoxLayout.LeftToRight)

        app_name_lbl = QLabel('Word Book', self)
        app_name_lbl.setAlignment(Qt.AlignCenter)
        app_name_lbl_font = app_name_lbl.font()
        app_name_lbl_font.setBold(True)
        app_name_lbl_font.setPointSize(20)
        app_name_lbl.setFont(app_name_lbl_font)

        add_btn = QPushButton('&Add', self)
        test_btn = QPushButton('&Test', self)
        edit_btn = QPushButton('&Edit', self)
        exit_btn = QPushButton('E&xit', self)

        main_vbox.addStretch(1)
        main_vbox.addWidget(app_name_lbl)
        main_vbox.addStretch(1)
        main_vbox.addWidget(add_btn)
        main_vbox.addWidget(test_btn)
        main_vbox.addWidget(edit_btn)
        main_vbox.addWidget(exit_btn)
        main_vbox.addStretch(1)

        main_box.addStretch(1)
        main_box.addLayout(main_vbox)
        main_box.addStretch(1)

        main_layout = QGroupBox()
        main_layout.setLayout(main_box)

        ### add menu layout
        add_grid = QGridLayout()
        add_grid.addWidget(QLabel('Word: '), 0, 0)
        add_grid.addWidget(QLabel('Meaning: '), 1, 0)
        added_word = QLineEdit()
        add_grid.addWidget(added_word, 0, 1)
        added_mean = QLineEdit()
        add_grid.addWidget(added_mean, 1, 1)

        add_back_btn = QPushButton('back')
        add_grid.addWidget(add_back_btn, 2, 1)
        add_store_btn = QPushButton('store')
        add_grid.addWidget(add_store_btn, 2, 0)

        add_layout = QGroupBox()
        add_layout.setLayout(add_grid)

        ### test menu layout
        test_grid = QGridLayout()

        test_grid.addWidget(self.test_word, 0, 0)
        test_answer = QLineEdit()
        test_grid.addWidget(test_answer, 0, 1)

        test_back_btn = QPushButton('back')
        test_grid.addWidget(test_back_btn, 1, 1)
        # submit answer
        test_submit_btn = QPushButton('submit')
        test_grid.addWidget(test_submit_btn, 1, 0)

        test_layout = QGroupBox()
        test_layout.setLayout(test_grid)

        ### edit menu layout
        edit_box = QBoxLayout(QBoxLayout.TopToBottom)
        edit_box.addWidget(self.edit_table)
        edit_back_btn = QPushButton('back')
        edit_box.addWidget(edit_back_btn)

        edit_layout = QGroupBox()
        edit_layout.setLayout(edit_box)

        # all layout stacked in stacked widget and set layout
        self.stacked_widget.addWidget(main_layout)
        self.stacked_widget.addWidget(add_layout)
        self.stacked_widget.addWidget(test_layout)
        self.stacked_widget.addWidget(edit_layout)

        widget_layout = QBoxLayout(QBoxLayout.LeftToRight)
        widget_layout.addWidget(self.stacked_widget)

        self.setLayout(widget_layout)

        add_btn.clicked.connect(self.add_ui)
        test_btn.clicked.connect(self.test_ui)
        edit_btn.clicked.connect(self.edit_ui)
        exit_btn.clicked.connect(QCoreApplication.instance().quit)
        add_back_btn.clicked.connect(self.main_ui)
        add_store_btn.clicked.connect(lambda: self.add_word(added_word.text() + ',' + added_mean.text()))
        test_back_btn.clicked.connect(self.main_ui)
        test_submit_btn.clicked.connect(lambda: self.confirm_answer(test_answer.text(), self.mean))
        edit_back_btn.clicked.connect(self.main_ui)
        self.edit_table.itemChanged.connect(self.edit_word_set)

        self.setWindowTitle('Word Book')
        self.setGeometry(300, 300, 350, 300)

    def main_ui(self):
        self.stacked_widget.setCurrentIndex(0)

    def add_ui(self):
        self.stacked_widget.setCurrentIndex(1)

    def test_ui(self):
        # read all word sets and choice one word set
        word_sets = self.word_data

        word_set = choice(word_sets)

        # separate word and mean in word set
        word_set = word_set[:-1]
        word, self.mean = word_set.split(',')
        self.test_word.setText(word)

        self.stacked_widget.setCurrentIndex(2)

    def edit_ui(self):
        number_of_word_sets = len(self.word_data)
        self.edit_table.setRowCount(number_of_word_sets)
        self.edit_table.setColumnCount(2)

        words = []
        means = []
        # separate word and mean in word set
        for word_set in self.word_data:
            word_set = word_set[:-1]   # del \n
            word, mean = word_set.split(',')
            words.append(word)
            means.append(mean)
        # set words and means on the table
        i = 0
        for word in words:
            self.edit_table.setItem(i, 0, QTableWidgetItem(word))
            i += 1

        i = 0
        for mean in means:
            self.edit_table.setItem(i, 1, QTableWidgetItem(mean))
            i += 1

        self.stacked_widget.setCurrentIndex(3)

    def confirm_answer(self, input_answer, correct_answer):
        if input_answer == correct_answer:
            QMessageBox.about(self, 'message', 'correct')
        else:
            QMessageBox.about(self, 'message', 'wrong')

    def add_word(self, word_set):
        self.word_data.append(word_set + '\n')
        with open('word_list.csv', 'w', encoding='utf-8') as word_file:
            for word_set in self.word_data:
                word_file.write(word_set)

    def edit_word_set(self, item):
        change_row = item.row()
        word, mean = self.word_data[change_row].split(',')
        if item.column() == 0:
            self.word_data[change_row] = self.word_data[change_row].replace(word, item.text())
        else:
            self.word_data[change_row] = self.word_data[change_row].replace(mean, item.text() + '\n')
        with open('word_list.csv', 'w', encoding='utf-8') as word_file:
            for word_set in self.word_data:
                word_file.write(word_set)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WordBook()
    ex.show()
    sys.exit(app.exec_())
