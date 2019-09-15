from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, QPushButton, QGridLayout, QGroupBox, QTableWidget, QTableWidgetItem,
                             QVBoxLayout, QLayout, QStackedLayout, QWidget, QTextEdit,QLineEdit, QLabel,QHBoxLayout, QMessageBox, QAbstractItemView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database_class import Database




class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.set_UI()

        self.set_welcome_layout()

        self.db = Database()

        self.description_dict = {}

        self.code_dict = {}

        self.title = ""

        self.language = ""


    def set_UI(self):

        self.setWindowTitle("LearningStep")

        self.setGeometry(230,100,900,500)

        self.set_upper_menu()

        self.create_main_layout()


        self.stacked_layout =QStackedLayout()
        self.stacked_layout.addWidget(self.main_widget)



        ##############

        self.create_record_task_menu_layout()
        self.stacked_layout.addWidget(self.record_task_widget)

        #######

        self.create_play_task_menu_layout()
        self.stacked_layout.addWidget(self.play_task_widget)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)

    def create_main_layout(self):

        ### WIDGETS

        self.display_description = QLineEdit()
        self.display_code = QTextEdit()
        self.display_title = QLabel('Title')
        self.display_step = QLabel('Steps')
        self.finish_button = QPushButton('Finish')
        self.next_button = QPushButton('Next')


        ### GRIDS

        self.main_grid = QGridLayout()
        self.right_grid = QGridLayout()





        ### ADD WIDGETS

        self.right_grid.addWidget(self.display_step,0,0)
        self.right_grid.addWidget(self.finish_button, 1, 0)
        self.right_grid.addWidget(self.next_button, 2, 0)


        self.main_grid.addWidget(self.display_description,0,0)
        self.main_grid.addWidget(self.display_code,1,0)
        self.main_grid.addWidget(self.display_title,0,1)
        self.main_grid.addItem(self.right_grid,1,1)


        ### LAYOUT FORMATION
        font = QFont('Arial', 12)
        font.setBold(True)

        self.display_description.setMaximumWidth(600)
        self.display_description.setAlignment(Qt.AlignHCenter)


        self.display_code.setMaximumWidth(600)
        self.display_code.setMinimumWidth(600)
        self.display_code.setMaximumHeight(500)




        self.display_title.setFont(font)
        self.display_title.setAlignment(Qt.AlignHCenter)

        self.display_step.setAlignment(Qt.AlignCenter)
        self.display_step.setFont(font)

        self.finish_button.setMinimumHeight(60)
        self.next_button.setMinimumHeight(60)


        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_grid)

        #### BEHAVIOURS ####

        self.finish_button.clicked.connect(self.finish_button_method)
        self.next_button.clicked.connect(self.next_button_method)


    def create_record_task_menu_layout(self):



        self.record_task_grid = QVBoxLayout()
        self.record_task_grid_h = QHBoxLayout()

        self.record_label_1 = QLabel('Provide the title of the task:')
        self.record_label_2 = QLabel('Provide field of the task:')

        self.record_text_title = QLineEdit()
        self.record_text_language = QLineEdit()

        self.record_button_cancel = QPushButton('Cancel')
        self.record_button_start = QPushButton('Start')




        self.record_task_grid.addWidget(self.record_text_title)
        self.record_task_grid.addWidget(self.record_label_2)
        self.record_task_grid.addWidget(self.record_text_language)

        self.record_task_grid_h.addWidget(self.record_button_cancel)
        self.record_task_grid_h.addWidget(self.record_button_start)

        self.record_task_grid.addItem(self.record_task_grid_h)

        self.record_task_widget = QWidget()
        self.record_task_widget.setLayout(self.record_task_grid)

        #### BEHAVIOUR ####

        self.record_button_cancel.clicked.connect(self.cancel_record_task_method)

        self.record_button_start.clicked.connect(self.start_record_task_method)

    def create_play_task_menu_layout(self):





        #### WIDGETS ####

        self.play_label_1 = QLabel('CHOOSE ONE OF AVAILABLE TASKS:')

        self.play_task_button = QPushButton('Play Selected Task')

        self.play_task_cancel_button = QPushButton('Cancel')

        # Table

        self.play_table = QTableWidget()


        #### GRIDS ####

        self.play_task_grid = QVBoxLayout()

        self.play_task_grid.addWidget(self.play_label_1)

        self.play_task_grid.addWidget(self.play_table)

        self.play_task_grid.addWidget(self.play_task_button)

        self.play_task_grid.addWidget(self.play_task_cancel_button)



        self.play_task_widget = QWidget()

        self.play_task_widget.setLayout(self.play_task_grid)

        #### BEHAVIOUR ####

        self.play_task_cancel_button.clicked.connect(self.cancel_record_task_method)



    def load_to_play_table(self):

        rows = self.db.load_available_tasks()
        self.play_table.setRowCount(len(rows))
        self.play_table.setColumnCount(6)
        self.play_table.setHorizontalHeaderLabels(['Task title (short description)', 'Language', 'Creation Date', 'Last Pass Date', 'Pass Count', 'ID'])
        self.play_table.verticalHeader().hide()
        self.play_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.play_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        for i, row in enumerate(rows):

            self.play_table.setItem(i,0,QTableWidgetItem(row[0]))
            self.play_table.setItem(i, 1, QTableWidgetItem(row[1]))
            self.play_table.setItem(i, 2, QTableWidgetItem(row[2]))
            self.play_table.setItem(i, 3, QTableWidgetItem(row[3]))
            self.play_table.setItem(i, 4, QTableWidgetItem(str(row[4])))
            self.play_table.setItem(i, 5, QTableWidgetItem(str(row[5])))



    def set_upper_menu(self):


        self.statusBar()

        mainMenu = self.menuBar()

        optionsMenu = mainMenu.addMenu('&Menu')

        menuRecord = QAction('&Record New Task',self)
        menuRecord.setStatusTip('Record New Task and save it into database...')
        menuRecord.triggered.connect(self.menuRecord_method)

        menuPlay = QAction('&Play The Task',self)
        menuPlay.setStatusTip('Play one of the tasks from the available...')
        menuPlay.triggered.connect(self.menuPlay_method)


        menuAbout = QAction('&About',self)
        menuAbout.setStatusTip('About the LearningStep app...')

        menuExit = QAction("&Exit", self)
        menuExit.setStatusTip('Exit the application...')


        optionsMenu.addAction(menuRecord)
        optionsMenu.addAction(menuPlay)
        optionsMenu.addAction(menuAbout)
        optionsMenu.addAction(menuExit)



    ################################







    #### BEHAVIOUR METHODS ####


    def finish_button_method(self):

        #### RECORD TASK ####

        if self.step == 1 and self.display_description.text() == "" and self.display_code.toPlainText() == "":

            self.set_welcome_layout()

            return

        choice = QMessageBox.question(self, "Finish", 'Yes - Finish and save task to the database\nNo - Finish and don\'t save task\nCancel - back to the recording',
                             QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)


        if choice == QMessageBox.Yes:

            self.description_dict[self.step] = self.display_description.text()

            self.code_dict[self.step] = self.display_code.toPlainText()

            self.db.add_task(self.description_dict,self.code_dict,self.title,self.language)

            self.set_welcome_layout()

        elif choice == QMessageBox.No:

            self.set_welcome_layout()

        elif choice == QMessageBox.Cancel:


            return

    def next_button_method(self):

        #### RECORD TASK ####

        # check if fields are not empty

        if self.display_description.text() == "":

            QMessageBox.information(self,'Empty field!','There is empty description field. Please write something to proceed.')

            return

        if self.display_code.toPlainText() == "":

            QMessageBox.information(self, 'Empty field!', 'There is empty code field. Please write something to proceed.')

            return



        choice = QMessageBox.question(self, 'Next step', 'Do you want to proceed to the next step?',
                                      QMessageBox.Yes | QMessageBox.No)

        if choice == QMessageBox.Yes:

            # add to dictionaries

            self.description_dict[self.step] = self.display_description.text()

            self.code_dict[self.step] = self.display_code.toPlainText()




            self.step += 1

            self.display_step.setText("Step\n{0}".format(self.step))

            self.display_description.clear()

            self.display_code.clear()

        else:

            return


    def menuRecord_method(self):

        self.clear_record_menu()

        self.stacked_layout.setCurrentIndex(1)

    def menuPlay_method(self):

        self.play_table.clear()

        self.load_to_play_table()

        self.stacked_layout.setCurrentIndex(2)


    def cancel_record_task_method(self):

        self.clear_record_menu()

        self.stacked_layout.setCurrentIndex(0)


    def start_record_task_method(self):

        if self.record_text_title.text() == "" or self.record_text_language.text() == "":


            QMessageBox.information(self,'Warning!','Title and field has to be fulfilled!')

        else:

            self.title = self.record_text_title.text()

            self.language = self.record_text_language.text()

            self.set_record_layout()

            self.stacked_layout.setCurrentIndex(0)



    def clear_record_menu(self):

        self.record_text_title.setText('')
        self.record_text_language.setText('')

    def set_welcome_layout(self):

        self.display_description.setDisabled(True)
        self.display_code.setDisabled(True)
        self.display_title.setText('Title')
        self.display_step.setText('Step\n/')

        self.finish_button.setDisabled(True)
        self.next_button.setDisabled(True)

        self.description_dict = {}
        self.code_dict = {}

        self.title = ""
        self.language = ""

    def set_record_layout(self):

        self.step = 1
        self.display_description.setEnabled(True)
        self.display_code.setEnabled(True)
        self.display_title.setText(self.record_text_title.text().capitalize())
        self.display_step.setText('Step\n{0}'.format(self.step))
        self.display_description.clear()
        self.display_code.clear()
        self.finish_button.setEnabled(True)
        self.next_button.setEnabled(True)

if __name__ == '__main__':

    app = QApplication([])
    window = MainWindow()
    window.show()
    window.raise_()
    app.exec_()
