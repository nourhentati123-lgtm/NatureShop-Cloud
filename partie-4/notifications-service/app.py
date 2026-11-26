import os
import sqlite3
from datetime import datetime, timezone
from flask import Flask, jsonify, request

app = Flask(__name__)
CHEMIN_BD = os.getenv("DB_PATH", "/data/notifications.db")


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response


@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        return "", 204


def obtenir_bd():
    connexion = sqlite3.connect(CHEMIN_BD)
    connexion.row_factory = sqlite3.Row
    return connexion


def initialiser_bd():
    os.makedirs(os.path.dirname(CHEMIN_BD), exist_ok=True)
    with obtenir_bd() as bd:
        bd.execute(
            """CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destinataire TEXT NOT NULL,
                message TEXT NOT NULL,
                cree_le TEXT NOT NULL
            )"""
        )


@app.post("/notify")
def notify():
    donnees = request.get_json(silent=True) or {}
    if "recipient" not in donnees or "message" not in donnees:
        return jsonify(erreur="Champs requis : recipient, message"), 400
    maintenant = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with obtenir_bd() as bd:
        curseur = bd.execute(
            "INSERT INTO notifications (destinataire, message, cree_le) VALUES (?,?,?)",
            (donnees["recipient"], donnees["message"], maintenant),
        )
    # Simulation d'envoi d'email/SMS : visible dans `docker logs`
    print(f"[NOTIFICATION] -> {donnees['recipient']} : {donnees['message']}", flush=True)
    return jsonify(id=curseur.lastrowid, statut="envoye", cree_le=maintenant), 201


@app.get("/notifications")
def lister_notifications():
    with obtenir_bd() as bd:
        lignes = bd.execute("SELECT * FROM notifications ORDER BY id DESC").fetchall()
    return jsonify([dict(ligne) for ligne in lignes])


initialiser_bd()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)