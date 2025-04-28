import sys
import csv
import os
import datetime as dt

from PyQt5.QtWidgets import (QApplication,QWidget,QGridLayout,QLineEdit,
                            QCalendarWidget,QLabel,QComboBox,QPushButton,QVBoxLayout)
from PyQt5.QtCore import Qt

class UserCustomer(QWidget):

    def __init__(self,kalendarsat):
        super().__init__()
        self.kalendar = kalendarsat 
        self.ime_label = QLabel("Unesi ime:")
        self.prezime_label = QLabel("Unesi Prezime:")
        self.ime_unos = QLineEdit()
        self.prezime_unos = QLineEdit()
        self.button = QPushButton("Potvrdi")
        self.upozorenje_label = QLabel(self)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addWidget(self.ime_label)
        layout.addWidget(self.ime_unos)
        layout.addWidget(self.prezime_label)
        layout.addWidget(self.prezime_unos)
        layout.addWidget(self.button)
        layout.addWidget(self.upozorenje_label)

        self.setLayout(layout)
        self.button.clicked.connect(self.provjeri_unos_i_prebaci)

        self.setStyleSheet("""
                
                QLabel{
                       font-size : 20px; 
                       font-style : Arial;       }
                QLineEdit{
                        font-size : 30px; 
                        font-style : Arial;
                        font-family : calibri;   
                }
                QPushButton{
                        font-size : 30px; 
                        font-style : Arial; 
                           }
                
""")

    def provjeri_unos_i_prebaci(self):
        ime = self.ime_unos.text()
        prezime = self.prezime_unos.text()

        if ime and prezime:
            self.close()
            self.kalendar.prikazi_kalendar_s_podacima(ime,prezime)
        else:
            self.upozorenje_label.setText("Unesi ime i prezime")


class CalendarClock(QWidget):

    def __init__(self):
        super().__init__()
        self.calendar = QCalendarWidget(self)
        self.datum_label = QLabel("Odaberi datum:")
        self.vrijeme_label = QLabel("Odaberi vrijeme:")
        self.unos_label_datum = QLabel(self)
        self.unos_label_vrijeme = QLabel(self)
        self.d_menu = QComboBox(self)
        self.submit_button = QPushButton("Spremi",self)
        self.full_label = QLabel(self)
        self.odabrani_datum = None
        self.odabrano_vrijme = None
        self.ime_prezmime = QLabel(self)
        self.initUI()

    def initUI(self):
        #Window
        self.setWindowTitle("Aplikacija")

        #QCombo
        for i in range(13):
            self.d_menu.addItem(f"{(i+7)+1}:00")
            self.d_menu.addItem(f"{(i+7)+1}:30")
        self.d_menu.setMaxVisibleItems(5)
        self.d_menu.setStyleSheet("font-size : 27px;"
                                  "font-family : calibri;" )
        self.d_menu.currentIndexChanged.connect(self.save_time)

        #Calendar
        self.calendar.setStyleSheet("font-size : 25px;"
                                    "font-family : Arial")
        self.calendar.clicked.connect(self.save_date)

        #QPushButton
        self.submit_button.clicked.connect(self.submit)
        self.submit_button.setStyleSheet("font-size : 30px;"
                                         "font-weight : bold;"
                                         "color : #3275a8;"
                                         "font-family : calibri;" )
        

        grid = QGridLayout()
        grid.addWidget(self.ime_prezmime,1,0)
        grid.addWidget(self.datum_label,2,0)
        grid.addWidget(self.calendar,3,0)
        grid.addWidget(self.vrijeme_label,2,1)
        grid.addWidget(self.d_menu,3,1,)
        grid.addWidget(self.unos_label_datum,4,0)
        grid.addWidget(self.unos_label_vrijeme,4,1)
        grid.addWidget(self.submit_button,5,0,1,2)
        grid.addWidget(self.full_label,6,0,1,2)
        self.setLayout(grid)

        self.setStyleSheet("""
            QLabel{
                font-size : 30px;
                font-family : calibry;
                qproperty-alignment: AlignCenter;                      
                padding : 10px;}
             
        """)
    
    def prikazi_kalendar_s_podacima(self,ime, prezime):
        self.ime_korisnika = ime
        self.prezime_korisnika = prezime
        self.ime_prezmime.setText(f"{ime} {prezime}")
        self.ime_prezmime.setStyleSheet("font-size:20px;"
                                        "qproperty-alignment : AlignLeft;"
                                        "color : #3275a8;"
                                        "font-weight : bold;")
        self.show()


    def save_date(self, date):
        danasnji_datum = dt.datetime.now().date()
        odabrani_qdate = date
        odabrani_datum = odabrani_qdate.toPyDate()

        if odabrani_datum < danasnji_datum:
            self.unos_label_datum.setText("Datum ne može biti u prošlosti!")
        else:
            self.odabrani_datum = odabrani_qdate.toString(Qt.ISODate)
            self.unos_label_datum.setText(self.odabrani_datum)

    def save_time(self,index):
        self.odabrano_vrijme = self.d_menu.itemText(index)
        self.unos_label_vrijeme.setText(self.odabrano_vrijme)

    def submit(self):
        if self.odabrani_datum is not None and self.odabrano_vrijme is not None:
            self.full_label.setText(f"Termin spremljen za {self.ime_korisnika} {self.prezime_korisnika}!")
            self.write_csv_dt()
        else:
            self.full_label.setText("Molimo odaberite datum i vrijeme.")

    def write_csv_dt(self):
        naziv_csv_datoteke = os.path.join(os.path.dirname(__file__),"rezervacija.csv")
        try:
            with open(naziv_csv_datoteke, 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([self.ime_korisnika, self.prezime_korisnika, self.odabrani_datum, self.odabrano_vrijme])
        except:
            self.full_label.setText(f"Došlo je do greške prilikom upisa u CSV.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    kalendar_prozor = CalendarClock()
    ime_prezime_prozor = UserCustomer(kalendar_prozor)
    ime_prezime_prozor.show()
    sys.exit(app.exec_())