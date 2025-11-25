from abc import ABC, abstractmethod

class ApplicationState(ABC):

    @abstractmethod
    def shortlist(self, application):
        pass

    @abstractmethod
    def accept(self, application):
        pass

    @abstractmethod
    def reject(self, application):
        pass

    @abstractmethod
    def can_shortlist(self):
        pass

    @abstractmethod
    def can_accept(self):
        pass

    @abstractmethod
    def can_reject(self):
        pass

    @abstractmethod
    def get_state_name(self):
        pass

