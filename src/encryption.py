import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import base64
import os

def derive_key(master_password: str, salt: bytes = None) -> tuple:
    """
    Derive a key from the master password using PBKDF2.
    
    Args:
        master_password (str): The master password
        salt (bytes): Optional salt. If None, a new salt will be generated.
        
    Returns:
        tuple: (derived_key, salt)
    """
    if salt is None:
        salt = get_random_bytes(16)  # 128-bit salt
    
    # Derive a 256-bit key using PBKDF2
    key = PBKDF2(master_password, salt, dkLen=32, count=100000)
    return key, salt

def encrypt_data(data: str, key: bytes) -> str:
    """
    Encrypt data using AES-256 in CBC mode.
    
    Args:
        data (str): The data to encrypt
        key (bytes): The encryption key
        
    Returns:
        str: Base64 encoded encrypted data (IV + ciphertext)
    """
    # Convert data to bytes
    data_bytes = data.encode('utf-8')
    
    # Create cipher
    cipher = AES.new(key, AES.MODE_CBC)
    
    # Pad data to be multiple of 16 bytes (AES block size)
    padding_length = 16 - (len(data_bytes) % 16)
    data_bytes += bytes([padding_length]) * padding_length
    
    # Encrypt data
    ciphertext = cipher.encrypt(data_bytes)
    
    # Combine IV and ciphertext
    encrypted_data = cipher.iv + ciphertext
    
    # Return base64 encoded result
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt_data(encrypted_data: str, key: bytes) -> str:
    """
    Decrypt data using AES-256 in CBC mode.
    
    Args:
        encrypted_data (str): Base64 encoded encrypted data (IV + ciphertext)
        key (bytes): The decryption key
        
    Returns:
        str: Decrypted data
    """
    # Decode base64
    encrypted_bytes = base64.b64decode(encrypted_data)
    
    # Extract IV and ciphertext
    iv = encrypted_bytes[:16]
    ciphertext = encrypted_bytes[16:]
    
    # Create cipher
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    
    # Decrypt data
    decrypted_data = cipher.decrypt(ciphertext)
    
    # Remove padding
    padding_length = decrypted_data[-1]
    decrypted_data = decrypted_data[:-padding_length]
    
    # Return decoded string
    return decrypted_data.decode('utf-8')