# app.py
import streamlit as st
from story import HISTORY, get_cena

# Configuração da página
st.set_page_config(
    page_title="História em Quadrinhos",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS BÁSICO E LIMPO
def aplicar_css():
    st.markdown("""
        <style>
        /* Remove tudo do Streamlit */
        .stApp {
            background: #0a0a0a !important;
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
        #MainMenu {display: none !important;}
        footer {display: none !important;}
        header {display: none !important;}
        .stDeployButton {display: none !important;}
        
        /* Container principal */
        .main-container {
            background: #0a0a0a;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        /* Título */
        .titulo {
            font-size: 3.5rem;
            font-weight: 900;
            color: #ffffff;
            font-family: 'Georgia', serif;
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
        
        /* Imagens */
        .imagem-container {
            max-width: 900px;
            width: 100%;
            margin: 0 auto;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.8);
        }
        
        .imagem-container img {
            width: 100%;
            height: auto;
            display: block;
        }
        
        /* Botões - TODOS OS BOTÕES USAM STREAMLIT */
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
            font-family: 'Arial', sans-serif !important;
        }
        
        .stButton button:hover {
            background: #d4a843 !important;
            color: #0a0a0a !important;
            box-shadow: 0 10px 40px rgba(212,168,67,0.3) !important;
        }
        
        /* Botão COMEÇAR (dourado cheio) */
        .btn-comecar button {
            background: #d4a843 !important;
            color: #0a0a0a !important;
            border: none !important;
        }
        
        .btn-comecar button:hover {
            background: #e8c86a !important;
            transform: scale(1.02) !important;
        }
        
        /* Pergunta da escolha */
        .pergunta {
            color: #ffffff;
            font-size: 1.4rem;
            font-weight: 300;
            text-align: center;
            margin: 30px 0 20px 0;
            font-family: 'Georgia', serif;
        }
        
        /* Mensagem final */
        .mensagem {
            color: #d4a843;
            font-size: 1.3rem;
            text-align: center;
            margin: 30px 0;
            font-family: 'Georgia', serif;
        }
        
        /* Responsivo */
        @media (max-width: 768px) {
            .titulo {
                font-size: 2.5rem;
            }
            .stButton button {
                font-size: 0.8rem !important;
                padding: 14px 20px !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES ---
def inicializar_estado():
    if "cena_atual" not in st.session_state:
        st.session_state.cena_atual = "inicio"

def ir_para_cena(cena_id):
    if cena_id in HISTORY:
        st.session_state.cena_atual = cena_id
        st.rerun()

def reiniciar_historia():
    st.session_state.cena_atual = "inicio"
    st.rerun()

# --- APLICAR CSS ---
aplicar_css()

# --- INICIALIZAR ---
inicializar_estado()

# --- CONTAINER ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# --- CENA ATUAL ---
cena_id = st.session_state.cena_atual
cena = get_cena(cena_id)

if cena:
    # ===== TELA INICIAL =====
    if cena["tipo"] == "inicio":
        st.markdown(f"""
            <h1 class="titulo">{cena.get("titulo", "História")}</h1>
            <div class="linha"></div>
            <p class="subtitulo">{cena.get("descricao", "")}</p>
        """, unsafe_allow_html=True)
        
        # Capa - ALT VAZIO!
        st.markdown(f"""
            <div class="imagem-container">
                <img src="{cena['imagem']}" alt="">
            </div>
        """, unsafe_allow_html=True)
        
        # Botão COMEÇAR
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="btn-comecar">', unsafe_allow_html=True)
            if st.button("▶ COMEÇAR", key="comecar", use_container_width=True):
                ir_para_cena("cena_01")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== CENA NORMAL =====
    elif cena["tipo"] == "cena":
        # Imagem - ALT VAZIO!
        st.markdown(f"""
            <div class="imagem-container">
                <img src="{cena['imagem']}" alt="">
            </div>
        """, unsafe_allow_html=True)
        
        # Botão CONTINUAR
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("▶ CONTINUAR", key="continuar", use_container_width=True):
                if "proxima" in cena:
                    ir_para_cena(cena["proxima"])
    
    # ===== CENA DE ESCOLHA =====
    elif cena["tipo"] == "escolha":
        # Imagem - ALT VAZIO!
        st.markdown(f"""
            <div class="imagem-container">
                <img src="{cena['imagem']}" alt="">
            </div>
        """, unsafe_allow_html=True)
        
        # Pergunta
        st.markdown(f'<p class="pergunta">{cena.get("pergunta", "O que fazer?")}</p>', unsafe_allow_html=True)
        
        # Botões de escolha
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
        # Imagem - ALT VAZIO!
        st.markdown(f"""
            <div class="imagem-container">
                <img src="{cena['imagem']}" alt="">
            </div>
        """, unsafe_allow_html=True)
        
        # Mensagem
        if "mensagem" in cena:
            st.markdown(f'<p class="mensagem">✦ {cena["mensagem"]} ✦</p>', unsafe_allow_html=True)
        
        # Botão RECOMEÇAR
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("↻ RECOMEÇAR", key="reiniciar", use_container_width=True):
                reiniciar_historia()

st.markdown('</div>', unsafe_allow_html=True)