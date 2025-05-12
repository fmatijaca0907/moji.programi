import csv
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout,QLineEdit,QPushButton,QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import class_osoba
import Dobrodosli

class RegistracijskiProzor(QWidget):
    
    def __init__(self):
        super().__init__()
        self.naslov_label = QLabel("Unesi podatke za registraciju")
        self.tip_label = QLabel("Tip računa:")
        self.tip_combo = QComboBox()
        self.ime_label = QLabel("Unesi ime:")
        self.ime_unos = QLineEdit()
        self.prezime_label = QLabel("Unesi prezime:")
        self.prezime_unos = QLineEdit()
        self.email_label = QLabel("Unesi email:")
        self.email_unos = QLineEdit()
        self.telefon_label = QLabel("Unesi telefon:")
        self.telefon_unos = QLineEdit()
        self.lozinka_label = QLabel("Unesi lozinku:")
        self.lozinka_unos = QLineEdit()
        self.potvrda_loz_label = QLabel("Potvrdi lozinku:")
        self.potvrda_loz_unos = QLineEdit()
        self.regis_button = QPushButton("Registriraj se")
        self.greska_label = QLabel()
        self.natrag_button = QPushButton("Natrag")

        
        self.initUI()

    def initUI(self):

        #QWidgtet
        self.setStyleSheet("background-color: #98FB98;")
        self.setGeometry(700, 300, 500, 500)
        self.setWindowTitle("Kozmetički Salon")

        #QComboBox
        self.tip_combo.addItems(["Korisnik","Zaposlenik","Admin"])
        self.tip_combo.setStyleSheet("""
              QComboBox {
                font-family: "Arial";
                font-size: 20px;
                color: #333333;
                background-color: #F0FFF0;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 5px;}
""")

        #QLabel
        self.naslov_label.setContentsMargins(0,0,15,15)
        self.naslov_label.setStyleSheet("font-size : 40px;"
                                        "font-family : Times New Roman")
        self.ostale_labele = [self.tip_label,self.ime_label, self.prezime_label, self.email_label,self.telefon_label,
                              self.lozinka_label, self.potvrda_loz_label,self.telefon_label]
        
        self.ostali_unos = [self.ime_unos,self.prezime_unos,self.email_unos,self.telefon_unos,
                            self.lozinka_unos,self.potvrda_loz_unos]
        self.greska_label.setFont(QFont("Arial",20))

        #QLineEdit
        self.lozinka_unos.setEchoMode(QLineEdit.Password)
        self.potvrda_loz_unos.setEchoMode(QLineEdit.Password)
        for unos in self.ostali_unos:
            unos.setStyleSheet("""
                QLineEdit {
                    font-family: "Arial";
                    font-size: 20px;
                    color: #333333;
                    background-color: #F0FFF0;
                    border: 1px solid #cccccc;
                    border-radius: 5px;
                    padding: 5px;
                }
            """)

        #QPushButton
        gumb_font = QFont("Times New Roman", 14)
        self.regis_button.setFont(gumb_font)
        self.regis_button.setStyleSheet("""
            QPushButton {
                background-color: #228B22;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.regis_button.clicked.connect(self.registriraj_korisnika)
        self.natrag_button.setFont(gumb_font)
        self.natrag_button.setStyleSheet("""
            QPushButton {
                background-color: #228B22;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.natrag_button.clicked.connect(self.vrati_se)


        layout = QGridLayout()
        layout.addWidget(self.naslov_label,0,0,1,2,alignment=Qt.AlignCenter)
        layout.addWidget(self.tip_combo,1,1)
        
        font_label = QFont("Arial",13,60)
        for i,labela in enumerate(self.ostale_labele):
            labela.setFont(font_label)
            layout.addWidget(labela,i + 1,0)
        
        font_unos = QFont("Times New Roman", 12)
        for i, unos in enumerate(self.ostali_unos):
            unos.setFont(font_unos)
            layout.addWidget(unos, i + 2, 1)
        layout.addWidget(self.regis_button,8,0,1,2)
        layout.addWidget(self.natrag_button,9,0,1,2)

        layout.addWidget(self.greska_label,10,0,1,2)

        self.setLayout(layout)

    def registriraj_korisnika(self):
        tip = self.tip_combo.currentText()
        ime = self.ime_unos.text().strip()
        prezime = self.prezime_unos.text().strip()
        email = self.email_unos.text().strip()
        telefon = self.telefon_unos.text().strip()
        input_fields = [
            (self.ime_unos, "Molimo unesite ime."),
            (self.prezime_unos, "Molimo unesite prezime."),
            (self.email_unos, "Molimo unesite email."),
            (self.telefon_unos, "Molimo unesite telefonski broj."),
            (self.lozinka_unos, "Molimo unesite lozinku."),
            (self.potvrda_loz_unos, "Molimo potvrdite lozinku.")]
        
        all_filled = True
        for unos, poruka in input_fields:
            if not unos.text().strip():
                self.greska_label.setText(poruka)
                all_filled = False
                break

        if not all_filled:
            return
        
        lozinka = self.lozinka_unos.text()
        potvrda_lozinke = self.potvrda_loz_unos.text()
        

        if lozinka != potvrda_lozinke:
            self.lozinka_label.setStyleSheet("color: red;")
            self.potvrda_loz_label.setStyleSheet("color: red;")
            self.greska_label.setText("Lozinke se ne podudaraju.")
            return
        
        try:
            if tip == "Korisnik":
                nova_osoba = class_osoba.Korisnik(ime,prezime,email,telefon,lozinka)
            elif tip == "Zaposlenik":
                nova_osoba = class_osoba.Zaposlenik(ime, prezime, email, telefon, lozinka)
            elif tip == "Admin":
                nova_osoba = class_osoba.Administrator(ime, prezime, email, telefon, lozinka)
            self.spremi_csv([nova_osoba])
            self.greska_label.setText("Uspješno")
        except ValueError:
            self.greska_label.setText("Greska u formatu email")
        except Exception as e:
            print(f"Došlo je do pogreške: {e}")
            self.greska_label.setText(f"Došlo je do pogreške: {e}")
    def spremi_csv(self,lista):
        try:
            with open("sve_osobe.csv", 'a',encoding='latin-1') as csvfile:
                writer = csv.writer(csvfile)
                prvi_red = csvfile.tell() == 0
                if prvi_red:
                    zaglavlje = ["Tip", "Ime", "Prezime", "Email", "Telefon", "Lozinka"]
                    writer.writerow(zaglavlje)
                for objekt in lista:
                    writer.writerow(objekt.podaci_za_csv())
        except Exception:
            self.greska_label.setText("Greska pre spremanju")


    def vrati_se(self):
        self.dobrodosli_prozor = Dobrodosli.DobrodosliProzor()
        self.dobrodosli_prozor.show()
        self.close() 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dobrodosli = RegistracijskiProzor()
    dobrodosli.show()
    sys.exit(app.exec_())
