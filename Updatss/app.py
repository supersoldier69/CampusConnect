from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Predefined user credentials
VALID_USERNAME = "23b81a3232"
VALID_PASSWORD = "password123"

# Login route
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user_type = data.get('userType')
    
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return jsonify({
            "success": True,
            "message": "Login successful",
            "userType": user_type
        })
    else:
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

if __name__ == '__main__':
    app.run(debug=True, port=5001)