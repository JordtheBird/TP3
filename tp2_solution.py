import datetime
import math
import textwrap

LIMITE_MINIMUM_D_AGE_PAR_CLASSEMENT = {
    # pour regarder un film ou une série d'une catégorie, votre âge doit être supérieur à la limite.
    "TV-Y": 0,          # Le programme est évalué comme étant approprié aux enfants.
    "TV-Y7": 7,         # Le programme est destiné aux enfants âgés de 7 ans et plus.
    "TV-Y7-FV": 7,      # Le programme est destiné aux enfants âgés de 7 ans et plus.
    "TV-G": 10,         # La plupart des parents peuvent considérer ce programme comme approprié pour les enfants.
    "TV-PG": 14,        # Contient des éléments que les parents peuvent considérer inappropriés pour les enfants
    "TV-14": 14,        # Contient des éléments pouvant être inappropriés pour les enfants de moins de 14 ans
    "TV-MA": 17,        # Uniquement réservé aux adultes et inapproprié pour la jeune audience de moins de 17 ans.

    "G": 0,             # Tous les âges sont admis. Rien qui offenserait les parents pour le visionnage par les enfants.
    "PG": 7,            # Certains matériaux peuvent ne pas convenir aux jeunes enfants
    "PG-13": 13,        # Certains contenus peuvent ne pas convenir aux enfants de moins de 13 ans.
    "R": 17,            # Les moins de 17 ans doivent être accompagnés d'un parent ou d'un tuteur adulte.
    "NC-17": 18,        # Personne de 17 ans et moins admis. Clairement adulte. Les enfants ne sont pas admis.
    "NR": 13,           # Non-rated donc par défaut, il doit être considéré comme PG-13
    "UR": 13,           # Unrated donc par défaut, il doit être considéré comme PG-13
    "": 13,             # Si la valeur est manquante, donc par défaut, il doit être considéré comme PG-13
}


def afficher_menu_et_choisir_action():
    """
    Fonction permettant d'afficher le menu des choix disponibles
    et récupérer le choix de l'utilisateur.
    
    Returns:
        int: Le choix de l'utilisateur (une valeur entière entre 1 et 7).
    """
    choix_menu = None
    while choix_menu is None:
        try:
            print("Menu")
            print("1 - Rechercher des films ou séries avec une expression")
            print("2 - Rechercher des films ou séries selon le genre")
            print("3 - Rechercher des films ou séries selon les acteurs")
            print("4 - Afficher la médiathèque par ordre des shows les plus récemment ajoutés")
            print("5 - Afficher la médiathèque par ordre des shows les plus populaires")
            print("6 - Afficher la médiathèque par ordre des shows les mieux évalués")
            print("7 - Quitter l'application")
            choix_menu = int(input("Veuillez entrer votre choix: "))
            assert 1 <= choix_menu <= 7
        except (ValueError, AssertionError):
            print("Votre choix n'est pas dans la liste des options. Veuillez réessayer.")
            choix_menu = None
    return choix_menu


def demander_informations_utilisateur():
    """
    Fonction permettant de récupérer les informations de l'utilisateur.
    
    Returns:
        dict: Un dictionnaire contenant l'ensemble des informations
              de l'utilisateur (nom, âge, pays, abonnement).
    """
    nom = input("Veuillez entrer votre nom d'utilisateur: ").lower()

    age = None
    while age is None:
        try:
            age = int(input("Veuillez entrer votre âge: "))
            assert age >= 0
        except (ValueError, AssertionError):
            print("Votre âge doit être un entier positif.")
            age = None

    pays = input("Veuillez entrer votre pays: ").lower()

    abonnement = None
    while abonnement is None:
        try:
            abonnement = int(input("Veuillez entrer votre type d'abonnement - 1 [régional] ou 2 [international]: "))
            assert abonnement in [1, 2]
        except (ValueError, AssertionError):
            print("Le type d'abonement doit être 1 pour régional ou 2 pour international.")
            abonnement = None
    return dict(nom=nom, age=age, pays=pays, abonnement=abonnement)


def convertir_ligne_en_show(ligne, ligne_des_titres):
    """
    Fonction permettant de convertir une chaîne de caractères représentant un show
    en un dictionnaire représentant un show (i.e un dictionnaire avec les bons types).
    Notez que les clés du dictionnaire sont fournies par le paramètre ligne_des_titres,
    les valeurs sont fournies par le paramètre ligne et le séparateur des éléments
    de la ligne est '|'.

    Args:
        ligne (str): La ligne à convertir en un dictionnaire show. 
        ligne_des_titres (str): La première ligne contenant l'ensemble des titres. 
    
    Returns:
        dict: Un dictionnaire représentant le show.
    """
    res = {cle: valeur for cle, valeur in zip(ligne_des_titres.split("|"), ligne.split("|"))}
    res["acteurs"] = [] if len(res["acteurs"]) == 0 else res["acteurs"].split(", ")
    res["pays"] = res["pays"].split(", ")
    res["directeurs"] = [] if len(res["directeurs"]) == 0 else res["directeurs"].split(", ")
    res["categories"] = [] if len(res["categories"]) == 0 else res["categories"].split(", ")
    res["popularite"] = float(res["popularite"])
    res["note"] = float(res["note"])
    res["annee_sortie"] = int(res["annee_sortie"])
    date = res["date_ajout"] if (res["date_ajout"] != "") else "January 1, 2000"
    # La chaîne de format "%B %d, %Y" équivaut à des dates sous la forme "August 14, 2020"
    res["date_ajout"] = datetime.datetime.strptime(date.strip(), "%B %d, %Y")
    return res


def afficher_details_du_show(show):
    """
    Fonction permettant d'afficher toutes les informations relatives
    à un show.

    Args:
        show (dict): Un dictionnaire représentant le show.
    """
    sdate = "Ajouté le " + show["date_ajout"].strftime("%d %B %Y")
    pop = f"Note: [{show['note']:.1f}/10] Popularité: {show['popularite']:.1f}"
    s = f"""
    {show["type"]:<10s} - {show["titre"]:>50s} ({show["langue"].upper()}) {pop:>100s}
    Année: {str(show["annee_sortie"]):<10s} Durée: {show["duree"]:<10s} {sdate:>130s}
    Synopsis: {textwrap.shorten(show["description"], width=150, placeholder="..."):<}
    Acteurs: {"Inconnus" if len(show["acteurs"]) == 0 else ", ".join(show["acteurs"]):<50s} 
    Directeurs: {"Inconnus" if len(show["directeurs"]) == 0 else ", ".join(show["directeurs"]):<50s}
    """
    print(s)


def charger_mediatheque(nom_fichier):
    """
    Cette fonction permet de lire et charger en mémoire la médiathèque.
    Elle retourne un dictionnaire où chaque clé représente l'id d'un show
    et la valeur associée représente un show.
    Vous devez impérativement utiliser la fonction convertir_ligne_en_show.

    Args:
        nom_fichier (str): Le chemin menant au fichier contenant la médiathèque.

    Returns:
        dict: Dictionnaires des shows de la médiathèque. Les clés sont des show_ids et les valeurs sont des shows.
    """
    mediatheque = {}

    with open(nom_fichier) as fichier:
        ligne_des_titres, *lignes_des_shows = [ligne.strip() for ligne in fichier]

        for ligne in lignes_des_shows:
            show = convertir_ligne_en_show(ligne, ligne_des_titres)
            mediatheque[show['show_id']] = show

    return mediatheque


def afficher_mediatheque(mediatheque, nombre_de_shows_par_page=10, attribut_pour_trier="date_ajout"):
    """
    Fonction permettant d'afficher l'ensemble des shows présents dans la
    médiathèque fournie en entrée. Cette fonction offre la pagination de l'affichage s'il y a trop de show dans la médiathèque.

    Args:
        mediathèque (dict): Médiathèque à afficher.
        nombre_de_shows_par_page (int, optional): Nombre de shows à afficher par page. La valeur par défaut est de 10.
        attribut_pour_trier (str): Attribut de tri.
    """
    nb_pages = int(math.ceil(len(mediatheque) / nombre_de_shows_par_page))
    show_ids = trier_ids_par_attribut(mediatheque, attribut_pour_trier)
    i = 0
    while i < nb_pages:
        print(f"Page: {i+1} sur {nb_pages}")
        for j in range(i*nombre_de_shows_par_page, min(len(show_ids), (i+1)*nombre_de_shows_par_page)):
            afficher_details_du_show(mediatheque[show_ids[j]])
        print(f"Page: {i+1} sur {nb_pages}")
        choix = input("Entrer s [page suivante], p [page précédente], q [quitter]: ")
        if choix.lower() == "s":
            if i < nb_pages - 1:
                i += 1
        elif choix.lower() == "p":
            if i > 0:
                i -= 1
        else:
            break

def filtrer_ids_sur_attribut_par_inclusion_de_string(mediatheque, attribut, valeur):
    """
    Fonction permettant de récupérer uniquement les ids des shows de la médiathèque 
    où la valeur de l'attribut passé en argument contient la valeur passée en argument. Notez que le filtre doit être insensible à la casse.

    Args:
        mediathèque (dict): Médiathèque à filtrer.
        attribut (str): Attribut de filtre
        valeur (str): Valeur de filtre.

    Returns:
        list: Liste des show_ids respectant les critères du filtre.
    """
    val = valeur.lower() if isinstance(valeur, str) else valeur
    return [show_id for show_id, show in mediatheque.items() if val in show[attribut].lower()]


def filtrer_ids_sur_attribut_par_inclusion_de_liste_de_string(mediatheque, attribut, valeur):
    """
    Fonction permettant de récupérer uniquement les shows de la médiathèque 
    où la valeur de l'attribut passé en argument contient la valeur passée en argument.
    Cette fonction est différente de la précédente dans le sens où la valeur de l'attribut contient des liste de chaine de charactères. Notez que le filtre doit être insensible à la casse.

    Args:
        mediathèque (dict): Médiathèque à filtrer.
        attribut (str): Attribut de filtre
        valeur (str): Attribut de filtre.

    Returns:
        list: Liste des show_ids respectant les critères du filtre.
    """
    val = valeur.lower() if isinstance(valeur, str) else valeur
    return [show_id for show_id, show in mediatheque.items() if any([val in p.lower() for p in show[attribut]])]


def filtrer_ids_sur_age(mediatheque, age):
    """
    Fonction permettant de récupérer uniquement les shows de la médiathèque 
    où la limite d'âge est respectée (i.e des shows où le classement permet à l'utilisateur de regarder). 
    Vous devez donc utiliser le dictionnaire LIMITE_MINIMUM_D_AGE_PAR_CLASSEMENT ci-dessus et l'attribut "classement" des shows.

    Args:
        mediathèque (dict): Médiathèque à filtrer.
        age (int): Âge

    Returns:
        list: Liste des show_ids respectant la limite d'âge.
    """
    classements_autorises = [classement for classement, limite in LIMITE_MINIMUM_D_AGE_PAR_CLASSEMENT.items() if age >= limite]
    return [show_id for show_id, show in mediatheque.items() if show["classement"] in classements_autorises]


def trier_ids_par_attribut(mediatheque, attribut):
    """
    Fonction permettant de trier les show_ids d'une médiathèque en ordre décroissant en se basant 
    sur un attribut particulier des shows. Vous devez utiliser la fonction native sorted qui opère sur les listes.

    Args:
        mediathèque (dict): Médiathèque à filtrer.
        attribut (str): Attribut de tri

    Returns:
        list: Liste des show_ids triée en ordre décroissant  de l'attribut d'intérêt.
    """
    show_ids = list(mediatheque.keys())
    show_ids = sorted(show_ids, key=lambda show_id: mediatheque[show_id][attribut])[::-1]
    return show_ids


def lister_valeurs_uniques_par_attribut(mediatheque, attribut):
    """
    Fonction permettant de récupérer un attribut de type liste de la médiathèque. En gros, vous devez retourner les valeurs uniques contenues dans toutes les listes de cet attribut. Ces valeurs devront être triées par ordre croissant.

    Args:
        mediathèque (dict): Médiathèque à filtrer.
        attribut (str): Attribut dont le contenu devra contenir des valeurs uniques.

    Returns:
        list: Liste des valeurs unique de l'attribut de type list.
    """
    return sorted(list(set([el for show in mediatheque.values() for el in show[attribut]])))


if __name__ == '__main__':
    fichier_des_shows = "ulflix.txt"
    mediatheque_globale = charger_mediatheque(fichier_des_shows)

    print("#"*80, "###{:^74s}###".format("Bienvenue dans ULFlix"), "#"*80, sep="\n")
    print("Pour commencer, veuillez nous fournir vos renseignements de connexion.")

    utilisateur = demander_informations_utilisateur()
    selection_ids = filtrer_ids_sur_age(mediatheque_globale, utilisateur["age"])
    if utilisateur["abonnement"] == 1:
        temp = filtrer_ids_sur_attribut_par_inclusion_de_liste_de_string(mediatheque_globale, "pays", utilisateur["pays"])
        selection_ids = list(set(selection_ids).intersection(temp))
    mediatheque_utilisateur = {show_id: mediatheque_globale[show_id] for show_id in selection_ids}

    print(f"Hey {utilisateur['nom'].capitalize()}! Tu as accès à {len(mediatheque_utilisateur)} films ou séries télés.")

    continuer_programme = True
    while continuer_programme:
        choix_menu = afficher_menu_et_choisir_action()
        if choix_menu == 1: # Rechercher des films ou séries avec une expression
            recherche = input("Veuillez les termes de votre recherche: ")
            titre_ids = filtrer_ids_sur_attribut_par_inclusion_de_string(mediatheque_utilisateur,
                                                                             "titre", recherche)
            desc_ids = filtrer_ids_sur_attribut_par_inclusion_de_string(mediatheque_utilisateur,
                                                                             "description", recherche)
            selection_ids = list(set(titre_ids).union(desc_ids))
            mediatheque_recherche = {show_id: mediatheque_globale[show_id] for show_id in selection_ids}
            print(f"{len(selection_ids)} résultats trouvés")
            afficher_mediatheque(mediatheque_recherche, nombre_de_shows_par_page=10, attribut_pour_trier="popularite")
        elif choix_menu == 2: # Rechercher des films ou séries selon le genre
            genres = sorted(lister_valeurs_uniques_par_attribut(mediatheque_utilisateur, "categories"))
            print("Catégories disponibles:")
            for i, genre in enumerate(genres): print(f"{i+1:>2} - {genre}")
            choix_categorie = None
            while choix_categorie is None:
                try:
                    choix_categorie = int(input("Entrer votre choix de catégorie: "))
                    assert choix_categorie in range(1, len(genres) + 1)
                except (ValueError, AssertionError):
                    print("Le choix de catégories est invalide. Réessayer svp.")
                    choix_categorie = None
            choix_categorie = genres[choix_categorie-1]
            selection_ids = filtrer_ids_sur_attribut_par_inclusion_de_liste_de_string(mediatheque_utilisateur,
                                                                             "categories", choix_categorie)
            mediatheque_recherche = {show_id: mediatheque_globale[show_id] for show_id in selection_ids}
            print(f"{len(selection_ids)} résultats trouvés")
            afficher_mediatheque(mediatheque_recherche, nombre_de_shows_par_page=10, attribut_pour_trier="popularite")

        elif choix_menu == 3: # Rechercher des films ou séries selon les acteurs
            recherche = input("Veuillez entrer le nom ou prénom d'un acteur: ")
            selection_ids = filtrer_ids_sur_attribut_par_inclusion_de_liste_de_string(mediatheque_utilisateur, "acteurs", recherche)
            mediatheque_recherche = {show_id: mediatheque_globale[show_id] for show_id in selection_ids}
            print(f"{len(selection_ids)} résultats trouvés")
            afficher_mediatheque(mediatheque_recherche, nombre_de_shows_par_page=10, attribut_pour_trier="popularite")

        elif choix_menu == 4: # Afficher les films ou séries les plus récents
            afficher_mediatheque(mediatheque_utilisateur, nombre_de_shows_par_page=10, attribut_pour_trier="date_ajout")

        elif choix_menu == 5: # Afficher les films ou séries les plus populaires
            afficher_mediatheque(mediatheque_utilisateur, nombre_de_shows_par_page=10, attribut_pour_trier="popularite")

        elif choix_menu == 6: # Afficher les films ou séries les plus mieux évalués
            afficher_mediatheque(mediatheque_utilisateur, nombre_de_shows_par_page=10, attribut_pour_trier="note")

        else:
            continuer_programme = False
