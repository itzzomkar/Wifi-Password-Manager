import sys
import os
import unittest

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from encryption import derive_key, encrypt_data, decrypt_data

class TestEncryption(unittest.TestCase):
    
    def test_derive_key(self):
        """Test key derivation from password"""
        password = "test_password_123"
        key, salt = derive_key(password)
        
        # Check that we get a 32-byte key
        self.assertEqual(len(key), 32)
        # Check that we get a 16-byte salt
        self.assertEqual(len(salt), 16)
        
        # Test that the same password produces the same key with the same salt
        key2, _ = derive_key(password, salt)
        self.assertEqual(key, key2)
    
    def test_encrypt_decrypt(self):
        """Test encryption and decryption"""
        password = "test_password_123"
        data = "This is a test message for encryption!"
        
        # Derive key
        key, _ = derive_key(password)
        
        # Encrypt data
        encrypted = encrypt_data(data, key)
        
        # Decrypt data
        decrypted = decrypt_data(encrypted, key)
        
        # Check that decrypted data matches original
        self.assertEqual(data, decrypted)
    
    def test_different_keys(self):
        """Test that different passwords produce different keys"""
        password1 = "password1"
        password2 = "password2"
        
        key1, _ = derive_key(password1)
        key2, _ = derive_key(password2)
        
        self.assertNotEqual(key1, key2)

if __name__ == '__main__':
    unittest.main()