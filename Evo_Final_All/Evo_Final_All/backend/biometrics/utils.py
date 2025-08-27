import base64, json
from pathlib import Path
from utils import encrypt_bytes, decrypt_bytes, get_or_create_key

STORAGE = Path('biom_data'); STORAGE.mkdir(exist_ok=True)

def enroll_face(username: str, image_b64: str):
    data = base64.b64decode(image_b64.split(',',1)[-1])
    path = STORAGE / f"{username}_face.enc"
    # store encrypted raw image bytes (prototype). In prod, store templates, not raw images.
    encrypted = encrypt_bytes(data)
    with open(path, 'wb') as f:
        f.write(encrypted)
    return {'ok': True, 'path': str(path)}

def verify_face(username: str, image_b64: str):
    path = STORAGE / f"{username}_face.enc"
    if not path.exists():
        return {'ok': False, 'match': False}
    # naive compare: decrypt stored and compare bytes (not reliable) - placeholder
    data = base64.b64decode(image_b64.split(',',1)[-1])
    stored = decrypt_bytes(path.read_bytes())
    match = data == stored
    return {'ok': True, 'match': match}