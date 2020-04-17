from PyQt5 import QtGui, QtWidgets
import speedtest
import csv
import datetime
import speed
import sys

class ExampleApp(QtWidgets.QMainWindow, speed .Ui_MainWindow):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.goButton.clicked.connect(self.getSpeeds)
        self.resetButton.clicked.connect(self.resetIt)
        self.upSpeedValue= 0.0
        self.downSpeedValue=0.0

    def getSpeeds(self):

        self.goButton.setEnabled(False)
        self.resetButton.setEnabled(False)

        self.resetIt()

        servers = []
        # If you want to test against a specific server
        # servers = [1234]

        threads = None
        # If you want to use a single threaded test
        # threads = 1
        self.downloadBar.setValue(25)
        self.uploadBar.setValue(25)
        s = speedtest.Speedtest()
        s.get_servers(servers)
        s.get_best_server()

        #download speed test
        self.downloadBar.setValue(50)
        s.download(threads=threads)
        self.downloadBar.setValue(100)

        # update display to user
        results_dict = s.results.dict()
        # self.downSpeedValue = round(results_dict['download'] / 1000000, 2)
        self.downSpeedValue = round(s.results.download / 1000000, 2)
        self.downSpeed.display(str(self.downSpeedValue))

        # upload speed test
        self.uploadBar.setValue(50)
        s.upload(threads=threads)
        self.uploadBar.setValue(100)

        # update display to user
        results_dict = s.results.dict()
        # self.upSpeedValue = round(results_dict['upload'] / 1000000, 2)
        self.upSpeedValue = round(s.results.upload / 1000000, 2)
        self.upSpeed.display(str(self.upSpeedValue))

        self.recordResults(results_dict)

        self.goButton.setEnabled(True)
        self.resetButton.setEnabled(True)

    def resetIt(self):
        self.uploadBar.setValue(0)
        self.downloadBar.setValue(0)
        self.downSpeed.display("0")
        self.upSpeed.display("0")


    def recordResults(self, results):
        with open('employee_file.csv', mode='w') as speed_file:
            speed_writer = csv.writer(speed_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            speed_writer.writerow(["Date",str(datetime.datetime.now()),"Download Speeds",round(results['download'] / 1000000, 3),"Upload Speeds",round(results['upload'] / 100000, 3)])

        speed_file.close()




def main():
    app = QtWidgets.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()