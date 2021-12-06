import numpy as np


def movement_law_func(qa, qb, qda=np.array([0.0, 0.0, 0.0]), qdb=np.array([0.0, 0.0, 0.0]),
                      qdda=np.array([0.0, 0.0, 0.0]), qddb=np.array([0.0, 0.0, 0.0]),
                      Ka=np.array([0,0,0]), Kv=np.array([0,0,0]), Te=5e-3, tfmax = 100.):
    """Calcul les différents q, qd, qdd entre qa et qb, qda et qdb, qdda, et qddb
    qui satisfont la loi de mouvement. (Pour le BE nous n'avons pas besoin de qdda et qddb)
    ENTREE : qa, qb, qda, qdb, qdda, qddb, Ka, Kv vecteurs de taille (m étant le nombre de qi)
    Te, tfmax float
    SORTIE : n-uplet (t, qs, qds, qdds)
    t vecteur de taille n
    qs, qds, qdds vecteurs de taille (m, n) (m étant le nombre de qi)
    """

    # Pour trouver un tf optimal, on initialise tf puis on calcul les q, qd et qdd, si les limites Ka ou Kv sont
    # dépassées alors on recommence le calcul en prenant un tf plus grand jusqu'à trouver le premier tf qui
    # nous permette de respecter les limites Kv et Ka.
    tf = 0.1
    condition = False
    # On initialise les listes qui vont contenir les q, qd, qdd
    list_q = []
    list_qd = []
    list_qdd = []
    # On répète l'opération tant que tous les q, qd, qdd ne sont pas inférieurs aux limites
    while not condition and tf < tfmax:
        # On calcul un vecteur de temps de 0 à tf en prenant des points en fonction de Te
        t = np.linspace(0, tf, int((1/Te) * tf))

        # On vide les listes
        list_q = []
        list_qd = []
        list_qdd = []

        # On parcours les qi
        for x, (qia, qib, qdia, qdib, Kiv, Kia) in enumerate(zip(qa, qb, qda, qdb, Kv, Ka)):

            # On applique la méthode vue en cours
            a0 = qia
            a1 = qdia
            a2 = 0
            a3 = (12 * qia - 12 * qib + 9 * qdia * tf + 3 * qdib * tf + 10 * qia * tf ** 2 - 10 * qib * tf ** 2 + 6 * qdia * tf ** 3 + 4 * qdib * tf ** 3) / (tf ** 3 * (2 * tf ** 2 - 3))
            a4 = -((10 * tf ** 2 + 3) * (3 * qia - 3 * qib + 2 * qdia * tf + qdib * tf)) / (tf ** 4 * (2 * tf ** 2 - 3))
            a5 = -(6 * (3 * qia - 3 * qib + 2 * qdia * tf + qdib * tf)) / (tf ** 2 * (- 2 * tf ** 3 + 3 * tf))

            # On calcul la position, vitesse et acceleration pour chaque qi
            # Au lieu de caluler chaque point un par un on utilise les fonctionnalités de Numpy sur les vecteurs
            # Numpy accepte la multiplication de vecteur par in scalaire et une puissance de vecteur
            f = a0 + a1*t + a2 * t**2 + a3 * t**3 + a4 * t**4 + a5 * t**5
            v = a1 + 2*a2*t + 3*a3*t**2 + 4*a4 * t**3 + 5 * a5 * t**4
            a = 2*a2 + 6*a3*t + 12 * a4*t**2 + 20 * a5 * t**3
            # Si à un moment on dépasse les limites en vitesses ou on en position on arrete la boucle for
            # et on incrémente tf pour essayer de rentrer dans les limites
            if np.max(v) > Kiv or np.max(a) > Kia or abs(np.min(v)) > Kiv or abs(np.min(a)) > Kia:
                tf += 0.1
                break
            # On ajoute les vecteurs à leurs listes respectives
            list_q.append(f)
            list_qd.append(v)
            list_qdd.append(a)
        else:
            condition = True

    if tf > tfmax:
        print("Le robot met trop de temps à rejoindre son objectif, impossible de trouver un tf acceptable.")

    # On renvoie tout et on transforme list_q, list_qd, list_qdd en vecteurs de taille (m, n) (m étant le nombre de qi)
    # et n étant de nombre de points
    return t, np.stack(list_q), np.stack(list_qd), np.stack(list_qdd)

