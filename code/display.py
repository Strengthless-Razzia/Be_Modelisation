import model as md
import rpr
import movement_law
import numpy as np

"""BE 2020 :    
    Raphaël Bizet
    Margot Cobourg
    Maureen Delauney Le Dins 
    Aurélien Marchal"""

"""Toutes les mesures sont en cm et tous les angles en radian"""

if __name__ == '__main__':

    # Caractéristiques du robot RPR
    """
    m longueur O0O1
    n longueur O3O4
    Kv limite en vitesse des qi
    Kv limite en accélération des qi
    qmin min accepté pour les qi
    qmax max accepté pour les qi
    """
    m = 40.0
    n = 20.0
    Kv = np.array([np.pi * 4, 50., np.pi*4])
    Ka = Kv/0.1
    qmin = np.array([-3 * np.pi / 4, 0.0, -3 * np.pi / 4])
    qmax = np.array([3 * np.pi / 4, 200.0, 3 * np.pi / 4])

    # On crée une instance du bras de robot RPR avec ces caractéristiques
    robot_arm = rpr.RPR(m, n, Kv=Kv, Ka=Ka, qmin=qmin, qmax=qmax)

    # On créer un modèle avec le bras de robot et la loi de mouvement
    model = md.Model(robot_arm, movement_law.movement_law_func)

    # On créée les trois points par lesquels le robot doit passer et un vecteur vitesse pour le pt B
    Xa = np.array([100.0, 0.0, m])
    Xb = np.array([-100., 0.0, m])
    Xc = np.array([50.0, 0.0, m-n])
    Xdb = np.array([0., 0., 10.])

    # On lance la fonction principale
    success = model.trois_points(Xa, Xb, Xdb, Xc)
    #q = model.robot_arm.q(Xb)
    #qd = model.robot_arm.qd(Xdb, q)
    #print(model.robot_arm.Xd(qd, q))
