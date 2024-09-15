import pytest
from datetime import datetime, timedelta
from ..app.users import User
from ..app.topics import Topic
from ..app.alerts.alerts import InformativeAlert, UrgentAlert


def create_informative_alert(content, expiration_days=None, targeted_user=None):
    expiration_date = None
    if expiration_days is not None:
        expiration_date = datetime.now() + timedelta(days=expiration_days)
    return InformativeAlert(content=content, expiration_date=expiration_date, targeted_user=targeted_user)

def create_urgent_alert(content, expiration_days=None, targeted_user=None):
    expiration_date = None
    if expiration_days is not None:
        expiration_date = datetime.now() + timedelta(days=expiration_days)
    return UrgentAlert(content=content, expiration_date=expiration_date, targeted_user=targeted_user)

@pytest.fixture
def user1():
    return User("test_user1")

@pytest.fixture
def user2():
    return User("test_user2")


@pytest.fixture
def topic1():
    return Topic("test_topic1")

@pytest.fixture
def topic2():
    return Topic("test_topic2")

@pytest.fixture
def informative_alert():
    return create_informative_alert("Informative alert")

@pytest.fixture
def urgent_alert():
    return create_urgent_alert("Urgent alert", expiration_days=1)


@pytest.fixture
def urgent_alert2():
    return create_urgent_alert("Urgent alert 2", expiration_days=1)

@pytest.fixture
def expired_alert():
    return create_informative_alert("Expired Informative alert", expiration_days=-1)


@pytest.fixture
def targeted_user1_alert(user1):
    return create_informative_alert("Informative alert for user1", targeted_user=user1)




class TestUser:

    def test_user_subscribe_to_topic(self, user1, topic1):
        user1.subscribe_to_topic(topic1)
        assert user1 in topic1.subscribers

    def test_user_update_alert(self, user1, informative_alert):
        user1.update(informative_alert)

        assert len(user1.get_alerts()) == 1
        assert user1.get_alerts()[0] == informative_alert
        assert user1.alert_read_status[informative_alert] == False

    def test_user_mark_alert_as_read(self, user1, informative_alert):
        user1.update(informative_alert)
        user1.read_alert(informative_alert)

        assert user1.alert_read_status[informative_alert] == True

    def test_user_get_unread_unexpired_alerts(self, user1, informative_alert, expired_alert):
        user1.update(informative_alert)
        user1.update(expired_alert)

        unread_unexpired_alerts = user1.get_unread_unexpired_alerts()

        assert len(unread_unexpired_alerts) == 1
        assert unread_unexpired_alerts[0] == informative_alert

    def test_user_alert_order(self, user1, informative_alert, urgent_alert, urgent_alert2):
        user1.update(urgent_alert)
        user1.update(informative_alert)
        user1.update(urgent_alert2)

        alerts = user1.get_alerts()

        assert alerts[0] == urgent_alert2
        assert alerts[2] == informative_alert


class TestTopic:

    def test_topic_notify_all_users(self, user1, user2, topic1, informative_alert):
        topic1.subscribe(user1)
        topic1.subscribe(user2)

        topic1.notify(informative_alert)

        assert informative_alert in user1.get_alerts()
        assert informative_alert in user2.get_alerts()

    def test_topic_notify_targeted_user(self, user1, user2, topic1, targeted_user1_alert):
        topic1.subscribe(user1)
        topic1.subscribe(user2)

        topic1.notify(targeted_user1_alert)

        assert targeted_user1_alert in user1.get_alerts()
        assert targeted_user1_alert not in user2.get_alerts()

    def test_topic_get_non_expired_alerts(self, topic1, informative_alert, expired_alert, urgent_alert):
        topic1.add_alert(informative_alert)
        topic1.add_alert(expired_alert)
        topic1.add_alert(urgent_alert)
        
        non_expired_alerts = topic1.get_non_expired_alerts()

        assert len(non_expired_alerts) == 2
        assert non_expired_alerts[0] == urgent_alert

    def test_topic_does_not_notify_non_subscribed_user(self, user1, user2, topic1, targeted_user1_alert):
        topic1.subscribe(user2)

        topic1.notify(targeted_user1_alert)

        assert targeted_user1_alert not in user1.get_alerts()



class TestAlerts:

    def test_informative_alert_initialization(self, informative_alert):
        assert informative_alert.get_type() == "Informative"
        assert not informative_alert.is_expired()

    def test_urgent_alert_initialization(self, urgent_alert):
        assert urgent_alert.get_type() == "Urgent"
        assert not urgent_alert.is_expired()

    def test_informative_alert_expiration(self, expired_alert):
        assert expired_alert.is_expired()

    def test_urgent_alert_expiration(self, urgent_alert):
        assert not urgent_alert.is_expired()