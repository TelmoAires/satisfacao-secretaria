from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
from datetime import datetime
import os
import csv

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


# Página principal
@app.route("/")
def index():
    return render_template("index.html")


# Registar clique
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


# Área de administração
@app.route("/admin")
def admin():
    conn = ligar_bd()
    cursor = conn.cursor()

    # Histórico
    cursor.execute("""
        SELECT nivel, data_hora
        FROM respostas
        ORDER BY data_hora DESC
    """)
    dados = cursor.fetchall()

    # Totais por tipo
    cursor.execute("""
        SELECT nivel, COUNT(*)
        FROM respostas
        GROUP BY nivel
    """)
    totais_raw = cursor.fetchall()
    conn.close()

    # Converter para dicionário
    totais = {
        "Muito Satisfeito": 0,
        "Satisfeito": 0,
        "Insatisfeito": 0
    }

    for nivel, total in totais_raw:
        totais[nivel] = total

    return render_template(
        "admin.html",
        dados=dados,
        totais=totais
    )


# Exportar TXT
@app.route("/exportar_txt")
def exportar_txt():
    conn = ligar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT nivel, data_hora FROM respostas")
    dados = cursor.fetchall()
    conn.close()

    with open("cliques.txt", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["Nivel", "DataHora"])
        writer.writerows(dados)

    return send_file("cliques.txt", as_attachment=True)


# Exportar CSV (abre no Excel)
@app.route("/exportar_excel")
def exportar_excel():
    conn = ligar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT nivel, data_hora FROM respostas")
    dados = cursor.fetchall()
    conn.close()

    with open("cliques.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Nivel", "DataHora"])
        writer.writerows(dados)

    return send_file("cliques.csv", as_attachment=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

