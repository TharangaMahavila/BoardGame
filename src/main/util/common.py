import re

EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def validate_email(email: str):
    # Checks whether the given email matches the EMAIL_REGEX pattern
    # If it does not match, an exception is raised to indicate invalid format
    if not EMAIL_REGEX.match(email):
        raise ValueError("Invalid email format")
