import requests
from app.config import get_settings

settings = get_settings()


def send_sms(to: str, message: str) -> bool:
    """Send SMS using MSG91 (Indian SMS gateway)"""
    if not settings.MSG91_AUTH_KEY:
        print("MSG91 credentials not configured")
        return False
    
    try:
        url = "https://api.msg91.com/api/v5/flow/"
        payload = {
            "authkey": settings.MSG91_AUTH_KEY,
            "mobiles": to,
            "message": message,
            "sender": settings.MSG91_SENDER_ID,
            "route": "4",
            "country": "91"
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print(f"SMS sent to {to}")
            return True
        else:
            print(f"Failed to send SMS: {response.text}")
            return False
    except Exception as e:
        print(f"SMS error: {e}")
        return False
