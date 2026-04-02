import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import base64

class RSACipher:
    def __init__(self):
        # Đường dẫn đến thư mục keys (dựa trên cấu trúc folder của bạn)
        self.key_dir = os.path.join(os.path.dirname(__file__), 'keys')
        if not os.path.exists(self.key_dir):
            os.makedirs(self.key_dir)

    def generate_keys(self):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        # Lưu Private Key
        with open(os.path.join(self.key_dir, 'privateKey.pem'), 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        # Lưu Public Key
        with open(os.path.join(self.key_dir, 'publicKey.pem'), 'wb') as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        return "Keys generated and saved in rsa/keys/"

    def encrypt(self, message):
        with open(os.path.join(self.key_dir, 'publicKey.pem'), 'rb') as f:
            public_key = serialization.load_pem_public_key(f.read())
        
        ciphertext = public_key.encrypt(
            message.encode(),
            padding.PKCS1v15()
        )
        return base64.b64encode(ciphertext).decode()

    def decrypt(self, ciphertext):
        with open(os.path.join(self.key_dir, 'privateKey.pem'), 'rb') as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
        
        raw_cipher = base64.b64decode(ciphertext)
        plaintext = private_key.decrypt(
            raw_cipher,
            padding.PKCS1v15()
        )
        return plaintext.decode()

    def sign(self, message):
        with open(os.path.join(self.key_dir, 'privateKey.pem'), 'rb') as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
        
        signature = private_key.sign(
            message.encode(),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode()

    def verify(self, message, signature):
        try:
            with open(os.path.join(self.key_dir, 'publicKey.pem'), 'rb') as f:
                public_key = serialization.load_pem_public_key(f.read())
            
            sig_bytes = base64.b64decode(signature)
            public_key.verify(
                sig_bytes,
                message.encode(),
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False