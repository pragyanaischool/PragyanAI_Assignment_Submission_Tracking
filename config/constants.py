# config/constants.py

# ==============================
# 📌 USER STATUS
# ==============================
STATUS_ACTIVE = "active"
STATUS_INACTIVE = "inactive"
STATUS_PENDING = "pending"
STATUS_APPROVED = "approved"
STATUS_REJECTED = "rejected"


# ==============================
# 📚 ASSIGNMENT STATUS
# ==============================
ASSIGNMENT_ASSIGNED = "assigned"
ASSIGNMENT_STARTED = "started"
ASSIGNMENT_SUBMITTED = "submitted"
ASSIGNMENT_COMPLETED = "completed"
ASSIGNMENT_OVERDUE = "overdue"


# ==============================
# 🧠 TEST MODES
# ==============================
MODE_TEST = "test"                 # RAG guided test
MODE_UPLOAD = "upload"             # Direct submission


# ==============================
# 📊 ANALYTICS LABELS
# ==============================
ANALYTICS_COMPLETED = "completed"
ANALYTICS_PENDING = "pending"
ANALYTICS_OVERDUE = "overdue"


# ==============================
# 📁 FILE TYPES
# ==============================
FILE_TYPE_PDF = "pdf"
FILE_TYPE_DOCX = "docx"
FILE_TYPE_TXT = "txt"
FILE_TYPE_IMAGE = "image"


# ==============================
# 🎯 DEFAULT VALUES
# ==============================
DEFAULT_SCORE = 0
DEFAULT_TIME_SPENT = 0
DEFAULT_ATTEMPTS = 1


# ==============================
# ⚠️ ERROR MESSAGES
# ==============================
ERR_USER_NOT_FOUND = "User not found"
ERR_INVALID_LOGIN = "Invalid credentials"
ERR_ACCESS_DENIED = "Access denied"
ERR_FILE_TOO_LARGE = "File size exceeds limit"
ERR_INVALID_FILE_TYPE = "Invalid file type"


# ==============================
# ✅ SUCCESS MESSAGES
# ==============================
MSG_LOGIN_SUCCESS = "Login successful"
MSG_SUBMISSION_SUCCESS = "Submission successful"
MSG_TEST_COMPLETED = "Test completed"
MSG_UPLOAD_SUCCESS = "File uploaded successfully"
