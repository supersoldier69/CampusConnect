from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime, timedelta
import re
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

def convert_js_to_json(js_str):
    # Remove JavaScript comments
    js_str = re.sub(r'//.*?\n|/\*.*?\*/', '', js_str, flags=re.S)
    
    # Remove variable declarations and exports
    js_str = re.sub(r'const\s+\w+\s*=\s*', '', js_str)
    js_str = re.sub(r'if.*module\.exports.*}$', '', js_str, flags=re.S)
    
    # Add quotes to unquoted property names (handles nested objects too)
    js_str = re.sub(r'(\b\w+)(?=\s*:(?!\s*{))', r'"\1"', js_str)
    
    # Replace single quotes with double quotes
    js_str = js_str.replace("'", '"')
    
    # Remove trailing commas
    js_str = re.sub(r',(\s*[}\]])', r'\1', js_str)
    
    # Fix property names that might have spaces
    js_str = re.sub(r'(\w+)\s+(\w+):', r'"\1 \2":', js_str)
    
    # Remove semicolons
    js_str = js_str.replace(';', '')
    
    # Clean up any remaining whitespace and newlines
    js_str = re.sub(r'\s+', ' ', js_str).strip()
    
    # Extract just the object literal part
    match = re.search(r'{.*}', js_str)
    if match:
        js_str = match.group(0)
    
    return js_str

# Load and parse credentials from credentials.js
def parse_credentials(file_content):
    try:
        # Remove variable declarations and exports
        content = file_content.strip()
        
        # Split into faculty and student sections
        sections = content.split('const studentCredentials =')
        
        # Parse faculty credentials
        faculty_str = sections[0].replace('const facultyCredentials =', '').strip()
        faculty_str = convert_js_to_json(faculty_str)
        
        # Parse student credentials
        student_str = sections[1] if len(sections) > 1 else '{}'
        student_str = convert_js_to_json(student_str)
        
        # Remove the debug print statements
        faculty_credentials = json.loads(faculty_str)
        student_credentials = json.loads(student_str)
        return faculty_credentials, student_credentials
    except Exception as e:
        print(f"Error parsing credentials: {e}")
        return {}, {}

# Load credentials
with open('credentials.js', 'r', encoding='utf-8') as file:
    credentials_content = file.read()
    facultyCredentials, studentCredentials = parse_credentials(credentials_content)

if not facultyCredentials or not studentCredentials:
    print("Warning: Failed to load credentials properly")

# Login route
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user_type = data.get('userType')
    
    # Check faculty credentials
    if user_type == 'faculty' and username in facultyCredentials:
        if facultyCredentials[username]['password'] == password:
            return jsonify({
                "success": True,
                "message": "Login successful",
                "userType": "faculty",
                "name": facultyCredentials[username]['name']
            })
    
    # Check student credentials
    if user_type == 'student' and username in studentCredentials:
        if studentCredentials[username]['password'] == password:
            return jsonify({
                "success": True,
                "message": "Login successful",
                "userType": "student",
                "name": studentCredentials[username]['name']
            })
    
    return jsonify({
        "success": False,
        "message": "Invalid username or password"
    }), 401

# Dashboard data endpoints
@app.route('/api/dashboard/schedule')
def get_dashboard_schedule():
    schedule = [
        {
            "time": "09:00\n10:30",
            "subject": "Advanced Mathematics",
            "location": "Room 305, Engineering Building",
            "status": "in-progress"
        },
        {
            "time": "11:00\n12:30",
            "subject": "Computer Science",
            "location": "Lab 201, Computer Building",
            "status": "upcoming"
        },
        {
            "time": "14:00\n15:30",
            "subject": "Physics Lab",
            "location": "Physics Building, Room 105",
            "status": "upcoming"
        }
    ]
    return jsonify(schedule)

@app.route('/api/dashboard/progress')
def get_course_progress():
    progress = [
        {
            "subject": "Advanced Mathematics",
            "progress": 68,
            "color": "blue"
        },
        {
            "subject": "Computer Science",
            "progress": 92,
            "color": "green"
        },
        {
            "subject": "Physics",
            "progress": 45,
            "color": "orange"
        }
    ]
    return jsonify(progress)

@app.route('/api/dashboard/attendance')
def get_attendance_summary():
    attendance = [
        {
            "subject": "Advanced Mathematics",
            "percentage": 85,
            "status": "good"
        },
        {
            "subject": "Computer Science",
            "percentage": 92,
            "status": "excellent"
        },
        {
            "subject": "Physics",
            "percentage": 70,
            "status": "warning"
        },
        {
            "subject": "English Literature",
            "percentage": 95,
            "status": "excellent"
        }
    ]
    return jsonify(attendance)

@app.route('/api/dashboard/assignments')
def get_upcoming_assignments():
    assignments = [
        {
            "title": "Research Paper",
            "subject": "English Literature",
            "dueIn": 2,
            "icon": "description",
            "color": "orange"
        },
        {
            "title": "Problem Set 5",
            "subject": "Advanced Mathematics",
            "dueIn": 5,
            "icon": "calculate",
            "color": "purple"
        }
    ]
    return jsonify(assignments)

# Data storage
data = {
    'todays_classes': [],
    'upcoming_exams': [],
    'attendance_summary': [],
    'results_summary': [],
    'social_posts': [],
    'trending_topics': [],
    'recommended_videos': []
}

# Data storage for assignments
assignments_data = {}

# Grades data storage
grades_data = {}

# Initialize with sample data
def initialize_data():
    data['todays_classes'] = [
        {
            "time": "8:00 AM - 9:00 AM",
            "subject": "Data Structures & Algorithms",
            "status": "completed"
        },
        {
            "time": "9:00 AM - 10:00 AM",
            "subject": "Business Analytics",
            "status": "completed"
        },
        {
            "time": "10:15 AM - 11:15 AM",
            "subject": "Database Management Systems",
            "status": "missed"
        },
        {
            "time": "11:15 AM - 12:15 PM",
            "subject": "Operating Systems",
            "status": "upcoming"
        },
        {
            "time": "1:15 PM - 2:15 PM",
            "subject": "Web Development Basics",
            "status": "upcoming"
        },
        {
            "time": "2:15 PM - 3:15 PM",
            "subject": "Soft Skills & Communication",
            "status": "upcoming"
        }
    ]

    data['upcoming_exams'] = [
        {
            "date": "15th Feb",
            "subject": "Data Structures & Algorithms"
        },
        {
            "date": "18th Feb",
            "subject": "Database Management Systems"
        },
        {
            "date": "21st Feb",
            "subject": "Business Analytics"
        },
        {
            "date": "24th Feb",
            "subject": "Operating Systems"
        },
        {
            "date": "27th Feb",
            "subject": "Web Development"
        }
    ]

    data['attendance_summary'] = [
        {
            "subject": "Data Structures & Algorithms",
            "percentage": 85,
            "status": "good"
        },
        {
            "subject": "Database Management Systems",
            "percentage": 90,
            "status": "good"
        },
        {
            "subject": "Business Analytics",
            "percentage": 75,
            "status": "warning"
        },
        {
            "subject": "Operating Systems",
            "percentage": 65,
            "status": "danger"
        },
        {
            "subject": "Web Development",
            "percentage": 95,
            "status": "good"
        }
    ]

    data['results_summary'] = [
        {
            "subject": "Data Structures & Algorithms",
            "percentage": 88,
            "grade": "A"
        },
        {
            "subject": "Database Management Systems",
            "percentage": 91,
            "grade": "A+"
        },
        {
            "subject": "Business Analytics",
            "percentage": 76,
            "grade": "B"
        },
        {
            "subject": "Operating Systems",
            "percentage": 69,
            "grade": "C"
        },
        {
            "subject": "Web Development",
            "percentage": 95,
            "grade": "A+"
        }
    ]

    # Social media data
    data['social_posts'] = [
        {
            "id": 1,
            "user": {
                "name": "Student Name",
                "username": "@username",
                "avatar": "student.jpg"
            },
            "content": "Just finished my Data Structures assignment! 🎉 #Coding #StudentLife",
            "media": "coding.jpg",
            "media_type": "image",
            "timestamp": "2h ago",
            "stats": {
                "comments": 24,
                "retweets": 12,
                "likes": 156
            }
        },
        {
            "id": 2,
            "user": {
                "name": "Student Name",
                "username": "@username",
                "avatar": "student.jpg"
            },
            "content": "Check out my latest study vlog! 📚 #StudyWithMe",
            "media": "study-vlog.mp4",
            "media_type": "video",
            "timestamp": "4h ago",
            "stats": {
                "comments": 45,
                "retweets": 23,
                "likes": 289
            }
        }
    ]

    data['trending_topics'] = [
        {"name": "#CampusLife", "posts": 2500},
        {"name": "#StudyGroup", "posts": 1800},
        {"name": "#ExamPrep", "posts": 1200},
        {"name": "#CampusEvents", "posts": 950}
    ]

    data['recommended_videos'] = [
        {
            "id": 1,
            "title": "How to Ace Your Exams",
            "thumbnail": "video1.jpg",
            "category": "Study Tips",
            "views": 250000
        },
        {
            "id": 2,
            "title": "Campus Tour 2024",
            "thumbnail": "video2.jpg",
            "category": "Campus Life",
            "views": 180000
        },
        {
            "id": 3,
            "title": "Study With Me",
            "thumbnail": "video3.jpg",
            "category": "Study Tips",
            "views": 150000
        }
    ]

# Initialize data
initialize_data()

# API Routes for fetching data
@app.route('/api/todays-classes')
def get_todays_classes():
    return jsonify(data['todays_classes'])

@app.route('/api/upcoming-exams')
def get_upcoming_exams():
    return jsonify(data['upcoming_exams'])

@app.route('/api/attendance-summary')
def get_attendance_data():
    return jsonify(data['attendance_summary'])

@app.route('/api/results-summary')
def get_results_summary():
    return jsonify(data['results_summary'])

# API Routes for updating data
@app.route('/api/todays-classes', methods=['POST'])
def update_todays_classes():
    new_class = request.json
    data['todays_classes'].append(new_class)
    return jsonify({"message": "Class added successfully"})

@app.route('/api/upcoming-exams', methods=['POST'])
def update_upcoming_exams():
    new_exam = request.json
    data['upcoming_exams'].append(new_exam)
    return jsonify({"message": "Exam added successfully"})

@app.route('/api/attendance-summary', methods=['POST'])
def update_attendance_summary():
    new_attendance = request.json
    data['attendance_summary'].append(new_attendance)
    return jsonify({"message": "Attendance updated successfully"})

@app.route('/api/results-summary', methods=['POST'])
def update_results_summary():
    new_result = request.json
    data['results_summary'].append(new_result)
    return jsonify({"message": "Result updated successfully"})

# API Routes for deleting data
@app.route('/api/todays-classes/<int:index>', methods=['DELETE'])
def delete_todays_class(index):
    if 0 <= index < len(data['todays_classes']):
        data['todays_classes'].pop(index)
        return jsonify({"message": "Class deleted successfully"})
    return jsonify({"error": "Invalid index"}), 400

@app.route('/api/upcoming-exams/<int:index>', methods=['DELETE'])
def delete_upcoming_exam(index):
    if 0 <= index < len(data['upcoming_exams']):
        data['upcoming_exams'].pop(index)
        return jsonify({"message": "Exam deleted successfully"})
    return jsonify({"error": "Invalid index"}), 400

@app.route('/api/attendance-summary/<int:index>', methods=['DELETE'])
def delete_attendance(index):
    if 0 <= index < len(data['attendance_summary']):
        data['attendance_summary'].pop(index)
        return jsonify({"message": "Attendance record deleted successfully"})
    return jsonify({"error": "Invalid index"}), 400

@app.route('/api/results-summary/<int:index>', methods=['DELETE'])
def delete_result(index):
    if 0 <= index < len(data['results_summary']):
        data['results_summary'].pop(index)
        return jsonify({"message": "Result deleted successfully"})
    return jsonify({"error": "Invalid index"}), 400

# API Routes for editing data
@app.route('/api/todays-classes/<int:index>', methods=['PUT'])
def edit_todays_class(index):
    if 0 <= index < len(data['todays_classes']):
        data['todays_classes'][index] = request.json
        return jsonify({"message": "Class updated successfully"})
    return jsonify({"error": "Invalid index"}), 400

@app.route('/api/upcoming-exams/<int:index>', methods=['PUT'])
def edit_upcoming_exam(index):
    if 0 <= index < len(data['upcoming_exams']):
        data['upcoming_exams'][index] = request.json
        return jsonify({"message": "Exam updated successfully"})
    return jsonify({"error": "Invalid index"}), 400

@app.route('/api/attendance-summary/<int:index>', methods=['PUT'])
def edit_attendance(index):
    if 0 <= index < len(data['attendance_summary']):
        data['attendance_summary'][index] = request.json
        return jsonify({"message": "Attendance record updated successfully"})
    return jsonify({"error": "Invalid index"}), 400

@app.route('/api/results-summary/<int:index>', methods=['PUT'])
def edit_result(index):
    if 0 <= index < len(data['results_summary']):
        data['results_summary'][index] = request.json
        return jsonify({"message": "Result updated successfully"})
    return jsonify({"error": "Invalid index"}), 400

# Social Media Routes
@app.route('/api/social/posts')
def get_social_posts():
    return jsonify(data['social_posts'])

@app.route('/api/social/posts', methods=['POST'])
def create_social_post():
    new_post = request.json
    new_post['id'] = len(data['social_posts']) + 1
    new_post['timestamp'] = "Just now"
    new_post['stats'] = {
        "comments": 0,
        "retweets": 0,
        "likes": 0
    }
    data['social_posts'].insert(0, new_post)
    return jsonify({"message": "Post created successfully", "post": new_post})

@app.route('/api/social/posts/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    for post in data['social_posts']:
        if post['id'] == post_id:
            post['stats']['likes'] += 1
            return jsonify({"message": "Post liked successfully"})
    return jsonify({"error": "Post not found"}), 404

@app.route('/api/social/posts/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    comment = request.json.get('comment')
    if not comment:
        return jsonify({"error": "Comment is required"}), 400
    
    for post in data['social_posts']:
        if post['id'] == post_id:
            post['stats']['comments'] += 1
            return jsonify({"message": "Comment added successfully"})
    return jsonify({"error": "Post not found"}), 404

@app.route('/api/social/trending')
def get_trending_topics():
    return jsonify(data['trending_topics'])

@app.route('/api/social/videos')
def get_recommended_videos():
    return jsonify(data['recommended_videos'])

# Real-time attendance data storage
attendance_records = {}

@app.route('/api/attendance/students', methods=['GET'])
def get_class_students():
    class_id = request.args.get('class')
    subject = request.args.get('subject')
    section = request.args.get('section')
    
    try:
        # Read attendance records
        with open('attendance_records.json', 'r') as f:
            attendance_records = json.load(f)
        
        # Get today's date
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Get students from today's attendance records for the specified subject
        students = []
        if today in attendance_records and subject in attendance_records[today]:
            for student_id, attendance_data in attendance_records[today][subject].items():
                if attendance_data['class'] == class_id and attendance_data['section'] == section:
                    # Get student name from credentials
                    student_name = studentCredentials.get(student_id, {}).get('name', f"Student {student_id}")
                    # Extract initials for avatar
                    initials = student_id[:2].upper()
                    students.append({
                        "id": student_id,
                        "name": student_name,
                        "avatar": initials,
                        "status": attendance_data['status'],
                        "timestamp": attendance_data['timestamp']
                    })
        
        # If no students found for today, return a default list with actual names
        if not students:
            default_students = [
                "23BB1A3201", "23BB1A3202", "23BB1A3203", "23BB1A3204", "23BB1A3205",
                "23BB1A3206", "23BB1A3207", "23BB1A3208", "23BB1A3209", "23BB1A3210",
                "23BB1A3211", "23BB1A3212", "23BB1A3213", "23BB1A3214", "23BB1A3215",
                "23BB1A3216", "23BB1A3217", "23BB1A3218", "23BB1A3219", "23BB1A3220",
                "23BB1A3221", "23BB1A3222", "23BB1A3223", "23BB1A3224", "23BB1A3225",
                "23BB1A3226", "23BB1A3227", "23BB1A3228", "23BB1A3229", "23BB1A3230",
                "23BB1A3231", "23BB1A3232", "23BB1A3233", "23BB1A3234", "23BB1A3235",
                "23BB1A3236", "23BB1A3237", "23BB1A3238", "23BB1A3239", "23BB1A3240",
                "23BB1A3241", "23BB1A3242", "23BB1A3243", "23BB1A3244", "23BB1A3245",
                "23BB1A3246", "23BB1A3247", "23BB1A3248", "23BB1A3249", "23BB1A3250",
                "23BB1A3251", "23BB1A3252", "23BB1A3253", "23BB1A3254", "23BB1A3255",
                "23BB1A3256", "23BB1A3257", "23BB1A3258", "23BB1A3259", "23BB1A3260",
                "23BB1A3261", "23BB1A3262", "23BB1A3263", "23BB1A3264"
            ]
            students = []
            for student_id in default_students:
                student_name = studentCredentials.get(student_id, {}).get('name', f"Student {student_id}")
                initials = student_id[:2].upper()
                students.append({
                    "id": student_id,
                    "name": student_name,
                    "avatar": initials,
                    "status": "not_marked",
                    "timestamp": datetime.now().isoformat()
                })
        
        return jsonify(students)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching students: {str(e)}"
        }), 500

@app.route('/api/attendance/mark', methods=['POST'])
def mark_attendance():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['studentId', 'status', 'class', 'subject', 'section', 'date']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Get current attendance records or initialize if not exists
        attendance_file = 'attendance_records.json'
        try:
            with open(attendance_file, 'r') as f:
                attendance_records = json.load(f)
        except FileNotFoundError:
            attendance_records = {}
        
        # Structure: date -> subject -> studentId -> attendance_data
        if data['date'] not in attendance_records:
            attendance_records[data['date']] = {}
        if data['subject'] not in attendance_records[data['date']]:
            attendance_records[data['date']][data['subject']] = {}
            
        # Store attendance record
        attendance_records[data['date']][data['subject']][data['studentId']] = {
            'status': data['status'],
            'timestamp': datetime.now().isoformat(),
            'class': data['class'],
            'section': data['section'],
            'markedBy': request.headers.get('Username', 'unknown')
        }
        
        # Save to file
        with open(attendance_file, 'w') as f:
            json.dump(attendance_records, f, indent=2)
            
        return jsonify({
            'success': True,
            'message': 'Attendance marked successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error marking attendance: {str(e)}'
        }), 500

@app.route('/api/attendance/status', methods=['GET'])
def get_attendance_status():
    student_id = request.args.get('studentId')
    today = datetime.now().strftime('%Y-%m-%d')
    current_day = datetime.now().strftime('%A').upper()
    
    try:
        # Read attendance records
        try:
            with open('attendance_records.json', 'r') as f:
                attendance_records = json.load(f)
        except FileNotFoundError:
            attendance_records = {}
            
        # Define the weekly schedule based on the timetable
        weekly_schedule = {
            'MONDAY': [
                {"time": "9:00 AM - 10:00 AM", "subject": "Computational Statistics", "code": "CS101", "room": "110 CM"},
                {"time": "10:00 AM - 11:00 AM", "subject": "Design & Analysis of Algorithms", "code": "DAA101", "room": "110 CM"},
                {"time": "11:10 AM - 12:10 PM", "subject": "Operating Systems", "code": "OS101", "room": "110 CM"},
                {"time": "12:10 PM - 1:10 PM", "subject": "Python for EDA", "code": "EDA101", "room": "110 CM"},
                {"time": "1:55 PM - 3:55 PM", "subject": "RFP LAB", "code": "RFP101", "room": "308 CM"}
            ],
            'TUESDAY': [
                {"time": "9:00 AM - 10:00 AM", "subject": "Software Engineering", "code": "PSE101", "room": "110 CM"},
                {"time": "10:00 AM - 1:10 PM", "subject": "SE LAB", "code": "SE101", "room": "105 CB"},
                {"time": "1:55 PM - 2:55 PM", "subject": "Computational Statistics", "code": "CS101", "room": "110 CM"},
                {"time": "2:55 PM - 3:55 PM", "subject": "Design & Analysis of Algorithms", "code": "DAA101", "room": "110 CM"}
            ],
            'WEDNESDAY': [
                {"time": "9:00 AM - 12:10 PM", "subject": "E-BOX LAB", "code": "EBOX101", "room": "203 MB"},
                {"time": "12:10 PM - 1:10 PM", "subject": "Design & Analysis of Algorithms", "code": "DAA101", "room": "110 CM"},
                {"time": "1:55 PM - 2:55 PM", "subject": "Operating Systems", "code": "OS101", "room": "110 CM"},
                {"time": "2:55 PM - 3:55 PM", "subject": "Library", "code": "LIB101", "room": "Library"}
            ],
            'THURSDAY': [
                {"time": "9:00 AM - 12:10 PM", "subject": "CS & EDA LAB", "code": "CSEDA101", "room": "308 CM"},
                {"time": "12:10 PM - 1:10 PM", "subject": "Python for EDA", "code": "EDA101", "room": "110 CM"},
                {"time": "1:55 PM - 2:55 PM", "subject": "Software Engineering", "code": "PSE101", "room": "110 CM"},
                {"time": "2:55 PM - 3:55 PM", "subject": "Mentoring", "code": "MEN101", "room": "110 CM"}
            ],
            'FRIDAY': [
                {"time": "9:00 AM - 12:10 PM", "subject": "ALG & OS LAB", "code": "ALGOS101", "room": "304 CM"},
                {"time": "12:10 PM - 1:10 PM", "subject": "Software Engineering", "code": "PSE101", "room": "110 CM"},
                {"time": "1:55 PM - 3:55 PM", "subject": "RFP LAB", "code": "RFP101", "room": "308 CM"}
            ],
            'SATURDAY': [
                {"time": "9:00 AM - 10:00 AM", "subject": "CRT", "code": "CRT101", "room": "110 CM"},
                {"time": "12:10 PM - 1:10 PM", "subject": "Computational Statistics", "code": "CS101", "room": "110 CM"},
                {"time": "11:10 AM - 12:10 PM", "subject": "Operating Systems", "code": "OS101", "room": "110 CM"},
                {"time": "1:55 PM - 2:55 PM", "subject": "Python for EDA", "code": "EDA101", "room": "110 CM"},
                {"time": "2:55 PM - 3:55 PM", "subject": "Sports", "code": "SPT101", "room": "Ground"}
            ]
        }
        
        # Get today's schedule
        schedule = weekly_schedule.get(current_day, [])
        
        # Get current time to determine ongoing class
        current_time = datetime.now().strftime('%H:%M')
        
        # Add attendance status to each class
        for class_info in schedule:
            subject_code = class_info["code"]
            if today in attendance_records and subject_code in attendance_records[today]:
                if student_id in attendance_records[today][subject_code]:
                    class_info["attendance"] = attendance_records[today][subject_code][student_id]
                else:
                    class_info["attendance"] = {"status": "not_marked"}
            else:
                class_info["attendance"] = {"status": "not_marked"}
            
            # Determine if this is the current class
            time_range = class_info["time"].split(" - ")
            start_time = datetime.strptime(time_range[0], '%I:%M %p').strftime('%H:%M')
            end_time = datetime.strptime(time_range[1], '%I:%M %p').strftime('%H:%M')
            
            if start_time <= current_time <= end_time:
                class_info["current"] = True
            else:
                class_info["current"] = False
        
        return jsonify({
            "success": True,
            "schedule": schedule,
            "day": current_day
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching attendance status: {str(e)}"
        }), 500

@app.route('/api/assignments/create', methods=['POST'])
def create_assignment():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['title', 'subject', 'description', 'dueDate', 'instructor']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Generate a unique ID for the assignment
        assignment_id = str(len(assignments_data) + 1)
        
        # Create assignment object
        assignment = {
            'id': assignment_id,
            'title': data['title'],
            'subject': data['subject'],
            'description': data['description'],
            'dueDate': data['dueDate'],
            'instructor': data['instructor'],
            'attachments': data.get('attachments', []),
            'createdAt': datetime.now().isoformat(),
            'createdBy': request.headers.get('Username', 'unknown'),
            'submissions': 0
        }
        
        # Store assignment
        assignments_data[assignment_id] = assignment
        
        return jsonify({
            'success': True,
            'message': 'Assignment created successfully',
            'assignment': assignment
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error creating assignment: {str(e)}'
        }), 500

@app.route('/api/assignments/faculty/<faculty_id>', methods=['GET'])
def get_faculty_assignments(faculty_id):
    try:
        # Filter assignments created by this faculty
        faculty_assignments = [
            assignment for assignment in assignments_data.values()
            if assignment['createdBy'] == faculty_id
        ]
        
        return jsonify({
            'success': True,
            'assignments': faculty_assignments
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching assignments: {str(e)}'
        }), 500

@app.route('/api/assignments/student/<student_id>', methods=['GET'])
def get_student_assignments(student_id):
    try:
        # For now, return all assignments
        # In a real implementation, you would filter by the student's courses
        student_assignments = list(assignments_data.values())
        
        return jsonify({
            'success': True,
            'assignments': student_assignments
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching assignments: {str(e)}'
        }), 500

@app.route('/api/grades', methods=['POST'])
def submit_grades():
    try:
        data = request.json
        term = data.get('term')
        type = data.get('type')
        subject = data.get('subject')
        grades = data.get('grades', [])

        if not all([term, type, subject, grades]):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400

        # Store grades for each student
        for grade in grades:
            student_id = grade.get('studentId')
            marks = grade.get('marks')
            
            if not student_id or marks is None:
                continue

            # Initialize student's grades if not exists
            if student_id not in grades_data:
                grades_data[student_id] = []

            # Add new grade entry
            grades_data[student_id].append({
                'subject': subject,
                'type': type,
                'term': term,
                'marks': marks,
                'maxMarks': 10 if type == 'assignment' else 30,
                'status': 'Graded',
                'timestamp': datetime.now().isoformat()
            })

        return jsonify({
            'success': True,
            'message': 'Grades submitted successfully'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error submitting grades: {str(e)}'
        }), 500

@app.route('/api/grades/<student_id>', methods=['GET'])
def get_student_grades(student_id):
    try:
        if student_id not in grades_data:
            return jsonify([])

        # Get all grades for the student
        student_grades = grades_data[student_id]
        
        # Sort by timestamp (newest first)
        student_grades.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return jsonify(student_grades)

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching grades: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)