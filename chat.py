import streamlit as st
import openai

# Konfigurasi API
OPENAI_API_KEY = st.secrets["GROQ_API_KEY"]
BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
CHAT_COMPLETIONS_URL = "https://api.groq.com/openai/v1"
CHAT_COMPLETIONS_URL = "https://rumahguru.org/api"
MODEL = "gemma2-9b-it"
MAX_TOKENS = 150
TEMPERATURE = 0.7

# Konfigurasi OpenAI
openai.api_key = OPENAI_API_KEY
openai.api_base = BASE_URL

# Judul aplikasi
st.title("GroqChatbots")

# Deskripsi aplikasi
st.write("""
    Aplikasi chatbot berbasis AI!
""")

# Input pengguna untuk parameter opsional
st.sidebar.header("Pengaturan AI")
selected_model = st.sidebar.selectbox("Pilih Model", ["gemma2-9b-it", "llama3-70b-8192"])
max_tokens = st.sidebar.slider("Batas Panjang Jawaban (Tokens)", 50, 500, MAX_TOKENS)
temperature = st.sidebar.slider("Tingkat Kreativitas (Temperature)", 0.0, 1.0, TEMPERATURE, 0.1)
max_history = st.sidebar.slider("Jumlah Pesan dalam Konteks", 1, 50, 20)

# Inisialisasi session state untuk menyimpan history percakapan
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Fungsi untuk mendapatkan jawaban dari OpenAI
def get_ai_response(messages, model, max_tokens, temperature):
    try:
        response = openai.ChatCompletion.create(
            api_base=CHAT_COMPLETIONS_URL,
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            n=1,
            stop=None
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Tampilkan history percakapan
for message in st.session_state['chat_history']:
    if message["role"] == "user":
        st.markdown(
            f'<div style="background-color: #e6f3ff; padding: 10px; border-radius: 10px; margin: 5px 0;">'
            f'<strong>Anda:</strong> {message["content"]}'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div style="background-color: #f0f0f0; padding: 10px; border-radius: 10px; margin: 5px 0;">'
            f'<strong>AI:</strong> {message["content"]}'
            f'</div>',
            unsafe_allow_html=True
        )

# CSS untuk posisi fixed di bawah
st.markdown(
    """
    <style>
    .fixed-input {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: white;
        padding: 10px 20px;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        z-index: 1000;
        display: flex;
        gap: 10px;
        box-sizing: border-box;
    }
    .input-container {
        flex-grow: 1;
    }
    .button-container {
        display: flex;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# JavaScript untuk event Enter
st.markdown(
    """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const input = document.querySelector('input[data-testid="stTextInput"]');
        input.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                document.querySelector('button[kind="primary"]').click();
            }
        });
    });
    </script>
    """,
    unsafe_allow_html=True
)

# Container untuk input dan tombol
st.markdown('<div class="fixed-input">', unsafe_allow_html=True)
col1, col2 = st.columns([4, 1])
with col1:
    user_question = st.text_input("Pertanyaan Anda:", key="user_input", placeholder="Ketik pertanyaan Anda...", label_visibility="collapsed")
with col2:
    send_button = st.button("Kirim", type="primary")

# Logika pengiriman pesan
if send_button and user_question.strip():
    st.session_state['chat_history'].append({"role": "user", "content": user_question})
    if len(st.session_state['chat_history']) > max_history * 2:
        st.session_state['chat_history'] = st.session_state['chat_history'][-max_history * 2:]
    
    with st.spinner("Memproses jawaban..."):
        ai_response = get_ai_response(st.session_state['chat_history'], selected_model, max_tokens, temperature)
    
    st.session_state['chat_history'].append({"role": "assistant", "content": ai_response})
    st.experimental_rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Tambahkan padding di bawah konten utama agar tidak tertutup input
st.markdown('<div style="padding-bottom: 80px;"></div>', unsafe_allow_html=True)
