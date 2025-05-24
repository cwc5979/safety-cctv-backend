# app/utils/fcm_util.py
import firebase_admin
from firebase_admin import credentials, messaging
import os

firebase_cred_path = os.getenv("FIREBASE_CRED_PATH", "fcm.json")
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_cred_path)
    firebase_admin.initialize_app(cred)

def send_fcm_notification(token: str, title: str, body: str) -> str:
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=token
    )
    return messaging.send(message)
