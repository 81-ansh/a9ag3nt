from PySide6.QtWidgets import QWidget, QMessageBox, QFileDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout, QFrame
from PySide6.QtCore import Qt, QSize, QEvent
from PySide6.QtGui import QPixmap, QFont, QIcon
import threading
import google.generativeai as genai
genai.configure(api_key="YOUR_API_KEY")


model = genai.GenerativeModel("gemini-2.5-flash")

class AIAssistantPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.ai_agent = main_window.get_ai_agent()
        self.uploaded_file_content = ""

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        header_layout = QHBoxLayout()
        #bot icon
        icon = QLabel()
        icon_pixmap = QPixmap("ui/icons/bot_icon_black.png").scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon.setContentsMargins(10, 0, 10, 0)
        icon.setMaximumWidth(70)
        icon.setPixmap(icon_pixmap)
        text_layout = QVBoxLayout()

        title = QLabel("AI Assistant")
        title.setFont(QFont("Segoe UI"))
        title.setStyleSheet("color: #000000; font-size: 24px; font-weight: bold;")
        
        subtitle = QLabel("Your intelligent financial consolidation companion")
        subtitle.setStyleSheet("color: #000000")
        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)

        # Add icon and text to header layout
        header_layout.addWidget(icon)
        header_layout.addLayout(text_layout)

        # Add header layout to main layout
        layout.addLayout(header_layout)

        self.setLayout(layout)

        # Bottom Frames Container (chat + sidebar)
        bottom_frames_container = QWidget()
        bottom_frames_container.setStyleSheet("background-color: transparent; border-radius: 14px;")
        bottom_frames_container.setMaximumWidth(1500)
        bottom_frames_layout = QHBoxLayout(bottom_frames_container)
        bottom_frames_layout.setContentsMargins(0, 0, 0, 0)
        bottom_frames_layout.setSpacing(20)
        layout.addWidget(bottom_frames_container)

        # Outer Chat Frame
        outer_chat_frame = QFrame()
        outer_chat_frame.setStyleSheet("background-color: transparent; border-radius: 12px;")
        outer_chat_layout = QVBoxLayout(outer_chat_frame)
        outer_chat_layout.setContentsMargins(15, 15, 15, 15)

        # Chat Frame
        chat_frame = QFrame()
        chat_frame.setStyleSheet("background-color: #ffffff; border: 1px solid #cccccc; border-radius: 10px;")
        chat_layout = QVBoxLayout(chat_frame)
        chat_layout.setSpacing(10)
        chat_frame.setContentsMargins(0, 10, 0, 10)

        icon_label = QLabel()
        icon_pixmap = QPixmap("ui/icons/message_icon.png").scaled(25, 25, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setContentsMargins(10, 0, 5, 0)
        icon_label.setStyleSheet("border: 0px;")
        icon_label.setPixmap(icon_pixmap)
        
        header = QLabel("Conversation")
        header.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header.setStyleSheet("color: black; border: 0px;")
        header_layout = QHBoxLayout()
        header_layout.addWidget(icon_label)
        header_layout.addWidget(header)
        header_layout.addStretch()
        chat_layout.addLayout(header_layout)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setContentsMargins(0,0,0,0)
        self.chat_display.setStyleSheet("background-color: #f2f2f2; border-radius:0px; color: black; font-size: 14px;")
        chat_layout.addWidget(self.chat_display)

        input_layout = QHBoxLayout()

        # Upload File Button
        self.upload_button = QPushButton()
        self.upload_button.setIcon(QIcon("ui/icons/plus_icon.png"))
        self.upload_button.setFixedSize(44, 44)
        self.upload_button.setStyleSheet("""
            QPushButton {
                background-color: #09173f;
                border: none;
                border-radius: 10px;
                color: white;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #47526f;
            }
        """)
        self.upload_button.clicked.connect(self.upload_file)

        self.textbox = QTextEdit()
        self.textbox.setFixedHeight(40)
        self.textbox.setStyleSheet("background-color: #e0e0e0; color: black; font-size: 16px")
        self.textbox.setViewportMargins(10, 5, 0, 0)
        self.textbox.installEventFilter(self)
        self.send_button = QPushButton()
        self.send_button.setIcon(QIcon("ui/icons/send_icon.png"))
        self.send_button.setIconSize(QSize(24, 24))  # Adjust icon size
        self.send_button.setFixedSize(44, 44)  # Optional: square button
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #09173f;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #47526f;
            }
        """)
        self.send_button.clicked.connect(self.send_message)

        input_layout.addWidget(self.upload_button)
        input_layout.addWidget(self.textbox)
        input_layout.addWidget(self.send_button)
        chat_layout.addLayout(input_layout)

        outer_chat_layout.addWidget(chat_frame)

        # Side Panel Frame
        side_outer_frame = QFrame()
        side_outer_frame.setStyleSheet("background-color: transparent; border-radius: 12px;")
        side_outer_layout = QVBoxLayout(side_outer_frame)
        side_outer_layout.setContentsMargins(15, 15, 15, 20)

        side_panel = QWidget()
        side_layout = QVBoxLayout(side_panel)
        side_layout.setSpacing(60)

        # Quick Actions
        action_frame = QFrame()
        action_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                color: black;
                border: 1px solid #cccccc;
                border-radius: 10px;
            }
        """)
        action_layout = QVBoxLayout(action_frame)
        action_layout.setContentsMargins(20, 20, 20, 20)
        action_layout.setSpacing(15)
        action_frame.setMaximumHeight(600)
        action_frame.setMinimumHeight(300)

        quick_actions_label = QLabel("Quick Actions")
        quick_actions_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        quick_actions_label.setStyleSheet("border:0px;")
        action_layout.addWidget(quick_actions_label)


        #Analyze Variances  
        analyze_variances_button = QPushButton()
        analyze_variances_button.setMinimumHeight(60)
        analyze_variances_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                border: none;
                border-radius: 8px;
                border: 1px solid #cccccc;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #36d399;
                color:#000000
            }
        """)

        # Create icon
        icon_label = QLabel()
        icon_pixmap = QPixmap("ui/icons/analytics_icon_black.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setStyleSheet("background-color:transparent; border: 0px;")
        icon_label.setMaximumWidth(30)

        # Create title and subtitle labels
        title_label = QLabel("Analyze Variances")
        title_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        title_label.setStyleSheet("color: #000000; border:0px; background-color: transparent")
        subtitle_label = QLabel("Find discrepancies in consolidation data")
        subtitle_label.setStyleSheet("color: #444444; border:0px; background-color: transparent; font-size: 11px;")

        # Create vertical layout for text
        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)
        text_layout.addWidget(title_label)
        text_layout.addWidget(subtitle_label)

        # Main layout inside button
        btn_layout = QHBoxLayout(analyze_variances_button)
        btn_layout.addWidget(icon_label)
        btn_layout.addLayout(text_layout)
        

        # Add to layout
        action_layout.addWidget(analyze_variances_button)


        #Generate Report  
        generate_report_button = QPushButton()
        generate_report_button.setMinimumHeight(60)
        generate_report_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                border: none;
                border-radius: 8px;
                border: 1px solid #cccccc;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #36d399;
                color:#000000
            }
        """)

        # Create icon
        icon_label = QLabel()
        icon_pixmap = QPixmap("ui/icons/reports_icon_black.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setStyleSheet("background-color:transparent; border:0px;")
        icon_label.setMaximumWidth(30)

        # Create title and subtitle labels
        title_label = QLabel("Generate Report")
        title_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        title_label.setStyleSheet("color: #000000; border:0px; background-color: transparent")

        subtitle_label = QLabel("Create comprehensive financial reports")
        subtitle_label.setStyleSheet("color: #444444; border:0px; background-color: transparent; font-size: 11px;")

        # Create vertical layout for text
        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)
        text_layout.addWidget(title_label)
        text_layout.addWidget(subtitle_label)

        # Main layout inside button
        btn_layout = QHBoxLayout(generate_report_button)
        btn_layout.addWidget(icon_label)
        btn_layout.addLayout(text_layout)
        
        # Add to layout
        action_layout.addWidget(generate_report_button)

        #Calculate Adjustments
        Calculate_adjustments_button = QPushButton()
        Calculate_adjustments_button.setMinimumHeight(60)
        Calculate_adjustments_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                border: none;
                border-radius: 8px;
                border: 1px solid #cccccc;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #36d399;
                color:#000000
            }
        """)

        # Create icon
        icon_label = QLabel()
        icon_pixmap = QPixmap("ui/icons/calculator_icon_black.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setStyleSheet("background-color:transparent; border:0px;")
        icon_label.setMaximumWidth(30)

        # Create title and subtitle labels
        title_label = QLabel("Calculate Adjustments")
        title_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        title_label.setStyleSheet("color: #000000; border:0px; background-color: transparent")

        subtitle_label = QLabel("Compute elimination entries")
        subtitle_label.setStyleSheet("color: #444444; border:0px; background-color: transparent; font-size: 11px;")

        # Create vertical layout for text
        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)
        text_layout.addWidget(title_label)
        text_layout.addWidget(subtitle_label)

        # Main layout inside button
        btn_layout = QHBoxLayout(Calculate_adjustments_button)
        btn_layout.addWidget(icon_label)
        btn_layout.addLayout(text_layout)
        
        # Add to layout
        action_layout.addWidget(Calculate_adjustments_button)

        #Smart Insights
        smart_insights_button = QPushButton()
        smart_insights_button.setMinimumHeight(60)
        smart_insights_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                border: none;
                border-radius: 8px;
                border: 1px solid #cccccc;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #36d399;
                color:#000000
            }
        """)

        # Create icon
        icon_label = QLabel()
        icon_pixmap = QPixmap("ui/icons/brain_icon.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setStyleSheet("background-color:transparent; border:0px;")
        icon_label.setMaximumWidth(30)

        # Create title and subtitle labels
        title_label = QLabel("Smart Insights")
        title_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        title_label.setStyleSheet("color: #000000; border:0px; background-color: transparent")

        subtitle_label = QLabel("Get AI-powered financial insights")
        subtitle_label.setStyleSheet("color: #444444; border:0px; background-color: transparent; font-size: 11px;")

        # Create vertical layout for text
        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)
        text_layout.addWidget(title_label)
        text_layout.addWidget(subtitle_label)

        # Main layout inside button
        btn_layout = QHBoxLayout(smart_insights_button)
        btn_layout.addWidget(icon_label)
        btn_layout.addLayout(text_layout)
        
        # Add to layout
        action_layout.addWidget(smart_insights_button)

        # AI Capabilities
        capabilities_frame = QFrame()
        capabilities_frame.setStyleSheet("background-color: #ffffff;border: 1px solid #cccccc; color: black; border-radius: 10px;")
        capabilities_frame.setMaximumHeight(600)
        capabilities_layout = QVBoxLayout(capabilities_frame)
        capabilities_layout.setContentsMargins(20, 20, 20, 20)
        capabilities_layout.setSpacing(10)

        capabilities_label = QLabel("AI Capabilities")
        capabilities_label.setStyleSheet("border: 0px;")
        capabilities_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        capabilities_layout.addWidget(capabilities_label)

        capabilities = [
            "Variance analysis and anomaly detection",
            "Automated consolidation insights",
            "Real-time financial analysis",
            "Custom report generation"
        ]
        for cap in capabilities:
            label = QLabel(f"• {cap}")
            label.setStyleSheet("font-size: 14px; border: 0px;")
            capabilities_layout.addWidget(label)

        side_layout.addWidget(action_frame)
        side_layout.addWidget(capabilities_frame)
        side_layout.addStretch()

        side_panel.setLayout(side_layout)
        side_outer_layout.addWidget(side_panel)

        # Combine both panels
        bottom_frames_layout.addWidget(outer_chat_frame, 3)
        bottom_frames_layout.addWidget(side_outer_frame, 1)


    def eventFilter(self, source, event):
        if source == self.textbox and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return and not event.modifiers() & Qt.ShiftModifier:
                self.send_message()
                return True
        return super().eventFilter(source, event)

    def send_message(self):
        message = self.textbox.toPlainText().strip()
        if message:
            self.chat_display.append(f"<b style='color:#03a9f4;'>You:</b> {message}")
            self.textbox.clear()

            # If file content exists, send it with the message
            if self.uploaded_file_content:
                full_prompt = f"{message}\n\n[Uploaded File Content Below:]\n{self.uploaded_file_content}"
            else:
                full_prompt = message

            threading.Thread(target=self.get_ai_response, args=(full_prompt,), daemon=True).start()

    def get_ai_response(self, message):
        try:
            # Wrap user message with a prompt to simplify the language
            simple_prompt = (
                "You are a financial AI assistant.\n"
                "And if the user attach a excel file then make a table of it.\n"
                "Summarize the data.\n"
                "If the user's input contains financial entries or accounting balances, convert it into a clean, structured table with relevant columns like Account Code, Account Name, Account Type, Debit, Credit, Currency, Month, Year, etc.\n"
                "Always try to guess appropriate headers based on data and explain the table briefly.\n"
                "If no table is possible, just respond normally in simple sentences.\n\n"
                f"User's input:\n{message}"
            )

            response = model.generate_content(simple_prompt)

            if response.text:
                plain_text = response.text.strip()
                self.chat_display.append(f"<b style='color:#00c853;'>AI:</b> {plain_text}")

        except Exception as e:
            self.chat_display.append(f"<span style='color:red;'>[Error: {str(e)}]</span>")

    def upload_file(self):
        import pandas as pd
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select File", "", "Supported Files (*.txt *.pdf *.xlsx *.xls)"
        )
        
        if file_path:
            try:
                content = self.read_file_content(file_path)
                self.uploaded_file_content = content

                
                file_name = file_path.split("/")[-1]
                self.chat_display.append(f"""
                    <div style='color:#155724; padding:8px; border-radius:8px; margin:5px 0;'>
                    📁 <b>{file_name}</b> uploaded successfully!
                    </div>
                """)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not read file:\n{str(e)}")  


    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            file_name = file_path.split("/")[-1]
            self.file_label.setText(file_name)
            self.file_label.setStyleSheet("padding: 5px;")
            self.file_frame_widget.show()

    def clear_file(self):
        self.file_label.setText("")
        self.file_frame_widget.hide()

    #File Reading Logic
    def read_file_content(self, file_path):
        if file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

        elif file_path.endswith(".pdf"):
            from PyPDF2 import PdfReader
            reader = PdfReader(file_path)
            return "\n".join([page.extract_text() or "" for page in reader.pages])

        elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
            import pandas as pd
            df = pd.read_excel(file_path, sheet_name=None)  # All sheets
            all_text = []
            for sheet, data in df.items():
                all_text.append(f"--- Sheet: {sheet} ---")
                all_text.append(data.to_string(index=False))  # Tabular text
            return "\n\n".join(all_text)

        else:
            raise ValueError("Unsupported file type.")
        
    def get_excel_table_html(self, file_path):
        import pandas as pd
        df_sheets = pd.read_excel(file_path, sheet_name=None)
        html_output = ""
        for sheet_name, df in df_sheets.items():
            html_output += f"<h3>{sheet_name}</h3>"
            html_output += df.to_html(index=False, border=0, classes='excel-table')
        return html_output
    
    def convert_to_html_table(self, raw_text):
        import re
        rows = []
        lines = raw_text.split('*')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            match = re.match(r'\*\*(.*?) \(Account (\d+)\):\*\* You have a (debit|credit) balance of \$(.*)\.', line)
            if match:
                name, account_number, balance_type, amount = match.groups()
                rows.append((name, account_number, balance_type.capitalize(), f"${amount}"))

        html_table = """
        <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; font-family: Segoe UI;">
            <thead style="background-color: #36d399; color: black;">
                <tr>
                    <th>Account Name</th>
                    <th>Account Number</th>
                    <th>Type</th>
                    <th>Amount</th>
                </tr>
            </thead>
            <tbody>
        """
        for row in rows:
            html_table += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
        html_table += "</tbody></table>"
        return html_table


    def clear_file(self):
        self.file_label.setText("")
        self.file_frame_widget.hide()   

    def update_db_status(self, is_connected: bool):
        # Could add logic to enable/disable AI query based on DB status
        pass
