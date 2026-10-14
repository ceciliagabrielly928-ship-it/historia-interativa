# =========================================================
# A GARRAFA DO FUTURO
# app.py
# =========================================================

import streamlit as st
import streamlit.components.v1 as components
from story import HISTORY, get_cena
from pathlib import Path
import base64


# =========================================================
# CONFIGURAÇÃO
# =========================================================

st.set_page_config(
    page_title="A Garrafa do Futuro",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# IMAGENS
# =========================================================

def caminho_imagem(caminho):
    if not caminho:
        return None

    caminho = str(caminho).replace("\\", "/")

    candidatos = [
        Path(caminho),
        Path(__file__).resolve().parent / caminho.lstrip("/")
    ]

    if "/assets/" in caminho:
        rel = "assets/" + caminho.split("/assets/", 1)[1]
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

    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif"
    }.get(arquivo.suffix.lower(), "application/octet-stream")

    dados = base64.b64encode(arquivo.read_bytes()).decode("ascii")

    return f"data:{mime};base64,{dados}"


def renderizar_imagem(caminho, alt="Imagem da história"):
    uri = imagem_data_uri(caminho)

    if uri is None:
        st.error(f"Imagem não encontrada: {caminho}")
        return False

    st.markdown(
        f"""
        <div class="imagem-container">
            <img src="{uri}" alt="{alt}">
        </div>
        """,
        unsafe_allow_html=True
    )

    return True


# =========================================================
# CSS GLOBAL
# =========================================================

def aplicar_css():
    st.markdown(
        """
        <style>

        .stApp { background: #ffffff !important; }

        .main > div {
            padding: 0 !important;
            max-width: 100% !important;
        }

        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
            padding-top: 0 !important;
        }

        .stApp > div:first-child { margin-top: 0 !important; }

        #MainMenu { display: none !important; }
        footer { display: none !important; }
        header { display: none !important; }
        .stDeployButton { display: none !important; }

        /* =========================================
           CONTAINER PRINCIPAL
        ========================================= */

        .main-container {
            background: #ffffff;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            padding: 18px 18px 40px 18px;
        }

        /* =========================================
           TÍTULO
        ========================================= */

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

        /* =========================================
           IMAGEM
        ========================================= */

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

        /* =========================================
           BOTÕES
        ========================================= */

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

        /* =========================================
           TEXTOS
        ========================================= */

        .pergunta {
            color: #333333;
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

        /* =========================================
           CENAS NORMAIS
        ========================================= */

        .texto-cena {
            width: min(1000px, 100%);
            margin: 0 auto 25px auto;
            color: #333333;
            font-family: Georgia, serif;
            font-size: 1.25rem;
            line-height: 1.7;
            text-align: center;
        }

        .personagem {
            color: #d4a843;
            font-family: Arial, sans-serif;
            font-weight: 700;
            font-size: 1rem;
            text-align: center;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .dialogo {
            width: min(900px, 100%);
            margin: 0 auto 25px auto;
            padding: 20px 25px;
            background: #faf8f4;
            border-left: 4px solid #d4a843;
            border-radius: 10px;
            color: #333;
            font-family: Georgia, serif;
            font-size: 1.15rem;
            line-height: 1.6;
            text-align: center;
        }

        @media (max-width: 768px) {
            .main-container { padding: 10px 10px 30px 10px; }
            .titulo { font-size: 2.2rem; }
            .imagem-container { border-radius: 16px; margin-bottom: 16px; }
            .imagem-container img { max-height: 70vh; }
            .stButton button {
                font-size: 0.8rem !important;
                padding: 14px 20px !important;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# QUIZ — PERGUNTAS
# =========================================================

PERGUNTAS_QUIZ = [
    {
        "pergunta":
            "Karla mostra a garrafa de PET encontrada pelos amigos e pergunta: "
            "qual decisão ajuda a dar um destino correto ao material e evita que "
            "ele permaneça no ambiente causando impactos?",
        "alternativas": {
            "A": "Juntá-la com outros resíduos sem separar os materiais",
            "B": "Colocá-la no lixo comum junto aos demais resíduos",
            "C": "Deixá-la em um terreno vazio até encontrar uma nova utilidade",
            "D": "Levá-la a um ponto de coleta ou encaminhá-la para reciclagem"
        },
        "correta": "D"
    },
    {
        "pergunta":
            "Depois de descobrirem o que significa PET, os amigos precisam escolher "
            "uma atitude para diminuir o problema antes que novas garrafas sejam "
            "produzidas. Qual decisão atende melhor a esse objetivo?",
        "alternativas": {
            "A": "Aumentar os pontos de coleta para receber mais garrafas descartáveis",
            "B": "Guardar as garrafas usadas para evitar que sejam encontradas no ambiente",
            "C": "Substituir garrafas descartáveis por recipientes que possam ser usados novamente",
            "D": "Separar as garrafas usadas e enviá-las para uma cooperativa"
        },
        "correta": "C"
    }
]


# =========================================================
# ESTADO
# =========================================================

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


def _checar_reset_via_url():
    """
    Permite que botões DENTRO dos iframes (components.html)
    acionem um recomeço de história via query param ?reset=1.
    """
    try:
        reset = st.query_params.get("reset")
    except Exception:
        try:
            reset = st.experimental_get_query_params().get("reset", [None])[0]
        except Exception:
            reset = None

    if reset == "1":
        st.session_state.cena_atual = "inicio"
        st.session_state.quiz_pontuacao = 0
        st.session_state.quiz_respondeu = False
        st.session_state.quiz_resposta_dada = None
        st.session_state.quiz_finalizado = False

        try:
            st.query_params.clear()
        except Exception:
            try:
                st.experimental_set_query_params()
            except Exception:
                pass


# =========================================================
# QUIZ — RENDERIZAÇÃO
# =========================================================

def renderizar_quiz(numero_pergunta):
    pergunta = PERGUNTAS_QUIZ[numero_pergunta]

    st.markdown(
        """
        <style>

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.meu-quiz-container) {
            background-color: #ffffff !important;
            border-radius: 20px !important;
            box-shadow: 0 15px 45px rgba(0, 0, 0, 0.06) !important;
            border: 1px solid #e7e2da !important;
            padding: 35px 45px !important;
            margin: 15px auto !important;
            width: 100% !important;
            max-width: 1100px !important;
        }

        .quiz-header {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0 auto 28px auto;
            width: 100%;
        }

        .quiz-titulo {
            color: #292929;
            font-family: Arial, sans-serif;
            font-size: 28px;
            font-weight: 800;
            letter-spacing: 3px;
            text-align: center;
            margin-bottom: 13px;
        }

        .quiz-linha {
            width: 55px;
            height: 3px;
            background: #d4b04d;
            border-radius: 3px;
            margin: 0 auto;
        }

        .quiz-pergunta {
            background: #faf7f0;
            border-left: 4px solid #d4b04d;
            border-radius: 14px;
            padding: 22px 25px;
            margin: 0 auto 30px auto;
            color: #333333;
            font-family: Arial, sans-serif;
            font-size: 17px;
            line-height: 1.7;
            text-align: left;
            width: 100%;
            box-sizing: border-box;
        }

        div[data-testid="stButton"] { margin-bottom: 14px !important; }

        div[data-testid="stButton"] > button {
            width: 100% !important;
            min-height: 58px !important;
            border-radius: 8px !important;
            border: 2px solid #d4b04d !important;
            background: #ffffff !important;
            color: #bd9638 !important;
            font-family: Arial, sans-serif !important;
            font-size: 15px !important;
            font-weight: 600 !important;
            letter-spacing: 0 !important;
            text-transform: none !important;
            text-align: left !important;
            padding: 14px 20px !important;
            box-shadow: none !important;
            transition: all 0.2s ease-in-out !important;
        }

        div[data-testid="stButton"] > button:hover {
            background: #fffaf0 !important;
            border-color: #b88e30 !important;
            color: #b88e30 !important;
        }

        .box-resposta {
            padding: 14px 20px;
            margin-bottom: 14px;
            border-radius: 8px;
            font-family: Arial, sans-serif;
            font-size: 15px;
            font-weight: 600;
            letter-spacing: 0;
            text-align: left;
        }

        .quiz-feedback {
            margin-top: 10px;
            margin-bottom: 10px;
            padding: 16px 18px;
            border-radius: 8px;
            text-align: center;
            font-family: Arial, sans-serif;
            font-size: 15px;
            line-height: 1.5;
        }

        .area-recomecar { margin-top: 25px; }

        @media (max-width: 650px) {
            div[data-testid="stVerticalBlockBorderWrapper"]:has(.meu-quiz-container) {
                padding: 22px 16px !important;
            }
            .quiz-titulo { font-size: 23px; letter-spacing: 2px; }
            .quiz-pergunta { font-size: 15px; padding: 18px; }
            div[data-testid="stButton"] > button {
                font-size: 14px !important;
                padding: 12px 14px !important;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([0.2, 12, 0.2])

    with col2:
        with st.container(border=True):

            st.markdown(
                '<div class="meu-quiz-container"></div>',
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div class="quiz-header">
                    <div class="quiz-titulo">DESAFIO</div>
                    <div class="quiz-linha"></div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="quiz-pergunta">
                    {pergunta["pergunta"]}
                </div>
                """,
                unsafe_allow_html=True
            )

            for letra, texto in pergunta["alternativas"].items():

                if not st.session_state.quiz_respondeu:

                    if st.button(
                        f"{letra}) {texto}",
                        key=f"quiz_{numero_pergunta}_{letra}",
                        use_container_width=True
                    ):
                        st.session_state.quiz_respondeu = True
                        st.session_state.quiz_resposta_dada = letra

                        if letra == pergunta["correta"]:
                            st.session_state.quiz_pontuacao += 1

                        st.rerun()

                else:

                    resposta_dada = st.session_state.quiz_resposta_dada
                    correta = pergunta["correta"]

                    if letra == correta:
                        st.markdown(
                            f"""
                            <div class="box-resposta"
                                style="background:#edf7ed;border:2px solid #75ad75;color:#286b2f;">
                                ✓ &nbsp; {letra}) &nbsp; {texto}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    elif letra == resposta_dada:
                        st.markdown(
                            f"""
                            <div class="box-resposta"
                                style="background:#fff0f0;border:2px solid #d88b8b;color:#8a3030;">
                                ✕ &nbsp; {letra}) &nbsp; {texto}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"""
                            <div class="box-resposta"
                                style="background:#ffffff;border:2px solid #d4b04d;color:#bd9638;">
                                {letra}) &nbsp; {texto}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            if st.session_state.quiz_respondeu:

                resposta_dada = st.session_state.quiz_resposta_dada
                correta = pergunta["correta"]

                if resposta_dada == correta:
                    st.markdown(
                        """
                        <div class="quiz-feedback"
                            style="background:#edf7ed;border:1.5px solid #75ad75;color:#286b2f;">
                            <strong>Resposta correta!</strong>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="quiz-feedback"
                            style="background:#fff0f0;border:1.5px solid #d88b8b;color:#8a3030;">
                            <strong>Não foi dessa vez!</strong>
                            <br>
                            A resposta correta é
                            <strong>{correta})</strong>.
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.markdown('<div class="area-recomecar">', unsafe_allow_html=True)

                if st.button(
                    "↻ RECOMEÇAR HISTÓRIA",
                    key=f"reiniciar_quiz_{numero_pergunta}",
                    use_container_width=True
                ):
                    reiniciar_historia()

                st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# DESAFIO — DECODIFIQUE OS PLÁSTICOS (7 números)
# =========================================================

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
        background: transparent;
        color: #292929;
        padding: 10px;
    }

    /* =========================================
       CARD ARREDONDADO — IGUAL AO DO QUIZ
    ========================================= */

    .container {
        width: 100%;
        max-width: 1000px;
        margin: 0 auto;
        background: #ffffff;
        border: 1px solid #e7e2da;
        border-radius: 20px;
        padding: 40px 50px 45px;
        box-shadow: 0 15px 45px rgba(0, 0, 0, 0.06);
    }

    /* =========================================
       HEADER PADRONIZADO — DESAFIO + LINHA DOURADA
    ========================================= */

    .desafio-header {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0 auto 30px auto;
        width: 100%;
    }

    .desafio-titulo {
        color: #292929;
        font-family: Arial, sans-serif;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: 3px;
        text-align: center;
        margin-bottom: 13px;
    }

    .desafio-linha {
        width: 55px;
        height: 3px;
        background: #d4b04d;
        border-radius: 3px;
        margin: 0 auto;
    }

    /* =========================================
       CAIXA DA KARLA — MESMO ESTILO DA PERGUNTA DO QUIZ
    ========================================= */

    .karla {
        background: #faf7f0;
        border-left: 4px solid #d4b04d;
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 32px;
        font-size: 15px;
        line-height: 1.7;
        font-family: Arial, sans-serif;
        color: #333333;
    }
    .karla strong {
        display: block;
        margin-bottom: 6px;
        font-size: 13px;
        letter-spacing: 1.5px;
        color: #b28c24;
    }

    h2 {
        font-size: 14px;
        font-weight: 800;
        letter-spacing: 2px;
        text-align: center;
        margin: 27px 0 15px;
        color: #666;
        font-family: Arial, sans-serif;
    }

    .banco, .numeros, .opcoes {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 9px;
    }
    .banco { margin-bottom: 32px; }

    .palavra {
        border: 1px solid #cbb15e;
        border-radius: 999px;
        padding: 8px 18px;
        font-size: 13px;
        font-weight: 700;
        color: #bd9638;
        background: #ffffff;
        font-family: Arial, sans-serif;
    }

    .numeros { gap: 12px; margin: 22px 0 28px; }

    .numero {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 65px;
        height: 65px;
        border: 2px solid #d9d7d2;
        border-radius: 50%;
        background: #fff;
        font-size: 25px;
        font-weight: 700;
        cursor: pointer;
        color: #333;
        font-family: Arial, sans-serif;
        transition: all 0.2s;
    }

    .numero:hover, .opcao:hover:not(:disabled) {
        border-color: #d4b04d;
        background: #fffaf0;
    }

    .numero.selecionado, .numero.concluido {
        border-color: #d4b04d;
        background: #d4b04d;
        color: #fff;
    }

    .desafio {
        display: none;
        margin-top: 25px;
        padding: 27px 28px 30px;
        border: 1px solid #e4e0d8;
        border-radius: 17px;
        background: #faf9f6;
        text-align: center;
    }
    .desafio.ativo { display: block; }

    .pista-titulo {
        font-weight: 800;
        font-size: 14px;
        letter-spacing: 2px;
        margin-bottom: 14px;
        color: #b28c24;
        font-family: Arial, sans-serif;
    }

    .pista {
        font-size: 16px;
        line-height: 1.65;
        margin-bottom: 23px;
        font-family: Arial, sans-serif;
        color: #333;
    }

    .opcao {
        border: 2px solid #d4b04d;
        background: #fff;
        border-radius: 8px;
        padding: 11px 22px;
        cursor: pointer;
        font-weight: 700;
        font-size: 14px;
        color: #bd9638;
        font-family: Arial, sans-serif;
        transition: all 0.2s;
    }
    .opcao:hover:not(:disabled) {
        background: #fffaf0;
        border-color: #b88e30;
        color: #b88e30;
    }
    .opcao:disabled { cursor: default; opacity: 0.6; }

    .feedback {
        margin-top: 18px;
        font-weight: 700;
        font-size: 15px;
        min-height: 25px;
        font-family: Arial, sans-serif;
    }

    .final {
        display: none;
        margin-top: 25px;
        padding: 25px 20px;
        background: #faf7f0;
        border: 1px solid #e4d7ae;
        border-radius: 12px;
        text-align: center;
        font-size: 18px;
        font-weight: 700;
        line-height: 1.6;
        font-family: Arial, sans-serif;
        color: #333;
    }

    /* =========================================
       BOTÃO RECOMEÇAR — MESMO ESTILO DO QUIZ
    ========================================= */

    .btn-recomecar {
        display: none;
        margin: 26px auto 0 auto;
        width: 100%;
        max-width: 460px;
        background: transparent;
        color: #d4a843;
        border: 2px solid #d4a843;
        border-radius: 4px;
        padding: 16px 40px;
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 4px;
        text-transform: uppercase;
        cursor: pointer;
        font-family: Arial, sans-serif;
        transition: all 0.3s ease;
    }
    .btn-recomecar:hover {
        background: #d4a843;
        color: #0a0a0a;
        box-shadow: 0 10px 40px rgba(212, 168, 67, 0.3);
    }

    @media (max-width: 650px) {
        body { padding: 5px; }
        .container { padding: 28px 20px; border-radius: 18px; }
        .desafio-titulo { font-size: 22px; letter-spacing: 2px; }
        .numero { width: 50px; height: 50px; font-size: 21px; }
        .desafio { padding: 22px 15px; }
        .btn-recomecar { font-size: 13px; padding: 14px 24px; letter-spacing: 3px; }
    }
    </style>
    </head>
    <body>
    <div class="container">

    <div class="desafio-header">
        <div class="desafio-titulo">DESAFIO</div>
        <div class="desafio-linha"></div>
    </div>

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
    <button class="numero" type="button" onclick="abrirDesafio(1)">1</button>
    <button class="numero" type="button" onclick="abrirDesafio(2)">2</button>
    <button class="numero" type="button" onclick="abrirDesafio(3)">3</button>
    <button class="numero" type="button" onclick="abrirDesafio(4)">4</button>
    <button class="numero" type="button" onclick="abrirDesafio(5)">5</button>
    <button class="numero" type="button" onclick="abrirDesafio(6)">6</button>
    <button class="numero" type="button" onclick="abrirDesafio(7)">7</button>
    </div>

    <div id="desafio" class="desafio">
    <div id="pistaTitulo" class="pista-titulo"></div>
    <div id="pista" class="pista"></div>
    <div id="opcoes" class="opcoes"></div>
    <div id="feedback" class="feedback"></div>
    </div>

    <div id="final" class="final">
    <p>Parabéns! Você decodificou todos os tipos de plástico!</p>
    <button class="btn-recomecar" type="button" onclick="recomecarHistoria()">
        ↻ RECOMEÇAR HISTÓRIA
    </button>
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
    const resolvidos = new Set();

    function abrirDesafio(numero) {
        numeroAtual = numero;
        document.getElementById("desafio").classList.add("ativo");
        document.getElementById("final").style.display = "none";

        document.getElementById("pistaTitulo").textContent = "PISTA " + numero;
        document.getElementById("pista").textContent = '"' + desafios[numero].pista + '"';

        const feedback = document.getElementById("feedback");
        feedback.textContent = "";
        feedback.style.color = "";

        document.querySelectorAll(".numero").forEach((botao, i) => {
            botao.classList.toggle("selecionado", i + 1 === numero);
            botao.classList.toggle("concluido", resolvidos.has(i + 1));
        });

        const area = document.getElementById("opcoes");
        area.innerHTML = "";
        palavras.forEach(palavra => {
            const botao = document.createElement("button");
            botao.type = "button";
            botao.className = "opcao";
            botao.textContent = palavra;
            botao.onclick = () => verificarResposta(palavra);
            area.appendChild(botao);
        });

        if (resolvidos.has(numero)) {
            feedback.textContent = "✓ Você já resolveu este desafio!";
            feedback.style.color = "#247a3d";
            area.querySelectorAll("button").forEach(botao => { botao.disabled = true; });
        }
    }

    function verificarResposta(resposta) {
        const feedback = document.getElementById("feedback");
        if (resposta === desafios[numeroAtual].resposta) {
            feedback.textContent = "✓ Acertou!";
            feedback.style.color = "#247a3d";

            resolvidos.add(numeroAtual);
            document.querySelectorAll(".numero")[numeroAtual - 1].classList.add("concluido");
            document.querySelectorAll(".opcao").forEach(botao => { botao.disabled = true; });

            if (resolvidos.size === 7) {
                document.getElementById("desafio").classList.remove("ativo");
                document.getElementById("final").style.display = "block";
            }
        } else {
            feedback.textContent = "✗ Tente novamente!";
            feedback.style.color = "#b3261e";
        }
    }

    function recomecarHistoria() {
        try {
            const url = new URL(window.parent.location.href);
            url.searchParams.set("reset", "1");
            window.parent.location.href = url.toString();
        } catch (e) {
            try {
                window.top.location.href = "?reset=1";
            } catch (e2) {
                window.top.location.reload();
            }
        }
    }
    </script>
    </body>
    </html>
    """

    components.html(html_desafio, height=1000, scrolling=True)


# =========================================================
# DESAFIO — POLÍMERO (LACUNA / PREENCHER)
# =========================================================

def renderizar_desafio_polimero():

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
        background: transparent;
        color: #292929;
        padding: 10px;
    }

    /* =========================================
       CARD ARREDONDADO — IGUAL AO DO QUIZ
    ========================================= */

    .container {
        width: 100%;
        max-width: 720px;
        margin: 0 auto;
        background: #ffffff;
        border: 1px solid #e7e2da;
        border-radius: 20px;
        padding: 45px 55px 45px;
        box-shadow: 0 15px 45px rgba(0, 0, 0, 0.06);
        text-align: center;
    }

    /* =========================================
       HEADER PADRONIZADO — DESAFIO + LINHA DOURADA
    ========================================= */

    .desafio-header {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0 auto 32px auto;
        width: 100%;
    }

    .desafio-titulo {
        color: #292929;
        font-family: Arial, sans-serif;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: 3px;
        text-align: center;
        margin-bottom: 13px;
    }

    .desafio-linha {
        width: 55px;
        height: 3px;
        background: #d4b04d;
        border-radius: 3px;
        margin: 0 auto;
    }

    /* =========================================
       TEXTO DO DESAFIO COM LACUNA
    ========================================= */

    .texto-desafio {
        font-size: 17px;
        line-height: 1.9;
        color: #333333;
        margin-bottom: 30px;
        max-width: 560px;
        margin-left: auto;
        margin-right: auto;
        text-align: center;
        font-family: Arial, sans-serif;
    }

    .lacuna {
        display: inline-block;
        min-width: 130px;
        border-bottom: 2px solid #333333;
        margin: 0 6px;
        height: 1.1em;
        vertical-align: middle;
    }

    /* =========================================
       BOTÃO DICA
    ========================================= */

    .btn-dica {
        background-color: #222222;
        color: #ffffff;
        border: none;
        border-radius: 10px;
        padding: 12px 26px;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1.2px;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 22px;
        transition: background 0.2s;
        font-family: Arial, sans-serif;
    }
    .btn-dica:hover { background-color: #3b3b3b; }

    .dica-box {
        display: none;
        background: #faf7f0;
        border-left: 4px solid #d4b04d;
        padding: 14px 18px;
        font-size: 14px;
        color: #555555;
        border-radius: 8px;
        margin: 0 auto 22px auto;
        text-align: left;
        max-width: 560px;
        line-height: 1.6;
        font-family: Arial, sans-serif;
    }

    /* =========================================
       INPUT DE RESPOSTA
    ========================================= */

    .input-resposta {
        width: 100%;
        max-width: 560px;
        padding: 16px 20px;
        font-size: 16px;
        font-family: Arial, sans-serif;
        border: 1.5px solid #d8d3ca;
        border-radius: 10px;
        outline: none;
        background: #ffffff;
        color: #333333;
        margin: 0 auto 26px auto;
        display: block;
        transition: border-color 0.2s, box-shadow 0.2s;
    }

    .input-resposta::placeholder { color: #a8a39b; }

    .input-resposta:focus {
        border-color: #222222;
        box-shadow: 0 0 0 3px rgba(34, 34, 34, 0.06);
    }

    .input-resposta:disabled {
        background: #f5f5f5;
        color: #555;
        cursor: not-allowed;
    }

    /* =========================================
       BOTÃO RESPONDER
    ========================================= */

    .btn-acao {
        background-color: #222222;
        color: #ffffff;
        border: none;
        border-radius: 10px;
        padding: 14px 42px;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 1.5px;
        cursor: pointer;
        transition: background 0.2s;
        font-family: Arial, sans-serif;
    }
    .btn-acao:hover { background-color: #3b3b3b; }

    .btn-acao:disabled {
        opacity: 0.4;
        cursor: not-allowed;
    }

    .feedback {
        font-weight: 700;
        font-size: 15px;
        margin-top: 22px;
        min-height: 24px;
        font-family: Arial, sans-serif;
    }

    /* =========================================
       BOTÃO RECOMEÇAR — MESMO ESTILO DO QUIZ
       (só aparece após acertar)
    ========================================= */

    .btn-recomecar {
        display: none;
        margin: 30px auto 0 auto;
        width: 100%;
        max-width: 460px;
        background: transparent;
        color: #d4a843;
        border: 2px solid #d4a843;
        border-radius: 4px;
        padding: 16px 40px;
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 4px;
        text-transform: uppercase;
        cursor: pointer;
        font-family: Arial, sans-serif;
        transition: all 0.3s ease;
    }
    .btn-recomecar:hover {
        background: #d4a843;
        color: #0a0a0a;
        box-shadow: 0 10px 40px rgba(212, 168, 67, 0.3);
    }

    @media (max-width: 650px) {
        body { padding: 5px; }
        .container { padding: 32px 22px 32px; border-radius: 18px; }
        .desafio-titulo { font-size: 22px; letter-spacing: 2px; }
        .texto-desafio { font-size: 15px; line-height: 1.8; }
        .lacuna { min-width: 90px; }
        .input-resposta { padding: 13px 16px; font-size: 15px; }
        .btn-recomecar { font-size: 13px; padding: 14px 24px; letter-spacing: 3px; }
    }
    </style>
    </head>
    <body>
    <div class="container">

        <div class="desafio-header">
            <div class="desafio-titulo">DESAFIO</div>
            <div class="desafio-linha"></div>
        </div>

        <div class="texto-desafio">
            O PET é um <span class="lacuna"></span> formado pela repetição de
            unidades menores, formando uma cadeia de moléculas.
        </div>

        <button type="button" class="btn-dica" onclick="mostrarDica()">
            💡 VER DICA
        </button>

        <div id="dicaBox" class="dica-box">
            <strong>Dica:</strong> É uma macromolécula formada pela união
            de várias moléculas menores (monômeros). Começa com a letra 'P'.
        </div>

        <input
            type="text"
            id="respostaUsuario"
            class="input-resposta"
            placeholder="Digite sua resposta..."
            autocomplete="off"
        />

        <div>
            <button
                type="button"
                id="btnResponder"
                class="btn-acao"
                onclick="verificarRespostaPolimero()"
            >
                RESPONDER
            </button>
        </div>

        <div id="feedback" class="feedback"></div>

        <button
            type="button"
            id="btnRecomecar"
            class="btn-recomecar"
            onclick="recomecarHistoria()"
        >
            ↻ RECOMEÇAR HISTÓRIA
        </button>

    </div>

    <script>
    function mostrarDica() {
        const caixa = document.getElementById("dicaBox");
        caixa.style.display = (caixa.style.display === "block") ? "none" : "block";
    }

    function verificarRespostaPolimero() {
        const resp = document.getElementById("respostaUsuario").value.trim().toLowerCase();
        const feedback = document.getElementById("feedback");

        if (resp === "polímero" || resp === "polimero") {
            feedback.textContent = "✓ Resposta correta! Parabéns!";
            feedback.style.color = "#286b2f";

            document.getElementById("respostaUsuario").disabled = true;
            document.getElementById("btnResponder").disabled = true;

            document.getElementById("btnRecomecar").style.display = "block";

        } else {
            feedback.textContent = "✗ Tente novamente!";
            feedback.style.color = "#b3261e";
        }
    }

    function recomecarHistoria() {
        try {
            const url = new URL(window.parent.location.href);
            url.searchParams.set("reset", "1");
            window.parent.location.href = url.toString();
        } catch (e) {
            try {
                window.top.location.href = "?reset=1";
            } catch (e2) {
                window.top.location.reload();
            }
        }
    }

    document.getElementById("respostaUsuario").addEventListener("keydown", function(e) {
        if (e.key === "Enter") {
            verificarRespostaPolimero();
        }
    });
    </script>
    </body>
    </html>
    """

    components.html(html_desafio, height=700, scrolling=False)


# =========================================================
# FUNÇÃO PARA RENDERIZAR UMA CENA NORMAL
# =========================================================

def renderizar_cena_normal(cena):

    if cena.get("imagem"):
        renderizar_imagem(cena["imagem"], "Imagem da história")

    personagem = (
        cena.get("personagem")
        or cena.get("personagem_nome")
        or cena.get("nome")
    )

    texto = (
        cena.get("texto")
        or cena.get("dialogo")
        or cena.get("fala")
        or cena.get("descricao")
    )

    if personagem and texto:
        st.markdown(
            f"""
            <div class="personagem">
                {personagem}
            </div>

            <div class="dialogo">
                {texto}
            </div>
            """,
            unsafe_allow_html=True
        )
    elif texto:
        st.markdown(
            f"""
            <div class="texto-cena">
                {texto}
            </div>
            """,
            unsafe_allow_html=True
        )

    if cena.get("titulo"):
        st.markdown(
            f"""
            <h1 class="titulo">
                {cena["titulo"]}
            </h1>
            """,
            unsafe_allow_html=True
        )

    proxima = (
        cena.get("proxima")
        or cena.get("proxima_cena")
        or cena.get("proximo")
        or cena.get("next")
    )

    if proxima:
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            if st.button(
                "CONTINUAR",
                key=f"continuar_{st.session_state.cena_atual}",
                use_container_width=True
            ):
                ir_para_cena(proxima)


# =========================================================
# INÍCIO DO APP
# =========================================================

aplicar_css()
inicializar_estado()
_checar_reset_via_url()


# =========================================================
# CONTAINER PRINCIPAL
# =========================================================

st.markdown('<div class="main-container">', unsafe_allow_html=True)


# =========================================================
# CENA ATUAL
# =========================================================

cena_id = st.session_state.cena_atual


# =========================================================
# DESAFIO — QUIZ 1
# =========================================================

if cena_id == "desafio_quiz_1":
    renderizar_quiz(0)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# =========================================================
# DESAFIO — QUIZ 2
# =========================================================

elif cena_id == "desafio_quiz_2":
    renderizar_quiz(1)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# =========================================================
# DESAFIO — DECODIFIQUE OS PLÁSTICOS (7 números)
# =========================================================

elif cena_id == "desafio_plasticos":
    renderizar_desafio_plasticos()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# =========================================================
# DESAFIO — POLÍMERO (LACUNA)
# =========================================================

elif cena_id == "desafio_polimero":
    renderizar_desafio_polimero()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# =========================================================
# BUSCAR CENA NO STORY.PY
# =========================================================

cena = get_cena(cena_id)

if cena is None:
    st.error(f"Cena não encontrada: `{cena_id}`")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# =========================================================
# TIPO: INÍCIO
# =========================================================

if cena.get("tipo") == "inicio":

    if cena.get("imagem"):
        renderizar_imagem(cena["imagem"], "Capa da história")

    if cena.get("titulo"):
        st.markdown(
            f'<h1 class="titulo">{cena["titulo"]}</h1>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="linha"></div>', unsafe_allow_html=True)

    if cena.get("descricao"):
        st.markdown(
            f'<p class="subtitulo">{cena["descricao"]}</p>',
            unsafe_allow_html=True
        )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown('<div class="btn-comecar">', unsafe_allow_html=True)
        if st.button("▶ COMEÇAR", key="comecar", use_container_width=True):
            st.session_state.cena_atual = "pagina_01"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# TIPO: CENA
# =========================================================

elif cena.get("tipo") == "cena":
    renderizar_cena_normal(cena)


# =========================================================
# TIPO: ESCOLHA
# =========================================================

elif cena.get("tipo") == "escolha":

    if cena.get("imagem"):
        renderizar_imagem(cena["imagem"])

    if cena.get("pergunta"):
        st.markdown(
            f'<p class="pergunta">{cena["pergunta"]}</p>',
            unsafe_allow_html=True
        )

    opcoes = list(cena.get("opcoes", {}).items())

    if len(opcoes) >= 2:
        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                opcoes[0][0],
                key=f"escolha_1_{cena_id}",
                use_container_width=True
            ):
                ir_para_cena(opcoes[0][1])

        with col2:
            if st.button(
                opcoes[1][0],
                key=f"escolha_2_{cena_id}",
                use_container_width=True
            ):
                ir_para_cena(opcoes[1][1])


# =========================================================
# TIPO: FINAL
# =========================================================

elif cena.get("tipo") == "final":

    if cena.get("imagem"):
        renderizar_imagem(cena["imagem"])

    if cena.get("mensagem"):
        st.markdown(
            f'<p class="mensagem">✦ {cena["mensagem"]} ✦</p>',
            unsafe_allow_html=True
        )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        if cena_id == "feedback_01b":
            if st.button(
                "FAZER O DESAFIO",
                key="ir_desafio_1",
                use_container_width=True
            ):
                ir_para_cena("desafio_quiz_1")

        elif cena_id == "feedback_02a":
            if st.button(
                "FAZER O DESAFIO",
                key="ir_desafio_2",
                use_container_width=True
            ):
                ir_para_cena("desafio_quiz_2")

        elif cena_id == "feedback_03a":
            if st.button(
                "FAZER O DESAFIO",
                key="ir_desafio_3",
                use_container_width=True
            ):
                ir_para_cena("desafio_plasticos")

        elif cena_id == "pagina_12b":
            if st.button(
                "FAZER O DESAFIO FINAL",
                key="ir_desafio_4",
                use_container_width=True
            ):
                ir_para_cena("desafio_polimero")


# =========================================================
# TIPO DESCONHECIDO
# =========================================================

else:
    st.error(
        f"Tipo de cena não reconhecido: `{cena.get('tipo')}`"
    )


# =========================================================
# FECHAR CONTAINER
# =========================================================

st.markdown("</div>", unsafe_allow_html=True)