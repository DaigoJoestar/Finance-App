from schemas import UserCreateSchema, UserUpdateSchema
from services.user_service import UserService

class UserController:
    @staticmethod
    def create_user(data):
        schema = UserCreateSchema()
        errors = schema.validate(data)
        if errors:
            return None, errors, 400
        try:
            user = UserService.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                role=data.get('role', 'viewer'),
                active=data.get('active', True)
            )
            return user.to_dict(), None, 201
        except ValueError as e:
            return None, {"error": str(e)}, 409

    @staticmethod
    def get_users(page, per_page):
        result = UserService.get_users(page, per_page)
        return result, 200

    @staticmethod
    def get_user(user_id):
        try:
            user = UserService.get_user_by_id(user_id)
            return user.to_dict(), None, 200
        except ValueError as e:
            return None, {"error": str(e)}, 404

    @staticmethod
    def update_user(user_id, data):
        schema = UserUpdateSchema(partial=True)
        errors = schema.validate(data)
        if errors:
            return None, errors, 400
        try:
            user = UserService.update_user(user_id, data)
            return user.to_dict(), None, 200
        except ValueError as e:
            return None, {"error": str(e)}, 404

    @staticmethod
    def delete_user(user_id):
        try:
            UserService.delete_user(user_id)
            return {"message": "User deleted"}, None, 200
        except ValueError as e:
            return None, {"error": str(e)}, 404