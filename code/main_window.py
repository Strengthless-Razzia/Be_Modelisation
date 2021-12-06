from PyQt5.QtWidgets import QMainWindow, QApplication
from graph_wigdet import GraphWidget
from dock_widget import DockWidget
import sys

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.init_UI()
    
    def init_UI(self):
        self.graph_widget =  GraphWidget()
        self.setCentralWidget(self.graph_widget)

        self.dock = DockWidget()

        self.addDockWidget(1, self.dock)

        self.dock.widget().Q_updated.connect(self.graph_widget.update_Q)

        self.show()


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()