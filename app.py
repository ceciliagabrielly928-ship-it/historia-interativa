# app.py
import streamlit as st
import streamlit.components.v1 as components
from story import HISTORY, get_cena
from pathlib import Path
import base64

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
# IMAGENS
# ==========================================
def caminho_imagem(caminho):
    if not caminho:
        return None
    caminho = str(caminho).replace('\\', '/')
    candidatos = [Path(caminho), Path(__file__).resolve().parent / caminho.lstrip('/')]
    if '/assets/' in caminho:
        rel = 'assets/' + caminho.split('/assets/', 1)[1]
        candidatos.append(Path(__file__).resolve().parent / rel)
    for arquivo in candidatos:
        try:
            if arquivo.is_file():
                return arquivo
        except OSError:
            pass
    return None

def imagem_data_uri(caminho):
    arquivo = caminho_imagem(caminho)
    if arquivo is None:
        return None
    mime = {'.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp','.gif':'image/gif'}.get(arquivo.suffix.lower(), 'application/octet-stream')
    dados = base64.b64encode(arquivo.read_bytes()).decode('ascii')
    return f'data:{mime};base64,{dados}'

def renderizar_imagem(caminho, alt='Imagem da história'):
    uri = imagem_data_uri(caminho)
    if uri is None:
        st.error(f'Imagem não encontrada: {caminho}')
        return False
    st.markdown(f'''
        <div class="imagem-container">
            <img src="{uri}" alt="{alt}">
        </div>
    ''', unsafe_allow_html=True)
    return True


# ==========================================
# CSS GLOBAL
# ==========================================
def aplicar_css():
    st.markdown("""
        <style>
        .stApp { background: #ffffff !important; }
        .main > div { padding: 0 !important; max-width: 100% !important; }
        .block-container { padding: 0 !important; max-width: 100% !important; padding-top: 0 !important; }
        .stApp > div:first-child { margin-top: 0 !important; }
        #MainMenu {display: none !important;}
        footer {display: none !important;}
        header {display: none !important;}
        .stDeployButton {display: none !important;}
        
        .main-container {
            background: #ffffff;
            min-height: 0vh;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            padding: 18px 18px 40px 18px;
        }
        
        .titulo {
            font-size: 3.5rem;
            font-weight: 900;
            color: #222222;
            font-family: Georgia, serif;
            text-align: center;
            margin-bottom: 5px;
        }
        
        .subtitulo {
            font-size: 0.9rem;
            color: #666;
            text-align: center;
            letter-spacing: 4px;
            text-transform: uppercase;
            margin-bottom: 20px;
        }
        
        .linha {
            width: 60px;
            height: 2px;
            background: #d4a843;
            margin: 10px auto 25px auto;
        }
        
        .imagem-container {
            width: min(1000px, 100%);
            margin: 0 auto 22px auto;
            background: #ffffff;
            border: 1px solid #e5e5e5;
            border-radius: 24px;
            overflow: hidden;
            box-shadow: 0 8px 28px rgba(0,0,0,0.10);
        }
        
        .imagem-container img {
            width: 100%;
            max-height: 85vh;
            height: auto;
            object-fit: contain;
            display: block;
            margin: 0 auto;
        }
        
        .stButton button {
            width: 100% !important;
            padding: 16px 40px !important;
            font-size: 1rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 4px !important;
            border-radius: 4px !important;
            border: 2px solid #d4a843 !important;
            background: transparent !important;
            color: #d4a843 !important;
            transition: all 0.3s ease !important;
            font-family: Arial, sans-serif !important;
        }
        
        .stButton button:hover {
            background: #d4a843 !important;
            color: #0a0a0a !important;
            box-shadow: 0 10px 40px rgba(212,168,67,0.3) !important;
        }
        
        .btn-comecar button {
            background: #d4a843 !important;
            color: #0a0a0a !important;
            border: none !important;
        }
        
        .btn-comecar button:hover {
            background: #e8c86a !important;
            transform: scale(1.02) !important;
        }
        
        .pergunta {
            color: #ffffff;
            font-size: 1.4rem;
            font-weight: 300;
            text-align: center;
            margin: 30px 0 20px 0;
            font-family: Georgia, serif;
        }
        
        .mensagem {
            color: #d4a843;
            font-size: 1.3rem;
            text-align: center;
            margin: 30px 0;
            font-family: Georgia, serif;
        }
        
        @media (max-width: 768px) {
            .main-container { padding: 10px 10px 30px 10px; }
            .titulo { font-size: 2.2rem; }
            .imagem-container { border-radius: 16px; margin-bottom: 16px; }
            .imagem-container img { max-height: 70vh; }
            .stButton button { font-size: 0.8rem !important; padding: 14px 20px !important; }
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
            background: #0d1f0d !important;
            min-height: 100vh;
            padding: 40px 20px;
        }
        .quiz-box {
            max-width: 800px;
            margin: 0 auto;
        }
        .quiz-card {
            background: rgba(20, 40, 20, 0.9);
            border: 2px solid #4ade80;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 10px 40px rgba(74, 222, 128, 0.2);
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
            color: #ffffff;
            font-size: 1.15rem;
            line-height: 1.6;
            font-family: Georgia, serif;
        }
        .quiz-karla {
            display: inline-block;
            background: #4ade80;
            color: #0d1f0d;
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
                                background: rgba(74, 222, 128, 0.2); border: 2px solid #4ade80;
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
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }

    body {
        font-family: Arial, sans-serif;
        background:  #ffffff;
        color: #222;
        padding: 28px 20px 35px;
    }

    .container {
        width: 100%;
        max-width: 900px;
        margin: 0 auto;
        background: #ffffff;
        border-radius: 24px;
        padding: 38px 45px 42px;
        border: 1px solid #e9e2d6;
        box-shadow: 0 12px 35px rgba(0,0,0,0.09);
    }

    /* ===== TÍTULO ===== */

    h1 {
        text-align: center;
        font-size: 27px;
        font-weight: 800;
        margin-bottom: 12px;
        color: #222;
        letter-spacing: 0.5px;
    }

    h1::after {
        content: "";
        display: block;
        width: 55px;
        height: 3px;
        background: #d4a843;
        border-radius: 10px;
        margin: 13px auto 28px;
    }

    /* ===== FALA DA KARLA ===== */

    .karla {
        background: #faf7f0;
        border-left: 4px solid #d4a843;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 30px;
        font-size: 16px;
        line-height: 1.6;
        color: #444;
    }

    .karla strong {
        display: block;
        margin-bottom: 5px;
        color: #222;
        font-size: 14px;
        letter-spacing: 1.5px;
    }

    /* ===== TÍTULOS DAS SEÇÕES ===== */

    h2 {
        font-size: 15px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 25px;
        margin-bottom: 15px;
        color: #555;
        text-align: center;
    }

    /* ===== BANCO DE PALAVRAS ===== */

    .banco {
        display: flex;
        flex-wrap: wrap;
        gap: 9px;
        justify-content: center;
        margin-bottom: 32px;
    }

    .palavra {
        background: #ffffff;
        border: 1px solid #d4a843;
        color: #333;
        border-radius: 20px;
        padding: 8px 16px;
        font-weight: 700;
        font-size: 13px;
        letter-spacing: 0.5px;
    }

    /* ===== NÚMEROS ===== */

    .numeros {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin: 22px 0 28px;
    }

    .numero {
        width: 72px;
        height: 72px;
        min-height: 72px;
        flex: none;

        border: 2px solid #d8d3ca;
        border-radius: 50%;

        background: #ffffff;
        color: #333;

        font-size: 27px;
        font-weight: 700;

        cursor: pointer;
        transition: all 0.25s ease;
    }

    .numero:hover {
        border-color: #d4a843;
        background: #faf7f0;
        transform: translateY(-4px);
        box-shadow: 0 7px 15px rgba(212,168,67,0.18);
    }

    .numero.selecionado {
        background: #d4a843;
        border-color: #d4a843;
        color: #222;
        box-shadow: 0 6px 16px rgba(212,168,67,0.25);
        transform: translateY(-3px);
    }

    .numero.concluido {
        background: #f1eee7;
        border-color: #d4a843;
        color: #8a6a20;
    }

    /* ===== ÁREA DA PISTA ===== */

    .desafio {
        display: none;
        margin-top: 10px;
        padding: 27px 30px;
        border-radius: 17px;
        background: #faf8f4;
        border: 1px solid #e8e1d5;
    }

    .desafio.ativo {
        display: block;
        animation: aparecer 0.25s ease;
    }

    @keyframes aparecer {
        from {
            opacity: 0;
            transform: translateY(8px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .pista-titulo {
        font-weight: 800;
        font-size: 14px;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 12px;
        color: #d4a843;
        text-align: center;
    }

    .pista {
        font-size: 17px;
        line-height: 1.6;
        margin-bottom: 22px;
        color: #333;
        text-align: center;
    }

    /* ===== OPÇÕES ===== */

    .opcoes {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
    }

    .opcao {
        border: 1px solid #cfc9bd;
        background: #ffffff;
        color: #333;
        border-radius: 9px;
        padding: 11px 18px;
        cursor: pointer;
        font-weight: 700;
        transition: all 0.2s ease;
        font-size: 14px;
    }

    .opcao:hover {
        background: #d4a843;
        border-color: #d4a843;
        color: #222;
        transform: translateY(-2px);
    }

    .opcao:disabled {
        cursor: default;
    }

    /* ===== FEEDBACK ===== */

    .feedback {
        margin-top: 18px;
        font-weight: 700;
        font-size: 16px;
        min-height: 25px;
        text-align: center;
    }

    /* ===== FINAL ===== */

    .final {
        display: none;
        margin-top: 25px;
        padding: 22px;
        background: #faf7f0;
        border: 1px solid #d4a843;
        border-radius: 14px;
        text-align: center;
        font-size: 18px;
        font-weight: 700;
        color: #333;
    }

    /* ===== CELULAR ===== */

    @media (max-width: 650px) {

        body {
            padding: 15px 10px 25px;
        }

        .container {
            padding: 27px 18px 30px;
            border-radius: 19px;
        }

        h1 {
            font-size: 21px;
        }

        .numeros {
            gap: 7px;
        }

        .numero {
            width: 43px;
            height: 43px;
            min-height: 43px;
            font-size: 18px;
        }

        .pista {
            font-size: 15px;
        }

        .desafio {
            padding: 22px 16px;
        }
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
            <button class="numero" onclick="abrirDesafio(1)">1</button>
            <button class="numero" onclick="abrirDesafio(2)">2</button>
            <button class="numero" onclick="abrirDesafio(3)">3</button>
            <button class="numero" onclick="abrirDesafio(4)">4</button>
            <button class="numero" onclick="abrirDesafio(5)">5</button>
            <button class="numero" onclick="abrirDesafio(6)">6</button>
            <button class="numero" onclick="abrirDesafio(7)">7</button>
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
    
    components.html(html_desafio, height=850, scrolling=True)
    
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
            background: #f4f1eb;
            padding: 20px;
        }
        .desafio {
            width: 100%;
            max-width: 650px;
            background: white;
            padding: 40px;
            border-radius: 20px;
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
    
    components.html(html_polimero, height=650, scrolling=True)
    
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
        # A CAPA APARECE IMEDIATAMENTE AO ABRIR O SITE.
        renderizar_imagem(cena["imagem"], "Capa da história")

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
        renderizar_imagem(cena["imagem"])
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("▶ CONTINUAR", key="continuar", use_container_width=True):
                if "proxima" in cena:
                    ir_para_cena(cena["proxima"])
    
    # ===== ESCOLHA =====
    elif cena["tipo"] == "escolha":
        renderizar_imagem(cena["imagem"])
        
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
        renderizar_imagem(cena["imagem"])
        
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