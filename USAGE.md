# Wi-Fi Password Manager - Usage Guide

## Getting Started

1. **Installation**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Running the Application**:
   ```bash
   python src/main.py
   ```

## First Time Setup

When you first run the application, you'll be prompted to create a master password:

1. Enter a strong master password (at least 8 characters recommended)
2. Click "Unlock Database" or press Enter
3. Your encrypted database will be created automatically

## Features

### Adding Wi-Fi Credentials
1. Navigate to "Add Wi-Fi" in the sidebar
2. Enter the network name (SSID)
3. Enter the password
4. Select the security type (WPA, WPA2, WEP, or NOPASS)
5. Click "Save"

### Viewing Wi-Fi Credentials
1. Navigate to "View Wi-Fi" in the sidebar
2. All saved networks will be displayed in a table
3. Passwords are hidden by default for security

### Managing Wi-Fi Credentials
- **Copy Password**: Select a network and click "Copy Password" to copy the password to your clipboard
- **Delete Network**: Select a network and click "Delete Selected" to remove it

### Generating QR Codes
1. Navigate to "Generate QR" in the sidebar
2. Select a network from the list
3. Click "Generate QR Code"
4. The QR code will be displayed and saved to `assets/qr_codes/`

### Theme Toggle
- Use the "Toggle Theme" button to switch between light and dark modes

### Logout
- Click "Logout" to return to the master password screen

## Security Features

- All data is encrypted using AES-256 encryption
- Master password is hashed using PBKDF2 with a random salt
- Database file (`wifi_data.enc`) is stored locally
- No internet connection is required or used
- Passwords are never stored in plain text

## Troubleshooting

### Forgotten Master Password
If you forget your master password, there is no recovery option. You will need to delete the `wifi_data.enc` file to start over.

### Application Not Starting
1. Ensure all dependencies are installed: `pip install -r requirements.txt`
2. Check that you're running Python 3.6 or higher
3. Make sure the `src` directory is in the correct location

### QR Code Issues
If QR codes are not generating:
1. Check that the `assets/qr_codes/` directory exists and is writable
2. Ensure you have selected a network before generating

## File Structure

```
wifi-password-manager/
├── src/
│    ├── main.py          # Application entry point
│    ├── gui.py           # Graphical user interface
│    ├── encryption.py    # AES-256 encryption functions
│    ├── database.py      # Database management
│    ├── qrcode_generator.py  # QR code generation
│    └── utils.py         # Utility functions
├── tests/                # Unit tests
├── assets/
│    ├── app_icon.png     # Application icon
│    └── qr_codes/        # Generated QR codes
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── USAGE.md              # This file
```