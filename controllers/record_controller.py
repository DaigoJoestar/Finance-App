from schemas import RecordSchema
from services.record_service import RecordService

class RecordController:
    @staticmethod
    def create_record(data, user_id):
        schema = RecordSchema()
        errors = schema.validate(data)
        if errors:
            return None, errors, 400
        try:
            record = RecordService.create_record(
                amount=data['amount'],
                type_=data['type'],
                category=data['category'],
                date_val=data['date'],
                description=data.get('description'),
                user_id=user_id
            )
            return record.to_dict(), None, 201
        except Exception as e:
            return None, {"error": str(e)}, 500

    @staticmethod
    def get_records(filters, page, per_page):
        result = RecordService.get_records(filters, page, per_page)
        return result, 200

    @staticmethod
    def get_record(record_id):
        try:
            record = RecordService.get_record_by_id(record_id)
            return record.to_dict(), None, 200
        except ValueError as e:
            return None, {"error": str(e)}, 404

    @staticmethod
    def update_record(record_id, data):
        schema = RecordSchema(partial=True)
        errors = schema.validate(data)
        if errors:
            return None, errors, 400
        try:
            record = RecordService.update_record(record_id, data)
            return record.to_dict(), None, 200
        except ValueError as e:
            return None, {"error": str(e)}, 404

    @staticmethod
    def delete_record(record_id):
        try:
            RecordService.delete_record(record_id)
            return {"message": "Record deleted"}, None, 200
        except ValueError as e:
            return None, {"error": str(e)}, 404