![logo](Logo.png)

# ✈️ PNpilot - Aircraft Part Number Scraper

PNpilot is a smart scraping bot that takes a list of aircraft part numbers and finds the **cheapest prices** across multiple aviation parts websites. It's designed as a **MVP** with built-in safety, login support, proxy rotation, and a Streamlit UI for simple use.

---

## 📁 Project Structure

```bash
pnpilot/
├── app.py                 # Streamlit web app for uploading, running, and downloading results
├── main.py                # Core scraping bot
├── secret.env             # Login credentials (one per site)
├── proxies.txt            # List of proxies for IP rotation
├── input_parts.csv        # Input from user (auto-generated)
├── pnpilot_results.csv    # Final results (auto-generated)
├── processed.txt          # Tracks already scraped part numbers
├── failed.txt             # Logs part numbers that failed scraping
├── README_PNPilot.md      # This documentation
```

---

## 🧠 How It Works

1. **Upload a CSV** with a column named `Part Number` via the Streamlit UI.
2. The bot searches each part number on 3 different websites.
3. For each part number, it finds the **cheapest offer**, including price, link, and supplier.
4. Saves successful results to `pnpilot_results.csv`, and failed ones to `failed.txt`.
5. Avoids reprocessing already-completed part numbers using `processed.txt`.

---

## 🖥️ Technologies Used

| Category            | Tech                            |
|---------------------|----------------------------------|
| Core Scraper        | `Python` + `requests`, `bs4`    |
| Bot UI              | `Streamlit`                     |
| File Handling       | `pandas`, `dotenv`              |
| Proxy Management    | Manual proxy list (`proxies.txt`) |

---

## 🔐 Authentication
- Each site login is handled via email + password stored in `.env`
- Structure of `secret.env`:

```env
EMAIL_SITE_A=your_email_a
PASSWORD_SITE_A=your_password_a
EMAIL_SITE_B=your_email_b
PASSWORD_SITE_B=your_password_b
EMAIL_SITE_C=your_email_c
PASSWORD_SITE_C=your_password_c
```

---

## 🌐 Proxy Setup
- Proxies are rotated for every request.
- Add one proxy per line in `proxies.txt`:

```txt
http://123.123.123.123:8080
http://234.234.234.234:3128
```

---

## 📥 Failed Scrapes
- Failed part numbers (due to site errors, parsing issues, etc.) are logged in `failed.txt`
- These can be retried in future runs manually or in a retry script

---

## 📤 Resume Support
- All successful part numbers are saved in `processed.txt`
- Script automatically skips part numbers that already exist in this file

---

## ⚠️ Warnings & Best Practices

| Issue                         | Mitigation                                                  |
|------------------------------|--------------------------------------------------------------|
| IP blocks or bans            | Use proxies from `proxies.txt`, limit scraping rate         |
| Server overload              | Set a reasonable batch size (100–300 part numbers)          |
| Data parsing errors          | Customize `parse_site_X` functions per website structure     |
| CSV structure mismatch       | Ensure input CSV has column `Part Number`                   |
| Site layout changes          | Update scraping functions if a site changes its HTML layout |
| Environment variables missing| Check `.env` file before starting                           |

---

## 🚀 Running the App

```bash
streamlit run app.py
```

---

## ✅ Features Recap
- [x] Multiple website login
- [x] Proxy rotation
- [x] Streamlit UI
- [x] Resume/retry via `processed.txt` and `failed.txt`
- [x] Batch control with slider
- [x] Download results and failed parts from the UI

---

## 🛠️ Future Improvements (Optional)
- Retry logic for failed parts
- CAPTCHA detection and bypass (if needed)
- Headless browser support (Selenium or Playwright)
- Deploy on Streamlit Cloud, Render, or Docker

---

## 👨‍💻 Made for developers, data analysts, and aviation supply teams.
Happy scraping! ✈️