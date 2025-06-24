import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
from dotenv import load_dotenv

# Load credentials from secret.env
load_dotenv("secret.env")

# -------------------------
# 1. Configurations
# -------------------------

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

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

SESSIONS = {}

# -------------------------
# 2. Login Function
# -------------------------

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
                print(f"✅ Logged in to {site_name}.")
                SESSIONS[site_name] = session
            else:
                print(f"❌ Login failed for {site_name}.")
        except Exception as e:
            print(f"❌ ERROR logging in to {site_name}: {e}")

# -------------------------
# 3. Site-Specific Parsers
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

# Link parsers to their websites
PARSERS = {
    "Website A": parse_website_a,
    "Website B": parse_website_b,
    "Website C": parse_website_c
}

# -------------------------
# 4. Universal Scraper
# -------------------------

def search_on_site(part_number, site_name, search_url_template):
    session = SESSIONS.get(site_name)
    if not session:
        print(f"⚠️ No session for {site_name}. Skipping.")
        return None

    url = search_url_template.format(part_number)
    try:
        res = session.get(url)
        if res.status_code != 200:
            print(f"❌ {site_name} - Failed to fetch page for {part_number}")
            return None

        parser = PARSERS.get(site_name)
        if parser:
            return parser(res.text, part_number, res.url)
        else:
            print(f"⚠️ No parser defined for {site_name}.")
            return None

    except Exception as e:
        print(f"⚠️ Error scraping {site_name} for {part_number}: {e}")
        return None

# -------------------------
# 5. Process CSV
# -------------------------

def process_all_parts(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    all_results = []

    for part in df["Part Number"]:
        print(f"\n🔍 Searching for: {part}")
        site_results = []

        for site_name, search_url in SEARCH_URLS.items():
            result = search_on_site(part, site_name, search_url)
            if result:
                site_results.append(result)
            time.sleep(random.uniform(1.5, 3.5))

        if site_results:
            best = min(site_results, key=lambda x: x['Price'])
            all_results.append(best)
        else:
            print(f"❌ No results for {part}")

    if all_results:
        pd.DataFrame(all_results).to_csv(output_csv, index=False)
        print(f"\n✅ Results saved to: {output_csv}")
    else:
        print("\n⚠️ No data to save.")

# -------------------------
# 6. Main
# -------------------------

if __name__ == "__main__":
    print("🔐 Logging in...")
    login_all_sites()
    print("\n📦 Processing parts...")
    process_all_parts("input_parts.csv", "pnpilot_results.csv")
