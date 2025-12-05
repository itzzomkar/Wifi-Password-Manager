import json
import os
import base64
from typing import Dict, List, Optional
from encryption import derive_key, encrypt_data, decrypt_data

DB_FILE = "wifi_data.enc"
MASTER_KEY_FILE = "master_key.hash"

class DatabaseManager:
    def __init__(self):
        self.key = None
        self.salt = None
        
    def initialize_database(self, master_password: str) -> bool:
        """
        Initialize the database with a master password.
        
        Args:
            master_password (str): The master password
            
        Returns:
            bool: True if initialization successful, False otherwise
        """
        # Check if database already exists
        if os.path.exists(DB_FILE):
            return self.unlock_database(master_password)
        else:
            # Create new database
            key, salt = derive_key(master_password)
            self.key = key
            self.salt = salt
            
            # Create empty database
            empty_db = encrypt_data(json.dumps([]), key)
            with open(DB_FILE, 'w') as f:
                f.write(empty_db)
            
            # Save key hash for verification
            self._save_master_key_hash(master_password, salt)
            return True
    
    def unlock_database(self, master_password: str) -> bool:
        """
        Unlock the database with the master password.
        
        Args:
            master_password (str): The master password
            
        Returns:
            bool: True if unlocked successfully, False otherwise
        """
        # Verify master password
        if not self._verify_master_password(master_password):
            return False
            
        # Load salt
        if os.path.exists(MASTER_KEY_FILE):
            with open(MASTER_KEY_FILE, 'r') as f:
                data = json.load(f)
                self.salt = base64.b64decode(data['salt'])
        
        # Derive key
        self.key, _ = derive_key(master_password, self.salt)
        
        # Test decryption
        try:
            self._load_data()
            return True
        except Exception:
            return False
    
    def _verify_master_password(self, master_password: str) -> bool:
        """
        Verify the master password against the saved hash.
        
        Args:
            master_password (str): The master password to verify
            
        Returns:
            bool: True if password is correct, False otherwise
        """
        if not os.path.exists(MASTER_KEY_FILE):
            return True  # First time setup
            
        with open(MASTER_KEY_FILE, 'r') as f:
            data = json.load(f)
            saved_hash = data['hash']
            salt = base64.b64decode(data['salt'])
            
        key, _ = derive_key(master_password, salt)
        key_hash = base64.b64encode(key).decode('utf-8')
        
        return key_hash == saved_hash
    
    def _save_master_key_hash(self, master_password: str, salt: bytes):
        """
        Save the master key hash for verification.
        
        Args:
            master_password (str): The master password
            salt (bytes): The salt used for key derivation
        """
        key, _ = derive_key(master_password, salt)
        key_hash = base64.b64encode(key).decode('utf-8')
        salt_b64 = base64.b64encode(salt).decode('utf-8')
        
        with open(MASTER_KEY_FILE, 'w') as f:
            json.dump({'hash': key_hash, 'salt': salt_b64}, f)
    
    def _load_data(self) -> List[Dict]:
        """
        Load and decrypt data from the database file.
        
        Returns:
            List[Dict]: Decrypted data
        """
        if not os.path.exists(DB_FILE):
            return []
            
        with open(DB_FILE, 'r') as f:
            encrypted_data = f.read()
            
        if not encrypted_data:
            return []
            
        decrypted_data = decrypt_data(encrypted_data, self.key)
        return json.loads(decrypted_data)
    
    def _save_data(self, data: List[Dict]):
        """
        Encrypt and save data to the database file.
        
        Args:
            data (List[Dict]): Data to save
        """
        encrypted_data = encrypt_data(json.dumps(data), self.key)
        with open(DB_FILE, 'w') as f:
            f.write(encrypted_data)
    
    def add_wifi(self, ssid: str, password: str, security: str) -> bool:
        """
        Add a new Wi-Fi credential to the database.
        
        Args:
            ssid (str): Network SSID
            password (str): Network password
            security (str): Security type (WPA/WPA2/WEP)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            data = self._load_data()
            
            # Check if SSID already exists
            for item in data:
                if item['ssid'] == ssid:
                    # Update existing entry
                    item['password'] = password
                    item['security'] = security
                    self._save_data(data)
                    return True
            
            # Add new entry
            data.append({
                'ssid': ssid,
                'password': password,
                'security': security
            })
            
            self._save_data(data)
            return True
        except Exception:
            return False
    
    def get_all_wifi(self) -> List[Dict]:
        """
        Get all Wi-Fi credentials from the database.
        
        Returns:
            List[Dict]: List of Wi-Fi credentials
        """
        try:
            return self._load_data()
        except Exception:
            return []
    
    def delete_wifi(self, ssid: str) -> bool:
        """
        Delete a Wi-Fi credential from the database.
        
        Args:
            ssid (str): Network SSID to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            data = self._load_data()
            
            # Find and remove the entry
            filtered_data = [item for item in data if item['ssid'] != ssid]
            
            # Check if anything was removed
            if len(filtered_data) == len(data):
                return False  # Nothing was removed
                
            self._save_data(filtered_data)
            return True
        except Exception:
            return False