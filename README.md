
```markdown
# Quora Clone 

A **Django-based** web application that replicates core functionalities of Quora — allowing users to ask questions, write answers, explore topics, and Spaces.

---

## 🌟 Features

- 🔐 **User Authentication**
  - Sign Up, Log In, and Log Out
- ❓ **Questions & Answers**
  - Post questions and respond with answers
- 👍 **Like System**
  - Like/unlike answers from the community
- 🏷️ **Topics**
  - Categorize questions and browse by topic
- 🧩 **Spaces**
  - Create and join spaces focused on specific domains
- 🙋‍♂️ **User Profile**
  - View personal questions and answers
- ⚙️ **Admin Panel**
  - Enhanced with [Django Jazzmin](https://github.com/farridav/django-jazzmin) for modern UI and model management

---

## 🚀 Quick Start (Local Development)

### 1. Clone the Repository

```bash
git clone https://github.com/vivek129/quora_clone.git
cd quora_clone
```

### 2. Create Virtual Environment

```bash
python -m venv env
# Windows
.\env\Scripts\activate
# macOS/Linux
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Start the Server

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🔑 Admin Access

- **URL:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Username:** `admin`
- **Password:** `admin`

---

## 👥 Test Users

You can log in with the following test user:

| Username | Password    |
|----------|-------------|
| ravi     | password123 |
| raju     | password123 |
| kiran    | password123 |
| manoj    | password123 |
| Sai      | password123 |

More users were pre-seeded in the database via custom Django management commands.

---

## ☁️ Deployment on AWS

This application is deployed on **AWS EC2**, configured using **Nginx** and **Gunicorn**:

### Nginx
- Reverse proxy setup
- Handles static/media routing
- Defined in: `nginx/nginx.conf`

### Gunicorn
- Python WSGI HTTP Server
- Configured via systemd:
  - `gunicorn/gunicorn.service`
  - `gunicorn/gunicorn.socket`

### Useful Scripts
- Deployment automation in the `/scripts` folder:
  - Dependency setup
  - Nginx/Gunicorn integration
  - Static collection

---

## 📂 Project Structure

```
quora_clone/
├── core/                
├── templates/          
├── static/             
├── quora_clone/ 
├── manage.py
├── requirements.txt
├── nginx/
├── gunicorn/
└── scripts/
```

---


