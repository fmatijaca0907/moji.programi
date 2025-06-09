from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGridLayout, QInputDialog, QLineEdit,
    QSpacerItem, QSizePolicy, QMessageBox, QComboBox
)
from PyQt5.QtCore import (
    Qt, QSize, QRectF, QPoint,
    QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup,
    QTimer
)
from PyQt5.QtGui import QFont, QIcon, QPainter, QBrush, QPen, QColor
from datetime import datetime

class CircularProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(80, 80)
        self.setMaximumSize(80, 80)

        self.value = 100 # Inicijalno 100% preostalog
        self.text_color = QColor(245, 245, 220)
        self.bg_circle_color = QColor(60, 60, 60, 150)
        self.progress_color = QColor(76, 175, 80) # Zelena
        self.font = QFont("Arial", 10, QFont.Bold)

        self.spent_amount = 0.0 # Potrošeni iznos za ovu kategoriju
        self.assigned_budget = 0.01 # Ukupan dodijeljeni budžet za ovu kategoriju (kumulativno)
                                    # Postavljeno na 0.01 da se izbjegne ZeroDivisionError

        self.default_segment_color = QColor(76, 175, 80) # Zelena
        self.warning_color = QColor(220, 20, 60) # Crvena za upozorenje

    def set_values(self, spent_amount, assigned_budget):
        self.spent_amount = spent_amount
        # Osiguravamo da assigned_budget nije nula, da izbjegnemo ZeroDivisionError
        self.assigned_budget = max(0.01, assigned_budget) 

        remaining_amount = self.assigned_budget - self.spent_amount

        if self.assigned_budget > 0:
            # Postotak preostalog
            percentage_remaining = (remaining_amount / self.assigned_budget) * 100
        else:
            percentage_remaining = 0 # Ako nema dodijeljenog budžeta, onda je 0% preostalo

        # Pobrini se da postotak ne bude negativan
        percentage_remaining = max(0, percentage_remaining)

        # Ključna promjena: zaokruživanje postotka.
        # Ako je postotak veći od 0, ali manji od 1, postavit ćemo ga na 1%
        if percentage_remaining > 0 and percentage_remaining < 1:
            self.value = 1
        else:
            self.value = int(percentage_remaining) # Zaokružujemo na cijeli broj

        # Osiguravamo da je vrijednost za crtanje između 0 i 100
        self.value = min(100, max(0, self.value))

        # Ažuriranje boje na temelju PREOSTALOG postotka
        # Boja upozorenja ako je preostalo 15% ili manje budžeta
        if self.value <= 15 and self.assigned_budget > 0 and remaining_amount > 0:
            self.progress_color = self.warning_color 
        elif remaining_amount <= 0: # Ako je budžet potrošen (ili u minusu), također crvena
            self.progress_color = self.warning_color
            self.value = 0 # Ako nema preostalog, krug je prazan
        else:
            self.progress_color = self.default_segment_color 
            
        self.update()

    def set_default_segment_color(self, qcolor_object):
        self.default_segment_color = qcolor_object
        self.progress_color = self.default_segment_color 
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        width = rect.width()
        height = rect.height()
        side = min(width, height)
        x = (width - side) / 2
        y = (height - side) / 2
        margin = 4
        outer_rect = QRectF(x + margin, y + margin, side - 2*margin, side - 2*margin)

        painter.setPen(QPen(self.bg_circle_color, 8))
        painter.drawEllipse(outer_rect)

        painter.setPen(QPen(self.progress_color, 8))
        # Kut crtanja počinje od vrha (90 stupnjeva) i ide u smjeru kazaljke na satu za PREOSTALI postotak
        start_angle = 90 * 16 
        # Span angle predstavlja PREOSTALI postotak
        span_angle = int(self.value * 3.6) * 16 
        painter.drawArc(outer_rect, start_angle, span_angle)

        painter.setPen(QPen(self.text_color))
        painter.setFont(self.font)
        text = f"{self.value}%" # Prikazujemo self.value koji je ograničen na 100%
        painter.drawText(outer_rect, Qt.AlignCenter, text)

        painter.end()


class FinAppMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Moja Aplikacija za Štednju")
        self.setGeometry(100, 100, 800, 550)

        self.total_earned = 0.0
        # Ove varijable sada predstavljaju UKUPAN DODIJELJENI IZNOS za svaku kategoriju
        self.needs_budget = 0.0
        self.wants_budget = 0.0
        self.savings_budget = 0.0
        
        # Ove varijable predstavljaju UKUPAN POTROŠENI IZNOS iz svake kategorije
        self.needs_spent = 0.0 
        self.wants_spent = 0.0
        self.savings_spent = 0.0

        # Varijable za praćenje proširenog stanja za svaku kategoriju
        self.is_needs_expanded = False
        self.is_wants_expanded = False # Vraćeno na False (default)
        self.is_savings_expanded = False # Vraćeno na False (default)

        self.is_category_input_expanded = False
        self.is_income_input_expanded = False 

        self.init_ui()
        self.update_budget_display()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_grid_layout = QGridLayout(central_widget)
        self.setStyleSheet("background-color: #1E2226; color: #F5F5DC;")

        self.main_grid_layout.setColumnStretch(0, 1)
        self.main_grid_layout.setColumnStretch(1, 4)
        self.main_grid_layout.setColumnStretch(2, 2)

        top_left_layout = QHBoxLayout()

        menu_button = QPushButton()
        menu_button.setText("☰")

        menu_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 28px;
                color: #A0D0FF;
                padding: 0px 5px 0px 0px;
            }
            QPushButton:hover {
                color: #FFFFFF;
            }
            QPushButton::menu-indicator {
                image: none;
            }
        """)

        top_left_layout.addSpacing(10)
        top_left_layout.addWidget(menu_button)
        top_left_layout.addSpacing(5)

        user_name_label = QLabel("Dobrodošli Korisnik!")
        user_name_label.setFont(QFont("Arial", 14, QFont.Bold))
        user_name_label.setStyleSheet("color: white;")
        user_name_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        top_left_layout.addWidget(user_name_label)
        top_left_layout.addStretch()

        self.date_label = QLabel(datetime.now().strftime("%d.%m.%Y."))
        self.date_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.date_label.setStyleSheet("color: white;")
        self.date_label.setAlignment(Qt.AlignTop | Qt.AlignRight)
        self.main_grid_layout.addWidget(self.date_label, 0, 2, 1, 1, Qt.AlignTop | Qt.AlignRight)

        top_left_widget = QWidget()
        top_left_widget.setLayout(top_left_layout)
        self.main_grid_layout.addWidget(top_left_widget, 0, 0, 1, 2, Qt.AlignTop | Qt.AlignLeft)


        self.main_grid_layout.setRowStretch(0, 1)
        self.main_grid_layout.setRowStretch(1, 2)

        self.budget_items_vbox = QVBoxLayout()
        self.budget_items_vbox.setSpacing(20)

        # --- Potrebe (Needs) ---
        self.needs_hbox = QHBoxLayout()
        self.needs_progress_bar = CircularProgressBar()
        self.needs_progress_bar.set_default_segment_color(QColor(31, 119, 180)) 
        self.needs_hbox.addWidget(self.needs_progress_bar)

        self.needs_label_btn = QPushButton(f"Potrebe (50%): €{self.needs_budget - self.needs_spent:.2f} (€{self.needs_budget:.2f})")
        self.needs_label_btn.setFont(QFont("Arial", 16, QFont.Bold))
        self.needs_label_btn.setStyleSheet("""
            QPushButton {
                color: #1F77B4;
                background-color: transparent;
                border: none;
                text-align: left;
                padding: 20px;
            }
            QPushButton:hover {
                color: #46B0FF;
            }
        """)
        self.needs_label_btn.setFlat(True)
        self.needs_label_btn.clicked.connect(lambda: self.toggle_budget_input("needs"))
        self.needs_hbox.addWidget(self.needs_label_btn)
        self.needs_hbox.addStretch()

        self.needs_widget = QWidget()
        self.needs_widget.setLayout(self.needs_hbox)
        self.budget_items_vbox.addWidget(self.needs_widget)

        # Needs input widget
        self.needs_input_widget = QWidget()
        self.needs_input_layout = QHBoxLayout(self.needs_input_widget)
        self.needs_input_layout.setContentsMargins(0, 5, 0, 5)
        self.needs_input_layout.addSpacing(90)
        
        self.needs_amount_input = QLineEdit()
        self.needs_amount_input.setPlaceholderText("Iznos (€)")
        self.needs_amount_input.setFont(QFont("Arial", 12))
        self.needs_amount_input.setStyleSheet("""
            QLineEdit {
                background-color: #3C4248;
                color: #F5F5DC;
                border: 1px solid #778899;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        self.needs_amount_input.setFixedWidth(150)
        self.needs_input_layout.addWidget(self.needs_amount_input)

        self.needs_pay_btn = QPushButton("Uplati")
        self.needs_pay_btn.setFont(QFont("Arial", 10, QFont.Bold))
        self.needs_pay_btn.setStyleSheet("""
            QPushButton {
                background-color: #2CA02C;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3CB371;
            }
        """)
        self.needs_pay_btn.clicked.connect(self.process_needs_payment)
        self.needs_input_layout.addWidget(self.needs_pay_btn)

        self.needs_cancel_btn = QPushButton("Odustani")
        self.needs_cancel_btn.setFont(QFont("Arial", 10, QFont.Bold))
        self.needs_cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #DC3545;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #E65A6B;
            }
        """)
        self.needs_cancel_btn.clicked.connect(lambda: self.toggle_budget_input("needs"))
        self.needs_input_layout.addWidget(self.needs_cancel_btn)

        self.needs_input_layout.addStretch()
        
        # Inicijalno sakrij input widget i dodaj ga u layout
        self.needs_input_widget.hide()
        self.needs_input_widget.setMinimumHeight(0)
        self.needs_input_widget.setMaximumHeight(0)
        self.budget_items_vbox.addWidget(self.needs_input_widget)


        # --- Želje (Wants) ---
        self.wants_hbox = QHBoxLayout()
        self.wants_progress_bar = CircularProgressBar()
        self.wants_progress_bar.set_default_segment_color(QColor(255, 127, 14))
        self.wants_hbox.addWidget(self.wants_progress_bar)

        self.wants_label_btn = QPushButton(f"Želje (30%): €{self.wants_budget - self.wants_spent:.2f} (€{self.wants_budget:.2f})")
        self.wants_label_btn.setFont(QFont("Arial", 16, QFont.Bold))
        self.wants_label_btn.setStyleSheet("""
            QPushButton {
                color: #FF7F0E;
                background-color: transparent;
                border: none;
                text-align: left;
                padding: 20px;
            }
            QPushButton:hover {
                color: #FF9933;
            }
        """)
        self.wants_label_btn.setFlat(True)
        # Ovdje nije povezano, kao što si tražio
        # self.wants_label_btn.clicked.connect(lambda: self.toggle_budget_input("wants")) 
        self.wants_hbox.addWidget(self.wants_label_btn)
        self.wants_hbox.addStretch()

        self.wants_widget = QWidget()
        self.wants_widget.setLayout(self.wants_hbox)
        self.budget_items_vbox.addWidget(self.wants_widget)

        # Wants input widget (postoji, ali je sakriven i bez funkcionalnih veza)
        self.wants_input_widget = QWidget()
        self.wants_input_layout = QHBoxLayout(self.wants_input_widget)
        self.wants_input_layout.setContentsMargins(0, 5, 0, 5)
        self.wants_input_layout.addSpacing(90)
        
        self.wants_amount_input = QLineEdit()
        self.wants_amount_input.setPlaceholderText("Iznos (€)")
        self.wants_amount_input.setFont(QFont("Arial", 12))
        self.wants_amount_input.setStyleSheet("""
            QLineEdit {
                background-color: #3C4248;
                color: #F5F5DC;
                border: 1px solid #778899;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        self.wants_amount_input.setFixedWidth(150)
        self.wants_input_layout.addWidget(self.wants_amount_input)

        self.wants_pay_btn = QPushButton("Uplati")
        self.wants_pay_btn.setFont(QFont("Arial", 10, QFont.Bold))
        self.wants_pay_btn.setStyleSheet("""
            QPushButton {
                background-color: #2CA02C;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3CB371;
            }
        """)
        # self.wants_pay_btn.clicked.connect(self.process_wants_payment)
        self.wants_input_layout.addWidget(self.wants_pay_btn)

        self.wants_cancel_btn = QPushButton("Odustani")
        self.wants_cancel_btn.setFont(QFont("Arial", 10, QFont.Bold))
        self.wants_cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #DC3545;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #E65A6B;
            }
        """)
        # self.wants_cancel_btn.clicked.connect(lambda: self.toggle_budget_input("wants"))
        self.wants_input_layout.addWidget(self.wants_cancel_btn)

        self.wants_input_layout.addStretch()

        self.wants_input_widget.hide()
        self.wants_input_widget.setMinimumHeight(0)
        self.wants_input_widget.setMaximumHeight(0)
        self.budget_items_vbox.addWidget(self.wants_input_widget)


        # --- Štednja (Savings) ---
        self.savings_hbox = QHBoxLayout()
        self.savings_progress_bar = CircularProgressBar()
        self.savings_progress_bar.set_default_segment_color(QColor(44, 160, 44))
        self.savings_hbox.addWidget(self.savings_progress_bar)

        self.savings_label_btn = QPushButton(f"Štednja (20%): €{self.savings_budget - self.savings_spent:.2f} (€{self.savings_budget:.2f})")
        self.savings_label_btn.setFont(QFont("Arial", 16, QFont.Bold))
        self.savings_label_btn.setStyleSheet("""
            QPushButton {
                color: #2CA02C;
                background-color: transparent;
                border: none;
                text-align: left;
                padding: 20px;
            }
            QPushButton:hover {
                color: #3CB371;
            }
        """)
        self.savings_label_btn.setFlat(True)
        # Ovdje nije povezano, kao što si tražio
        # self.savings_label_btn.clicked.connect(lambda: self.toggle_budget_input("savings")) 
        self.savings_hbox.addWidget(self.savings_label_btn)
        self.savings_hbox.addStretch()

        self.savings_widget = QWidget()
        self.savings_widget.setLayout(self.savings_hbox)
        self.budget_items_vbox.addWidget(self.savings_widget)

        # Savings input widget (postoji, ali je sakriven i bez funkcionalnih veza)
        self.savings_input_widget = QWidget()
        self.savings_input_layout = QHBoxLayout(self.savings_input_widget)
        self.savings_input_layout.setContentsMargins(0, 5, 0, 5)
        self.savings_input_layout.addSpacing(90)
        
        self.savings_amount_input = QLineEdit()
        self.savings_amount_input.setPlaceholderText("Iznos (€)")
        self.savings_amount_input.setFont(QFont("Arial", 12))
        self.savings_amount_input.setStyleSheet("""
            QLineEdit {
                background-color: #3C4248;
                color: #F5F5DC;
                border: 1px solid #778899;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        self.savings_amount_input.setFixedWidth(150)
        self.savings_input_layout.addWidget(self.savings_amount_input)

        self.savings_pay_btn = QPushButton("Uplati")
        self.savings_pay_btn.setFont(QFont("Arial", 10, QFont.Bold))
        self.savings_pay_btn.setStyleSheet("""
            QPushButton {
                background-color: #2CA02C;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 5px;
            }
            QPushButton:hover {{
                background-color: #3CB371;
            }}
        """)
        # self.savings_pay_btn.clicked.connect(self.process_savings_payment)
        self.savings_input_layout.addWidget(self.savings_pay_btn)

        self.savings_cancel_btn = QPushButton("Odustani")
        self.savings_cancel_btn.setFont(QFont("Arial", 10, QFont.Bold))
        self.savings_cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #DC3545;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 5px;
            }
            QPushButton:hover {{
                background-color: #E65A6B;
            }}
        """)
        # self.savings_cancel_btn.clicked.connect(lambda: self.toggle_budget_input("savings"))
        self.savings_input_layout.addWidget(self.savings_cancel_btn)

        self.savings_input_layout.addStretch()

        self.savings_input_widget.hide()
        self.savings_input_widget.setMinimumHeight(0)
        self.savings_input_widget.setMaximumHeight(0)
        self.budget_items_vbox.addWidget(self.savings_input_widget)


        self.budget_items_vbox.addStretch()

        budget_container_widget = QWidget()
        budget_container_widget.setLayout(self.budget_items_vbox)
        self.main_grid_layout.addWidget(budget_container_widget, 2, 1, 1, 1, Qt.AlignLeft | Qt.AlignTop)

        self.main_grid_layout.setRowStretch(2, 10)

        self.main_grid_layout.setRowStretch(3, 2)


        self.bottom_panel_container = QWidget()
        self.bottom_panel_vbox = QVBoxLayout(self.bottom_panel_container)
        self.bottom_panel_vbox.setContentsMargins(0, 0, 0, 0)
        self.bottom_panel_vbox.setSpacing(0)

        self.initial_elements_hbox = QHBoxLayout()
        self.total_earned_label_bottom = QLabel(f"Ukupno zarađeno: €{self.total_earned:.2f}")
        self.total_earned_label_bottom.setFont(QFont("Arial", 14))
        self.total_earned_label_bottom.setStyleSheet("color: #F5F5DC;")
        self.total_earned_label_bottom.setAlignment(Qt.AlignLeft)
        self.initial_elements_hbox.addWidget(self.total_earned_label_bottom)
        self.initial_elements_hbox.addStretch()

        button_width = 145 

        self.add_income_btn = QPushButton("Dodaj prihod")
        self.add_income_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.add_income_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #1E8449; 
                color: white;
                border: none;
                padding: 8px 5px; 
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #239B56; 
            }}
        """)
        self.add_income_btn.setFixedWidth(button_width) 
        self.add_income_btn.clicked.connect(self.show_income_input)
        self.initial_elements_hbox.addWidget(self.add_income_btn)

        self.add_to_category_btn = QPushButton("Dodijeli iznos")
        self.add_to_category_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.add_to_category_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #1E8449; 
                color: white;
                border: none;
                padding: 8px 5px; 
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #239B56; 
            }}
        """)
        self.add_to_category_btn.setFixedWidth(button_width) 
        self.add_to_category_btn.clicked.connect(self.show_category_input)
        self.initial_elements_hbox.addWidget(self.add_to_category_btn)


        self.initial_elements_widget = QWidget()
        self.initial_elements_widget.setLayout(self.initial_elements_hbox)
        self.bottom_panel_vbox.addWidget(self.initial_elements_widget)

        # Kreiranje HBoxa za gumb i input
        self.category_input_elements_hbox = QHBoxLayout()
        self.category_input_elements_hbox.setContentsMargins(0, 0, 0, 0)
        self.category_input_elements_hbox.setSpacing(10)

        self.category_input_elements_hbox.addStretch()
        
        self.category_amount_input_field = QLineEdit()
        self.category_amount_input_field.setPlaceholderText("Unesite iznos (€)")
        self.category_amount_input_field.setFont(QFont("Arial", 12))
        self.category_amount_input_field.setStyleSheet("""
            QLineEdit {
                background-color: #3C4248;
                color: #F5F5DC;
                border: 1px solid #778899;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        self.category_amount_input_field.setFixedWidth(150)
        self.category_input_elements_hbox.addWidget(self.category_amount_input_field)

        category_button_width = 80 

        self.btn_needs = QPushButton("Potrebe")
        self.btn_needs.setFont(QFont("Arial", 10, QFont.Bold))
        self.btn_needs.setStyleSheet(f"""
            QPushButton {{
                background-color: #1F77B4; 
                color: white;
                border: none;
                padding: 6px 5px; 
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #46B0FF;
            }}
        """)
        self.btn_needs.setFixedWidth(category_button_width) 
        self.btn_needs.clicked.connect(lambda: self.confirm_category_amount("Potrebe"))
        self.category_input_elements_hbox.addWidget(self.btn_needs)

        self.btn_wants = QPushButton("Želje")
        self.btn_wants.setFont(QFont("Arial", 10, QFont.Bold))
        self.btn_wants.setStyleSheet(f"""
            QPushButton {{
                background-color: #FF7F0E; 
                color: white;
                border: none;
                padding: 6px 5px; 
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #FF9933;
            }}
        """)
        self.btn_wants.setFixedWidth(category_button_width) 
        self.btn_wants.clicked.connect(lambda: self.confirm_category_amount("Želje"))
        self.category_input_elements_hbox.addWidget(self.btn_wants)

        self.btn_savings = QPushButton("Štednja")
        self.btn_savings.setFont(QFont("Arial", 10, QFont.Bold))
        self.btn_savings.setStyleSheet(f"""
            QPushButton {{
                background-color: #2CA02C; 
                color: white;
                border: none;
                padding: 6px 5px; 
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #3CB371;
            }}
        """)
        self.btn_savings.setFixedWidth(category_button_width) 
        self.btn_savings.clicked.connect(lambda: self.confirm_category_amount("Štednja"))
        self.category_input_elements_hbox.addWidget(self.btn_savings)

        self.cancel_category_btn = QPushButton("Odustani")
        self.cancel_category_btn.setFont(QFont("Arial", 10, QFont.Bold))
        self.cancel_category_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #DC3545;
                color: white;
                border: none;
                padding: 6px 5px; 
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #E65A6B;
            }}
        """)
        self.cancel_category_btn.setFixedWidth(category_button_width) 
        self.cancel_category_btn.clicked.connect(self.hide_category_input)
        self.category_input_elements_hbox.addWidget(self.cancel_category_btn)

        self.category_input_elements_hbox.addStretch()

        self.category_input_elements_widget = QWidget()
        self.category_input_elements_widget.setLayout(self.category_input_elements_hbox)
        self.bottom_panel_vbox.addWidget(self.category_input_elements_widget)

        self.category_input_elements_widget.hide()
        self.category_input_elements_widget.setMinimumHeight(0)
        self.category_input_elements_widget.setMaximumHeight(0)


        self.income_input_elements_hbox = QHBoxLayout()
        self.income_input_elements_hbox.setContentsMargins(0, 0, 0, 0)
        self.income_input_elements_hbox.setSpacing(10)

        self.income_input_elements_hbox.addStretch()
        
        self.income_input_field = QLineEdit()
        self.income_input_field.setPlaceholderText("Unesite iznos (€)")
        self.income_input_field.setFont(QFont("Arial", 12))
        self.income_input_field.setStyleSheet("""
            QLineEdit {
                background-color: #3C4248;
                color: #F5F5DC;
                border: 1px solid #778899;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        self.income_input_field.setFixedWidth(250)
        self.income_input_elements_hbox.addWidget(self.income_input_field)

        self.confirm_income_btn = QPushButton("Potvrdi")
        self.confirm_income_btn.setFont(QFont("Arial", 10, QFont.Bold))
        self.confirm_income_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #2CA02C;
                color: white;
                border: none;
                padding: 6px 5px; 
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #3CB371;
            }}
        """)
        self.confirm_income_btn.setFixedWidth(category_button_width) 
        self.confirm_income_btn.clicked.connect(self.confirm_income)
        self.income_input_elements_hbox.addWidget(self.confirm_income_btn)

        self.cancel_income_btn = QPushButton("Odustani")
        self.cancel_income_btn.setFont(QFont("Arial", 10, QFont.Bold))
        self.cancel_income_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #DC3545;
                color: white;
                border: none;
                padding: 6px 5px; 
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #E65A6B;
            }}
        """)
        self.cancel_income_btn.setFixedWidth(category_button_width) 
        self.cancel_income_btn.clicked.connect(self.cancel_income)
        self.income_input_elements_hbox.addWidget(self.cancel_income_btn)

        self.income_input_elements_hbox.addStretch()

        self.income_input_elements_widget = QWidget()
        self.income_input_elements_widget.setLayout(self.income_input_elements_hbox)
        self.bottom_panel_vbox.addWidget(self.income_input_elements_widget)

        self.income_input_elements_widget.hide()
        self.income_input_elements_widget.setMinimumHeight(0)
        self.income_input_elements_widget.setMaximumHeight(0)


        self.main_grid_layout.addWidget(self.bottom_panel_container, 4, 0, 1, 3, Qt.AlignBottom)
        self.main_grid_layout.setRowStretch(4, 1)


    def show_category_input(self):
        self.hide_all_input_panels_except("category")
        
        button_height = self.btn_needs.sizeHint().height() 
        target_height = self.category_amount_input_field.sizeHint().height() + button_height + 20 
        
        self.animation = QPropertyAnimation(self.category_input_elements_widget, b"maximumHeight")
        self.animation.setDuration(300)
        self.animation.setStartValue(self.category_input_elements_widget.height())
        self.animation.setEndValue(target_height)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        self.category_input_elements_widget.show()
        
        self.animation.finished.connect(self.category_amount_input_field.setFocus)
        
        self.animation.start()
        self.is_category_input_expanded = True

    def hide_category_input(self):
        self.animation = QPropertyAnimation(self.category_input_elements_widget, b"maximumHeight")
        self.animation.setDuration(300)
        self.animation.setStartValue(self.category_input_elements_widget.height())
        self.animation.setEndValue(0)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        self.animation.finished.connect(self.category_input_elements_widget.hide)
        
        self.animation.start()
        self.category_amount_input_field.clear()
        self.is_category_input_expanded = False


    def confirm_category_amount(self, selected_category): 
        try:
            amount_str = self.category_amount_input_field.text()
            amount = float(amount_str)
            if amount > 0:
                if selected_category == "Potrebe":
                    self.needs_budget += amount
                elif selected_category == "Želje":
                    self.wants_budget += amount
                elif selected_category == "Štednja":
                    self.savings_budget += amount
                
                self.update_budget_display()
            else:
                QMessageBox.warning(self, "Greška", "Iznos mora biti veći od nule.")
        except ValueError:
            QMessageBox.warning(self, "Greška", "Molimo unesite valjan broj.")
        finally:
            self.hide_category_input()

    def show_income_input(self):
        self.hide_all_input_panels_except("income")

        target_height = self.income_input_field.sizeHint().height() + 20
        
        self.animation = QPropertyAnimation(self.income_input_elements_widget, b"maximumHeight")
        self.animation.setDuration(300)
        self.animation.setStartValue(self.income_input_elements_widget.height())
        self.animation.setEndValue(target_height)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        self.income_input_elements_widget.show()
        
        self.animation.finished.connect(self.income_input_field.setFocus)
        
        self.animation.start()
        self.is_income_input_expanded = True 

    def hide_income_input(self):
        self.animation = QPropertyAnimation(self.income_input_elements_widget, b"maximumHeight")
        self.animation.setDuration(300)
        self.animation.setStartValue(self.income_input_elements_widget.height())
        self.animation.setEndValue(0)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        self.animation.finished.connect(self.income_input_elements_widget.hide)
        
        self.animation.start()
        self.is_income_input_expanded = False 
    
    def update_budget_display(self):
        # Ovdje su svi progress barovi i labele ažurirane
        self.needs_label_btn.setText(f"Potrebe (50%): €{self.needs_budget - self.needs_spent:.2f} (€{self.needs_budget:.2f})")
        self.wants_label_btn.setText(f"Želje (30%): €{self.wants_budget - self.wants_spent:.2f} (€{self.wants_budget:.2f})")
        self.savings_label_btn.setText(f"Štednja (20%): €{self.savings_budget - self.savings_spent:.2f} (€{self.savings_budget:.2f})")

        self.needs_progress_bar.set_values(self.needs_spent, self.needs_budget)
        self.wants_progress_bar.set_values(self.wants_spent, self.wants_budget)
        self.savings_progress_bar.set_values(self.savings_spent, self.savings_budget)


    def confirm_income(self):
        try:
            amount_str = self.income_input_field.text()
            amount = float(amount_str)
            if amount > 0:
                self.total_earned += amount
                self.total_earned_label_bottom.setText(f"Ukupno zarađeno: €{self.total_earned:.2f}")

                needs_portion = amount * 0.50
                wants_portion = amount * 0.30
                savings_portion = amount * 0.20

                self.needs_budget += needs_portion
                self.wants_budget += wants_portion
                self.savings_budget += savings_portion
                
                self.update_budget_display()

            else:
                QMessageBox.warning(self, "Greška", "Iznos mora biti veći od nule.")
        except ValueError:
            QMessageBox.warning(self, "Greška", "Molimo unesite valjan broj.")
        finally:
            self.income_input_field.clear()
            self.hide_income_input()

    def cancel_income(self):
        self.income_input_field.clear()
        self.hide_income_input()

    def hide_all_input_panels_except(self, current_panel_type=None):
        """Skriva sve input panele osim onog koji je specificiran."""
        # Paneli za plaćanje
        panels_to_check = {
            "needs": {"widget": self.needs_input_widget, "field": self.needs_amount_input, "expanded_attr": "is_needs_expanded"},
            # Sada ih provjeravamo, ali samo će se zatvoriti ako su prethodno bili otvoreni
            # (što se neće dogoditi jer je njihova funkcionalnost isključena)
            "wants": {"widget": self.wants_input_widget, "field": self.wants_amount_input, "expanded_attr": "is_wants_expanded"},
            "savings": {"widget": self.savings_input_widget, "field": self.savings_amount_input, "expanded_attr": "is_savings_expanded"}
        }

        for panel_type, data in panels_to_check.items():
            # Provjeravamo samo ako je panel_type različit od trenutnog i ako je proširen (u stanju self.is_expanded_attr)
            if panel_type != current_panel_type and getattr(self, data["expanded_attr"]):
                self._hide_single_budget_input(data["widget"], data["field"], panel_type)
        
        # Panel za dodjelu kategorijama
        if current_panel_type != "category" and self.is_category_input_expanded:
            self.hide_category_input()

        # Panel za prihod
        if current_panel_type != "income" and self.is_income_input_expanded:
            self.hide_income_input()

    def toggle_budget_input(self, budget_type):
        """Prikazuje ili skriva input panel za plaćanje odabrane kategorije."""
        # Ova funkcija će sada raditi samo za 'needs'
        if budget_type != "needs":
            return # Zanemari klik za "Wants" i "Savings" za sada

        is_expanded_attr = f"is_{budget_type}_expanded"
        is_expanded = getattr(self, is_expanded_attr)
        
        if is_expanded:
            self._hide_single_budget_input(getattr(self, f"{budget_type}_input_widget"), 
                                          getattr(self, f"{budget_type}_amount_input"), 
                                          budget_type)
        else:
            # Važno: Pozivamo hide_all_input_panels_except da zatvorimo sve OSTALE inpute,
            # ali ne i onaj koji planiramo otvoriti.
            self.hide_all_input_panels_except(budget_type) 
            
            input_widget = getattr(self, f"{budget_type}_input_widget")
            amount_input_field = getattr(self, f"{budget_type}_amount_input")
            
            input_widget.show()
            target_height = amount_input_field.sizeHint().height() + 20 
            animation = QPropertyAnimation(input_widget, b"maximumHeight")
            animation.setDuration(300)
            animation.setStartValue(0) 
            animation.setEndValue(target_height)
            animation.setEasingCurve(QEasingCurve.OutQuad)
            animation.start()
            setattr(self, is_expanded_attr, True)
            amount_input_field.setFocus()

    def _hide_single_budget_input(self, input_widget, amount_input_field, budget_type_name):
        """Pomoćna metoda za direktno skrivanje input widgeta za budžet i ažuriranje stanja."""
        animation = QPropertyAnimation(input_widget, b"maximumHeight")
        animation.setDuration(300)
        animation.setStartValue(input_widget.height())
        animation.setEndValue(0)
        animation.setEasingCurve(QEasingCurve.InQuad)
        animation.finished.connect(input_widget.hide) 
        animation.start()
        amount_input_field.clear()
        setattr(self, f"is_{budget_type_name}_expanded", False) 


    def process_needs_payment(self):
        self._process_payment(self.needs_amount_input, "needs")

    def _process_payment(self, amount_input_field, budget_type):
        """Pomoćna metoda za obradu plaćanja za bilo koju kategoriju."""
        # Ova funkcija će sada raditi samo za 'needs'
        if budget_type != "needs":
            return # Zanemari plaćanje za "Wants" i "Savings" za sada

        try:
            amount_str = amount_input_field.text()
            amount = float(amount_str)
            if amount > 0:
                current_budget_attr = f"{budget_type}_budget"
                current_spent_attr = f"{budget_type}_spent"

                current_budget = getattr(self, current_budget_attr)
                current_spent = getattr(self, current_spent_attr)

                if current_budget - current_spent >= amount:
                    setattr(self, current_spent_attr, current_spent + amount)
                    self.update_budget_display()
                    amount_input_field.clear()
                    self._hide_single_budget_input(getattr(self, f"{budget_type}_input_widget"), 
                                                   getattr(self, f"{budget_type}_amount_input"), 
                                                   budget_type)
                else:
                    QMessageBox.warning(self, "Nedovoljno sredstava", 
                                        f"Nemate dovoljno sredstava u kategoriji {budget_type.capitalize()}. Dostupno: €{current_budget - current_spent:.2f}")
            else:
                QMessageBox.warning(self, "Greška", "Iznos mora biti veći od nule.")
        except ValueError:
            QMessageBox.warning(self, "Greška", "Molimo unesite valjan broj.")


# --- Pokretanje aplikacije ---
if __name__ == '__main__':
    app = QApplication([])
    main_window = FinAppMainWindow()
    main_window.show()
    app.exec_()