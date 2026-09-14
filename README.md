# AdosX Engineering - Data Reconciliation Engine

## Setup Instructions

**Prerequisites:** Python 3.10+ and Node.js v18+.

1. **Clone and setup the backend:**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # (On MacOS/Linux: source venv/bin/activate)
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py import_data
   python manage.py runserver
