class LoginService:
    def __init__(self):
        pass

    def member_registration(self, fname, lname, street, city, postal, phone, email, password):
        try:
            required_fields = {
                "first_name": fname,
                "last_name": lname,
                "street": street,
                "city": city,
                "postal_code": postal,
                "email": email,
                "password": password
                }
            optional_fields = {
                "phone": phone
            }
            for field, value in required_fields.items():
                if not value.strip():
                    raise ValueError(f"{field} is mandatory")
        except Exception as e:
            raise e
