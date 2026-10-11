from agents.agent import Agent, Message


class AgentFournisseur(Agent):
    def __init__(self, id: str, nom: str):
        super().__init__(id, nom)
        self.services: list = []
        self.boite_reception: dict = {}      # {"A1": [msg1], "A2": [msg1], ...}
        self.acheteurs_connus: dict = {}     # {"A1": agent_acheteur, ...}

    def ajouter_service(self, service):
        self.services.append(service)

    def recevoir_message(self, message: Message, expediteur_agent=None):
        """Stocke le message dans la boîte de l'acheteur correspondant."""
        if message.expediteur not in self.boite_reception:
            self.boite_reception[message.expediteur] = []
        self.boite_reception[message.expediteur].append(message)
        if expediteur_agent:
            self.acheteurs_connus[message.expediteur] = expediteur_agent

    def evaluer_offre(self, service_id: str, prix_propose: float) -> bool:
        for service in self.services:
            if service.id == service_id:
                return prix_propose >= service.contraintes.prix_minimal
        return False

    def agir(self):
        """Traite les offres de chaque acheteur et envoie une réponse."""
        for acheteur_id, messages in self.boite_reception.items():
            for msg in messages:
                if msg.contenu.get("type") == "offre":
                    service_id = msg.contenu["service_id"]
                    prix = msg.contenu["prix"]
                    accepte = self.evaluer_offre(service_id, prix) # la réponse
                    print(f"[{self.nom}] Offre de {acheteur_id} : {prix}€ -> {'ACCEPTÉE' if accepte else 'REFUSÉE'}")

                    # répondre à l'acheteur
                    if acheteur_id in self.acheteurs_connus:
                        acheteur = self.acheteurs_connus[acheteur_id]
                        reponse = Message(
                            expediteur=self.id,
                            destinataire=acheteur_id,
                            contenu={"type": "reponse", "accepte": accepte}
                        )
                        acheteur.recevoir_message(reponse)

        self.boite_reception.clear()
