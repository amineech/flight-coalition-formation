from datetime import date
from agents.agent import Agent
from models.personne import * 
from agents.agent import Message


class AgentAcheteur(Agent):
    def __init__(self, id: str, nom: str, personne):
        super().__init__(id, nom)
        self.personne = personne
        self.offre_courante: float = personne.strategie.offre_initiale
        self.nb_soumissions: dict = {}  # {"service_id": nb_soumissions, ...}
        self.negociation_terminee: bool = False

    def faire_offre(self, fournisseur: Agent, service):
        strategie = self.personne.strategie
        budget_max = self.personne.contraintes.budget_max
        contraintes = self.personne.contraintes
        preferences = self.personne.preferences

        if self.negociation_terminee:
            print(f"[{self.nom}] Négociation déjà terminée.")
            return

        nb = self.nb_soumissions.get(service.id, 0)
        if nb >= strategie.nb_soumissions_max:
            print(f"[{self.nom}] Nombre max de soumissions atteint pour {service.id} ({strategie.nb_soumissions_max}).")
            self.negociation_terminee = True
            return

        if date.today() > contraintes.date_limite_achat:
            print(f"[{self.nom}] Date limite d'achat dépassée. Abandon.")
            self.negociation_terminee = True
            return

        if service.compagnie in contraintes.compagnies_refusees:
            print(f"[{self.nom}] Compagnie '{service.compagnie}' refusée. Abandon.")
            self.negociation_terminee = True
            return

        if self.offre_courante > budget_max:
            print(f"[{self.nom}] Offre {self.offre_courante}€ dépasse le budget max {budget_max}€. Abandon.")
            self.negociation_terminee = True
            return

        if preferences.compagnies_preferees:
            if service.compagnie not in preferences.compagnies_preferees:
                print(f"[{self.nom}] Compagnie '{service.compagnie}' non préférée, mais on continue.")

        
        msg = Message(expediteur=self.id, destinataire=fournisseur.id, contenu={
            "type": "offre",
            "service_id": service.id,
            "prix": self.offre_courante
        })
        fournisseur.recevoir_message(msg, expediteur_agent=self)
        self.nb_soumissions[service.id] = nb + 1
        print(f"[{self.nom}] Offre envoyée : {self.offre_courante}€ (soumission {nb + 1} pour {service.id})")

    def agir(self):
        messages = self.percevoir()
        for msg in messages:
            if msg.contenu.get("type") == "reponse":
                if msg.contenu["accepte"]:
                    print(f"[{self.nom}] Offre acceptée à {self.offre_courante}€ !")
                    self.negociation_terminee = True
                else:
                    print(f"[{self.nom}] Offre refusée, je prépare une nouvelle offre.")
                    strategie = self.personne.strategie
                    self.offre_courante = strategie.calculer_prochaine_offre(self.offre_courante)
