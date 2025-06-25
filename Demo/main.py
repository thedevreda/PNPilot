import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
from dotenv import load_dotenv

load_dotenv()

# Load input part numbers (limit for testing)
input_df = pd.read_csv(r"C:\Users\The Dev Reda\Desktop\Code\PNPilot\Demo\input_parts.csv")
part_numbers = input_df["Part Number"].astype(str).tolist()[:30]  # Test only 30 parts

# Track already processed
if os.path.exists(r"C:\Users\The Dev Reda\Desktop\Code\PNPilot\Demo\processed.txt"):
    with open(r"C:\Users\The Dev Reda\Desktop\Code\PNPilot\Demo\processed.txt", "r") as f:
        processed = set(line.strip() for line in f)
else:
    processed = set()

# User-Agent pool
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/88.0.4324.96 Safari/537.36"
]

headers = lambda: {"User-Agent": random.choice(user_agents)}

# Append result to CSV
def save_result(data):
    df = pd.DataFrame([data])
    df.to_csv(r"C:\Users\The Dev Reda\Desktop\Code\PNPilot\Demo\pnpilot_results.csv", mode="a", header=not os.path.exists(r"C:\Users\The Dev Reda\Desktop\Code\PNPilot\Demo\pnpilot_results.csv"), index=False)

# Append failed parts
def save_failed(part_number):
    with open(r"C:\Users\The Dev Reda\Desktop\Code\PNPilot\Demo\failed.txt", "a") as f:
        f.write(part_number + "\n")

# Save processed
def mark_processed(part_number):
    with open(r"C:\Users\The Dev Reda\Desktop\Code\PNPilot\Demo\processed.txt", "a") as f:
        f.write(part_number + "\n")

# DEMO scraping logic (replace with real one)
def scrape_demo(part_number, session):
    try:
        url = f"https://httpbin.org/get?part={part_number}"  # test endpoint that returns JSON
        res = session.get(url, headers=headers(), timeout=10)

        if "captcha" in res.text.lower() or "are you human" in res.text.lower():
            print(f"🚨 CAPTCHA detected for {part_number}")
            save_failed(part_number)
            return

        data = res.json()

        save_result({
            "Part Number": part_number,
            "Price": "$123.00",
            "Link": data.get("url", url),
            "Supplier": "DemoSupplier"
        })
        mark_processed(part_number)
    except Exception as e:
        print(f"❌ Failed {part_number}: {e}")
        save_failed(part_number)

# Run demo scraping
session = requests.Session()

for part_number in part_numbers:
    if part_number in processed:
        continue

    scrape_demo(part_number, session)
    time.sleep(random.uniform(2, 4))
