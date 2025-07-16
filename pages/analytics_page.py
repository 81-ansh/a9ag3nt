from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from PySide6.QtCore import Qt

class AnalyticsPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db = main_window.get_database_manager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("📈 Data Analytics")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)
        self.load_analytics()

    def load_analytics(self):
        try:
            if self.db:
                queries = {
                    "Top 5 Tables by Row Count":
                        """SELECT table_name FROM (
                             SELECT table_name
                             FROM all_tables
                             ORDER BY num_rows DESC
                         ) WHERE ROWNUM <= 5"""
                }

                results = []
                for label, query in queries.items():
                    result = self.db.fetch_all(query)
                    results.append(f"{label}:\n" + "\n".join([f"  - {row[0]}" for row in result]))

                self.output.setText("\n\n".join(results))
            else:
                self.output.setText("DB not initialized.")
        except Exception as e:
            self.output.setText(f"Error loading analytics: {e}")

    def update_db_status(self, is_connected: bool):
        # Optionally add a "refresh" or grey out content if disconnected
        pass
