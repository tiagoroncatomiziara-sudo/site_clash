import random
from flask import Flask, render_template, request

app = Flask(__name__)

#===========================cartas===========================
cartas = {
"Hog Rider": {"elixir": 4, "tipo": "win"},
"Giant": {"elixir": 5, "tipo": "win"},
"Golem": {"elixir": 8, "tipo": "win"},
"Balloon": {"elixir": 5, "tipo": "win"},
"Royal Giant": {"elixir": 6, "tipo": "win"},
"Lava Hound": {"elixir": 7, "tipo": "win"},
"X-Bow": {"elixir": 6, "tipo": "win"},
"Mortar": {"elixir": 4, "tipo": "win"},
"Miner": {"elixir": 3, "tipo": "win"},
"Goblin Barrel": {"elixir": 3, "tipo": "win"},
"Graveyard": {"elixir": 5, "tipo": "win"},
"Royal Hogs": {"elixir": 5, "tipo": "win"},
"Ram Rider": {"elixir": 5, "tipo": "win"},
"Battle Ram": {"elixir": 4, "tipo": "win"},
"Wall Breakers": {"elixir": 2, "tipo": "win"},
"Goblin Drill": {"elixir": 4, "tipo": "win"},
"Three Musketeers": {"elixir": 9, "tipo": "win"},

"P.E.K.K.A": {"elixir": 7, "tipo": "tank"},
"Mega Knight": {"elixir": 7, "tipo": "tank"},
"Electro Giant": {"elixir": 7, "tipo": "tank"},
"Elixir Golem": {"elixir": 3, "tipo": "tank"},
"Goblin Giant": {"elixir": 6, "tipo": "tank"},
"Ice Golem": {"elixir": 2, "tipo": "tank"},
"Giant Skeleton": {"elixir": 6, "tipo": "tank"},

"Knight": {"elixir": 3, "tipo": "support"},
"Valkyrie": {"elixir": 4, "tipo": "support"},
"Mini P.E.K.K.A": {"elixir": 4, "tipo": "support"},
"Musketeer": {"elixir": 4, "tipo": "support"},
"Wizard": {"elixir": 5, "tipo": "support"},
"Witch": {"elixir": 5, "tipo": "support"},

"Minions": {"elixir": 3, "tipo": "air"},
"Bats": {"elixir": 2, "tipo": "air"},
"Baby Dragon": {"elixir": 4, "tipo": "air"},

"Cannon": {"elixir": 3, "tipo": "defense"},
"Tesla": {"elixir": 4, "tipo": "defense"},

"Zap": {"elixir": 2, "tipo": "spell"},
"Arrows": {"elixir": 3, "tipo": "spell"},
"Fireball": {"elixir": 4, "tipo": "spell"},

"Skeletons": {"elixir": 1, "tipo": "cycle"},
"Goblins": {"elixir": 2, "tipo": "cycle"}
}

#==========================gerador===========================

def gerar_deck_inteligente(elixir_desejado):
    melhores_deck = None
    menor_diferenca = float("inf")

    for _ in range(3000):
        deck = []

        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "win"], 1)
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "tank"], 1)
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "support"], 2)
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "air"], 1)
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "spell"], 2)

        while len(deck) < 8:
            carta = random.choice(list(cartas.keys()))
            if carta not in deck:
                deck.append(carta)

        media = sum(cartas[c]["elixir"] for c in deck) / 8
        diferenca = abs(media - elixir_desejado)

        if diferenca < menor_diferenca:
            menor_diferenca = diferenca
            melhores_deck = deck

    return melhores_deck

#======================avaliador=============================

def avaliar_deck(deck, cartas):
    nota = 0
    tipos = [cartas[n]['tipo'] for n in deck]

    if 'win' in tipos:
        nota += 2
    else:
        nota -= 2

    if 'defense' in tipos:
        nota += 2
    else:
        nota -= 2   # CORRIGIDO

    if 'support' in tipos:
        nota += 2
    else:
        nota -= 1

    if 'air' in tipos:
        nota += 2
    else:
        nota -= 1

    if 'spell' in tipos:
        nota += 1
    else:
        nota -= 0.5

    media = sum(cartas[n]['elixir'] for n in deck) / len(deck)

    if 2 <= media <= 4:
        nota += 1.5

    return round(nota, 1), round(media, 1)

#======================ROTAS=============================

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        acao = request.form.get("acao")

        if acao == "gerar":
            elixir = float(request.form["elixir"])
            deck = gerar_deck_inteligente(elixir)

            nota, media = avaliar_deck(deck, cartas)

            return render_template("criar_deck.html",
                                   deck=deck,
                                   cartas=cartas,
                                   nota=nota,
                                   media=media)

        elif acao == "arena":
            return render_template("filtro_arena.html")

    return render_template("index.html")


@app.route("/arena", methods=["POST"])
def arena():
    arena = int(request.form["arena"])

    deck = random.sample(list(cartas.keys()), 8)

    nota, media = avaliar_deck(deck, cartas)

    return render_template("criar_deck.html",
                           deck=deck,
                           cartas=cartas,
                           nota=nota,
                           media=media)

#======================RUN=============================

if __name__ == "__main__":
    app.run(debug=True)
