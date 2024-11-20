import sys
import math
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QLabel, QLineEdit, QPushButton,
    QGraphicsScene, QGraphicsView, QGroupBox, QFormLayout
)
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt
from nozzel import NozzleDesign

class NozzleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nozzle Design and Visualization")
        self.setGeometry(100, 100, 1200, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)

        self.left_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_layout, stretch=1)

        self.input_group = QGroupBox("Input Parameters")
        self.input_layout = QFormLayout()
        self.input_group.setLayout(self.input_layout)
        self.left_layout.addWidget(self.input_group)

        self.inputs = {}
        self.add_input_field("Thrust (F) [N]:", "1000")
        self.add_input_field("Chamber Pressure (Pc) [Pa]:", "2000000")
        self.add_input_field("Atmospheric Pressure (Pa) [Pa]:", "101325")
        self.add_input_field("Specific Heat Ratio (γ):", "1.042")
        self.add_input_field("Thrust Coefficient (CF):", "1.5")
        self.add_input_field("Expansion Ratio (ε):", "20")

        self.generate_button = QPushButton("Generate Nozzle Design")
        self.generate_button.clicked.connect(self.generate_nozzle)
        self.left_layout.addWidget(self.generate_button)

        self.results_group = QGroupBox("Design Results")
        self.results_layout = QVBoxLayout()
        self.results_group.setLayout(self.results_layout)
        self.left_layout.addWidget(self.results_group)

        self.results_labels = {}

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.main_layout.addWidget(self.view, stretch=2)

    def add_input_field(self, label_text, default_value):
        input_field = QLineEdit()
        input_field.setText(default_value)
        self.input_layout.addRow(QLabel(label_text), input_field)
        self.inputs[label_text] = input_field

    def generate_nozzle(self):
        self.scene.clear()
        self.results_layout.setContentsMargins(0, 0, 0, 0)

        try:
            F = float(self.inputs["Thrust (F) [N]:"].text())
            Pc = float(self.inputs["Chamber Pressure (Pc) [Pa]:"].text())
            Pa = float(self.inputs["Atmospheric Pressure (Pa) [Pa]:"].text())
            γ = float(self.inputs["Specific Heat Ratio (γ):"].text())
            CF = float(self.inputs["Thrust Coefficient (CF):"].text())
            ε = float(self.inputs["Expansion Ratio (ε):"].text())
        except ValueError:
            self.statusBar().showMessage("Invalid input values!")
            return

        nozzle = NozzleDesign(F, Pc, Pa, γ, CF, ε)
        design = nozzle.design_nozzle()

        for key, value in design.items():
            if key not in self.results_labels:
                label = QLabel(f"{key}: {value:.4f}")
                self.results_labels[key] = label
                self.results_layout.addWidget(label)
            else:
                self.results_labels[key].setText(f"{key}: {value:.4f}")

        At = design["Throat Area (At)"]
        Ae = design["Exit Area (Ae)"]
        convergent_angle = design["Convergent Angle"]
        divergent_angle = design["Divergent Angle"]

        throat_radius = math.sqrt(At / math.pi)
        exit_radius = math.sqrt(Ae / math.pi)
        convergent_length = throat_radius / math.tan(math.radians(convergent_angle))
        divergent_length = (exit_radius - throat_radius) / math.tan(math.radians(divergent_angle))
        total_length = convergent_length + divergent_length

        scale = 500  
        pen = QPen(Qt.black)
        pen.setWidth(2)

        inlet_radius = throat_radius * 2
        self.scene.addLine(0, -inlet_radius * scale, convergent_length * scale, -throat_radius * scale, pen)
        self.scene.addLine(0, inlet_radius * scale, convergent_length * scale, throat_radius * scale, pen)

        self.scene.addLine(
            convergent_length * scale, -throat_radius * scale,
            total_length * scale, -exit_radius * scale, pen
        )
        
        self.scene.addLine(
            convergent_length * scale, throat_radius * scale,
            total_length * scale, exit_radius * scale, pen
        )

        self.view.setScene(self.scene)
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NozzleApp()
    window.show()
    sys.exit(app.exec_())
