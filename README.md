# whatsapp-alert-bot

Reads a contact list from Google Sheets, generates a personalised
WhatsApp message per contact using the Groq API, and delivers each
one via Meta WhatsApp Cloud API — on a daily automated schedule.

Built for businesses that communicate with customers via WhatsApp
and want to automate personalised outreach at scale.

## how it works
Google Sheets → Python → Groq API (LLaMA 3.3) → WhatsApp Cloud API → delivered
1. Authenticates with Google Sheets API via service account
2. Pulls contact list with name, phone, and message context
3. Calls Groq API to generate personalised message per contact
4. Delivers via Meta WhatsApp Cloud API
5. Repeats daily at 09:00 via schedule library

## tech

| layer | tool |
|---|---|
| language | Python 3.12 |
| sheet integration | gspread + google-auth |
| content generation | Groq API — llama-3.3-70b-versatile |
| delivery | Meta WhatsApp Cloud API v18 |
| scheduling | schedule library |

## configuration

```python
PHONE_NUMBER_ID   = ""  # From Meta Developer Portal
ACCESS_TOKEN      = ""  # Meta API access token
GROQ_API_KEY      = ""  # Groq API key
SHEET_NAME        = ""  # Google Sheet name
YOUR_SERVICE      = ""  # Business context for content generation
```

## sheet format

| Name | Phone | Message Topic |
|---|---|---|
| James Miller | 447911123456 | monthly offer |

Phone format: country code + number, no + sign. UK example: `447911123456`

## setup

```bash
git clone https://github.com/aayanzahid01/whatsapp-alert-bot
pip install gspread google-auth groq requests schedule
```

Add `credentials.json`, fill settings block, run:

```bash
python whatsapp_sender.py
```

## notes
- `credentials.json` not included — generate from Google Cloud Console
- Phone numbers in sheet must follow international format without + sign
- Designed for Meta WhatsApp Business API — production deployment requires verified Meta Business account
