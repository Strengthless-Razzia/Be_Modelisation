syms x y z m n k l c1 s1 c2 s2 c3 s3

eqns = [
x == c1*c2*(c3*n + m) - c1*s2*s3*n + c1*k,
y == s1*c2*(c3*n + m) - s1*s2*s3*n,
z == s2*(c3* n +m) +c2*s3*n + l
];

S = solve(eqns, [c1 s1 c2 s2 c3 s3]);
S.c1
S.s1
S.c2
S.s2
S.c3
S.s3