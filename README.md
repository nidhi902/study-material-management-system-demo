# Study Material Sharing Portal
> A Django-based web portal for students and teachers to share study materials.

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Screenshots](#screenshots)
- [Live Demo](#live-demo)
- [Future Features](#future-features)
- [Note](#note)

## Description
A portal where students and teachers can register. Teachers require an access code. Students can register without access code. Teachers can upload study materials. Students can view/download. Email verification is implemented.

## Features
- Email verification system (console backend in public demo)
- Role-based access: Teachers vs Students
- Upload/download study materials
- Material management by subjects
- Authentication (login/logout)
- Future: Categorization of materials like assignments, notes, etc.

## Tech Stack
- Python 3.x
- Django 4.x
- SQLite (for demo)
- HTML / CSS / Bootstrap

## Installation
1. Clone the repo  
2. Create virtual environment  
3. Install requirements  
4. Run the project with `python manage.py runserver`

## Screenshots
![Teacher Registration](screenshots/teacher_register.png)
![Student Registration](screenshots/student_register.png)
![Email Verification](screenshots/email_console.png)
![Teacher Upload](screenshots/upload_page.png)
![Student View/Download](screenshots/student_view.png)

## Live Demo
[Check the live project](https://your-render-link.com)](https://study-material-sharing-portal-1.onrender.com)

## Future Features
- Categorization of study materials: assignments, notes, study guides
- Advanced search and filter
- Teacher-student analytics for downloads/views

## Note
- Public repo uses **console email backend**, real emails only in private repo/live deployment
- Static files, media, and SQLite database are ignored in public repo
