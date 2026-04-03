from enum import Enum


class Roles(str, Enum):
    ADMIN = "admin"
    STUDENT = "student"
    FACULTY = "faculty"
    SUPER_ADMIN = "super_admin"


ROLE_PERMISSIONS = {
    Roles.ADMIN: [
        "approve_students",
        "add_test",
        "view_all_students",
        "view_all_tests",
        "view_analytics",
        "download_reports",
    ],
    Roles.STUDENT: [
        "take_test",
        "submit_assignment",
        "view_own_analytics",
        "view_tests",
    ],
    Roles.FACULTY: [
        "add_test",
        "view_students",
        "view_analytics",
        "review_submissions",
    ],
    Roles.SUPER_ADMIN: [
        "all_access",
    ],
}


def has_permission(role, permission):
    if role == Roles.SUPER_ADMIN:
        return True
    return permission in ROLE_PERMISSIONS.get(role, [])


def is_admin(role):
    return role in {Roles.ADMIN, Roles.SUPER_ADMIN}


def is_student(role):
    return role == Roles.STUDENT


def is_faculty(role):
    return role in {Roles.FACULTY, Roles.ADMIN, Roles.SUPER_ADMIN}


def require_permission(user, permission):
    if not user:
        raise Exception("User not logged in")

    role = user.get("role")

    if not has_permission(role, permission):
        raise PermissionError(f"Access Denied: {permission}")
