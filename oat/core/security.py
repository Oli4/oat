import base64
from io import StringIO

import pandas as pd
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def get_fernet(password):
    # 16 bytes of salt. I chose it to be constant because the key stays on the
    # users machine and otherwise I would have to store the salt somewhere.
    SALT = b'\x1e\x97\x83<S\xaf0}\x1f\xa2,-jc\x93\x82'
    password = password.encode("utf8")
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=SALT,
                     iterations=100000, backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return Fernet(key)


def get_local_patient_info(path, fernet):
    with open(path, "rb") as myfile:
        contents = myfile.read()
        return pd.read_csv(StringIO(fernet.decrypt(contents).decode('utf8')))
