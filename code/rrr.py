import numpy as np
import robot_arm
import random


class RRR(robot_arm.Robot_arm):
    """Classe du robot RPR, elle hérite de la classe bras de Robot;
    le robot étudié dans le BE est une instance de cette classe"""
    def __init__(self, l, k, m, n,
                 Kv=np.array([np.pi, 25, np.pi]),
                 Ka=np.array([np.pi, 25, np.pi])/0.1,
                 qmin=np.array([-3*np.pi/4, 0.0, -3*np.pi/4]),
                 qmax=np.array([3*np.pi/4, 200.0, 3*np.pi/4])):

        """Initialisation de la classe. qmin et qmax simulent les butées du robot (cette méthode marche
        bien pour les prismatiques mais est discutable pour les rotoïdes)
        ENTREE : m float, longueur O0O1
        n float, longueur O3O4
        Kv vecteur de taille 3, limite en vitesse des qi
        Kv vecteur de taille 3, limite en accélération des qi
        qmin vecteur de taille 3, min accepté pour les qi
        qmax vecteur de taille 3, max accepté pour les qi"""

        self.m = m
        self.n = n
        self.l = l
        self.k = k
        # ot_vect désique le vecteur 0304 de l'organe terminal
        self.ot_vect = np.array([[n], [0], [0]])

        # Le robot RRR est un robot avec 3 liasions
        super().__init__(3, Kv, Ka, qmin=qmin, qmax=qmax)
        
    def mgd_detail(self, q):
        """Calcule les différentes matrices élémentaires du MGD pour plus de détail
        ENTREE : q vecteur de taille 3
        SORTIE : matrice de taille 4,4"""
        
        s1 = np.sin(q[0])
        s2 = np.sin(q[1])
        s3 = np.sin(q[2])
        c1 = np.cos(q[0])
        c2 = np.cos(q[1])
        c3 = np.cos(q[2])
        
        T01 = np.zeros((4, 4))
        T12 = np.zeros((4, 4))
        T23 = np.zeros((4, 4))
        
        T01[0, :] = np.array([c1, -s1, 0, 0])
        T01[1, :] = np.array([s1, c1, 0, 0])
        T01[2, :] = np.array([0, 0, 1, self.l])
        T01[3, :] = np.array([0, 0, 0, 1])
        
        T12[0, :] = np.array([c2, -s2, 0, self.k])
        T12[1, :] = np.array([0, 0, -1, 0])
        T12[2, :] = np.array([s2, c2, 0, 0])
        T12[3, :] = np.array([0, 0, 0, 1])
        
        T23[0, :] = np.array([c3, -s3, 0, self.m])
        T23[1, :] = np.array([s3, c3, 0, 0])
        T23[2, :] = np.array([0, 0, 1, 0])
        T23[3, :] = np.array([0, 0, 0, 1])
        
        return T01, T12, T23
    
    def mgd_func(self, q):
        """Calcule la Matrice T03(q) du MGD
        ENTREE : q vecteur de taille 3
        SORTIE : matrice de taille 4,4"""

        # Variables pour alléger le code
        s1 = np.sin(q[0])
        s2 = np.sin(q[1])
        s3 = np.sin(q[2])
        c1 = np.cos(q[0])
        c2 = np.cos(q[1])
        c3 = np.cos(q[2])
        

        #Création d'une matrice 4,4 de zéros
        T03 = np.zeros((4, 4))

        # Modifications des valeurs de la matrices
        T03[0, 0] = c1*c2*c3 - c1*s2*s3
        T03[0, 1] = -c1*c2*s3 - c1*s2*c3
        T03[0, 2] = s1
        T03[0, 3] = c1*c2*self.m  + c1*self.k
        T03[1, 0] = s1*c2*c3 -s1*c2*s3
        T03[1, 1] = -s1*c2*s3 -s1*s2*c3
        T03[1, 2] = -c1
        T03[1, 3] = s1*c2*self.m + s1* self.k
        T03[2, 0] = c3*s2 +c2*s3
        T03[2, 1] = -s2*s3 +c2*c3
        T03[2, 2] = 0
        T03[2, 3] = s2*self.m+ self.l
        T03[3, 0] = 0
        T03[3, 1] = 0 
        T03[3, 2] = 0
        T03[3, 3] = 1

        return T03

    def mgi_func(self, X):
        """Implémente les équations trouvées grace au MGI. Renvoie la liste des solutions trouvée pour un X donné
        sans se soucier des butées (si il n'y a aucune solution renvoie une liste vide).
        ENTREE : X vecteur de taille 3
        SORTIE : liste de vecteurs de taille 3"""

        # Variables pour alléger le code
        n = self.n
        m = self.m
        k = self.k
        l = self.l
        x = X[0]
        y = X[1]
        z = X[2]

        # q1 se trouve directement
        q1 = np.arctan2(y,x)
        
        # Initialisation de la liste des solutions
        list_sol = []

        # Les équations sont résolues avec un + ou moins c3 donc on rajoute un eps à -1 ou 1 (il y aura donc 2 solutions maximum)
        Epsilonesin = [1, -1]

      #  c3 = ((dist(x,y) - k) **2(z - l)**2 - m**2 - n**2)/(2*m*n)
        # On parcours toutes les possiblités pour les deux épsilones
       # for epssin in Epsilonesin:
          #  q3 = np.arctan2(epssin * np.sqrt(1 - c3 **2), c3)
            #c2 = z - 
            # On ajoute le q à la liste des solutions
           # list_sol.append(np.array([q1, q2, q3]))

        return list_sol

    def X(self, q):
        """Utilise la matrice calculée par le MGD pour calculer X (position de l'organe terminal) en fonction de q
        ENTREE : q vecteur de taille 3
        SORTIE : vecteur de taille 3"""
        T = self.mgd_func(q)

        # Calcul à l'aide de la formule du cours
        return np.reshape(T[:3, 3:4] + np.matmul(T[:3, :3], self.ot_vect), (3, ))

    def Xd(self, q, qd):
        """Calcule la vitesse de l'organe terminal avec q et qd données.
        ENTREE : q vecteur de taille 3
        qd vecteur de taille 3
        SORTIE : vecteur de taille 3"""

        # Variables pour alléger le code
        n = self.n
        q1 = q[0]
        q2 = q[1]
        q3 = q[2]
        qd1 = qd[0]
        qd2 = qd[1]
        qd3 = qd[2]

        # Calcul la vitesse avec la méthode de deriver le MGD
        dx = -q2 * qd1 * np.cos(q1) + qd2 * np.sin(q1) - n*(qd3 * np.cos(q3) * np.cos(q1) + qd1 * np.sin(q1) * np.sin(q3))
        dy = q2 * qd1 * np.sin(q1) - qd2 * np.cos(q1) + n*(qd3 * np.cos(q3) * np.sin(q1) + qd1 * np.cos(q1) * np.sin(q3))
        dz = qd3 * np.sin(q3) * n

        return np.array([dx, dy, dz])

    def Xdd(self, q, qd, qdd):
        """Calcule l'accélération de l'organe terminal avec  q, qd et qdd données.
        ENTREE : q vecteur de taille 3
        qd vecteur de taille 3
        qdd vecteur de taille 3
        SORTIE : vecteur de taille 3"""

        # Variables pour alléger le code
        n = self.n
        q1 = q[0]
        q2 = q[1]
        q3 = q[2]
        qd1 = qd[0]
        qd2 = qd[1]
        qd3 = qd[2]
        qdd1 = qdd[0]
        qdd2 = qdd[1]
        qdd3 = qdd[2]

        # Calcule l'accélération avec la méthode de dériver deux fois le MGD
        xdd = -(qd2 * qd1 - q2 * qdd1) * np.cos(q1) - q2 * np.sin(q1) * (qd1 ** 2) + (
                qdd2 * np.sin(q1) - qd1 * np.cos(q1) * qd2) - n*(
            (qdd3 * np.cos(q3) + np.sin(q3) * qd3 ** 2) * np.cos(q1) + qd3 * np.cos(q3) * qd1 * np.sin(q1) + (
                    qdd1 * np.sin(q1) - np.cos(q1) * qd1 ** 2) * np.sin(q3) + qd1 * np.sin(q1) * qd3 * np.cos(q3))

        ydd = (qd2 * qd1 - q2 * qdd1) * np.sin(q1) - q2 * np.cos(q1) * qd1 ** 2 - (
                qdd2 * np.cos(q1) + qd2 * qd1 * np.sin(q1)) + n*(
            (qdd3 * np.cos(q3) + np.sin(q3) * qd3 ** 2) * np.sin(q1) + (qdd1 * np.cos(q1) + np.sin(q1) * qd1 ** 2) * np.sin(
                q3))

        zdd = (qdd3 * np.sin(q3) + np.cos(q3) * qd3 ** 2) * n
        return np.array([xdd, ydd, zdd])

    def q(self, X):
        """Calcul un q possible pour un vecteur X donné en prenant en compte les butées.
        S'il n'y a pas de solution, raise une NoSolutionExeption et renvoie None
        ENTREE : X vecteur de taille 3
        SORTIE : vecteur de taille 3 ou None si aucune solution n'est trouvée
        """

        # Récupère la liste des solutions calculées à partir du MGI
        list_sol = self.mgi_func(X)

        # Initialise la liste les solutions possibles (après implémentation des butées)
        possible_sol = []

        # On parcours les solutions
        for q in list_sol:

            # On initialise une variable qui permettra de dire si une solution est valide
            valid = True

            # Cas où il y a des limites en max et min
            if self.qmin is not None and self.qmax is not None:
                # On parcours tous les qi
                for qi, qi_min, qi_max in zip(q, self.qmin, self.qmax):
                    # Si cette égalité n'est pas vérifiée alors la solution n'est pas valide
                    if not qi_max >= qi >= qi_min:
                        valid = False

            # Même chose si il n'y a pas de limite en min
            elif self.qmin is None:
                for qi, qi_max in zip(q, self.qmax):
                    if not qi_max >= qi:
                        valid = False

            # Même chose si il n'y a pas de limite en max
            elif self.qmax is None:
                for qi, qi_min in zip(q, self.min):
                    if not qi >= qi_min:
                        valid = False

            # Si il n'y a pas de limite la solution est forcément valide
            else:
                pass

            if valid:
                # Ajoute la solition aux solutions possibles si elle est valide
                possible_sol.append(q)

        if len(possible_sol) > 0:
            # Si il y a au moins une solution possible renvoie une solution au hasard
            # (on peut aussi renvoyer la première solution possible)
            return random.choice(possible_sol)
        else:
            # Si on a pas trouvé de solution on raise une NoSolutionException et on renvoie None
            raise robot_arm.NoSolutionException()
            return None

    def qd(self, Xd, q):
        # Variables pour alléger le code
        q1 = q[0]
        q2 = q[1]
        q3 = q[2]
        dx = Xd[0]
        dy = Xd[1]
        dz = Xd[2]
        n = self.n

        # On implémente le MGI trouvé en trouvant les dqi en fontion des dx et qi grace à matlab

        qd1 = -(dz * n * np.cos(q3) * np.cos(q1) ** 2 - n * q1 * np.cos(q1) * np.sin(q1) * np.sin(q3) ** 2 + dx *
                np.cos(q1) * np.sin(q3) - dz * n * np.cos(q3) * np.sin(q1) ** 2 + dy * np.sin(q1) * np.sin(q3)) / (
                np.sin(q3) * (q2 * np.cos(q1) ** 2 + n * np.sin(q3) * np.cos(q1) * np.sin(q1) - q2 * np.sin(q1) ** 2))

        qd2 = -(- q1 * n ** 2 * np.cos(q1) * np.sin(q1) * np.sin(q3) ** 2 - dz * np.cos(q3) * n ** 2 * np.sin(q1) ** 2 -
                q1 * q2 * n * np.cos(q1) ** 2 * np.sin(q3) + dy * n * np.sin(q1) * np.sin(q3) + dy * q2 * np.cos(q1) +
                dx * q2 * np.sin(q1)) / (q2 * np.cos(q1) ** 2 + n * np.sin(q3) * np.cos(q1) * np.sin(q1) -
                q2 * np.sin(q1) ** 2)

        qd3 = dz / (np.sin(q3)*n)

        # S'il y a nan parmis les dqi cela signifie qu'il n'y a pas de solution.
        if np.nan in np.array([qd1, qd2, qd3]):
            raise robot_arm.NoSolutionException()

        return np.array([qd1, qd2, qd3])

