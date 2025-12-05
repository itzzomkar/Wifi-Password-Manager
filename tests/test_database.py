import sys
import os
import unittest
import tempfile
import shutil

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from database import DatabaseManager

class TestDatabase(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.original_db = os.environ.get('DB_FILE', '')
        self.original_master = os.environ.get('MASTER_KEY_FILE', '')
        
        # Change working directory to temp directory
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
    
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        # Restore original working directory
        os.chdir(self.original_cwd)
        
        # Remove temporary directory
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_initialize_database(self):
        """Test database initialization"""
        db = DatabaseManager()
        result = db.initialize_database("test_password")
        self.assertTrue(result)
        
        # Check that database files were created
        self.assertTrue(os.path.exists("wifi_data.enc"))
        self.assertTrue(os.path.exists("master_key.hash"))
    
    def test_add_and_retrieve_wifi(self):
        """Test adding and retrieving Wi-Fi credentials"""
        db = DatabaseManager()
        
        # Initialize database
        self.assertTrue(db.initialize_database("test_password"))
        
        # Add a Wi-Fi network
        result = db.add_wifi("TestNetwork", "testpass123", "WPA")
        self.assertTrue(result)
        
        # Retrieve Wi-Fi networks
        networks = db.get_all_wifi()
        self.assertEqual(len(networks), 1)
        self.assertEqual(networks[0]["ssid"], "TestNetwork")
        self.assertEqual(networks[0]["password"], "testpass123")
        self.assertEqual(networks[0]["security"], "WPA")
    
    def test_delete_wifi(self):
        """Test deleting Wi-Fi credentials"""
        db = DatabaseManager()
        
        # Initialize database
        self.assertTrue(db.initialize_database("test_password"))
        
        # Add a Wi-Fi network
        db.add_wifi("TestNetwork", "testpass123", "WPA")
        
        # Delete the Wi-Fi network
        result = db.delete_wifi("TestNetwork")
        self.assertTrue(result)
        
        # Check that network was deleted
        networks = db.get_all_wifi()
        self.assertEqual(len(networks), 0)
    
    def test_unlock_database(self):
        """Test unlocking database with correct password"""
        db = DatabaseManager()
        
        # Initialize database
        self.assertTrue(db.initialize_database("test_password"))
        
        # Try to unlock with correct password
        result = db.unlock_database("test_password")
        self.assertTrue(result)
    
    def test_unlock_database_wrong_password(self):
        """Test unlocking database with wrong password"""
        db = DatabaseManager()
        
        # Initialize database
        self.assertTrue(db.initialize_database("test_password"))
        
        # Try to unlock with wrong password
        result = db.unlock_database("wrong_password")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()