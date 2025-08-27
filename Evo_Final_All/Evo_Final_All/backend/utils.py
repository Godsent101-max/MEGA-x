import os
from cryptography.fernet import Fernet
from pathlib import Path

KEY_PATH = Path('secret.key')

def get_or_create_key():
    # use env var if set, else generate/save a local key (for prototype only)
    k = os.getenv('EVO_FERNET_KEY')
    if k:
        return k.encode('utf-8') if isinstance(k, str) else k
    if KEY_PATH.exists():
        return KEY_PATH.read_bytes()
    k = Fernet.generate_key()
    KEY_PATH.write_bytes(k)
    return k

def encrypt_bytes(b: bytes) -> bytes:
    from cryptography.fernet import Fernet
    f = Fernet(get_or_create_key())
    return f.encrypt(b)

def decrypt_bytes(token: bytes) -> bytes:
    from cryptography.fernet import Fernet
    f = Fernet(get_or_create_key())
    return f.decrypt(token)