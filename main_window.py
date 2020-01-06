from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, QPushButton, QGroupBox, QTableWidget, QTableWidgetItem, QComboBox, QGridLayout,
                             QVBoxLayout, QStackedLayout, QWidget, QTextEdit, QLineEdit, QLabel, QHBoxLayout, QMessageBox, QAbstractItemView,
                             QFileDialog)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap
from database_class import Database
import time
import os
from functools import partial
import datetime
import shutil
import sys




class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()

        self.universal_font = QFont('Calibri', 13)

        self.set_UI()

        self.set_welcome_layout()

        self.db = Database()

        self.description_dict = {}

        self.code_dict = {}

        self.picture_dict = {}

        self.title = ""

        self.language = ""

        self.record_or_play = True # record is True, play is False

        self.about_dict = {1:'LearningStep\n\nThis application is named LearningStep. The purpose is to learn and repeat self made text-lessons in intervals of time.',
                           2:'Record New Task\n\nConstruct your own lesson in steps.\nProvide title as short description, choose language (field of interests) and by clicking next move forward lessons.'
                             '\nOne step consists of description (upper text field) and code (lower text field).\nYou can also attach an image to every step.'
                             '\nTo proceed next step, click Next button.\nWhen all steps are written, click Finish button to save the lesson.',
                           3:'Play The Task\n\nPlay previously recorded task (choose from the table of available tasks).\nGo through all tasks by clicking Next button.\nAt first you see description and then code field.\n'
                             'When you will walk through all steps you can decide whether this approach was satisfying. Only if so, task will be completed,\n updated to database '
                             'and reminded after certain interval of time.',
                           4:'Delete Task\n\nDelete task according to provided task ID.\nBe aware that images stored in database will also be deleted.',
                           5:'Time intervals are:\n\n1 day, 3 days, 7 days, 10 days, 14 days, 28 days, 60 days, 90 days, 180 days...',
                           6:'Credits:\n\nDariusz Giemza, 2019',
                           7:''}




    def set_UI(self):
        """Set main window properties and create stacked layouts"""
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



        ########

        self.create_delete_task_menu_layout()
        self.stacked_layout.addWidget(self.delete_task_widget)

        ########

        self.create_about_menu_layout()
        self.stacked_layout.addWidget(self.about_widget)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)

    def create_main_layout(self):
        """Create startin layouy"""
        ### WIDGETS

        self.display_description = QLineEdit()
        self.display_code = QTextEdit()
        self.display_title = QLabel('Title')
        self.display_step = QLabel('Steps')
        self.picture_button = QPushButton()
        self.finish_button = QPushButton('Finish')
        self.next_button = QPushButton('Next')

        self.alpha_button = QPushButton('α')
        self.beta_button = QPushButton('β')
        self.pi_button = QPushButton('π')
        self.omega_button = QPushButton('Ω')
        self.lambda_button = QPushButton('λ')
        self.mi_button = QPushButton('µ')
        self.sigma_button = QPushButton('σ')
        self.sum_button = QPushButton('Σ')
        self.delta_button = QPushButton('Δ')
        self.gamma_button = QPushButton('Γ')
        self.not_equal_button = QPushButton('≠')
        self.approx_equal_button = QPushButton('≈')
        self.sqrt_button = QPushButton('√')
        self.gt_button = QPushButton('≥')
        self.lt_button = QPushButton('≤')
        self.degree_button = QPushButton('°')



        icon = QIcon('imgs/picture.png')
        self.picture_button.setIcon(icon)

        ### GRIDS

        self.main_grid = QGridLayout()
        self.right_grid = QGridLayout()
        self.symbols_grid = QGridLayout()

        ### ADD WIDGETS

        self.symbols_grid.addWidget(self.alpha_button,0,0)
        self.symbols_grid.addWidget(self.beta_button,0,1)
        self.symbols_grid.addWidget(self.pi_button, 0, 2)
        self.symbols_grid.addWidget(self.omega_button, 0, 3)
        self.symbols_grid.addWidget(self.lambda_button, 0, 4)
        self.symbols_grid.addWidget(self.mi_button, 0, 5)
        self.symbols_grid.addWidget(self.sigma_button, 0, 6)
        self.symbols_grid.addWidget(self.sum_button, 0, 7)
        self.symbols_grid.addWidget(self.delta_button,1,0)
        self.symbols_grid.addWidget(self.gamma_button,1,1)
        self.symbols_grid.addWidget(self.not_equal_button,1,2)
        self.symbols_grid.addWidget(self.approx_equal_button, 1, 3)
        self.symbols_grid.addWidget(self.sqrt_button, 1, 4)
        self.symbols_grid.addWidget(self.gt_button,1,5)
        self.symbols_grid.addWidget(self.lt_button,1,6)
        self.symbols_grid.addWidget(self.degree_button,1,7)


        self.right_grid.addWidget(self.display_step,0,0)
        self.right_grid.addWidget(self.picture_button,1,0)
        self.right_grid.addWidget(self.finish_button, 2, 0)
        self.right_grid.addWidget(self.next_button, 3, 0)



        self.main_grid.addItem(self.symbols_grid,2,0)
        self.main_grid.addWidget(self.display_description,0,0)
        self.main_grid.addWidget(self.display_code,1,0)
        self.main_grid.addWidget(self.display_title,0,1)
        self.main_grid.addItem(self.right_grid,1,1)


        ### LAYOUT FORMATION
        font = QFont('Calibri', 15)
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
        self.picture_button.clicked.connect(self.picture_button_method)

        self.alpha_button.clicked.connect(self.alpha_button_method)
        self.beta_button.clicked.connect(self.beta_button_method)
        self.pi_button.clicked.connect(self.pi_button_method)
        self.omega_button.clicked.connect(self.omega_button_method)
        self.lambda_button.clicked.connect(self.lambda_button_method)
        self.mi_button.clicked.connect(self.mi_button_method)
        self.sigma_button.clicked.connect(self.sigma_button_method)
        self.sum_button.clicked.connect(self.sum_button_method)
        self.delta_button.clicked.connect(self.delta_button_method)
        self.gamma_button.clicked.connect(self.gamma_button_method)
        self.not_equal_button.clicked.connect(self.not_equal_button_method)
        self.approx_equal_button.clicked.connect(self.approx_equal_button_method)
        self.sqrt_button.clicked.connect(self.sqrt_button_method)
        self.gt_button.clicked.connect(self.gt_button_method)
        self.lt_button.clicked.connect(self.lt_button_method)
        self.degree_button.clicked.connect(self.degree_button_method)



    #### SPECIAL SYMBOLS METHODS ####

    def alpha_button_method(self):

        text = self.display_code.toPlainText()
        self.display_code.setText(text + 'α')


    def beta_button_method(self):

        text = self.display_code.toPlainText()
        self.display_code.setText(text + 'β')


    def pi_button_method(self):

        text = self.display_code.toPlainText()
        self.display_code.setText(text + 'π')


    def omega_button_method(self):

        text = self.display_code.toPlainText()
        self.display_code.setText(text + 'Ω')


    def lambda_button_method(self):

        text = self.display_code.toPlainText()
        self.display_code.setText(text + 'λ')


    def mi_button_method(self):

        text = self.display_code.toPlainText()
        self.display_code.setText(text + 'µ')


    def sigma_button_method(self):

        text = self.display_code.toPlainText()
        self.display_code.setText(text + 'σ')


    def sum_button_method(self):

        text = self.display_code.toPlainText()
        self.display_code.setText(text + 'Σ')


    def delta_button_method(self):

        text = self.display_code.toPlainText()
        self.display_code.setText(text + 'Δ')



    def gamma_button_method(self):

        text = self.display_code.toPlainText()
        self.display_code.setText(text + 'Γ')


    def not_equal_button_method(self):

        text = self.display_code.toPlainText()
        self.display_code.setText(text + '≠')


    def approx_equal_button_method(self):

        text = self.display_code.toPlainText()
        self.display_code.setText(text + '≈')


    def sqrt_button_method(self):

        text = self.display_code.toPlainText()
        self.display_code.setText(text + '√')


    def gt_button_method(self):

        text = self.display_code.toPlainText()
        self.display_code.setText(text + '≥')


    def lt_button_method(self):

        text = self.display_code.toPlainText()
        self.display_code.setText(text + '≤')


    def degree_button_method(self):

        text = self.display_code.toPlainText()
        self.display_code.setText(text + '°')




    def create_record_task_menu_layout(self):
        """Create layout for recording new taks"""

        self.record_task_grid = QVBoxLayout()

        self.record_task_grid_h = QHBoxLayout()

        self.record_label_1 = QLabel('TITLE OF THE TASK:')
        self.record_label_2 = QLabel('LANGUAGE (FIELD):')

        self.record_label_1.setAlignment(Qt.AlignCenter)

        self.record_text_title = QLineEdit()
        self.record_text_title.setAlignment(Qt.AlignHCenter)

        self.record_combo_box = QComboBox()
        self.record_combo_box.addItem("---")
        self.record_combo_box.addItem("Python")
        self.record_combo_box.addItem("R")
        self.record_combo_box.addItem("Machine Learning")
        self.record_combo_box.addItem("Deep Learning")
        self.record_combo_box.addItem("Statistics")
        self.record_combo_box.addItem("English")


        self.record_button_cancel = QPushButton('Cancel')
        self.record_button_start = QPushButton('Start')


        #### ALIGNMENT, SHAPES AND FONT####

        self.record_label_1.setFont(self.universal_font)
        self.record_label_2.setFont(self.universal_font)

        self.record_label_1.setAlignment(Qt.AlignCenter)
        self.record_text_title.setMaximumWidth(250)
        self.record_text_title.setMinimumWidth(350)

        self.record_label_2.setAlignment(Qt.AlignCenter)
        self.record_combo_box.setMaximumWidth(350)
        self.record_combo_box.setMinimumWidth(200)

        self.record_combo_box.setMinimumHeight(30)

        self.record_button_cancel.setMinimumHeight(40)
        self.record_button_start.setMinimumHeight(40)

        #### GRIDS ####


        self.record_task_grid.addWidget(self.record_label_1)
        self.record_task_grid.addWidget(self.record_text_title, alignment=Qt.AlignHCenter)
        self.record_task_grid.addWidget(self.record_label_2)
        self.record_task_grid.addWidget(self.record_combo_box, alignment=Qt.AlignCenter | Qt.AlignTop)

        self.record_task_grid_h.addWidget(self.record_button_cancel)
        self.record_task_grid_h.addWidget(self.record_button_start)

        self.record_task_grid.addItem(self.record_task_grid_h)

        self.record_task_widget = QWidget()
        self.record_task_widget.setLayout(self.record_task_grid)

        #### BEHAVIOUR ####

        self.record_button_cancel.clicked.connect(self.cancel_task_method)

        self.record_button_start.clicked.connect(self.start_record_task_method)

    def create_play_task_menu_layout(self):
        """Create play task layout"""

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


        #### ALIGNMENT, FONTS AND SHAPES ####

        self.play_label_1.setFont(self.universal_font)

        self.play_task_button.setMinimumHeight(40)

        self.play_task_cancel_button.setMinimumHeight(40)


        ####

        self.play_task_widget = QWidget()

        self.play_task_widget.setLayout(self.play_task_grid)



        #### BEHAVIOUR ####

        self.play_task_cancel_button.clicked.connect(self.cancel_task_method)

        self.play_task_button.clicked.connect(self.play_task_method)

    def create_delete_task_menu_layout(self):
        """Create delete layout"""

        #### WIDGETS ####


        self.delete_task_label = QLabel('PROVIDE TASK ID TO DELETE TASK:')

        self.delete_task_text_box = QLineEdit()

        self.delete_task_delete_button = QPushButton('DELETE')

        self.delete_task_cancel_button = QPushButton('Cancel')


        #### GRIDS ####

        self.delete_task_grid = QVBoxLayout()

        self.delete_task_grid_h = QHBoxLayout()


        self.delete_task_grid_h.addWidget(self.delete_task_cancel_button)

        self.delete_task_grid_h.addWidget(self.delete_task_delete_button)


        self.delete_task_grid.addWidget(self.delete_task_label, alignment=Qt.AlignCenter )

        self.delete_task_grid.addWidget(self.delete_task_text_box, alignment=Qt.AlignTop | Qt.AlignCenter)

        self.delete_task_grid.addItem(self.delete_task_grid_h)


        #### ALIGNMENT, FONT AND SHAPES ####

        self.delete_task_text_box.setAlignment(Qt.AlignHCenter)

        self.delete_task_label.setFont(self.universal_font)

        self.delete_task_text_box.setMaximumWidth(200)

        self.delete_task_cancel_button.setMinimumHeight(40)

        self.delete_task_delete_button.setMinimumHeight(40)

        #####


        self.delete_task_widget = QWidget()

        self.delete_task_widget.setLayout(self.delete_task_grid)

        #### BEHAVIOUR ####

        self.delete_task_cancel_button.clicked.connect(self.cancel_task_method)

        self.delete_task_delete_button.clicked.connect(self.delete_task)

    def create_about_menu_layout(self):
        """Create about layout"""

        self.about_label = QLabel('Sample')

        self.about_next_button = QPushButton('Next')

        self.about_cancel_button = QPushButton('Cancel')


        #### GRID ####

        self.about_grid_H = QHBoxLayout()

        self.about_grid_H.addWidget(self.about_cancel_button)

        self.about_grid_H.addWidget(self.about_next_button)

        self.about_grid_V = QVBoxLayout()

        self.about_grid_V.addWidget(self.about_label)

        self.about_grid_V.addItem(self.about_grid_H)

        self.about_widget = QWidget()

        self.about_widget.setLayout(self.about_grid_V)


        self.about_label.setFont(self.universal_font)

        self.about_label.setAlignment(Qt.AlignHCenter)


        self.about_cancel_button.setMinimumHeight(40)

        self.about_next_button.setMinimumHeight(40)


        #### BEHAVIOUR ####

        self.about_cancel_button.clicked.connect(self.cancel_task_method)

        self.about_next_button.clicked.connect(self.about_next_method)

    def set_upper_menu(self):
        """Create rolling  Menu"""

        self.statusBar()

        mainMenu = self.menuBar()

        optionsMenu = mainMenu.addMenu('&Menu')

        menuRecord = QAction('&Record New Task',self)
        menuRecord.setStatusTip('Record New Task and save it into database...')
        menuRecord.triggered.connect(self.menuRecord_method)

        menuPlay = QAction('&Play The Task',self)
        menuPlay.setStatusTip('Play one of the tasks from the available...')
        menuPlay.triggered.connect(self.menuPlay_method)


        menuDelete = QAction('&Delete task',self)
        menuDelete.setStatusTip('Delete one task for given task ID...')
        menuDelete.triggered.connect(self.menuDelete_method)


        menuAbout = QAction('&About',self)
        menuAbout.setStatusTip('About the LearningStep app...')
        menuAbout.triggered.connect(self.menuAbout_method)

        menuExit = QAction("&Exit", self)
        menuExit.setStatusTip('Exit the application...')
        menuExit.triggered.connect(self.menuExit_method)


        optionsMenu.addAction(menuRecord)
        optionsMenu.addAction(menuPlay)
        optionsMenu.addAction(menuDelete)
        optionsMenu.addAction(menuAbout)
        optionsMenu.addAction(menuExit)

    def about_next_method(self):
        """About layout, Next button"""

        if self.about_step < 7:
            self.about_step +=1
        else:
            self.about_step = 1

        self.about_label.setText(self.about_dict[self.about_step])

    def delete_task(self):
        """Delete layout, Delete button"""

        try:
            task_id = int(self.delete_task_text_box.text())

        except:

            task_id = self.delete_task_text_box.text()

        if self.delete_task_text_box.text() == "":

            QMessageBox.information(self, 'Empty text box', 'In order to delete task, please provide a valid task ID!')

            return

        if not self.delete_task_text_box.text().isnumeric():

            QMessageBox.information(self, 'Invalid input', 'In order to delete task, please provide numeric value that corresponds to task ID!')

            return

        if not self.db.check_if_task_id_exists(task_id):

            QMessageBox.information(self, 'No such task ID', 'There is no task ID in database: {0}'.format(task_id))

            return

        choice = QMessageBox.question(self, "Delete task", 'Are you sure to delete task and all dependend images?\nYou will not be able to restore deleted data. Task ID: {0}'.format(task_id),
                                      QMessageBox.Yes | QMessageBox.No)


        if choice == QMessageBox.Yes:

            self.title, self.description_dict, self.code_dict, self.picture_dict, self.pass_count = self.db.get_selected_task(task_id)

            self.db.delete_images(self.picture_dict)

            self.db.delete_task(task_id)

            QMessageBox.information(self, 'Task deleted', 'Task with ID {0} has been successfully deleted from database!'.format(task_id))

            self.stacked_layout.setCurrentIndex(0)

            self.set_welcome_layout()

        elif choice == QMessageBox.No:

            return


    def load_to_play_table(self):
        """Load table with available tasks"""

        rows = self.db.load_available_tasks()

        self.play_table.setRowCount(len(rows))

        self.play_table.setColumnCount(6)

        self.play_table.setHorizontalHeaderLabels(['Task title (short description)', 'Language (Field)', 'Creation Date', 'Last Pass Date', 'Pass Count', 'ID'])

        self.play_table.verticalHeader().hide()

        self.play_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.play_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.play_table.setColumnWidth(0, 280)

        self.play_table.setColumnWidth(1, 180)

        self.play_table.setColumnWidth(2, 110)

        self.play_table.setColumnWidth(3, 110)


        for i, row in enumerate(rows):

            item = QTableWidgetItem(row[0])
            item.setTextAlignment(Qt.AlignCenter)
            self.play_table.setItem(i,0,item)

            item = QTableWidgetItem(row[1])
            item.setTextAlignment(Qt.AlignCenter)
            self.play_table.setItem(i, 1, item)

            item = QTableWidgetItem(row[2])
            item.setTextAlignment(Qt.AlignCenter)
            self.play_table.setItem(i, 2, item)

            item = QTableWidgetItem(row[3])
            item.setTextAlignment(Qt.AlignCenter)
            self.play_table.setItem(i, 3, item)

            item = QTableWidgetItem(str(row[4]))
            item.setTextAlignment(Qt.AlignCenter)
            self.play_table.setItem(i, 4, item)

            item = QTableWidgetItem(str(row[5]))
            item.setTextAlignment(Qt.AlignCenter)
            self.play_table.setItem(i, 5, item)

    def picture_button_method(self):
        """Picture button to load or display picture"""

        if self.record_or_play:

            #### RECORD TASK ####



            path = QFileDialog.getOpenFileName(self, 'Load picture to database','c:\\',"Image files (*.jpg *.gif, *.png)")

            # if path is empty
            if path[0] == '':

                return

            try:

                extension = path[0][-3:].lower()

                now = datetime.datetime.now()

                image_name = self.title + "_STEP_" + str(self.step) + "_" + str(now.year) + "_" + str(now.month) + "_" + str(now.day)

                filename_ext = "{0}.{1}".format(image_name,extension)

                shutil.copy(path[0],'temp_pic/{0}'.format(filename_ext))

                self.picture_dict[self.step] = image_name


            except:

                QMessageBox.information(self, 'Error', 'Something has gone wrong during copying picture to the album. Please try once again.')


        else:

            #### PLAY TASK ####

            if self.picture_dict[self.step] != "":


                image_path = self.db.readBlobData(self.picture_dict[self.step])

                self.picture_window = ImageWindow(image_path)

                self.picture_window.show()

                self.remove_temp_pictures()

            else:

                QMessageBox.information(self, 'Error', 'Application could not find attached picture. It might have been deleted or moved.')


    def finish_button_method(self):
        """Finish record and play button"""

        if self.record_or_play:

            #### RECORD TASK ####

            if self.step == 1 and self.display_description.text() == "" and self.display_code.toPlainText() == "":

                self.remove_temp_pictures()

                self.set_welcome_layout()

                return

            choice = QMessageBox.question(self, "Finish", '[Yes] - Finish and save task to the database\n[No] - Finish and don\'t save task\n[Cancel] - back to the recording',
                                 QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)


            if choice == QMessageBox.Yes:

                if self.display_description.text() == "" or self.display_code.toPlainText() == "":

                    pass

                else:

                    self.description_dict[self.step] = self.display_description.text()

                    self.code_dict[self.step] = self.display_code.toPlainText()

                self.db.add_task(self.description_dict,self.code_dict,self.picture_dict, self.title,self.language)

                self.images_to_database()

                self.remove_temp_pictures()

                self.set_welcome_layout()

            elif choice == QMessageBox.No:

                self.remove_temp_pictures()

                self.set_welcome_layout()

            elif choice == QMessageBox.Cancel:

                return

        else:

            #### PLAY TASK ####

            choice = QMessageBox.question(self, "Task completed", 'Are you satisfied with the level of task accomplishment? If [Yes], it will be available in next interval of time.',
                                          QMessageBox.Yes | QMessageBox.No)

            if choice == QMessageBox.Yes:

                next_pass_date = self.db.update_task(self.task_id, self.pass_count)

                QMessageBox.information(self, 'Task accomplished', 'Task has been accomplished. Expect it on the list on {0}'.format(next_pass_date))

                self.set_welcome_layout()




            elif choice == QMessageBox.No:

                QMessageBox.information(self, 'Task unaccomplished','Well... Try next time!')



                self.set_welcome_layout()



    def next_button_method(self):
        """Next record and play button"""

        #### RECORD TASK ####

        if self.record_or_play:

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

                self.picture_dict[self.step] = ""

                self.display_step.setText("Step\n{0}".format(self.step))

                self.display_description.clear()

                self.display_code.clear()

            else:

                return

        else:
            #### PLAY ####


            if self.description_or_code:

                self.display_code_play_layout()

            else:

                self.next_step_play_layout()


    def play_task_method(self):
        """Play task starting method"""

        if self.play_table.selectedIndexes() == []:

            return

        row = self.play_table.selectedIndexes()[0].row()

        self.task_id = self.play_table.item(row,5).text()


        self.title, self.description_dict, self.code_dict, self.picture_dict, self.pass_count = self.db.get_selected_task(self.task_id)

        self.step = 1

        self.stacked_layout.setCurrentIndex(0)

        self.set_play_layout()


    def cancel_task_method(self):
        """Cancel button method"""

        self.clear_record_menu()

        self.stacked_layout.setCurrentIndex(0)


    def start_record_task_method(self):
        """Start recording method"""

        if self.record_text_title.text() == "" or self.record_combo_box.currentText() == "---":

            QMessageBox.information(self,'Warning!','Title and field has to be fulfilled!')

        else:

            self.title = self.record_text_title.text()

            self.language = self.record_combo_box.currentText()

            self.set_record_layout()

            self.stacked_layout.setCurrentIndex(0)

    def remove_temp_pictures(self):
        """Removes all pictures from temp_pic folder"""

        folder = 'temp_pic'

        for filename in os.listdir(folder):

            file_path = os.path.join(folder,filename)

            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)

            except Exception as e:
                print(e)


    def clear_record_menu(self):
        """Clear Record menu"""
        self.record_text_title.setText('')

        self.record_combo_box.setCurrentIndex(0)

    def set_welcome_layout(self):
        """Set startin layout"""
        self.display_description.setDisabled(True)

        self.display_code.setDisabled(True)

        self.display_description.clear()

        self.display_code.clear()

        self.display_title.setText('Title')

        self.display_step.setText('Step\n/')

        self.picture_button.setDisabled(True)

        self.finish_button.setDisabled(True)

        self.next_button.setDisabled(True)

        self.alpha_button.setDisabled(True)
        self.beta_button.setDisabled(True)
        self.pi_button.setDisabled(True)
        self.omega_button.setDisabled(True)
        self.lambda_button.setDisabled(True)
        self.mi_button.setDisabled(True)
        self.sigma_button.setDisabled(True)
        self.sum_button.setDisabled(True)
        self.delta_button.setDisabled(True)
        self.gamma_button.setDisabled(True)
        self.not_equal_button.setDisabled(True)
        self.approx_equal_button.setDisabled(True)
        self.sqrt_button.setDisabled(True)
        self.gt_button.setDisabled(True)
        self.lt_button.setDisabled(True)
        self.degree_button.setDisabled(True)




        self.description_dict = {}

        self.code_dict = {}

        self.picture_dict = {}

        self.title = ""

        self.language = ""

    def set_record_layout(self):
        """Set layout while Record"""

        self.step = 1

        self.picture_dict[1] = ""

        self.display_description.setReadOnly(False)

        self.display_code.setReadOnly(False)

        self.display_description.setEnabled(True)

        self.display_code.setEnabled(True)

        self.display_title.setText(self.record_text_title.text())

        self.display_step.setText('Step\n{0}'.format(self.step))

        self.display_description.clear()

        self.display_code.clear()

        self.picture_button.setEnabled(True)

        self.finish_button.setEnabled(True)

        self.next_button.setEnabled(True)

        self.alpha_button.setDisabled(False)
        self.beta_button.setDisabled(False)
        self.pi_button.setDisabled(False)
        self.omega_button.setDisabled(False)
        self.lambda_button.setDisabled(False)
        self.mi_button.setDisabled(False)
        self.sigma_button.setDisabled(False)
        self.sum_button.setDisabled(False)
        self.delta_button.setDisabled(False)
        self.gamma_button.setDisabled(False)
        self.not_equal_button.setDisabled(False)
        self.approx_equal_button.setDisabled(False)
        self.sqrt_button.setDisabled(False)
        self.gt_button.setDisabled(False)
        self.lt_button.setDisabled(False)
        self.degree_button.setDisabled(False)



    def get_dict_highest_value(self):
        """Get highest value of step from dictionary"""

        self.key_list = self.description_dict.keys()
        return str(max(self.key_list))


    def set_play_layout(self):
        """Set layout while play"""

        self.finish_button.setDisabled(True)

        self.next_button.setEnabled(False)

        self.alpha_button.setDisabled(True)
        self.beta_button.setDisabled(True)
        self.pi_button.setDisabled(True)
        self.omega_button.setDisabled(True)
        self.lambda_button.setDisabled(True)
        self.mi_button.setDisabled(True)
        self.sigma_button.setDisabled(True)
        self.sum_button.setDisabled(True)
        self.delta_button.setDisabled(True)
        self.gamma_button.setDisabled(True)
        self.not_equal_button.setDisabled(True)
        self.approx_equal_button.setDisabled(True)
        self.sqrt_button.setDisabled(True)
        self.gt_button.setDisabled(True)
        self.lt_button.setDisabled(True)
        self.degree_button.setDisabled(True)


        QTimer.singleShot(3000, partial(self.next_button.setEnabled, True))

        self.display_description.setReadOnly(True)

        self.display_code.setReadOnly(True)

        self.display_description.setEnabled(True)

        self.display_code.setEnabled(True)

        self.display_title.setText(self.title)

        self.display_step.setText('Step\n1/{0}'.format(self.get_dict_highest_value()))

        self.display_description.setText(self.description_dict[self.step])

        self.description_or_code = True

        self.remove_temp_pictures()



    def display_code_play_layout(self):
        """Displays code while Play"""

        self.description_or_code = False


        self.display_code.setText(self.code_dict[self.step])


        if self.picture_dict[self.step] != "":

            self.picture_button.setEnabled(True)

        if self.step == int(self.get_dict_highest_value()):

            self.finish_button.setEnabled(True)
            self.next_button.setDisabled(True)

        else:
            self.next_button.setEnabled(False)
            QTimer.singleShot(1500, partial(self.next_button.setEnabled, True))



    def next_step_play_layout(self):
        """Click Next during Play"""




        self.step += 1



        self.description_or_code = True

        self.picture_button.setEnabled(False)

        self.next_button.setEnabled(False)
        QTimer.singleShot(3000, partial(self.next_button.setEnabled, True))

        self.display_code.clear()
        self.display_description.setText(self.description_dict[self.step])
        self.display_step.setText('Step\n{0}/{1}'.format(str(self.step),self.get_dict_highest_value()))


    def images_to_database(self):

        for filename in os.listdir('temp_pic'):

            if filename.endswith( ('.jpg','.png','.gif') ):

                image_name = filename[:-4]

                image_path = os.path.join('temp_pic',filename)

                image_ext = filename[-3:]

                self.db.insertBLOB(image_name, image_path, image_ext)


    def menuRecord_method(self):
        """Upper Menu option"""

        self.remove_temp_pictures()

        self.clear_record_menu()

        self.record_or_play = True

        self.stacked_layout.setCurrentIndex(1)

        self.display_description.setText('')

        self.display_code.setText('')



    def menuPlay_method(self):
        """Upper Menu option"""
        self.play_table.clear()

        self.load_to_play_table()

        self.record_or_play = False

        self.stacked_layout.setCurrentIndex(2)

        self.display_description.setText('')

        self.display_code.setText('')


    def menuDelete_method(self):
        """Upper Menu option"""
        self.delete_task_text_box.clear()

        self.stacked_layout.setCurrentIndex(3)


    def menuAbout_method(self):
        """Upper Menu option"""
        self.about_step = 1

        self.about_label.setText(self.about_dict[self.about_step])

        self.stacked_layout.setCurrentIndex(4)


    def menuExit_method(self):
        """Upper Menu option"""
        sys.exit()




class ImageWindow(QWidget):
    """Pop up window with to display picture"""
    def __init__(self, path):
        super().__init__()

        self.setWindowTitle('Picture')

        self.setGeometry(500,100,500,500)

        self.label = QLabel()

        picture = QPixmap(path)

        picture = picture.scaledToWidth(500)

        self.label.setPixmap(picture)

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.label)

        self.setLayout(self.layout)







if __name__ == '__main__':

    if not os.path.exists('temp_pic'):
        os.makedirs('temp_pic')

    app = QApplication([])
    window = MainWindow()
    window.show()
    window.raise_()
    app.exec_()
