# app.py
import streamlit as st
import streamlit.components.v1 as components
from story import HISTORY, get_cena

import base64
from pathlib import Path


@st.cache_data(show_spinner=False)
def imagem_base64(caminho):
    """Converte a imagem do projeto em Base64 para o <img> do HTML.
    Aceita caminhos relativos e também caminhos antigos do Codespaces.
    """
    recebido = Path(str(caminho))
    raiz = Path(__file__).parent

    candidatos = []
    if recebido.is_absolute():
        candidatos.append(recebido)
        # Converte caminhos antigos /workspaces/... para a pasta atual do projeto.
        partes = recebido.parts
        if "assets" in partes:
            i = partes.index("assets")
            candidatos.append(raiz.joinpath(*partes[i:]))
    else:
        candidatos.append(raiz / recebido)
        candidatos.append(Path.cwd() / recebido)

    arquivo = next((x for x in candidatos if x.exists() and x.is_file()), None)
    if arquivo is None:
        return ""

    tipos = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    tipo = tipos.get(arquivo.suffix.lower(), "application/octet-stream")
    dados = base64.b64encode(arquivo.read_bytes()).decode("utf-8")
    return f"data:{tipo};base64,{dados}"

# ==========================================
# CONFIGURAÇÃO
# ==========================================
st.set_page_config(
    page_title="A Garrafa do Futuro",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CSS GLOBAL
# ==========================================
def aplicar_css():
    st.markdown("""
        <style>
        /* ===== BASE ===== */
        html, body, [data-testid="stAppViewContainer"] {
            background: #ffffff !important;
        }

        .stApp {
            background: #ffffff !important;
            color: #222222 !important;
        }

        .main > div, .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }

        #MainMenu, footer, header, .stDeployButton {
            display: none !important;
        }

        /* ===== CARTÃO PRINCIPAL ===== */
        .main-container {
            width: calc(100% - 32px);
            max-width: 1500px;
            min-height: calc(100vh - 32px);
            margin: 16px auto;
            padding: clamp(22px, 3vw, 42px);
            background: #ffffff;
            border-radius: 28px;
            box-shadow: 0 10px 35px rgba(0,0,0,0.10);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            overflow: hidden;
        }

        /* ===== TÍTULO ===== */
        .titulo {
            width: 100%;
            font-size: clamp(2rem, 4vw, 4rem);
            line-height: 1.08;
            font-weight: 800;
            color: #222222;
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0 0 8px 0;
        }

        .subtitulo {
            width: 100%;
            font-size: clamp(0.9rem, 1.5vw, 1.2rem);
            line-height: 1.4;
            color: #667085;
            text-align: center;
            margin: 0 0 8px 0;
        }

        .linha {
            width: 90px;
            height: 4px;
            background: #e4aa2c;
            border-radius: 999px;
            margin: 12px auto 26px auto;
        }

        /* ===== IMAGEM ===== */
        .imagem-container {
            width: 100%;
            max-width: 1420px;
            margin: 0 auto 24px auto;
            background: #ffffff;
            border: 1px solid #eeeeee;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 8px 28px rgba(0,0,0,0.10);
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .imagem-container img {
            width: 100%;
            max-width: 100%;
            max-height: 76vh;
            height: auto;
            object-fit: contain;
            display: block;
        }

        /* A capa fica no topo. A caixa acompanha a imagem e nunca cria um
           grande espaço branco quando o arquivo não é encontrado. */
        .imagem-capa {
            min-height: 0;
            height: auto;
            margin-top: 0;
            margin-bottom: 28px;
        }

        .imagem-capa img {
            width: 100%;
            max-height: calc(100vh - 80px);
            height: auto;
            object-fit: contain;
        }

        /* ===== BOTÕES ===== */
        .stButton {
            display: flex;
            justify-content: center;
        }

        .stButton button {
            min-height: 52px !important;
            padding: 12px 30px !important;
            font-size: 0.95rem !important;
            font-weight: 800 !important;
            border-radius: 12px !important;
            border: none !important;
            background: #e4aa2c !important;
            color: #ffffff !important;
            transition: transform 0.18s ease, box-shadow 0.18s ease !important;
        }

        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(228,170,44,0.28) !important;
        }

        .btn-comecar button {
            background: #e4aa2c !important;
            color: #ffffff !important;
        }

        /* ===== TEXTO DAS CENAS ===== */
        .pergunta {
            width: 100%;
            max-width: 1200px;
            color: #44546a;
            background: #f6f7f8;
            border-left: 5px solid #718096;
            border-radius: 12px;
            padding: 18px 24px;
            font-size: clamp(1rem, 1.8vw, 1.35rem);
            line-height: 1.55;
            text-align: left;
            margin: 8px auto 22px auto;
            font-family: Arial, sans-serif;
            box-sizing: border-box;
        }

        .mensagem {
            color: #26834b;
            font-size: clamp(1rem, 1.8vw, 1.3rem);
            text-align: center;
            margin: 18px 0;
            font-family: Arial, sans-serif;
            font-weight: 700;
        }

        /* ===== RESPONSIVO ===== */
        @media (max-width: 768px) {
            .main-container {
                width: calc(100% - 16px);
                min-height: calc(100vh - 16px);
                margin: 8px auto;
                padding: 16px;
                border-radius: 20px;
            }

            .imagem-container {
                border-radius: 14px;
                margin-bottom: 18px;
            }

            .imagem-container img {
                max-height: 68vh;
            }

            .pergunta {
                padding: 14px 16px;
            }
        }
        </style>
    """, unsafe_allow_html=True)


# ==========================================
# DADOS DO QUIZ (2 perguntas = 2 desafios)
# ==========================================
PERGUNTAS_QUIZ = [
    {
        "pergunta": "Karla mostra a garrafa de PET encontrada pelos amigos e pergunta: qual decisão ajuda a dar um destino correto ao material e evita que ele permaneça no ambiente causando impactos?",
        "alternativas": {
            "A": "Juntá-la com outros resíduos sem separar os materiais",
            "B": "Colocá-la no lixo comum junto aos demais resíduos",
            "C": "Deixá-la em um terreno vazio até encontrar uma nova utilidade",
            "D": "Levá-la a um ponto de coleta ou encaminhá-la para reciclagem"
        },
        "correta": "D"
    },
    {
        "pergunta": "Depois de descobrirem o que significa PET, os amigos precisam escolher uma atitude para diminuir o problema antes que novas garrafas sejam produzidas. Qual decisão atende melhor a esse objetivo?",
        "alternativas": {
            "A": "Aumentar os pontos de coleta para receber mais garrafas descartáveis",
            "B": "Guardar as garrafas usadas para evitar que sejam encontradas no ambiente",
            "C": "Substituir garrafas descartáveis por recipientes que possam ser usados novamente",
            "D": "Separar as garrafas usadas e enviá-las para uma cooperativa"
        },
        "correta": "C"
    }
]


# ==========================================
# ESTADO
# ==========================================
def inicializar_estado():
    if "cena_atual" not in st.session_state:
        st.session_state.cena_atual = "inicio"
    if "quiz_pontuacao" not in st.session_state:
        st.session_state.quiz_pontuacao = 0
    if "quiz_respondeu" not in st.session_state:
        st.session_state.quiz_respondeu = False
    if "quiz_resposta_dada" not in st.session_state:
        st.session_state.quiz_resposta_dada = None
    if "quiz_finalizado" not in st.session_state:
        st.session_state.quiz_finalizado = False


def ir_para_cena(cena_id):
    st.session_state.cena_atual = cena_id
    st.session_state.quiz_respondeu = False
    st.session_state.quiz_resposta_dada = None
    st.session_state.quiz_finalizado = False
    st.rerun()


def reiniciar_historia():
    st.session_state.cena_atual = "inicio"
    st.session_state.quiz_pontuacao = 0
    st.session_state.quiz_respondeu = False
    st.session_state.quiz_resposta_dada = None
    st.session_state.quiz_finalizado = False
    st.rerun()


# ==========================================
# DESAFIO: QUIZ (usado para pergunta 1 e pergunta 2)
# ==========================================
def renderizar_quiz(numero_pergunta):
    """numero_pergunta: 0 ou 1 (índice da pergunta)"""
    
    st.markdown("""
        <style>
        .quiz-wrapper {
            background: #ffffff !important;
            min-height: 100vh;
            padding: 40px 20px;
        }
        .quiz-box {
            max-width: 800px;
            margin: 0 auto;
        }
        .quiz-card {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        }
        .quiz-numero {
            color: #4ade80;
            font-size: 0.9rem;
            font-weight: bold;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-bottom: 15px;
            font-family: Arial, sans-serif;
        }
        .quiz-texto {
            color: #333333;
            font-size: 1.15rem;
            line-height: 1.6;
            font-family: Georgia, serif;
        }
        .quiz-karla {
            display: inline-block;
            background: #4ade80;
            color: #ffffff;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            text-align: center;
            line-height: 40px;
            font-weight: bold;
            font-size: 1.2rem;
            margin-right: 10px;
            vertical-align: middle;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="quiz-wrapper"><div class="quiz-box">', unsafe_allow_html=True)
    
    pergunta = PERGUNTAS_QUIZ[numero_pergunta]
    
    # Card da pergunta
    st.markdown(f"""
        <div class="quiz-card">
            <div class="quiz-numero">
                <span class="quiz-karla">K</span> Desafio de Karla
            </div>
            <div class="quiz-texto">{pergunta["pergunta"]}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # ===== NÃO RESPONDEU =====
    if not st.session_state.quiz_respondeu:
        for letra, texto in pergunta["alternativas"].items():
            if st.button(f"{letra})  {texto}", key=f"alt_{numero_pergunta}_{letra}"):
                st.session_state.quiz_respondeu = True
                st.session_state.quiz_resposta_dada = letra
                st.rerun()
    
    # ===== RESPONDEU =====
    else:
        resposta_dada = st.session_state.quiz_resposta_dada
        resposta_correta = pergunta["correta"]
        
        for letra, texto in pergunta["alternativas"].items():
            if letra == resposta_correta:
                st.markdown(f"""
                    <div style="padding: 14px 20px; margin-bottom: 8px; border-radius: 10px;
                                background: rgba(74, 222, 128, 0.2); border: 1px solid #e5e7eb;
                                color: #ffffff; font-family: Arial;">
                        <strong>{letra})</strong> {texto} ✅
                    </div>
                """, unsafe_allow_html=True)
            elif letra == resposta_dada:
                st.markdown(f"""
                    <div style="padding: 14px 20px; margin-bottom: 8px; border-radius: 10px;
                                background: rgba(239, 68, 68, 0.2); border: 2px solid #ef4444;
                                color: #ffffff; font-family: Arial;">
                        <strong>{letra})</strong> {texto} ❌
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="padding: 14px 20px; margin-bottom: 8px; border-radius: 10px;
                                background: rgba(255, 255, 255, 0.05); border: 1px solid #333;
                                color: #888; font-family: Arial;">
                        <strong>{letra})</strong> {texto}
                    </div>
                """, unsafe_allow_html=True)
        
        if resposta_dada == resposta_correta:
            st.markdown("""
                <div style="background: rgba(74, 222, 128, 0.15); border-left: 4px solid #4ade80;
                            border-radius: 8px; padding: 20px; margin: 20px 0; color: #4ade80;
                            font-size: 1.1rem; font-weight: bold; font-family: Arial;">
                    ✅ Resposta correta! Karla está orgulhosa de vocês!
                </div>
            """, unsafe_allow_html=True)
        else:
            texto_correto = pergunta["alternativas"][resposta_correta]
            st.markdown(f"""
                <div style="background: rgba(239, 68, 68, 0.15); border-left: 4px solid #ef4444;
                            border-radius: 8px; padding: 20px; margin: 20px 0; color: #fca5a5;
                            font-size: 1.1rem; font-weight: bold; font-family: Arial;">
                    ❌ Resposta incorreta.
                    <span style="color: #4ade80; display: block; margin-top: 10px; font-size: 1rem;">
                        💡 Resposta correta: {resposta_correta}) {texto_correto}
                    </span>
                </div>
            """, unsafe_allow_html=True)
        
        # Botão recomeçar
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("↻ RECOMEÇAR HISTÓRIA", key=f"reiniciar_quiz_{numero_pergunta}"):
                reiniciar_historia()
    
    st.markdown('</div></div>', unsafe_allow_html=True)


# ==========================================
# DESAFIO: DECODIFICAR PLÁSTICOS (7 números)
# ==========================================
def renderizar_desafio_plasticos():
    html_desafio = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: Arial, sans-serif;
            background: #f5f1e8;
            color: #222;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            width: 100%;
            max-width: 950px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 35px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        }
        h1 {
            text-align: center;
            font-size: 28px;
            margin-bottom: 25px;
            color: #222;
        }
        .karla {
            background: #f0f0f0;
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 25px;
            font-size: 16px;
            line-height: 1.5;
            color: #222;
        }
        .karla strong { display: block; margin-bottom: 5px; }
        h2 {
            font-size: 18px;
            margin-top: 25px;
            margin-bottom: 12px;
            color: #222;
        }
        .banco {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin-bottom: 30px;
        }
        .palavra {
            background: #eeeeee;
            border-radius: 8px;
            padding: 9px 13px;
            font-weight: bold;
            font-size: 14px;
            color: #222;
        }
        .numeros {
            display: flex;
            justify-content: space-between;
            gap: 10px;
            margin: 30px 0;
        }
        .numero {
            flex: 1;
            min-height: 70px;
            border: none;
            border-bottom: 3px solid #222;
            background: transparent;
            font-size: 30px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.2s;
            color: #222;
        }
        .numero:hover { background: #f0f0f0; }
        .numero.selecionado { background: #e6e6e6; }
        .numero.concluido { border-bottom: 4px solid #333; background: #dcdcdc; }
        .desafio {
            display: none;
            margin-top: 20px;
            padding: 25px;
            border-radius: 15px;
            background: #f7f7f7;
        }
        .desafio.ativo { display: block; }
        .pista-titulo {
            font-weight: bold;
            font-size: 19px;
            margin-bottom: 10px;
            color: #222;
        }
        .pista {
            font-size: 17px;
            line-height: 1.5;
            margin-bottom: 20px;
            color: #333;
        }
        .opcoes {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .opcao {
            border: 2px solid #333;
            background: white;
            border-radius: 9px;
            padding: 11px 16px;
            cursor: pointer;
            font-weight: bold;
            transition: 0.2s;
            font-size: 14px;
            color: #222;
        }
        .opcao:hover { background: #eeeeee; }
        .opcao:disabled { cursor: default; }
        .feedback {
            margin-top: 18px;
            font-weight: bold;
            font-size: 17px;
            min-height: 25px;
        }
        .final {
            display: none;
            margin-top: 25px;
            padding: 22px;
            background: #eeeeee;
            border-radius: 12px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            color: #222;
        }
        @media (max-width: 650px) {
            .container { padding: 20px; }
            h1 { font-size: 22px; }
            .numeros { gap: 4px; }
            .numero { font-size: 22px; min-height: 55px; }
            .pista { font-size: 15px; }
        }
    </style>
    </head>
    <body>
    <div class="container">
        <h1>DESAFIO — DECODIFIQUE OS PLÁSTICOS</h1>
        <div class="karla">
            <strong>KARLA:</strong>
            "Esses números não estão aqui por acaso. Cada um representa um tipo de plástico. Use as pistas para descobrir qual é qual!"
        </div>
        <h2>BANCO DE PALAVRAS</h2>
        <div class="banco">
            <span class="palavra">PP</span>
            <span class="palavra">PET</span>
            <span class="palavra">PVC</span>
            <span class="palavra">PS</span>
            <span class="palavra">LDPE</span>
            <span class="palavra">OTHER</span>
            <span class="palavra">HDPE</span>
        </div>
        <h2>IDENTIFIQUE CADA PLÁSTICO</h2>
        <div class="numeros">
            <button class="numero" onclick="abrirDesafio(1)">①</button>
            <button class="numero" onclick="abrirDesafio(2)">②</button>
            <button class="numero" onclick="abrirDesafio(3)">③</button>
            <button class="numero" onclick="abrirDesafio(4)">④</button>
            <button class="numero" onclick="abrirDesafio(5)">⑤</button>
            <button class="numero" onclick="abrirDesafio(6)">⑥</button>
            <button class="numero" onclick="abrirDesafio(7)">⑦</button>
        </div>
        <div id="desafio" class="desafio">
            <div class="pista-titulo" id="pistaTitulo"></div>
            <div class="pista" id="pista"></div>
            <div class="opcoes" id="opcoes"></div>
            <div class="feedback" id="feedback"></div>
        </div>
        <div id="final" class="final">
            🎉 Parabéns! Você decodificou todos os tipos de plástico!
        </div>
    </div>
    <script>
    const desafios = {
        1: { pista: "Sou transparente, leve e muito usado em garrafas de água e refrigerante. Minha sigla tem três letras.", resposta: "PET" },
        2: { pista: "Sou conhecido por ser resistente e apareço bastante em embalagens de produtos de limpeza, frascos e recipientes.", resposta: "HDPE" },
        3: { pista: "Posso aparecer em canos, tubos e alguns tipos de embalagens. Meu nome é formado por três letras.", resposta: "PVC" },
        4: { pista: "Sou mais flexível e apareço bastante em sacolas plásticas, filmes e embalagens.", resposta: "LDPE" },
        5: { pista: "Posso ser encontrado em potes, tampas e embalagens de alimentos. Sou conhecido por resistir bem ao calor.", resposta: "PP" },
        6: { pista: "Sou usado em alguns copos descartáveis, bandejas e embalagens. Meu nome começa com 'poliestireno'.", resposta: "PS" },
        7: { pista: "Não sou um único tipo de plástico. Essa categoria reúne outros plásticos que não se encaixam nos seis anteriores.", resposta: "OTHER" }
    };
    const palavras = ["PP", "PET", "PVC", "PS", "LDPE", "OTHER", "HDPE"];
    let numeroAtual = null;
    let resolvidos = [];
    
    function abrirDesafio(numero) {
        numeroAtual = numero;
        const d = desafios[numero];
        document.getElementById("desafio").classList.add("ativo");
        document.getElementById("pistaTitulo").textContent = "PISTA " + numero;
        document.getElementById("pista").textContent = '"' + d.pista + '"';
        document.getElementById("feedback").textContent = "";
        criarOpcoes();
        document.querySelectorAll(".numero").forEach((b, i) => {
            b.classList.remove("selecionado");
            if (i + 1 === numero) b.classList.add("selecionado");
        });
    }
    
    function criarOpcoes() {
        const area = document.getElementById("opcoes");
        area.innerHTML = "";
        palavras.forEach(p => {
            const b = document.createElement("button");
            b.className = "opcao";
            b.textContent = p;
            b.onclick = () => verificarResposta(p);
            area.appendChild(b);
        });
    }
    
    function verificarResposta(resposta) {
        const correta = desafios[numeroAtual].resposta;
        const fb = document.getElementById("feedback");
        if (resposta === correta) {
            fb.textContent = "✓ Acertou!";
            fb.style.color = "#247a3d";
            if (!resolvidos.includes(numeroAtual)) resolvidos.push(numeroAtual);
            document.querySelectorAll(".numero")[numeroAtual - 1].classList.add("concluido");
            document.querySelectorAll(".opcao").forEach(b => b.disabled = true);
            if (resolvidos.length === 7) {
                setTimeout(() => {
                    document.getElementById("final").style.display = "block";
                    document.getElementById("desafio").classList.remove("ativo");
                }, 600);
            }
        } else {
            fb.textContent = "✗ Tente novamente!";
            fb.style.color = "#b3261e";
        }
    }
    </script>
    </body>
    </html>
    """
    
    components.html(html_desafio, height=760, scrolling=False)
    
    # Botão recomeçar
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("↻ RECOMEÇAR HISTÓRIA", key="reiniciar_plasticos"):
            reiniciar_historia()


# ==========================================
# DESAFIO: POLÍMERO
# ==========================================
def renderizar_desafio_polimero():
    html_polimero = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: Arial, sans-serif;
            background: #ffffff;
            padding: 20px;
        }
        .desafio {
            width: 100%;
            max-width: 900px;
            background: white;
            padding: clamp(24px, 5vw, 48px);
            border-radius: 22px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        }
        h1 {
            font-size: 24px;
            margin-bottom: 30px;
            color: #222;
        }
        .pergunta {
            font-size: 19px;
            line-height: 1.6;
            color: #333;
        }
        .dica {
            display: none;
            margin: 20px 0;
            padding: 18px;
            background: #f5f5f5;
            border-left: 4px solid #555;
            border-radius: 8px;
            text-align: left;
            line-height: 1.5;
            font-size: 15px;
            color: #333;
        }
        button {
            border: none;
            padding: 13px 22px;
            margin: 10px 5px;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            background: #222;
            color: white;
            transition: 0.2s;
            font-size: 15px;
        }
        button:hover {
            transform: translateY(-2px);
            opacity: 0.9;
        }
        input {
            width: 100%;
            padding: 15px;
            margin-top: 20px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
            outline: none;
        }
        input:focus { border-color: #555; }
        #resultado {
            margin-top: 20px;
            font-size: 18px;
            font-weight: bold;
        }
        .acerto { color: #247a3d; }
        .erro { color: #b3261e; }
    </style>
    </head>
    <body>
    <div class="desafio">
        <h1>DESAFIO — DECODIFIQUE OS PLÁSTICOS</h1>
        <p class="pergunta">
            O PET é um <strong>__________</strong> formado pela repetição
            de unidades menores, formando uma cadeia de moléculas.
        </p>
        <button onclick="mostrarDica()" id="dicaBtn">💡 VER DICA</button>
        <div class="dica" id="dica">
            "Imagine um colar: uma grande estrutura construída pela repetição
            de várias peças menores. Na Química, damos um nome específico para
            esse tipo de estrutura. Começa com P."
        </div>
        <input type="text" id="resposta" placeholder="Digite sua resposta..." autocomplete="off">
        <button onclick="verificarResposta()" id="responderBtn">RESPONDER</button>
        <div id="resultado"></div>
    </div>
    <script>
    function mostrarDica() {
        const d = document.getElementById("dica");
        const b = document.getElementById("dicaBtn");
        if (d.style.display === "none" || d.style.display === "") {
            d.style.display = "block";
            b.textContent = "🙈 ESCONDER DICA";
        } else {
            d.style.display = "none";
            b.textContent = "💡 VER DICA";
        }
    }
    
    function verificarResposta() {
        const c = document.getElementById("resposta");
        const r = document.getElementById("resultado");
        const b = document.getElementById("responderBtn");
        const resp = c.value.trim().toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g, "");
        if (resp === "polimero") {
            r.textContent = "🎉 ACERTOU! O PET é um polímero.";
            r.className = "acerto";
            c.disabled = true;
            b.disabled = true;
            b.style.opacity = "0.5";
            b.style.cursor = "default";
        } else {
            r.textContent = "❌ Quase! Tente novamente.";
            r.className = "erro";
            c.value = "";
            c.focus();
        }
    }
    </script>
    </body>
    </html>
    """
    
    components.html(html_polimero, height=680, scrolling=False)
    
    # Botão recomeçar
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("↻ RECOMEÇAR HISTÓRIA", key="reiniciar_polimero"):
            reiniciar_historia()


# ==========================================
# APLICAR
# ==========================================
aplicar_css()
inicializar_estado()

# ==========================================
# CONTAINER
# ==========================================
st.markdown('<div class="main-container">', unsafe_allow_html=True)

cena_id = st.session_state.cena_atual

# ==========================================
# DESAFIOS (TELAS SEPARADAS)
# ==========================================
if cena_id == "desafio_quiz_1":
    renderizar_quiz(0)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

if cena_id == "desafio_quiz_2":
    renderizar_quiz(1)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

if cena_id == "desafio_plasticos":
    renderizar_desafio_plasticos()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

if cena_id == "desafio_polimero":
    renderizar_desafio_polimero()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# CENAS DA HISTÓRIA
# ==========================================
cena = get_cena(cena_id)

if cena:
    # ===== INÍCIO =====
    if cena["tipo"] == "inicio":
        # ===== IMAGEM DA CAPA: PRIMEIRO ELEMENTO DA TELA =====
        st.markdown(f"""
            <div class="imagem-container imagem-capa">
                <img src="{imagem_base64(cena['imagem'])}" alt="Capa da história">
            </div>
        """, unsafe_allow_html=True)

        # Título e descrição aparecem depois da imagem
        st.markdown(f"""
            <h1 class="titulo">{cena.get("titulo", "História")}</h1>
            <div class="linha"></div>
            <p class="subtitulo">{cena.get("descricao", "")}</p>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="btn-comecar">', unsafe_allow_html=True)
            if st.button("▶ COMEÇAR", key="comecar", use_container_width=True):
                ir_para_cena("pagina_01")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== CENA =====
    elif cena["tipo"] == "cena":
        st.markdown(f"""
            <div class="imagem-container">
                <img src="{imagem_base64(cena['imagem'])}" alt="Imagem da cena">
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("▶ CONTINUAR", key="continuar", use_container_width=True):
                if "proxima" in cena:
                    ir_para_cena(cena["proxima"])
    
    # ===== ESCOLHA =====
    elif cena["tipo"] == "escolha":
        st.markdown(f"""
            <div class="imagem-container">
                <img src="{imagem_base64(cena['imagem'])}" alt="Imagem da cena">
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f'<p class="pergunta">{cena.get("pergunta", "O que fazer?")}</p>', unsafe_allow_html=True)
        
        opcoes = list(cena["opcoes"].items())
        if len(opcoes) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                if st.button(opcoes[0][0], key="escolha_1", use_container_width=True):
                    ir_para_cena(opcoes[0][1])
            with col2:
                if st.button(opcoes[1][0], key="escolha_2", use_container_width=True):
                    ir_para_cena(opcoes[1][1])
    
    # ===== FINAL =====
    elif cena["tipo"] == "final":
        st.markdown(f"""
            <div class="imagem-container">
                <img src="{imagem_base64(cena['imagem'])}" alt="Imagem da cena">
            </div>
        """, unsafe_allow_html=True)
        
        if "mensagem" in cena:
            st.markdown(f'<p class="mensagem">✦ {cena["mensagem"]} ✦</p>', unsafe_allow_html=True)
        
        # Botão de desafio específico para cada final
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Final 1 → Quiz Pergunta 1
            if cena_id == "feedback_01b":
                if st.button("🎯 FAZER O DESAFIO", key="ir_desafio_1", use_container_width=True):
                    ir_para_cena("desafio_quiz_1")
            
            # Final 2 → Quiz Pergunta 2
            elif cena_id == "feedback_02a":
                if st.button("🎯 FAZER O DESAFIO", key="ir_desafio_2", use_container_width=True):
                    ir_para_cena("desafio_quiz_2")
            
            # Final 3 → Decodificar Plásticos
            elif cena_id == "feedback_03a":
                if st.button("🎯 FAZER O DESAFIO", key="ir_desafio_3", use_container_width=True):
                    ir_para_cena("desafio_plasticos")
            
            # Final 4 (vitória) → Polímero
            elif cena_id == "pagina_12b":
                if st.button("🎯 FAZER O DESAFIO FINAL", key="ir_desafio_4", use_container_width=True):
                    ir_para_cena("desafio_polimero")

st.markdown('</div>', unsafe_allow_html=True)