# app/utils/notifier.py
from firebase_admin import messaging
from typing import List

def send_notification(tokens: List[str], title: str, body: str):
    """
    FCM 멀티캐스트 메시지 전송 (data 페이로드 없이)
    """
    message = messaging.MulticastMessage(
        tokens=tokens,
        notification=messaging.Notification(title=title, body=body)
    )
    response = messaging.send_multicast(message)

    # 실패한 토큰 로그 찍기
    if response.failure_count:
        for idx, resp in enumerate(response.responses):
            if not resp.success:
                print(f"Failed to send to {tokens[idx]}: {resp.exception}")
    return response
