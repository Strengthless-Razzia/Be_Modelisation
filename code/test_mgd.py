import model as md
from rrr import RRR
import movement_law
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt



m, n, l, k= 1, 2, 3, 4


rrr = RRR(l, k, m, n)


q1 = 0
q2 = 0
q3 = 0

m1, m2, m3 = rrr.mgd_detail(np.array([q1, q2, q3]))
 

mfin = rrr.mgd_func(np.array([q1, q2, q3]) )

print("T03 avec les paramètres calculés\n")
print(mfin)
t34 = ([1,0,0,n],[0,1,0,0],[0,0,1,0],[0,0,0,1])
mcompare = m1@m2@m3@t34


print("Produit des 3 matrices élémentaires\n")
print(mcompare) 

X1 = (m1 @ np.array([0, 0, 0, 1]))[:3]
X2 = (m1 @ m2 @ np.array([0, 0, 0, 1]))[:3]
X3 = (m1 @ m2 @ m3 @ np.array([0, 0, 0, 1]))[:3]

fig = plt.figure()
ax = plt.axes(projection='3d')

ax.plot3D([0, X1[0], X2[0], X3[0]], [0, X1[1], X2[1], X3[1]], [0, X1[2], X2[2], X3[2]] , 'maroon')

ax.set_xlabel('$X$', fontsize=20, rotation=150)
ax.set_xlim(-1, 1)
ax.set_ylabel('Y')
ax.set_ylim(-1, 1)
ax.set_zlabel('Z')
ax.set_ylim(-1, 1)


ax.set_title('Visualisation du test MGD')
plt.show()
