import random
from flask import Flask, render_template, request

app = Flask(__name__)

#===========================cartas===========================
cartas = {

# ===================== WIN CONDITIONS =====================
"Hog Rider": {"elixir": 4, "tipo": "win"},
"Giant": {"elixir": 5, "tipo": "win"},
"Golem": {"elixir": 8, "tipo": "win"},
"Balloon": {"elixir": 5, "tipo": "win"},
"Royal Giant": {"elixir": 6, "tipo": "win"},
"Lava Hound": {"elixir": 7, "tipo": "win"},
"Miner": {"elixir": 3, "tipo": "win"},
"Goblin Barrel": {"elixir": 3, "tipo": "win"},
"Graveyard": {"elixir": 5, "tipo": "win"},
"Royal Hogs": {"elixir": 5, "tipo": "win"},
"Ram Rider": {"elixir": 5, "tipo": "win"},
"Battle Ram": {"elixir": 4, "tipo": "win"},
"Wall Breakers": {"elixir": 2, "tipo": "win"},
"Goblin Drill": {"elixir": 4, "tipo": "win"},
"X-Bow": {"elixir": 6, "tipo": "win"},
"Mortar": {"elixir": 4, "tipo": "win"},

# ===================== TANKS =====================
"P.E.K.K.A": {"elixir": 7, "tipo": "tank"},
"Mega Knight": {"elixir": 7, "tipo": "tank"},
"Electro Giant": {"elixir": 7, "tipo": "tank"},
"Elixir Golem": {"elixir": 3, "tipo": "tank"},
"Goblin Giant": {"elixir": 6, "tipo": "tank"},
"Giant Skeleton": {"elixir": 6, "tipo": "tank"},
"Ice Golem": {"elixir": 2, "tipo": "tank"},

# ===================== SUPPORT TROOPS =====================
"Knight": {"elixir": 3, "tipo": "support"},
"Valkyrie": {"elixir": 4, "tipo": "support"},
"Mini P.E.K.K.A": {"elixir": 4, "tipo": "support"},
"Musketeer": {"elixir": 4, "tipo": "support"},
"Wizard": {"elixir": 5, "tipo": "support"},
"Witch": {"elixir": 5, "tipo": "support"},
"Executioner": {"elixir": 5, "tipo": "support"},
"Bowler": {"elixir": 5, "tipo": "support"},
"Prince": {"elixir": 5, "tipo": "support"},
"Dark Prince": {"elixir": 4, "tipo": "support"},
"Lumberjack": {"elixir": 4, "tipo": "support"},
"Bandit": {"elixir": 3, "tipo": "support"},

# ===================== AIR TROOPS =====================
"Minions": {"elixir": 3, "tipo": "air"},
"Bats": {"elixir": 2, "tipo": "air"},
"Baby Dragon": {"elixir": 4, "tipo": "air"},
"Mega Minion": {"elixir": 3, "tipo": "air"},
"Skeleton Dragons": {"elixir": 4, "tipo": "air"},
"Electro Dragon": {"elixir": 5, "tipo": "air"},
"Phoenix": {"elixir": 4, "tipo": "air"},

# ===================== DEFENSE BUILDINGS =====================
"Cannon": {"elixir": 3, "tipo": "defense"},
"Tesla": {"elixir": 4, "tipo": "defense"},
"Inferno Tower": {"elixir": 5, "tipo": "defense"},
"Bomb Tower": {"elixir": 4, "tipo": "defense"},
"X-Bow": {"elixir": 6, "tipo": "defense"},
"Mortar": {"elixir": 4, "tipo": "defense"},
"Furnace": {"elixir": 4, "tipo": "defense"},
"Goblin Hut": {"elixir": 4, "tipo": "defense"},
"Tombstone": {"elixir": 3, "tipo": "defense"},

# ===================== SPELLS =====================
"Zap": {"elixir": 2, "tipo": "spell"},
"Arrows": {"elixir": 3, "tipo": "spell"},
"Fireball": {"elixir": 4, "tipo": "spell"},
"Log": {"elixir": 2, "tipo": "spell"},
"Freeze": {"elixir": 4, "tipo": "spell"},
"Poison": {"elixir": 4, "tipo": "spell"},
"Lightning": {"elixir": 6, "tipo": "spell"},
"Rage": {"elixir": 2, "tipo": "spell"},
"Tornado": {"elixir": 3, "tipo": "spell"},
"Earthquake": {"elixir": 3, "tipo": "spell"},
"Mirror": {"elixir": 1, "tipo": "spell"},

# ===================== CYCLE / SMALL TROOPS =====================
"Skeletons": {"elixir": 1, "tipo": "cycle"},
"Ice Spirit": {"elixir": 1, "tipo": "cycle"},
"Fire Spirit": {"elixir": 1, "tipo": "cycle"},
"Electro Spirit": {"elixir": 1, "tipo": "cycle"},
"Goblins": {"elixir": 2, "tipo": "cycle"},
"Spear Goblins": {"elixir": 2, "tipo": "cycle"},
"Archers": {"elixir": 3, "tipo": "cycle"},
"Guards": {"elixir": 3, "tipo": "cycle"},

# ===================== SPECIAL TROOPS =====================
"Skeleton Army": {"elixir": 3, "tipo": "swarm"},
"Goblin Gang": {"elixir": 3, "tipo": "swarm"},
"Barbarians": {"elixir": 5, "tipo": "swarm"},
"Elite Barbarians": {"elixir": 6, "tipo": "swarm"},
"Three Musketeers": {"elixir": 9, "tipo": "swarm"}
}

#==========================gerador===========================

def gerar_deck_inteligente(elixir_desejado):
    melhores_deck = None
    menor_diferenca = float("inf")

    for _ in range(3000):
        deck = []

        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "defense"], 1)
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "win"], 1)
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "tank"], 1)
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "support"], 1)
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "air"], 1)
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "spell"], 1)
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "cycle"], 1)
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "swarm"], 1)

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
        nota += 2.1
    else:
        nota -= 2

    if 'defense' in tipos:
        nota += 2.3
    else:
        nota -= 2   # CORRIGIDO

    if 'support' in tipos:
        nota += 1.4
    else:
        nota -= 1

    if 'air' in tipos:
        nota += 1.2
    else:
        nota -= 1

    if 'spell' in tipos:
        nota += 0.8
    else:
        nota -= 0.5
    if 'cycle' in tipos:
        nota += 0.5
    else:
        nota -= 0.5

    if 'swarm' in tipos:
        nota += 0.5
    else:
        nota -= 0.5

    if 'tank' in tipos:
        nota += 1.5
    else:
        nota -= 1

    if sum(1 for n in deck if cartas[n]['tipo'] == 'win') <=3 or sum(1 for n in deck if cartas[n]['tipo'] == 'win') >= 5:
        nota -=0.6

    if sum(1 for n in deck if cartas[n]['tipo'] == 'defense') >=5:
        nota -=0.7

    if sum(1 for n in deck if cartas[n]['tipo'] == 'defense') <=5:
        nota += 0.2

    if sum(1 for n in deck if cartas[n]['tipo'] == 'support') >=5
        nota -=0.3

    if sum(1 for n in deck if cartas[n]['tipo'] == 'support') <=5:
        nota += 0.2

    if sum(1 for n in deck if cartas[n]['tipo'] == 'spell') >=5:
        nota -=0.3

    if sum(1 for n in deck if cartas[n]['tipo'] == 'spell') <=5:
        nota += 0.2

    media = sum(cartas[n]['elixir'] for n in deck) / len(deck)

    if 2 <= media <= 4:
        nota += 0.3
    else:
        nota -= 1
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
