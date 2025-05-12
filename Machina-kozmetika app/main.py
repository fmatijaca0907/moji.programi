import sys
from PyQt5.QtWidgets import QApplication
import Dobrodosli

if __name__ == '__main__':
    app = QApplication(sys.argv)
    prozor = Dobrodosli.DobrodosliProzor()
    prozor.show()
    sys.exit(app.exec_())