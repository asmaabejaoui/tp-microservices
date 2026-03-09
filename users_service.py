from fastapi import FastAPI
import httpx # Client HTTP indispensable pour la communication entre microservices

# Création du microservice "Utilisateurs" (Port 8000)
app = FastAPI()

# BASE DE DONNÉES LOCALE FICTIVE
# Ce service ne possède que les informations d'identité (ID et Nom).
users_db = {
    1: {"id": 1, "name": "Alice"},
    2: {"id": 2, "name": "Bob"}
}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """
    Rôle : Récupérer un utilisateur ET ses produits associés.
    Concept : Agrégation de services (Service Composition).
    """
    
    # 1. Recherche de l'utilisateur dans la base locale (Port 8000)
    user = users_db.get(user_id)
    if not user:
        return {"error": "User not found"}

    # 2. COMMUNICATION INTER-SERVICES (Appel au Port 8001)
    # Le service User devient un "client" du service Product.
    async with httpx.AsyncClient() as client:
        try:
            # Appel asynchrone pour ne pas bloquer le serveur pendant l'attente de la réponse
            products = await client.get(f"http://localhost:8001/products/{user_id}")
            
            # Si le service produit répond avec succès (200 OK), on récupère le JSON
            product_data = products.json() if products.status_code == 200 else []
            
        except httpx.ConnectError:
            # GESTION DE LA RÉSILIENCE :
            # Si le service Produit est en panne, on renvoie une liste vide 
            # au lieu de faire crasher toute l'application.
            product_data = []

    # 3. FUSION DES DONNÉES (Data Aggregation)
    # On combine les infos de l'utilisateur et la liste des produits reçue.
    return {**user, "products": product_data}