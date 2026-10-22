# SkillBridge: Career Skill Mapping & Learning Progress Tracker

[![Course](https://img.shields.io/badge/Course-Web%20Technology%20(COPCC503)-indigo.svg)](#)
[![Framework](https://img.shields.io/badge/Framework-Django%206.1-green.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](#)
[![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20MySQL-orange.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](#)

> **Course:** Web Technology (COPCC503), Third Year Computer Engineering (TE)  
> **Institute:** AISSMS Institute of Information Technology (IOIT), Pune  
> **Developer:** Dev-43 / Devesh Dolas  

---

## 🌟 Overview

**SkillBridge** is a modern, responsive web portal engineered to bridge the gap between academic engineering coursework and industry-grade job competency requirements.

Students can benchmark their self-assessed technical proficiencies against prerequisite roles (such as Full Stack Developer, Data Analyst, or Android Engineer), receive instant gap analysis (Strong, Weak, Missing), visualize readiness using Chart.js, track remedial progress using curated learning resources, and export their reports as structured XML and JSON feeds.

---

## 🚀 Key Features

- **🔐 Robust Authentication:** Secure session-based registration, login, logout, and profile management with Django authentication and CSRF protection.
- **🎯 Career Role Catalog:** Explore industry career tracks with prerequisite benchmarks on a 1–5 scale.
- **📝 Interactive Self-Assessment:** Rate skills with live-updating sliders, dynamic DOM row addition/removal, and client/server validation.
- **📊 Real-time Skill Gap Analysis:** Deterministic scoring algorithm with zero-reload status filtering and inline level simulation.
- **📈 Interactive Chart.js Visualizations:** Grouped bar chart comparing Required Benchmark vs Current Proficiency.
- **📚 Curated Learning Roadmap:** Targeted study resources (Articles, Books, Courses, Videos) with persistent progress notes and status tracking.
- **📥 XML Export (Unit III):** Download structured, well-formed XML skill reports.
- **🔗 JSON Web Services (Unit IV):** RESTful JSON endpoints for skill catalogs and gap analytics.
- **⚙️ Django Admin Panel:** Full management of roles, skills, role requirements (inlines), and learning resources.
- **🔄 Dual Database Support:** Zero-config SQLite for local development and MySQL support via PyMySQL.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.10+, Django (MVT Pattern) |
| **Frontend** | Semantic HTML5, Vanilla CSS3 (Custom Design System), JavaScript (DOM API) |
| **Data Visualization** | Chart.js (CDN + local offline fallback bundle) |
| **Database** | SQLite (development) & MySQL (production demo) |
| **Data Exchange** | XML (ElementTree), JSON REST endpoints |
| **Version Control** | Git & GitHub |

---

## ⚡ Quick Start Guide

### 1. Clone the Repository
```bash
git clone git@github.com:Dev-43/WT_Mini_Project.git
cd WT_Mini_Project
```

### 2. Activate Virtual Environment
**Windows (PowerShell):**
```powershell
.\venv\Scripts\activate
```
*(Or create a new environment: `python -m venv venv` followed by `pip install -r requirements.txt`)*

### 3. Run Migrations & Seed Sample Data
```bash
python manage.py migrate
python manage.py seed_data
```

### 4. Start the Development Server
```bash
python manage.py runserver
```
Open your browser and navigate to:
- **Web Portal:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Admin Panel:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🔑 Pre-Configured Demo Accounts

| Role | Username | Password | Purpose |
|---|---|---|---|
| **Administrator** | `admin` | `admin123` | Django Admin panel access to manage roles & catalog |
| **Student (Demo)** | `teststudent` | `password123` | Pre-configured student account with active assessments |

*(You can also register a new student account at `/register/`)*

---

## 🧪 Running Automated Tests

SkillBridge includes an automated test suite verifying all 12 items in the testing checklist:
```bash
python manage.py test
```
**Expected Output:**
```
Ran 11 tests in 27.5s
OK
```

---

## 🌐 Application Routes & Endpoints

| Route | Access | Description |
|---|---|---|
| `/` | Public | Landing page with hero section and feature cards |
| `/roles/` | Public | Explore engineering career tracks |
| `/roles/<id>/` | Public | Role competency benchmarks |
| `/register/` | Public | Student account registration |
| `/login/` | Public | Session sign-in |
| `/logout/` | Logged in | Sign out |
| `/dashboard/` | Logged in | Student readiness score and Chart.js visualization |
| `/assessment/` | Logged in | 0–5 proficiency rating with DOM dynamic rows |
| `/result/` | Logged in | Gap matrix with live filters and inline simulation |
| `/tracker/` | Logged in | Remedial study plan and persistent notes |
| `/profile/` | Logged in | Edit academic year, college, and target role |
| `/export/xml/` | Logged in | Download XML skill mapping report |
| `/api/skills/` | Logged in | JSON API returning skills catalog |
| `/api/result/` | Logged in | JSON API returning gap calculations |
| `/admin/` | Admin only | Django administration panel |

---

## 🗄️ Switching to MySQL

To run on MySQL Server:
1. Ensure MySQL Server is running on port 3306.
2. Create the database: `CREATE DATABASE skillbridge_db CHARACTER SET utf8mb4;`
3. Set the environment variable:
   ```powershell
   $env:USE_MYSQL = "True"
   $env:MYSQL_PASSWORD = "your_mysql_root_password"
   ```
4. Run migrations and load fixture data:
   ```bash
   python manage.py migrate
   python manage.py loaddata data.json
   ```

---

## 📖 Project Documentation & Viva Guide

Comprehensive documentation, Entity-Relationship (ER) diagram, Use Case diagram, Data Flow Diagrams (DFD Levels 0 & 1), Flowchart, and Viva Voce questions & answers are available in:
- [`docs/PROJECT_REPORT.md`](docs/PROJECT_REPORT.md)
- [`SKILLBRIDGE_BUILD.md`](SKILLBRIDGE_BUILD.md)

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
