from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import httpx # Bibliothèque pour effectuer des requêtes HTTP asynchrones entre services
import os
from fastapi.middleware.cors import CORSMiddleware

# Initialisation de l'application FastAPI qui servira de Gateway (Port 8002)
app = FastAPI()

# Configuration du Middleware CORS (Cross-Origin Resource Sharing)
# Essentiel pour permettre au navigateur (Frontend) de communiquer avec l'API
# sans être bloqué par les politiques de sécurité du navigateur.
app.add_middleware( 
    CORSMiddleware,
    allow_origins=["*"], # Autorise toutes les sources (origines)
    allow_methods=["*"], # Autorise toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"], # Autorise tous les headers
)

# --- SECTION DES ROUTES API (BACKEND) ---

# Définition de la route de la Gateway qui centralise l'accès aux utilisateurs
@app.get("/api/users/{user_id}")  
async def get_user(user_id: int):
    # Utilisation d'un client HTTP asynchrone pour ne pas bloquer le thread principal
    async with httpx.AsyncClient() as client:
        try:
            # LOGIQUE DE RÉPARTITION : La Gateway redirige la requête vers 
            # le microservice 'Users' qui tourne sur le port 8000.
            # C'est ici que se joue le rôle d'agrégateur/orchestrateur.
            response = await client.get(f"http://localhost:8000/users/{user_id}")
            
            # Retourne la réponse JSON fusionnée reçue du service Users
            return response.json()
        except Exception as e:
            # Gestion d'erreur au cas où l'un des microservices est hors ligne
            return {"error": f"Erreur de communication inter-services : {str(e)}"}

# --- SECTION DES FICHIERS STATIQUES (FRONTEND) ---

# Vérification et création automatique du dossier 'static' si nécessaire
if not os.path.exists("static"):
    os.makedirs("static")

# MONTAGE DES FICHIERS STATIQUES (HTML/JS)
# IMPORTANT : Placé après les routes API pour éviter que le sélecteur "/" 
# ne capture les requêtes destinées aux routes "/api/...".
# Cela permet de servir le fichier index.html à la racine du port 8002.
app.mount("/", StaticFiles(directory="static", html=True), name="static")