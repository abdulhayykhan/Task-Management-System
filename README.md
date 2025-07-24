# 🗂️ Task Management System

A simple, colorful, and responsive web-based task management system built with **Flask**. This app allows users to manage their daily tasks efficiently with an intuitive interface.

🔴 **Live App:** [Click here to use the app](https://task-management-system-ahk.up.railway.app/)  

---

## 🚀 Features

- ✅ **Create New Tasks** using the floating "+" action button.
- 📋 **View Task List** with individual task cards.
- 🔍 **Search Tasks** by name using the search bar.
- 🎯 **Filter by Status** (All, Done, Pending).
- 📅 **Due Date Display** shown clearly on each task.
- 🔄 **Task Completion Progress Bar** with percentage display.
- 📦 **Task Status Indicators** (e.g., "Done" with green check badge).
- ⭐ **Mark as Favorite** to prioritize tasks.
- 📝 **Edit Task** with inline update button.
- ℹ️ **View Task Details** modal or info button.
- 🔄 **Toggle Status** from Done ↔ Not Done.
- 🗑️ **Delete Task** permanently.
- ✨ **Responsive and colorful UI** with animated shadows and gradients.
- 🧪 **Unit tests included** (`test_app.py`) using `unittest`.

---

## 🛠️ Technologies Used

- **Python 3** – Core programming language
- **Flask** – Lightweight web framework
- **Flask RESTful** – For building REST APIs
- **SQLite** – Local SQL database (lightweight and file-based)
- **SQLAlchemy** – ORM for database operations
- **Jinja2** – Templating engine for dynamic HTML rendering
- **HTML5 & CSS3** – Frontend structure and styling
- **Gunicorn** – WSGI server for deploying Flask in production
- **Railway** – Platform-as-a-Service for cloud deployment

---

## 📁 Project Structure

Task-Management-System/
- ├── app.py - Main Flask application
- ├── test_app.py - Unit tests for the app
- ├── requirements.txt - Python dependencies
- ├── Procfile - Deployment entry for Railway
- ├── static/
  - │ └── style.css - Custom CSS styling
- ├── templates/
  - │ ├── index.html - Homepage: task list & filters
  - │ ├── edit.html - Edit task form
  -  │ ├── detail.html - Task detail view
  - │ └── delete_confirm.html - Confirmation before delete
- ├── instance/
  - │ └── tasks.db - SQLite database file
- └── README.md - Project documentation

---

## 🛠 Installation & Setup

### 📌 Requirements

- Python 3.8 or later
- Visual Studio Code or any Python IDE
- Git (optional, for cloning)
- pip (Python package manager)

### 📥 Steps to Run

1. **Clone or download** this repository:
```
git clone https://github.com/abdulhayykhan/Task-Management-System.git
cd Task-Management-System
```

2. **Create and activate a virtual environment** (recommended):
```
python -m venv venv
```
On Windows:
```
venv\Scripts\activate
```

On macOS/Linux:
```
source venv/bin/activate
```

3. **Install dependencies**:
```
pip install -r requirements.txt
```

4. **Run the Flask app**:
```
python app.py
```

5. **Access the app**:
Open your browser and go to:
```
http://127.0.0.1:5000
```

## 🧪 Running Tests
To run unit tests:
```
python test_app.py
```

---

## 📢 LinkedIn & GitHub Showcase

I’ll be posting a video and write-up on my [LinkedIn](https://www.linkedin.com/in/abdul-hayy-khan) profile showcasing this project and experience. Stay tuned!

---

## 🙋‍♂️ Author

**Abdul Hayy Khan**
📫 abdulhayykhan.1@gmail.com

---

## 📌 License

This project is for educational purposes as part of the DeveloperHub Corporation internship program. Feel free to use it for learning and inspiration. Attribution is appreciated.

---
