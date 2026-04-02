import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from playfair_ui import Ui_MainWindow
from playfair_cipher import PlayFairCipher

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Khởi tạo class thuật toán
        self.cipher_logic = PlayFairCipher()
        
        # Nối nút bấm với hàm xử lý
        self.ui.btn_encrypt.clicked.connect(self.encrypt_data)
        self.ui.btn_decrypt.clicked.connect(self.decrypt_data)

    def encrypt_data(self):
        # Đã sửa thành toPlainText() cho phù hợp với QPlainTextEdit của bạn
        plaintext = self.ui.txt_plain.toPlainText()
        key = self.ui.txt_key.toPlainText()
        
        if plaintext and key:
            matrix = self.cipher_logic.tao_ma_tran_playfair(key) 
            ciphertext = self.cipher_logic.ma_hoa_playfair(plaintext, matrix)
            # Đã sửa thành setPlainText()
            self.ui.txt_cipher.setPlainText(ciphertext)

    def decrypt_data(self):
        # Đã sửa thành toPlainText()
        ciphertext = self.ui.txt_cipher.toPlainText()
        key = self.ui.txt_key.toPlainText()
        
        if ciphertext and key:
            matrix = self.cipher_logic.tao_ma_tran_playfair(key)
            decrypted = self.cipher_logic.giai_ma_playfair(ciphertext, matrix)
            # Đã sửa thành setPlainText()
            self.ui.txt_plain.setPlainText(decrypted)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())