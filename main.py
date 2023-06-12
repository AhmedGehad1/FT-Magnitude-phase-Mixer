from PyQt5 import QtWidgets
from gui5 import Ui_MainWindow
import sys
import os
from modes import modes
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import logging
logging.basicConfig(level=logging.DEBUG,filename="Logging.log",format='%(lineno)s - %(levelname)s - %(message)s',filemode='w')
logger = logging.getLogger()

class mainwindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mainwindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.plot = [self.ui.image1, self.ui.image2, self.ui.updated1, self.ui.updated2, self.ui.output1,self.ui.output2]
        for i in range(len(self.plot)):
            self.plot[i].ui.histogram.hide()
            self.plot[i].ui.roiBtn.hide()
            self.plot[i].ui.menuBtn.hide()
            self.plot[i].ui.roiPlot.hide()

        self.comboboxes = [self.ui.comboBox1 , self.ui.comboBox2 ,self.ui.comboBox5,self.ui.comboBox7 ,self.ui.comboBox3 ,self.ui.comboBox4,self.ui.comboBox6 ]

        self.component = ['Select mode', 'magnitude', 'phase', 'real', 'imaginary']
        self.ui.comboBox1.addItems(self.component)
        self.ui.comboBox2.addItems(self.component)
        self.mix = ['mode', 'magnitude', 'phase', 'real', 'imaginary', 'uniform magnitude', 'uniform phase']
        self.ui.comboBox5.addItems(self.mix)
        self.ui.comboBox7.addItems(self.mix)
        self.outputno = ['output', 'Slot 1', 'Slot 2']
        self.ui.comboBox3.addItems(self.outputno)
        self.imageno = ['Chose image', 'image 1', 'image 2']
        self.ui.comboBox4.addItems(self.imageno)
        self.ui.comboBox6.addItems(self.imageno)

        self.gains = [self.ui.slider1, self.ui.slider2]

        self.ui.actionimage1.triggered.connect(lambda: self.open(1))
        self.ui.actionimage2.triggered.connect(lambda: self.open(2))

        self.comboboxes[0].currentIndexChanged.connect(lambda: modes.components(self, 0, 2,1, self.comboboxes[0].currentText()))
        self.comboboxes[1].currentIndexChanged.connect(lambda: modes.components(self, 1, 3,2, self.comboboxes[1].currentText()))
        self.comboboxes[4].currentIndexChanged.connect(lambda: modes.outputplace(self))
        self.comboboxes[5].currentIndexChanged.connect(lambda: modes.source(self))
        self.comboboxes[6].currentIndexChanged.connect(lambda: modes.source(self))
        self.comboboxes[2].currentIndexChanged.connect(lambda: modes.othercomponent(self, 2, 3))

        self.Mixer_options = [["magnitude", "uniform magnitude"], ["phase", "uniform phase"], ["real"], ["imaginary"]]

        self.gains[0].sliderReleased.connect(lambda: modes.drawmix(self))
        self.gains[1].sliderReleased.connect(lambda: modes.drawmix(self))
        
    def open(self, number) :
        filename = QFileDialog.getOpenFileName(self)
        if filename[0]:
            self.path = filename[0]
            self.read(self.path, number)

    def read(self, path, number):
        if number == 1 :
            self.img1 = modes(path)
            self.plot[0].show()
            self.plot[0].setImage(self.img1.img.T)
            self.images = [self.img1]
            logger.info('choose image 1')
        elif number == 2 :
            self.img2 = modes(path)
            logger.info('choose image 2')
            
            if self.img2.img.shape != self.img1.img.shape:
                error_message = QMessageBox()
                error_message.setIcon(QMessageBox.Question)
                error_message.setText("Image 2 not the same size as Image 1, please make sure it is" )
                error_message.setWindowTitle("Error")
                error_message.exec_()
                logger.warning("Image 2 not same size as image 1")
            else:
                self.img2 = modes(path)
                self.plot[1].show()
                self.plot[1].setImage(self.img2.img.T)
                self.images = [self.img1,self.img2]

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app = QtWidgets.QApplication(sys.argv)
    with open('Adaptic.qss', 'r') as f:
        styleSheet = f.read()
        app.setStyleSheet(styleSheet)

    application = mainwindow()
    application.show()
    app.exec_()