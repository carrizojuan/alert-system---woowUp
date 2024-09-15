from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

class Alert(ABC):
    def __init__(self, insertion_strategy, content: str, expiration_date: Optional[datetime] = None, targeted_user: Optional['User'] = None):
        self.content = content
        self.expiration_date = expiration_date
        self.targeted_user = targeted_user
        self.insertion_strategy = insertion_strategy

    def is_expired(self) -> bool:
        if self.expiration_date is None:
            return False
        return datetime.now() > self.expiration_date

    def is_for_all_users(self) -> bool:
        return self.targeted_user is None

    @abstractmethod
    def get_type(self) -> str:
        pass


class InformativeAlert(Alert):
    def __init__(self, content: str, expiration_date: Optional[datetime] = None, targeted_user: Optional['User'] = None):
        from .strategies import FIFOAlertInsertionStrategy
        super().__init__(FIFOAlertInsertionStrategy(), content, expiration_date, targeted_user)

    def get_type(self) -> str:
        return "Informative"


class UrgentAlert(Alert):
    def __init__(self, content: str, expiration_date: Optional[datetime] = None, targeted_user: Optional['User'] = None):
        from .strategies import LIFOAlertInsertionStrategy
        super().__init__(LIFOAlertInsertionStrategy(), content, expiration_date, targeted_user)

    def get_type(self) -> str:
        return "Urgent"