syms q1 q2 q3 m n k dx dy dz dq1 dq2 dq3

eqns = [
dx == -dq1*sin(q1)*k - n*(dq1*(sin(q1)*cos(q2)*cos(q3) - sin(q1)*sin(q2)*sin(q3)) - dq2*(cos(q2)*sin(q3)*cos(q1) + sin(q2)*cos(q1)*cos(q3)) + dq3*(cos(q3)*sin(q2)*cos(q1) + sin(q3)*cos(q1)*cos(q2))) - m*(dq1*sin(q1)*cos(q2) + dq2*sin(q2)*cos(q1)),
dy == m*(dq1*cos(q1)*cos(q2) - dq2*sin(q2)*sin(q1)) + n*(dq1*(cos(q1)*cos(q2)*cos(q3) - cos(q1)*sin(q2)*sin(q3)) - dq2*(2*cos(q1)*sin(q2)*cos(q3)) - dq3*(sin(q3)*sin(q1)*cos(q1) + cos(q3)*sin(q1)*sin(q2))),
dz == n*(dq2*(cos(q2)*cos(q3) - sin(q2)*sin(q3)) + dq3*(cos(q3)*cos(q2) - sin(q3)*sin(q2))) + dq2*cos(q2)*m
];

S = solve(eqns, [qd1 qd2 qd3]);
S.qd1
S.qd2
S.qd3