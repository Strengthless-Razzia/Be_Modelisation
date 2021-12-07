syms q1 q2 q3 m n k dx dy dz dq1 dq2 dq3

eqns = [
% c1 == cos(q1),
% s1 == sin(q1),
% c2 == cos(q2),
% s2 == sin(q2),
% c3 == cos(q3),
% s3 == sin(q3),
% dx == -dq1*s1*k - m*(dq1*s1*c2 + dq2*s2*c1) - n*(dq1*(c1*c2*c3 - c1*s2*s3) - dq2*(c2*s3*c1 + s2*c1*c3) + dq3*(c3*s2*c1 + s3*c1*c2)),
% dy == m*(dq1*c1*c2 - dq2*s2*s1) + n*(dq1*(c1*c2*c3 - c1*s2*s3) - dq2*(2*s2*c1*c3) - dq3*(s3*s1*c2 + c3*s1*s2)),
% dz == n*(dq2*(c2*c3 - s2*s3) + dq3*(c3*c2 - s3*s2)) + dq2*c2*m
dx == -dq1*sin(q1)*k - n*(dq1*(sin(q1)*cos(q2)*cos(q3) - sin(q1)*sin(q2)*sin(q3)) - dq2*(cos(q2)*sin(q3)*cos(q1) + sin(q2)*cos(q1)*cos(q3)) + dq3*(cos(q3)*sin(q2)*cos(q1) + sin(q3)*cos(q1)*cos(q2))) - m*(dq1*sin(q1)*cos(q2) + dq2*sin(q2)*cos(q1)),
dy == m*(dq1*cos(q1)*cos(q2) - dq2*sin(q2)*sin(q1)) + n*(dq1*(cos(q1)*cos(q2)*cos(q3) - cos(q1)*sin(q2)*sin(q3)) - dq2*(2*cos(q1)*sin(q2)*cos(q3)) - dq3*(sin(q3)*sin(q1)*cos(q1) + cos(q3)*sin(q1)*sin(q2))) + cos(q1)*k,
dz == n*(dq2*(cos(q2)*cos(q3) - sin(q2)*sin(q3)) + dq3*(cos(q3)*cos(q2) - sin(q3)*sin(q2))) + dq2*cos(q2)*m
];

S = solve(eqns, [dq1 dq2 dq3]);
S.dq1
S.dq2
S.dq3