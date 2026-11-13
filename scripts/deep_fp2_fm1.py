"""Further Pure 2 and Further Mechanics 1 depth content (original, Edexcel 9FM0 style).
Every stated result is recomputed with asserts; the build fails if any check fails."""
import math, cmath, itertools
import numpy as np
from fractions import Fraction as Fr
from deep_core import DEEP, deep, E, F, P, X, close, integ, deriv

N0 = len(DEEP)
rd = lambda x, n=4: round(float(x), n)
g = 9.8

# ------------------------------------------------------------------ fp2-groups
G8 = [1, 3, 5, 7]
assert all(a * b % 8 in G8 for a in G8 for b in G8) and all(a * a % 8 == 1 for a in G8)
order_add = lambda a, n: next(k for k in range(1, n + 1) if a * k % n == 0)
assert order_add(8, 12) == 3 and order_add(3, 12) == 4
G9 = [1, 2, 4, 5, 7, 8]; assert sorted(pow(2, k, 9) for k in range(1, 7)) == G9 and [pow(4, k, 9) for k in (1, 2, 3)] == [4, 7, 1] and 8 * 8 % 9 == 1
op = lambda a, b: a + b + a * b
for a, b, c in ((2, -0.5, 3), (0.7, 4, -3)): assert close(op(op(a, b), c), op(a, op(b, c))) and close(op(a, b), (1 + a) * (1 + b) - 1)
assert close(op(3, -0.75), 0) and 5 * 3 % 7 == 1
deep('fp2-groups',
 'Check the four axioms in order: closure, associativity (often inherited from ordinary arithmetic or composition), identity and inverses. Lagrange’s theorem limits the possible orders of subgroups and elements to divisors of the group order; a group is cyclic exactly when some element has order equal to the group order.',
 [E('A multiplicative group modulo 8', 'Show that G = {1, 3, 5, 7} under multiplication modulo 8 is a group, and find the order of each element.', 'Closure: 3 × 5 = 15 ≡ 7, 3 × 7 = 21 ≡ 5, 5 × 7 = 35 ≡ 3, and every square is ≡ 1.', 'Multiplication modulo 8 is associative; the identity is 1.', 'Each element is its own inverse, since a² ≡ 1 for every a in G.', 'So G is a group; 1 has order 1 and 3, 5, 7 each have order 2.', 'No element has order 4, so G is not cyclic: it is isomorphic to the Klein four-group.'),
  E('Lagrange’s theorem', 'In the group of integers modulo 12 under addition, find the order of 8 and the subgroup it generates, and list the possible orders of subgroups.', '8 + 8 = 16 ≡ 4 and 8 + 8 + 8 = 24 ≡ 0.', 'So 8 has order 3 and generates {0, 4, 8}.', 'By Lagrange’s theorem the order of any subgroup divides 12.', 'Possible orders: 1, 2, 3, 4, 6, 12.')],
 [F('Integers modulo 12 under addition.', 'the order of 3 is [[4]]'),
  F('Multiplication modulo 7.', 'the inverse of 5 is [[3]]'),
  F('A group of prime order 7.', 'the number of subgroups is [[2]]')],
 [X('<p>G = {1, 2, 4, 5, 7, 8} under multiplication modulo 9.</p>',
    P('Show that 2 is a generator of G.', [('M1', 'calculates successive powers of 2 modulo 9'), ('A1', '2, 4, 8, 7, 5, 1: all six elements')]),
    P('Find the order of 4.', [('B1', '3, since 4² ≡ 7 and 4³ ≡ 1')], ans=3),
    P('Write down a subgroup of G of order 2.', [('B1', '{1, 8}')]),
    P('State, with a reason, whether G is isomorphic to the integers modulo 6 under addition.', [('B1', 'both groups are cyclic of order 6'), ('B1', 'yes: for example 2ᵏ ↦ k')])),
  X('<p>D₃ is the group of symmetries of an equilateral triangle under composition.</p>',
    P('State the possible orders of subgroups of D₃.', [('B1', '1, 2, 3 and 6')]),
    P('Explain why D₃ is not cyclic.', [('B1', 'the rotations have order 3 or 1 and the reflections order 2'), ('B1', 'no element has order 6, so no single element generates the group')]),
    P('State, with a reason, whether D₃ is abelian.', [('B1', 'no: two different reflections composed in opposite orders give different rotations')])),
  X('<p>The operation ∗ is defined on S = {x ∈ ℝ : x ≠ −1} by a ∗ b = a + b + ab.</p>',
    P('Show that a ∗ b = (1 + a)(1 + b) − 1, and hence show that S is closed under ∗.', [('M1', 'expands (1 + a)(1 + b) − 1'), ('A1', '(1 + a)(1 + b) ≠ 0, so a ∗ b ≠ −1')]),
    P('Show that ∗ is associative.', [('M1', 'writes (a ∗ b) ∗ c using the product form'), ('A1', 'both bracketings equal (1 + a)(1 + b)(1 + c) − 1')]),
    P('Find the identity element and the inverse of 3.', [('B1', 'identity 0'), ('M1', '(1 + 3)(1 + b) = 1'), ('A1', 'b = −3/4')]))])

# ------------------------------------------------------------------ fp2-reduction
I = lambda n: integ(lambda x: x ** n * math.exp(x), 0, 1)
assert close(I(3), 6 - 2 * math.e, 1e-6) and close(I(2), math.e - 2, 1e-6)
assert close(integ(lambda x: math.sqrt(1 + math.sinh(x) ** 2), 0, math.log(2)), 0.75, 1e-7)
assert close(2 * math.pi * integ(lambda x: x ** 3 * math.sqrt(1 + 9 * x ** 4), 0, 1), math.pi / 27 * (10 * math.sqrt(10) - 1), 1e-6)
J = lambda n: integ(lambda x: x ** n * math.sin(x), 0, math.pi / 2)
assert close(J(0), 1) and close(J(2), math.pi - 2, 1e-7) and close(J(4), math.pi ** 3 / 2 - 12 * math.pi + 24, 1e-6)
assert close(integ(lambda t: math.sqrt(4 * t * t + 4 * t ** 4), 0, math.sqrt(3)), 14 / 3, 1e-6)
assert close(2 * math.pi * integ(lambda x: math.sqrt(4 - x * x) * math.sqrt(1 + x * x / (4 - x * x)), 0, 1), 4 * math.pi, 1e-7)
deep('fp2-reduction',
 'Integrate by parts so that the power drops, and write the result in terms of Iₙ₋₁ or Iₙ₋₂ before substituting any limits. Evaluate the boundary terms carefully, find the starting integral I₀ or I₁ directly, and step up one index at a time. For arc length and surface area, simplify 1 + (dy/dx)² before integrating; it is often a perfect square.',
 [E('A reduction formula with an exponential', 'Iₙ = ∫ xⁿeˣ dx from 0 to 1. Show that Iₙ = e − nIₙ₋₁ and find I₃.', 'By parts: Iₙ = [xⁿeˣ] from 0 to 1 − n∫ xⁿ⁻¹eˣ dx.', 'The boundary term is e − 0, so Iₙ = e − nIₙ₋₁ for n ≥ 1.', 'I₀ = e − 1, I₁ = e − (e − 1) = 1 and I₂ = e − 2.', 'I₃ = e − 3(e − 2) = 6 − 2e.'),
  E('Arc length of a catenary', 'Find the length of the curve y = cosh x from x = 0 to x = ln 2.', 'dy/dx = sinh x, so 1 + (dy/dx)² = 1 + sinh²x = cosh²x.', 's = ∫ cosh x dx from 0 to ln 2 = sinh(ln 2).', 'sinh(ln 2) = ½(2 − ½).', 's = ¾.'),
  E('A surface of revolution', 'The arc of y = x³ from x = 0 to x = 1 is rotated through 2π about the x-axis. Find the exact surface area.', 'S = 2π∫ y√(1 + (dy/dx)²) dx = 2π∫ x³√(1 + 9x⁴) dx.', 'By inspection the integral is (1/36) × (2/3)(1 + 9x⁴)^(3/2).', 'S = (2π/54)[(1 + 9x⁴)^(3/2)] from 0 to 1.', 'S = (π/27)(10√10 − 1).')],
 [F('Iₙ = ∫ cosⁿx dx from 0 to π/2, with Iₙ = ((n − 1)/n)Iₙ₋₂ and I₀ = π/2.', 'I₂ = π/[[4]]'),
  F('Arc length of y = x from x = 0 to x = 1.', '√[[2]]'),
  F('Arc length of y = cosh x from −ln 2 to ln 2.', '2 × ¾ = [[1.5]]')],
 [X('<p>Iₙ = ∫ xⁿ sin x dx from 0 to π/2, n ≥ 0.</p>',
    P('Show that Iₙ = n(π/2)ⁿ⁻¹ − n(n − 1)Iₙ₋₂ for n ≥ 2.', [('M1', 'integrates by parts once: [−xⁿ cos x] + n∫ xⁿ⁻¹ cos x dx'), ('A1', 'the boundary term is 0'), ('M1', 'integrates by parts again'), ('A1', 'reaches the given formula')]),
    P('Find the exact value of I₄.', [('B1', 'I₀ = 1'), ('M1', 'I₂ = π − 2'), ('A1', 'I₄ = π³/2 − 12π + 24')], ans=math.pi ** 3 / 2 - 12 * math.pi + 24)),
  X('', P('A curve has parametric equations x = t², y = ⅔t³, 0 ≤ t ≤ √3. Find the length of the curve.', [('M1', 'dx/dt = 2t and dy/dt = 2t²'), ('M1', '√(4t² + 4t⁴) = 2t√(1 + t²)'), ('M1', 'integrates: ⅔(1 + t²)^(3/2)'), ('A1', '14/3')], ans=14 / 3)),
  X('', P('The arc of y = √(4 − x²) between x = 0 and x = 1 is rotated through 2π about the x-axis. Find the exact area of the surface generated.', [('M1', '1 + (dy/dx)² = 4/(4 − x²)'), ('M1', 'y√(1 + (dy/dx)²) = 2'), ('A1', '2π∫ 2 dx from 0 to 1 = 4π')], ans=4 * math.pi))])

# ------------------------------------------------------------------ fp2-eigen
A = np.array([[3, 1], [2, 2]]); Pm = np.array([[1, 1], [1, -2]]); assert np.allclose(np.linalg.inv(Pm) @ A @ Pm, np.diag([4, 1]))
B = np.array([[2, 0, 0], [0, 3, 1], [0, 1, 3]]); Q = np.array([[1, 0, 0], [0, 1, 1], [0, -1, 1]]) / np.array([1, math.sqrt(2), math.sqrt(2)])
assert np.allclose(Q.T @ Q, np.eye(3)) and np.allclose(Q.T @ B @ Q, np.diag([2, 2, 4]))
A = np.array([[4, 1], [2, 3]]); Pm = np.array([[1, 1], [1, -2]]); assert np.allclose(np.linalg.inv(Pm) @ A @ Pm, np.diag([5, 2])) and np.array_equal(np.linalg.matrix_power(A, 4), [[422, 203], [406, 219]])
C = np.array([[1, 2, 0], [2, 1, 0], [0, 0, 3]]); assert np.allclose(C @ [1, 1, 0], [3, 3, 0]) and np.allclose(sorted(np.linalg.eigvalsh(C)), [-1, 3, 3])
Q2 = np.array([[1, 1, 0], [1, -1, 0], [0, 0, math.sqrt(2)]]) / math.sqrt(2); assert np.allclose(Q2.T @ C @ Q2, np.diag([3, -1, 3]))
Pm = np.array([[1, 1], [0, 1]]); assert np.allclose(Pm @ np.diag([2, -3]) @ np.linalg.inv(Pm), [[2, -5], [0, -3]])
assert np.allclose(sorted(np.linalg.eigvals(np.array([[2, 5], [1, 4]]))), sorted(np.roots([1, -6, 3])))
deep('fp2-eigen',
 'Form det(A − λI) = 0, solve for the eigenvalues, then solve (A − λI)v = 0 separately for each one; any non-zero multiple of an eigenvector is acceptable. Check with trace = sum of eigenvalues and determinant = product. For a symmetric matrix, normalise orthogonal eigenvectors so that P is orthogonal and PᵀAP = D.',
 [E('Diagonalising a 2 × 2 matrix', 'Find P and D such that P⁻¹AP = D for A = [[3,1],[2,2]].', 'det(A − λI) = (3 − λ)(2 − λ) − 2 = λ² − 5λ + 4 = 0, so λ = 1 or 4.', 'λ = 4: −x + y = 0 gives (1, 1).', 'λ = 1: 2x + y = 0 gives (1, −2).', 'P = [[1,1],[1,−2]] and D = [[4,0],[0,1]]; check: trace 5 = 4 + 1 and det 4 = 4 × 1.'),
  E('Orthogonal diagonalisation', 'A = [[2,0,0],[0,3,1],[0,1,3]]. Find an orthogonal matrix P and a diagonal matrix D with PᵀAP = D.', 'det(A − λI) = (2 − λ)[(3 − λ)² − 1] = (2 − λ)²(4 − λ), so λ = 2 (twice) and 4.', 'λ = 2: y + z = 0 gives two orthogonal vectors (1, 0, 0) and (0, 1, −1).', 'λ = 4: (0, 1, 1).', 'Normalise: P has columns (1,0,0), (0,1,−1)/√2 and (0,1,1)/√2.', 'D = diag(2, 2, 4).')],
 [F('A = [[2,5],[1,4]].', 'sum of eigenvalues = [[6]] and product = [[3]]'),
  F('A triangular matrix [[5,2],[0,−1]].', 'eigenvalues 5 and [[-1]]'),
  F('Eigenvalue 3 with eigenvector v.', 'A²v = [[9]]v')],
 [X('<p>A = [[4,1],[2,3]].</p>',
    P('Find the eigenvalues of A.', [('M1', 'det(A − λI) = 0'), ('M1', 'λ² − 7λ + 10 = 0'), ('A1', 'λ = 2 and λ = 5')]),
    P('Find a corresponding eigenvector for each eigenvalue.', [('M1', 'solves (A − λI)v = 0 for one eigenvalue'), ('A1', '(1, 1) for 5 and (1, −2) for 2')]),
    P('Write down matrices P and D such that P⁻¹AP = D.', [('B1', 'P = [[1,1],[1,−2]] with D = [[5,0],[0,2]] in the matching order')]),
    P('Hence find A⁴.', [('M1', 'A⁴ = PD⁴P⁻¹'), ('M1', 'P⁻¹ = ⅓[[2,1],[1,−1]]'), ('A1', '[[422,203],[406,219]]')])),
  X('<p>C = [[1,2,0],[2,1,0],[0,0,3]].</p>',
    P('Show that (1, 1, 0) is an eigenvector of C and state its eigenvalue.', [('M1', 'C(1,1,0)ᵀ = (3,3,0)ᵀ'), ('A1', 'eigenvalue 3')]),
    P('Find the other eigenvalues of C.', [('M1', '(3 − λ)[(1 − λ)² − 4] = 0'), ('A1', 'λ = 3 again'), ('A1', 'λ = −1')]),
    P('Find an orthogonal matrix P and a diagonal matrix D such that PᵀCP = D.', [('M1', 'orthogonal eigenvectors (1,1,0), (1,−1,0) and (0,0,1)'), ('A1', 'normalised columns (1,1,0)/√2, (1,−1,0)/√2, (0,0,1)'), ('A1', 'D = diag(3, −1, 3) in the matching order')])),
  X('', P('A 2 × 2 matrix A has eigenvalues 2 and −3 with corresponding eigenvectors (1, 0) and (1, 1). Find A.', [('M1', 'A = PDP⁻¹ with P = [[1,1],[0,1]]'), ('M1', 'P⁻¹ = [[1,−1],[0,1]]'), ('A1', 'A = [[2,−5],[0,−3]]')]))])

# ------------------------------------------------------------------ fp2-cayley
I2 = np.eye(2); I3 = np.eye(3)
A = np.array([[2, 1], [1, 3]]); assert np.allclose(A @ A, 5 * A - 5 * I2) and np.allclose(np.linalg.inv(A), (5 * I2 - A) / 5)
A = np.array([[1, 1, 0], [0, 2, 1], [0, 0, 3]]); A2 = A @ A
assert np.allclose(A2 @ A, 6 * A2 - 11 * A + 6 * I3) and np.allclose(np.linalg.inv(A), (A2 - 6 * A + 11 * I3) / 6)
A = np.array([[3, -1], [2, 0]]); assert np.allclose(A @ A, 3 * A - 2 * I2) and np.allclose(np.linalg.matrix_power(A, 4), 15 * A - 14 * I2) and np.allclose(np.linalg.inv(A), (3 * I2 - A) / 2)
A = np.array([[2, 0, 1], [0, 1, 0], [1, 0, 2]]); A2 = A @ A; assert np.allclose(np.poly(A), [1, -5, 7, -3]) and np.allclose(np.linalg.inv(A), (A2 - 5 * A + 7 * I3) / 3)
assert np.allclose(np.poly(np.array([[1, 2], [3, 4]])), [1, -5, -2])
# A² = 3A − 2I ⇒ A³ = 7A − 6I ; A² = 4A − 3I ⇒ A⁴ = 40A − 39I (checked on a matrix satisfying it)
M_ = np.array([[1, 0], [0, 3]]); assert np.allclose(M_ @ M_, 4 * M_ - 3 * I2) and np.allclose(np.linalg.matrix_power(M_, 4), 40 * M_ - 39 * I2) and np.allclose(np.linalg.inv(M_), (4 * I2 - M_) / 3)
M_ = np.array([[1, 0], [0, 2]]); assert np.allclose(np.linalg.matrix_power(M_, 3), 7 * M_ - 6 * I2)
deep('fp2-cayley',
 'Write the characteristic equation with λ replaced by A and the constant term multiplied by I. To reach a higher power, multiply through by A and substitute for A² repeatedly; to find an inverse, multiply through by A⁻¹, which is possible exactly when the constant term is non-zero.',
 [E('A square and an inverse', 'A = [[2,1],[1,3]]. Use the Cayley–Hamilton theorem to express A² and A⁻¹ in terms of A and I.', 'det(A − λI) = (2 − λ)(3 − λ) − 1 = λ² − 5λ + 5.', 'Cayley–Hamilton: A² − 5A + 5I = 0, so A² = 5A − 5I.', 'Multiply by A⁻¹: A − 5I + 5A⁻¹ = 0.', 'A⁻¹ = (5I − A)/5 = ⅕[[3,−1],[−1,2]].'),
  E('A 3 × 3 matrix', 'A = [[1,1,0],[0,2,1],[0,0,3]]. Express A³ and A⁻¹ in terms of A², A and I.', 'A is triangular, so its eigenvalues are 1, 2, 3 and the characteristic equation is (λ − 1)(λ − 2)(λ − 3) = 0.', 'λ³ − 6λ² + 11λ − 6 = 0, so A³ = 6A² − 11A + 6I.', 'Multiply by A⁻¹: A² − 6A + 11I − 6A⁻¹ = 0.', 'A⁻¹ = (A² − 6A + 11I)/6.')],
 [F('A = [[1,2],[3,4]].', 'characteristic polynomial λ² − [[5]]λ − [[2]]'),
  F('A² = 3A − 2I.', 'A³ = 3A² − 2A = [[7]]A − [[6]]I'),
  F('A² = 4A − 3I.', 'A⁻¹ = (4I − A)/[[3]]')],
 [X('<p>A = [[3,−1],[2,0]].</p>',
    P('Find the characteristic equation of A.', [('M1', '(3 − λ)(−λ) + 2'), ('A1', 'λ² − 3λ + 2 = 0')]),
    P('Hence express A⁴ in the form pA + qI.', [('M1', 'A² = 3A − 2I'), ('M1', 'A³ = 7A − 6I'), ('A1', 'A⁴ = 15A − 14I')]),
    P('Express A⁻¹ in the form rA + sI.', [('M1', 'multiplies A² − 3A + 2I = 0 by A⁻¹'), ('A1', 'A⁻¹ = −½A + (3/2)I')])),
  X('<p>A = [[2,0,1],[0,1,0],[1,0,2]].</p>',
    P('Show that the characteristic equation of A is λ³ − 5λ² + 7λ − 3 = 0.', [('M1', 'expands det(A − λI)'), ('M1', '(1 − λ)[(2 − λ)² − 1]'), ('A1', 'expands to the given cubic')]),
    P('Hence find A⁻¹ in terms of A², A and I.', [('M1', 'A³ − 5A² + 7A − 3I = 0'), ('M1', 'multiplies by A⁻¹'), ('A1', 'A⁻¹ = ⅓(A² − 5A + 7I)')])),
  X('<p>A 2 × 2 matrix A satisfies A² − 4A + 3I = 0.</p>',
    P('Find A⁴ in the form pA + qI.', [('M1', 'A³ = 4A² − 3A = 13A − 12I'), ('M1', 'A⁴ = 13A² − 12A'), ('A1', '40A − 39I')]),
    P('Explain why A is non-singular and find A⁻¹ in terms of A and I.', [('B1', 'A(4I − A) = 3I, and 3 ≠ 0'), ('B1', 'A⁻¹ = ⅓(4I − A)')]))])

# ------------------------------------------------------------------ fp2-mapping
for t in (0.4, 2.2, 4.0):
    z = 1 + cmath.exp(1j * t); w = 1 / z; assert close(w.real, 0.5)
    z = cmath.exp(1j * t); w = 2 * z + 1 - 1j; assert close(abs(w - (1 - 1j)), 2)
    z = t - 3 + 1j; w = 1 / z; assert close(w.real ** 2 + (w.imag + 0.5) ** 2, 0.25)
    z = 1j * (t - 2); w = (z - 1) / (z + 1); assert close(abs(w), 1)
    z = 1 + 1j * (t - 2); w = z * z; assert close(w.real, 1 - w.imag ** 2 / 4)
assert abs((0.5 + 0.2j - 1) / (0.5 + 0.2j + 1)) < 1
deep('fp2-mapping',
 'Make z the subject (z in terms of w), substitute into the equation of the locus in the z-plane, and then put w = u + iv and simplify. Lines and circles map to lines and circles under w = 1/z and under fractional linear maps; check a couple of individual points to confirm the image and spot any excluded point.',
 [E('A circle through the origin under w = 1/z', 'Find the image of the circle |z − 1| = 1 under w = 1/z.', 'z = 1/w, so |1/w − 1| = 1.', 'Multiply by |w|: |1 − w| = |w|.', 'The points w are equidistant from 0 and 1.', 'The image is the line Re(w) = ½ (the point z = 0 has no image).'),
  E('An enlargement and translation', 'Find the image of |z| = 1 under w = 2z + 1 − i.', 'z = (w − 1 + i)/2.', '|(w − (1 − i))/2| = 1.', 'The image is the circle |w − (1 − i)| = 2: centre 1 − i, radius 2.'),
  E('A sector under w = z²', 'Find the image of the region |z| ≤ 2, 0 ≤ arg z ≤ π/4 under w = z².', 'In polar form, |w| = |z|² and arg w = 2 arg z.', '|w| ≤ 4.', '0 ≤ arg w ≤ π/2.', 'The image is the quarter disc of radius 4 in the first quadrant.')],
 [F('w = 3z and |z| = 2.', '|w| = [[6]]'),
  F('w = z + 4 − i, image of |z| = 1.', 'centre ([[4]], [[-1]])'),
  F('w = z² and arg z = π/6.', 'arg w = π/[[3]]')],
 [X('<p>T maps z to w, where w = 1/z, z ≠ 0.</p>',
    P('Show that T maps the line Im(z) = 1 onto a circle, and find its centre and radius.', [('M1', 'z = 1/w = (u − iv)/(u² + v²)'), ('M1', 'imaginary part −v/(u² + v²) = 1'), ('A1', 'u² + v² + v = 0'), ('M1', 'completes the square'), ('A1', 'centre (0, −½), radius ½')]),
    P('State the point on this circle that is not the image of any point on the line.', [('B1', 'w = 0')])),
  X('<p>T maps z to w, where w = (z − 1)/(z + 1), z ≠ −1.</p>',
    P('Show that T maps the imaginary axis onto the circle |w| = 1.', [('M1', '|w| = |z − 1|/|z + 1|'), ('A1', 'points on the imaginary axis are equidistant from 1 and −1, so |w| = 1')]),
    P('Find the image of the region Re(z) &gt; 0.', [('B1', 'these points are closer to 1 than to −1'), ('B1', '|w| &lt; 1')])),
  X('<p>T maps z = x + iy to w = u + iv, where w = z².</p>',
    P('Show that u = x² − y² and v = 2xy.', [('B1', 'expands (x + iy)²')]),
    P('Find a Cartesian equation for the image of the line x = 1.', [('M1', 'u = 1 − y² and v = 2y'), ('M1', 'eliminates y'), ('A1', 'u = 1 − v²/4, a parabola')]))])

# ------------------------------------------------------------------ fp2-euclid
assert math.gcd(252, 198) == 18 and 4 * 252 - 5 * 198 == 18
assert 11 * 14 % 17 == 1 and 4 * 14 % 17 == 5 and 11 * 5 % 17 == 4
assert [x for x in range(15) if 6 * x % 15 == 9] == [4, 9, 14]
assert math.gcd(391, 299) == 23 and -3 * 391 + 4 * 299 == 23
assert 23 * 7 % 40 == 1 and 23 * 35 % 40 == 5
assert [x for x in range(14) if 8 * x % 14 == 6] == [6, 13] and not [x for x in range(14) if 8 * x % 14 == 5]
assert math.gcd(48, 18) == 6 and 7 * 3 % 10 == 1 and 2 ** 10 % 10 == 4
deep('fp2-euclid',
 'Run Euclid’s algorithm as a column of equations, then reverse it one line at a time to write the gcd as a combination of the original numbers. A linear congruence ax ≡ b (mod n) has solutions only if gcd(a, n) divides b, and then it has exactly gcd(a, n) solutions modulo n.',
 [E('Euclid and Bézout', 'Find gcd(252, 198) and integers a and b with 252a + 198b = gcd(252, 198).', '252 = 1 × 198 + 54; 198 = 3 × 54 + 36; 54 = 1 × 36 + 18; 36 = 2 × 18.', 'gcd = 18.', '18 = 54 − 36 = 54 − (198 − 3 × 54) = 4 × 54 − 198.', '= 4(252 − 198) − 198 = 4 × 252 − 5 × 198, so a = 4 and b = −5.'),
  E('Solving a congruence with an inverse', 'Solve 11x ≡ 4 (mod 17).', 'Find the inverse of 11: 11 × 14 = 154 = 9 × 17 + 1.', 'So 11⁻¹ ≡ 14 (mod 17).', 'x ≡ 4 × 14 = 56 ≡ 5 (mod 17).', 'Check: 11 × 5 = 55 = 3 × 17 + 4.'),
  E('A congruence with several solutions', 'Solve 6x ≡ 9 (mod 15).', 'gcd(6, 15) = 3 divides 9, so there are 3 solutions modulo 15.', 'Divide through by 3: 2x ≡ 3 (mod 5).', '2 × 4 = 8 ≡ 3, so x ≡ 4 (mod 5).', 'x ≡ 4, 9 or 14 (mod 15).')],
 [F('Euclid’s algorithm.', 'gcd(48, 18) = [[6]]'),
  F('An inverse modulo 10.', '7 × [[3]] ≡ 1 (mod 10)'),
  F('A power modulo 10.', '2¹⁰ = 1024 ≡ [[4]] (mod 10)')],
 [X('',
    P('Use Euclid’s algorithm to find the highest common factor of 391 and 299.', [('M1', '391 = 1 × 299 + 92 and 299 = 3 × 92 + 23'), ('A1', '92 = 4 × 23, so hcf = 23')], ans=23),
    P('Hence find integers a and b such that 391a + 299b = 23.', [('M1', '23 = 299 − 3 × 92'), ('M1', 'substitutes 92 = 391 − 299'), ('A1', 'a = −3, b = 4')])),
  X('', P('Solve the congruence 23x ≡ 5 (mod 40).', [('M1', 'finds the inverse of 23 modulo 40 by Euclid or trial'), ('A1', '23⁻¹ ≡ 7'), ('A1', 'x ≡ 35 (mod 40)')])),
  X('',
    P('Find all solutions of 8x ≡ 6 (mod 14), with 0 ≤ x &lt; 14.', [('M1', 'gcd(8, 14) = 2 divides 6'), ('M1', '4x ≡ 3 (mod 7), so x ≡ 6 (mod 7)'), ('A1', 'x = 6 and x = 13')]),
    P('Explain why 8x ≡ 5 (mod 14) has no solutions.', [('B1', 'gcd(8, 14) = 2 does not divide 5')]))])

# ------------------------------------------------------------------ fp2-count
assert pow(5, 100, 13) == 1 and pow(5, 4, 13) == 1 and 7392 % 11 == 0 and 2 - 9 + 3 - 7 == -11
assert len(set(itertools.permutations('BANANA'))) == 60 and pow(3, 102, 11) == 9 and all(pow(n, 5, 5) == n % 5 for n in range(20))
assert math.factorial(10) // (6 * 6 * 2) == 50400 and math.factorial(8) // (6 * 2) == 3360
nums = [n for n in range(1000, 10000) if len(set(str(n))) == 4]; assert len(nums) == 4536 and sum(1 for n in nums if n % 5 == 0) == 952
assert pow(2, 6, 7) == 1 and 2 ** 5 == 32 and math.comb(7, 2) == 21
deep('fp2-count',
 'For powers, reduce the exponent using Fermat’s little theorem (aᵖ⁻¹ ≡ 1 mod p when p is prime and does not divide a) before calculating. For counting, decide whether order matters and whether items repeat; divide by the factorials of repeated letters, and handle restrictions by fixing the restricted positions first.',
 [E('Fermat’s little theorem', 'Find the remainder when 5¹⁰⁰ is divided by 13.', '13 is prime and does not divide 5, so 5¹² ≡ 1 (mod 13).', '100 = 8 × 12 + 4, so 5¹⁰⁰ ≡ 5⁴ (mod 13).', '5⁴ = 625 = 48 × 13 + 1.', 'The remainder is 1.'),
  E('A divisibility test', 'Use the divisibility test for 11 to decide whether 7392 is divisible by 11.', '10 ≡ −1 (mod 11), so a number is congruent to the alternating sum of its digits.', 'From the units digit: 2 − 9 + 3 − 7 = −11.', '−11 ≡ 0 (mod 11), so 7392 is divisible by 11 (7392 = 11 × 672).'),
  E('Arrangements with repeated letters', 'How many different arrangements are there of the letters of BANANA?', '6 letters with A repeated 3 times and N repeated twice.', '6!/(3! × 2!) = 720/12.', '60 arrangements.')],
 [F('Fermat’s little theorem.', '2⁶ ≡ [[1]] (mod 7)'),
  F('Subsets of a 5-element set.', '2⁵ = [[32]]'),
  F('Choosing 2 from 7.', '⁷C₂ = [[21]]')],
 [X('',
    P('Use Fermat’s little theorem to find the remainder when 3¹⁰² is divided by 11.', [('M1', '3¹⁰ ≡ 1 (mod 11)'), ('M1', '3¹⁰² = (3¹⁰)¹⁰ × 3²'), ('A1', '9')], ans=9),
    P('Prove that n⁵ − n is divisible by 5 for every integer n.', [('B1', 'if 5 ∤ n, Fermat gives n⁴ ≡ 1, so n⁵ ≡ n'), ('B1', 'if 5 | n, both terms are multiples of 5; so 5 | n⁵ − n for all n')])),
  X('<p>The letters of the word STATISTICS are arranged in a line.</p>',
    P('Find the number of different arrangements.', [('M1', '10!/(3! 3! 2!)'), ('A1', '50 400')], ans=50400),
    P('Find the number of arrangements that begin and end with S.', [('M1', 'arranges the remaining 8 letters: 8!/(3! 2!)'), ('A1', '3360')], ans=3360)),
  X('',
    P('How many four-digit numbers (1000 to 9999) have four different digits?', [('M1', '9 × 9 × 8 × 7'), ('A1', '4536')], ans=4536),
    P('How many of these are divisible by 5?', [('M1', 'last digit 0: 9 × 8 × 7 = 504'), ('M1', 'last digit 5: 8 × 8 × 7 = 448'), ('A1', '952')], ans=952))])

# ------------------------------------------------------------------ fp2-recurrence
def seq(f, u0, u1, n):
    u = [u0, u1]
    while len(u) <= n: u.append(f(u[-1], u[-2]))
    return u
assert seq(lambda a, b: 4 * a - 4 * b, 1, 4, 10) == [(1 + n) * 2 ** n for n in range(11)]
u = [1]
for n in range(10): u.append(3 * u[-1] + 2 * n)
assert u == [(3 ** (n + 1) - 2 * n - 1) // 2 for n in range(11)]
assert seq(lambda a, b: a + 6 * b, 2, 1, 10) == [3 ** n + (-2) ** n for n in range(11)] and 3 ** 5 - 32 == 211
Pp = [5000.0]
for n in range(20): Pp.append(1.05 * Pp[-1] - 200)
assert all(close(Pp[n], 4000 + 1000 * 1.05 ** n) for n in range(21)) and min(n for n in range(21) if Pp[n] > 6000) == 15
v = [0]
for n in range(10): v.append(2 * v[-1] + 3 ** n)
assert v == [3 ** n - 2 ** n for n in range(11)]
assert 3 * 2 ** 4 == 48 and np.allclose(sorted(np.roots([1, -5, 6]).real), [2, 3]) and seq(lambda a, b: a + b, 1, 1, 6)[6] == 13
deep('fp2-recurrence',
 'For a homogeneous linear recurrence, solve the auxiliary equation and choose the form that matches its roots (distinct, repeated or complex). For a non-homogeneous one, add a particular solution shaped like the extra term, then use the initial terms on the complete general solution; check one term directly from the recurrence.',
 [E('A repeated auxiliary root', 'Solve uₙ₊₂ = 4uₙ₊₁ − 4uₙ with u₀ = 1 and u₁ = 4.', 'Auxiliary equation m² − 4m + 4 = 0 has the repeated root 2.', 'uₙ = (A + Bn)2ⁿ.', 'u₀ = 1 gives A = 1; u₁ = 2(1 + B) = 4 gives B = 1.', 'uₙ = (n + 1)2ⁿ; check u₂ = 16 − 4 = 12 = 3 × 4.'),
  E('A first-order recurrence with a linear term', 'Solve uₙ₊₁ = 3uₙ + 2n with u₀ = 1.', 'Complementary solution C × 3ⁿ.', 'Try uₙ = an + b: a(n + 1) + b = 3an + 3b + 2n gives a = −1 and b = −½.', 'uₙ = C × 3ⁿ − n − ½, and u₀ = 1 gives C = 3/2.', 'uₙ = (3ⁿ⁺¹ − 2n − 1)/2; check u₁ = 3 from the recurrence.')],
 [F('uₙ₊₁ = 2uₙ with u₀ = 3.', 'u₄ = [[48]]'),
  F('uₙ₊₂ = 5uₙ₊₁ − 6uₙ.', 'auxiliary roots [[2]] and [[3]]'),
  F('Fibonacci with F₁ = F₂ = 1.', 'F₇ = [[13]]')],
 [X('<p>uₙ₊₂ = uₙ₊₁ + 6uₙ, with u₀ = 2 and u₁ = 1.</p>',
    P('Find uₙ in terms of n.', [('M1', 'auxiliary equation m² − m − 6 = 0'), ('A1', 'm = 3 or m = −2'), ('M1', 'uₙ = A3ⁿ + B(−2)ⁿ'), ('M1', 'A + B = 2 and 3A − 2B = 1'), ('A1', 'uₙ = 3ⁿ + (−2)ⁿ')]),
    P('Find u₅.', [('B1', '211')], ans=211)),
  X('<p>A population is modelled by Pₙ₊₁ = 1.05Pₙ − 200, where Pₙ is the population n years after the start and P₀ = 5000.</p>',
    P('Find Pₙ in terms of n.', [('M1', 'constant solution: P = 1.05P − 200 gives 4000'), ('M1', 'Pₙ = 4000 + C(1.05)ⁿ'), ('A1', 'C = 1000'), ('A1', 'Pₙ = 4000 + 1000(1.05)ⁿ')]),
    P('Find the first year in which the population exceeds 6000.', [('M1', '1.05ⁿ &gt; 2, so n &gt; ln 2/ln 1.05 = 14.2'), ('A1', 'n = 15')], ans=15)),
  X('<p>uₙ₊₁ = 2uₙ + 3ⁿ, with u₀ = 0.</p>',
    P('Find uₙ in terms of n.', [('M1', 'complementary solution A2ⁿ'), ('M1', 'particular solution c3ⁿ with 3c = 2c + 1'), ('A1', 'c = 1'), ('A1', 'uₙ = 3ⁿ − 2ⁿ')]),
    P('Prove your result by induction.', [('B1', 'u₀ = 1 − 1 = 0'), ('M1', 'assumes uₖ = 3ᵏ − 2ᵏ and substitutes'), ('A1', 'uₖ₊₁ = 2(3ᵏ − 2ᵏ) + 3ᵏ = 3ᵏ⁺¹ − 2ᵏ⁺¹, with a conclusion')]))])

# ------------------------------------------------------------------ fm1-impulse
assert close(0.2 * (5 + 8), 2.6)
v1 = np.array([5, 2]) + np.array([-3, 4]) / 0.4; assert np.allclose(v1, [-2.5, 12]) and rd(np.linalg.norm(v1), 2) == 12.26
assert (3 * 4 - 2 * 1) / 5 == 2 and 0.5 * 3 * 16 + 0.5 * 2 * 1 - 0.5 * 5 * 4 == 15
assert close(0.15 * 50, 7.5) and close(7.5 / 0.05, 150)
v2 = np.array([4, -3]) + np.array([-2, 5]) / 0.5; assert np.allclose(v2, [0, 7]) and close(0.25 * 49 - 0.25 * 25, 6)
assert 8 * 300 / 1200 == 2 and 0.5 * 1200 * 4 / 0.5 == 4800
deep('fm1-impulse',
 'Choose a positive direction (or use vectors) and keep the signs of every velocity; impulse equals the change in momentum, m(v − u). In a collision or explosion, total momentum is conserved but kinetic energy usually is not, so find the velocities with momentum before you discuss energy.',
 [E('A rebounding ball', 'A ball of mass 0.2 kg hits the ground at 8 m s⁻¹ and rebounds at 5 m s⁻¹. Find the impulse exerted by the ground.', 'Take upwards as positive: u = −8 and v = 5.', 'I = m(v − u) = 0.2(5 − (−8)).', 'I = 2.6 N s, upwards.'),
  E('Impulse as a vector', 'A particle of mass 0.4 kg moving with velocity (5i + 2j) m s⁻¹ receives an impulse of (−3i + 4j) N s. Find its new velocity and speed.', 'I = m(v − u), so v = u + I/m.', 'v = (5i + 2j) + (−7.5i + 10j).', 'v = (−2.5i + 12j) m s⁻¹.', 'Speed = √(6.25 + 144) = 12.26 m s⁻¹.'),
  E('Coalescing particles', 'A particle of mass 3 kg moving at 4 m s⁻¹ collides with a particle of mass 2 kg moving at 1 m s⁻¹ in the opposite direction, and they coalesce. Find their common velocity and the loss of kinetic energy.', 'Momentum: 3(4) + 2(−1) = 5v.', 'v = 2 m s⁻¹ in the original direction of the 3 kg particle.', 'Kinetic energy before = 24 + 1 = 25 J; after = ½ × 5 × 2² = 10 J.', 'Loss = 15 J.')],
 [F('A force of 6 N acts for 0.5 s.', 'impulse = [[3]] N s'),
  F('A 2 kg particle speeds up from 3 to 7 m s⁻¹ in a straight line.', 'impulse = [[8]] N s'),
  F('A 4 kg particle moving at 2.5 m s⁻¹.', 'momentum = [[10]] N s')],
 [X('<p>A ball of mass 0.15 kg moving horizontally at 20 m s⁻¹ is hit by a bat and moves back along the same line at 30 m s⁻¹.</p>',
    P('Find the magnitude of the impulse on the ball.', [('M1', '0.15(30 − (−20))'), ('A1', '7.5 N s')], ans=7.5, unit='N s'),
    P('The ball is in contact with the bat for 0.05 s. Find the average force on the ball.', [('B1', '150 N')], ans=150, unit='N')),
  X('<p>A particle P of mass 0.5 kg moving with velocity (4i − 3j) m s⁻¹ receives an impulse of (−2i + 5j) N s.</p>',
    P('Find the velocity of P immediately after the impulse.', [('M1', 'u + I/m'), ('A1', '7j m s⁻¹')]),
    P('Find the gain in kinetic energy of P.', [('M1', 'initial kinetic energy ½ × 0.5 × 25 = 6.25 J'), ('M1', 'final kinetic energy ½ × 0.5 × 49 = 12.25 J'), ('A1', '6 J')], ans=6, unit='J')),
  X('<p>A gun of mass 1200 kg fires a shell of mass 8 kg horizontally at 300 m s⁻¹. The gun is free to recoil horizontally.</p>',
    P('Find the speed of recoil of the gun.', [('M1', 'conservation of momentum: 1200v = 8 × 300'), ('A1', '2 m s⁻¹')], ans=2, unit='m s⁻¹'),
    P('The gun is brought to rest in 0.5 m by a constant resisting force. Find the size of the force.', [('M1', 'kinetic energy ½ × 1200 × 2² = 2400 J'), ('M1', 'work done: F × 0.5 = 2400'), ('A1', '4800 N')], ans=4800, unit='N'))])

# ------------------------------------------------------------------ fm1-energy
assert 18000 / 15 == 1200 and close((1200 - 600) / 900, 2 / 3) and 18000 / 600 == 30
R = 5 * g * math.cos(math.radians(30)); ke = 5 * g * 4 * 0.5 - 0.2 * R * 4; assert rd(math.sqrt(2 * ke / 5), 2) == 5.06
Fz = 1500 + 4000 * g / 20; assert close(Fz, 3460) and close(Fz * 12, 41520) and close((Fz - 1500) / 4000, 0.49)
dec = 2 * g * 0.5 + 0.25 * 2 * g * math.cos(math.radians(30)); assert rd(36 / dec, 2) == 2.56
assert close(50 * g * 12 + 0.5 * 50 * 64, 7480)
deep('fm1-energy',
 'Write the work–energy principle as one equation: initial energy + work by driving forces = final energy + work against resistances, with each term in joules. For power, use P = Fv with the driving force F, then Newton’s second law for acceleration; maximum speed occurs when the driving force equals the total resistance.',
 [E('Power and acceleration', 'A car of mass 900 kg moves on a level road against a resistance of 600 N. Its engine works at 18 kW. Find its acceleration when its speed is 15 m s⁻¹, and its maximum speed.', 'Driving force F = P/v = 18 000/15 = 1200 N.', 'Newton’s second law: 1200 − 600 = 900a.', 'a = ⅔ m s⁻².', 'At maximum speed F = 600, so v = 18 000/600 = 30 m s⁻¹.'),
  E('Work–energy on a rough slope', 'A particle of mass 5 kg is released from rest and slides 4 m down a rough plane inclined at 30°. The coefficient of friction is 0.2. Find its speed.', 'Loss of potential energy = 5g × 4 sin 30° = 98 J.', 'R = 5g cos 30° = 42.4 N, so friction = 0.2R = 8.49 N, doing 33.9 J of work.', '½ × 5v² = 98 − 33.9 = 64.1.', 'v = 5.06 m s⁻¹.')],
 [F('A driving force of 400 N at 25 m s⁻¹.', 'power = [[10000]] W'),
  F('A 3 kg particle moving at 4 m s⁻¹.', 'kinetic energy = [[24]] J'),
  F('A 2 kg mass raised 5 m (g = 9.8).', 'gain in potential energy = [[98]] J')],
 [X('<p>A lorry of mass 4000 kg moves up a straight road inclined at α to the horizontal, where sin α = 1/20. The resistance to motion is 1500 N. The lorry moves at a constant speed of 12 m s⁻¹.</p>',
    P('Find the power of the engine.', [('M1', 'driving force = 1500 + 4000g sin α'), ('A1', '3460 N'), ('A1', '41.5 kW')], ans=41520, unit='W', tol=2e-3),
    P('The lorry reaches a level road. The power and the resistance are unchanged. Find the acceleration of the lorry at the instant its speed is 12 m s⁻¹.', [('M1', 'driving force 41 520/12 = 3460 N'), ('M1', '3460 − 1500 = 4000a'), ('A1', '0.49 m s⁻²')], ans=0.49, unit='m s⁻²')),
  X('', P('A particle of mass 2 kg is projected up a line of greatest slope of a rough plane inclined at 30° with speed 6 m s⁻¹. The coefficient of friction is 0.25. Use the work–energy principle to find how far up the plane the particle moves before coming to rest.', [('M1', 'friction = 0.25 × 2g cos 30° = 4.24 N'), ('M1', 'kinetic energy ½ × 2 × 36 = 36 J'), ('M1', '36 = (2g sin 30° + 4.24)d'), ('A1', 'd = 2.56 m')], ans=36 / dec, unit='m', tol=3e-3)),
  X('', P('A pump raises 50 kg of water per second through a height of 12 m and ejects it at 8 m s⁻¹. Find the power of the pump.', [('M1', 'potential energy per second 50g × 12 = 5880 J'), ('M1', 'kinetic energy per second ½ × 50 × 8² = 1600 J'), ('A1', '7480 W')], ans=7480, unit='W'))])

# ------------------------------------------------------------------ fm1-elastic
assert close(2 * g * 1.5 / 49, 0.6) and close(20 * 0.04 / 1.6, 0.5) and close(math.sqrt(2 * 0.5 / 0.5), math.sqrt(2))
lam = 4 * 1 * g; assert close(1 * g * (1 + 1), lam * 1 ** 2 / 2)
assert close(20 * 0.3 / 1.5, 4) and close(30 * 0.04 / 1.0, 1.2) and close(3 * g * 2 / 147, 0.4)
xe = 0.4 * g * 0.8 / 9.8; assert close(xe, 0.32)
dEPE = 9.8 * (0.42 ** 2 - 0.32 ** 2) / 1.6; v = math.sqrt(2 * (dEPE - 0.4 * g * 0.1) / 0.4); assert rd(v, 3) == 0.553 and close(v, math.sqrt(9.8 / (0.4 * 0.8)) * 0.1)
assert rd(math.sqrt(2 * 60 * 0.0225 / 1.0 / 1.5), 2) == 1.34
lam2 = 70 * g * 45 * 2 * 20 / 25 ** 2; assert rd(lam2, 1) == 1975.7
deep('fm1-elastic',
 'Use Hooke’s law T = λx/l for forces and E = λx²/2l for energy, where x is the extension, not the stretched length. In energy problems list every form at the start and at the end: kinetic, gravitational and elastic. Remember that a string is slack (no tension) once it is shorter than its natural length.',
 [E('Equilibrium on an elastic string', 'A particle of mass 2 kg hangs in equilibrium on an elastic string of natural length 1.5 m and modulus 49 N. Find the extension.', 'Equilibrium: T = mg = 19.6 N.', 'Hooke’s law: 49x/1.5 = 19.6.', 'x = 0.6 m.'),
  E('Released from a spring', 'A particle of mass 0.5 kg on a smooth horizontal table is attached to a spring of natural length 0.8 m and modulus 20 N. It is pulled out to an extension of 0.2 m and released. Find its speed as it passes through the natural length.', 'Elastic energy at release = 20 × 0.2²/(2 × 0.8) = 0.5 J.', 'At the natural length all of this is kinetic energy.', '½ × 0.5v² = 0.5, so v² = 2.', 'v = √2 ≈ 1.41 m s⁻¹.'),
  E('Falling on an elastic string', 'A particle of mass 1 kg is attached to one end of a light elastic string of natural length 1 m and modulus 4g N, whose other end is fixed at O. The particle is dropped from O. Find its greatest extension.', 'At the lowest point the particle is at rest, having fallen 1 + x metres.', 'Loss of potential energy = elastic energy: g(1 + x) = 4gx²/2.', '2x² − x − 1 = 0, so (2x + 1)(x − 1) = 0.', 'Greatest extension x = 1 m.')],
 [F('λ = 20 N, l = 1.5 m, extension 0.3 m.', 'tension = [[4]] N'),
  F('λ = 30 N, l = 0.5 m, extension 0.2 m.', 'elastic energy = [[1.2]] J'),
  F('A 3 kg mass hangs on a string with λ = 147 N, l = 2 m (g = 9.8).', 'extension = [[0.4]] m')],
 [X('<p>A particle of mass 0.4 kg hangs on a light elastic string of natural length 0.8 m and modulus 9.8 N, attached to a fixed point.</p>',
    P('Find the extension of the string in equilibrium.', [('M1', '0.4g = 9.8x/0.8'), ('A1', '0.32 m')], ans=0.32, unit='m'),
    P('The particle is pulled down a further 0.1 m and released from rest. Find its speed as it passes through the equilibrium position.', [('M1', 'elastic energy at extensions 0.42 m and 0.32 m'), ('M1', 'includes the gain in potential energy 0.4g × 0.1'), ('M1', '½ × 0.4v² = 0.453 − 0.392'), ('A1', '0.553 m s⁻¹')], ans=v, unit='m s⁻¹', tol=3e-3)),
  X('', P('A particle of mass 1.5 kg on a smooth horizontal surface is held against a spring of natural length 0.5 m and modulus 60 N, compressing it by 0.15 m. It is released. Find the speed with which it leaves the spring.', [('M1', 'elastic energy 60 × 0.15²/(2 × 0.5)'), ('A1', '1.35 J'), ('A1', '1.34 m s⁻¹')], ans=math.sqrt(1.8), unit='m s⁻¹', tol=3e-3)),
  X('<p>A bungee jumper of mass 70 kg is attached to an elastic rope of natural length 20 m. The other end is fixed to a bridge. She falls from rest at the bridge and first comes to instantaneous rest 45 m below it.</p>',
    P('Find the modulus of elasticity of the rope.', [('M1', 'energy equation: loss of potential energy = elastic energy'), ('M1', '70g × 45 = λ × 25²/(2 × 20)'), ('A1', 'λ = 1980 N (3 s.f.)')], ans=lam2, unit='N', tol=3e-3),
    P('State one modelling assumption you have made.', [('B1', 'the jumper is a particle, or air resistance is negligible, or the rope is light')]))])

# ------------------------------------------------------------------ fm1-direct
v1 = (15 - 4 - 2 * 2.8) / 5; v2 = v1 + 2.8; assert close(v1, 1.08) and close(v2, 3.88) and close(3 * v1 + 2 * v2, 11)
assert rd(37.5 + 4 - 1.5 * v1 ** 2 - v2 ** 2, 3) == 24.696
a1 = (16 - 4 * 2.5) / 6; b1 = a1 + 2.5; assert a1 == 1 and b1 == 3.5 and 2 * a1 + 4 * b1 == 16 and 38 - (1 + 24.5) == 12.5
assert close(0.4 * 3.5, 1.4) and close(0.3 * 13, 3.9) and close(0.15 * 39, 5.85)
for e in (0.2, 0.5, 0.8):
    vA, vB = (1 - 2 * e) / 3, (1 + e) / 3; assert close(vA + 2 * vB, 1) and close(vB - vA, e)
deep('fm1-direct',
 'Draw before-and-after diagrams with every velocity arrow in the same positive direction, so an answer that comes out negative tells you the particle moves the other way. Use two equations: conservation of momentum and Newton’s law of restitution, written as separation speed = e × approach speed.',
 [E('A head-on collision', 'A particle of mass 3 kg moving at 5 m s⁻¹ collides directly with a particle of mass 2 kg moving at 2 m s⁻¹ in the opposite direction. The coefficient of restitution is 0.4. Find their velocities after the collision and the kinetic energy lost.', 'Momentum: 3(5) + 2(−2) = 3v₁ + 2v₂, so 3v₁ + 2v₂ = 11.', 'Restitution: v₂ − v₁ = 0.4 × (5 + 2) = 2.8.', 'Solving: v₁ = 1.08 m s⁻¹ and v₂ = 3.88 m s⁻¹, both in the original direction of the 3 kg particle.', 'Kinetic energy before = 41.5 J and after = 16.80 J, so 24.7 J is lost.'),
  E('Rebounding from a wall', 'A sphere hits a smooth wall at right angles with speed 6 m s⁻¹ and e = ⅔. Find its speed after the impact and after a second impact with a parallel wall.', 'After the first impact: ⅔ × 6 = 4 m s⁻¹.', 'Its speed is unchanged until it reaches the second wall.', 'After the second impact: ⅔ × 4 = 8/3 m s⁻¹.')],
 [F('Equal masses, e = 1: A at 5 m s⁻¹ hits B at rest.', 'B moves at [[5]] m s⁻¹'),
  F('A ball hits a wall at 10 m s⁻¹ with e = 0.6.', 'rebound speed = [[6]] m s⁻¹'),
  F('Approach speed 8 m s⁻¹, e = 0.25.', 'separation speed = [[2]] m s⁻¹')],
 [X('<p>Particles P and Q, of masses 2 kg and 4 kg, move in the same direction along a straight line with speeds 6 m s⁻¹ and 1 m s⁻¹. P collides with Q. The coefficient of restitution is 0.5.</p>',
    P('Find the speeds of P and Q after the collision.', [('M1', 'conservation of momentum: 2v₁ + 4v₂ = 16'), ('M1', 'restitution: v₂ − v₁ = 0.5 × 5'), ('M1', 'solves the simultaneous equations'), ('A1', 'P: 1 m s⁻¹'), ('A1', 'Q: 3.5 m s⁻¹')]),
    P('Find the kinetic energy lost in the collision.', [('M1', '38 − (1 + 24.5)'), ('A1', '12.5 J')], ans=12.5, unit='J'),
    P('Q then hits a fixed wall at right angles, with coefficient of restitution 0.4. Show that P and Q collide again.', [('M1', 'Q rebounds at 1.4 m s⁻¹'), ('A1', 'P moves towards the wall and Q towards P, so they approach each other')])),
  X('<p>A particle A of mass m moving with speed u collides directly with a particle B of mass 2m at rest. The coefficient of restitution is e.</p>',
    P('Show that the speed of B after the collision is u(1 + e)/3.', [('M1', 'momentum: mu = mv_A + 2mv_B'), ('M1', 'restitution: v_B − v_A = eu'), ('A1', 'eliminates v_A to obtain the given result')]),
    P('Find the velocity of A after the collision, and the range of values of e for which A reverses its direction.', [('A1', 'v_A = u(1 − 2e)/3'), ('B1', 'reverses if e &gt; ½')])),
  X('<p>A ball of mass 0.3 kg moving horizontally at 8 m s⁻¹ hits a fixed vertical wall at right angles and rebounds at 5 m s⁻¹.</p>',
    P('Find the coefficient of restitution between the ball and the wall.', [('B1', 'e = 5/8')], ans=0.625),
    P('Find the magnitude of the impulse exerted by the wall.', [('M1', '0.3 × (5 − (−8))'), ('A1', '3.9 N s')], ans=3.9, unit='N s'),
    P('Find the kinetic energy lost in the impact.', [('M1', '½ × 0.3 × (64 − 25)'), ('A1', '5.85 J')], ans=5.85, unit='J'))])

# ------------------------------------------------------------------ fm1-oblique
par, per = 10 * math.cos(math.radians(60)), 10 * math.sin(math.radians(60)) * 0.5
assert rd(math.hypot(par, per), 3) == 6.614 and rd(math.degrees(math.atan2(per, par)), 1) == 40.9
assert close(0.5 * 9, 4.5) and close(0.25 * (52 - 25), 6.75)
assert close(3 - 0.75, 2.25) and close(2.25 - 0.75, 1.5)
h, vv = 12 * math.cos(math.radians(30)), 12 * math.sin(math.radians(30)) * 0.6
assert rd(math.hypot(h, vv), 1) == 11.0 and rd(math.degrees(math.atan2(vv, h)), 1) == 19.1 and close(1 - (h * h + vv * vv) / 144, 0.16)
a_, b_ = 2, 5; assert 2 * a_ + b_ == 9 and b_ - a_ == 0.5 * 6
e5 = Fr(5, 16); assert 64 * e5 ** 2 + 36 == Fr(169, 4) and close(0.2 * 8 * (1 + 5 / 16), 2.1)
deep('fm1-oblique',
 'Resolve every velocity parallel and perpendicular to the surface, or along and perpendicular to the line of centres. Smooth contact means the parallel components are unchanged; restitution and (for two spheres) momentum act only along the normal or line of centres. Recombine at the end for speed and direction.',
 [E('Oblique impact with a wall', 'A smooth sphere hits a smooth wall with speed 10 m s⁻¹ at 60° to the wall. The coefficient of restitution is 0.5. Find its speed and direction after the impact.', 'Parallel component 10 cos 60° = 5, unchanged.', 'Perpendicular component 10 sin 60° = 8.66, reversed and multiplied by 0.5: 4.33.', 'Speed = √(5² + 4.33²) = 6.61 m s⁻¹.', 'Angle with the wall = arctan(4.33/5) = 40.9°.'),
  E('Using vectors', 'A particle of mass 0.5 kg moving with velocity (4i − 6j) m s⁻¹ hits a smooth fixed surface whose normal is parallel to j. The coefficient of restitution is 0.5. Find its velocity after impact, the impulse and the loss of kinetic energy.', 'The i-component is unchanged; the j-component becomes +0.5 × 6 = 3.', 'v = (4i + 3j) m s⁻¹.', 'Impulse = 0.5 × (3 − (−6))j = 4.5j N s.', 'Kinetic energy loss = ½ × 0.5 × (52 − 25) = 6.75 J.'),
  E('Two spheres', 'Smooth spheres A and B have equal mass. A moves with velocity (3i + 4j) m s⁻¹ and hits B, which is at rest. At impact the line of centres is parallel to i and e = ½. Find their velocities after the collision.', 'Perpendicular to the line of centres, A keeps 4j and B has 0j.', 'Along i: momentum 3 = a + b; restitution b − a = ½ × 3.', 'b = 2.25 and a = 0.75.', 'A: (0.75i + 4j) m s⁻¹; B: 2.25i m s⁻¹.')],
 [F('Perpendicular component 6 m s⁻¹, e = 0.5.', 'after impact: [[3]] m s⁻¹'),
  F('A smooth surface: parallel component 8 m s⁻¹.', 'after impact: [[8]] m s⁻¹'),
  F('Components 3 and 4 after impact.', 'speed = [[5]] m s⁻¹')],
 [X('<p>A ball strikes a smooth horizontal floor with speed 12 m s⁻¹ at an angle of 30° to the floor. The coefficient of restitution is 0.6.</p>',
    P('Find the speed of the ball immediately after the impact.', [('M1', 'horizontal 12 cos 30° unchanged'), ('M1', 'vertical 0.6 × 12 sin 30° = 3.6'), ('A1', '11.0 m s⁻¹')], ans=math.hypot(h, vv), unit='m s⁻¹', tol=3e-3),
    P('Find the angle between the ball’s path and the floor after the impact.', [('M1', 'tan θ = 3.6/(12 cos 30°)'), ('A1', '19.1°')], ans=19.1, unit='°', tol=3e-3),
    P('Find the fraction of the ball’s kinetic energy lost.', [('M1', '1 − 121/144'), ('A1', '0.16')], ans=0.16)),
  X('<p>Smooth spheres A (mass 2 kg) and B (mass 1 kg) have velocities (5i + 2j) m s⁻¹ and (−i + 3j) m s⁻¹. When they collide the line of centres is parallel to i, and e = ½.</p>',
    P('Find the velocities of A and B immediately after the collision.', [('B1', 'j-components unchanged: 2j and 3j'), ('M1', 'momentum along i: 2a + b = 9'), ('M1', 'restitution: b − a = ½ × 6'), ('A1', 'a = 2, b = 5'), ('A1', 'A: (2i + 2j), B: (5i + 3j)')]),
    P('Find the impulse on B.', [('M1', '1 × (5 − (−1))i'), ('A1', '6i N s')])),
  X('<p>A particle of mass 0.2 kg moving with velocity (8i + 6j) m s⁻¹ hits a smooth fixed wall whose normal is parallel to i. Its speed after the impact is 6.5 m s⁻¹.</p>',
    P('Find the coefficient of restitution.', [('M1', 'velocity after (−8e i + 6j)'), ('M1', '64e² + 36 = 6.5²'), ('A1', 'e = 5/16')], ans=5 / 16),
    P('Find the magnitude of the impulse on the particle.', [('M1', '0.2 × 8(1 + e)'), ('A1', '2.1 N s')], ans=2.1, unit='N s'))])

assert len(DEEP) - N0 == 13
for k_, dd in DEEP.items():
    assert len(dd['examples']) >= 2 and len(dd['fills']) >= 3 and len(dd['exam']) >= 3 and len(dd['tip']) > 120, k_
    for q in dd['exam']:
        for p in q['parts']: assert p['m'] == len(p['ms']), (k_, p['q'])
