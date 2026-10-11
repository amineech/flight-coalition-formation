from itertools import combinations
from models.coalition import Coalition
from coalitions.valeur import calculer_valeur


def generer_coalitions(agents: list) -> list[Coalition]:
    """Génère toutes les coalitions possibles à partir d'une liste d'agents."""
    toutes = []
    compteur = 1

    for taille in range(1, len(agents) + 1):
        for combo in combinations(agents, taille):
            membres = list(combo)
            valeur = calculer_valeur(membres)
            coalition = Coalition(id=f"C{compteur}", membres=membres, valeur=valeur)
            toutes.append(coalition)
            compteur += 1

    return toutes
