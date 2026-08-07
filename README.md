# 🩸 BloodLink — Blood Donor & Emergency Network

> **AI-powered platform connecting verified blood donors with hospitals during emergencies. Features OTP email verification, role-based dashboards, and a smart compatibility matching engine built for Tamil Nadu.**

---

![BloodLink Banner](https://img.shields.io/badge/BloodLink-Emergency%20Network-dc2626?style=for-the-badge&logo=heart&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=for-the-badge&logo=typescript)
![Railway](https://img.shields.io/badge/Deployed%20on-Railway-0B0D0E?style=for-the-badge&logo=railway)

---

## 🌟 Features

| Feature | Description |
|---|---|
| 🔐 **OTP Email Verification** | Secure email verification via Brevo SMTP on every registration |
| 🤖 **AI Match Score Engine** | Compatibility score algorithm to find the best blood donors |
| 🏥 **Hospital Dashboard** | Hospitals create emergency requests and view matched donors |
| 💉 **Donor Dashboard** | Donors see live emergency feed and toggle availability |
| 🛡️ **Admin Console** | Admins verify hospitals and monitor security alerts |
| 🔒 **JWT Authentication** | Secure token-based login with protected routes |
| ⚡ **Rate Limiting** | Brute-force protection on all auth endpoints |

---

## 🛠️ Tech Stack

### Frontend
- **React 18** + **TypeScript** + **Vite**
- **TailwindCSS** — Styling
- **Framer Motion** — Animations
- **Lucide React** — Icons
- **React Router** — Navigation

### Backend
- **Python** + **Flask 3.0**
- **Flask-SQLAlchemy** — ORM / Database
- **Flask-JWT-Extended** — Authentication
- **Flask-Mail** — Email via Brevo SMTP
- **Flask-Limiter** — Rate Limiting
- **Flask-Talisman** — Security Headers
- **Gunicorn** — Production Server

### Database
- **SQLite** (development)
- **MySQL** (production via Railway)

### Email
- **Brevo SMTP Relay** (`smtp-relay.brevo.com`)

---

## 🚀 Local Development Setup

### Prerequisites
- Node.js 18+
- Python 3.10+
- A Brevo account (free) for email

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/bloodlink.git
cd bloodlink
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:
```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
MAIL_SERVER=smtp-relay.brevo.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-brevo-smtp-login@smtp-brevo.com
MAIL_PASSWORD=your-brevo-smtp-key
MAIL_DEFAULT_SENDER=your-verified-email@gmail.com
```

Run the backend:
```bash
python run.py
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## 🌐 Deployment (Railway)

### Environment Variables (set in Railway dashboard)

| Variable | Value |
|---|---|
| `MAIL_SERVER` | `smtp-relay.brevo.com` |
| `MAIL_PORT` | `587` |
| `MAIL_USE_TLS` | `True` |
| `MAIL_USERNAME` | `your-brevo-smtp-login@smtp-brevo.com` |
| `MAIL_PASSWORD` | `your-brevo-smtp-key` |
| `MAIL_DEFAULT_SENDER` | `your-verified-email@gmail.com` |
| `SECRET_KEY` | `your-strong-secret` |
| `JWT_SECRET_KEY` | `your-strong-jwt-secret` |
| `DATABASE_URL` | `mysql://...` *(Railway provides this)* |

---

## 👥 User Roles

```
Donor      → Register → Verify OTP → View emergency feed → Accept requests
Hospital   → Register → Verify OTP → Create requests → View AI-matched donors  
Admin      → Pre-seeded → Verify hospitals → Monitor security alerts
```

---

## 📁 Project Structure

```
bloodlink/
├── backend/
│   ├── app/
│   │   ├── models/        # Database models (User, Donor, Hospital...)
│   │   ├── routes/        # API endpoints (auth, donor, hospital, admin...)
│   │   ├── schemas/       # Marshmallow validation schemas
│   │   ├── utils/         # Email, security, matching, audit helpers
│   │   ├── config.py      # App configuration
│   │   ├── extensions.py  # Flask extensions
│   │   └── __init__.py    # App factory
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── pages/         # Auth & Dashboard pages
│   │   ├── components/    # Reusable UI components
│   │   └── App.tsx        # Routes
│   ├── index.html
│   └── package.json
├── Dockerfile             # Multi-stage build (Node + Python)
└── README.md
```

---

## 🔒 Security Features

- ✅ Bcrypt password hashing
- ✅ JWT access & refresh tokens
- ✅ OTP expiry (10 minutes)
- ✅ Rate limiting on all auth routes
- ✅ HTTP security headers via Flask-Talisman
- ✅ CORS protection
- ✅ Audit logging for all critical events

---

## 📧 Email Flow

```
User Registers → OTP Generated → Brevo SMTP sends email → User enters OTP → Account Activated
```
> If email fails (network issue), the OTP is printed to server logs as a fallback.

---

## 📄 License

MIT License — feel free to use and modify.

---

<div align="center">
  Made with ❤️ to save lives
  <br/>
  <strong>BloodLink — Every second counts.</strong>
</div>
