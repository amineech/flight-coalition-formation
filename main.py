from datetime import datetime, date
from models.service import Service, TypeService, ContraintesFournisseur, PreferencesFournisseur
from models.personne import Personne, ContraintesAcheteur, PreferencesAcheteur, StrategieNegociation
from agents.agent_fournisseur import AgentFournisseur
from agents.agent_acheteur import AgentAcheteur
from coalitions.idp import idp


def saisir_date(message: str) -> date:
    while True:
        try:
            return datetime.strptime(input(message), "%d/%m/%Y").date()
        except ValueError:
            print("Format invalide. Utilisez JJ/MM/AAAA.")


def saisir_liste(message: str) -> list[str]:
    entree = input(message).strip()
    if not entree:
        return []
    return [x.strip() for x in entree.split(",")]


def saisir_float(message: str) -> float:
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("Veuillez entrer un nombre valide.")


def saisir_int(message: str) -> int:
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Veuillez entrer un entier valide.")


def saisir_acheteur(numero: int) -> AgentAcheteur:
    print(f"\n--- Acheteur {numero} ---")
    nom                  = input("Nom : ").strip()
    budget_max           = saisir_float("Budget maximum (€) : ")
    date_limite_achat    = saisir_date("Date limite d'achat (JJ/MM/AAAA) : ")
    compagnies_refusees  = saisir_liste("Compagnies refusées (séparées par virgule, ou vide) : ")
    compagnies_preferees = saisir_liste("Compagnies préférées (séparées par virgule, ou vide) : ")
    lieu_depart_pref     = input("Lieu de départ préféré (ou vide) : ").strip()
    lieu_arrivee_pref    = input("Lieu d'arrivée préféré (ou vide) : ").strip()
    offre_initiale       = saisir_float("Offre initiale (€) : ")
    nb_soumissions_max   = saisir_int("Nombre max de soumissions : ")
    taux_augmentation    = saisir_float("Taux d'augmentation max par itération (ex: 0.10) : ")

    personne = Personne(
        id=f"P{numero}",
        nom=nom,
        contraintes=ContraintesAcheteur(
            budget_max=budget_max,
            date_limite_achat=date_limite_achat,
            compagnies_refusees=compagnies_refusees
        ),
        preferences=PreferencesAcheteur(
            compagnies_preferees=compagnies_preferees,
            lieu_depart_prefere=lieu_depart_pref,
            lieu_arrivee_prefere=lieu_arrivee_pref
        ),
        strategie=StrategieNegociation(
            offre_initiale=offre_initiale,
            nb_soumissions_max=nb_soumissions_max,
            taux_augmentation_max=taux_augmentation
        )
    )
    return AgentAcheteur(id=f"A{numero}", nom=f"Agent_{nom}", personne=personne)


# ─── Saisie du service ──────────────────────────────────────────────────────────
print("\n=== Configuration du Service ===")
type_input           = input("Type de service (avion/train) : ").strip().lower()
type_service         = TypeService.AVION if type_input == "avion" else TypeService.TRAIN
compagnie            = input("Compagnie : ").strip()
lieu_depart          = input("Lieu de départ : ").strip()
lieu_arrivee         = input("Lieu d'arrivée : ").strip()
date_depart          = saisir_date("Date de départ (JJ/MM/AAAA) : ")
date_arrivee         = saisir_date("Date d'arrivée (JJ/MM/AAAA) : ")
prix_minimal         = saisir_float("Prix minimal du service (€) : ")
date_limite_vente    = saisir_date("Date limite de vente (JJ/MM/AAAA) : ")
date_mise_en_vente   = saisir_date("Date souhaitée de mise en vente (JJ/MM/AAAA) : ")

service = Service(
    id="S1",
    type=type_service,
    compagnie=compagnie,
    lieu_depart=lieu_depart,
    lieu_arrivee=lieu_arrivee,
    date_depart=date_depart,
    date_arrivee=date_arrivee,
    contraintes=ContraintesFournisseur(prix_minimal=prix_minimal, date_limite_vente=date_limite_vente),
    preferences=PreferencesFournisseur(date_mise_en_vente=date_mise_en_vente)
)

fournisseur = AgentFournisseur(id="F1", nom=f"Agent_{compagnie}")
fournisseur.ajouter_service(service)

# Saisie des acheteurs
print("\n=== Configuration des Acheteurs ===")
nb_acheteurs = saisir_int("Nombre d'acheteurs : ")
acheteurs = [saisir_acheteur(i + 1) for i in range(nb_acheteurs)]

# Partie 1 : Négociation simultanée 
print("\n=== Partie 1 : Négociation simultanée ===\n")

while not all(a.negociation_terminee for a in acheteurs):
    # tous les acheteurs envoient leur offre en même temps
    for acheteur in acheteurs:
        if not acheteur.negociation_terminee:
            acheteur.faire_offre(fournisseur, service)

    # le fournisseur traite toutes les offres et répond à chacun
    fournisseur.agir()

    # chaque acheteur traite la réponse du fournisseur
    for acheteur in acheteurs:
        if not acheteur.negociation_terminee:
            acheteur.agir()
    print()

# Partie 2 : Coalitions via IDP 
print("\n=== Partie 2 : Formation de coalitions (IDP) ===\n")
valeur_totale, partition = idp(acheteurs)

for i, coalition in enumerate(partition, 1):
    noms = [a.nom for a in coalition]
    from coalitions.valeur import calculer_valeur
    valeur = calculer_valeur(coalition)
    reduction_par_membre = round(valeur / len(coalition), 2)
    print(f"Coalition {i} : {noms}")
    print(f"  → Valeur        : {valeur}€")
    print(f"  → Réduction/membre : {reduction_par_membre}€")
    print()

print(f"Valeur totale optimale : {valeur_totale}€")