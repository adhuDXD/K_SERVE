<div align="center">
  <h1>🎓 Kserve</h1>
  <p><b>A Comprehensive Educational Management & Attendance Platform</b></p>
</div>

<br />

**Kserve** is a high-performance educational management system tailored for institutions to streamline administrative, departmental, and academic workflows. Designed with distinct role-based permissions (Admin, HOD, and Faculty), Kserve provides modern tools to automate data entry, handle bulk faculty scheduling, and track student attendance in real-time.

## ✨ Key Features

- 🔐 **Role-Based Access Control:** Separate, secure dashboards tailored for Administrators, Heads of Departments (HODs), and Faculty members—navigated through a clean, unified sidebar interface.
- 👨‍🏫 **Bulk Automated Onboarding:** Administrators can instantly onboard massive amounts of faculty data via Excel (`.xlsx`) or `.csv` dataset uploads. The system intelligently auto-generates system credentials securely using logic such as joining dates.
- 📷 **Barcode Attendance Scanning:** A robust, camera-integrated barcode scanning interface that operates in real-time. Capable of adaptive scanning, logging attendance even without pre-generated weekly schedules, and verifying unique student IDs on-the-fly.
- 📊 **Department Analytics & Guides:** HODs and Faculty get access to dedicated spaces for weekly timetable assignment, substitute requests, department-wide announcements, and comprehensive profile views.

## 🛠️ Technology Stack

Built with a fast, modern Python web-stack:

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) for lightning-fast, high-performance API routing.
- **Database:** [SQLAlchemy](https://www.sqlalchemy.org/) (ORM) for secure relational data handling.
- **Frontend / Rendering:** [Jinja2 Templates](https://jinja.palletsprojects.com/) tightly integrated with HTML/CSS.
- **Data Engineering:** Powered by `pandas` and `openpyxl` for high-volume data ingestion.
- **Security:** Hardened by `python-jose` for JWT authentication and `bcrypt` for strict password handling.

## 🚀 Getting Started

### Prerequisites
Make sure you have [Python 3.8+](https://www.python.org/downloads/) installed.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/kserve.git
   cd kserve
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the application:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Open in Browser:**
   Navigate to `http://localhost:8000` to interact with Kserve.
