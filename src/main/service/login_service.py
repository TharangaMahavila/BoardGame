import bcrypt
from src.main.util.common import validate_email
from src.main.models.member import Member


class LoginService:
    def __init__(self, context=None, user_repo=None):
        self.context = context
        self.userRepo = user_repo

    def member_registration(self, fname, lname, street, city, postal, phone, email, password):
        try:
            # Dictionary of required fields that must not be empty
            required_fields = {
                "first_name": fname,
                "last_name": lname,
                "email": email,
                "password": password
                }

            # Validate required fields
            for field, value in required_fields.items():
                # Check if the field is empty or contains only spaces
                if not value.strip():
                    raise ValueError(f"{field} is mandatory")

                # Additional validation for email
                if field == "email":
                    validate_email(value)   # Check email format
                    self.check_email_already_in_use(value)  # Ensure email is unique

            # Hash the password using bcrypt before saving it
            hash_password = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()
                ).decode("utf-8")

            # Create a Member object with the provided details
            member = Member(
                "",
                fname,
                lname,
                street,
                city,
                postal,
                phone,
                email,
                hash_password
            )

            # Save the member to the database and return the new user ID
            return self.userRepo.save_member(member)
        except Exception as e:
            raise e

    def user_login(self, email, password):
        # Ensure both email and password are provided
        if not (email.strip() and password):
            raise ValueError("Email/Password required")

        # Validate email format
        validate_email(email)

        # Retrieve the user record by email
        member = self.userRepo.get_member_by_email(email)
        if not member:
            raise ValueError("Email address does not exist")

        # Compare the entered password with the stored hashed password
        if not bcrypt.checkpw(password.encode("utf-8"),
                              member["pwd_hash"].encode("utf-8")):
            raise ValueError("Invalid credentials")

        # Remove the password hash before returning the user object
        member.pop("pwd_hash", None)

        # Return the authenticated user data
        return member

    def check_email_already_in_use(self, email):
        # Check if the email already exists in the database
        member = self.userRepo.get_member_by_email(email)
        # If a user is found, prevent duplicate registration
        if member:
            raise ValueError("Email address is already in use. Please login")
