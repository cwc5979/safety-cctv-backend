from firebase_admin import messaging
from typing import List, Tuple

def send_notification(tokens: List[str], title: str, body: str, image_url: str = None) -> Tuple[int, int]:
    message = messaging.MulticastMessage(
        notification=messaging.Notification(title=title, body=body, image=image_url),
        tokens=tokens
    )
    response = messaging.send_multicast(message)
    return response.success_count, response.failure_count