import os
import httpx
from fastapi import FastAPI
import google.generativeai as genai

app = FastAPI()

# Inisialisasi Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

@app.post("/chat")
async def chat(user_text: str):
    try:
        # 1. Dapatkan jawaban teks dari Gemini
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(user_text)
        answer_text = response.text

        # 2. Perintahkan Piper di rumah untuk bersuara
        # Kita gunakan httpx untuk memanggil URL Cloudflare Anda
        tts_url = "https://tts.skendern8n.com/api/tts"
        
        async with httpx.AsyncClient() as client:
            # Mengirim teks ke Piper lokal via Cloudflare Tunnel
            await client.get(tts_url, params={"text": answer_text, "voice": "af_sky"})

        return {
            "gemini_response": answer_text,
            "tts_status": "Sent to Local Piper",
            "target": "tts.skendern8n.com"
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def home():
    return {"status": "Online", "bridge": "Render to IhubLLM"}
