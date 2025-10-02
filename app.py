from flask import Flask, request, render_template
import csv
from datetime import datetime
import os
import random

app = Flask(__name__)
CSV_FILE = "cliques.csv"

# Cria o CSV com cabeçalho se não existir
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["nome", "email", "setor", "data_hora", "ip"])

@app.route("/track")
def track():
    nome = request.args.get("nome")
    email = request.args.get("email")
    setor = request.args.get("setor")
    ip = request.remote_addr
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Salva os dados no CSV
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([nome, email, setor, data_hora, ip])

    return render_template("cesta_natal.html", mostrar_formulario=False, confirmacao=False)

@app.route("/sorteio-ti", methods=["GET", "POST"])
def sorteio_ti():
    if request.method == "POST":
        nome = request.form.get("nome")
        setor = request.form.get("setor")
        email = request.form.get("email")
        ip = request.remote_addr
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Salva tudo no mesmo CSV
        with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([nome, email, setor, data_hora, ip])
        numero_sorteio = f"{random.randint(0, 999):03d}"
        return render_template("cesta_natal.html", confirmacao=True, mostrar_formulario=False, numero_sorteio=numero_sorteio)
    elif request.args.get("form") == "1":
        return render_template("cesta_natal.html", mostrar_formulario=True, confirmacao=False)
    return render_template("cesta_natal.html", mostrar_formulario=False, confirmacao=False)

# Remove ou comente o antigo /cesta para evitar conflito
# @app.route("/cesta", methods=["GET", "POST"])
# def cesta():
#     if request.method == "POST":
#         nome = request.form.get("nome")
#         setor = request.form.get("setor")
#         email = request.form.get("email")
#         ip = request.remote_addr
#         data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         # Salva tudo no mesmo CSV
#         with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
#             writer = csv.writer(f)
#             writer.writerow([nome, email, setor, data_hora, ip])
#         numero_sorteio = f"{random.randint(0, 999):03d}"
#         return render_template("cesta_natal.html", confirmacao=True, mostrar_formulario=False, numero_sorteio=numero_sorteio)
#     elif request.args.get("form") == "1":
#         return render_template("cesta_natal.html", mostrar_formulario=True, confirmacao=False)
#     return render_template("cesta_natal.html", mostrar_formulario=False, confirmacao=False)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
