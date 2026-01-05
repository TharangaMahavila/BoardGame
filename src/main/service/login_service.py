import bcrypt
from src.main.util.common import validate_email
from src.main.models.member import Member


class LoginService:
    def __init__(self, context=None, user_repo=None):
        self.context = context
        self.userRepo = user_repo

    def member_registration(self, fname, lname, street, city, postal, phone, email, password):
        try:
            required_fields = {
                "first_name": fname,
                "last_name": lname,
                "email": email,
                "password": password
                }
            for field, value in required_fields.items():
                if not value.strip():
                    raise ValueError(f"{field} is mandatory")
                if field == "email":
                    validate_email(value)
                    self.check_email_already_in_use(value)

            hash_password = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()
                ).decode("utf-8")

            member = Member(
                fname,
                lname,
                street,
                city,
                postal,
                phone,
                email,
                hash_password
            )

            return self.userRepo.save_member(member)
        except Exception as e:
            raise e

    def user_login(self, email, password):
        if not (email.strip() and password):
            raise ValueError("Email/Password required")
        validate_email(email)
        member = self.userRepo.get_member_by_email(email)
        if not member:
            raise ValueError("Email address does not exist")
        if not bcrypt.checkpw(password.encode("utf-8"),
                              member["pwd_hash"].encode("utf-8")):
            raise ValueError("Invalid credentials")
        member.pop("pwd_hash", None)
        print(member)
        return member

    def check_email_already_in_use(self, email):
        member = self.userRepo.get_member_by_email(email)
        if member:
            raise ValueError("Email address is already in use. Please login")
