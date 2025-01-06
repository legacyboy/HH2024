from cryptography.hazmat.primitives import serialization, padding
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding
from cryptography.hazmat.backends import default_backend
import base64

def decrypt_with_rsa(encrypted_key_hex, private_key_pem):
    # Load the private key
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None,
        backend=default_backend()
    )
    
    # Convert hex string to bytes
    encrypted_data = bytes.fromhex(encrypted_key_hex)
    
    # Decrypt the data
    decrypted_data = private_key.decrypt(
        encrypted_data,
        asymmetric_padding.PKCS1v15()
    )
    
    return decrypted_data

# Your encrypted key and private key
encrypted_key = "1f4....a07"

private_key = """-----BEGIN RSA PRIVATE KEY-----
MII...hI=
-----END RSA PRIVATE KEY-----"""

try:
    # Attempt to decrypt
    decrypted_data = decrypt_with_rsa(encrypted_key, private_key)
    
    # Try to decode as various formats
    print("Decrypted data as hex:", decrypted_data.hex())
    try:
        print("Decrypted data as UTF-8:", decrypted_data.decode('utf-8'))
    except UnicodeDecodeError:
        print("Data is not valid UTF-8")
    try:
        print("Decrypted data as base64:", base64.b64encode(decrypted_data).decode())
    except:
        print("Could not encode as base64")
        
except Exception as e:
    print(f"Decryption failed: {str(e)}")
