from abc import ABC, abstractmethod


class AlertHandler(ABC):
    @abstractmethod
    def get_alerts(self) -> list:
        pass

    def add_alert_to_queue(self, alert: 'Alert') -> None:
        alert_list = self.get_alerts()
        strategy = alert.insertion_strategy
        strategy.insert_alert(alert, alert_list)


class UserAlertHandler(AlertHandler):
    def __init__(self, user: 'User') -> None:
        self.user = user

    def get_alerts(self) -> list:
        return self.user.alerts

    def handle(self, alert: 'Alert') -> None:
        self.add_alert_to_queue(alert)
        self.user.alert_read_status[alert] = False


class TopicAlertHandler(AlertHandler):
    def __init__(self, topic: 'Topic') -> None:
        self.topic = topic

    def get_alerts(self) -> list:
        return self.topic.alerts

    def handle(self, alert: 'Alert') -> None:
        self.add_alert_to_queue(alert)