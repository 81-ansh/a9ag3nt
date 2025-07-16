# ui/base_window.py
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QFrame, QPushButton, QLineEdit, QSizePolicy)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QFont, QPixmap, QIcon, QAction

class BaseWindow(QMainWindow):
    """Base window class with common navigation and layout"""
    
    # Signals for navigation
    navigate_to_dashboard = Signal()
    navigate_to_ai_assistant = Signal()
    navigate_to_consolidation = Signal()
    navigate_to_analytics = Signal()
    navigate_to_reports = Signal()
    navigate_to_company_setup = Signal()
    navigate_to_settings = Signal()
    
    def __init__(self):
        super().__init__()
        self.current_page = None
        self.nav_buttons = {}
        self.setup_base_layout()
        self.setup_window_properties()
    
    def setup_window_properties(self):
        """Setup basic window properties"""
        self.setWindowTitle("Financial Data Manager")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Set window icon if available
        try:
            self.setWindowIcon(QIcon("icon.png"))
        except:
            pass
    
    def setup_base_layout(self):
        self.setStyleSheet("background-color: #fdfdfd;")
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left Sidebar
        self.left_panel = self.create_left_panel()

        # Right Panel (Header + Main Content)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Fixed Header
        header = self.create_header()
        right_layout.addWidget(header)

        # Dynamic Main Content Area
        self.main_content = QWidget()
        self.main_content.setStyleSheet("background-color: #ffffff;")
        self.main_content.setLayout(QVBoxLayout())
        right_layout.addWidget(self.main_content)

        # Add panels to main layout
        main_layout.addWidget(self.left_panel)
        main_layout.addWidget(right_panel)

    
    def create_left_panel(self) -> QWidget:
        """Create left navigation panel"""
        left_panel = QWidget()
        left_panel.setStyleSheet("background-color: #0A0A0A; color: white;")
        left_panel.setFixedWidth(250)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        
        # Logo/Header section
        header_section = self.create_sidebar_header()
        left_layout.addWidget(header_section)
        
        # Navigation buttons
        nav_section = self.create_navigation_section()
        left_layout.addWidget(nav_section)
        
        # Spacer to push footer to bottom
        left_layout.addStretch()
        
        # Footer section
        footer_section = self.create_footer_section()
        left_layout.addWidget(footer_section)
        
        return left_panel
    
    def create_sidebar_header(self) -> QWidget:
        """Create header section with logo and title"""
        header_widget = QWidget()
        header_widget.setStyleSheet("background-color: #1a1a1a;")
        header_widget.setFixedHeight(80)
        
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 10, 20, 10)
        header_layout.setSpacing(5)

        # Icon
        icon = QLabel()
        pixmap = QPixmap("ui/icons/bar_graph_icon.png").scaled(45, 45, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon.setPixmap(pixmap)
        icon.setMaximumWidth(50)

        # Title and Subtitle in vertical layout
        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)

        title_label = QLabel("InstaFinZ")
        title_label.setStyleSheet("color: #ffffff; font-size: 18px; font-weight: bold;")

        subtitle_label = QLabel("Smart Consolidation")
        subtitle_label.setStyleSheet("color: #888888; font-size: 12px; font-weight: bold;")

        text_layout.addWidget(title_label)
        text_layout.addWidget(subtitle_label)

        # Add icon and text layout to header layout
        header_layout.addWidget(icon)
        header_layout.addLayout(text_layout)

        return header_widget
    
    def create_header(self) -> QWidget:
        #Top Frame 1
        top_first_frame = QFrame()
        top_first_frame.setFixedHeight(60)
        top_first_frame.setStyleSheet("background-color: rgba(0, 0, 0, 150);")
        top_first_layout = QHBoxLayout(top_first_frame)
        top_first_layout.setContentsMargins(15, 10, 15, 10)

        #Side Panel Button
        side_panel_button = QPushButton()
        side_panel_button.setIcon(QIcon("ui/icons/sidepanel_icon.png"))
        side_panel_button.setIconSize(QSize(25, 25))
        side_panel_button.setFixedSize(40, 40)
        side_panel_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #36d399;
            }
        """)

        #Search Bar
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search transactions, companies...")
        search_bar.setFixedHeight(35)
        search_bar.setMaximumWidth(300)

        search_icon = QIcon("ui/icons/search_icon.png")
        search_action = QAction(search_icon, "", search_bar)
        search_bar.addAction(search_action, QLineEdit.LeadingPosition)
        search_bar.setStyleSheet("""
            QLineEdit {
                background-color: #262626;
                color: #ffffff;
                border-radius: 6px;
                padding-left: 6px;
                font-size: 14px;
            }
            QLineEdit::placeholder {
                color: #999999;
            }
        """)

        #Notification Button
        Notification_Button = QPushButton()
        Notification_Button.setIcon(QIcon("ui/icons/notification_icon.png"))
        Notification_Button.setIconSize(QSize(25, 25))
        Notification_Button.setFixedSize(40, 40)
        Notification_Button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #262626;
            }
        """)

        #Profile Button
        Profile_Button = QPushButton()
        Profile_Button.setIcon(QIcon("ui/icons/profile_icon.png"))
        Profile_Button.setIconSize(QSize(25, 25))
        Profile_Button.setFixedSize(40, 40)
        Profile_Button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #262626;
            }
        """)

        top_first_layout.addWidget(side_panel_button)
        top_first_layout.addWidget(search_bar)
        top_first_layout.addStretch()
        top_first_layout.addWidget(Notification_Button)
        top_first_layout.addWidget(Profile_Button)

        return top_first_frame

    def create_navigation_section(self) -> QWidget:
        """Create navigation buttons section"""
        nav_widget = QWidget()
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setContentsMargins(0, 20, 0, 0)
        nav_layout.setSpacing(2)
        
        # Navigation buttons data
        nav_items = [
            ("Dashboard", "ui/icons/dashboard_icon.png", self.navigate_to_dashboard),
            ("AI Assistant", "ui/icons/bot_icon.png", self.navigate_to_ai_assistant),
            ("Consolidation", "ui/icons/calculator_icon.png",self.navigate_to_consolidation ),
            ("Analytics", "ui/icons/analytics_icon.png",self.navigate_to_analytics ),
            ("Reports", "ui/icons/reports_icon.png", self.navigate_to_reports),
            ("Company Setup", "ui/icons/company_icon.png", self.navigate_to_company_setup),
            ("Settings", "ui/icons/settings_icon.png", self.navigate_to_settings)
        ]
        
        for text, icon, signal in nav_items:
            button = self.create_nav_button(text, icon, signal)
            nav_layout.addWidget(button)
            self.nav_buttons[text.lower().replace(' ', '_')] = button
        
        return nav_widget
    
    def create_nav_button(self, text: str, icon_path: str, signal) -> QPushButton:
        """Create a navigation button"""
        button = QPushButton(text)
        button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #ffffff;
                border: none;
                padding: 15px 20px;
                text-align: left;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #333333;
            }
            QPushButton:pressed {
                background-color: #444444;
            }
            QPushButton[active="true"] {
                background-color: #2d5aa0;
                border-left: 4px solid #4a9eff;
            }
        """)
        button.setFixedHeight(50)
        # Set icon from file
        icon = QIcon(icon_path)
        button.setIcon(icon)
        button.setIconSize(QSize(24, 24))
        button.clicked.connect(signal)
        return button

    def create_footer_section(self) -> QWidget:
        """Create footer section"""
        footer_widget = QWidget()
        footer_widget.setStyleSheet("border-top: 1px solid #333;")
        footer_widget.setFixedHeight(60)
        
        footer_layout = QVBoxLayout(footer_widget)
        footer_layout.setContentsMargins(20, 10, 20, 10)
        
        # Status indicator
        status_label = QLabel("🟢 Connected")
        status_label.setStyleSheet("color: #4CAF50; font-size: 12px;")
        
        # Version info
        version_label = QLabel("v1.0.0")
        version_label.setStyleSheet("color: #666666; font-size: 10px;")
        
        footer_layout.addWidget(status_label)
        footer_layout.addWidget(version_label)
        
        return footer_widget
    
    def set_active_page(self, page_name: str):
        """Set active page and update navigation button styles"""
        # Reset all buttons
        for button in self.nav_buttons.values():
            button.setProperty("active", "false")
            button.setStyleSheet(button.styleSheet())
        
        # Set active button
        if page_name in self.nav_buttons:
            self.nav_buttons[page_name].setProperty("active", "true")
            self.nav_buttons[page_name].setStyleSheet(self.nav_buttons[page_name].styleSheet())
        
        self.current_page = page_name
    
    def set_main_content(self, widget: QWidget):
        """Set the main content widget"""
        # Check if there is an existing widget, if yes, remove it
        if self.main_content.layout():
            while self.main_content.layout().count():
                child = self.main_content.layout().takeAt(0)
                if child.widget():
                    child.widget().setParent(None)  # Unset the parent to prevent deletion
                    
        # Add new content
        self.main_content.layout().addWidget(widget)
        
    
    def show_loading(self, message: str = "Loading..."):
        """Show loading indicator in main content"""
        loading_widget = QWidget()
        loading_layout = QVBoxLayout(loading_widget)
        loading_layout.setAlignment(Qt.AlignCenter)
        
        loading_label = QLabel(message)
        loading_label.setStyleSheet("color: #666666; font-size: 16px;")
        loading_label.setAlignment(Qt.AlignCenter)
        
        loading_layout.addWidget(loading_label)
        self.set_main_content(loading_widget)
    
    def show_error(self, message: str):
        """Show error message in main content"""
        error_widget = QWidget()
        error_layout = QVBoxLayout(error_widget)
        error_layout.setAlignment(Qt.AlignCenter)
        
        error_label = QLabel(f"❌ Error: {message}")
        error_label.setStyleSheet("color: #f44336; font-size: 16px;")
        error_label.setAlignment(Qt.AlignCenter)
        
        retry_button = QPushButton("Retry")
        retry_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        retry_button.clicked.connect(self.handle_retry)
        
        error_layout.addWidget(error_label)
        error_layout.addWidget(retry_button)
        self.set_main_content(error_widget)
    
    def handle_retry(self):
        """Handle retry button click - to be overridden by subclasses"""
        pass
    
    def update_status(self, message: str, is_connected: bool = True):
        """Update status in footer"""
        # This would update the status label in the footer
        # Implementation depends on how you want to handle status updates
        pass
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Cleanup code here if needed
        event.accept()