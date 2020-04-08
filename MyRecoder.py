# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyrecoder.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from scipy.io import wavfile
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import sounddevice as sd
import time


class Ui_MainWindow(object):
    def __init__(self):
        self.sr = 44100
        self.max_duration = 600
        self.ch = 1
        self.save_num = 0
        self.audio = np.array([])
        self.input_device = sd.query_devices(kind='input')
        self.output_device = sd.query_devices(kind='output')
        self.time = 0
        self.status = 0

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(472, 340)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(180, 70, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setText('status')
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.input = QtWidgets.QLabel(self.centralwidget)
        self.input.setGeometry(QtCore.QRect(50, 130, 381, 16))
        self.input.setObjectName("input")
        self.input.setText('input device :: '+self.input_device['name'])

        self.output = QtWidgets.QLabel(self.centralwidget)
        self.output.setGeometry(QtCore.QRect(50, 170, 381, 15))
        self.output.setObjectName("output")
        self.output.setText('output device :: '+self.output_device['name'])

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(40, 210, 395, 30))
        self.widget.setObjectName("widget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.rec_B = QtWidgets.QPushButton(self.widget)
        self.rec_B.setObjectName("rec_B")
        self.horizontalLayout.addWidget(self.rec_B)
        self.rec_B.clicked.connect(self.rec)

        self.play_B = QtWidgets.QPushButton(self.widget)
        self.play_B.setObjectName("play_B")
        self.horizontalLayout.addWidget(self.play_B)
        self.play_B.clicked.connect(self.play)

        self.stop_B = QtWidgets.QPushButton(self.widget)
        self.stop_B.setObjectName("stop_B")
        self.horizontalLayout.addWidget(self.stop_B)
        self.stop_B.clicked.connect(self.stop)

        self.save_B = QtWidgets.QPushButton(self.widget)
        self.save_B.setObjectName("save_B")
        self.horizontalLayout.addWidget(self.save_B)
        self.save_B.clicked.connect(self.save)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 472, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.rec_B.setText(_translate("MainWindow", "REC"))
        self.play_B.setText(_translate("MainWindow", "PLAY"))
        self.stop_B.setText(_translate("MainWindow", "STOP"))
        self.save_B.setText(_translate("MainWindow", "SAVE"))

    def rec(self):
        self.audio = sd.rec(frames=self.max_duration*self.sr, samplerate=self.sr, channels=self.ch, dtype='float32',
                            device=self.input_device['name'])
        self.time = time.time()
        self.status = 'rec'
        self.label.setText('REC')

    def play(self):
        if len(self.audio) != 0:
            sd.play(data=self.audio, samplerate=self.sr, device=self.output_device['name'])
            self.label.setText('PLAY')
            self.status = 'play'
        else:
            self.label.setText('None')

    def stop(self):
        sd.stop()
        if self.status == 'rec':
            s_time = time.time() - self.time
            self.audio = self.audio[:int(round(s_time, 0)*self.sr)]
        self.status = 'stop'
        self.label.setText('STOP')

    def save(self):
        if len(self.audio) != 0:
            file_name = 'rec_audio'+str(self.save_num)+'.wav'
            wavfile.write(file_name, self.sr, self.audio)
            self.save_num += 1
            self.label.setText(str(self.save_num)+'_SAVE')
        else:
            self.label.setText('None')


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
