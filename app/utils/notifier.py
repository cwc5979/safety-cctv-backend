# 알림 전송 로직 예시 (FCM, WebSocket 등 연동)
def send_notification(user_id: int, message: str):
    # TODO: FCM 토큰 조회 후 푸시 전송 구현
    print(f"Send to user {user_id}: {message}")
