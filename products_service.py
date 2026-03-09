from fastapi import FastAPI

# Création de l'instance du microservice "Produits" (Port 8001)
# Ce service est indépendant et possède sa propre logique métier.
app = FastAPI()

# SIMULATION D'UNE BASE DE DONNÉES (In-Memory Database)
# Dans un système réparti réel, chaque microservice possède sa propre base de données.
# Ici, les produits sont liés à un 'user_id' pour simuler une relation.
products_db = {
    1: [{"id": 1, "name": "Book"}, {"id": 2, "name": "Pen"}],
    2: [{"id": 3, "name": "Laptop"}]
}

# DÉFINITION DU POINT D'ENTRÉE (ENDPOINT)
# Cette route permet de récupérer les produits d'un utilisateur spécifique.
@app.get("/products/{user_id}")
def get_products(user_id: int):
    """
    Rôle : Fournir les données brutes concernant les produits.
    Principe : Ce service ne connaît pas l'existence de la Gateway 
    ni du service Utilisateurs (Principe de l'Encapsulation).
    """
    
    # Recherche dans la "base de données" fictive. 
    # Si l'ID n'existe pas, on retourne une liste vide [].
    return products_db.get(user_id, [])