import numpy as np


class NoSolutionException(Exception):
    """Exception si le MGI ou MDI ne trouve pas de valeur"""
    def __init__(self):
        print("No possible solutions")


class Robot_arm:
    """Classe abstraite de laquelle hérite le robot RPR (sert juste à structure du code)"""
    def __init__(self, num_link, Kv, Ka, qmin=None, qmax=None):
        assert Kv.shape[0] == num_link and Ka.shape[0] == num_link
        self.Kv = Kv
        self.Ka = Ka
        self.qmin = qmin
        self.qmax = qmax

    def X(self, q):
        pass

    def Xd(self, q, qd):
        pass

    def Xdd(self, q, qd, qdd):
        pass

    def q(self, X):
        pass

    def qd(self, Xd, q):
        pass

    def qdd(self, X, Xd, Xdd):
        pass
