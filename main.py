import sys
import random
import string
#simple GUI Vigenere cipher client
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
)
#gfm wz iaqfbax gvwv 
class VigenereGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("noodle Cipher")
        self.setFixedSize(900, 600)

        self.background = QPixmap("images/bg.png")
        title = QLabel("NOODLE CIPHER")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")

        plain_label = QLabel("PLAIN TEXT")
        plain_label.setStyleSheet("color: white; font-size: 16px;")

        self.plain_text = QTextEdit()
        self.plain_text.setPlaceholderText("Enter plain text...")
        self.plain_text.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 170);
                color: white;
                border: 2px solid #555;
                border-radius: 8px;
                padding: 10px;
                font-size: 15px;
            }
        """)

        encrypted_label = QLabel("ENCRYPTED TEXT")
        encrypted_label.setStyleSheet("color: white; font-size: 16px;")

        self.encrypted_text = QTextEdit()
        self.encrypted_text.setPlaceholderText("Encrypted text...")
        self.encrypted_text.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 170);
                color: white;
                border: 2px solid #555;
                border-radius: 8px;
                padding: 10px;
                font-size: 15px;
            }
        """)
        key_label = QLabel("KEY")
        key_label.setStyleSheet("color: white; font-size: 16px;")

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Enter key...")
        self.key_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(0, 0, 0, 170);
                color: white;
                border: 2px solid #555;
                border-radius: 8px;
                padding: 10px;
                font-size: 15px;
            }
        """)

        encrypt_button = QPushButton("ENCRYPT")
        decrypt_button = QPushButton("DECRYPT")
        random_button = QPushButton("RANDOM KEY")

        button_style = """
            QPushButton {
                background-color: rgba(0, 0, 0, 200);
                color: white;
                border: 2px solid #666;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: rgba(50, 50, 50, 220);
            }

            QPushButton:pressed {
                background-color: rgba(90, 90, 90, 220);
            }
        """

        encrypt_button.setStyleSheet(button_style)
        decrypt_button.setStyleSheet(button_style)
        random_button.setStyleSheet(button_style)

        encrypt_button.clicked.connect(self.encrypt)
        decrypt_button.clicked.connect(self.decrypt)
        random_button.clicked.connect(self.generate_key)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(12)
        main_layout.addWidget(title)
        main_layout.addSpacing(10)
        text_layout = QHBoxLayout()
        text_layout.setSpacing(20)
        left_layout = QVBoxLayout()
        left_layout.addWidget(plain_label)
        left_layout.addWidget(self.plain_text)
        right_layout = QVBoxLayout()
        right_layout.addWidget(encrypted_label)
        right_layout.addWidget(self.encrypted_text)
        text_layout.addLayout(left_layout)
        text_layout.addLayout(right_layout)
        main_layout.addLayout(text_layout)
        main_layout.addWidget(key_label)
        main_layout.addWidget(self.key_input)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.addWidget(encrypt_button)
        button_layout.addWidget(decrypt_button)
        button_layout.addWidget(random_button)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.background.isNull():
            scaled = self.background.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
        painter.fillRect(
            self.rect(),
            QColor(0, 0, 0, 100)
        )

    def vigenere(self, text, key, decrypt=False):
        key = ''.join(c for c in key.upper() if c.isalpha())
        if not key:
            return text
        result = []
        key_index = 0
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                shift = ord(key[key_index % len(key)]) - ord('A')
                if decrypt:
                    shift = -shift
                new_char = chr(
                    (ord(char) - base + shift) % 26 + base
                )
                result.append(new_char)
                key_index += 1
            else:
                result.append(char)
        return ''.join(result)
      
    def encrypt(self):
        text = self.plain_text.toPlainText()
        key = self.key_input.text()
        if not key:
            return
        encrypted = self.vigenere(text, key)
        self.encrypted_text.setPlainText(encrypted)

    def decrypt(self):
        text = self.encrypted_text.toPlainText()
        key = self.key_input.text()
        if not key:
            return
        decrypted = self.vigenere(text, key, decrypt=True)
        self.plain_text.setPlainText(decrypted)
      
    def generate_key(self):
        length = 16
        key = ''.join(
            random.choice(string.ascii_uppercase)
            for _ in range(length)
        )
        self.key_input.setText(key)
      
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = VigenereGUI()
    window.show()

    sys.exit(app.exec())
