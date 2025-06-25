import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
from dotenv import load_dotenv

# -------------------------
# 1. Load Environment and Config
# -------------------------

load_dotenv("secret.env")

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

SEARCH_URLS = {
    "Website A": "https://example.com/search?q={}",
    "Website B": "https://example2.com/products?query={}",
    "Website C": "https://example3.com/find?keyword={}"
}

SESSIONS = {}

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/88.0.4324.96 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148"
]

headers = lambda: {"User-Agent": random.choice(user_agents)}

# -------------------------
# 2. Load Data and Logs
# -------------------------

input_df = pd.read_csv("input_parts.csv")
part_numbers = input_df["Part Number"].astype(str).tolist()

if os.path.exists("processed.txt"):
    with open("processed.txt", "r") as f:
        processed = set(line.strip() for line in f)
else:
    processed = set()

if os.path.exists("proxies.txt"):
    with open("proxies.txt", "r") as f:
        proxies = [line.strip() for line in f if line.strip()]
else:
    proxies = [None]

# -------------------------
# 3. Helper Functions
# -------------------------

def save_result(data):
    df = pd.DataFrame([data])
    df.to_csv("pnpilot_results.csv", mode="a", header=not os.path.exists("pnpilot_results.csv"), index=False)

def save_failed(part_number):
    with open("failed.txt", "a") as f:
        f.write(part_number + "\n")

def mark_processed(part_number):
    with open("processed.txt", "a") as f:
        f.write(part_number + "\n")

# -------------------------
# 4. Login
# -------------------------

def login_all_sites():
    for site_name, creds in CREDENTIALS.items():
        session = requests.Session()
        session.headers.update(headers())
        payload = {
            "email": creds["email"],
            "password": creds["password"]
        }
        try:
            res = session.post(creds["login_url"], data=payload)
            if res.status_code == 200 and "logout" in res.text.lower():
                print(f"✅ Logged in to {site_name}.")
                SESSIONS[site_name] = session
            else:
                print(f"❌ Login failed for {site_name}.")
        except Exception as e:
            print(f"❌ ERROR logging in to {site_name}: {e}")

# -------------------------
# 5. Site-Specific Parsers
# -------------------------

def parse_website_a(html, part_number, url):
    soup = BeautifulSoup(html, "html.parser")
    return {
        "Site": "Website A",
        "Part Number": part_number,
        "Part Name": soup.select_one(".part-name").text.strip(),
        "Price": float(soup.select_one(".price").text.strip().replace("$", "")),
        "Supplier": soup.select_one(".supplier").text.strip(),
        "Link": url
    }

def parse_website_b(html, part_number, url):
    soup = BeautifulSoup(html, "html.parser")
    return {
        "Site": "Website B",
        "Part Number": part_number,
        "Part Name": soup.select_one("h2.product-title").text.strip(),
        "Price": float(soup.select_one("span.product-price").text.strip().replace("$", "")),
        "Supplier": soup.select_one("div.vendor").text.strip(),
        "Link": url
    }

def parse_website_c(html, part_number, url):
    soup = BeautifulSoup(html, "html.parser")
    return {
        "Site": "Website C",
        "Part Number": part_number,
        "Part Name": soup.select_one(".item-name").text.strip(),
        "Price": float(soup.select_one(".item-cost").text.strip().replace("$", "")),
        "Supplier": soup.select_one(".item-supplier").text.strip(),
        "Link": url
    }

PARSERS = {
    "Website A": parse_website_a,
    "Website B": parse_website_b,
    "Website C": parse_website_c
}

# -------------------------
# 6. Scraper
# -------------------------

def search_on_site(part_number, site_name, search_url_template, proxy):
    session = SESSIONS.get(site_name)
    if not session:
        print(f"⚠️ No session for {site_name}. Skipping.")
        return None

    url = search_url_template.format(part_number)
    try:
        res = session.get(url, headers=headers(), proxies={"http": proxy, "https": proxy} if proxy else None, timeout=10)

        if "captcha" in res.text.lower() or "are you human" in res.text.lower():
            print(f"🚨 CAPTCHA for {part_number} on {site_name}")
            return None

        parser = PARSERS.get(site_name)
        if parser:
            return parser(res.text, part_number, res.url)
        else:
            print(f"⚠️ No parser defined for {site_name}.")
            return None

    except Exception as e:
        print(f"❌ Failed {part_number} on {site_name}: {e}")
        return None

# -------------------------
# 7. Main
# -------------------------

if __name__ == "__main__":
    print("🔐 Logging into all sites...")
    login_all_sites()

    print("\n🚀 Starting scraping process...")
    for part_number in part_numbers:
        if part_number in processed:
            continue

        results = []
        proxy = random.choice(proxies)
        for site, search_url in SEARCH_URLS.items():
            result = search_on_site(part_number, site, search_url, proxy)
            if result:
                results.append(result)
            time.sleep(random.uniform(1.5, 3.0))

        if results:
            best = min(results, key=lambda x: x['Price'])
            save_result(best)
        else:
            save_failed(part_number)

        mark_processed(part_number)
        time.sleep(random.uniform(2, 4))

    print("\n✅ Scraping complete.")
