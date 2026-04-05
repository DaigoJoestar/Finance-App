from models import User
from extensions import db

class UserService:
    @staticmethod
    def create_user(username, email, password, role='viewer', active=True):
        if User.query.filter_by(username=username).first():
            raise ValueError("Username already exists")
        if User.query.filter_by(email=email).first():
            raise ValueError("Email already exists")
        user = User(username=username, email=email, role=role, active=active)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_users(page, per_page):
        paginated = User.query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            "items": [u.to_dict() for u in paginated.items],
            "total": paginated.total,
            "page": page,
            "per_page": per_page,
            "pages": paginated.pages
        }

    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        return user

    @staticmethod
    def update_user(user_id, data):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.set_password(data['password'])
        if 'role' in data:
            user.role = data['role']
        if 'active' in data:
            user.active = data['active']
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        db.session.delete(user)
        db.session.commit()
        return True