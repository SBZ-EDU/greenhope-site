# send_outreach.py -- free Gmail outreach sender (dry-run by default)
# Setup: Google Account > Security > 2-Step Verification ON > App passwords > create one.
# Usage: 1) make leads.csv with columns: name,email,org,tpl
#        2) python3 send_outreach.py            (dry run - prints only)
#        3) python3 send_outreach.py --send     (real sending, max 40/day)
import csv, os, smtplib, sys, time, random
from email.message import EmailMessage
from getpass import getpass

TEMPLATES = {
 "job_en": {"sub": "Application: climate-tech developer (live demos inside)",
  "body": "Dear {name},\nI'm Soheil Sabzevari, a climate-tech developer in Istanbul (GreenHope / ForestAI / CityAir - live demos + pitch decks ready).\nMay I send my CV for a role or project collaboration at {org}?\nBest regards,\nSoheil | WhatsApp +1 208 503 3653"},
 "job_tr": {"sub": "Is basvurusu: iklim teknolojileri gelistirici",
  "body": "Merhaba {name},\nBen Soheil Sabzevari, Istanbul'da iklim teknolojileri gelistiricisiyim (GreenHope / ForestAI / CityAir - canli demo ve sunum hazir).\n{org} bunyesinde bir rol veya proje is birligi icin CV'mi gonderebilir miyim?\nSaygilar, Soheil | WhatsApp +1 208 503 3653"},
 "pilot_en": {"sub": "Pilot proposal: satellite methane screening (GreenHope)",
  "body": "Dear {name},\nI'm Soheil Sabzevari (GreenHope). We screen landfill methane hotspots with satellites + ground sensors (XPRIZE Mission Methane track).\nCan we set up a 15-min call about a pilot with {org}?\nDeck on request. Best, Soheil"},
}

def load(p):
    rows = []
    with open(p, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("email"):
                rows.append(r)
    return rows

live = "--send" in sys.argv
rows = load("leads.csv")
user = os.environ.get("GMAIL_USER") or input("Gmail: ")
srv = None
if live:
    key = os.environ.get("GMAIL_APPKEY") or getpass("App password: ")
    srv = smtplib.SMTP("smtp.gmail.com", 587)
    srv.starttls(); srv.login(user, key)
sent = 0
for r in rows:
    if sent >= 40:
        print("daily cap reached"); break
    t = TEMPLATES.get(r.get("tpl", "job_en"), TEMPLATES["job_en"])
    msg = EmailMessage()
    msg["From"] = user; msg["To"] = r["email"]
    msg["Subject"] = t["sub"].format(**r)
    msg.set_content(t["body"].format(**r))
    if live:
        srv.send_message(msg); sent += 1
        print("sent", r["email"])
        time.sleep(random.randint(20, 60))
    else:
        print("--- DRY RUN to", r["email"], "---")
        print(msg["Subject"])
if live and srv:
    srv.quit()
