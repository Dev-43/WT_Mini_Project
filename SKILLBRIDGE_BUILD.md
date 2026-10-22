# SkillBridge: Build Plan

**Title:** SkillBridge: A Web Portal for Career Skill Mapping and Learning Progress Tracking
**Course:** Web Technology (COPCC503), Third Year Computer Engineering, AISSMS IOIT
**Type:** Solo mini project

> This file is a plan, not code. Follow it yourself, or give it to an AI assistant to build from. Every decision below is fixed so nothing has to be guessed.

---

## 1. Stack (locked)

| Layer | Choice |
|---|---|
| Backend | Python + Django (MVT) |
| Frontend | HTML5, CSS, JavaScript, DOM |
| Database | SQLite during development, MySQL for the final demo |
| Auth | Django built-in authentication (sessions, CSRF) |
| Admin | Django admin |
| Chart | One JS chart library loaded via CDN (Chart.js) |
| Data exchange | XML export of the skill report, JSON endpoint for skill data |

Do not use React, Vue, Angular, or any separate frontend framework. Django templates render all pages.

---

## 1A. Setup (do this before build step 1)

Commands below are for Windows (Command Prompt or PowerShell). Mac and Linux differences are noted.

### A. Software to install

| Tool | Why | Check it works |
|---|---|---|
| Python 3.10 or newer (python.org). On Windows, tick "Add Python to PATH" in the installer | Runs Django | `python --version` |
| pip (comes with Python) | Installs packages | `pip --version` |
| Git (git-scm.com) | Version control | `git --version` |
| VS Code (code.visualstudio.com) | Editor | Opens normally |
| MySQL Server and MySQL Workbench (dev.mysql.com), needed only from build step 13 | Final demo database | Workbench connects to localhost |
| A browser with developer tools (Chrome or Firefox) | Testing JS and DOM | Press F12 |

On Mac or Linux, use `python3` and `pip3` in place of `python` and `pip`.

**Recommended VS Code extensions:** Python, Django (templates support), and Live Server is not needed because Django serves the pages.

### B. Project folder and virtual environment

1. Create a folder named `skillbridge` somewhere simple (for example `Documents`).
2. Open a terminal inside it (in VS Code: Terminal, New Terminal).
3. Create the virtual environment: `python -m venv venv`
4. Activate it:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
   - You should see `(venv)` at the start of the terminal line. Activate it every time you open a new terminal.
5. If PowerShell blocks activation, run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then try again.

### C. Install packages

1. With `(venv)` active: `pip install django`
2. Check: `python -m django --version`
3. Save the package list: `pip freeze > requirements.txt`
4. Install MySQL packages later, at build step 13 (see section F).

### D. Create the Django project and app

1. Create the project in the current folder: `django-admin startproject skillbridge .`
2. Create the app: `python manage.py startapp core`
3. Open `skillbridge/settings.py` and make these changes:
   - Add `core` to the installed apps list.
   - In the templates setting, add your top-level `templates` folder to the directories list so `master.html` is found.
   - Set the static files settings so the `static` folders are found.
   - Set the login URL, the redirect after login, and the redirect after logout to your pages.
   - Set the time zone to `Asia/Kolkata`.
4. Create the folders from section 8: `templates/` at the top level, and `core/templates/core/`, `core/static/core/css/`, `core/static/core/js/`, `core/static/core/img/`.

### E. First run and admin account

1. Create the database tables Django needs: `python manage.py migrate`
2. Create your admin login: `python manage.py createsuperuser` (enter username, email, password)
3. Start the server: `python manage.py runserver`
4. Open `http://127.0.0.1:8000/` for the site and `http://127.0.0.1:8000/admin/` for the admin panel.
5. Stop the server with `Ctrl + C`.

After you write or change models, always run both: `python manage.py makemigrations` then `python manage.py migrate`.

### F. Switch to MySQL (build step 13)

1. Install MySQL Server and Workbench. Remember the root password you set.
2. In Workbench, create an empty database named `skillbridge_db` (character set utf8mb4).
3. Install a connector package in the venv. Use `pip install mysqlclient`. If it fails on Windows with a build error, use `pip install pymysql` instead, and add the small PyMySQL setup line your Django version needs in the project's `__init__.py` (look up "PyMySQL Django install_as_MySQLdb").
4. In `settings.py`, change the database setting from SQLite to MySQL: engine `django.db.backends.mysql`, database name `skillbridge_db`, your MySQL user, password, host `localhost`, and port `3306`.
5. Run `python manage.py migrate` to create the tables in MySQL.
6. Run `python manage.py createsuperuser` again (the new database is empty), then re-enter the sample data through admin.
7. Do not commit your database password. Keep it in an environment variable or a local settings file that is listed in `.gitignore`.
8. Optional: before switching, you can copy SQLite data across with `python manage.py dumpdata > data.json` and, after switching, `python manage.py loaddata data.json`.

### G. Git and GitHub

1. In the project folder: `git init`
2. Create a `.gitignore` file that lists: `venv/`, `__pycache__/`, `db.sqlite3`, `*.pyc`, `.env`, and any local settings file with passwords.
3. First commit: `git add .` then `git commit -m "Initial Django setup"`
4. Create an empty repository on GitHub, then connect it and push: `git remote add origin <your-repo-url>`, `git branch -M main`, `git push -u origin main`
5. Commit after every build step with a short message such as "Add models" or "Add assessment page".

### H. JavaScript libraries (no install needed)

- **Chart.js** is loaded with a script tag from a CDN inside `master.html`. Load it before your own JS files.
- For a fully offline demo, download the Chart.js file once and place it in `core/static/core/js/`, then point the script tag at that local file.
- Test JS in the browser console (F12, Console tab). Errors show up there.

### I. Tools for the report

| Need | Free tool |
|---|---|
| ER diagram, use-case diagram, DFD, flowchart | draw.io (diagrams.net) |
| Screenshots | Windows Snipping Tool (Win + Shift + S) |
| Report writing | MS Word or Google Docs |
| Viewing the XML export | Browser or VS Code |
| Checking the JSON endpoint | Browser, or the Thunder Client extension in VS Code |

### J. Daily workflow

1. Open the project folder in VS Code.
2. Open a terminal and activate the venv.
3. Run `python manage.py runserver` and keep it running while you work.
4. After model changes, run makemigrations and migrate.
5. Test in the browser, then commit to Git.

### K. Common problems

| Problem | Fix |
|---|---|
| `python` not recognised | Reinstall Python with "Add to PATH" ticked, or try `py` instead of `python` |
| `No module named django` | The venv is not active, or Django was installed outside it. Activate it and install again |
| Static files (CSS/JS) not loading | Check the static settings, use the static tag in templates, and hard refresh with Ctrl + F5 |
| Template not found | Check the templates directory setting and the folder names |
| `no such table` error | Run makemigrations and migrate |
| CSRF verification failed | Add the CSRF token tag inside every POST form |
| Port already in use | Run on another port: `python manage.py runserver 8001` |
| MySQL access denied | Re-check the user, password, and that the database exists |

---

## 2. Scope

**In scope:** registration and login, role and skill catalog, skill self-assessment, skill mapping (gap) result, learning tracker, dashboard, admin panel, XML export, JSON endpoint.

**Out of scope (future scope in report):** AI recommendations, job-portal integration, automated skill tests, email notifications.

---

## 3. Users

- **Student:** registers, picks a role, rates skills, views result, tracks learning.
- **Admin:** manages roles, skills, required levels, and resources through Django admin.

---

## 4. Database design

| Table | Fields | Notes |
|---|---|---|
| User | Django built-in | username, email, password |
| Profile | user (one-to-one), college, year, target_role (FK to Role, nullable) | Created at registration |
| Role | id, name, description | Example: Full Stack Developer |
| Skill | id, name, category | Example: Python, Programming |
| RoleSkill | role (FK), skill (FK), required_level (1 to 5) | Unique together: role + skill |
| UserSkill | user (FK), skill (FK), current_level (0 to 5), updated_at | Unique together: user + skill |
| Resource | skill (FK), title, link, type (Course / Video / Book / Article) | Added by admin |
| Progress | user (FK), skill (FK), resource (FK, nullable), status, notes, date | Status: Not started / In progress / Done |

**Relationships:** User to UserSkill to Skill, and Role to RoleSkill to Skill.

**Core rule:** gap = required_level minus current_level, for each skill of the student's target role.

---

## 5. Skill mapping logic

For the student's target role, for each required skill:

1. Get required_level from RoleSkill.
2. Get current_level from UserSkill (treat missing as 0).
3. Gap = required minus current (minimum 0).
4. Status:
   - **Strong:** current is greater than or equal to required
   - **Weak:** current is at least 1 but below required
   - **Missing:** current is 0
5. Match percentage = sum of min(current, required) divided by sum of required, times 100.
6. Readiness score on the dashboard = match percentage adjusted upward by completed progress items. Keep it simple: use match percentage, and show learning completion separately.

---

## 6. Pages and URLs

| Page | URL | Access | Purpose |
|---|---|---|---|
| Home | / | Public | Landing page, project intro, login/register buttons |
| Register | /register/ | Public | Create account |
| Login | /login/ | Public | Sign in |
| Logout | /logout/ | Logged in | Sign out |
| Profile | /profile/ | Logged in | Edit college, year |
| Role list | /roles/ | Logged in | Browse roles, choose target role |
| Role detail | /roles/<id>/ | Logged in | Skills and required levels of a role |
| Assessment | /assessment/ | Logged in | Rate skills for the target role |
| Result | /result/ | Logged in | Match percentage and skill-wise status |
| Tracker | /tracker/ | Logged in | Learning status per gap skill |
| Dashboard | /dashboard/ | Logged in | Progress bars, chart, readiness score |
| XML export | /export/xml/ | Logged in | Skill report as XML download |
| JSON API | /api/skills/ and /api/result/ | Logged in | Skill data and result as JSON |
| Admin | /admin/ | Admin only | Manage catalog |

---

## 7. Module specs

### 7.1 Authentication
- Registration form: username, email, password, confirm password, college, year.
- Server-side validation in Django forms. Client-side validation in JS (empty fields, password match, email format).
- Login with session. Logout redirects to home.
- All app pages require login.
- Every form includes the CSRF token.

### 7.2 Role and skill catalog
- Roles and their required skills are entered by admin.
- Students see a card or table list of roles. Choosing one saves it as target_role in Profile.
- Role detail page lists each skill, category, and required level.

### 7.3 Skill assessment
- One page listing all skills of the target role.
- Each skill has a 0 to 5 rating input (select or slider).
- JS: show the selected value live beside the input, block submit if any rating is empty, and let the student add an extra skill row dynamically (dynamic row add/remove using DOM).
- On submit, save or update UserSkill rows.

### 7.4 Skill mapping result
- Shows overall match percentage at the top.
- Table of skills with columns: skill, required, current, gap, status.
- Colour-coded status (green strong, amber weak, red missing).
- JS: filter buttons (All / Missing / Weak / Strong) that show or hide rows without reloading, and a live match percentage update when the student edits a rating inline.

### 7.5 Learning tracker
- Lists only skills with a gap.
- For each, show resources from the Resource table and let the student set status and write notes.
- Status changes save to Progress.
- Show a small per-skill completion state.

### 7.6 Dashboard
- Overall match percentage and learning completion percentage.
- Progress bar per skill.
- One chart (bar or radar) comparing required vs current levels.
- Counts: strong, weak, missing.

### 7.7 XML export and JSON endpoint
- XML export: a downloadable file with student name, target role, match percentage, and each skill with required, current, and status.
- JSON endpoint: returns the same data as JSON for use by the dashboard chart.
- These two cover Units III and IV as add-ons.

### 7.8 Admin panel
- Register Role, Skill, RoleSkill, Resource, Profile, UserSkill, Progress in admin.
- RoleSkill editable inline inside the Role page.
- Search and filter on Skill and Resource.

---

## 8. Project structure (folders only)

```
skillbridge/
  manage.py
  skillbridge/          project settings and root URLs
  core/                 the single app
    models
    forms
    views
    urls
    admin
    templates/core/     all page templates
    static/core/
      css/
      js/
      img/
  templates/            master.html (base layout)
  requirements.txt
  README.md
```

Use one app (`core`) to keep the project small and easy to explain.

---

## 9. Templates

- **master.html** holds the header (logo, navigation), a content block, and a footer. Every other page extends it.
- Use the include tag for the navbar and footer pieces.
- Show different navigation links for logged-in and logged-out users.
- Use template tags: for loops (lists, tables), if conditions (status colours), url tags, static tags, and comments.
- CSS: one main stylesheet, responsive layout with flexbox or grid, a simple consistent colour scheme.

---

## 10. Build order (do these in sequence)

| Step | Task | Done when |
|---|---|---|
| 1 | Follow section 1A (parts A to E): install tools, create virtual environment, install Django, create project and `core` app | Server runs and shows the default page |
| 2 | Create master.html with header and footer, home page, static files set up | Home page shows styled layout |
| 3 | Write all models, run migrations, register in admin | Tables appear in admin |
| 4 | Add sample roles, skills, RoleSkill, resources through admin | At least 3 roles with 8 to 10 skills each |
| 5 | Registration, login, logout, profile | New user can sign up and log in |
| 6 | Role list, role detail, choose target role | Target role saves to profile |
| 7 | Assessment page and saving UserSkill | Ratings persist after reload |
| 8 | Result page with gap logic | Match percentage and statuses are correct |
| 9 | Learning tracker and Progress saving | Status and notes persist |
| 10 | Dashboard with progress bars and chart | Chart shows required vs current |
| 11 | JavaScript pass: validation, dynamic rows, live filters, live percentage | Works without page reload |
| 12 | XML export and JSON endpoint | File downloads and JSON loads |
| 13 | Switch database to MySQL (section 1A, part F), migrate, reload sample data | App works unchanged on MySQL |
| 14 | Responsive CSS pass and cleanup | Works on phone width |
| 15 | Testing checklist (section 12) | All items pass |
| 16 | Screenshots, diagrams, report | See section 13 |

---

## 11. Syllabus mapping (for viva and report)

| Unit | Where it appears |
|---|---|
| I: HTML, CSS | All pages: forms, tables, lists, links, images, CSS cascading, responsive layout |
| II: JavaScript, DOM | Form validation, dynamic skill rows, live filters, live percentage, chart, event handling |
| III: XML | XML export of skill report (add-on) |
| IV: Web Services | JSON endpoint for skill and result data (add-on) |
| V: JDBC | Not used. The Django ORM plays the same role of database connectivity. Be ready to explain this. |
| VI: Django | Project and app structure, MVT, URL dispatcher, static files, templates (tags, variables, loops, comments, include, extends, master.html with header and footer), models, forms, database integration |

| Course outcome | Covered by |
|---|---|
| 503.1 | HTML and CSS pages |
| 503.2 | JavaScript and DOM features |
| 503.5 | Database-backed application with real requirements |
| 503.6 | Django development |

---

## 12. Testing checklist

- Register with valid and invalid data, and with a duplicate username
- Login with wrong password
- Visiting protected pages while logged out redirects to login
- Choosing a role updates the profile
- Rating values outside 0 to 5 are rejected
- Re-submitting the assessment updates, not duplicates, UserSkill rows
- Match percentage is correct for these cases: all ratings 0, all ratings at required level, mixed ratings
- Skills with no rating are treated as 0
- Tracker status and notes persist after reload
- Dashboard chart matches result page numbers
- XML file opens and is well-formed
- JSON endpoint returns data only for the logged-in user
- App works on both SQLite and MySQL
- Layout holds on a narrow phone screen

---

## 13. Report and presentation checklist

**Report sections:** title page, abstract, problem statement, objectives, scope and limitations, technology used, system design, implementation, testing, screenshots, conclusion, future scope, references.

**Diagrams to prepare:**
- ER diagram (the 8 tables in section 4)
- Use-case diagram (Student and Admin)
- DFD level 0 and level 1
- Flowchart of the skill mapping logic (section 5)
- MVT architecture diagram

**Screenshots:** home, register, login, role list, assessment, result, tracker, dashboard, XML output, JSON output, admin panel.

**Viva topics to revise:** MVT, migrations, the ORM, template inheritance (extends and include), URL dispatcher, CSRF token, sessions, difference between GET and POST, how DOM events work in your JS, why Django replaces JDBC here, SQLite versus MySQL.

---

## 14. Sample data to seed

**Roles:** Full Stack Developer, Data Analyst, Android Developer (add more if time allows).

**Skills (examples):** HTML, CSS, JavaScript, Python, Django, SQL, Git, Data Structures, Problem Solving, Communication, Statistics, Excel.

**Required levels:** set between 2 and 5 depending on the role. Add 2 to 3 resources per skill (a course, a video, a book or article).

---

## 15. Rules to keep the project clean

- One app, one master template, one main stylesheet, a few focused JS files.
- Keep business logic (the gap calculation) in one place so it can be reused by the result page, dashboard, XML export, and JSON endpoint.
- Never trust client-side checks alone. Validate on the server too.
- Do not add features outside section 2 until every checklist item passes.
- Commit to Git after each build step.

---

## 16. If time is short (minimum viable version)

Keep: auth, role list, assessment, result page, simple dashboard, admin. Drop: XML export, JSON endpoint, MySQL switch, tracker notes. This still covers Units I, II, and VI.
