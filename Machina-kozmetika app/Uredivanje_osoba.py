from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QApplication,QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
import UrediZaposlenik
import UrediKorisnika

class UpravljanjeKorisnicimaProzor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Upravljanje korisnicima")
        self.setGeometry(750, 350, 500, 500)
        self.setStyleSheet("background-color: #98FF98;")
        self.initFonts()
        self.initWidgets()
        self.initLayout()
        
    def initFonts(self):
        self.naslov_font = QFont("Times New Roman",30,QFont.Bold)
        self.gumb_font = QFont("Arial",14)

    def initWidgets(self):
        self.naslov_label = QLabel("Studio Laura")
        self.naslov_label.setFont(self.naslov_font)
        self.naslov_label.setAlignment(Qt.AlignCenter)

        self.uredi_zaposlenike_button = QPushButton("Zaposlenici i usluge")
        self.uredi_zaposlenike_button.setFont(self.gumb_font)
        self.uredi_zaposlenike_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        self.uredi_zaposlenike_button.clicked.connect(self._otvori_uredi_zaposlenike)

        self.uredi_korisnike_button = QPushButton("Uredi korisnike")
        self.uredi_korisnike_button.setFont(self.gumb_font)
        self.uredi_korisnike_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        self.uredi_korisnike_button.clicked.connect(self._otvori_uredi_korisnike)

    def initLayout(self):
        layout = QGridLayout()
        layout.addWidget(self.naslov_label,0,0,1,2)
        layout.addWidget(self.uredi_zaposlenike_button,1,0)
        layout.addWidget(self.uredi_korisnike_button,1,1)
        self.setLayout(layout)

    def _otvori_uredi_zaposlenike(self):
        self.uredi_zaposlenike_prozor = UrediZaposlenik.ProzorSButtonima()
        self.uredi_zaposlenike_prozor.show()
        self.close()

    def _otvori_uredi_korisnike(self):
        self.uredi_korisnike_prozor = UrediKorisnika.ProzorUrediKorisnik()
        self.uredi_korisnike_prozor.show()
        self.close()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    prozor = UpravljanjeKorisnicimaProzor()
    prozor.show()
    sys.exit(app.exec_())