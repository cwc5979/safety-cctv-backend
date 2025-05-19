import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from app.config import settings

cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(cred)