from itertools import combinations
from coalitions.valeur import calculer_valeur


def idp(agents: list) -> tuple[float, list[list]]:
    """
    Trouve la partition optimale des agents via programmation dynamique.
    Retourne la valeur totale maximale et la liste des coalitions optimales.
    """
    n = len(agents)
    # on représente chaque sous-ensemble par un frozenset d'indices
    memo = {}  # frozenset d'indices → (meilleure valeur, meilleure partition)

    def best(indices: frozenset):
        if indices in memo:
            return memo[indices]

        membres = [agents[i] for i in indices]
        valeur_ensemble = calculer_valeur(membres)

        meilleure_valeur = valeur_ensemble
        meilleure_partition = [membres]

        # essayer tous les découpages en deux sous-groupes non vides
        indices_list = list(indices)
        for taille in range(1, len(indices_list) // 2 + 1):
            for combo in combinations(indices_list, taille):
                C1 = frozenset(combo)
                C2 = indices - C1
                if not C2:
                    continue
                val_C1, part_C1 = best(C1)
                val_C2, part_C2 = best(C2)
                if val_C1 + val_C2 > meilleure_valeur:
                    meilleure_valeur = val_C1 + val_C2
                    meilleure_partition = part_C1 + part_C2

        memo[indices] = (meilleure_valeur, meilleure_partition)
        return memo[indices]

    tous_indices = frozenset(range(n))
    valeur_totale, partition_optimale = best(tous_indices)
    return valeur_totale, partition_optimale
