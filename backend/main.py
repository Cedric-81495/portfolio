from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.post("/contact")
async def contact_form(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    try:
        subject = f"New message from {name}"
        body = f"Name: {name}\nEmail: {email}\n\n{message}"

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = os.getenv("MAIL_FROM")
        msg["To"] = os.getenv("MAIL_TO")

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(os.getenv("MAIL_FROM"), os.getenv("MAIL_PASS"))
        server.sendmail(os.getenv("MAIL_FROM"), os.getenv("MAIL_TO"), msg.as_string())
        server.quit()

        return JSONResponse(content={"message": "Message sent!"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
