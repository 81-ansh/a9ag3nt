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

        # --- Header Frame (Title + Buttons on same row) ---
        header_frame = QFrame()
        header_frame.setMaximumHeight(100)
        header_frame.setStyleSheet("background-color: transparent")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 20, 20, 20)
        header_layout.setSpacing(20)

        # --- Left: Title + Subtitle ---
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        title = QLabel("Dashboard")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #000000;")

        subtitle = QLabel("Welcome back! Here's your financial overview.")
        subtitle.setStyleSheet("color: #555555; font-size: 15px;")

        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)

        # --- Right: Buttons ---
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # New Entity Button
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

        # Run Consolidation Button
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

        # Animate on hover
        def animate_button(button, grow=True):
            anim = QPropertyAnimation(button, b"minimumSize")
            anim.setDuration(150)
            anim.setEasingCurve(QEasingCurve.OutCubic)
            if grow:
                anim.setEndValue(QSize(180, 55))
            else:
                anim.setEndValue(QSize(160, 45))
            anim.start()
            button._anim = anim  # keep reference

        def enterEvent(event):
            animate_button(run_btn, grow=True)
            return QPushButton.enterEvent(run_btn, event)

        def leaveEvent(event):
            animate_button(run_btn, grow=False)
            return QPushButton.leaveEvent(run_btn, event)

        run_btn.enterEvent = enterEvent
        run_btn.leaveEvent = leaveEvent

        # Centered frame for run_btn
        run_btn_frame = QFrame()
        run_btn_frame.setFixedSize(200, 65)
        run_btn_frame.setStyleSheet("border: 0px")
        run_btn_frame.setContentsMargins(0, -5, 0, 0)

        run_btn_layout = QVBoxLayout(run_btn_frame)
        run_btn_layout.setContentsMargins(0, 0, 0, 0)
        run_btn_layout.setAlignment(Qt.AlignCenter)
        run_btn_layout.addWidget(run_btn)

        # Add buttons
        button_layout.addWidget(new_entity_btn)
        button_layout.addWidget(run_btn_frame)

        # Add to header
        header_layout.addLayout(text_layout)
        header_layout.addStretch()
        header_layout.addLayout(button_layout)
        main_layout.addWidget(header_frame)

        # --- DB Status Label ---
        self.status_label = QLabel("Loading database stats...")
        self.status_label.setStyleSheet("color: gray; margin-left: 20px;")
        main_layout.addWidget(self.status_label)

    def refresh(self):
        if self.db:
            try:
                row = self.db.fetch_one("SELECT COUNT(*) FROM all_tables")
                self.status_label.setText(f"Total Tables in DB: {row[0]}")
            except Exception as e:
                self.status_label.setText(f"Error fetching DB data: {e}")

    def update_db_status(self, is_connected: bool):
        status = "Connected" if is_connected else "Disconnected"
        self.status_label.setText(f"Database Status: {status}")
