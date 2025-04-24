# Learning Management System (LMS)

A comprehensive Learning Management System built with Flask and JavaScript, designed to manage academic activities, student progress, and faculty-student interactions.

## Table of Contents
- [Features](#features)
- [Technical Stack](#technical-stack)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Setup and Installation](#setup-and-installation)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [Security Features](#security-features)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)
- [Database Schema and Relationships](#database-schema-and-relationships)

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

## Project Structure

```
├── app.py                 # Main Flask application
├── assets/               # Static assets directory
│   ├── images/          # Image resources
│   ├── icons/           # Icon resources
│   └── fonts/           # Custom fonts
├── credentials.js        # User authentication data
├── attendance_records.json # Attendance data
├── HTML Files:
│   ├── index.html        # Landing page
│   ├── dashboard.html    # Student dashboard
│   ├── faculty-dashboard.html # Faculty dashboard
│   ├── courses.html      # Course listing
│   ├── assignments.html  # Assignment management
│   ├── attendance.html   # Attendance tracking
│   ├── exams.html        # Exam information
│   ├── results.html      # Results display
│   ├── schedule.html     # Class schedule
│   └── social.html       # Social interaction platform
└── CSS Files:
    ├── styles.css        # Main stylesheet
    └── style2.css        # Additional styles
```

## API Documentation

### Authentication

#### Login
```http
POST /api/login
Content-Type: application/json

{
    "username": "student123",
    "password": "password123",
    "role": "student"
}
```

Response:
```json
{
    "status": "success",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
        "id": "STU001",
        "name": "John Doe",
        "role": "student",
        "email": "john.doe@example.com",
        "department": "Computer Science",
        "semester": 3
    }
}
```

#### Password Reset
```http
POST /api/auth/reset-password
Content-Type: application/json

{
    "email": "john.doe@example.com"
}
```

### Dashboard

#### Get Schedule
```http
GET /api/dashboard/schedule
Authorization: Bearer <token>
```

Response:
```json
{
    "schedule": [
        {
            "course": "Mathematics",
            "time": "09:00 AM",
            "room": "Room 101",
            "faculty": "Dr. Smith",
            "duration": "1 hour",
            "type": "Lecture",
            "topic": "Calculus Basics"
        }
    ]
}
```

#### Get Progress
```http
GET /api/dashboard/progress
Authorization: Bearer <token>
```

Response:
```json
{
    "courses": [
        {
            "id": "MATH101",
            "name": "Mathematics",
            "progress": 75,
            "completed_lessons": 15,
            "total_lessons": 20,
            "next_lesson": "Integration"
        }
    ]
}
```

### Attendance

#### Mark Attendance
```http
POST /api/attendance/mark
Authorization: Bearer <token>
Content-Type: application/json

{
    "student_id": "STU001",
    "course_id": "MATH101",
    "status": "present",
    "date": "2024-04-16",
    "time": "09:00 AM",
    "remarks": "On time"
}
```

#### Get Attendance Report
```http
GET /api/attendance/report/STU001
Authorization: Bearer <token>
```

Response:
```json
{
    "student_id": "STU001",
    "name": "John Doe",
    "attendance": {
        "MATH101": {
            "total_classes": 30,
            "present": 25,
            "absent": 5,
            "percentage": 83.33
        }
    }
}
```

### Assignments

#### Create Assignment
```http
POST /api/assignments/create
Authorization: Bearer <token>
Content-Type: application/json

{
    "title": "Math Assignment 1",
    "description": "Complete exercises 1-5",
    "due_date": "2024-04-20",
    "course_id": "MATH101",
    "max_marks": 100,
    "instructions": "Submit handwritten solutions",
    "attachments": ["exercise1.pdf", "exercise2.pdf"]
}
```

#### Submit Assignment
```http
POST /api/assignments/submit
Authorization: Bearer <token>
Content-Type: multipart/form-data

{
    "assignment_id": "ASG001",
    "student_id": "STU001",
    "submission": "assignment1.pdf",
    "comments": "Completed all exercises"
}
```

### Grades

#### Submit Grades
```http
POST /api/grades
Authorization: Bearer <token>
Content-Type: application/json

{
    "student_id": "STU001",
    "course_id": "MATH101",
    "assignment_id": "ASG001",
    "marks": 85,
    "feedback": "Good work, but show more steps",
    "graded_by": "FAC001"
}
```

#### Get Grade Report
```http
GET /api/grades/STU001
Authorization: Bearer <token>
```

Response:
```json
{
    "student_id": "STU001",
    "name": "John Doe",
    "grades": {
        "MATH101": {
            "assignments": [
                {
                    "id": "ASG001",
                    "title": "Math Assignment 1",
                    "marks": 85,
                    "max_marks": 100,
                    "feedback": "Good work"
                }
            ],
            "total_marks": 85,
            "grade": "A"
        }
    }
}
```

### Social Features

#### Create Post
```http
POST /api/social/posts
Authorization: Bearer <token>
Content-Type: application/json

{
    "content": "Need help with calculus assignment",
    "tags": ["math", "assignment"],
    "attachments": ["problem1.jpg"],
    "visibility": "public"
}
```

#### Add Comment
```http
POST /api/social/posts/123/comment
Authorization: Bearer <token>
Content-Type: application/json

{
    "content": "I can help you with that",
    "attachments": ["solution.pdf"]
}
```

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser
- Git
- Node.js (for frontend development)
- Redis (optional, for caching)
- Celery (optional, for task queue)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/lms.git
   cd lms
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install frontend dependencies:
   ```bash
   npm install
   ```

5. Configure the application:
   ```bash
   cp config.example.json config.json
   # Edit config.json with your settings
   ```

6. Initialize the database:
   ```bash
   python init_db.py
   ```

7. Run the application:
   ```bash
   # Development mode
   python app.py
   
   # Production mode
   gunicorn app:app
   ```

8. Access the application:
   - Open browser and navigate to `http://localhost:5000`
   - Default admin credentials:
     - Username: admin
     - Password: admin123

## Configuration

### Environment Variables
```bash
# Application
export FLASK_APP=app.py
export FLASK_ENV=development
export SECRET_KEY=your-secret-key
export DATABASE_URL=sqlite:///lms.db

# Email
export SMTP_SERVER=smtp.example.com
export SMTP_PORT=587
export SMTP_USERNAME=your-email@example.com
export SMTP_PASSWORD=your-password

# Redis (optional)
export REDIS_URL=redis://localhost:6379/0

# Celery (optional)
export CELERY_BROKER_URL=redis://localhost:6379/0
export CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Configuration File (config.json)
```json
{
    "application": {
        "name": "Learning Management System",
        "version": "1.0.0",
        "debug": false,
        "secret_key": "your-secret-key",
        "session_timeout": 3600
    },
    "database": {
        "path": "data/",
        "backup": true,
        "backup_path": "backups/",
        "backup_interval": "daily"
    },
    "security": {
        "password_policy": {
            "min_length": 8,
            "require_special": true,
            "require_numbers": true,
            "require_uppercase": true,
            "max_age_days": 90
        },
        "session": {
            "timeout": 3600,
            "secure": true,
            "http_only": true
        }
    },
    "email": {
        "smtp_server": "smtp.example.com",
        "port": 587,
        "use_tls": true,
        "sender": "noreply@example.com",
        "templates": {
            "welcome": "templates/email/welcome.html",
            "reset_password": "templates/email/reset_password.html"
        }
    },
    "storage": {
        "upload_path": "uploads/",
        "max_file_size": 10485760,
        "allowed_extensions": ["pdf", "doc", "docx", "jpg", "png"]
    },
    "logging": {
        "level": "INFO",
        "file": "logs/app.log",
        "max_size": 10485760,
        "backup_count": 5
    }
}
```

## Usage Guide

### For Students

1. **Accessing Dashboard**
   - Login with student credentials
   - View upcoming classes and assignments
   - Check attendance and grades
   - Access course materials
   - View notifications

2. **Submitting Assignments**
   - Navigate to Assignments section
   - Click "Submit Assignment"
   - Upload files and submit
   - Track submission status
   - View feedback and grades

3. **Viewing Grades**
   - Go to Results section
   - Select course
   - View detailed grade breakdown
   - Download grade reports
   - Track performance trends

4. **Managing Attendance**
   - View attendance records
   - Track attendance percentage
   - Request leave applications
   - View attendance trends
   - Download attendance reports

### For Faculty

1. **Managing Courses**
   - Access Faculty Dashboard
   - Create/Edit course materials
   - Set schedules and deadlines
   - Manage course enrollment
   - Track course completion

2. **Grading Assignments**
   - Open Assignment Management
   - Review submissions
   - Enter grades and feedback
   - Generate grade reports
   - Track submission status

3. **Attendance Management**
   - Use Attendance section
   - Mark attendance for classes
   - Generate attendance reports
   - Manage leave requests
   - Export attendance data

4. **Student Management**
   - View student profiles
   - Track student progress
   - Generate student reports
   - Send notifications
   - Manage student records

## Security Features

### Authentication
- JWT-based authentication
- Password hashing with bcrypt
- Session management
- Role-based access control
- Two-factor authentication (optional)
- Password reset functionality

### Data Protection
- Input validation
- XSS prevention
- CSRF protection
- Secure password storage
- Data encryption at rest
- Secure file uploads

### API Security
- Rate limiting
- Request validation
- Error handling
- Logging and monitoring
- API key authentication
- IP whitelisting

### Additional Security Measures
- Regular security audits
- Automated vulnerability scanning
- Secure headers configuration
- Content Security Policy
- Regular backup procedures
- Disaster recovery plan

## Troubleshooting

### Common Issues

1. **Application Not Starting**
   ```bash
   # Check if port 5000 is in use
   netstat -tuln | grep 5000
   
   # Try different port
   export FLASK_RUN_PORT=5001
   
   # Check for Python version
   python --version
   
   # Verify virtual environment
   which python
   ```

2. **Database Issues**
   - Check file permissions
   - Verify JSON file integrity
   - Ensure proper file paths
   - Check disk space
   - Verify backup status

3. **Authentication Problems**
   - Clear browser cache
   - Check token expiration
   - Verify credentials
   - Check session timeout
   - Verify JWT secret key

4. **File Upload Issues**
   - Check file size limits
   - Verify file extensions
   - Check storage permissions
   - Verify upload path
   - Check disk space

### Error Messages

- **401 Unauthorized**: Check login credentials
- **403 Forbidden**: Verify user permissions
- **404 Not Found**: Check API endpoint
- **500 Server Error**: Check server logs
- **413 Payload Too Large**: Check file size limits
- **429 Too Many Requests**: Check rate limiting

### Performance Issues
- Check server resources
- Monitor database queries
- Verify caching configuration
- Check network connectivity
- Monitor application logs

## FAQ

### General
Q: How do I reset my password?
A: Contact your system administrator for password reset.

Q: Can I access the system offline?
A: No, the system requires an active internet connection.

Q: How do I update my profile?
A: Navigate to Profile section and click Edit.

Q: Can I change my email address?
A: Contact your system administrator for email changes.

### Technical
Q: What browsers are supported?
A: Latest versions of Chrome, Firefox, Safari, and Edge.

Q: How do I backup my data?
A: System automatically creates daily backups in the backup directory.

Q: What file types can I upload?
A: PDF, DOC, DOCX, JPG, PNG (up to 10MB).

Q: How do I report a bug?
A: Use the Feedback section or contact support.

### Security
Q: Is my data secure?
A: Yes, we use industry-standard encryption and security measures.

Q: How often should I change my password?
A: Every 90 days as per security policy.

Q: Can I use the same password for multiple accounts?
A: No, please use unique passwords for security.

Q: What happens if I forget my password?
A: Use the password reset feature or contact support.

## Contributing

### Development Workflow

1. Fork the repository
2. Create feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Make changes and commit:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Create Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use ESLint for JavaScript
- Document all functions and classes
- Write unit tests for new features
- Follow Git commit conventions
- Maintain code documentation

### Testing
- Write unit tests
- Run integration tests
- Perform security testing
- Test cross-browser compatibility
- Verify mobile responsiveness

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses
- Flask: BSD License
- jQuery: MIT License
- Bootstrap: MIT License
- Redis: BSD License
- Celery: BSD License
- bcrypt: ISC License

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

## Data Flow

### Authentication Flow
1. User submits login credentials
2. Backend validates credentials
3. JWT token generated and sent to client
4. Client stores token in localStorage
5. Token included in subsequent API requests

### Dashboard Data Flow
1. User accesses dashboard
2. Frontend requests dashboard data
3. Backend validates token
4. Backend retrieves user-specific data
5. Data sent to frontend
6. Frontend renders dashboard components

### Assignment Submission Flow
1. Student uploads assignment file
2. Frontend sends file to backend
3. Backend validates file and stores it
4. Assignment status updated in database
5. Notification sent to faculty
6. Faculty can view and grade submission

## Implementation Details

### Backend Implementation

#### Database Management
```python
# db_manager.py - Database Operations
class DatabaseManager:
    def __init__(self):
        self.data_path = "data/"
        self.initialize_database()
        
    def initialize_database(self):
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
            self.create_initial_tables()
            
    def create_initial_tables(self):
        initial_data = {
            "users": [],
            "courses": [],
            "assignments": [],
            "attendance": []
        }
        self.save_data("database.json", initial_data)
        
    def get_user(self, user_id):
        data = self.load_data("database.json")
        return next((user for user in data["users"] if user["id"] == user_id), None)
```

#### API Implementation
```python
# api.py - API Endpoints
class API:
    def __init__(self, app):
        self.app = app
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.route('/api/courses', methods=['GET'])
        def get_courses():
            courses = self.db.get_courses()
            return jsonify(courses)
            
        @self.app.route('/api/assignments', methods=['POST'])
        def create_assignment():
            data = request.get_json()
            assignment = self.db.create_assignment(data)
            return jsonify(assignment)
```

### Frontend Implementation

#### Component Structure
```javascript
// components/AssignmentList.js
class AssignmentList {
    constructor(assignments) {
        this.assignments = assignments;
        this.render();
    }
    
    render() {
        const container = document.createElement('div');
        container.className = 'assignment-list';
        
        this.assignments.forEach(assignment => {
            const card = this.createAssignmentCard(assignment);
            container.appendChild(card);
        });
        
        return container;
    }
    
    createAssignmentCard(assignment) {
        const card = document.createElement('div');
        card.className = 'assignment-card';
        card.innerHTML = `
            <h3>${assignment.title}</h3>
            <p>${assignment.description}</p>
            <div class="due-date">Due: ${assignment.due_date}</div>
        `;
        return card;
    }
}
```

#### State Management
```javascript
// state/Store.js
class Store {
    constructor() {
        this.state = {
            user: null,
            courses: [],
            assignments: [],
            attendance: []
        };
        this.listeners = [];
    }
    
    setState(newState) {
        this.state = { ...this.state, ...newState };
        this.notifyListeners();
    }
    
    subscribe(listener) {
        this.listeners.push(listener);
    }
    
    notifyListeners() {
        this.listeners.forEach(listener => listener(this.state));
    }
}
```

## Error Handling

### Backend Error Handling
```python
# error_handler.py
class ErrorHandler:
    @staticmethod
    def handle_error(error):
        if isinstance(error, AuthenticationError):
            return jsonify({"error": "Authentication failed"}), 401
        elif isinstance(error, ValidationError):
            return jsonify({"error": str(error)}), 400
        else:
            return jsonify({"error": "Internal server error"}), 500
```

### Frontend Error Handling
```javascript
// error/ErrorHandler.js
class ErrorHandler {
    static handleError(error) {
        console.error('Error:', error);
        
        if (error.status === 401) {
            this.handleAuthError();
        } else if (error.status === 404) {
            this.handleNotFoundError();
        } else {
            this.handleGenericError(error);
        }
    }
    
    static handleAuthError() {
        localStorage.removeItem('token');
        window.location.href = '/login';
    }
}
```

## Testing

### Backend Testing
```python
# tests/test_api.py
class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        
    def test_login(self):
        response = self.client.post('/api/login', json={
            'username': 'test',
            'password': 'test123'
        })
        self.assertEqual(response.status_code, 200)
        
    def test_get_courses(self):
        response = self.client.get('/api/courses')
        self.assertEqual(response.status_code, 200)
```

### Frontend Testing
```javascript
// tests/Dashboard.test.js
describe('Dashboard', () => {
    beforeEach(() => {
        // Setup test environment
    });
    
    test('renders course list', () => {
        const dashboard = new Dashboard();
        expect(dashboard.courses.length).toBeGreaterThan(0);
    });
    
    test('handles API errors', () => {
        const dashboard = new Dashboard();
        // Test error handling
    });
});
```

## Deployment

### Production Setup
```bash
# Dockerfile
FROM python:3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
```

### Environment Configuration
```bash
# .env
FLASK_ENV=production
SECRET_KEY=your-production-secret
DATABASE_URL=postgresql://user:password@localhost/lms
REDIS_URL=redis://localhost:6379/0
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
| marks         |       | upload_date    |       | message        |
| grade         |       | type           |       | status         |
| feedback      |       | type           |       | created_at     |
| graded_by     |       | type           |       | read_at        |
+---------------+       +----------------+       +----------------+
```

### Schema Definitions

#### User Table
```json
{
    "users": [
        {
            "id": "string",
            "username": "string",
            "password": "string (hashed)",
            "email": "string",
            "role": "enum(student, faculty, admin)",
            "department": "string",
            "semester": "integer",
            "created_at": "datetime",
            "updated_at": "datetime"
        }
    ]
}
```

#### Course Table
```json
{
    "courses": [
        {
            "id": "string",
            "name": "string",
            "code": "string",
            "faculty_id": "string (foreign key)",
            "schedule": {
                "days": ["string"],
                "time": "string",
                "room": "string"
            },
            "credits": "integer",
            "status": "enum(active, inactive)",
            "created_at": "datetime",
            "updated_at": "datetime"
        }
    ]
}
```

#### Assignment Table
```json
{
    "assignments": [
        {
            "id": "string",
            "title": "string",
            "description": "string",
            "course_id": "string (foreign key)",
            "due_date": "datetime",
            "max_marks": "integer",
            "status": "enum(draft, published, closed)",
            "created_at": "datetime",
            "updated_at": "datetime"
        }
    ]
}
```

#### Attendance Table
```json
{
    "attendance": [
        {
            "id": "string",
            "student_id": "string (foreign key)",
            "course_id": "string (foreign key)",
            "date": "date",
            "status": "enum(present, absent, late)",
            "remarks": "string",
            "created_at": "datetime"
        }
    ]
}
```

#### Enrollment Table
```json
{
    "enrollments": [
        {
            "id": "string",
            "student_id": "string (foreign key)",
            "course_id": "string (foreign key)",
            "semester": "string",
            "grade": "string",
            "status": "enum(active, completed, dropped)",
            "enrolled_at": "datetime",
            "completed_at": "datetime"
        }
    ]
}
```

#### Submission Table
```json
{
    "submissions": [
        {
            "id": "string",
            "student_id": "string (foreign key)",
            "assignment_id": "string (foreign key)",
            "submission_date": "datetime",
            "file_path": "string",
            "marks": "integer",
            "feedback": "string",
            "status": "enum(submitted, graded, late)",
            "created_at": "datetime",
            "updated_at": "datetime"
        }
    ]
}
```

#### Grade Table
```json
{
    "grades": [
        {
            "id": "string",
            "student_id": "string (foreign key)",
            "course_id": "string (foreign key)",
            "assignment_id": "string (foreign key)",
            "marks": "integer",
            "grade": "string",
            "feedback": "string",
            "graded_by": "string (foreign key)",
            "graded_at": "datetime"
        }
    ]
}
```

#### Material Table
```json
{
    "materials": [
        {
            "id": "string",
            "course_id": "string (foreign key)",
            "title": "string",
            "description": "string",
            "file_path": "string",
            "upload_date": "datetime",
            "type": "enum(lecture, assignment, reference)",
            "uploaded_by": "string (foreign key)"
        }
    ]
}
```

#### Notification Table
```json
{
    "notifications": [
        {
            "id": "string",
            "user_id": "string (foreign key)",
            "type": "enum(assignment, grade, attendance, general)",
            "message": "string",
            "status": "enum(unread, read)",
            "created_at": "datetime",
            "read_at": "datetime"
        }
    ]
}
```

### Relationships

1. **User Relationships**
   - One-to-Many with Courses (faculty teaches courses)
   - One-to-Many with Enrollments (student enrolls in courses)
   - One-to-Many with Submissions (student submits assignments)
   - One-to-Many with Grades (faculty grades assignments)
   - One-to-Many with Notifications (user receives notifications)

2. **Course Relationships**
   - Many-to-One with User (faculty teaches course)
   - One-to-Many with Enrollments (course has enrollments)
   - One-to-Many with Assignments (course has assignments)
   - One-to-Many with Materials (course has materials)
   - One-to-Many with Attendance (course has attendance records)

3. **Assignment Relationships**
   - Many-to-One with Course (assignment belongs to course)
   - One-to-Many with Submissions (assignment has submissions)
   - One-to-Many with Grades (assignment has grades)

4. **Enrollment Relationships**
   - Many-to-One with User (enrollment belongs to student)
   - Many-to-One with Course (enrollment belongs to course)

5. **Attendance Relationships**
   - Many-to-One with User (attendance record belongs to student)
   - Many-to-One with Course (attendance record belongs to course)

6. **Submission Relationships**
   - Many-to-One with User (submission belongs to student)
   - Many-to-One with Assignment (submission belongs to assignment)

7. **Grade Relationships**
   - Many-to-One with User (grade belongs to student)
   - Many-to-One with Course (grade belongs to course)
   - Many-to-One with Assignment (grade belongs to assignment)
   - Many-to-One with User (grade given by faculty)

8. **Material Relationships**
   - Many-to-One with Course (material belongs to course)
   - Many-to-One with User (material uploaded by faculty)

9. **Notification Relationships**
   - Many-to-One with User (notification belongs to user)

### Indexes

```json
{
    "indexes": {
        "users": [
            {"field": "username", "unique": true},
            {"field": "email", "unique": true},
            {"field": "role"}
        ],
        "courses": [
            {"field": "code", "unique": true},
            {"field": "faculty_id"}
        ],
        "enrollments": [
            {"fields": ["student_id", "course_id", "semester"], "unique": true}
        ],
        "attendance": [
            {"fields": ["student_id", "course_id", "date"], "unique": true}
        ],
        "submissions": [
            {"fields": ["student_id", "assignment_id"], "unique": true}
        ],
        "grades": [
            {"fields": ["student_id", "course_id", "assignment_id"], "unique": true}
        ]
    }
}
```

### Data Validation Rules

1. **User Validation**
   - Username: alphanumeric, 3-20 characters
   - Email: valid email format
   - Password: minimum 8 characters, must contain special characters
   - Role: must be one of (student, faculty, admin)

2. **Course Validation**
   - Code: format: DEPT-XXX (e.g., CS-101)
   - Credits: 1-6
   - Schedule: valid days and time format

3. **Assignment Validation**
   - Due date: must be in future
   - Max marks: positive integer
   - Status: must be one of (draft, published, closed)

4. **Grade Validation**
   - Marks: must be <= max_marks
   - Grade: must be one of (A, B, C, D, F)

5. **Attendance Validation**
   - Status: must be one of (present, absent, late)
   - Date: must be valid date

### Data Integrity Constraints

1. **Foreign Key Constraints**
   - Course faculty_id must exist in users table
   - Enrollment student_id must exist in users table
   - Enrollment course_id must exist in courses table
   - Submission student_id must exist in users table
   - Submission assignment_id must exist in assignments table

2. **Unique Constraints**
   - One student can only submit once per assignment
   - One student can only have one attendance record per course per day
   - One student can only be enrolled once per course per semester

3. **Cascade Rules**
   - When a course is deleted, delete all related assignments
   - When a user is deleted, delete all related submissions
   - When an assignment is deleted, delete all related submissions

[Rest of the documentation remains unchanged...] 