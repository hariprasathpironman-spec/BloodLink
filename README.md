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
<div align="center">
  Made with ❤️ to save lives
  <br/>
  <strong>BloodLink — Every second counts.</strong>
</div>
