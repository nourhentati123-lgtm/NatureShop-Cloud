import os
import sqlite3
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)
CHEMIN_BD = os.getenv("DB_PATH", "/data/orders.db")
URL_CATALOGUE = os.getenv("CATALOGUE_URL", "http://catalogue:5001")
URL_NOTIFICATIONS = os.getenv("NOTIFICATIONS_URL", "http://notifications:5003")


def obtenir_bd():
    connexion = sqlite3.connect(CHEMIN_BD)
    connexion.row_factory = sqlite3.Row
    return connexion


def initialiser_bd():
    os.makedirs(os.path.dirname(CHEMIN_BD), exist_ok=True)
    with obtenir_bd() as bd:
        bd.execute(
            """CREATE TABLE IF NOT EXISTS commandes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email_client TEXT NOT NULL,
                produit_id INTEGER NOT NULL,
                nom_produit TEXT NOT NULL,
                quantite INTEGER NOT NULL,
                total REAL NOT NULL,
                statut TEXT NOT NULL DEFAULT 'confirmee'
            )"""
        )


@app.post("/orders")
def creer_commande():
    donnees = request.get_json(silent=True) or {}
    champs_manquants = [k for k in ("customer_email", "product_id", "quantity") if k not in donnees]
    if champs_manquants:
        return jsonify(erreur=f"Champs manquants : {', '.join(champs_manquants)}"), 400
    quantite = int(donnees["quantity"])
    if quantite <= 0:
        return jsonify(erreur="La quantité doit être positive"), 400

    # 1) Communication avec le service Catalogue
    try:
        reponse = requests.get(f"{URL_CATALOGUE}/products/{donnees['product_id']}", timeout=5)
    except requests.RequestException:
        return jsonify(erreur="Service Catalogue indisponible"), 503
    if reponse.status_code == 404:
        return jsonify(erreur="Produit introuvable"), 404
    produit = reponse.json()
    if produit["stock"] < quantite:
        return jsonify(erreur="Stock insuffisant", stock=produit["stock"]), 409

    total = round(produit["prix"] * quantite, 2)
    with obtenir_bd() as bd:
        curseur = bd.execute(
            "INSERT INTO commandes (email_client, produit_id, nom_produit, quantite, total)"
            " VALUES (?,?,?,?,?)",
            (donnees["customer_email"], produit["id"], produit["nom"], quantite, total),
        )
    commande_id = curseur.lastrowid

    # 2) Communication avec le service Notifications
    notifie = True
    try:
        requests.post(
            f"{URL_NOTIFICATIONS}/notify",
            json={
                "recipient": donnees["customer_email"],
                "message": f"Commande #{commande_id} confirmée : {quantite} x {produit['nom']} ({total} TND)",
            },
            timeout=5,
        )
    except requests.RequestException:
        notifie = False  # la commande reste valide même si la notification échoue

    return (
        jsonify(
            id=commande_id,
            produit=produit["nom"],
            quantite=quantite,
            total=total,
            statut="confirmee",
            notifie=notifie,
        ),
        201,
    )


@app.get("/orders")
def lister_commandes():
    with obtenir_bd() as bd:
        lignes = bd.execute("SELECT * FROM commandes ORDER BY id DESC").fetchall()
    return jsonify([dict(ligne) for ligne in lignes])


initialiser_bd()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
