from services.dashboard_service import DashboardService

class DashboardController:
    @staticmethod
    def get_summary(year):
        result = DashboardService.get_summary(year)
        return result, 200

    @staticmethod
    def get_category_totals(year):
        result = DashboardService.get_category_totals(year)
        return result, 200

    @staticmethod
    def get_recent(limit):
        result = DashboardService.get_recent(limit)
        return result, 200

    @staticmethod
    def get_trends(months):
        result = DashboardService.get_monthly_trends(months)
        return result, 200