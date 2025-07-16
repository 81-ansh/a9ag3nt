from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame
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
        run_btn.setFixedHeight(45)
        run_btn.setMinimumWidth(160)  # starting size
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
        #Animation Function
        def animate_button(button, grow=True):
            anim = QPropertyAnimation(button, b"minimumSize")
            anim.setDuration(150)
            anim.setEasingCurve(QEasingCurve.OutCubic)

            current_size = button.size()
            if grow:
                anim.setEndValue(QSize(current_size.width() + 20, current_size.height() + 4))
            else:
                anim.setEndValue(QSize(160, 45))  # original size

            anim.start()
            button._anim = anim  # prevent garbage collection

        def enterEvent(event):
            animate_button(run_btn, grow=True)
            return QPushButton.enterEvent(run_btn, event)

        def leaveEvent(event):
            animate_button(run_btn, grow=False)
            return QPushButton.leaveEvent(run_btn, event)

        run_btn.enterEvent = enterEvent
        run_btn.leaveEvent = leaveEvent



        # Add to layout
        button_layout.addWidget(new_entity_btn)
        button_layout.addWidget(run_btn)

        # --- Assemble header layout ---
        header_layout.addLayout(text_layout)
        header_layout.addStretch()
        header_layout.addLayout(button_layout)

        main_layout.addWidget(header_frame)

        # KPI Cards
        self.kpi_layout = QHBoxLayout()
        self.kpi_layout.setSpacing(20)

        self.kpi1 = self.create_kpi_card("Total Revenue", "$-", "+0%", True)
        self.kpi2 = self.create_kpi_card("Active Entities", "-", "+0", True)
        self.kpi3 = self.create_kpi_card("Consolidations", "-", "+0%", True)
        self.kpi4 = self.create_kpi_card("Users", "-", "-0%", False)

        for kpi in [self.kpi1, self.kpi2, self.kpi3, self.kpi4]:
            self.kpi_layout.addWidget(kpi)

        main_layout.addLayout(self.kpi_layout)

        # DB status label (dev/debug)
        self.status_label = QLabel("Loading database stats...")
        self.status_label.setStyleSheet("color: gray;")
        main_layout.addWidget(self.status_label)

    def create_kpi_card(self, title, value, change, is_positive=True):
        card = QFrame()
        card.setStyleSheet("background-color: white; border-radius: 10px; padding: 10px;")
        card.setFixedHeight(100)
        layout = QVBoxLayout(card)
        layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 10))
        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        change_label = QLabel(change)
        change_label.setFont(QFont("Segoe UI", 10))
        change_label.setStyleSheet(f"color: {'green' if is_positive else 'red'};")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(change_label)
        return card

    def create_recent_activity(self):
        panel = QFrame()
        panel.setStyleSheet("background-color: white; border-radius: 10px;")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        header = QLabel("Recent Activity")
        header.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(header)

        activities = [
            ("🟢", "Consolidation completed", "ABC Corp Q4 2024", "2 minutes ago"),
            ("🔵", "AI Analysis ready", "XYZ Holdings variance report", "15 minutes ago"),
            ("🟢", "New entity added", "Global Tech Ltd", "1 hour ago"),
            ("🟡", "Data sync failed", "Regional Sales Inc", "2 hours ago"),
        ]
        for icon, title, desc, time in activities:
            label = QLabel(f"{icon} <b>{title}</b><br><span style='color:gray'>{desc}</span> – {time}")
            label.setWordWrap(True)
            layout.addWidget(label)

        return panel

    def create_quick_actions(self):
        panel = QFrame()
        panel.setStyleSheet("background-color: white; border-radius: 10px;")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        header = QLabel("Quick Actions")
        header.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(header)

        actions = ["Add New Entity", "Start Consolidation", "View Analytics", "Manage Users"]
        for action in actions:
            btn = QPushButton(action)
            btn.setStyleSheet("background-color: yellow; padding: 10px; font-weight: bold;")
            layout.addWidget(btn)

        return panel

    def refresh(self):
        if self.db:
            try:
                tables_count = self.db.fetch_one("SELECT COUNT(*) FROM all_tables")[0]
                self.kpi2.findChild(QLabel, "").setText(str(tables_count))  # Entity KPI
                self.status_label.setText(f"Total Tables in DB: {tables_count}")
            except Exception as e:
                self.status_label.setText(f"Error fetching DB data: {e}")

    def update_db_status(self, is_connected: bool):
        status = "Connected" if is_connected else "Disconnected"
        self.status_label.setText(f"Database Status: {status}")
