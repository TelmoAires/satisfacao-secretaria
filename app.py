from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

def ligar_bd():
    conn = sqlite3.connect("satisfacao.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS respostas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nivel TEXT,
            data_hora TEXT
        )
    """)
    conn.commit()
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registar", methods=["POST"])
def registar():
    dados = request.get_json()
    nivel = dados["nivel"]
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = ligar_bd()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO respostas (nivel, data_hora) VALUES (?, ?)",
        (nivel, data_hora)
    )
    conn.commit()
    conn.close()

    return jsonify({"estado": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
