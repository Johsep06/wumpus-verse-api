import firebase_admin
from firebase_admin import credentials, auth, firestore
import os

def initialize_firebase():
    try:
        # Caminho para o arquivo de credenciais
        cred_path = "firebaseKey.json"
        
        # Verifica se o Firebase já foi inicializado
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        
        return auth, firestore
    except Exception as e:
        print(f"Erro ao inicializar Firebase: {e}")
        raise

# Inicializa o Firebase
firebase_auth, firestore_db = initialize_firebase()

# Obtém a instância do Firestore
db = firestore_db.client()