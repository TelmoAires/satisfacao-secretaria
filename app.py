EXT
        )
    """)
    conn.commit()
    return conn

# Página principal
@app.route("/")
def index():
    return render_template("index.html")

# Rota para registar cliques
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

# Rota para exportar Excel
@app.route("/exportar_excel")
def exportar_excel():
    conn = sqlite3.connect("satisfacao.db")
    df = pd.read_sql_query("SELECT * FROM respostas", conn)
    conn.close()
    df.to_excel("cliques.xlsx", index=False)
    return send_file("cliques.xlsx", as_attachment=True)

# Rota para exportar TXT
@app.route("/exportar_txt")
def exportar_txt():
    conn = sqlite3.connect("satisfacao.db")
    df = pd.read_sql_query("SELECT * FROM respostas", conn)
    conn.close()
    df.to_csv("cliques.txt", sep="\t", index=False)
    return send_file("cliques.txt", as_attachment=True)


@app.route("/admin")
    def admin():
    conn = sqlite3.connect("satisfacao.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nivel, data_hora
        FROM respostas
        ORDER BY data_hora DESC
    """)
    dados = cursor.fetchall()
    conn.close()

    return render_template("admin.html", dados=dados)



# Início da aplicação
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



