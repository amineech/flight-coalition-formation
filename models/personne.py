from dataclasses import dataclass, field
from datetime import date


@dataclass
class ContraintesAcheteur:
    budget_max: float                              
    date_limite_achat: date                        
    compagnies_refusees: list[str] = field(default_factory=list)


@dataclass
class PreferencesAcheteur:
    compagnies_preferees: list[str] = field(default_factory=list)
    lieu_depart_prefere: str = ""
    lieu_arrivee_prefere: str = ""


@dataclass
class StrategieNegociation:
    offre_initiale: float                         
    nb_soumissions_max: int = 6                     
    taux_augmentation_max: float = 0.10            

    def calculer_prochaine_offre(self, offre_courante: float) -> float:
        """Calcule la prochaine offre selon la courbe de croissance."""
        return round(offre_courante * (1 + self.taux_augmentation_max), 2)


@dataclass
class Personne:
    id: str
    nom: str
    contraintes: ContraintesAcheteur
    preferences: PreferencesAcheteur
    strategie: StrategieNegociation

    def __str__(self):
        return (f"Personne({self.nom}) | Budget: {self.contraintes.budget_max}€ | "
                f"Limite achat: {self.contraintes.date_limite_achat} | "
                f"Offre initiale: {self.strategie.offre_initiale}€")
