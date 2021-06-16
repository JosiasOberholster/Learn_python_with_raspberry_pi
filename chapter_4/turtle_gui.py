import turtle
import sys
from PySide.QtCore import *
from PySide.QtGui import *

class TurtleControl(QWidget):
    def __init__(self, turtle):
        super(TurtleControl, self).__init__()
        self.turtle = turtle

        self.left_btn = QPushButton("Left", self)
        self.right_btn = QPushButton("Right", self)
        self.move_btn = QPushButton("Move", self)
        self.distance_spin = QSpinBox()
        self.red_spin = QSpinBox()
        self.green_spin = QSpinBox()
        self.blue_spin = QSpinBox()
        self.red_label = QLabel("Red", self)
        self.green_label = QLabel("Green", self)
        self.blue_label = QLabel("Blue", self)
        self.colour_btn = QPushButton("Colour", self)

        self.controlsLayout = QGridLayout()
        self.controlsLayout.addWidget(self.left_btn, 0, 0)
        self.controlsLayout.addWidget(self.right_btn, 0, 1)
        self.controlsLayout.addWidget(self.distance_spin, 1, 0)
        self.controlsLayout.addWidget(self.move_btn, 1, 1)
        self.controlsLayout.addWidget(self.red_spin, 2, 1)
        self.controlsLayout.addWidget(self.green_spin, 3, 1)
        self.controlsLayout.addWidget(self.blue_spin, 4, 1)
        self.controlsLayout.addWidget(self.red_label, 2, 0)
        self.controlsLayout.addWidget(self.green_label, 3, 0)
        self.controlsLayout.addWidget(self.blue_label, 4, 0)
        self.controlsLayout.addWidget(self.colour_btn, 5, 0)
        self.setLayout(self.controlsLayout)

        self.distance_spin.setRange(0, 100)
        self.distance_spin.setSingleStep(5)
        self.distance_spin.setValue(20)

        for spinner in [self.red_spin, self.green_spin, self.blue_spin]:
            spinner.setRange(0, 255)
            spinner.setSingleStep(5)
            spinner.setValue(150)

        self.move_btn.clicked.connect(self.move_turtle)
        self.right_btn.clicked.connect(self.turn_turtle_right)
        self.left_btn.clicked.connect(self.turn_turtle_left)
        self.colour_btn.clicked.connect(self.colour_turtle)

    def turn_turtle_left(self):
        self.turtle.left(45)
    
    def turn_turtle_right(self):
        self.turtle.right(45)
        
    def move_turtle(self):
        self.turtle.forward(self.distance_spin.value())

    def colour_turtle(self):
        self.turtle.color(self.red_spin.value(), self.green_spin.value(), self.blue_spin.value())

#Setup turtle
window = turtle.Screen()
babbage = turtle.Turtle()
window.colormode(255)

#Create a Qt application
app = QApplication(sys.argv)
control_window = TurtleControl(babbage)
control_window.show()

# Enter Qt application main loop
app.exec_()
sys.exit()
