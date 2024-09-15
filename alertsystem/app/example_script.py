
from datetime import datetime, timedelta
from .alert_system import AlertSystem

system = AlertSystem()

user1 = system.register_user("Alice")
user2 = system.register_user("Bob")

news_topic = system.register_topic("News")
sports_topic = system.register_topic("Sports")

system.subscribe_user_to_topic(user1, news_topic)
system.subscribe_user_to_topic(user2, sports_topic)


system.send_alert(
    content="Breaking News: Global Event!", 
    alert_type="informative", 
    expiration_date=datetime.now() + timedelta(days=1), 
    topic=news_topic
)

system.send_alert(
    content="Exclusive: Personal Offer!", 
    alert_type="urgent", 
    expiration_date=datetime.now() - timedelta(days=1), 
    topic=news_topic, 
    targeted_user=user1
)

system.send_alert(
    content="Sports Update: Match Results", 
    alert_type="informative", 
    expiration_date=datetime.now() + timedelta(days=2), 
    topic=sports_topic
)

unread_alerts = system.get_unread_alerts(user1)

system.mark_alert_as_read(user1, unread_alerts[0])

unread_alerts_user1 = system.get_unread_alerts(user1)

unexpired_alerts_news = system.get_unexpired_alerts(news_topic)



