from models import FinancialRecord
from extensions import db
from datetime import date

class RecordService:
    @staticmethod
    def create_record(amount, type_, category, date_val, description, user_id):
        
        if isinstance(date_val, str):
            date_val = date.fromisoformat(date_val)
            
        record = FinancialRecord(
            amount=amount,
            type=type_,
            category=category,
            date=date_val,
            description=description,
            user_id=user_id
        )
        db.session.add(record)
        db.session.commit()
        return record

    @staticmethod
    def get_records(filters, page, per_page):
        query = FinancialRecord.query
        if filters.get('type'):
            query = query.filter_by(type=filters['type'])
        if filters.get('category'):
            query = query.filter_by(category=filters['category'])
        if filters.get('date_from'):
            query = query.filter(FinancialRecord.date >= filters['date_from'])
        if filters.get('date_to'):
            query = query.filter(FinancialRecord.date <= filters['date_to'])
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            "items": [r.to_dict() for r in paginated.items],
            "total": paginated.total,
            "page": page,
            "per_page": per_page,
            "pages": paginated.pages
        }

    @staticmethod
    def get_record_by_id(record_id):
        record = FinancialRecord.query.get(record_id)
        if not record:
            raise ValueError("Record not found")
        return record

    @staticmethod
    def update_record(record_id, data):
        record = FinancialRecord.query.get(record_id)
        if not record:
            raise ValueError("Record not found")
        for key, value in data.items():
            if key == 'date' and isinstance(value, str):
                value = date.fromisoformat(value)
            setattr(record, key, value)
        db.session.commit()
        return record

    @staticmethod
    def delete_record(record_id):
        record = FinancialRecord.query.get(record_id)
        if not record:
            raise ValueError("Record not found")
        db.session.delete(record)
        db.session.commit()
        return True