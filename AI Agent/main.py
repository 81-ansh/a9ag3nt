# main.py
import sys
import os
import logging
import threading
from typing import Optional

from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

# Import custom modules
from pages.ai_assistant_page import AIAssistantPage
from pages.dashboard_page import DashboardPage
from pages.analytics_page import AnalyticsPage
from database.db_manager import DatabaseManager, DatabaseConfig
from ai.financial_agent import FinancialAIAgent
from config.config_manager import ConfigManager
from ui.base_window import BaseWindow


class MainApplication(BaseWindow):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.db_manager = DatabaseManager()
        self.ai_agent: Optional[FinancialAIAgent] = None

        self.setup_logging()
        self.setup_pages()
        self.setup_database()
        self.setup_ai_agent()
        self.setup_navigation()

        self.connection_timer = QTimer()
        self.connection_timer.timeout.connect(self.check_database_connection)
        self.connection_timer.start(30000)

    def setup_logging(self):
        config = self.config_manager.get_config()
        logging.basicConfig(
            level=getattr(logging, config.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.FileHandler('app.log'), logging.StreamHandler()]
        )
        self.logger = logging.getLogger(__name__)

    def setup_pages(self):
        self.dashboard_page = DashboardPage(self)
        self.ai_assistant_page = AIAssistantPage(self)
        self.analytics_page = AnalyticsPage(self)
        self.set_main_content(self.dashboard_page)
        self.set_active_page('dashboard')

    def setup_database(self):
        try:
            config = self.config_manager.get_config()
            db_config = DatabaseConfig(
                host=config.database.host,
                port=config.database.port,
                service_name=config.database.service_name,
                username=config.database.username,
                password=config.database.password
            )
            success = self.db_manager.configure(db_config, pool_size=10)
            self.update_connection_status(success)
            if success:
                self.logger.info("Database connection established successfully")
            else:
                self.logger.error("Database connection failed")
                self.show_database_error()
        except Exception as e:
            self.logger.error(f"DB setup error: {e}")
            self.show_database_error()

    def setup_ai_agent(self):
        try:
            config = self.config_manager.get_config()
            if config.ai.gemini_api_key:
                self.ai_agent = FinancialAIAgent(config.ai.gemini_api_key)
                self.logger.info("AI Agent initialized successfully")
        except Exception as e:
            self.logger.error(f"AI setup error: {e}")

    def setup_navigation(self):
        self.navigate_to_dashboard.connect(lambda: self.navigate("dashboard"))
        self.navigate_to_ai_assistant.connect(lambda: self.navigate("ai_assistant"))
        self.navigate_to_consolidation.connect(lambda: self.navigate("consolidation"))  # Alias
        self.navigate_to_analytics.connect(lambda: self.navigate("analytics"))
        self.navigate_to_reports.connect(lambda: self.navigate("reports"))
        self.navigate_to_company_setup.connect(lambda: self.navigate("company_setup"))
        self.navigate_to_settings.connect(lambda: self.show_message("Settings page not implemented"))

    def navigate(self, page_name: str):
        page_map = {
            'dashboard': self.dashboard_page,
            'ai_assistant': self.ai_assistant_page,
            'analytics': self.analytics_page,
        }
        page = page_map.get(page_name)
        if page:
            self.set_main_content(page)
            self.set_active_page(page_name)

    def show_message(self, msg: str):
        box = QMessageBox(self)
        box.setWindowTitle("Info")
        box.setText(msg)
        box.exec()

    def check_database_connection(self):
        def check():
            is_connected = self.db_manager.test_connection()
            self.update_connection_status(is_connected)
        threading.Thread(target=check, daemon=True).start()

    def update_connection_status(self, is_connected: bool):
        title = f"InstaFinZ AI Assistant - Oracle DB: {'Connected' if is_connected else 'Disconnected'}"
        self.setWindowTitle(title)
        if hasattr(self.current_page, 'update_db_status'):
            self.current_page.update_db_status(is_connected)

    def show_database_error(self):
        QMessageBox.critical(self, "DB Error", "Failed to connect to Oracle DB.")

    def get_database_manager(self): return self.db_manager
    def get_ai_agent(self): return self.ai_agent

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = MainApplication()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
