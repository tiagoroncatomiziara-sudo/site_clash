from flask import Flask, render_template, request
import random

app = Flask(__name__)

# ==========================================================
# CARTAS
# ==========================================================

cartas = {

    # Condições de vitória
    "Gigante": {"elixir": 5, "tipo": "win_condition"},
    "Corredor": {"elixir": 4, "tipo": "win_condition"},
    "Balão": {"elixir": 5, "tipo": "win_condition"},
    "Golem": {"elixir": 8, "tipo": "win_condition"},
    "P.E.K.K.A": {"elixir": 7, "tipo": "win_condition"},
    "Mineiro": {"elixir": 3, "tipo": "win_condition"},
    "Morteiro": {"elixir": 4, "tipo": "win_condition"},
    "X-Besta": {"elixir": 6, "tipo": "win_condition"},
    "Quebra-Muros": {"elixir": 2, "tipo": "win_condition"},
    "Gigante Goblin": {"elixir": 6, "tipo": "win_condition"},
    "Aríete de Batalha": {"elixir": 4, "tipo": "win_condition"},

    # Tanques / suporte
    "Cavaleiro": {"elixir": 3, "tipo": "defesa"},
    "Valquíria": {"elixir": 4, "tipo": "defesa"},
    "Mini P.E.K.K.A": {"elixir": 4, "tipo": "defesa"},
    "Príncipe": {"elixir": 5, "tipo": "suporte"},
    "Príncipe das Trevas": {"elixir": 4, "tipo": "suporte"},
    "Lenhador": {"elixir": 4, "tipo": "suporte"},
    "Bandida": {"elixir": 3, "tipo": "suporte"},
    "Fantasma Real": {"elixir": 3, "tipo": "suporte"},
    "Mega Cavaleiro": {"elixir": 7, "tipo": "defesa"},

    # Defesa aérea / suporte
    "Arqueiras": {"elixir": 3, "tipo": "aerea"},
    "Mosqueteira": {"elixir": 4, "tipo": "aerea"},
    "Bebê Dragão": {"elixir": 4, "tipo": "aerea"},
    "Servos": {"elixir": 3, "tipo": "aerea"},
    "Morcegos": {"elixir": 2, "tipo": "aerea"},
    "Caçador": {"elixir": 4, "tipo": "aerea"},
    "Mago": {"elixir": 5, "tipo": "aerea"},
    "Executor": {"elixir": 5, "tipo": "aerea"},
    "Arqueiro Mágico": {"elixir": 4, "tipo": "aerea"},

    # Feitiços pequenos
    "Zap": {"elixir": 2, "tipo": "small_spell"},
    "Flechas": {"elixir": 3, "tipo": "small_spell"},
    "Bola de Neve": {"elixir": 2, "tipo": "small_spell"},
    "O Tronco": {"elixir": 2, "tipo": "small_spell"},
    "Barril de Bárbaro": {"elixir": 2, "tipo": "small_spell"},

    # Feitiços grandes
    "Bola de Fogo": {"elixir": 4, "tipo": "big_spell"},
    "Veneno": {"elixir": 4, "tipo": "big_spell"},
    "Relâmpago": {"elixir": 6, "tipo": "big_spell"},
    "Foguete": {"elixir": 6, "tipo": "big_spell"},
    "Terremoto": {"elixir": 3, "tipo": "big_spell"},

    # Estruturas
    "Canhão": {"elixir": 3, "tipo": "building"},
    "Torre Inferno": {"elixir": 5, "tipo": "building"},
    "Tesla": {"elixir": 4, "tipo": "building"},

    # Ciclo
    "Esqueletos": {"elixir": 1, "tipo": "cycle"},
    "Goblins": {"elixir": 2, "tipo": "cycle"},
    "Espírito de Gelo": {"elixir": 1, "tipo": "cycle"},
    "Espírito Elétrico": {"elixir": 1, "tipo": "cycle"},
}


# ==========================================================
# FUNÇÃO PARA GERAR DECK
# ==========================================================

def gerar_deck(elixir_desejado):

    melhor_deck = None
    melhor_pontuacao = float("-inf")
    melhor_media = 0

    for _ in range(15000):

        deck = random.sample(list(cartas.keys()), 8)

        tipos = [cartas[carta]["tipo"] for carta in deck]

        # --------------------------------------------------
        # ELIXIR
        # --------------------------------------------------

        soma_elixir = sum(cartas[carta]["elixir"] for carta in deck)
        media = soma_elixir / 8

        diferenca_elixir = abs(media - elixir_desejado)

        # Quanto mais próximo do desejado, melhor
        pontuacao = 20 - (diferenca_elixir * 15)

        # --------------------------------------------------
        # CONDIÇÃO DE VITÓRIA
        # --------------------------------------------------

        if "win_condition" in tipos:
            pontuacao += 20
        else:
            pontuacao -= 30

        # --------------------------------------------------
        # DEFESA
        # --------------------------------------------------

        quantidade_defesa = tipos.count("defesa")

        if quantidade_defesa >= 1:
            pontuacao += 8

        if quantidade_defesa >= 2:
            pontuacao += 5

        # --------------------------------------------------
        # DEFESA AÉREA
        # --------------------------------------------------

        quantidade_aerea = tipos.count("aerea")

        if quantidade_aerea >= 1:
            pontuacao += 10

        if quantidade_aerea >= 2:
            pontuacao += 5

        # --------------------------------------------------
        # FEITIÇOS
        # --------------------------------------------------

        if "small_spell" in tipos:
            pontuacao += 8

        if "big_spell" in tipos:
            pontuacao += 10

        # --------------------------------------------------
        # CICLO
        # --------------------------------------------------

        if "cycle" in tipos:
            pontuacao += 5

        # --------------------------------------------------
        # EVITAR MUITAS CARTAS PESADAS
        # --------------------------------------------------

        cartas_pesadas = sum(
            1 for carta in deck
            if cartas[carta]["elixir"] >= 6
        )

        if cartas_pesadas >= 4:
            pontuacao -= 15

        # --------------------------------------------------
        # EVITAR DECK MUITO LEVE
        # --------------------------------------------------

        if media < 2:
            pontuacao -= 10

        # --------------------------------------------------
        # SALVAR MELHOR DECK
        # --------------------------------------------------

        if pontuacao > melhor_pontuacao:

            melhor_pontuacao = pontuacao
            melhor_deck = deck
            melhor_media = media

    return melhor_deck, melhor_media


# ==========================================================
# ROTA PRINCIPAL
# ==========================================================

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        try:
            elixir_desejado = float(request.form["elixir"])

            if elixir_desejado < 1 or elixir_desejado > 9:
                return render_template(
                    "index.html",
                    erro="Digite um elixir entre 1 e 9."
                )

        except ValueError:

            return render_template(
                "index.html",
                erro="Digite um número válido."
            )

        deck, elixir_medio = gerar_deck(elixir_desejado)

        return render_template(
            "criar_deck.html",
            deck=deck,
            cartas=cartas,
            elixir_medio=round(elixir_medio, 2)
        )

    return render_template("index.html")


# ==========================================================
# INICIAR SERVIDOR
# ==========================================================

if __name__ == "__main__":
    app.run(debug=True)

