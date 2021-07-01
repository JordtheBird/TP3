class Compte():
    def __init__(self, numero, solde = 0.0):
        self.numero = numero
        self.solde = solde

    def deposer(self, montant):
        """ 
            Dépose un montant d'argent dans le compte

            Args:
                montant (float): Le montant d'argent déposé dans le compte.
        """
        self.solde += montant

    def retirer(self, montant):
        """ 
            Retire un montant d'argent du compte

            Args:
                montant (float): Le montant d'argent retiré du compte.
        """
        self.solde -= montant
    
class CompteSansDette(Compte):
    """
        Un compte de banque pour lequel il est impossible d'avoir un solde négatif

        Attributs:
            numero (int): Le numéro de compte
            solde (float): Le montant d'argent dans le compte
    """

    def __init__(self, numero):
        """ 
            Constructeur de la classe CompteSansDette. Reçoit un numéro de compte en argument, 
            et initialise le solde à 0.00$

            Args:
                numero (int): Le numéro de compte
        """
        super().__init__(numero)

    def retirer(self, montant):
        """ 
            Retire un montant d'argent du compte. Lance une exception si le solde est insuffisant.

            Args:
                montant (float): Le montant d'argent retiré du compte.
        """
        if self.solde < montant:
            raise Exception("Erreur de retrait: Le solde ne peut pas être négatif")

class Client:
    def __init__(self, nom):
        """
            Constructeur de la classe Client. Reçoit le nom du client, et initialise le dictionnaire de comptes
            
            Args:
                nom (str): Le nom du client
        """
        self.nom = nom
        self.comptes = {}

    def ajouter_compte(self, numero):
        """
            Ajoute un compte au client
            
            Args:
                numero (int): Numéro de compte qui sera ajouté au dictionnaire des comptes
        """
        self.comptes[numero] = Compte(numero)
    
    def deposer_dans_compte(self, numero_de_compte, montant):
        """
            Dépose un montant d'argent dans le compte du client.

            Args:
                numero (int): Numéro du compte dans lequel on veut faire le dépot
                montant (float): Montant d'argent à déposer
        """
        self.comptes[numero_de_compte].deposer(montant)

    def retirer_dans_compte(self, numero_de_compte, montant):
        self.comptes[numero_de_compte].retirer(montant) # self.comptes[numero_de_compte] est un objet de type compte. On peut utiliser la méthode de cette classe retirer() ou déposer()
    
    def lister_soldes_comptes(self):
        """
            Affiche le nom du client, le numéro et le solde de chacun de ses comptes
        """
        print("Client: {}".format(self.nom))
        for compte in self.comptes.values():
            print("Compte {}: {:6.2f}".format(compte.numero, compte.solde))

class Banque:
    """
        Banque avec plusieurs clients
        
        Attributs:
            clients (list): Une liste des clients de la banque
    """
    def __init__(self):
        """
            Constructeut de la classe Banque. Initialise l'attribut clients
        """
        self.clients = []
    
    def ajouter_client(self, client):
        """
            Ajoute un client à la liste de la banque.
            
            Args:
                client (Client): Le client à ajouter à la liste
        """
        self.clients.append(client)

    def recuperer_client(self, nom):
        """
            Récupère les informations du client de la banque via son nom
            
            Args:
                nom (str): Le nom du client
            
            Returns:
                Client: L'objet Client associée à ce nom si il existe. 
                Autrement, return None.
        """
        for client in self.clients:
            if client.nom == nom:
                return client
        return None

    def lister_clients_et_comptes(self):
        """
            Affiche la liste des clients et l'information de leurs comptes.
        """
        for client in self.clients:
            client.lister_soldes_comptes()
            print()

if __name__ == "__main__":
    client_1 = Client("Jordan")
    client_1.ajouter_compte(1010)
    client_1.ajouter_compte(1111)
    client_1.deposer_dans_compte(1010, 1000)
    client_1.deposer_dans_compte(1111, 1869)
    client_1.retirer_dans_compte(1010, 250)

    client_2 = Client("Alix")
    client_2.ajouter_compte(1707)
    client_2.deposer_dans_compte(1707, 500)
    
    banque = Banque()
    banque.ajouter_client(client_1)
    banque.ajouter_client(client_2)
    banque.lister_clients_et_comptes()