from image_select import map, current_file_path, get_folder, set_paths, save_and_delete, whats_the_name
from image_select import image_starting_path, current_image_path
from PySide6.QtWidgets import QMainWindow, QLabel, QWidget, QPushButton, QHBoxLayout, QLineEdit, QMessageBox, QStatusBar
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("image Book")
        # set vertical layout & Horizontal layout
        self.center_widget = QWidget(self)
        self.h_layout = QHBoxLayout()
        self.line_layout = QHBoxLayout()
        self.setCentralWidget(self.center_widget)
        self.center_widget.setLayout(self.h_layout)

        # line bar (for get_path and re_name functions)
        self.line_edit = QLineEdit()
        self.line_edit.setFixedSize(300,40)
        self.line_edit.hide()
        self.line_edit.returnPressed.connect(self.hide_folder_line)
        self.rename_line = QLineEdit()
        self.rename_line.setFixedSize(300,40)
        self.rename_line.hide()
        self.rename_line.returnPressed.connect(self.save_new_name)

        # menubar options
        menubar = self.menuBar()
        folder = menubar.addAction("Open Folder")
        folder.triggered.connect(self.show_folder_line)
        rename = menubar.addAction("Rename")
        rename.triggered.connect(self.re_name)
        hide_text_bar = menubar.addAction("Hide text bar")
        hide_text_bar.triggered.connect(self.hide_all)
        quit_action = menubar.addAction("Quit")
        quit_action.triggered.connect(self.quit_function)
        self.setStatusBar(QStatusBar(self))

        # central image
        self.pixmap = map()
        self.label_image = QLabel(self)
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.label_image.setPixmap(QPixmap(self.pixmap))

        self.update_image()
        # next and previous
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_clicked)
        self.previous_button = QPushButton("Previous")
        self.previous_button.clicked.connect(self.previous_clicked)

        # add to the layout
        self.h_layout.addWidget(self.previous_button, 20,Qt.AlignmentFlag.AlignLeft)
        self.h_layout.addWidget(self.label_image, Qt.AlignmentFlag.AlignVCenter)
        self.h_layout.addWidget(self.next_button, 20,Qt.AlignmentFlag.AlignRight)
        self.h_layout.addChildLayout(self.line_layout)

    # hides all text bars
    def hide_all(self):
        self.line_edit.hide()
        self.line_edit.setText("")
        self.rename_line.hide()
        self.rename_line.setText("")

    # to make sure the image keeps it's aspect ratio when the window is resized
    def resizeEvent(self, event):
        self.update_image()
        return super().resizeEvent(event)
    
    # updates the pixmap (size and all)
    def update_image(self):
        scaled_pixmap = self.pixmap.scaled(self.label_image.size(),
                                            Qt.AspectRatioMode.KeepAspectRatio, 
                                            Qt.TransformationMode.SmoothTransformation)
        self.label_image.setPixmap(scaled_pixmap)
        self.statusBar().showMessage(whats_the_name())

    # error message
    def error_box(self, message: str):
        QMessageBox.critical(
            self,
            "Critical Error",
            message,
            QMessageBox.StandardButton.Ok
        )

    # condition for error message
    def flage_condition(self, flage, message = "The path you provided was not correct or the folder was empty."):
        if flage == False:
            self.error_box(message)
            return True
        
    # display the next image in the folder
    def next_clicked(self):
        global image_starting_path
        new_path = current_file_path()
        image_starting_path = new_path
        new_pixmap = map(new_path)
        self.pixmap = new_pixmap
        self.update_image()

    # display the previous image in the folder
    def previous_clicked(self):
        global image_starting_path
        new_path = current_file_path(False)
        image_starting_path = new_path
        new_pixmap = map(new_path)
        self.pixmap = new_pixmap
        self.update_image()

    # menubar options
    # hides text bar after the user presses enter
    def hide_folder_line(self):
        self.line_edit.hide()
        folder_path = get_folder(self.line_edit.text())
        if self.flage_condition(folder_path):
            return
        new_path = set_paths(folder_path)
        if self.flage_condition(folder_path):
            return
        new_pixmap = map(new_path)
        self.pixmap = new_pixmap
        self.update_image()

    # shows text bar and asks user for a folder path
    def show_folder_line(self):
        self.line_edit.setPlaceholderText("Enter Folder Path")
        self.line_layout.addWidget(self.line_edit, alignment= Qt.AlignmentFlag.AlignLeft)
        self.line_edit.show()

    # rename current image
    def save_new_name(self):
        self.rename_line.hide()
        new_path = save_and_delete(self.rename_line.text())
        if self.flage_condition(new_path, "Can not change 0 Default.jpg. try a diffrent image"):
            return
        new_pixmap = map(new_path)
        self.pixmap = new_pixmap
        new_path = current_image_path.split('/')
        set_paths(new_path[0])
        self.update_image()

    # shows text bar and asks for the new name
    def re_name(self):
        self.rename_line.setPlaceholderText("Name")
        self.line_layout.addWidget(self.rename_line, alignment= Qt.AlignmentFlag.AlignLeft)
        self.rename_line.show()

    # another way to quit the program
    def quit_function(self):
        self.app.quit()