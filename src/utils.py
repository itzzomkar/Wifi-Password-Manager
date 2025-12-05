import re

def validate_ssid(ssid: str) -> bool:
    """
    Validate Wi-Fi SSID.
    
    Args:
        ssid (str): The SSID to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # SSID must be between 1 and 32 characters
    if not ssid or len(ssid) > 32:
        return False
    
    # SSID should not contain null characters
    if '\x00' in ssid:
        return False
    
    return True

def validate_password(password: str, security: str) -> bool:
    """
    Validate Wi-Fi password based on security type.
    
    Args:
        password (str): The password to validate
        security (str): Security type (WPA/WPA2/WEP)
        
    Returns:
        bool: True if valid, False otherwise
    """
    if security.upper() == "WEP":
        # WEP keys are either 10 or 26 hexadecimal characters, or 5 or 13 ASCII characters
        if re.match(r'^[0-9A-Fa-f]{10}$', password) or re.match(r'^[0-9A-Fa-f]{26}$', password):
            return True
        elif len(password) == 5 or len(password) == 13:
            return True
        else:
            return False
    elif security.upper() in ["WPA", "WPA2"]:
        # WPA/WPA2 passwords should be between 8 and 63 characters
        return 8 <= len(password) <= 63
    else:
        # For other security types, just check if it's not empty
        return len(password) > 0

def validate_security_type(security: str) -> bool:
    """
    Validate security type.
    
    Args:
        security (str): The security type to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    return security.upper() in ["WPA", "WPA2", "WEP", "NOPASS"]