# =========================================================
# A GARRAFA DO FUTURO
# app.py
# =========================================================

import streamlit as st
import streamlit.components.v1 as components
from story import HISTORY, get_cena
from pathlib import Path
import base64
import textwrap


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

        candidatos.append(
            Path(__file__).resolve().parent / rel
        )

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
    }.get(
        arquivo.suffix.lower(),
        "application/octet-stream"
    )

    dados = base64.b64encode(
        arquivo.read_bytes()
    ).decode("ascii")

    return f"data:{mime};base64,{dados}"


def renderizar_imagem(
    caminho,
    alt="Imagem da história"
):

    uri = imagem_data_uri(caminho)

    if uri is None:

        st.error(
            f"Imagem não encontrada: {caminho}"
        )

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

        .stApp {
            background: #ffffff !important;
        }

        .main > div {
            padding: 0 !important;
            max-width: 100% !important;
        }

        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
            padding-top: 0 !important;
        }

        .stApp > div:first-child {
            margin-top: 0 !important;
        }

        #MainMenu {
            display: none !important;
        }

        footer {
            display: none !important;
        }

        header {
            display: none !important;
        }

        .stDeployButton {
            display: none !important;
        }


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