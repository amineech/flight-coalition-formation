from dataclasses import dataclass
from datetime import date
from enum import Enum


class TypeService(Enum):
    AVION = "avion"
    TRAIN = "train"


@dataclass
class ContraintesFournisseur:
    prix_minimal: float      
    date_limite_vente: date   


@dataclass
class PreferencesFournisseur:
    date_mise_en_vente: date  


@dataclass
class Service:
    id: str
    type: TypeService
    compagnie: str
    lieu_depart: str
    lieu_arrivee: str
    date_depart: date
    date_arrivee: date
    contraintes: ContraintesFournisseur
    preferences: PreferencesFournisseur

    def __str__(self):
        return (f"[{self.type.value.upper()}] {self.compagnie} | "
                f"{self.lieu_depart} -> {self.lieu_arrivee} | "
                f"Départ: {self.date_depart} | Prix min: {self.contraintes.prix_minimal}€")
