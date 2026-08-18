import random
from flask import Flask, render_template, request

app = Flask(__name__)

# Cartas com tipo
cartas = {
    "Giant": {"elixir": 5, "tipo": "tank"},
    "Golem": {"elixir": 8, "tipo": "tank"},
    "P.E.K.K.A": {"elixir": 7, "tipo": "tank"},

    "Hog Rider": {"elixir": 4, "tipo": "win"},
    "Balloon": {"elixir": 5, "tipo": "win"},
    "X-Bow": {"elixir": 6, "tipo": "win"},

    "Musketeer": {"elixir": 4, "tipo": "air"},
    "Baby Dragon": {"elixir": 4, "tipo": "air"},
    "Minions": {"elixir": 3, "tipo": "air"},

    "Knight": {"elixir": 3, "tipo": "support"},
    "Valkyrie": {"elixir": 4, "tipo": "support"},
    "Mini P.E.K.K.A": {"elixir": 4, "tipo": "support"},

    "Fireball": {"elixir": 4, "tipo": "spell"},
    "Zap": {"elixir": 2, "tipo": "spell"},
    "Arrows": {"elixir": 3, "tipo": "spell"},
}

def gerar_deck_inteligente(elixir_desejado):
    melhores_deck = None
    menor_diferenca = float("inf")

    for _ in range(3000):

        deck = []

        # garante estrutura
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "win"], 1)
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "tank"], 1)
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "support"], 2)
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "air"], 1)
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "spell"], 2)

        # completa até 8 cartas
        while len(deck) < 8:
            carta = random.choice(list(cartas.keys()))
            if carta not in deck:
                deck.append(carta)

        # calcula média
        media = sum(cartas[c]["elixir"] for c in deck) / 8
        diferenca = abs(media - elixir_desejado)

        if diferenca < menor_diferenca:
            menor_diferenca = diferenca
            melhores_deck = deck

    return melhores_deck


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        elixir = float(request.form["elixir"])
        deck = gerar_deck_inteligente(elixir)

        return render_template("criar_deck.html", deck=deck, cartas=cartas)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
