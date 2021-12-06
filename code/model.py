import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation


class Model:
    """Classe qui lie le robot avec la loi de mouvement"""
    def __init__(self, robot_arm, movement_law, Te=10e-3):
        """"""
        self.robot_arm = robot_arm
        self.movement_law = movement_law
        self.Te = Te

    def trajectory(self, qs, qds, qdds):
        """Calcule la liste des X, Xd, Xdd qui correspondent à la liste des q, qd, qdd grace au MGD et MDD du robot
        ENTREE : qs, qds, qdds, vecteurs de taille (m, n) m étant le nombre de qi
        SORTIE : X, Xd, Xdd, vecteurs de taille (n, 3)"""

        # Initialisation des listes de position, vitesse et accélération
        list_X = []
        list_Xd = []
        list_Xdd = []
        for q, qd, qdd in zip(qs.T, qds.T, qdds.T):

            # On calcul chaque vecteur X, Xd, Xdd et on les ajoute à la liste
            list_X.append(self.robot_arm.X(q))
            list_Xd.append(self.robot_arm.Xd(q, qd))
            list_Xdd.append(self.robot_arm.Xdd(q, qd, qdd))

        # On renvoie les listes de vecteurs qu'on transforme en vecteurs de taille (n, 3)
        return np.stack(list_X), np.stack(list_Xd), np.stack(list_Xdd)

    def trois_points(self, Xa, Xb, Xdb, Xc):
        """Fonction principale : Calcul une trajectoire pour le robot qui passe par les points Xa, Xb, Xc
        avec une vitesse Xdb en Xb
        ENTREE: 3 vecteurs de position et un vecteur vitesse pour le point intermédiaire
        SORTIE:
        Si le model trouve au moins une solution pour chaque entrée :
        - Affiche les valeurs des q, qd, qdd, et X, Xd, Xdd pour toute la trajectoire
        - Affiche la trajectoire du robot en 3d avec une petite animation sympahique
        - return True
        Sinon :
        - return False et print une erreur"""

        try: # Le système peut ne pas trouver de solution et raise une Exception
            # On calcule les qa, qb, qc correspondants aux Xa, Xb, Xc
            qa = self.robot_arm.q(Xa)
            qb = self.robot_arm.q(Xb)
            qc = self.robot_arm.q(Xc)

            # On calcule le qdb correspondant au Xdb. Xda = Xdc = [0.0, 0.0, 0.0]
            qda = np.array([0.0, 0.0, 0.0])
            qdb = self.robot_arm.qd(Xdb, qb)
            qdc = np.array([0.0, 0.0, 0.0])

        except Exception as e: # Gere le cas ou aucune solution n'est trouvée
            return False

        # On calcule les listes des q, qd, et qdd entre les deux premiers points et les deux suivant grâce à la
        # loi demouvement
        # On récupere aussi la liste des valeurs de t correspondante
        tab, qab, qdab, qddab = self.movement_law(qa, qb, qdb=qdb, Ka=self.robot_arm.Ka, Kv=self.robot_arm.Kv, Te=self.Te)
        tbc, qbc, qdbc, qddbc = self.movement_law(qb, qc, qda=qdb, Ka=self.robot_arm.Ka, Kv=self.robot_arm.Kv, Te=self.Te)

        # On décale les valeurs de temps entre B et C pour les faire commencer après le dernier temps entre A et B
        tbc = tbc + tab[-1]

        # On concatène les valeurs entre A et B et les valeurs entre B et C pour avoir les valeurs entre A et C
        tac = np.concatenate((tab, tbc))
        qac = np.concatenate((qab, qbc), axis=1)
        qdac = np.concatenate((qdab, qdbc), axis=1)
        qddac = np.concatenate((qddab, qddbc), axis=1)

        # On calule les valeurs de position, vitesse et accélération pour tous les q, qd et qdd entre A et C
        Xac, Xdac, Xddac = self.trajectory(qac, qdac, qddac)

        # Affichage des résulats
        self.display_values(tac, qac, qdac, qddac, Xac, Xdac, Xddac)
        self.plot_trajectory(Xac[:, 0], Xac[:, 1], Xac[:, 2], Xa, Xb, Xc)

        return True

    def display_values(self, t, list_q, list_qd, list_qdd, list_X, list_Xd, list_Xdd):
        """Affiche les valeurs des q, qd, qdd et X, Xd, Xdd
        ENTREE : t vecteur de taille n
        list_q, list_qd, list_qdd vecteurs de taille (m, n) m étant le nombre de qi
        list_X, list_Xd, list_Xdd vecteurs de taille (n, 3)"""
        num_q = len(list_q)
        fig, axs = plt.subplots( 3 + num_q, 3, sharex=True)

        for i in range(len(list_q)):
            axs[0, i].plot(t, list_q[i, :], 'b')
            axs[0, i].legend(['q' + str(i + 1)])
            axs[1, i].plot(t, list_qd[i, :], 'g')
            axs[1, i].legend(['qd' + str(i + 1)])
            axs[2, i].plot(t, list_qdd[i, :], 'r')
            axs[2, i].legend(['qdd' + str(i + 1)])

        axs[num_q, 0].plot(t, list_X[:, 0])
        axs[num_q, 1].plot(t, list_X[:, 1])
        axs[num_q, 2].plot(t, list_X[:, 2])
        axs[num_q, 0].legend(['x'])
        axs[num_q, 1].legend(['y'])
        axs[num_q, 2].legend(['z'])

        axs[num_q + 1, 0].plot(t, list_Xd[:, 0])
        axs[num_q + 1, 1].plot(t, list_Xd[:, 1])
        axs[num_q + 1, 2].plot(t, list_Xd[:, 2])
        axs[num_q + 1, 0].legend(['xd'])
        axs[num_q + 1, 1].legend(['yd'])
        axs[num_q + 1, 2].legend(['zd'])

        axs[num_q + 2, 0].plot(t, list_Xdd[:, 0])
        axs[num_q + 2, 1].plot(t, list_Xdd[:, 1])
        axs[num_q + 2, 2].plot(t, list_Xdd[:, 2])
        axs[num_q + 2, 0].legend(['xdd'])
        axs[num_q + 2, 1].legend(['ydd'])
        axs[num_q + 2, 2].legend(['zdd'])

    def plot_trajectory(self, xs, ys, zs, Xa, Xb, Xc):
        """Affiche la trajectoire du robot en 3d avec une animation qui se répète
        ainsi que les trois points par lequels passent le robot (code non détaillé ligne par ligne)
        ENTREE : xs, ys, zs vecteurs de taille n
        Xa, Xb , Xc vecteurs de taille 3"""
        fig = plt.figure()
        ax = p3.Axes3D(fig)

        ln, = ax.plot([], [], [], 'r', label='Trajectory')

        ax.scatter(Xa[0], Xa[1], Xa[2], marker='x')
        ax.scatter(Xb[0], Xb[1], Xb[2], marker='x')
        ax.scatter(Xc[0], Xc[1], Xc[2], marker='x')

        ax.text(Xa[0], Xa[1], Xa[2], 'Xa', color='red')
        ax.text(Xb[0], Xb[1], Xb[2], 'Xb', color='red')
        ax.text(Xc[0], Xc[1], Xc[2], 'Xc', color='red')

        # Affiche le premier segment pour aider à se représenter le robot dans l'espace
        # Ne marchera pas pour un robot différent
        ax.plot([0.0, 0.0], [0.0, 0.0], [0.0, self.robot_arm.m], 'b-')

        def init():
            ax.set_xlim(min(0.0, np.min(xs)), np.max(xs))
            ax.set_ylim(min(0.0, np.min(ys)), np.max(ys))
            ax.set_zlim(min(0.0, np.min(zs)), np.max(zs))
            return ln,

        def update(frame):
            ln.set_data(xs[:frame], ys[:frame])
            ln.set_3d_properties(zs[:frame])
            return ln,

        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')

        anim = animation.FuncAnimation(fig, update, len(xs), init_func=init, interval=50, blit=False)
        plt.show()
