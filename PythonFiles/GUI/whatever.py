import PyQt4 import QtCore, QtGui




import sys
app = QtGui.QApplication(sys.argv)
MainWindow = QtGui.QMainWindow()
frame = QtGui.frame

ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())