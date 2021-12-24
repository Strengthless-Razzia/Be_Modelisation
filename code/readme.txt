
BE 2021 :
    Raphaël Bizet

Le code se constitue de 5 fichier principaux :
    - robot_arm.py :    - Robot_Arm est une classe abstraite qui sert d'interface
                        - NoSolutionException est une Exception qui sert dans le MGI

    - rrr.py :  RRR qui une classe héritant de Robot_Arm
                C'est la classe du robot étudié dans le BE où se trouvent tous les calculs de modélisation.
                Si on voulait modéliser un autre robot il faudrait créer une autre classe du type RRR qui extend Robot_arm et qui surcharge toutes les méthodes données dans la classe Robot_Arm.

    -model.py : Model qui est la classe qui lie la loi de mouvement et le robot. Elle contient la méthode troisPoints et s'occupe d'afficher les résultats.
                Cette classe est faite pour marcher avec n'importe quel robot tant qu'il hérite de Robot_Arm et qu'il surcharge toutes ces méthodes.
                Cette classe est aussi faite pour marcher avec n'importe qu'elle loi de mouvement si elle est de la même forme que celle implémentée.

    -movement_law.py : contient la fonction loi de mouvement polynomiale. C'est celle de l'année dernière, je n'ai pas pu implémenter la nouvelle

    -display.py : classe main qui doit être lancée et modifiée pour tester.


Les Tests du MGD sont principalement des implémentations de Widget sur RRR, et on peut les obtenir en exécutant : 

	- MainWindow pour la visualisation du bras en changeant les qi
	- testMGD pour les calculs de matrice et une visualisation plus limitée. 