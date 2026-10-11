from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Message:
    expediteur: str
    destinataire: str
    contenu: dict


class Agent(ABC):
    def __init__(self, id: str, nom: str):
        self.id = id
        self.nom = nom
        self.boite_reception: list[Message] = []

    def envoyer_message(self, destinataire: 'Agent', contenu: dict):
        msg = Message(expediteur=self.id, destinataire=destinataire.id, contenu=contenu)
        destinataire.recevoir_message(msg)

    def recevoir_message(self, message: Message):
        self.boite_reception.append(message)

    def percevoir(self) -> list[Message]:
        """Lecture des messages de la boîte de réception..."""
        messages = self.boite_reception.copy()
        self.boite_reception.clear()
        return messages

    @abstractmethod
    def agir(self):
        pass
