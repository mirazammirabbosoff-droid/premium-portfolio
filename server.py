from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Разрешаем HTML-странице отправлять запросы на этот сервер
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Твои данные от BotFather и userinfobot
TELEGRAM_TOKEN = "8707549015:AAE2vtRc0GB3QV5Tv8qg_ZlSGffTbnD3i3o"
YOUR_CHAT_ID = "5867885595"

@app.post("/send-message")
async def send_to_telegram(name: str = Form(...), telegram: str = Form(...), message: str = Form(...)):
    # Формируем красивый текст сообщения
    text = (
        "🔔 <b>Новая заявка с сайта!</b>\n\n"
        f"👤 <b>Имя:</b> {name}\n"
        f"✈️ <b>Telegram:</b> {telegram}\n"
        f"📝 <b>Задача:</b> {message}"
    )
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": YOUR_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return {"status": "success", "message": "Данные отправлены!"}
        else:
            raise HTTPException(status_code=400, detail="Ошибка Telegram API. Проверь, запущен ли бот.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)