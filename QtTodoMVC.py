import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *

class App(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.store = dict()
        self.show_flag = "ALL"
        for task in ['Visit Los Angeles',
                     'Hike Mt Washington',
                     'Learn React',
                     'Write a Side Project by Go or Rust',
                     'Join My Local School Board',
                     ] :
            self.store[task] = False

        self.title = 'PyQt Todo MVC'

        self.vlayout = QVBoxLayout()
        self.vlayout.addStretch(1)
        self.vlayout.setContentsMargins(0,0,0,0)
        self.vlayout.setSpacing(0)

        self.line_edit = QLineEdit()
        self.vlayout.addWidget(self.line_edit)
        self.line_edit.returnPressed.connect(self.add_row)

        self.layout = QGridLayout()
        self.create_grid_layout()
        self.horizontalGroupBox = QGroupBox()
        self.horizontalGroupBox.setLayout(self.layout)
        self.vlayout.addWidget(self.horizontalGroupBox)

        self.cb = QComboBox()
        self.cb.addItem('All')
        self.cb.addItem('Active')
        self.cb.addItem('Inactive')
        self.cb.currentIndexChanged.connect(self.selection_changed)
        self.vlayout.addWidget(self.cb)

        central = QWidget()
        central.setLayout(self.vlayout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(central)
        self.scroll.setWidgetResizable(True)
        self.scroll.setMinimumWidth(600)
        self.scroll.setMinimumHeight(300)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.setCentralWidget(self.scroll)
        self.setWindowTitle(self.title)
        #self.setGeometry(self.left, self.top, self.width, self.height)

        self.show()

    def selection_changed(self, i):
        print('Items in the list:\n')
        print('Current index: ', i, ' ', self.cb.currentText())
        self.show_flag = self.cb.currentText()
        self.render()
        return

        print(self.layout.rowCount())
        print(self.layout.columnCount())

        for row in range(0, self.layout.rowCount()):
            w = self.layout.itemAtPosition(row, 0).widget()
            if (w.isChecked()):
                key = self.layout.itemAtPosition(row, 1).widget().text()
                print(key)
                self.delete_widget(w)

        self.update()
        self.show()

    def set_item_state(self):
        sender = self.sender()
        idx = QLayout.indexOf(self.layout, sender)
        (i, j, rowSpan, columnSpan) = self.layout.getItemPosition(idx)
        w = self.layout.itemAtPosition(i, 1).widget()
        text = w.text()
        self.store[text] = sender.isChecked()

    def delete_widget(self, w):
        self.layout.removeWidget(w)
        w.deleteLater()
        del w

    def add_row(self):
        sender = self.sender()
        key = sender.text()
        self.store[key] = False
        self.render()

    def remove_row(self, checkState):
        sender = self.sender()
        idx = QLayout.indexOf(self.layout, sender)
        (i, j, rowSpan, columnSpan) = self.layout.getItemPosition(idx)
        w = self.layout.itemAtPosition(i, 1).widget()
        text = w.text()
        self.store.pop(text, None)
        self.render()

    def render(self):
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 600
        self.clear_grid_layout()
        self.create_grid_layout()

    def clear_grid_layout(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        self.scroll.update()
        return

    def create_grid_layout(self):
        self.layout.setColumnStretch(1, 4)
        self.layout.setColumnStretch(2, 4)

        i = 0
        for key, val in self.store.items():
            if(self.show_flag.lower() == "all" or (self.show_flag.lower() == "active" and val == False) or (self.show_flag.lower() == "inactive" and val == True)):
                lineEdit = QLineEdit(key, self)
                checkBoxToggle = QCheckBox(self)
                checkBoxToggle.setCheckState(Qt.Unchecked)
                checkBoxToggle.stateChanged.connect(self.set_item_state)
                checkBoxDelete = QCheckBox(self)
                checkBoxDelete.stateChanged.connect(self.remove_row)

                self.layout.addWidget(checkBoxToggle, i, 0)
                self.layout.addWidget(lineEdit, i, 1)
                self.layout.addWidget(checkBoxDelete, i, 2)
                i = i + 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
