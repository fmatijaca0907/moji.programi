import sys
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout,QPushButton,QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import Registracijski
import Prijava

class DobrodosliProzor(QWidget):
    def __init__(self):
        super().__init__()
        self.pozdrav_labela = QLabel("Dobro došli u kozmetički salon")
        self.laura_label = QLabel("Studio Laura")
        self.prijava_button = QPushButton("Prijavi se")
        self.registracija_button = QPushButton("Registriraj se")
        self.registracija_prozor = None
        self.initUI()

    def initUI(self):
        
        #QWidget
        self.setWindowTitle("Kozmetički Salon Laura")
        self.setGeometry(700, 300, 500, 500)
        self.setStyleSheet("background-color: #98FB98;")
        
        #QLabel
        #Pozdrav
        self.pozdrav_labela.setAlignment(Qt.AlignCenter)
        pozdrav_font = QFont("Times New Roman", 18, QFont.Bold)
        self.pozdrav_labela.setFont(pozdrav_font)
        self.pozdrav_labela.setStyleSheet("color: #333333;")
        #Studio
        self.laura_label.setAlignment(Qt.AlignCenter)
        laura_font = QFont("Script MT Bold", 24)
        self.laura_label.setFont(laura_font)
        self.laura_label.setStyleSheet("color: #555555;")


        #PushButton
        gumb_font = QFont("Times New Roman", 14)
        self.registracija_button.setFont(gumb_font)
        self.prijava_button.setFont(gumb_font) 
        self.registracija_button.clicked.connect(self.otvori_reg_prozor)
        self.prijava_button.clicked.connect(self.otvori_prijava_prozor)
        self.prijava_button.setStyleSheet("background-color: #228B22; color: white;padding : 10px;border-radius: 5px;")
        self.registracija_button.setStyleSheet("background-color: #228B22; color: white; padding : 10px;border-radius: 5px;")

        layout = QVBoxLayout()
        layout.addWidget(self.pozdrav_labela)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.addWidget(self.laura_label)
        layout.addWidget(self.prijava_button)
        layout.addWidget(self.registracija_button)
        self.setLayout(layout)

    def otvori_reg_prozor(self):
        self.registracija_prozor = Registracijski.RegistracijskiProzor()
        self.registracija_prozor.show()
        self.close()

    def otvori_prijava_prozor(self):
        self.prijava_prozor = Prijava.PrijavaProzor()
        self.prijava_prozor.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dobrodosli = DobrodosliProzor()
    dobrodosli.show()
    sys.exit(app.exec_())
