from abc import abstractmethod
from Capacity import Capacity

class EventCapacity(Capacity) :
    """
        Capacité permettant à l'agent d'envoyer et de recevoir des événements
        dans les espaces auxquels il participe.
    """
    def __init__(self,owner=None) :
        
        super().__init__(owner)
    
    @abstractmethod
    def emit(self, event)-> None :
        """
                Diffuse un événement dans l'espace par défaut de l'agent.
                :param event: L'instance de l'événement à diffuser.
        """
        pass
    
    @abstractmethod
    def receive(self,event)-> None :
        """ Traite un événement reçu. """
        pass
    
    @abstractmethod
    def wake(self, event)-> None :
        """
                Réveille les comportements (Behaviors) de l'agent qui attendent
                cet événement spécifique.
                """
        pass