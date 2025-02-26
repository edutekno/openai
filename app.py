import streamlit as st
import openai

OPENAI_API_KEY=st.secrets["GROQ_API_KEY"]
BASE_URL = "https://api.groq.com/openai/v1"  # Default base URL OpenAI
#BASE_URL="https://openrouter.ai/api/v1"
MODEL = "gemma2-9b-it"  # Model default
MAX_TOKENS = 150  # Batas panjang jawaban
TEMPERATURE = 0.7  # Tingkat kreativitas (0.0 - 1.0)

# Konfigurasi OpenAI
openai.api_key = OPENAI_API_KEY
openai.api_base = BASE_URL

# Judul aplikasi
st.title("Aplikasi FAQ dengan AI")

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

# Input pertanyaan dari pengguna
user_question = st.text_input("Pertanyaan Anda:")

# Fungsi untuk mendapatkan jawaban dari OpenAI
def get_ai_response(question, model, max_tokens, temperature):
    try:
        if model.startswith("gpt"):
            # Untuk model GPT (chat-based models)
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": question}],
                max_tokens=max_tokens,
                temperature=temperature,
                n=1,
                stop=None
            )
            return response.choices[0].message["content"].strip()
        else:
            # Untuk model non-chat (seperti text-davinci-003)
            response = openai.Completion.create(
                engine=model,
                prompt=question,
                max_tokens=max_tokens,
                temperature=temperature,
                n=1,
                stop=None
            )
            return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Tombol untuk mengirim pertanyaan
if st.button("Kirim"):
    if user_question.strip() == "":
        st.warning("Silakan masukkan pertanyaan terlebih dahulu.")
    else:
        with st.spinner("Memproses jawaban..."):
            ai_response = get_ai_response(user_question, selected_model, max_tokens, temperature)
        st.success("Jawaban dari AI:")
        st.write(ai_response)
