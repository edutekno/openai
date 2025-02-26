import streamlit as st
import openai

# Konfigurasi API
OPENAI_API_KEY = st.secrets["GROQ_API_KEY"]
BASE_URL = "https://api.groq.com/openai/v1/chat/completions"  # Default base URL OpenAI
CHAT_COMPLETIONS_URL = "https://api.groq.com/openai/v1"  # 
MODEL = "gemma2-9b-it"  # Model default
MAX_TOKENS = 150  # Batas panjang jawaban
TEMPERATURE = 0.7  # Tingkat kreativitas (0.0 - 1.0)

# Konfigurasi OpenAI
openai.api_key = OPENAI_API_KEY
openai.api_base = BASE_URL

# Judul aplikasi
st.title("Aplikasi Chatbot dengan GROQ")

# Deskripsi aplikasi
st.write("""
    Selamat datang di aplikasi chatbot berbasis AI! 
    Silakan ajukan pertanyaan Anda, dan AI akan memberikan jawaban terbaik.
""")

# Input pengguna untuk parameter opsional
#st.sidebar.header("Pengaturan")
selected_model = st.sidebar.selectbox("Pilih Model", ["gemma2-9b-it", "llama3-70b-8192"])
max_tokens = st.sidebar.slider("Batas Panjang Jawaban (Tokens)", 50, 500, MAX_TOKENS)
temperature = st.sidebar.slider("Tingkat Kreativitas (Temperature)", 0.0, 1.0, TEMPERATURE, 0.1)
max_history = st.sidebar.slider("Jumlah Pesan dalam Konteks", 1, 50, 20)  # Batasan pesan dalam prompt

# Inisialisasi session state untuk menyimpan history percakapan
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Fungsi untuk mendapatkan jawaban dari OpenAI
def get_ai_response(messages, model, max_tokens, temperature):
    try:
        response = openai.ChatCompletion.create(
            api_base=CHAT_COMPLETIONS_URL,  # Gunakan base URL khusus untuk chat
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
st.write("### Percakapan")
for message in st.session_state['chat_history']:
    if message["role"] == "user":
        # Tampilkan pesan pengguna dengan background biru
        st.markdown(
            f'<div style="background-color: #e6f3ff; padding: 10px; border-radius: 10px; margin: 5px 0;">'
            f'<strong>Anda:</strong> {message["content"]}'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        # Tampilkan pesan AI dengan background abu-abu
        st.markdown(
            f'<div style="background-color: #f0f0f0; padding: 10px; border-radius: 10px; margin: 5px 0;">'
            f'<strong>AI:</strong> {message["content"]}'
            f'</div>',
            unsafe_allow_html=True
        )

# CSS untuk membuat input dan tombol tetap di bagian bawah
st.markdown(
    """
    <style>
    .fixed-bottom {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: white;
        padding: 10px;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
        z-index: 1000;
    }
    .stButton button {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# JavaScript untuk menangani event tombol Enter
st.markdown(
    """
    <script>
    function handleEnter(event) {
        if (event.key === "Enter") {
            document.querySelector("button[title='Kirim']").click();
        }
    }
    document.addEventListener("keydown", handleEnter);
    </script>
    """,
    unsafe_allow_html=True
)

# Kotak input dan tombol kirim di bagian bawah layar
with st.container():
    st.markdown('<div class="fixed-bottom">', unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])  # Membagi layout menjadi 2 kolom
    with col1:
        user_question = st.text_input("Pertanyaan Anda:", key="input", placeholder="Ketik pertanyaan Anda di sini...", label_visibility="collapsed")
    with col2:
        if st.button("Kirim"):
            if user_question.strip() != "":
                # Tambahkan pertanyaan pengguna ke history
                st.session_state['chat_history'].append({"role": "user", "content": user_question})

                # Batasi history sesuai dengan max_history (FIFO)
                if len(st.session_state['chat_history']) > max_history * 2:  # *2 karena ada pesan user dan AI
                    st.session_state['chat_history'] = st.session_state['chat_history'][-max_history * 2:]

                # Dapatkan jawaban dari AI dengan mengirimkan history sebagai konteks
                with st.spinner("Memproses jawaban..."):
                    ai_response = get_ai_response(st.session_state['chat_history'], selected_model, max_tokens, temperature)

                # Tambahkan jawaban AI ke history
                st.session_state['chat_history'].append({"role": "assistant", "content": ai_response})

                # Refresh halaman untuk menampilkan pesan terbaru
                st.experimental_rerun()
    st.markdown('</div>', unsafe_allow_html=True)
