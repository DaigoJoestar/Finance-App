from flask_jwt_extended import create_access_token
from models import User

class AuthController:
    @staticmethod
    def login(username, password):
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password) or not user.active:
            return None, "Invalid credentials or inactive user"
        token = create_access_token(identity=user.username)
        return {"access_token": token, "role": user.role}, None