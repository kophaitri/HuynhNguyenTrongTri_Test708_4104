import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
# Đảm bảo đường dẫn import đúng theo cấu trúc folder rsa1
from rsa.rsa_cipher import RSACipher 
from ui.rsa import Ui_MainWindow # type: ignore

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cipher = RSACipher()
        
        # Kết nối nút bấm
        self.ui.btn_gen_keys.clicked.connect(self.handle_gen_keys)
        self.ui.btn_encrypt.clicked.connect(self.handle_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.handle_decrypt)
        self.ui.btn_sign.clicked.connect(self.handle_sign)
        self.ui.btn_verify.clicked.connect(self.handle_verify)

    def handle_gen_keys(self):
        res = self.cipher.generate_keys()
        QMessageBox.information(self, "Success", res)

    def handle_encrypt(self):
        try:
            text = self.ui.txt_plain_text.toPlainText()
            if not text: return
            result = self.cipher.encrypt(text)
            self.ui.txt_cipher_text.setPlainText(result)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Lỗi: {str(e)}")

    def handle_decrypt(self):
        try:
            cipher = self.ui.txt_cipher_text.toPlainText()
            if not cipher: return
            result = self.cipher.decrypt(cipher)
            self.ui.txt_plain_text.setPlainText(result)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Lỗi: {str(e)}")

    def handle_sign(self):
        try:
            text = self.ui.txt_info.toPlainText()
            if not text: return
            result = self.cipher.sign(text)
            self.ui.txt_sign.setPlainText(result)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Lỗi: {str(e)}")

    def handle_verify(self):
        try:
            text = self.ui.txt_info.toPlainText()
            sig = self.ui.txt_sign.toPlainText()
            if not text or not sig: return
            valid = self.cipher.verify(text, sig)
            if valid:
                QMessageBox.information(self, "Result", "Chữ ký HỢP LỆ!")
            else:
                QMessageBox.warning(self, "Result", "Chữ ký SAI!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Lỗi: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())