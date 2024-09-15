from datetime import datetime
from typing import Optional

from .alerts.alerts import Alert
from .alerts.factories import AlertFactory
from .topics import Topic
from .users import User


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class AlertSystem(metaclass=SingletonMeta):
    
    def __init__(self):
        self.users = []
        self.topics = []

    def register_user(self, name: str) -> User:
        user = User(name)
        self.users.append(user)
        return user
    
    def register_topic(self, name: str) -> Topic:
        topic = Topic(name)
        self.topics.append(topic)
        return topic
    

    def subscribe_user_to_topic(self, user: User, topic: Topic) -> None:
        user.subscribe_to_topic(topic)


    def send_alert(self, content: str, alert_type: str, expiration_date: Optional[datetime], topic: Topic, targeted_user: Optional['User'] = None):
        alert = AlertFactory.create_alert(alert_type=alert_type, content=content, expiration_date=expiration_date, targeted_user=targeted_user)
        topic.notify(alert)

   
    def mark_alert_as_read(self, user: User, alert: Alert) -> None:
        user.read_alert(alert)
    
    
    def get_unread_alerts(self, user: User) -> list[Alert]:
        return user.get_unread_unexpired_alerts()
    
    def get_unexpired_alerts(self, topic: Topic) -> list[Alert]:
        return topic.get_non_expired_alerts()