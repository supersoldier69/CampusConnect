// Import credentials
const { facultyCredentials, studentCredentials } = require('./credentials.js');

function handleLogin(username, password) {
    // Check faculty credentials
    if (facultyCredentials[username]) {
        if (facultyCredentials[username].password === password) {
            return {
                success: true,
                user: facultyCredentials[username]
            };
        }
    }

    // Check student credentials
    if (studentCredentials[username]) {
        if (studentCredentials[username].password === password) {
            return {
                success: true,
                user: studentCredentials[username]
            };
        }
    }

    return {
        success: false,
        message: "Invalid username or password"
    };
}

// Function to get student list for faculty
function getStudentList() {
    return Object.values(studentCredentials).map(student => ({
        id: student.username,
        name: student.name
    }));
}

// Function to get faculty list
function getFacultyList() {
    return Object.values(facultyCredentials).map(faculty => ({
        id: faculty.username,
        name: faculty.name
    }));
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { handleLogin, getStudentList, getFacultyList };
} 