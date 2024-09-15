from typing import List


from .alerts.alerts import Alert

class Topic:
    def __init__(self, name) -> None:
        from .users import User
        self.name = name
        self.subscribers: List[User] = []
        self.alerts: List[Alert] = []

    def subscribe(self, user: 'Observer') -> None:
        if user not in self.subscribers:
            self.subscribers.append(user)

    def unsubscribe(self, user: 'User') -> None:
        if user in self.subscribers:
            self.subscribers.remove(user)
    
    def notify(self, alert: 'Alert') -> None:
        
        self.add_alert(alert)

        if alert.is_for_all_users():
            for subscriber in self.subscribers:
                subscriber.update(alert)
        else:
            if alert.targeted_user in self.subscribers:
                alert.targeted_user.update(alert)

    def add_alert(self, alert: 'Alert') -> None:
        from .alerts.alert_handlers import TopicAlertHandler
        topic_handler = TopicAlertHandler(self)
        topic_handler.handle(alert)

    def get_non_expired_alerts(self) -> List['Alert']:
        return [alert for alert in self.alerts if not alert.is_expired()]