
import email
import email
import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import secrets
import mysql.connector
from pathlib import Path
import uuid
import shutil
from tkinter import filedialog

from database import get_connection

# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("CampusCare - College Complaint Management")
root.geometry("900x600")
root.minsize(700, 500)
root.configure(bg="#F3F5F9")

ADMIN_EMAIL = "admin@campuscare.com"
ADMIN_PASSWORD = "Admin@123"

# ---------------- STYLES ----------------

style = ttk.Style()
style.configure("TButton", padding=8, font=("Arial", 10))
style.configure("TLabel", font=("Arial", 11))

# ---------------- PAGE CONTAINER ----------------

container = ttk.Frame(root, padding=30)
container.pack(fill="both", expand=True)

def clear_page():
    for widget in container.winfo_children():
        widget.destroy()

def heading(title, subtitle=""):
    ttk.Label(
        container,
        text=title,
        font=("Arial", 24, "bold")
    ).pack(pady=(15, 5))

    if subtitle:
        ttk.Label(
            container,
            text=subtitle
        ).pack(pady=(0, 20))

def hash_password(password):
    salt = secrets.token_hex(16)

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        600000
    ).hex()

    return f"{salt}${hashed}"


def verify_password(password, stored_hash):
    try:
        salt, original_hash = stored_hash.split("$")

        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt),
            600000
        ).hex()

        return secrets.compare_digest(
            new_hash, original_hash
        )

    except (ValueError, TypeError):
        return False
# ---------------- HOME PAGE ----------------

def home_page():
    clear_page()
    heading(
        "CampusCare",
        "College Complaint Management System"
    )

    ttk.Label(
        container,
        text="Please select your login type."
    ).pack(pady=15)

    ttk.Button(
        container,
        text="Student Login",
        command=student_login_page
    ).pack(pady=8)

    ttk.Button(
        container,
        text="Admin Login",
        command=admin_login_page
    ).pack(pady=8)

    ttk.Button(
        container,
        text="Student Registration",
        command=register_page
    ).pack(pady=8)


# ---------------- STUDENT LOGIN ----------------

def student_login_page():
    clear_page()
    heading("Student Login", "Login to your student account")

    ttk.Label(container, text="Email").pack()
    email_entry = ttk.Entry(container, width=35)
    email_entry.pack(pady=5)

    ttk.Label(container, text="Password").pack(pady=(10, 0))
    password_entry = ttk.Entry(container, width=35, show="*")
    password_entry.pack(pady=5)

    def login():
        email = email_entry.get().strip().lower()
        password = password_entry.get()

        if not email or not password:
            messagebox.showerror(
                "Error", "Enter email and password."
            )
            return

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT full_name, password
                FROM students
                WHERE email = %s
                """,
                (email,)
            )

            student = cursor.fetchone()

            if student and password == student[1]:
                messagebox.showinfo(
                    "Success", "Login successful!"
                )
                category_page(email)

            else:
                messagebox.showerror(
                    "Login Failed",
                    "Invalid email or password."
                )

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error", str(error)
            )

        finally:
            if cursor is not None:
                cursor.close()

            if connection is not None and connection.is_connected():
                connection.close()

    ttk.Button(
        container, text="Login", command=login
    ).pack(pady=15)

    ttk.Button(
        container,
        text="Create New Account",
        command=register_page
    ).pack()

    ttk.Button(
        container, text="Back", command=home_page
    ).pack(pady=10)



# ---------------- ADMIN LOGIN ----------------

def admin_login_page():
    clear_page()
    heading("Admin Login", "Authorized administrators only")

    ttk.Label(container, text="Admin Email").pack()
    email_entry = ttk.Entry(container, width=35)
    email_entry.pack(pady=5)

    ttk.Label(container, text="Password").pack(pady=(10, 0))
    password_entry = ttk.Entry(container, width=35, show="*")
    password_entry.pack(pady=5)

    def login():
        email = email_entry.get().strip().lower()
        password = password_entry.get()

        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            messagebox.showinfo("Success", "Admin login successful!")
            admin_dashboard()
        else:
            messagebox.showerror(
                "Login Failed", "Invalid admin credentials."
            )

    ttk.Button(
        container, text="Login", command=login
    ).pack(pady=15)

    ttk.Button(
        container, text="Back", command=home_page
    ).pack()

# ---------------- STUDENT REGISTRATION ----------------


def register_page():
    clear_page()
    heading("Student Registration", "Create your account")

    ttk.Label(container, text="Full Name").pack()
    name_entry = ttk.Entry(container, width=35)
    name_entry.pack(pady=5)

    ttk.Label(container, text="Email").pack(pady=(8, 0))
    email_entry = ttk.Entry(container, width=35)
    email_entry.pack(pady=5)

    ttk.Label(container, text="Password").pack(pady=(8, 0))
    password_entry = ttk.Entry(container, width=35, show="*")
    password_entry.pack(pady=5)

    def register():
        name = name_entry.get().strip()
        email = email_entry.get().strip().lower()
        password = password_entry.get()

        if not name or not email or not password:
            messagebox.showerror(
                "Error", "Please fill in all fields."
            )
            return

        if "@" not in email or "." not in email.split("@")[-1]:
            messagebox.showerror(
                "Error", "Enter a valid email."
            )
            return

        if len(password) < 8:
            messagebox.showerror(
                "Error", "Password must be at least 8 characters."
            )
            return

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            password_hash = password

            cursor.execute(
            """
            INSERT INTO students (full_name, email, password)
            VALUES (%s, %s, %s)
            """,
            (name, email, password)
            )

            connection.commit()

            messagebox.showinfo(
                "Success", "Registration successful!"
            )
            student_login_page()

        except mysql.connector.IntegrityError:
            messagebox.showerror(
                "Error", "This email is already registered."
            )

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Error", str(error)
            )

        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None and connection.is_connected():
                connection.close()

    ttk.Button(
        container, text="Register", command=register
    ).pack(pady=15)

    ttk.Button(
        container, text="Back", command=home_page
    ).pack()




def complaint_form(email, complaint_window, selected_category):
    form_frame = ttk.Frame(complaint_window, padding=20)
    form_frame.pack(fill="both", expand=True)

    # Category-specific heading
    ttk.Label(
        form_frame,
        text=f"Submit a Complaint",
        font=("Arial", 22, "bold")
    ).pack(pady=(5, 5))

    ttk.Label(
        form_frame,
        text=f"Category: {selected_category}",
        font=("Arial", 13, "bold")
    ).pack(pady=(0, 8))

    ttk.Label(
        form_frame,
        text=f"Logged in as: {email}"
    ).pack(pady=(0, 15))

    # Complaint title
    ttk.Label(
        form_frame,
        text="Complaint Title"
    ).pack()

    title_entry = ttk.Entry(form_frame, width=55)
    title_entry.pack(pady=5)

    # Description
    ttk.Label(
        form_frame,
        text="Complaint Description"
    ).pack(pady=(8, 0))

    description_box = tk.Text(
        form_frame,
        width=55,
        height=6,
        wrap="word"
    )
    description_box.pack(pady=5)

    # Optional photo
    selected_photo = {"path": None}

    photo_label = ttk.Label(
        form_frame,
        text="No photo selected"
    )
    photo_label.pack(pady=5)

    def choose_photo():
        path = filedialog.askopenfilename(
            parent=complaint_window,
            title="Select Complaint Photo",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg")
            ]
        )

        if path:
            extension = Path(path).suffix.lower()

            if extension not in (".png", ".jpg", ".jpeg"):
                messagebox.showerror(
                    "Invalid File",
                    "Please select a PNG or JPEG image.",
                    parent=complaint_window
                )
                return

            selected_photo["path"] = path
            photo_label.config(text=Path(path).name)

    ttk.Button(
        form_frame,
        text="Attach Photo (Optional)",
        command=choose_photo
    ).pack(pady=5)

    # Submit complaint
    def submit_complaint():
        title = title_entry.get().strip()
        description = description_box.get(
            "1.0", "end"
        ).strip()

        if not title or not description:
            messagebox.showerror(
                "Missing Information",
                "Please enter the title and description.",
                parent=complaint_window
            )
            return

        if len(title) > 150:
            messagebox.showerror(
                "Invalid Title",
                "Title must not exceed 150 characters.",
                parent=complaint_window
            )
            return

        connection = None
        cursor = None
        saved_photo = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                "SELECT id FROM students WHERE email = %s",
                (email,)
            )
            student = cursor.fetchone()

            if not student:
                messagebox.showerror(
                    "Error",
                    "Student account not found.",
                    parent=complaint_window
                )
                return

            complaint_id = (
                "CC-" + uuid.uuid4().hex[:12].upper()
            )

            photo_path = None
            source = selected_photo["path"]

            if source:
                extension = Path(source).suffix.lower()
                destination = UPLOAD_DIR / (
                    complaint_id + extension
                )

                shutil.copy2(source, destination)
                saved_photo = destination
                photo_path = str(destination)

            cursor.execute(
                """
                INSERT INTO complaints
                (complaint_id, student_id, title, category,
                 description, photo_path)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    complaint_id,
                    student[0],
                    title,
                    selected_category,
                    description,
                    photo_path
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Complaint Submitted",
                f"Complaint registered successfully!\n\n"
                f"Complaint ID: {complaint_id}\n"
                f"Category: {selected_category}\n"
                f"Status: Pending",
                parent=complaint_window
            )

            complaint_window.destroy()

        except Exception as error:
            if connection is not None:
                connection.rollback()

            if saved_photo is not None and saved_photo.exists():
                saved_photo.unlink()

            messagebox.showerror(
                "Submission Failed",
                str(error),
                parent=complaint_window
            )

        finally:
            if cursor is not None:
                cursor.close()

            if connection is not None and connection.is_connected():
                connection.close()

    ttk.Button(
        form_frame,
        text="SUBMIT COMPLAINT",
        command=submit_complaint
    ).pack(pady=12)


# ---------------- COMPLAINT CATEGORY PAGE ----------------

def category_page(email):
    clear_page()

    heading(
        "CampusCare",
        "Select the category of your complaint"
    )

    ttk.Label(
        container,
        text=f"Logged in as: {email}"
    ).pack(pady=(0, 20))

    ttk.Label(
        container,
        text="Complaint Category",
        font=("Arial", 13, "bold")
    ).pack(pady=8)

    category_box = ttk.Combobox(
        container,
        values=[
            "Room & Infrastructure",
            "Washroom & Hygiene",
            "Mess & Food",
            "Amenities & Utilities",
            "Security & Discipline"
        ],
        state="readonly",
        width=35,
        font=("Arial", 12)
    )
    category_box.pack(pady=10)
    category_box.set("Room & Infrastructure")

    def continue_to_form():
        category = category_box.get()

        if not category:
            messagebox.showerror(
                "Error",
                "Please select a complaint category."
            )
            return

        open_complaint_window(email, category)

    ttk.Button(
        container,
        text="Continue to Complaint Form",
        command=continue_to_form
    ).pack(pady=15)

    ttk.Button(
        container,
        text="Logout",
        command=home_page
    ).pack(pady=5)


def open_complaint_window(email, category):
    complaint_window = tk.Toplevel(root)
    complaint_window.title("CampusCare - Complaint Form")
    complaint_window.geometry("600x650")
    complaint_window.minsize(500, 550)

    complaint_form(email, complaint_window, category)

# ---------------- STUDENT DASHBOARD ----------------


def student_dashboard(email):
    clear_page()

    heading(
        "Student Dashboard",
        f"Logged in as {email}"
    )

    ttk.Label(
        container,
        text="Welcome to CampusCare!",
        font=("Arial", 15, "bold")
    ).pack(pady=20)

    ttk.Button(
        container,
        text="Submit a New Complaint",
        command=lambda: category_page(email)
    ).pack(pady=10)

    ttk.Button(
        container,
        text="Logout",
        command=home_page
    ).pack(pady=10)


# ---------------- ADMIN DASHBOARD ----------------

def admin_dashboard():
    clear_page()
    heading("Admin Dashboard", "CampusCare Administration")

    ttk.Label(
        container,
        text="Welcome, Administrator!"
    ).pack(pady=20)

    ttk.Label(
        container,
        text="Complaint management will be added in later steps."
    ).pack(pady=5)

    ttk.Button(
        container,
        text="Logout",
        command=home_page
    ).pack(pady=20)

# ---------------- START APPLICATION ----------------

home_page()
root.mainloop()
