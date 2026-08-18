from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Cartas (em inglês para funcionar com imagens)
cartas = {
    "Giant": 5,
    "Hog Rider": 4,
    "Balloon": 5,
    "Golem": 8,
    "P.E.K.K.A": 7,
    "Miner": 3,
    "X-Bow": 6,
    "Mortar": 4,

    "Knight": 3,
    "Valkyrie": 4,
    "Mini P.E.K.K.A": 4,
    "Prince": 5,

    "Archers": 3,
    "Musketeer": 4,
    "Baby Dragon": 4,
    "Minions": 3,
    "Bats": 2,

    "Zap": 2,
    "Arrows": 3,
    "Snowball": 2,
    "The Log": 2,

    "Fireball": 4,
    "Poison": 4,
    "Rocket": 6,

    "Cannon": 3,
    "Tesla": 4,

    "Skeletons": 1,
    "Goblins": 2,
    "Ice Spirit": 1
}

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        elixir_desejado = float(request.form["elixir"])

        deck = random.sample(list(cartas.keys()), 8)

        media = sum(cartas[c] for c in deck) / 8

        return render_template(
            "criar_deck.html",
            deck=deck,
            cartas=cartas,
            elixir_medio=round(media, 2)
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
