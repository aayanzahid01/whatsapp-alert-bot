import gspread
from google.oauth2.service_account import Credentials
from groq import Groq
import requests
import schedule
import time

# ============================================================
# SETTINGS — only change these per client
# ============================================================
PHONE_NUMBER_ID   = ""
ACCESS_TOKEN      = ""
GROQ_API_KEY      = ""
SHEET_NAME        = ""
YOUR_SERVICE      = ""
# ============================================================

# Google Sheets setup
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

def generate_message(name, topic):
    """Use Groq AI to write a personalised WhatsApp message"""
    groq_client = Groq(api_key=GROQ_API_KEY)
    prompt = f"""Write a short, friendly WhatsApp message for a business.
    
Customer name: {name}
Topic: {topic}
Business service: {YOUR_SERVICE}

Rules:
- Maximum 3 sentences
- Casual and warm tone
- No emojis
- End with a call to action
- Do not include subject line or greeting label, just the message text"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def send_whatsapp(phone_number, message):
    """Send a WhatsApp message using Meta Cloud API"""
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {
            "body": message
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def run_campaign():
    """Main function — reads sheet, generates messages, sends via WhatsApp"""
    print("Starting WhatsApp campaign...")
    
    # Open the Google Sheet
    sheet = client.open(SHEET_NAME).sheet1
    rows = sheet.get_all_records()
    
    for row in rows:
        name = row["Name"]
        phone = str(row["Phone"])
        topic = row["Message Topic"]
        
        print(f"Processing {name} ({phone})...")
        
        # Generate AI message
        message = generate_message(name, topic)
        print(f"Message: {message}")
        
        # Send via WhatsApp
        result = send_whatsapp(phone, message)
        print(f"Result: {result}")
        print("---")
        
        # Wait 2 seconds between messages to avoid rate limits
        time.sleep(2)
    
    print("Campaign complete!")

# Run once immediately then every day at 9am
run_campaign()
schedule.every().day.at("09:00").do(run_campaign)

while True:
    schedule.run_pending()
    time.sleep(60)