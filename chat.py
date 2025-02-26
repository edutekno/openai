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
st.title("Aplikasi FAQ dengan GROQ")

# Deskripsi aplikasi
st.write("""
    Selamat datang di aplikasi FAQ berbasis AI! 
    Silakan ajukan pertanyaan Anda, dan AI akan memberikan jawaban terbaik.
""")

# Input pengguna untuk parameter opsional
st.sidebar.header("Pengaturan")
selected_model = st.sidebar.selectbox("Pilih Model", ["gemma2-9b-it", "llama3-70b-8192"])
max_tokens = st.sidebar.slider("Batas Panjang Jawaban (Tokens)", 50, 500, MAX_TOKENS)
temperature = st.sidebar.slider("Tingkat Kreativitas (Temperature)", 0.0, 1.0, TEMPERATURE, 0.1)

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

# Input pertanyaan dari pengguna
user_question = st.text_input("Pertanyaan Anda:", key="input", placeholder="Ketik pertanyaan Anda di sini...")

# Tombol untuk mengirim pertanyaan
if st.button("Kirim"):
    if user_question.strip() == "":
        st.warning("Silakan masukkan pertanyaan terlebih dahulu.")
    else:
        # Tambahkan pertanyaan pengguna ke history
        st.session_state['chat_history'].append({"role": "user", "content": user_question})

        # Batasi history menjadi 20 pesan (FIFO)
        if len(st.session_state['chat_history']) > 20:
            st.session_state['chat_history'].pop(0)

        # Dapatkan jawaban dari AI dengan mengirimkan history sebagai konteks
        with st.spinner("Memproses jawaban..."):
            ai_response = get_ai_response(st.session_state['chat_history'], selected_model, max_tokens, temperature)

        # Tambahkan jawaban AI ke history
        st.session_state['chat_history'].append({"role": "assistant", "content": ai_response})

        # Tampilkan jawaban AI
        st.success("Jawaban dari AI:")
        st.write(ai_response)

# Tampilkan history percakapan
st.write("### History Percakapan")
for message in st.session_state['chat_history']:
    if message["role"] == "user":
        st.write(f"**Anda:** {message['content']}")
    else:
        st.write(f"**AI:** {message['content']}")
