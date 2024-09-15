from abc import ABC, abstractmethod
from typing import Dict, List

from .alerts.alert_handlers import UserAlertHandler

from .topics import Topic
from .alerts.alerts import Alert

class Observer(ABC):
    
    @abstractmethod
    def update(self, alert: 'Alert') -> None:
        pass


class User(Observer):

    def __init__(self, name: str) -> None:
        self.name = name
        self.alerts: List['Alert'] = []
        self.alert_read_status: Dict['Alert', bool] = {}

    def get_alerts(self) -> List['Alert']:
        return self.alerts
    
    def read_alert(self, alert: 'Alert') -> None:
        if alert in self.alerts:
            self.alert_read_status[alert] = True
        
    def subscribe_to_topic(self, topic: 'Topic') -> None:
        topic.subscribe(self)
    
    def update(self, alert: 'Alert') -> None:
        if alert not in self.alerts:
            handler = UserAlertHandler(self)
            handler.handle(alert)
        
    def get_unread_unexpired_alerts(self) -> List['Alert']:
        return [
            alert 
            for alert in self.alerts 
            if not self.alert_read_status.get(alert, False) and not alert.is_expired()
        ]