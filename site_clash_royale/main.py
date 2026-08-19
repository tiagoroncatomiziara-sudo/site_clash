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
    melhor_deck = None
    melhor_nota = -1

    for _ in range(4000):

        deck = []

        # garante estrutura básica REAL
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "win"], 1)
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "defense"], 1)
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "tank"], 1)
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "spell"], 1)
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "cycle"], 1)
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "support"], 1)
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "air"], 1)
        deck += random.sample([c for c in cartas if cartas[c]["tipo"] == "win"], 1)

        # garante 8 cartas únicas
        deck = list(set(deck))

        while len(deck) < 8:
            c = random.choice(list(cartas.keys()))
            if c not in deck:
                deck.append(c)

        nota, media = avaliar_deck(deck, cartas)

        # bônus por bater elixir desejado
        bonus = max(0, 2 - abs(media - elixir_desejado))
        nota += bonus

        if nota > melhor_nota:
            melhor_nota = nota
            melhor_deck = deck

    return melhor_deck
#======================avaliador=============================

def avaliar_deck(deck, cartas):
    tipos = [cartas[c]["tipo"] for c in deck]
    elixires = [cartas[c]["elixir"] for c in deck]

    score = 0

    # =========================
    # ⚡ ELIXIR CURVE (0 a 3 pts)
    # =========================
    media = sum(elixires) / 8

    if 2.6 <= media <= 3.6:
        score += 3
    elif 3.6 < media <= 4.2:
        score += 2
    elif 2.2 <= media < 2.6:
        score += 1
    else:
        score -= 2

    # =========================
    # 🎯 WIN CONDITION (0 a 3 pts)
    # =========================
    win = tipos.count("win")

    if win == 1:
        score += 3
    elif win == 2:
        score += 2
    elif win == 0:
        score -= 3
    else:
        score -= 2

    # =========================
    # 🧱 DEFESA (0 a 2 pts)
    # =========================
    defense = tipos.count("defense")

    if defense == 1:
        score += 2
    elif defense == 2:
        score += 1
    elif defense == 0:
        score -= 2
    elif defense >= 4:
        score -= 2

    # =========================
    # 🔥 SPELL BALANCE (0 a 2 pts)
    # =========================
    spell = tipos.count("spell")

    if spell == 1:
        score += 2
    elif spell == 2:
        score += 1
    elif spell == 0:
        score -= 2
    elif spell >= 4:
        score -= 2

    # =========================
    # 🔁 CYCLE (0 a 1.5 pts)
    # =========================
    cycle = tipos.count("cycle")

    if cycle >= 2:
        score += 1.5
    elif cycle == 1:
        score += 0.5
    else:
        score -= 1

    # =========================
    # 🛡️ TANK (0 a 1.5 pts)
    # =========================
    tank = tipos.count("tank")

    if tank == 1:
        score += 1.5
    elif tank == 0:
        score -= 1

    # =========================
    # 🌬️ AIR COVER (0 a 1.5 pts)
    # =========================
    if "air" in tipos:
        score += 1.5
    else:
        score -= 1

    # =========================
    # 💥 PRESSÃO OFFENSIVA (0 a 1.5 pts)
    # =========================
    pressure = sum(1 for c in deck if cartas[c]["tipo"] in ["win", "tank", "support"])

    if pressure >= 5:
        score += 1.5
    elif pressure <= 3:
        score -= 1

    # =========================
    # ⚠️ OVERLOAD DE ELIXIR (penalidade forte)
    # =========================
    caros = sum(1 for c in deck if cartas[c]["elixir"] >= 6)

    if caros >= 4:
        score -= 2.5
    elif caros == 3:
        score -= 1

    # =========================
    # 🧬 VARIEDADE (anti deck lixo)
    # =========================
    unique_types = len(set(tipos))

    if unique_types >= 6:
        score += 1
    elif unique_types <= 3:
        score -= 2

    # =========================
    # 🎲 MICRO VARIAÇÃO (evita empate)
    # =========================
    import random
    score += random.uniform(-0.1, 0.1)

    # =========================
    # 📊 NORMALIZAÇÃO FINAL (0–10)
    # =========================
    if score < 0:
        score = 0
    if score > 12:
        score = 12

    nota_final = (score / 12) * 10

    return round(nota_final, 1), round(media, 2)

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
