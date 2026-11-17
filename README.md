# 🎓 Recruitment & Placement Management System (RPMS)

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.x-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

---

## 📋 Abstract

The **Recruitment & Placement Management System (RPMS)** is a Python + MySQL desktop application designed to automate and streamline the end-to-end recruitment and placement activities of students/candidates in a training institute. It manages the full lifecycle — from candidate registration and job posting through eligibility screening, interview scheduling, offer management, and final placement confirmation — via a structured console interface and an HTML UI prototype.

---

## 🛠️ Tech Stack

| Layer       | Technology                     |
|-------------|--------------------------------|
| Language    | Python 3.10+                   |
| Database    | MySQL 8.x                      |
| DB Driver   | mysql-connector-python ≥ 9.0   |
| UI Prototype| HTML5 / CSS3 (static, browser) |
| Architecture| Layered OOP (Main→Service→DAO) |

---

## ✨ Features — 9 Modules

| # | Module                | Description                                                        |
|---|-----------------------|--------------------------------------------------------------------|
| 1 | **Candidate Mgmt**    | Register, search, update, deactivate candidates with validations   |
| 2 | **Company Mgmt**      | Manage recruiting companies and their status                       |
| 3 | **Job Mgmt**          | Post jobs with eligibility criteria, close jobs                    |
| 4 | **Applications**      | Apply to jobs with automated full eligibility check                |
| 5 | **Eligibility Engine**| Validates %, passing year, backlogs, deadline, duplicate checks    |
| 6 | **Interview Mgmt**    | Schedule rounds (Aptitude/Technical/HR), record feedback & ratings |
| 7 | **Offer Mgmt**        | Issue offer letters, track acceptance/rejection/expiry             |
| 8 | **Placement Mgmt**    | Confirm joining, mark candidates as PLACED                         |
| 9 | **Reports**           | 6 built-in analytical reports with aggregations                    |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                    main.py (Entry)                   │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│              rpms/app/main.py (Console Menu)         │
│    Menus: Candidates | Companies | Jobs | Apps …     │
└──────┬──────────┬──────────┬──────────┬─────────────┘
       │          │          │          │
┌──────▼──┐ ┌────▼────┐ ┌───▼────┐ ┌───▼──────────┐
│Candidate│ │ Company │ │  Job   │ │  Application │  … (Service Layer)
│ Service │ │ Service │ │Service │ │   Service    │
└──────┬──┘ └────┬────┘ └───┬────┘ └───┬──────────┘
       │          │          │          │
┌──────▼──┐ ┌────▼────┐ ┌───▼────┐ ┌───▼──────────┐
│Candidate│ │ Company │ │  Job   │ │  Application │  … (DAO Layer)
│   DAO   │ │   DAO   │ │  DAO   │ │     DAO      │
└──────┬──┘ └────┬────┘ └───┬────┘ └───┬──────────┘
       │          │          │          │
┌──────▼──────────▼──────────▼──────────▼──────────┐
│                    MySQL 8.x                       │
│          Database: recruitment_portal              │
└───────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
RPMS_Project/
├── main.py                            ← Entry point
├── requirements.txt                   ← Dependencies
├── README.md                          ← This file
├── .gitignore
│
├── rpms/
│   ├── __init__.py
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py                    ← Console menu controller
│   ├── model/
│   │   ├── __init__.py
│   │   ├── candidate.py
│   │   ├── company.py
│   │   ├── job.py
│   │   ├── application.py
│   │   ├── interview.py
│   │   ├── offer.py
│   │   └── placement.py
│   ├── dao/
│   │   ├── __init__.py
│   │   ├── candidate_dao.py
│   │   ├── company_dao.py
│   │   ├── job_dao.py
│   │   ├── application_dao.py
│   │   ├── interview_dao.py
│   │   ├── offer_dao.py
│   │   └── placement_dao.py
│   ├── service/
│   │   ├── __init__.py
│   │   ├── candidate_service.py
│   │   ├── company_service.py
│   │   ├── job_service.py
│   │   ├── application_service.py
│   │   ├── eligibility_service.py
│   │   ├── interview_service.py
│   │   ├── offer_service.py
│   │   ├── placement_service.py
│   │   ├── report_service.py
│   │   └── activity_log_service.py
│   ├── exception/
│   │   ├── __init__.py
│   │   └── exceptions.py
│   └── util/
│       ├── __init__.py
│       ├── db_connection.py           ← ⚠️ Update DB credentials here
│       └── validation.py
│
├── sql/
│   └── rpms_full_setup.sql            ← Full DB schema + seed data
│
├── docs/
│   ├── test_cases.md
│   └── er_diagram.md
│
└── ui/                                ← Static HTML prototype
    ├── css/
    │   └── styles.css
    ├── login.html                     ← Start here
    ├── dashboard.html
    ├── candidates.html
    ├── candidate-detail.html
    ├── add-candidate.html
    ├── companies.html
    ├── jobs.html
    ├── add-job.html
    ├── applications.html
    ├── interviews.html
    ├── placement-process.html
    └── reports.html
```

---

## ⚙️ Prerequisites

| Requirement               | Version     |
|---------------------------|-------------|
| Python                    | 3.10+       |
| MySQL Server              | 8.x         |
| mysql-connector-python    | ≥ 9.0       |
| pip                       | Latest      |

---

## 🚀 Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/RPMS_Project.git
cd RPMS_Project
```

### 2. Create & Activate Virtual Environment

```bash
# Windows
py -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. MySQL Database Setup

```sql
-- In MySQL Workbench or CLI:
CREATE DATABASE recruitment_portal;
```

Then run the full schema + seed script:

```bash
mysql -u root -p recruitment_portal < sql/rpms_full_setup.sql
```

### 5. Configure Database Credentials

Open `rpms/util/db_connection.py` and update:

```python
HOST     = "localhost"
PORT     = 3306
USER     = "root"        # ← your MySQL username
PASSWORD = "root"        # ← your MySQL password
DATABASE = "recruitment_portal"
```

### 6. Run the Application

```bash
python main.py
```

---

## 🖥️ Console Menu

```
==========================================
   RECRUITMENT & PLACEMENT SYSTEM
==========================================
  1. Candidates
  2. Companies
  3. Jobs
  4. Applications
  5. Interviews
  6. Offers
  7. Placements
  8. Reports
  9. Exit
==========================================
Enter your choice:
```

Each option opens a sub-menu with full CRUD operations.  
Example — **Candidates sub-menu:**

```
---------- CANDIDATES ----------
  1. Add New Candidate
  2. View All Candidates
  3. Search Candidate (ID / Name / Technology)
  4. Update Candidate
  5. Deactivate Candidate
  0. Back to Main Menu
---------------------------------
```

---

## 🗄️ Database Schema Overview

| Table                    | Purpose                                            |
|--------------------------|----------------------------------------------------|
| `candidates`             | Candidate profiles with eligibility attributes     |
| `companies`              | Recruiting company master                          |
| `jobs`                   | Job postings with eligibility criteria             |
| `applications`           | Candidate-to-job applications with eligibility log |
| `eligibility_checks`     | Detailed per-rule eligibility evaluation records   |
| `interviews`             | Interview round scheduling                         |
| `interview_feedback`     | Ratings and recommendation per interview round     |
| `offers`                 | Offer letters with package and joining date        |
| `placements`             | Actual joining confirmation records                |
| `workflow_history`       | Full audit trail of application status changes     |
| `technologies`           | Technology master list                             |
| `candidate_technologies` | Many-to-many: candidates ↔ technologies            |
| `job_technologies`       | Many-to-many: jobs ↔ required technologies         |
| `users`                  | System login users (admin / recruiter / viewer)    |
| `activity_log`           | System-level action audit log                      |

---

## 🔄 Application Workflow

```
  APPLIED
     │
     ▼
 SHORTLISTED ─────────────────────────────► REJECTED
     │
     ▼
 INTERVIEW_SCHEDULED
     │
     ▼
 INTERVIEWED ─────────────────────────────► REJECTED
     │
     ▼
 SELECTED
     │
     ▼
 OFFERED ──────────────────────────────────► REJECTED
     │
     ▼
 JOINED
```

> **Invalid status jumps are blocked** — e.g., moving from APPLIED directly to SELECTED raises a workflow exception.

---

## 📊 Available Reports

| # | Report Name                   | Description                                 |
|---|-------------------------------|---------------------------------------------|
| 1 | Candidates by Technology      | Count grouped by primary technology         |
| 2 | Open Jobs                     | All currently OPEN job postings             |
| 3 | Applications by Status        | Count of applications grouped by status     |
| 4 | Company-wise Placements       | Placement count per recruiting company      |
| 5 | Placed Candidates             | Full list of PLACED candidates              |
| 6 | Unplaced Candidates           | Candidates still awaiting placement         |

---

## 🌐 UI Prototype

The `ui/` folder contains a **static HTML prototype** (no backend required).

**How to open:**

1. Navigate to the `ui/` folder
2. Open `login.html` in any modern browser (Chrome / Firefox / Edge)
3. Click through all pages using the navigation bar

**Pages available:**

| File                      | Page Description                   |
|---------------------------|------------------------------------|
| `login.html`              | Login screen                       |
| `dashboard.html`          | KPI summary dashboard              |
| `candidates.html`         | Candidate listing & search         |
| `candidate-detail.html`   | Candidate profile detail view      |
| `add-candidate.html`      | Add / Edit candidate form          |
| `companies.html`          | Company listing                    |
| `jobs.html`               | Job listings with filters          |
| `add-job.html`            | Post new job form                  |
| `applications.html`       | Application pipeline view          |
| `interviews.html`         | Interview schedule & feedback      |
| `placement-process.html`  | Offer + Joining + Placement tabs   |
| `reports.html`            | Analytics and reports dashboard    |

---

## ✅ Student Deliverables Checklist

- [ ] `main.py` — application entry point
- [ ] `rpms/model/` — all 7 model classes
- [ ] `rpms/dao/` — all 7 DAO classes with SQL queries
- [ ] `rpms/service/` — all 10 service classes with business logic
- [ ] `rpms/exception/exceptions.py` — all 8 custom exceptions
- [ ] `rpms/util/db_connection.py` — MySQL connection helper
- [ ] `rpms/util/validation.py` — shared input validators
- [ ] `rpms/app/main.py` — full console menu (all 9 modules)
- [ ] `sql/rpms_full_setup.sql` — complete DB schema + seed data
- [ ] `ui/` — all 12 HTML pages + CSS stylesheet
- [ ] `docs/test_cases.md` — 20+ test cases
- [ ] `docs/er_diagram.md` — ER diagram with all 15 tables
- [ ] `README.md` — this file, complete and accurate
- [ ] `requirements.txt` — all dependencies listed
- [ ] `activity_log.txt` — generated at runtime (auto-created)

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
