import qrcode
import os
from PIL import Image

def generate_wifi_qr(ssid: str, password: str, security: str = "WPA") -> str:
    """
    Generate a Wi-Fi QR code and save it as a PNG file.
    
    Args:
        ssid (str): Network SSID
        password (str): Network password
        security (str): Security type (WPA/WPA2/WEP/NOPASS)
        
    Returns:
        str: Path to the generated QR code image
    """
    # Ensure security type is valid
    if security.upper() not in ["WPA", "WPA2", "WEP", "NOPASS"]:
        security = "WPA"
    
    # Create the Wi-Fi QR code format
    # WIFI:T:WPA;S:<SSID>;P:<PASSWORD>;
    if security.upper() == "NOPASS":
        wifi_string = f"WIFI:T:{security};S:{ssid};;"
    else:
        wifi_string = f"WIFI:T:{security};S:{ssid};P:{password};;"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(wifi_string)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Ensure qr_codes directory exists
    qr_dir = os.path.join("assets", "qr_codes")
    if not os.path.exists(qr_dir):
        os.makedirs(qr_dir)
    
    # Save image
    filename = f"{ssid.replace(' ', '_')}_qr.png"
    filepath = os.path.join(qr_dir, filename)
    img.save(filepath)
    
    return filepath