#SIA (Sistem Informasi Booking Hotel) dengan Flask (micro web framework Python)
---


# Cara Install SIA
---
**Requirement**

1. Flask==0.12

2. Jinja2==2.9.5

3. MySQL-python==1.2.5

4. Werkzeug==0.11.15



# Install Sistem ke localhost
---
**Intall Vitualenv**

`$ virtualenv venv`

`$ source venv/bin/activate`

**Install packages yang dibutuhkan**

`(venv)$ pip install -r requirements.txt`

**Setup**

1. Ubah koneksi database pada file config.json

2. Eksekusi file db.py `python query/db.py`

**Menjalankan Sistem di localhost**

`(venv)$ python manage.py runserver`
