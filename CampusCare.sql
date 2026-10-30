
-- ==========================================
-- CAMPUSCARE DATABASE
-- ==========================================

CREATE DATABASE IF NOT EXISTS campuscare;

USE campuscare;


-- ==========================================
-- STUDENTS TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ==========================================
-- COMPLAINTS TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS complaints (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    complaint_id VARCHAR(30) UNIQUE,
    student_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    photo_path VARCHAR(500),
    priority VARCHAR(20) NOT NULL DEFAULT 'Medium',
    status VARCHAR(30) NOT NULL DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_complaint_student
        FOREIGN KEY (student_id)
        REFERENCES students(id)
);


-- ==========================================
-- VERIFY DATABASE AND TABLES
-- ==========================================

SHOW TABLES;

DESCRIBE students;

DESCRIBE complaints;


-- ==========================================
-- VIEW STUDENT RECORDS
-- ==========================================

SELECT
    id,
    full_name,
    email,
    password,
    created_at
FROM students;


-- ==========================================
-- VIEW COMPLAINT RECORDS
-- ==========================================

SELECT
    complaint_id,
    student_id,
    title,
    category,
    description,
    priority,
    status,
    created_at
FROM complaints;

SELECT
    complaints.complaint_id,
    students.email,
    complaints.category,
    complaints.title,
    complaints.description
FROM complaints
JOIN students
ON complaints.student_id = students.id
ORDER BY complaints.created_at DESC;

