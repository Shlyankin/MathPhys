# Created by Shlyankin Nickolay
from PyQt5 import QtWidgets
from mydesign import Ui_MainWindow
from util import Task
import pyqtgraph as pg
import sys

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.task = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.graphWidget = pg.PlotWidget()
        self.ui.layoutGraph.addWidget(self.graphWidget)
        self.graphWidget.setBackground('w')
        self.graphWidget.setLabel('left', 'Температура (К)', color='red', size=30)
        self.graphWidget.setLabel('bottom', 'Радиус (см)', color='red', size=30)
        self.ui.label_current_time.setText("Индекс времени k = " + str(0))
        self.ui.sliderImage.valueChanged.connect(self.plotNextGraph)
        self.ui.buttonCaluclate.clicked.connect(self.calculate)
        self.ui.buttonClear.clicked.connect(self.clear)


    def clear(self):
        self.ui.edit_R.setText("")
        self.ui.edit_l.setText("")
        self.ui.edit_k.setText("")
        self.ui.edit_c.setText("")
        self.ui.edit_T.setText("")
        self.ui.edit_Uc.setText("")
        self.ui.edit_alpha.setText("")
        self.ui.edit_K.setText("")
        self.ui.edit_I.setText("")
        self.graphWidget.clear()
        self.task = None
        self.ui.label_gridInfo.setStyleSheet("color: rgb(0, 0, 0);")
        self.ui.label_gridInfo.setText("")
        self.ui.label_max_t.setText("0")
        self.ui.sliderImage.setMaximum(0)
        self.ui.label_current_time.setText("Индекс времени k = " + str(0))

    def calculate(self):
        self.ui.label_gridInfo.setStyleSheet("color: rgb(0, 0, 0);")
        self.ui.label_gridInfo.setText("")
        try:
            R =     float(self.ui.edit_R.text())
            l =     float(self.ui.edit_l.text())
            k =     float(self.ui.edit_k.text())
            c =     float(self.ui.edit_c.text())
            T =     float(self.ui.edit_T.text())
            Uc =    float(self.ui.edit_Uc.text())
            alpha = float(self.ui.edit_alpha.text())
            K =     int(  self.ui.edit_K.text())
            I =     int(  self.ui.edit_I.text())
            self.ui.label_gridInfo.setStyleSheet("color: rgb(255, 0, 0);")
            self.ui.label_gridInfo.setText("Идут вычисления. Подождите.")
            self.task = Task(R, l, k, c, alpha, T, Uc, K, I)
            answer = self.task.calculate()
            answer_analytic = self.task.analytic_decision()
            self.ui.label_gridInfo.setText("Готово!")
            y = answer[0]
            x = self.task.r
            self.ui.sliderImage.setValue(0)
            self.ui.label_max_t.setText(str(len(answer) - 1))
            self.ui.sliderImage.setMaximum(len(answer) - 1)
            self.graphWidget.clear()
            self.plotGraph(x, answer_analytic[0], "Температура при t=0", 'b')
            self.plotGraph(x, y, "Температура при t=0", 'r')
            self.ui.label_gridInfo.setText(self.ui.label_gridInfo.text() +
                                           "\nabsolute error: " + str(self.task.calculateAbsError()))

        except ValueError:
            self.ui.label_gridInfo.setStyleSheet("color: rgb(255, 0, 0);")
            self.ui.label_gridInfo.setText("Проверьте поля!")

    def plotNextGraph(self):
        t = self.ui.sliderImage.value()
        self.ui.label_current_time.setText("Индекс времени k = " + str(t))
        if(self.task != None):
            y = self.task.answer[t]
            x = self.task.r
            self.graphWidget.clear()
            self.plotGraph(x, self.task.answer_analytic[t], "Температура при t=0", 'b')
            self.plotGraph(x, y, "Температура при t="+str(t), 'r')

    def plotGraph(self, x, y, plotname, color):
        self.graphWidget.showGrid(x=True, y=True)
        pen = pg.mkPen(color=color, width=3)
        self.graphWidget.plot(x, y, name=plotname, pen=pen)



app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())

