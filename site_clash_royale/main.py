from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Cartas e custo de elixir
cartas = {
    "Cavaleiro": 3,
    "Arqueiras": 3,
    "Mosqueteira": 4,
    "Gigante": 5,
    "Mini P.E.K.K.A": 4,
    "Valquíria": 4,
    "Príncipe": 5,
    "Mago": 5,
    "Bebê Dragão": 4,
    "Balão": 5,
    "Corredor": 4,
    "Golem": 8,
    "P.E.K.K.A": 7,
    "Mega Cavaleiro": 7,
    "Esqueletos": 1,
    "Goblins": 2,
    "Morcegos": 2,
    "Servos": 3,
    "Canhão": 3,
    "Torre Inferno": 5,
    "Flechas": 3,
    "Bola de Fogo": 4,
    "Zap": 2,
    "O Tronco": 2,
    "Veneno": 4,
    "Relâmpago": 6,
    "Tornado": 3,
    "Fúria": 2,
    "Mineiro": 3,
    "Bandida": 3,
    "Lenhador": 4,
    "Caçador": 4,
    "Executor": 5,
    "Morteiro": 4,
    "X-Besta": 6,
    "Aríete de Batalha": 4,
    "Quebra-Muros": 2,
    "Gigante Goblin": 6,
    "Recrutas Reais": 7,
    "Fantasma Real": 3,
    "Arqueiro Mágico": 4,
    "Cavaleiro Dourado": 4,
    "Rainha Arqueira": 5,
    "Rei Esqueleto": 4,
    "Monge": 5
}


@app.route("/", methods=["GET", "POST"])
def index():

    # Quando o usuário enviar o formulário
    if request.method == "POST":

        elixir_desejado = float(request.form["elixir"])

        melhor_deck = None
        melhor_media = None
        menor_diferenca = float("inf")

        # Tenta várias combinações
        for _ in range(5000):

            deck = random.sample(list(cartas.keys()), 8)

            soma = sum(cartas[carta] for carta in deck)
            media = soma / 8

            diferenca = abs(media - elixir_desejado)

            if diferenca < menor_diferenca:
                menor_diferenca = diferenca
                melhor_deck = deck
                melhor_media = media

        # Mostra o resultado
        return render_template(
            "criar_deck.html",
            deck=melhor_deck,
            cartas=cartas,
            elixir_medio=melhor_media
        )

    # Quando o usuário abre o site pela primeira vez
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
