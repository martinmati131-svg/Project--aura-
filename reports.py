import pandas as pd
from fpdf import FPDF
from flask import Flask
from flask_mail import Mail, Message
from datetime import datetime
import os

app = Flask(__name__)

# --- EMAIL CONFIG (Use Environment Variables for 2026 Security) ---
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.getenv("EMAIL_USER"),
    MAIL_PASSWORD=os.getenv("EMAIL_PASS")
)
mail = Mail(app)

def create_pdf_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Aura Intelligence: Weekly Sentinel Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Generated: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align='C')
    
    # Load Data
    if os.path.exists("aura_compliance_audit.csv"):
        df = pd.read_csv("aura_compliance_audit.csv")
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Total Compliance Events: {len(df)}", ln=True)
        # Add table or summary logic here
    
    report_name = f"Aura_Report_{datetime.now().strftime('%Y_%W')}.pdf"
    pdf.output(report_name)
    return report_name

def send_email(report_path):
    with app.app_context():
        msg = Message(
            subject=f"Aura Weekly Intelligence - {datetime.now().strftime('%b %d, 2026')}",
            sender=app.config['MAIL_USERNAME'],
            recipients=["your-email@example.com"]
        )
        msg.body = "Please find the attached weekly Sentinel report for Aura Intelligence."
        with open(report_path, "rb") as fp:
            msg.attach(report_path, "application/pdf", fp.read())
        mail.send(msg)

if __name__ == "__main__":
    path = create_pdf_report()
    send_email(path)
    print(f"📧 Weekly Report Dispatched: {path}")
