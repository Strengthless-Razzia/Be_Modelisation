syms x y z m n k l q1 q2 q3

eqn = [
x == cos(q1)*(cos(q2)*(cos(q3)*n + m) - sin(q2)*sin(q3)*n + k) ,
y == sin(q1)*(cos(q2)*(cos(q3)*n + m) - sin(q2)*sin(q3)*n + k) ,
z == sin(q2)*(cos(q3)* n +m) +cos(q2)*sin(q3)*n + l
];

S = solve(eqn, [q1 q2 q3]);
S.q1
S.q2
S.q3