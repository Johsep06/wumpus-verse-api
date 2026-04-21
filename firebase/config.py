import firebase_admin
from firebase_admin import credentials, auth, firestore, exceptions


def initialize_firebase():
    try:
        cred_path = "firebaseKey.json"

        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)

        return auth, firestore
    except Exception as e:
        print(f"Erro ao inicializar Firebase: {e}")
        raise


firebase_auth, firestore_db = initialize_firebase()
db = firestore_db.client()
