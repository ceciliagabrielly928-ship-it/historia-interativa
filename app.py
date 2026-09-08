# app.py
import streamlit as st
from story import HISTORY, get_cena
import streamlit.components.v1 as components

# Configuração da página
st.set_page_config(
    page_title="História em Quadrinhos",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS para layout de QUADRINHO
def aplicar_css():
    st.markdown("""
        <style>
        /* RESET COMPLETO - REMOVE TUDO DO STREAMLIT */
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
        
        /* Esconder TODOS os elementos do Streamlit */
        #MainMenu {display: none !important;}
        footer {display: none !important;}
        header {display: none !important;}
        .stDeployButton {display: none !important;}
        .stAlert {display: none !important;}
        .stException {display: none !important;}
        
        /* Esconder qualquer botão do Streamlit */
        .stButton button {
            display: none !important;
        }
        
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
        
        /* ===== TELA INICIAL ===== */
        .pagina-inicial {
            max-width: 900px;
            width: 100%;
            text-align: center;
            padding: 40px 20px;
        }
        
        .titulo-principal {
            font-size: 4.5rem;
            font-weight: 900;
            color: #ffffff;
            font-family: 'Georgia', serif;
            margin-bottom: 10px;
            letter-spacing: 4px;
            text-shadow: 0 0 60px rgba(212,168,67,0.15);
        }
        
        .subtitulo {
            font-size: 1rem;
            color: #666;
            font-family: 'Arial', sans-serif;
            margin-bottom: 30px;
            letter-spacing: 6px;
            text-transform: uppercase;
        }
        
        .linha-dourada {
            width: 60px;
            height: 2px;
            background: #d4a843;
            margin: 15px auto 25px auto;
        }
        
        /* Imagem da capa */
        .capa-container {
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 30px 80px rgba(0,0,0,0.9);
            margin: 20px 0 35px 0;
        }
        
        .capa-container img {
            width: 100%;
            height: auto;
            display: block;
        }
        
        /* ===== BOTÃO COMEÇAR ===== */
        .btn-comecar {
            display: inline-block;
            padding: 18px 60px;
            background: #d4a843;
            color: #0a0a0a !important;
            font-size: 1.1rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 4px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Arial', sans-serif;
            text-decoration: none;
        }
        
        .btn-comecar:hover {
            background: #e8c86a;
            transform: scale(1.02);
            box-shadow: 0 10px 40px rgba(212,168,67,0.3);
        }
        
        /* ===== PÁGINA DA HISTÓRIA ===== */
        .historia-container {
            max-width: 1000px;
            width: 100%;
            margin: 0 auto;
        }
        
        .imagem-historia {
            width: 100%;
            height: auto;
            display: block;
            border-radius: 8px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.8);
        }
        
        /* ===== BOTÃO CONTINUAR ===== */
        .btn-continuar {
            display: block;
            width: 100%;
            max-width: 400px;
            margin: 35px auto 0 auto;
            padding: 16px;
            background: transparent;
            color: #d4a843;
            font-size: 0.9rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 6px;
            border: 2px solid #d4a843;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Arial', sans-serif;
            text-align: center;
        }
        
        .btn-continuar:hover {
            background: #d4a843;
            color: #0a0a0a;
        }
        
        /* ===== TELA DE ESCOLHA ===== */
        .pergunta-escolha {
            color: #ffffff;
            font-size: 1.4rem;
            font-weight: 300;
            text-align: center;
            margin: 30px 0 25px 0;
            font-family: 'Georgia', serif;
            letter-spacing: 2px;
        }
        
        .container-escolhas {
            display: flex;
            gap: 20px;
            max-width: 700px;
            margin: 0 auto;
        }
        
        .btn-escolha {
            flex: 1;
            padding: 16px 20px;
            background: transparent;
            color: #ffffff;
            font-size: 0.9rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 3px;
            border: 1px solid #333;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Arial', sans-serif;
            text-align: center;
        }
        
        .btn-escolha:hover {
            border-color: #d4a843;
            color: #d4a843;
            background: rgba(212,168,67,0.05);
        }
        
        /* ===== TELA FINAL ===== */
        .final-container {
            max-width: 900px;
            width: 100%;
            text-align: center;
        }
        
        .mensagem-final {
            color: #d4a843;
            font-size: 1.3rem;
            font-weight: 300;
            font-family: 'Georgia', serif;
            margin: 30px 0;
            letter-spacing: 2px;
        }
        
        .btn-reiniciar {
            display: inline-block;
            padding: 14px 40px;
            background: transparent;
            color: #888;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 4px;
            border: 1px solid #333;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Arial', sans-serif;
        }
        
        .btn-reiniciar:hover {
            border-color: #d4a843;
            color: #d4a843;
        }
        
        /* ===== RESPONSIVO ===== */
        @media (max-width: 768px) {
            .titulo-principal {
                font-size: 2.8rem;
            }
            
            .container-escolhas {
                flex-direction: column;
                gap: 12px;
            }
            
            .btn-escolha {
                padding: 14px;
            }
            
            .pergunta-escolha {
                font-size: 1.1rem;
            }
            
            .btn-comecar {
                padding: 14px 40px;
                font-size: 0.9rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE NAVEGAÇÃO ---
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

# --- CONTAINER PRINCIPAL ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# --- PEGAR CENA ATUAL ---
cena_id = st.session_state.cena_atual
cena = get_cena(cena_id)

if cena:
    # ===== TELA INICIAL =====
    if cena["tipo"] == "inicio":
        st.markdown(f"""
        <div class="pagina-inicial">
            <h1 class="titulo-principal">{cena.get("titulo", "História")}</h1>
            <div class="linha-dourada"></div>
            <p class="subtitulo">{cena.get("descricao", "")}</p>
            
            <div class="capa-container">
                <img src="{cena['imagem']}" alt="Capa da história">
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # BOTÃO COMEÇAR USANDO STREAMLIT (funciona 100%)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("▶ COMEÇAR", key="btn_comecar", use_container_width=True):
                ir_para_cena("cena_01")
        
        # Esconder o botão do Streamlit e mostrar um HTML estilizado
        st.markdown("""
        <style>
        /* Esconder o botão original do Streamlit */
        .stButton button {
            display: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # HTML do botão bonito que chama o botão do Streamlit
        components.html("""
        <div style="display:flex; justify-content:center; margin-top:10px;">
            <button class="btn-comecar" onclick="document.querySelector('.stButton button').click();">
                ▶ COMEÇAR
            </button>
        </div>
        """, height=80)
    
    # ===== CENA NORMAL =====
    elif cena["tipo"] == "cena":
        st.markdown('<div class="historia-container">', unsafe_allow_html=True)
        
        # Imagem
        st.markdown(f"""
            <img src="{cena['imagem']}" class="imagem-historia" alt="Página da história">
        """, unsafe_allow_html=True)
        
        # Botão continuar (Streamlit escondido)
        if st.button("", key="btn_continuar", use_container_width=True):
            if "proxima" in cena:
                ir_para_cena(cena["proxima"])
        
        # HTML do botão bonito
        components.html("""
        <div style="display:flex; justify-content:center; margin-top:30px;">
            <button class="btn-continuar" onclick="document.querySelector('.stButton button').click();">
                ▶ CONTINUAR
            </button>
        </div>
        """, height=80)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== CENA DE ESCOLHA =====
    elif cena["tipo"] == "escolha":
        st.markdown('<div class="historia-container">', unsafe_allow_html=True)
        
        # Imagem
        st.markdown(f"""
            <img src="{cena['imagem']}" class="imagem-historia" alt="Página da história">
        """, unsafe_allow_html=True)
        
        # Pergunta
        st.markdown(f"""
            <p class="pergunta-escolha">{cena.get("pergunta", "O que fazer?")}</p>
        """, unsafe_allow_html=True)
        
        # Botões Streamlit escondidos
        opcoes = list(cena["opcoes"].items())
        if len(opcoes) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("", key="escolha_1", use_container_width=True):
                    ir_para_cena(opcoes[0][1])
            with col2:
                if st.button("", key="escolha_2", use_container_width=True):
                    ir_para_cena(opcoes[1][1])
            
            # HTML dos botões bonitos
            components.html(f"""
            <div style="display:flex; gap:20px; justify-content:center; max-width:700px; margin:0 auto;">
                <button class="btn-escolha" onclick="document.querySelectorAll('.stButton button')[0].click();" style="flex:1;">
                    {opcoes[0][0]}
                </button>
                <button class="btn-escolha" onclick="document.querySelectorAll('.stButton button')[1].click();" style="flex:1;">
                    {opcoes[1][0]}
                </button>
            </div>
            """, height=100)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== FINAL =====
    elif cena["tipo"] == "final":
        st.markdown('<div class="final-container">', unsafe_allow_html=True)
        
        # Imagem
        st.markdown(f"""
            <img src="{cena['imagem']}" class="imagem-historia" alt="Final da história">
        """, unsafe_allow_html=True)
        
        # Mensagem
        if "mensagem" in cena:
            st.markdown(f"""
                <p class="mensagem-final">✦ {cena['mensagem']} ✦</p>
            """, unsafe_allow_html=True)
        
        # Botão reiniciar (Streamlit escondido)
        if st.button("", key="btn_reiniciar", use_container_width=True):
            reiniciar_historia()
        
        # HTML do botão bonito
        components.html("""
        <div style="display:flex; justify-content:center; margin-top:10px;">
            <button class="btn-reiniciar" onclick="document.querySelector('.stButton button').click();">
                ↻ RECOMEÇAR
            </button>
        </div>
        """, height=80)
        
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)