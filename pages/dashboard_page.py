from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame, QSizePolicy
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve

class DashboardPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = main_window.get_database_manager()
        self.setStyleSheet("background-color: #cccccc;")

        self.init_ui()
        self.refresh()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # --- Header Frame (Title + Buttons) ---
        header_frame = QFrame()
        header_frame.setMaximumHeight(100)
        header_frame.setStyleSheet("background-color: transparent")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 20, 20, 20)
        header_layout.setSpacing(20)

        # Title + Subtitle
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        title = QLabel("Dashboard")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #000000;")

        subtitle = QLabel("Welcome back! Here's your financial overview.")
        subtitle.setStyleSheet("color: #555555; font-size: 15px;")

        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        new_entity_btn = QPushButton("New Entity")
        new_entity_btn.setFixedHeight(45)
        new_entity_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: black;
                font-weight: bold;
                padding: 6px 16px;
                border-radius: 6px;
                border: 1px solid #cccccc;
            }
            QPushButton:hover {
                background-color: #36d399;
                color: #ffffff;
            }
        """)

        run_btn = QPushButton("Run Consolidation")
        run_btn.setMinimumSize(160, 45)
        run_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        run_btn.setStyleSheet("""
            QPushButton {
                background-color: #09173f;
                color: #ffffff;
                font-weight: bold;
                padding: 6px 16px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #09173f;
            }
        """)

        def animate_button(button, grow=True):
            anim = QPropertyAnimation(button, b"minimumSize")
            anim.setDuration(150)
            anim.setEasingCurve(QEasingCurve.OutCubic)
            if grow:
                anim.setEndValue(QSize(180, 55))
            else:
                anim.setEndValue(QSize(160, 45))
            anim.start()
            button._anim = anim  # retain reference

        def enterEvent(event):
            animate_button(run_btn, grow=True)
            return QPushButton.enterEvent(run_btn, event)

        def leaveEvent(event):
            animate_button(run_btn, grow=False)
            return QPushButton.leaveEvent(run_btn, event)

        run_btn.enterEvent = enterEvent
        run_btn.leaveEvent = leaveEvent

        run_btn_frame = QFrame()
        run_btn_frame.setFixedSize(200, 65)
        run_btn_frame.setContentsMargins(0, -5, 0, 0)
        run_btn_layout = QVBoxLayout(run_btn_frame)
        run_btn_layout.setContentsMargins(0, 0, 0, 0)
        run_btn_layout.setAlignment(Qt.AlignCenter)
        run_btn_layout.addWidget(run_btn)

        button_layout.addWidget(new_entity_btn)
        button_layout.addWidget(run_btn_frame)

        # Header layout
        header_layout.addLayout(text_layout)
        header_layout.addStretch()
        header_layout.addLayout(button_layout)
        main_layout.addWidget(header_frame)

        # --- DB Status Label ---
        self.status_label = QLabel("Loading database stats...")
        self.status_label.setStyleSheet("color: gray; margin-left: 20px;")
        main_layout.addWidget(self.status_label)

        # --- KPI Card Row ---
        self.kpi_layout = QHBoxLayout()
        self.kpi_layout.setSpacing(20)
        self.kpi_layout.setContentsMargins(20, 0, 20, 0)

        self.kpi_cards = []
        for _ in range(4):
            card = self.create_kpi_card("", "", "")
            self.kpi_layout.addWidget(card)
            self.kpi_cards.append(card)

        main_layout.addLayout(self.kpi_layout)

    def create_kpi_card(self, title, value, change):
        card = QFrame()
        card.setFixedSize(220, 100)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 10px;
                border: 1px solid #ddd;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 10))

        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 18, QFont.Bold))

        change_label = QLabel(change)
        change_label.setFont(QFont("Segoe UI", 10))

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(change_label)

        # Store labels for later update
        card.title_label = title_label
        card.value_label = value_label
        card.change_label = change_label

        return card

    def refresh(self):
        if self.db:
            try:
                results = self.db.fetch_all("SELECT title, value, change FROM dashboard_kpis LIMIT 4")
                for i, row in enumerate(results):
                    if i >= len(self.kpi_cards):
                        break
                    title, value, change = row
                    self.kpi_cards[i].title_label.setText(title)
                    self.kpi_cards[i].value_label.setText(str(value))
                    self.kpi_cards[i].change_label.setText(change)
            except Exception as e:
                print("Error fetching KPI data:", e)

    def update_db_status(self, is_connected: bool):
        status = "Connected" if is_connected else "Disconnected"
        self.status_label.setText(f"Database Status: {status}")
