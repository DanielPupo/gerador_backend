import os
from dotenv import load_dotenv

load_dotenv()

# Configurações da API do Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-pro"

SYSTEM_INSTRUCTION = """
Você é o motor de inteligência por trás de um gerador de elencos táticos baseado estritamente na estética e mecânicas do modo Ultimate Team do jogo EA SPORTS FC (antigo FIFA). 
Sua missão é receber uma requisição tática ou tema do usuário e montar um esquadrão perfeito e ultra-realista.

REGRAS CRÍTICAS DE NEGÓCIO PARA EVITAR BUGS:
1. VALIDAÇÃO DE ATLETAS EXISTENTES: Você NUNCA deve inventar jogadores ou utilizar nomes sugeridos pelo usuário que sejam fictícios, humorísticos ou desconhecidos. Utilize apenas jogadores de futebol reais, profissionais ativos (ou lendas consagradas do futebol que possuam cartas no jogo) que estejam presentes na base de dados internacional da API-Sports. Se o usuário sugerir um nome inválido ou desconhecido, ignore a sugestão dele e substitua por um jogador real e famoso que se encaixe no contexto tático.
2. CONSISTÊNCIA DE NOMES: Escreva os nomes dos jogadores e dos clubes em seu formato internacional padrão para maximizar a taxa de acerto na busca da API de fotos (ex: usar 'Vinícius Júnior' em vez de 'Vini', 'Manchester City' em vez de 'City').
3. COMPOSIÇÃO DO ELENCO: O time principal deve ter EXATAMENTE 11 jogadores distribuídos perfeitamente conforme a formação tática escolhida. O banco de reservas deve conter EXATAMENTE 7 jogadores adicionais reais.
4. ATRIBUTOS EA FC: Para cada jogador titular, atribua valores realistas de 1 a 99 para as 6 características principais do jogo de acordo com a posição (PAC, SHO, PAS, DRI, DEF, PHY) e determine um Overall (OVR) condizente. Selecione também um PlayStyle+ (ex: Finesse Shot+, Power Shot+, Intercept+, Whipped Pass+, Technical+).
"""

TEAM_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "nome_do_time": {"type": "STRING", "description": "Nome customizado para o elenco (ex: Galácticos EA, Samba Stars)."},
        "formacao_tatica": {"type": "STRING", "description": "Formação clássica do EA FC (ex: 4-3-3, 4-2-3-1, 3-5-2, 4-4-2)."},
        "quimica_total": {"type": "INTEGER", "description": "Química calculada do elenco de 0 a 33 baseada em ligas e nacionalidades comuns."},
        "estilo_de_jogo": {"type": "STRING", "description": "Diretriz tática principal do time (ex: Tiki-Taka, Contra-Ataque Veloz, Pressão Alta)."},
        "jogadores": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "nome_completo": {"type": "STRING", "description": "Nome completo do jogador de futebol real."},
                    "clube": {"type": "STRING", "description": "Nome oficial do clube atual do jogador."},
                    "posicao_campo": {"type": "STRING", "description": "Sigla internacional da posição no EA FC (ex: GK, CB, LB, RB, CDM, CM, CAM, LW, RW, ST)."},
                    "overall": {"type": "INTEGER", "description": "Pontuação geral de atributos do jogador (OVR) de 40 a 99."},
                    "playstyle_plus": {"type": "STRING", "description": "Habilidade especial assinatura (ex: Finesse Shot+, Power Shot+, Intercept+, Jockey+)."},
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
            "description": "Lista contendo exatamente 11 jogadores titulares mapeados na formação."
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
            "description": "Lista contendo exatamente 7 jogadores reservas de alto nível."
        },
        "instrucoes_de_jogador": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Diretrizes táticas para os jogadores (ex: 'Laterais: Ficar na Defesa', 'Atacantes: Chegar por Trás')."
        }
    },
    "required": ["nome_do_time", "formacao_tatica", "quimica_total", "estilo_de_jogo", "jogadores", "jogadores_reservas", "instrucoes_de_jogador"]
}