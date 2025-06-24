import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
from dotenv import load_dotenv
# Load credentials from secret.env
load_dotenv("secret.env")
# Store site-specific credentials
CREDENTIALS = {
    "Website A": {
        "login_url": "https://example.com/login",
        "email": os.getenv("EMAIL_SITE_A"),
        "password": os.getenv("PASSWORD_SITE_A")
    },
    "Website B": {
        "login_url": "https://example2.com/login",
        "email": os.getenv("EMAIL_SITE_B"),
        "password": os.getenv("PASSWORD_SITE_B")
    },
    "Website C": {
        "login_url": "https://example3.com/login",
        "email": os.getenv("EMAIL_SITE_C"),
        "password": os.getenv("PASSWORD_SITE_C")
    }
}
# Search URLs per website
SEARCH_URLS = {
    "Website A": "https://example.com/search?q={}",
    "Website B": "https://example2.com/search?q={}",
    "Website C": "https://example3.com/search?q={}"
}
# Headers to look like a real browser
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
# Step 1: Login per site and keep session
SESSIONS = {}
def login_all_sites():
    for site_name, creds in CREDENTIALS.items():
        session = requests.Session()
        session.headers.update(HEADERS)
        payload = {
            "email": creds["email"],
            "password": creds["password"]
        }
        try:
            res = session.post(creds["login_url"], data=payload)
            if res.status_code == 200 and "logout" in res.text.lower():
                print(f"✅ Logged in to {site_name} successfully.")
                SESSIONS[site_name] = session
            else:
                print(f"❌ Login failed for {site_name}.")
        except Exception as e:
            print(f"❌ ERROR logging in to {site_name}: {e}")
# Modifed cuz every website has one unique code
# Step 2: Search part on one site
def search_on_site(part_number, site_name, search_url_template):
    session = SESSIONS.get(site_name)
    if not session:
        print(f"⚠️ No session found for {site_name}. Skipping.")
        return None
    url = search_url_template.format(part_number)
    try:
        res = session.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        # Customize these selectors based on actual site HTML
        part_name = soup.select_one(".part-name").text.strip()
        price = float(soup.select_one(".price").text.strip().replace("$", ""))
        supplier = soup.select_one(".supplier").text.strip()
        return {
            "Site": site_name,
            "Part Number": part_number,
            "Part Name": part_name,
            "Price": price,
            "Supplier": supplier,
            "Link": res.url
        }
    except Exception as e:
        print(f"⚠️ Error on {site_name} for {part_number}: {e}")
        return None
# Step 3: Handle the whole CSV
def process_all_parts(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    all_results = []
    for part in df["Part Number"]:
        print(f"\n🔍 Checking {part}")
        site_results = []
        for site_name, search_url in SEARCH_URLS.items():
            result = search_on_site(part, site_name, search_url)
            if result:
                site_results.append(result)
            time.sleep(random.uniform(1.5, 3.5))  # Avoid IP blocking
        if site_results:
            best = min(site_results, key=lambda x: x['Price'])
            all_results.append(best)
        else:
            print(f"❌ No results found for {part}")
    # Save results
    out_df = pd.DataFrame(all_results)
    out_df.to_csv(output_csv, index=False)
    print(f"\n✅ Done. Results saved in: {output_csv}")
# Final Runner
if __name__ == "__main__":
    print("🔐 Logging in to all websites...")
    login_all_sites()
    print("\n📥 Reading input and processing parts...")
    process_all_parts("input_parts.csv", "pnpilot_results.csv")
