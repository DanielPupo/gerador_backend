# Este dicionário diz ao Gemini exatamente quais campos ele deve responder
TEAM_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "nome_do_time": {"type": "STRING", "description": "O nome criativo da esclação ou time"},
        "quantidade_de_jogadores": {"type": "STRING", "description": "Quantidade de jogadores totais (ex: '11 jogadores')"},
        "qualidades_do_time": {"type": "STRING", "description": "Time com muita técnica, força, entrosamento, etc."},
        "jogadores": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Lista de jogadores e seus respectivos clubes"
        },
        "variabilidade_do_time": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Como esse time pode jogar, diferentes esquemas táticos e posições dos jogadores"
        }
    },
    "required": ["nome_do_time", "quantidade_de_jogadores", "qualidades_do_time", "jogadores", "variabilidade_do_time"]
}

SYSTEM_INSTRUCTION = """
    Você é um Técnico de futebol profissional renomado. Sua tarefa é criar escalações incríveis e perfeitas utilizando prioritariamente os jogadores fornecidos pelo usuário. 
    Você pode sugerir jogadores extras (como os reservas ou suplentes) se necessário para o time ficar completo.
    Você DEVE preencher todos os campos do esquema fornecido estritamente em português.
    -O nome do time deve ser criativo e relacionado com as qualidades do time.
    -A quantidade de jogadores deve ser expressa em palavras, não em números (ex: '11 jogadores', não '11').
    -As qualidades do time devem ser descritas de forma detalhada, falando sobre a técnica, força, entrosamento, etc.
    -A lista de jogadores deve conter o nome do jogador e seu respectivo clube entre parênteses (ex: 'Neymar (PSG)').
    -A variabilidade do time deve falar sobre os diferentes esquemas táticos e posições dos jogadores, como o time pode jogar.
    - Não utilize jogadores que não sejam de futebol, ou seja, não utilize jogadores de outros esportes.
    - Não utilize jogadores que não sejam atletas, ou seja, não utilize atores, cantores, etc.
"""