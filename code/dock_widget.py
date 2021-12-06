from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDockWidget, QVBoxLayout, QWidget
import numpy as np
from slider_widget import CustomSlider

class DockWidget(QDockWidget):

    

    def __init__(self, parent=None):
        super().__init__(parent = parent)
        
        self.init_UI()
    

    def init_UI(self):
        self.setWindowTitle("Dock Area")
        self.setWidget(SlidersWidget(self))

        


class SlidersWidget(QWidget):

    Q_updated = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent = parent)
        self.Q = np.array([0.0, 0.0, 0.0])
        self.init_UI()
    

    def init_UI(self):
        self.setLayout(QVBoxLayout())

        slider1 = CustomSlider(init_value= 0.0,min = -np.pi, max=np.pi, name='q1')
        slider2 = CustomSlider(init_value= 0.0,min = -np.pi, max=np.pi, name='q2')
        slider3 = CustomSlider(init_value= 0.0,min = -np.pi, max=np.pi, name='q3')

        slider1.valueChangedSignal.connect(self.update_q1)
        slider2.valueChangedSignal.connect(self.update_q2)
        slider3.valueChangedSignal.connect(self.update_q3)


        self.layout().addWidget(slider1)
        self.layout().addWidget(slider2)
        self.layout().addWidget(slider3)

    def update_q1(self, value):
        self.Q[0] = value
        self.Q_updated.emit(self.Q)

    def update_q2(self, value):
        self.Q[1] = value
        self.Q_updated.emit(self.Q)

    def update_q3(self, value):
        self.Q[2] = value
        self.Q_updated.emit(self.Q)
