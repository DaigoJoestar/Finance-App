from models import FinancialRecord
from sqlalchemy import func, extract
from datetime import datetime, timedelta

class DashboardService:
    @staticmethod
    def get_summary(year=None):
        query = FinancialRecord.query
        if year:
            query = query.filter(extract('year', FinancialRecord.date) == year)
        total_income = query.filter_by(type='income').with_entities(func.sum(FinancialRecord.amount)).scalar() or 0.0
        total_expense = query.filter_by(type='expense').with_entities(func.sum(FinancialRecord.amount)).scalar() or 0.0
        return {
            "total_income": float(total_income),
            "total_expense": float(total_expense),
            "net_balance": float(total_income - total_expense)
        }

    @staticmethod
    def get_category_totals(year=None):
        query = FinancialRecord.query
        if year:
            query = query.filter(extract('year', FinancialRecord.date) == year)
        income_cat = query.filter_by(type='income').with_entities(
            FinancialRecord.category, func.sum(FinancialRecord.amount)
        ).group_by(FinancialRecord.category).all()
        expense_cat = query.filter_by(type='expense').with_entities(
            FinancialRecord.category, func.sum(FinancialRecord.amount)
        ).group_by(FinancialRecord.category).all()
        return {
            "income_by_category": {c: float(a) for c, a in income_cat},
            "expense_by_category": {c: float(a) for c, a in expense_cat}
        }

    @staticmethod
    def get_recent(limit=5):
        recent = FinancialRecord.query.order_by(FinancialRecord.date.desc()).limit(limit).all()
        return {"recent_transactions": [r.to_dict() for r in recent]}

    @staticmethod
    def get_monthly_trends(months=12):
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30*months)
        records = FinancialRecord.query.filter(FinancialRecord.date >= start_date).all()
        trends = {}
        for r in records:
            key = r.date.strftime("%Y-%m")
            if key not in trends:
                trends[key] = {"income": 0.0, "expense": 0.0}
            if r.type == "income":
                trends[key]["income"] += r.amount
            else:
                trends[key]["expense"] += r.amount
        sorted_items = sorted(trends.items())
        return {
            "months": [m for m, _ in sorted_items],
            "income": [v["income"] for _, v in sorted_items],
            "expense": [v["expense"] for _, v in sorted_items],
            "net": [v["income"] - v["expense"] for _, v in sorted_items]
        }