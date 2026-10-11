from dataclasses import dataclass, field


@dataclass
class Coalition:
    id: str
    membres: list        # liste d'AgentAcheteur
    valeur: float = 0.0  # réduction obtenue ensemble

    def __str__(self):
        noms = [m.nom for m in self.membres]
        return f"Coalition({noms}) → valeur: {self.valeur}"
