# Wi-Fi Password Manager

A secure, offline Wi-Fi password manager with AES-256 encryption and QR code generation capabilities.

![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)

## 🌟 Features

- **Local Encrypted Storage**: All data is encrypted using AES-256 encryption
- **Master Password Protection**: Secure access with a master password
- **Wi-Fi Credential Management**: Add, view, and delete Wi-Fi credentials
- **QR Code Generation**: Export any Wi-Fi credential as a connect-ready QR code
- **Fully Offline**: No internet usage required
- **Modern GUI**: Clean and intuitive user interface with dark/light theme toggle
- **Password Recovery**: Forgot password reset functionality

## 🛠 Tech Stack

- **Python 3.x**
- **Tkinter**: GUI framework
- **PyCryptodome**: AES-256 encryption
- **Pillow**: Image processing for QR codes
- **qrcode**: QR code generation

## 📁 Folder Structure

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
└── README.md            # This file
```

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/itzzomkar/wifi-password-manager.git
   cd wifi-password-manager
   ```

2. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Running the Application

Run the application using:
```bash
python src/main.py
```

For detailed usage instructions, see [USAGE.md](USAGE.md).

## 🔐 Setting Master Password

On first launch, you'll be prompted to create a master password. This password will be used to encrypt and decrypt all your Wi-Fi credentials. Make sure to choose a strong password and remember it, as there is no password recovery option.

### Forgot Password

If you forget your master password:
1. Click the "Forgot Password" button on the login screen
2. Confirm that you want to reset (this will delete all saved Wi-Fi networks)
3. Create a new master password

## 🔒 How Encryption Works

1. **Key Derivation**: When you set your master password, it is processed through PBKDF2 with a random salt to generate a secure encryption key.
2. **Data Encryption**: All Wi-Fi credentials are encrypted using AES-256 in CBC mode before being stored in the `wifi_data.enc` file.
3. **Data Integrity**: Each encrypted entry includes an HMAC to ensure data integrity.
4. **Storage**: The encrypted database is stored locally in the `wifi_data.enc` file.

## 📱 QR Code Generation

Generate QR codes for easy sharing of Wi-Fi credentials:
1. Navigate to "Generate QR" in the sidebar
2. Select a network from the list
3. Click "Generate QR Code"
4. Scan the QR code with your mobile device to connect

The QR code follows the official Wi-Fi QR format:
```
WIFI:T:WPA;S:<SSID>;P:<PASSWORD>;;

```

## 🎨 User Interface

### Dark/Light Theme
- Toggle between dark and light themes using the theme button
- Theme preference is remembered between sessions

### Navigation
- **Add Wi-Fi**: Add new Wi-Fi networks
- **View Wi-Fi**: View and manage saved networks
- **Generate QR**: Create QR codes for sharing

## ⚠️ Security Notes

- All data is stored locally on your device
- Never share your master password
- The application works completely offline
- Your Wi-Fi credentials are never transmitted over the internet
- It's recommended to backup your `wifi_data.enc` file regularly

## 🧪 Testing

Run the unit tests to verify functionality:
```bash
python tests/run_tests.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

Project Link: [https://github.com/itzzomkar/wifi-password-manager](https://github.com/itzzomkar/wifi-password-manager)
