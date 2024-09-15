from abc import ABC, abstractmethod

class AlertInsertionStrategy(ABC):
    @abstractmethod
    def insert_alert(self, alert: 'Alert', alert_list: list['Alert']) -> None:
        pass



class LIFOAlertInsertionStrategy(AlertInsertionStrategy):
    def insert_alert(self, alert: 'Alert', alert_list: list['Alert']) -> None:
        alert_list.insert(0, alert)


class FIFOAlertInsertionStrategy(AlertInsertionStrategy):
    def insert_alert(self, alert: 'Alert', alert_list: list['Alert']) -> None:
        alert_list.append(alert)