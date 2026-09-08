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

# CSS para layout de QUADRINHO
def aplicar_css():
    st.markdown("""
        <style>
        /* RESET COMPLETO */
        .stApp {
            background: #1a1a1a !important;
        }
        
        .main > div {
            padding: 0 !important;
            max-width: 100% !important;
        }
        
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        
        /* Esconder TODOS os elementos do Streamlit */
        #MainMenu {display: none !important;}
        footer {display: none !important;}
        header {display: none !important;}
        .stDeployButton {display: none !important;}
        .stAlert {display: none !important;}
        
        /* Container principal - fundo preto */
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
            text-shadow: 0 0 60px rgba(255,215,0,0.2);
        }
        
        .subtitulo {
            font-size: 1.2rem;
            color: #888;
            font-family: 'Arial', sans-serif;
            margin-bottom: 30px;
            letter-spacing: 6px;
            text-transform: uppercase;
        }
        
        .linha-dourada {
            width: 80px;
            height: 2px;
            background: #d4a843;
            margin: 20px auto;
        }
        
        /* Imagem da capa */
        .capa-container {
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 30px 80px rgba(0,0,0,0.9), 0 0 60px rgba(212,168,67,0.1);
            margin: 20px 0 30px 0;
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
            font-size: 1.2rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 4px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            font-family: 'Arial', sans-serif;
        }
        
        .btn-comecar:hover {
            background: #e8c86a;
            transform: scale(1.02);
            box-shadow: 0 10px 40px rgba(212,168,67,0.4);
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
            margin: 30px auto 0 auto;
            padding: 16px;
            background: transparent;
            color: #d4a843;
            font-size: 1rem;
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
            font-size: 1.6rem;
            font-weight: 300;
            text-align: center;
            margin: 30px 0;
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
            font-size: 1rem;
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
            font-size: 1.4rem;
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
            font-size: 0.9rem;
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
                font-size: 1.2rem;
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
            
            <button class="btn-comecar" onclick="window.location.href='?comecar=true'">▶ COMEÇAR</button>
        </div>
        """, unsafe_allow_html=True)
        
        # Botão começar (Streamlit)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("", key="btn_comecar", use_container_width=True, type="primary"):
                ir_para_cena("cena_01")
        
        # Esconder o botão do Streamlit (vamos mostrar só o HTML)
        st.markdown("""
        <style>
        .stButton button {
            display: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # JavaScript para o botão HTML
        st.markdown("""
        <script>
        document.querySelector('.btn-comecar').addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = window.location.href.split('?')[0] + '?comecar=true';
        });
        </script>
        """, unsafe_allow_html=True)
        
        # Detectar clique no botão HTML
        import urllib.parse
        query_params = st.query_params
        if query_params.get("comecar") == "true":
            ir_para_cena("cena_01")
    
    # ===== CENA NORMAL =====
    elif cena["tipo"] == "cena":
        st.markdown('<div class="historia-container">', unsafe_allow_html=True)
        
        # Imagem
        st.markdown(f"""
            <img src="{cena['imagem']}" class="imagem-historia" alt="Página da história">
        """, unsafe_allow_html=True)
        
        # Botão continuar (HTML)
        st.markdown("""
            <button class="btn-continuar" id="btn-continuar">▶ CONTINUAR</button>
        """, unsafe_allow_html=True)
        
        # Botão Streamlit escondido
        if st.button("", key="btn_continuar", use_container_width=True):
            if "proxima" in cena:
                ir_para_cena(cena["proxima"])
        
        st.markdown("""
        <style>
        .stButton button {display: none !important;}
        </style>
        <script>
        document.getElementById('btn-continuar').addEventListener('click', function() {
            document.querySelector('.stButton button').click();
        });
        </script>
        """, unsafe_allow_html=True)
        
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
        
        # Botões de escolha (HTML)
        opcoes = list(cena["opcoes"].items())
        if len(opcoes) >= 2:
            st.markdown(f"""
            <div class="container-escolhas">
                <button class="btn-escolha" id="escolha_1">{opcoes[0][0]}</button>
                <button class="btn-escolha" id="escolha_2">{opcoes[1][0]}</button>
            </div>
            """, unsafe_allow_html=True)
            
            # Botões Streamlit escondidos
            col1, col2 = st.columns(2)
            with col1:
                if st.button("", key="escolha_1", use_container_width=True):
                    ir_para_cena(opcoes[0][1])
            with col2:
                if st.button("", key="escolha_2", use_container_width=True):
                    ir_para_cena(opcoes[1][1])
            
            st.markdown("""
            <style>
            .stButton button {display: none !important;}
            </style>
            <script>
            document.getElementById('escolha_1').addEventListener('click', function() {
                document.querySelectorAll('.stButton button')[0].click();
            });
            document.getElementById('escolha_2').addEventListener('click', function() {
                document.querySelectorAll('.stButton button')[1].click();
            });
            </script>
            """, unsafe_allow_html=True)
        
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
        
        # Botão reiniciar
        st.markdown("""
            <button class="btn-reiniciar" id="btn-reiniciar">↻ RECOMEÇAR</button>
        """, unsafe_allow_html=True)
        
        if st.button("", key="btn_reiniciar", use_container_width=True):
            reiniciar_historia()
        
        st.markdown("""
        <style>
        .stButton button {display: none !important;}
        </style>
        <script>
        document.getElementById('btn-reiniciar').addEventListener('click', function() {
            document.querySelector('.stButton button').click();
        });
        </script>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)