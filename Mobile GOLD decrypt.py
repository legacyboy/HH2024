import base64
from Crypto.Cipher import AES

# Example: The provided encryption key (Base64 encoded)
ek = base64.b64decode("rmDJ1wJ7ZtKy3lkLs6X9bZ2Jvpt6jL6YWiDsXtgjkXw=")

# Base64 encoded IV string (replace with the actual IV)
iv_base64 = "Q2hlY2tNYXRlcml4"  # replace with actual Base64 IV

# Decode the Base64 encoded IV
iv = base64.b64decode(iv_base64)

# Ensure the IV is exactly 12 bytes for AES/GCM (standard for GCM mode)
if len(iv) != 12:
    raise ValueError("The IV must be 12 bytes long for AES/GCM.")

# Array of Base64 encoded ciphertexts (replace with your actual ciphertexts)
ciphertexts_base64 = [
        "L2HD1a45w7EtSN41J7kx/hRgPwR8lDBg9qUicgz1qhRgSg==", "IWna1u1qu/4LUNVrbpd8riZ+w9oZNN1sPRS2ujQpMqAAt114Yw==", "MWfO0+M1t5IvQtN2ad9w3hp81sYQIIaX6veq03bnk6I4H/1n89gW", "LmHJ164506skXdh3K9MZ/BBiw90TRO2mD0Hp9Nuoxu4ghx5/WQ==", "J2XF2645xKciX9RgK9MR+wZ60NIbKIsOTRSHP0jkBJPaF0djlqbc", "LGfJ0q451qslWt14aZd8rjtr1ZMtJItIvrKk8RRQWh2U6bQSEdPga59XDQ==", "LWTBzOt4u/4KXt99aJ18riBgy8cSJcpvtrKnM4IEsMDr9AwtlSJW+S/jdoHvXA==", "I2HM3+w1t4opQ953c5x8rjZvzNITIEFFaMC3bP4bW/FptwSEIzo=", "K3vJ2Od1+79qEeN2apZ8rjx6w98OKXRQNvvj/tYXj2mFoDhaZw==", "O33D06452K0nWtA1J7kx/hRgtZNzI71BDpxorJ6mxImw/A==",

, "J2zf2/B95PJmf9RuJ7k1/AZr259XFLll5xvRfxu/YDOTFR460RwK+Q=="
]

# Function to decrypt each ciphertext
def decrypt_ciphertexts(ciphertexts_base64):
    for ciphertext_base64 in ciphertexts_base64:
        # Base64 decode the ciphertext and tag
        ciphertext_with_tag = base64.b64decode(ciphertext_base64)
        
        # Split the ciphertext and tag (assuming the last 16 bytes are the tag)
        ciphertext = ciphertext_with_tag[:-16]  # Ciphertext without tag
        tag = ciphertext_with_tag[-16:]  # Last 16 bytes as tag

        # Initialize the cipher in AES/GCM mode
        cipher = AES.new(ek, AES.MODE_GCM, nonce=iv)

        try:
            # Decrypt and authenticate
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            print(f"Decrypted text: {plaintext.decode('utf-8')}")
        except ValueError as e:
            print(f"Decryption failed: {str(e)}")

# Decrypt the array of ciphertexts
decrypt_ciphertexts(ciphertexts_base64)
