# 💰 Expense Tracker

A secure, full-stack expense tracking application built with Flask and SQLite. Track your daily spending with categories, view spending summaries, and analyze your financial habits.

![Flask](https://img.shields.io/badge/Flask-3.0.3-blue)
![SQLite](https://img.shields.io/badge/SQLite-3-green)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)
![Security](https://img.shields.io/badge/Security-CSRF%20%7C%20XSS%20%7C%20SQLi-red)

## ✨ Features

- ✅ **Add Expenses** - Record spending with amount, category, description, and date
- ✅ **8 Categories** - Food, Transport, Utilities, Entertainment, Health, Shopping, Education, Other
- ✅ **Spending Summary** - Total spent with category breakdown
- ✅ **Monthly Trends** - Visual bar chart of spending over time
- ✅ **Delete Expenses** - Remove entries with confirmation
- ✅ **Fully Responsive** - Works on mobile, tablet, and desktop

## 🔒 Security Features

| Protection | Implementation |
|------------|---------------|
| **CSRF** | Flask-WTF tokens on all forms |
| **XSS** | Input sanitization + template auto-escaping |
| **SQL Injection** | Parameterized queries only |
| **Rate Limiting** | 30 requests/minute for adding expenses |
| **Input Validation** | Amount limits, category whitelist, date validation |
| **Size Limits** | 16MB max request size |

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Git
- GitHub account

### Step 1: Clone the Repository

```bash
git clone https://github.com/Deathfrosthacker/expense-tracker.git
cd expense-tracker
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scriptsctivate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python app.py
```

Open your browser and go to: **http://localhost:5000**

## 📁 Project Structure

```
expense-tracker/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore            # Files to ignore in Git
├── expenses.db           # SQLite database (created on first run)
├── static/
│   ├── css/
│   │   └── style.css     # Application styles
│   └── js/               # JavaScript files (if needed)
└── templates/
    └── index.html        # Main page template
```

## 🛠️ Development Commands

| Command | Description |
|---------|-------------|
| `python app.py` | Run development server |
| `pip list` | List installed packages |
| `pip freeze > requirements.txt` | Update dependencies |

## 🌐 Deployment Options

### Option 1: PythonAnywhere (Free & Easy)

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com) and create a free account
2. Open a **Bash console** and run:
```bash
git clone https://github.com/Deathfrosthacker/expense-tracker.git
cd expense-tracker
mkvirtualenv --python=/usr/bin/python3.10 venv
pip install -r requirements.txt
```
3. Go to **Web** tab → **Add a new web app** → **Manual configuration** → **Python 3.10**
4. Set:
   - **Source code**: `/home/yourusername/expense-tracker`
   - **Working directory**: `/home/yourusername/expense-tracker`
   - **WSGI file**: Edit and replace with:
```python
import sys
path = '/home/yourusername/expense-tracker'
if path not in sys.path:
    sys.path.append(path)
from app import app as application
```
5. Add environment variable in **Web** tab:
   - Name: `SECRET_KEY`
   - Value: `your-random-secret-key-here-change-this`
6. Reload the web app

### Option 2: Render (Free Tier)

1. Push your code to GitHub
2. Go to [render.com](https://render.com) and sign up
3. Click **New +** → **Web Service**
4. Connect your GitHub repository
5. Set:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Add environment variable:
   - Key: `SECRET_KEY`
   - Value: Generate a random string (use: `openssl rand -hex 32`)
7. Click **Create Web Service**

### Option 3: Heroku

1. Install Heroku CLI: [devcenter.heroku.com](https://devcenter.heroku.com/articles/heroku-cli)
2. Login and create app:
```bash
heroku login
heroku create your-expense-tracker
git push heroku main
```
3. Set environment variable:
```bash
heroku config:set SECRET_KEY=$(openssl rand -hex 32)
```

## ⚠️ Important Security Notes

1. **Change SECRET_KEY** before deploying to production:
   ```bash
   # Generate a secure key
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Then set it as environment variable:
   ```bash
   export SECRET_KEY="your-generated-key"
   ```

2. **Never commit** the database file or `.env` file (already in `.gitignore`)

3. **Keep dependencies updated**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main page with all data |
| `/add` | POST | Add new expense |
| `/delete/<id>` | POST | Delete expense by ID |
| `/api/summary` | GET | JSON summary by category |

## 🤝 Contributing

Feel free to fork this project and submit pull requests!

## 📄 License

This project is open source and available under the MIT License.

---

**Made with ❤️ by Deathfrosthacker**
