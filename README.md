# 🏫 CampusCare — College Complaint Management System

CampusCare is a desktop-based College Complaint Management System developed using **Python, Tkinter, and MySQL**. It provides a centralized platform for students to submit complaints related to college facilities and infrastructure.

The system aims to make complaint submission and management easier, more organized, and transparent.

## ✨ Features

- **Student Login:** Allows students to log in to the application.
- **Complaint Categories:** Organizes complaints into categories such as:
  - Room & Infrastructure
  - Washroom & Hygiene
  - Mess & Food
  - Amenities & Utilities
  - Security & Discipline
- **Complaint Submission:** Students can submit a complaint with a title and description.
- **Photo Attachment:** Supports attaching photos to complaints.
- **Unique Complaint ID:** Generates a unique ID for identifying complaints.
- **Complaint Status:** Stores complaint status, such as Pending.
- **MySQL Database:** Stores student and complaint information.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Tkinter | Desktop graphical user interface |
| MySQL | Database management |
| MySQL Connector/Python | Connecting Python to MySQL |
| Git & GitHub | Version control and source code hosting |

## 📁 Project Structure

```text
CampusCare/
├── main.py
├── database.py
├── CampusCare.sql
├── test_db.py
├── .gitignore
└── README.md
```

- `main.py` — Main application and graphical interface.
- `database.py` — MySQL database connection configuration.
- `CampusCare.sql` — SQL script for database setup.
- `test_db.py` — Database connection testing script.
- `.gitignore` — Specifies files Git should ignore.

## ⚙️ Prerequisites

Before running CampusCare, make sure you have installed:

- Python 3
- MySQL Server
- MySQL Connector for Python
- Visual Studio Code or another Python editor

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/akshitmahajan1507-boop/CampusCare.git
```

### 2. Open the project directory

```bash
cd CampusCare
```

### 3. Install the required Python package

```bash
python -m pip install mysql-connector-python
```

### 4. Set up the MySQL database

1. Start MySQL Server.
2. Open MySQL Workbench.
3. Open the `CampusCare.sql` file.
4. Execute the SQL statements to create the database and required tables.

### 5. Configure the database connection

Open `database.py` and configure the MySQL connection settings to match your local environment.

Make sure the database name, username, password, and host are correct.

**Security note:** Do not publish real database passwords or sensitive credentials in a public repository.

### 6. Run the application

```bash
python main.py
```

The CampusCare desktop application should open if the dependencies and database configuration are correct.

## 🗄️ Database

CampusCare uses MySQL to store student information and complaint records.

The database includes tables for:

- **Students:** Student account information.
- **Complaints:** Complaint details, category, description, photo path, priority, status, and creation timestamp.

Refer to `CampusCare.sql` for the database schema.

## 🔮 Future Enhancements

- Admin dashboard for complaint management.
- Real-time complaint status updates.
- Email or in-app notifications.
- Complaint history for students.
- Search, filtering, and analytics.
- Role-based access control.
- Improved password security.

## 🎯 Project Objective

The main objective of CampusCare is to simplify college complaint management by providing students with a structured way to report problems and helping institutions organize complaint records efficiently.

## 👨‍💻 Author

**Akshit Mahajan**

GitHub: [@akshitmahajan1507-boop](https://github.com/akshitmahajan1507-boop)

## 📄 License

This project was developed for educational purposes. A formal open-source license can be added if the project is intended for public reuse.
