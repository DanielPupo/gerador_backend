def analisar_time(jogadores_info):

    quimica = 65

    ligas = []
    nacionalidades = []

    for jogador in jogadores_info.values():

        liga = jogador.get("liga")
        nacionalidade = jogador.get("nacionalidade")

        if liga:
            ligas.append(liga)

        if nacionalidade:
            nacionalidades.append(nacionalidade)

    bonus_liga = len(ligas) - len(set(ligas))
    bonus_nacionalidade = len(nacionalidades) - len(set(nacionalidades))

    quimica += bonus_liga * 3
    quimica += bonus_nacionalidade * 2

    quimica = min(quimica, 100)

    estilo = "Equilibrado"

    if quimica >= 90:
        estilo = "Elite Competitiva"

    elif quimica >= 80:
        estilo = "Controle de Posse"

    elif quimica >= 70:
        estilo = "Ataque Rápido"

    return {
        "quimica": quimica,
        "estilo": estilo,
        "dica": gerar_dica(quimica)
    }


def gerar_dica(quimica):

    if quimica >= 90:
        return "Seu time possui química absurda. Ideal para pressão alta e trocas rápidas de passe."

    if quimica >= 80:
        return "Equipe equilibrada. Excelente para controle de posse e construção ofensiva."

    return "Seu elenco possui pouca sincronia. Considere jogadores da mesma liga ou nacionalidade."