from datetime import datetime
from typing import Optional

from .alerts import Alert, InformativeAlert, UrgentAlert
from ..users import User


class AlertFactory:
    @staticmethod
    def create_alert(alert_type: str, content:str, expiration_date: Optional[datetime] = None, targeted_user: Optional['User'] = None) -> Alert:
        
        if alert_type == "informative":
            return InformativeAlert(content, expiration_date, targeted_user)
        elif alert_type == "urgent":
            return UrgentAlert(content, expiration_date, targeted_user)