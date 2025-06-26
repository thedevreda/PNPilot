# Project Architecture: PNpilot Scalable MVP

## 🎯 Goal:
A hosted scraping-based MVP that allows users to upload part numbers, scrape multiple vendor websites for prices, and return the cheapest offer, all securely and efficiently.

---

## 🧱 Core Tech Stack (With Prioritization & Focus Areas)

### 1. 🧠 Python (Main Language) — **FOCUS MOST**
- Web scraping: `requests`, `BeautifulSoup`, `lxml`
- Automation: `time`, `random`, `schedule`, `os`
- File handling: `pandas`, `csv`, `dotenv`

✅ **Focus on:**
- Writing reusable scraping functions
- Handling exceptions, CAPTCHA logic
- Login/session handling with cookies and tokens


### 2. 🌍 Flask or FastAPI — **VERY HIGH PRIORITY**
- Converts your bot to a web app/backend
- Exposes API endpoints for uploads, scraping, and downloads

✅ **Focus on:**
- Building secure file upload/download endpoints
- User session management
- API design (POST /scrape, GET /status, etc)


### 3. 📦 Streamlit — **Important for UI MVP**
- Frontend UI for uploading part number lists and viewing results

✅ **Focus on:**
- File uploader (`st.file_uploader()`)
- Data table display and alert banners
- Button-triggered backend interaction


### 4. 🧰 Celery + Redis — **Essential for Scaling Later**
- Manages background tasks (scraping jobs)

✅ **Focus on:**
- Creating asynchronous jobs with retry logic
- Tracking task states (PENDING, SUCCESS, FAILED)
- Integrating Flask + Celery with Redis broker


### 5. 📊 PostgreSQL + SQLAlchemy — **Important for Storage**
- Stores users, job statuses, and results

✅ **Focus on:**
- Creating tables for jobs, users, results
- Writing ORM models and queries
- Using SQLAlchemy to link data to Flask


### 6. 🐳 Docker — **Deployment Critical**
- Containerize app for consistent deployment

✅ **Focus on:**
- Writing `Dockerfile` and `docker-compose.yml`
- Separating services: Flask, Celery, Redis, PostgreSQL


### 7. ☁️ Cloud Hosting — **Deploy MVP**
- Use Render, Railway, or Heroku for simplicity

✅ **Focus on:**
- Deploying multi-service apps (Flask + worker + DB)
- Auto redeployment on code push
- Setting env variables in cloud dashboard


### 8. 🔁 Proxy & CAPTCHA Avoidance — **Optional but Useful**
- Rotating proxies or tools like ScraperAPI

✅ **Focus on:**
- Handling request retries
- Implementing user-agent rotation
- Integrating proxy list fallback


### 9. 🔐 Authentication — **User Access Control**
- Prevent abuse and allow user-specific data

✅ **Focus on:**
- Basic login/signup (Flask-Login or OAuth)
- Secure credential storage with hashed passwords
- Optional: JWT tokens


### 10. 📈 Monitoring & Logging
- Track performance, failures, and system status

✅ **Focus on:**
- Use `logging`, `sentry.io`, or `Flask-Logging`
- Show alerts in UI on failures (e.g. part not found)

---

## 📁 Suggested Folder Structure

```
pnpilot/
├── app.py                  # Flask app
├── streamlit_app.py        # UI frontend
├── bot/
│   ├── scraper.py          # Scraping logic
│   ├── login.py            # Login/session functions
│   ├── parsers.py          # Site-specific HTML parsers
│   ├── tasks.py            # Celery async tasks
├── models/
│   └── database.py         # SQLAlchemy models
├── data/
│   ├── input_parts.csv     # Uploaded files
│   ├── processed.txt       # Track completed parts
│   ├── failed.txt          # Log failed searches
├── .env                    # API keys and credentials
├── Dockerfile              # Docker config
├── docker-compose.yml      # Multi-service app config
├── requirements.txt
└── README.md
```

---

## ✅ Recommendation
You already have a **strong base** with Python, Pandas, SQL. Now focus on:
1. **Flask** — run your scraper as an API.
2. **Streamlit** — give it a clean interface.
3. **Celery + Redis** — handle multiple jobs at once.
4. **Docker** — deploy it all cleanly to a cloud host.

