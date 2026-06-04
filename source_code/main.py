import sys
import os
from PyQt5.QtWidgets import (QApplication, QPushButton, QLabel, QMainWindow, QVBoxLayout,
                             QWidget, QHBoxLayout, QTextEdit, QFileDialog, QMessageBox)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QVBoxLayout(main_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        self.setWindowTitle("TO-DO LIST")
        self.setGeometry(200, 200, 1000, 700)
        self.setWindowIcon(QIcon("logo.png"))

        # SOLID NEON COLORS
        self.setStyleSheet("""
            QMainWindow {
                background-color: #8B008B;
            }
        """)

        self.filename = None

        self.create_header()
        self.create_content_area()
        self.setup_shortcuts()
        self.connect_buttons()

    def create_header(self):
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 15, 20, 15)
        header_layout.setSpacing(15)

        # CENTERED HEADER ROW
        header_row = QHBoxLayout()
        header_row.setSpacing(40)
        header_row.setContentsMargins(0, 0, 0, 0)

        # Logo - LEFT side
        logo_label = QLabel()
        pixmap = QPixmap("logo.png")
        scale_pixmap = pixmap.scaled(90, 90, Qt.KeepAspectRatio)
        logo_label.setPixmap(scale_pixmap)
        logo_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        logo_label.setStyleSheet("""
            background-color: #A100A1;
            border: 3px solid #FF00FF;
            border-radius: 25px;
            padding: 12px;
            box-shadow: 0 10px 30px rgba(255,0,255,0.6);
        """)
        header_row.addWidget(logo_label)

        header_row.addStretch(1)

        # Title - DEAD CENTER
        title_label = QLabel("QUICK NOTES")
        title_label.setFont(QFont("Helvetica", 32, QFont.Bold))
        title_label.setStyleSheet("""
            background-color: #FF00FF;
            color: #000;
            padding: 25px 60px;
            border-radius: 40px;
            border: 4px solid #A100A1;
            font-weight: bold;
            box-shadow: 0 12px 35px rgba(255,0,255,0.7);
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        """)
        title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        header_row.addWidget(title_label, 0, Qt.AlignCenter)

        header_row.addStretch(1)
        header_row.addSpacing(100)

        header_layout.addLayout(header_row)
        header_layout.addStretch(1)

        header_widget.setStyleSheet("""
            background-color: #9932CC;
            border-radius: 30px;
            border: 3px solid #FF00FF;
        """)
        header_widget.setFixedHeight(150)
        self.main_layout.addWidget(header_widget, 0)


    def create_content_area(self):
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(25)

        # LEFT: Buttons
        buttons_widget = QWidget()
        buttons_layout = QVBoxLayout(buttons_widget)
        buttons_layout.setSpacing(12)
        buttons_layout.setContentsMargins(25, 40, 15, 40)

        self.btn_open = QPushButton("📁 Open")
        self.btn_new = QPushButton("✏️ New")
        self.btn_save = QPushButton("💾 Save")
        self.btn_delete = QPushButton("🗑️ Delete")

        button_style = """
            QPushButton {
                background-color: #FF00FF;
                color: #000;
                border: 3px solid #A100A1;
                border-radius: 28px;
                padding: 18px 30px;
                font-size: 16px;
                font-weight: bold;
                min-height: 55px;
                min-width: 130px;
                max-width: 150px;
                box-shadow: 0 10px 30px rgba(255,0,255,0.6);
                text-shadow: 0 1px 2px rgba(255,255,255,0.5);
            }
            QPushButton:hover {
                background-color: #C71585;
                box-shadow: 0 15px 40px rgba(255,0,255,0.8);
            }
            QPushButton:pressed {
                background-color: #A100A1;
                box-shadow: 0 5px 20px rgba(255,0,255,0.4);
            }
        """

        for btn in [self.btn_open, self.btn_new, self.btn_save, self.btn_delete]:
            btn.setStyleSheet(button_style)
            buttons_layout.addWidget(btn)
        buttons_layout.addStretch()

        # CENTER: TYPEABLE Todo Area
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(35, 35, 35, 35)

        # Area title
        area_title = QLabel("📝 Your To-do's")
        area_title.setStyleSheet("""
            color: #FF00FF;
            font-size: 28px;
            font-weight: bold;
            padding-bottom: 20px;
            text-shadow: 0 4px 10px rgba(0,0,0,0.7);
            border-bottom: 2px solid #A100A1;
        """)
        area_title.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(area_title)

        # TYPE HERE! (Darker, less white)
        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText(
            "💡 Start typing your todos...\n\n"
            "• Ctrl+N = New\n"
            "• Ctrl+X = Delete File\n"
            "• Ctrl+O = Open\n"
            "• Ctrl+S = Save")
        self.text_area.setStyleSheet("""
            QTextEdit {
                background-color: #1a0f2e;
                color: #e6d5ff;
                border-radius: 30px;
                padding: 30px;
                font-size: 18px;
                font-family: 'Segoe UI', Arial;
                border: 4px solid #A100A1;
                box-shadow: 0 20px 50px rgba(0,0,0,0.6),
                            inset 0 2px 10px rgba(255,255,255,0.1);
            }
            QTextEdit:focus {
                border-color: #FF00FF;
                box-shadow: 0 0 40px rgba(255,0,255,0.8),
                            0 20px 50px rgba(0,0,0,0.6);
            }
        """)
        self.text_area.setMinimumHeight(320)
        center_layout.addWidget(self.text_area, 1)

        # Status label
        self.status_label = QLabel("Ready to create your todo list!")
        self.status_label.setStyleSheet("""
            color: #e6d5ff;
            font-size: 16px;
            padding: 15px;
            background-color: #7D26CD;
            border-radius: 20px;
            border: 2px solid #A100A1;
            text-shadow: 0 2px 6px rgba(0,0,0,0.8);
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        center_layout.addWidget(self.status_label)

        # RIGHT: Completed area
        right_widget = QWidget()
        right_widget.setStyleSheet("""
            background-color: #7D26CD;
            border-radius: 30px;
            border: 3px dashed #FF00FF;
        """)
        right_layout = QVBoxLayout(right_widget)
        right_layout.addStretch()

        content_layout.addWidget(buttons_widget, 0)
        content_layout.addWidget(center_widget, 2)
        content_layout.addWidget(right_widget, 0)

        self.main_layout.addWidget(content_widget, 1)

    def setup_shortcuts(self):
        self.new_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        self.new_shortcut.activated.connect(self.new_file)

        self.delete_shortcut = QShortcut(QKeySequence("Ctrl+X"), self)
        self.delete_shortcut.activated.connect(self.delete_file)

        self.open_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.open_shortcut.activated.connect(self.open_file)

        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.save_shortcut.activated.connect(self.save_file)

    def connect_buttons(self):
        self.btn_open.clicked.connect(self.open_file)
        self.btn_new.clicked.connect(self.new_file)
        self.btn_save.clicked.connect(self.save_file)
        self.btn_delete.clicked.connect(self.delete_file)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Todo", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.text_area.setPlainText(content)
                self.filename = file_path
                self.status_label.setText(f"Opened: {os.path.basename(file_path)}")
                self.setWindowTitle(f"TO-DO LIST - {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not open file:\n{str(e)}")

    def new_file(self):
        reply = QMessageBox.question(self, "New File", "Create new todo list? Unsaved changes will be lost.", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.text_area.clear()
            self.filename = None
            self.status_label.setText("Ready to create your todo list!")
            self.setWindowTitle("TO-DO LIST")

    def save_file(self):
        if self.filename:
            try:
                with open(self.filename, 'w', encoding='utf-8') as f:
                    f.write(self.text_area.toPlainText())
                self.status_label.setText(f"Saved: {os.path.basename(self.filename)}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not save file:\n{str(e)}")
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Todo List", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.text_area.toPlainText())
                self.filename = file_path
                self.status_label.setText(f"Saved: {os.path.basename(file_path)}")
                self.setWindowTitle(f"TO-DO LIST - {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not save file:\n{str(e)}")

    def delete_file(self):
        if self.filename and os.path.exists(self.filename):
            reply = QMessageBox.question(self, "Delete File", f"Delete file:\n{os.path.basename(self.filename)}?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    os.remove(self.filename)
                    self.new_file()
                    self.status_label.setText("File deleted!")
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Could not delete file:\n{str(e)}")
        else:
            QMessageBox.information(self, "Info", "No file to delete!")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()