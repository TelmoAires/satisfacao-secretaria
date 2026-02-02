from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
from datetime import datetime
import pandas as pd
import csv
import os

# =========================
# Função para ligar à BD SQLite
# =========================
def ligar_bd():
    return sqlite3.connect("satisfacao.db")

# =========================
# Inicializa BD (uma vez)
# =========================
if not os.path.exists("satisfacao.db"):
    conn = ligar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS respostas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nivel TEXT,
            data_hora TEXT
        )
    """)
    conn.commit()
    conn.close()

# =========================
# Inicializa Flask
# =========================
app = Flask(__name__)

# Página principal
@app.route("/")
def index():
    return render_template("index.html")

# Registo de cliques
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

# Exportar Excel
@app.route("/exportar_excel")
def exportar_excel():
    conn = ligar_bd()
    df = pd.read_sql_query("SELECT * FROM respostas ORDER BY data_hora DESC", conn)
    conn.close()
    df.to_excel("cliques.xlsx", index=False)
    return send_file("cliques.xlsx", as_attachment=True)

# Exportar TXT
@app.route("/exportar_txt")
def exportar_txt():
    conn = ligar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT nivel, data_hora FROM respostas ORDER BY data_hora DESC")
    dados = cursor.fetchall()
    conn.close()

    with open("cliques.txt", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["Nivel", "DataHora"])
        writer.writerows(dados)

    return send_file("cliques.txt", as_attachment=True)

# Área admin
@app.route("/admin")
def admin():
    conn = ligar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT nivel, data_hora FROM respostas ORDER BY data_hora DESC")
    dados = cursor.fetchall()
    conn.close()

    # Totais para gráfico
    totais = {"Muito Satisfeito":0, "Satisfeito":0, "Insatisfeito":0}
    for d in dados:
        if d[0] in totais:
            totais[d[0]] += 1

    return render_template("admin.html", dados=dados, totais=totais)

# Run
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
