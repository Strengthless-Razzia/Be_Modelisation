from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np
from rrr import RRR


class GraphWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111, projection='3d')

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.canvas)

        m, n, l, k = 1, 1, 1, 1


        self.robot = RRR(l, k, m, n)

        #On commence avec les q_i fig 
        q1 = np.pi/2
        q2 = 0
        q3 = 0

        self.Q = np.array([q1, q2, q3])


        mfin = self.robot.mgd_func(np.array([q1, q2, q3]) )

        self.update_graph()

    def update_Q(self, value):
        self.Q = value
        print('Updated Q with value :', value)
        self.update_graph()

    def update_graph(self):
        m1, m2, m3 = self.robot.mgd_detail(self.Q)

        X1 = (m1 @ np.array([0, 0, 0, 1]))[:3]
        X2 = (m1 @ m2 @ np.array([0, 0, 0, 1]))[:3]
        X3 = (m1 @ m2 @ m3 @ np.array([0, 0, 0, 1]))[:3]
        X4 = self.robot.X(self.Q)

        self.axes.cla()  # Clear the canvas.
        self.axes.plot3D(   [0, X1[0], X2[0], X3[0], X4[0]], 
                            [0, X1[1], X2[1], X3[1], X4[1]], 
                            [0, X1[2], X2[2], X3[2], X4[2]] , 'red', linewidth=10)
        self.axes.set_xlabel('X')
        self.axes.set_xlim(-2.0, 2.0)
        self.axes.set_ylabel('Y')
        self.axes.set_ylim(-2.0, 2.0)
        self.axes.set_zlabel('Z')
        self.axes.set_zlim(0.0, 2.0)

        self.axes.set_title('Visualisation du test MGD')
        self.canvas.draw()


