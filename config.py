# config.py

TEAM_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "nome_do_time": {"type": "STRING", "description": "Nome criativo e personalizado para o elenco (ex: Galácticos FC)."},
        "formacao_tatica": {"type": "STRING", "description": "Formação tática clássica do EA FC (ex: 4-3-3, 4-2-3-1, 3-5-2)."},
        "quimica_total": {"type": "INTEGER", "description": "Química fictícia do elenco de 0 a 33 baseada em nacionalidades e ligas."},
        "estilo_de_jogo": {"type": "STRING", "description": "Mentalidade tática (ex: Tiki-Taka, Contra-Ataque Veloz)."},
        "jogadores": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "nome_completo": {"type": "STRING", "description": "Nome completo do jogador real de futebol."},
                    "clube": {"type": "STRING", "description": "Clube atual ou histórico do jogador."},
                    "posicao_campo": {"type": "STRING", "description": "Sigla internacional da posição no EA FC (ex: GK, CB, CM, CAM, ST)."},
                    "overall": {"type": "INTEGER", "description": "Overall (OVR) do jogador de 50 a 99."},
                    "playstyle_plus": {"type": "STRING", "description": "Habilidade especial (ex: Finesse Shot+, Intercept+, Power Shot+)."},
                    "stats": {
                        "type": "OBJECT",
                        "properties": {
                            "pac": {"type": "INTEGER", "description": "Ritmo (Pace)"},
                            "sho": {"type": "INTEGER", "description": "Finalização (Shooting)"},
                            "pas": {"type": "INTEGER", "description": "Passe (Passing)"},
                            "dri": {"type": "INTEGER", "description": "Condução (Dribbling)"},
                            "def": {"type": "INTEGER", "description": "Defesa (Defending)"},
                            "phy": {"type": "INTEGER", "description": "Físico (Physicality)"}
                        },
                        "required": ["pac", "sho", "pas", "dri", "def", "phy"]
                    }
                },
                "required": ["nome_completo", "clube", "posicao_campo", "overall", "playstyle_plus", "stats"]
            },
            "description": "Lista contendo EXATAMENTE 11 jogadores titulares na ordem da formação."
        },
        "jogadores_reservas": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "nome_completo": {"type": "STRING"},
                    "clube": {"type": "STRING"},
                    "posicao_campo": {"type": "STRING"},
                    "overall": {"type": "INTEGER"}
                },
                "required": ["nome_completo", "clube", "posicao_campo", "overall"]
            },
            "description": "Lista contendo EXATAMENTE 7 jogadores reservas reais de alto nível."
        },
        "instrucoes_de_jogador": {
            "type": "ARRAY",
            "items": {"type": "STRING", "description": "Instruções individuais de jogo estilo prancheta do EA FC."}
        }
    },
    "required": ["nome_do_time", "formacao_tatica", "quimica_total", "estilo_de_jogo", "jogadores", "jogadores_reservas", "instrucoes_de_jogador"]
}

SYSTEM_INSTRUCTION = """
Você é o motor de inteligência artificial de um simulador tático baseado no modo Ultimate Team do jogo EA SPORTS FC.
Ao receber o comando do usuário, você deve montar um time competitivo seguindo estas diretrizes:
1. VALIDAÇÃO DE JOGADORES: Use APENAS jogadores reais e profissionais que existam no banco de dados mundial do futebol. Se o usuário fornecer um jogador fictício, inventado ou desconhecido, substitua imediatamente por um atleta real de elite mundial correspondente à posição.
2. ESTRUTURA: Retorne exatamente 11 titulares no objeto 'jogadores' e exatamente 7 reservas no objeto 'jogadores_reservas'.
3. ATRIBUTOS E POSIÇÕES: Defina estatísticas condizentes de 1 a 99 e posições oficiais do EA FC (GK, CB, LB, RB, CDM, CM, CAM, RW, LW, ST).
"""