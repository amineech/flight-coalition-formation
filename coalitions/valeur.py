def calculer_valeur(membres: list) -> float:
    if not membres:
        return 0.0

    # budget total de la coalition
    budgets = [m.personne.contraintes.budget_max for m in membres]
    budget_total = sum(budgets)

    # taux de réduction selon la taille (1 acheteur => 5%, 2 => 10%, 3 => 15%...)
    taux = len(membres) * 0.05

    # bonus compatibilité : pénalise si les budgets sont trop différents
    ecart = max(budgets) - min(budgets)
    bonus = 1.0 if ecart < 100 else 0.8 if ecart < 300 else 0.6


    #on peut déduire que la réduction dépend à la fois de nombre d'acheteurs avec les différences entre leurs budgets

    return round(budget_total * taux * bonus, 2)
