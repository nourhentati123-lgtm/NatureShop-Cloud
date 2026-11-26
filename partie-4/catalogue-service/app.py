import os
import sqlite3
from flask import Flask, jsonify, render_template

app = Flask(__name__)
CHEMIN_BD = os.getenv("DB_PATH", "/data/catalogue.db")


def obtenir_bd():
    connexion = sqlite3.connect(CHEMIN_BD)
    connexion.row_factory = sqlite3.Row
    return connexion


def initialiser_bd():
    os.makedirs(os.path.dirname(CHEMIN_BD), exist_ok=True)
    with obtenir_bd() as bd:
        bd.execute(
            """CREATE TABLE IF NOT EXISTS produits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                categorie TEXT NOT NULL,
                prix REAL NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0
            )"""
        )
        if bd.execute("SELECT COUNT(*) FROM produits").fetchone()[0] == 0:
            bd.executemany(
                "INSERT INTO produits (nom, categorie, prix, stock) VALUES (?,?,?,?)",
                [
                    ("Savon d'Alep naturel", "savons", 9.5, 50),
                    ("Huile d'argan bio 50ml", "huiles essentielles", 32.0, 20),
                    ("Huile essentielle de romarin", "huiles essentielles", 18.0, 35),
                    ("Crème au karité", "cosmétiques naturels", 24.0, 15),
                ],
            )


@app.after_request
def ajouter_cors(reponse):
    reponse.headers["Access-Control-Allow-Origin"] = "*"
    reponse.headers["Access-Control-Allow-Headers"] = "Content-Type"
    reponse.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return reponse


@app.get("/")
def accueil():
    return render_template("index.html")


@app.get("/products")
def lister_produits():
    with obtenir_bd() as bd:
        lignes = bd.execute("SELECT * FROM produits").fetchall()
    return jsonify([dict(ligne) for ligne in lignes])


@app.get("/products/<int:product_id>")
def get_product(product_id):
    with obtenir_bd() as bd:
        ligne = bd.execute("SELECT * FROM produits WHERE id=?", (product_id,)).fetchone()
    if ligne is None:
        return jsonify(erreur="Produit introuvable"), 404
    return jsonify(dict(ligne))


initialiser_bd()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

