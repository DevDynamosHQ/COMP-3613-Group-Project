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


class AppliedState(ApplicationState):

    def shortlist(self, application):
        application._state = ShortlistedState()
        return True

    def accept(self, application):
        raise ValueError("Cannot accept an application that hasn't been shortlisted.")
    
    def reject(self, application):
        raise ValueError("Cannot reject an application that hasn't been shortlisted.")
    
    def can_shortlist(self):
        return True
    
    def can_accept(self):
        return False
    
    def can_reject(self):
        return False
    
    def get_state_name(self):
        return "applied"


class ShortlistedState(ApplicationState):

    def shortlist(self, application):
        raise ValueError("Application is already shortlisted.")


    def accept(self, application):
        application._state = AcceptedState()
        return True


    def reject(self, application):
        application._state = RejectedState()
        return True


    def can_shortlist(self):
        return False


    def can_accept(self):
        return True


    def can_reject(self):
        return True


    def get_state_name(self):
        return "shortlisted"


