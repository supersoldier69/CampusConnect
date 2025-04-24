# Learning Management System (LMS) Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Technical Stack](#technical-stack)
4. [System Architecture](#system-architecture)
5. [Database Schema and Relationships](#database-schema-and-relationships)
6. [API Documentation](#api-documentation)
7. [Setup and Installation](#setup-and-installation)
8. [Configuration](#configuration)
9. [Usage Guide](#usage-guide)
10. [Security Features](#security-features)
11. [Troubleshooting](#troubleshooting)
12. [FAQ](#faq)
13. [Contributing](#contributing)
14. [License](#license)

## Introduction

The Learning Management System (LMS) is a comprehensive web-based platform designed to manage academic activities, student progress, and faculty-student interactions. Built with Flask and JavaScript, it provides a robust and user-friendly interface for educational institutions.

## Features

### Student Features
- **Dashboard**
  - Real-time course progress tracking
  - Upcoming class schedule
  - Assignment deadlines
  - Attendance statistics
  - Grade overview
  - Personalized notifications
  - Quick access to recent activities

- **Attendance**
  - View attendance records
  - Track attendance percentage
  - Receive attendance notifications
  - Request leave applications
  - View attendance trends

- **Assignments**
  - Submit assignments online
  - Track submission status
  - View feedback and grades
  - Download assignment materials
  - Request deadline extensions

- **Exams**
  - View exam schedule
  - Access exam results
  - Download hall tickets
  - View exam guidelines
  - Check exam room allocation

- **Courses**
  - Access course materials
  - View course syllabus
  - Track course progress
  - Download lecture notes
  - Access recorded lectures

- **Social Platform**
  - Interact with peers
  - Share study materials
  - Join study groups
  - Create discussion threads
  - Share announcements

### Faculty Features
- **Student Management**
  - View student profiles
  - Track student progress
  - Manage student records
  - Generate student reports
  - Send notifications to students

- **Course Management**
  - Create and update courses
  - Upload course materials
  - Set course schedules
  - Manage course enrollment
  - Track course completion

- **Assignment Management**
  - Create assignments
  - Grade submissions
  - Provide feedback
  - Set deadlines
  - Track submission status

- **Attendance**
  - Mark attendance
  - Generate reports
  - Track attendance trends
  - Export attendance data
  - Manage leave requests

- **Grade Management**
  - Submit grades
  - Generate grade reports
  - Track student performance
  - Calculate final grades
  - Export grade sheets

- **Analytics**
  - View class performance
  - Generate progress reports
  - Track attendance trends
  - Analyze student performance
  - Generate statistical reports

## Technical Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: JSON-based storage
- **Authentication**: Custom JWT-based system
- **API**: RESTful architecture
- **Caching**: Redis (optional)
- **Task Queue**: Celery (optional)

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Responsive design
- **JavaScript**: Interactive features
- **AJAX**: Asynchronous data loading
- **Bootstrap**: UI components
- **jQuery**: DOM manipulation

### Development Tools
- **Version Control**: Git
- **Code Editor**: VS Code recommended
- **Browser**: Chrome/Firefox for development
- **Testing**: pytest, Jest
- **CI/CD**: GitHub Actions
- **Documentation**: Swagger/OpenAPI

## System Architecture

### Backend Architecture

#### Flask Application Structure
```python
# app.py - Main Application Entry Point
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime, timedelta
import re

app = Flask(__name__)
CORS(app)

# Database Models
class User:
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

class Course:
    def __init__(self, id, name, faculty_id, schedule):
        self.id = id
        self.name = name
        self.faculty_id = faculty_id
        self.schedule = schedule

# Authentication Middleware
def authenticate_token(token):
    try:
        # Verify JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except:
        return None

# API Routes
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    # Authentication logic
    return jsonify({"token": token, "user": user_data})

@app.route('/api/dashboard', methods=['GET'])
@require_auth
def get_dashboard():
    # Dashboard data retrieval
    return jsonify(dashboard_data)
```

#### Data Storage
```python
# data_manager.py - Data Management
class DataManager:
    def __init__(self):
        self.data_path = "data/"
        
    def load_data(self, filename):
        with open(f"{self.data_path}{filename}", 'r') as f:
            return json.load(f)
            
    def save_data(self, filename, data):
        with open(f"{self.data_path}{filename}", 'w') as f:
            json.dump(data, f, indent=4)
```

#### Authentication System
```python
# auth.py - Authentication System
import jwt
from datetime import datetime, timedelta

class AuthManager:
    def __init__(self):
        self.secret_key = "your-secret-key"
        
    def generate_token(self, user_id, role):
        payload = {
            'user_id': user_id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
        
    def verify_token(self, token):
        try:
            return jwt.decode(token, self.secret_key, algorithms=['HS256'])
        except:
            return None
```

### Frontend Architecture

#### HTML Structure
```html
<!-- dashboard.html - Student Dashboard -->
<!DOCTYPE html>
<html>
<head>
    <title>Student Dashboard</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="dashboard-container">
        <header>
            <h1>Student Dashboard</h1>
            <nav>
                <ul>
                    <li><a href="#courses">Courses</a></li>
                    <li><a href="#assignments">Assignments</a></li>
                    <li><a href="#attendance">Attendance</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <section id="courses">
                <!-- Course content -->
            </section>
            <section id="assignments">
                <!-- Assignment content -->
            </section>
        </main>
    </div>
    <script src="dashboard.js"></script>
</body>
</html>
```

#### JavaScript Implementation
```javascript
// dashboard.js - Dashboard Functionality
class Dashboard {
    constructor() {
        this.token = localStorage.getItem('token');
        this.userId = localStorage.getItem('userId');
        this.initializeDashboard();
    }
    
    async initializeDashboard() {
        try {
            const response = await fetch('/api/dashboard', {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });
            const data = await response.json();
            this.renderDashboard(data);
        } catch (error) {
            console.error('Error loading dashboard:', error);
        }
    }
    
    renderDashboard(data) {
        // Render dashboard components
        this.renderCourses(data.courses);
        this.renderAssignments(data.assignments);
        this.renderAttendance(data.attendance);
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new Dashboard();
});
```

#### CSS Styling
```css
/* styles.css - Main Stylesheet */
:root {
    --primary-color: #3498db;
    --secondary-color: #2ecc71;
    --text-color: #333;
}

.dashboard-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
}

nav ul {
    display: flex;
    list-style: none;
    gap: 20px;
}

nav a {
    text-decoration: none;
    color: var(--text-color);
    font-weight: 500;
}

section {
    margin-bottom: 40px;
    padding: 20px;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
```

## Database Schema and Relationships

### Entity Relationship Diagram (ERD)

```
+---------------+       +----------------+       +----------------+
|     User      |       |     Course     |       |   Assignment   |
+---------------+       +----------------+       +----------------+
| id            |<----->| id             |<----->| id             |
| username      |       | name           |       | title          |
| password      |       | code           |       | description    |
| email         |       | faculty_id     |       | course_id      |
| role          |       | schedule       |       | due_date       |
| department    |       | credits        |       | max_marks      |
| semester      |       | status         |       | status         |
+---------------+       +----------------+       +----------------+
       ^                        ^                        ^
       |                        |                        |
       |                        |                        |
+---------------+       +----------------+       +----------------+
|   Attendance  |       |    Enrollment  |       |   Submission   |
+---------------+       +----------------+       +----------------+
| id            |       | id             |       | id             |
| student_id    |       | student_id     |       | student_id     |
| course_id     |       | course_id      |       | assignment_id  |
| date          |       | semester       |       | submission_date|
| status        |       | grade          |       | file_path      |
| remarks       |       | status         |       | marks          |
+---------------+       +----------------+       +----------------+
       ^                        ^                        ^
       |                        |                        |
       |                        |                        |
+---------------+       +----------------+       +----------------+
|     Grade     |       |    Material    |       |   Notification |
+---------------+       +----------------+       +----------------+
| id            |       | id             |       | id             |
| student_id    |       | course_id      |       | title          |
| course_id     |       | description    |       | file_path      |
| assignment_id |       | upload_date    |       | type           |
| marks         |       | type           |       | message        |
| grade         |       | upload_date    |       | status         |
| feedback      |       | upload_date    |       | created_at     |
| read_at       |       | upload_date    |       | read_at        |
+---------------+       +----------------+       +----------------+
```

## API Documentation

[API Documentation section remains the same as in the previous update...]

## Setup and Installation

[Setup and Installation section remains the same as in the previous update...]

## Configuration

[Configuration section remains the same as in the previous update...]

## Usage Guide

[Usage Guide section remains the same as in the previous update...]

## Security Features

[Security Features section remains the same as in the previous update...]

## Troubleshooting

[Troubleshooting section remains the same as in the previous update...]

## FAQ

[FAQ section remains the same as in the previous update...]

## Contributing

[Contributing section remains the same as in the previous update...]

## License

[License section remains the same as in the previous update...] 