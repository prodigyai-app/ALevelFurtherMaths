"""Core Pure depth: extra worked examples, fill-the-gaps and multi-part exam questions (original, Edexcel 9FM0 style).
Every stated result is recomputed below with asserts; build.py refuses to build if any check fails."""
import cmath, math
import numpy as np
from fractions import Fraction as Fr

def close(a, b, tol=1e-7): return abs(a - b) <= tol * max(1, abs(b))
def integ(f, a, b, n=20000):  # midpoint rule
    h = (b - a) / n
    return sum(f(a + (i + .5) * h) for i in range(n)) * h
def deriv(f, x, h=1e-5): return (f(x + h) - f(x - h)) / (2 * h)
def deriv2(f, x, h=1e-4): return (f(x + h) - 2 * f(x) + f(x - h)) / (h * h)

def E(title, q, *steps): return dict(title=title, q=q, steps=list(steps))
def F(q, *lines): return dict(q=q, lines=list(lines))
def P(q, ms, ans=None, tol=1e-3, unit=''):
    d = dict(q=q, m=len(ms), ms=[list(x) for x in ms])
    if ans is not None: d['ans'] = dict(a=round(float(ans), 10), tol=tol, unit=unit)
    return d
def X(stem, *parts): return dict(stem=stem, parts=list(parts))

DEEP = {}
def deep(id, tip, examples, fills, exam): DEEP[id] = dict(tip=tip, examples=examples, fills=fills, exam=exam)

# ------------------------------------------------------------------ cp-induction
for n in range(1, 9):
    assert (7 ** n - 1) % 6 == 0 and (4 ** n + 6 * n - 1) % 9 == 0
    assert sum(r ** 3 for r in range(1, n + 1)) == n * n * (n + 1) ** 2 // 4
    assert sum(r * (r + 1) for r in range(1, n + 1)) * 3 == n * (n + 1) * (n + 2)
    assert np.array_equal(np.linalg.matrix_power(np.array([[1, 1], [0, 1]]), n), np.array([[1, n], [0, 1]]))
    assert 4 ** (n + 1) + 6 * (n + 1) - 1 == 4 * (4 ** n + 6 * n - 1) - 18 * n + 9
u = 5
for n in range(1, 8): assert u == 3 ** n + 2; u = 3 * u - 4
deep('cp-induction',
 'State the proposition for n = k exactly as given, and make the step where the assumption is used visible. A proof that never uses the inductive hypothesis is not a proof by induction. Finish with a conclusion that mentions the base case, the step and the set of integers covered.',
 [E('Divisibility', 'Prove by induction that 7ⁿ − 1 is divisible by 6 for all positive integers n.', 'n = 1: 7 − 1 = 6, which is divisible by 6.', 'Assume 7ᵏ − 1 = 6m for some integer m.', '7ᵏ⁺¹ − 1 = 7(7ᵏ − 1) + 6.', '= 42m + 6 = 6(7m + 1), a multiple of 6.', 'True for n = 1, and true for n = k implies true for n = k + 1, so true for all positive integers n.'),
  E('A matrix power', 'Prove by induction that [[1,1],[0,1]]ⁿ = [[1,n],[0,1]] for all positive integers n.', 'n = 1: both sides are [[1,1],[0,1]].', 'Assume [[1,1],[0,1]]ᵏ = [[1,k],[0,1]].', 'Multiply by one more factor: [[1,k],[0,1]][[1,1],[0,1]] = [[1,1 + k],[0,1]].', 'This is the stated result with n = k + 1.', 'True for n = 1 and the step holds, so the result is true for all positive integers n.'),
  E('A sum with a product term', 'Prove by induction that Σ r(r + 1) from r = 1 to n equals n(n + 1)(n + 2)/3.', 'n = 1: LHS = 2 and RHS = 1 × 2 × 3/3 = 2.', 'Assume the sum to k is k(k + 1)(k + 2)/3.', 'Sum to k + 1 = k(k + 1)(k + 2)/3 + (k + 1)(k + 2).', '= (k + 1)(k + 2)(k + 3)/3, taking out the common factor (k + 1)(k + 2)/3.', 'This is the formula with n = k + 1; with the base case, it holds for all positive integers n.')],
 [F('Adding the next odd number.', 'k² + (2k + [[1]]) = (k + 1)²'),
  F('Taking out a common factor.', 'k(k + 1)(k + 2)/3 + (k + 1)(k + 2) = (k + 1)(k + 2)(k + [[3]])/3'),
  F('Setting up a divisibility step.', '5ᵏ⁺¹ − 1 = 5(5ᵏ − 1) + [[4]]')],
 [X('', P('Prove by induction that, for all positive integers n, Σ r³ from r = 1 to n equals n²(n + 1)²/4.', [('B1', 'n = 1: LHS = 1, RHS = 1 × 4/4 = 1'), ('M1', 'assumes true for n = k and adds (k + 1)³'), ('M1', 'takes out the factor (k + 1)²/4'), ('A1', '(k + 1)²(k² + 4k + 4)/4'), ('A1', '= (k + 1)²(k + 2)²/4, the result for n = k + 1'), ('A1', 'complete conclusion: base case, inductive step, all positive integers')])),
  X('<p>f(n) = 4ⁿ + 6n − 1, where n is a positive integer.</p>',
    P('Find f(1) and f(2).', [('B1', 'f(1) = 9 and f(2) = 27')]),
    P('Prove by induction that f(n) is divisible by 9 for all positive integers n.', [('M1', 'assumes f(k) = 9m and considers f(k + 1) = 4ᵏ⁺¹ + 6k + 5'), ('M1', 'writes f(k + 1) = 4f(k) − 18k + 9'), ('A1', '= 9(4m − 2k + 1)'), ('A1', 'conclusion using f(1) = 9 as the base case')])),
  X('<p>A sequence is defined by u₁ = 5 and uₙ₊₁ = 3uₙ − 4.</p>',
    P('Find u₂ and u₃.', [('B1', 'u₂ = 11 and u₃ = 29')]),
    P('Prove by induction that uₙ = 3ⁿ + 2.', [('B1', 'n = 1: 3 + 2 = 5 = u₁'), ('M1', 'assumes uₖ = 3ᵏ + 2 and substitutes into uₖ₊₁ = 3uₖ − 4'), ('A1', 'uₖ₊₁ = 3ᵏ⁺¹ + 6 − 4 = 3ᵏ⁺¹ + 2'), ('A1', 'complete conclusion')]))])

# ------------------------------------------------------------------ cp-complex
r = np.roots([1, -5, 11, -15]); assert any(close(z, 1 + 2j) for z in r) and any(close(z, 3) for z in r)
assert close((3 - 2j) ** 2, 5 - 12j) and close((2 + 3j) * (1 - 1j), 5 + 1j) and close((4 + 2j) / (1 + 1j), 3 - 1j)
assert np.allclose(np.polymul([1, -2, 2], [1, -4, 13]), [1, -6, 23, -34, 26])
assert close((7 + 4j) / (2 - 1j), 2 + 3j) and close((3 + 4j) ** 2, -7 + 24j)
deep('cp-complex',
 'Decide first whether the coefficients are real: only then do non-real roots come in conjugate pairs. When dividing, write the conjugate multiplication as a separate line so the real denominator is visible, and when finding square roots keep both sign choices until the final line.',
 [E('Using a given complex root', 'Given that 1 + 2i is a root of z³ − 5z² + 11z − 15 = 0, solve the equation completely.', 'Real coefficients, so 1 − 2i is also a root.', '(z − 1 − 2i)(z − 1 + 2i) = z² − 2z + 5.', 'z³ − 5z² + 11z − 15 = (z² − 2z + 5)(z − 3), comparing the z³ and constant terms.', 'Check the z term: 6 + 5 = 11.', 'The roots are 1 + 2i, 1 − 2i and 3.'),
  E('Square roots of a complex number', 'Find the square roots of 5 − 12i.', 'Let (a + bi)² = 5 − 12i with a, b real.', 'Real and imaginary parts: a² − b² = 5 and 2ab = −12.', 'Substituting b = −6/a gives a⁴ − 5a² − 36 = 0, so (a² − 9)(a² + 4) = 0.', 'a is real, so a = ±3 and b = ∓2.', 'The square roots are 3 − 2i and −3 + 2i.')],
 [F('Multiply.', '(2 + 3i)(1 − i) = [[5]] + [[1]]i'),
  F('Divide using the conjugate.', '(4 + 2i)/(1 + i) = (4 + 2i)(1 − i)/[[2]] = [[3]] − i'),
  F('z = 3 − 4i.', 'zz* = [[25]]')],
 [X('<p>f(z) = z⁴ − 6z³ + 23z² − 34z + 26. Given that 1 + i is a root of f(z) = 0:</p>',
    P('write down another complex root;', [('B1', '1 − i')]),
    P('solve f(z) = 0 completely.', [('M1', 'forms (z − 1 − i)(z − 1 + i)'), ('A1', 'z² − 2z + 2'), ('M1', 'divides or compares coefficients to find the other quadratic factor'), ('A1', 'z² − 4z + 13'), ('A1', 'z = 2 ± 3i (with 1 ± i)')])),
  X('<p>The complex number z satisfies (2 − i)z = 7 + 4i.</p>',
    P('Find z in the form a + bi.', [('M1', 'multiplies numerator and denominator by 2 + i'), ('A1', 'numerator 10 + 15i, denominator 5'), ('A1', 'z = 2 + 3i')]),
    P('z is a root of z² + pz + q = 0, where p and q are real. Find p and q.', [('M1', 'uses the conjugate root 2 − 3i: sum 4, product 13'), ('A1', 'p = −4, q = 13')])),
  X('', P('Find the square roots of −7 + 24i.', [('M1', 'a² − b² = −7 and 2ab = 24'), ('M1', 'eliminates to a⁴ + 7a² − 144 = 0'), ('A1', 'a² = 9 (a² = −16 rejected)'), ('A1', '3 + 4i and −3 − 4i')]))])

# ------------------------------------------------------------------ cp-argand
assert close(integ(lambda t: 0.5 * (4 * math.cos(t)) ** 2, 0, math.pi / 4), math.pi + 2, 1e-6)
assert close(abs(complex(-2, 2)) + math.sqrt(2), 3 * math.sqrt(2)) and close(math.asin(math.sqrt(2) / abs(complex(-2, 2))), math.pi / 6)
assert close(3 * math.pi / 4 + math.pi / 6, 11 * math.pi / 12)
for x in (0.0, 2.0, 5.5): y = 3 * x - 8; assert close(abs(complex(x, y) - 6), abs(complex(x, y) - 2j))
assert close(8 / math.sqrt(10), 4 * math.sqrt(10) / 5)
deep('cp-argand',
 'Translate each condition into geometry before any algebra: |z − a| is a distance from the point a, and arg(z − a) is a direction measured at a. Mark the fixed points first, state whether each boundary is included, and remember that a half-line from an arg condition does not include its starting point.',
 [E('Greatest and least modulus on a circle', 'z satisfies |z − 3 − 4i| = 2. Find the least and greatest values of |z|.', 'The locus is a circle, centre (3, 4), radius 2.', 'The centre is √(3² + 4²) = 5 from the origin.', 'The nearest and farthest points lie on the line through the origin and the centre.', 'Least |z| = 5 − 2 = 3; greatest |z| = 5 + 2 = 7.'),
  E('A half-line', 'Sketch the locus arg(z + 1 − i) = 3π/4 and give its Cartesian equation.', 'Write as arg(z − (−1 + i)) = 3π/4: a half-line starting at (−1, 1).', 'The direction 3π/4 has gradient tan(3π/4) = −1 and points up and to the left.', 'y − 1 = −(x + 1), so y = −x.', 'The locus is y = −x for x < −1; the point (−1, 1) itself is excluded (open circle).'),
  E('Area of a region', 'Find the area of the region defined by |z − 2| ≤ 2 and 0 ≤ arg z ≤ π/4.', 'The circle has centre (2, 0) and radius 2, so it passes through the origin; in polar form r = 4cos θ.', 'The region is swept out from the origin for 0 ≤ θ ≤ π/4.', 'Area = ½∫ 16cos²θ dθ = 4∫ (1 + cos 2θ) dθ from 0 to π/4.', '= 4[θ + ½ sin 2θ] = 4(π/4 + ½).', 'Area = π + 2.')],
 [F('Read off the circle |z − 3 + 2i| = 5.', 'centre ([[3]], [[-2]]), radius [[5]]'),
  F('Perpendicular bisector |z − 4| = |z + 2|.', 'the line x = [[1]]'),
  F('Points on |z − 3 − 4i| = 2.', 'greatest |z| = 5 + 2 = [[7]]')],
 [X('<p>The complex number z satisfies |z + 2 − 2i| = √2.</p>',
    P('Describe the locus of z.', [('B1', 'circle with centre (−2, 2)'), ('B1', 'radius √2')]),
    P('Find the greatest value of |z|.', [('M1', 'distance of the centre from O is 2√2, then adds the radius'), ('A1', '3√2')], ans=3 * math.sqrt(2)),
    P('Find the greatest value of arg z, where −π &lt; arg z ≤ π.', [('M1', 'uses the tangent from O: right angle between tangent and radius'), ('A1', 'sin α = √2/(2√2), so α = π/6'), ('A1', '3π/4 + π/6 = 11π/12')], ans=11 * math.pi / 12)),
  X('<p>The region R is defined by |z| ≤ 4 and π/6 ≤ arg z ≤ π/2.</p>',
    P('Find the exact area of R.', [('B1', 'R is a sector of the circle centre O, radius 4'), ('M1', '½ × 4² × (π/2 − π/6)'), ('A1', '8π/3')], ans=8 * math.pi / 3)),
  X('<p>The complex number z satisfies |z − 6| = |z − 2i|.</p>',
    P('Find a Cartesian equation of the locus of z.', [('M1', '(x − 6)² + y² = x² + (y − 2)²'), ('M1', 'expands and simplifies: −12x + 36 = −4y + 4'), ('A1', 'y = 3x − 8')]),
    P('Find the least value of |z|.', [('M1', 'perpendicular distance from O to 3x − y − 8 = 0'), ('A1', '8/√10 = 4√10/5')], ans=8 / math.sqrt(10)))])

# ------------------------------------------------------------------ cp-exponential
z, w = 2 * cmath.exp(1j * math.pi / 3), 3 * cmath.exp(-1j * math.pi / 4)
assert close(z * w, 6 * cmath.exp(1j * math.pi / 12)) and close(z / w, (2 / 3) * cmath.exp(7j * math.pi / 12))
assert close((1 + 1j * math.sqrt(3)) ** 6, 64)
z = -2 + 2j * math.sqrt(3); assert close(abs(z), 4) and close(cmath.phase(z), 2 * math.pi / 3) and close(z ** 4, -128 + 128j * math.sqrt(3))
z, w = 4 * cmath.exp(1j * math.pi / 6), 2 * cmath.exp(-1j * math.pi / 3)
assert close(z * w, 8 * cmath.exp(-1j * math.pi / 6)) and close(z / w, 2j)
q = (1 + 1j) / (math.sqrt(3) - 1j); assert close(abs(q), math.sqrt(2) / 2) and close(cmath.phase(q), 5 * math.pi / 12)
deep('cp-exponential',
 'Plot the number before quoting an argument: the quadrant decides the angle, not the calculator value of arctan. Use exponential or modulus-argument form for products, quotients and powers, Cartesian form for sums, and bring every final argument back into (−π, π].',
 [E('Products and quotients', 'z = 2e^(iπ/3) and w = 3e^(−iπ/4). Find zw and z/w in the form re^(iθ) with −π < θ ≤ π.', 'Multiply moduli and add arguments: zw = 6e^(i(π/3 − π/4)).', 'zw = 6e^(iπ/12).', 'Divide moduli and subtract arguments: z/w = (2/3)e^(i(π/3 + π/4)).', 'z/w = (2/3)e^(7πi/12).'),
  E('A power in Cartesian form', 'Find (1 + i√3)⁶ in the form a + bi.', '|1 + i√3| = 2 and the point is in the first quadrant with arg = π/3.', '1 + i√3 = 2e^(iπ/3).', '(2e^(iπ/3))⁶ = 2⁶ e^(2πi).', 'e^(2πi) = 1, so (1 + i√3)⁶ = 64.')],
 [F('Modulus.', '|−5 + 12i| = [[13]]'),
  F('Argument of a point on the negative imaginary axis.', 'arg(−2i) = −π/[[2]]'),
  F('Euler.', 'e^(iπ) = [[-1]]')],
 [X('<p>z = −2 + 2√3 i.</p>',
    P('Find the modulus and the argument of z.', [('B1', '|z| = 4'), ('M1', 'uses arctan(√3) with z in the second quadrant'), ('A1', 'arg z = 2π/3')]),
    P('Find z⁴ in the form a + bi.', [('M1', '4⁴ e^(8πi/3)'), ('M1', 'reduces the argument to 2π/3'), ('A1', '−128 + 128√3 i')])),
  X('<p>z = 4(cos π/6 + i sin π/6) and w = 2(cos(−π/3) + i sin(−π/3)).</p>',
    P('Find zw in modulus-argument form.', [('M1', 'multiplies moduli and adds arguments'), ('A1', '8(cos(−π/6) + i sin(−π/6))')]),
    P('Find z/w in the form a + bi.', [('M1', 'modulus 4 ÷ 2 = 2'), ('M1', 'argument π/6 + π/3 = π/2'), ('A1', '2i')])),
  X('<p>w = (1 + i)/(√3 − i).</p>',
    P('Find |w| and arg w, giving exact answers.', [('B1', '|1 + i| = √2 with argument π/4'), ('B1', '|√3 − i| = 2 with argument −π/6'), ('M1', 'divides the moduli and subtracts the arguments'), ('A1', '|w| = √2/2 and arg w = 5π/12')]))])

# ------------------------------------------------------------------ cp-demoivre
for t in (0.3, 1.1, 2.4):
    assert close(math.cos(3 * t), 4 * math.cos(t) ** 3 - 3 * math.cos(t))
    assert close(math.sin(t) ** 4, (math.cos(4 * t) - 4 * math.cos(2 * t) + 3) / 8)
    assert close(math.sin(5 * t), 16 * math.sin(t) ** 5 - 20 * math.sin(t) ** 3 + 5 * math.sin(t))
for k, a in enumerate([math.pi / 12, 7 * math.pi / 12, -11 * math.pi / 12, -5 * math.pi / 12]): assert close((2 * cmath.exp(1j * a)) ** 4, 8 + 8j * math.sqrt(3))
for a in (-math.pi / 6, math.pi / 2, -5 * math.pi / 6): assert close((2 * cmath.exp(1j * a)) ** 3, -8j)
for x in (0, math.sin(math.pi / 5), -math.sin(math.pi / 5), math.sin(2 * math.pi / 5), -math.sin(2 * math.pi / 5)): assert abs(16 * x ** 5 - 20 * x ** 3 + 5 * x) < 1e-9
assert round(math.sin(math.pi / 5), 3) == 0.588 and round(math.sin(2 * math.pi / 5), 3) == 0.951
assert close(math.cos(2 * math.pi / 5) + math.cos(4 * math.pi / 5), -0.5) and close(math.sqrt(3) / 4 * (2 * math.sqrt(3)) ** 2, 3 * math.sqrt(3))
deep('cp-demoivre',
 'For roots, write the right-hand side with its general argument θ + 2kπ before dividing by n, and list exactly n values of k. For identities, decide whether you need real or imaginary parts before expanding, and convert everything to one trigonometric function at the end.',
 [E('A multiple-angle identity', 'Use de Moivre’s theorem to show that cos 3θ = 4cos³θ − 3cos θ.', '(cos θ + i sin θ)³ = cos 3θ + i sin 3θ.', 'Expanding with c = cos θ, s = sin θ: c³ + 3ic²s − 3cs² − is³.', 'Equate real parts: cos 3θ = c³ − 3cs².', 'Replace s² by 1 − c²: cos 3θ = c³ − 3c(1 − c²).', 'cos 3θ = 4cos³θ − 3cos θ.'),
  E('Fourth roots', 'Solve z⁴ = 8 + 8√3 i, giving the roots in the form re^(iθ) with −π < θ ≤ π.', '|8 + 8√3 i| = 16 and the argument is π/3.', 'z⁴ = 16e^(i(π/3 + 2kπ)).', 'z = 2e^(i(π/12 + kπ/2)) for k = 0, 1, −1, −2.', 'z = 2e^(iπ/12), 2e^(7πi/12), 2e^(−5πi/12), 2e^(−11πi/12).'),
  E('A power of sine', 'Express sin⁴θ in terms of cos 4θ and cos 2θ.', 'With z = e^(iθ): z − 1/z = 2i sin θ and zⁿ + 1/zⁿ = 2cos nθ.', '(2i sin θ)⁴ = z⁴ − 4z² + 6 − 4/z² + 1/z⁴.', '16 sin⁴θ = (z⁴ + 1/z⁴) − 4(z² + 1/z²) + 6 = 2cos 4θ − 8cos 2θ + 6.', 'sin⁴θ = (cos 4θ − 4cos 2θ + 3)/8.')],
 [F('De Moivre.', '(cos θ + i sin θ)⁵ = cos [[5]]θ + i sin [[5]]θ'),
  F('Roots of unity.', 'the sum of the n distinct nth roots of unity is [[0]]'),
  F('Cube roots of 27.', 'each root has modulus [[3]]')],
 [X('',
    P('Use de Moivre’s theorem to show that sin 5θ = 16sin⁵θ − 20sin³θ + 5sin θ.', [('M1', 'expands (c + is)⁵ with the binomial theorem'), ('M1', 'takes imaginary parts: 5c⁴s − 10c²s³ + s⁵'), ('M1', 'replaces c² by 1 − s²'), ('A1', '5s(1 − 2s² + s⁴) − 10s³(1 − s²) + s⁵'), ('A1', '16s⁵ − 20s³ + 5s')]),
    P('Hence find all the solutions of 16x⁵ − 20x³ + 5x = 0, giving non-zero roots to 3 decimal places.', [('M1', 'sets x = sin θ and solves sin 5θ = 0'), ('A1', 'θ = kπ/5'), ('A1', 'x = 0, ±0.588, ±0.951')])),
  X('',
    P('Solve z³ = −8i, giving the roots in the form re^(iθ) with −π &lt; θ ≤ π.', [('B1', 'modulus 2'), ('M1', 'arguments (−π/2 + 2kπ)/3'), ('A1', '2e^(−iπ/6)'), ('A1', '2e^(iπ/2) and 2e^(−5πi/6)')]),
    P('The roots are the vertices of a triangle in the Argand diagram. Find its exact area.', [('M1', 'equilateral triangle inscribed in a circle of radius 2: side 2√3'), ('A1', '3√3')], ans=3 * math.sqrt(3))),
  X('<p>ω = e^(2πi/5).</p>',
    P('Show that 1 + ω + ω² + ω³ + ω⁴ = 0.', [('M1', 'geometric series: (ω⁵ − 1)/(ω − 1)'), ('A1', 'ω⁵ = 1 and ω ≠ 1, so the sum is 0')]),
    P('Hence find the exact value of cos(2π/5) + cos(4π/5).', [('M1', 'takes real parts: 1 + 2cos(2π/5) + 2cos(4π/5) = 0'), ('A1', '−½')], ans=-0.5))])

# ------------------------------------------------------------------ cp-matrix
for k in (0.0, 1.0, 4 / 7): assert close(np.linalg.det(np.array([[1, 2, 0], [3, -1, 2], [1, 0, k]])), 4 - 7 * k)
M = np.array([[2, 0, 1], [1, 1, 0], [0, 1, 1]]); assert close(np.linalg.det(M), 3) and np.allclose(np.linalg.inv(M) * 3, [[1, 1, -1], [-1, 2, 1], [1, -2, 2]])
assert close(np.linalg.det(np.array([[4, 3], [2, 5]])), 14) and np.array_equal(np.array([[1, 2], [3, 4]]) @ np.array([2, 1]), [4, 10])
for k in (3, -2): assert close(np.linalg.det(np.array([[k, 2], [3, k - 1]])), 0)
assert np.allclose(np.linalg.inv(np.array([[4, 2], [3, 3]])) * 6, [[3, -2], [-3, 4]])
A = np.array([[1, 0, 2], [2, 1, 0], [0, 3, 1]]); assert close(np.linalg.det(A), 13)
ADJ = np.round(np.linalg.inv(A) * 13).astype(int); assert np.allclose(A @ ADJ, 13 * np.eye(3)) and ADJ.tolist() == [[1, 6, -2], [-2, 1, 4], [6, -3, 1]]
assert np.array_equal(A @ np.array([1, 2, 2]), [5, 4, 8])
A2 = np.array([[2, 1], [5, 3]]); B2 = np.array([[1, 1], [2, -1]]); assert np.array_equal(A2 @ B2, [[4, 1], [11, 2]]) and np.allclose(np.linalg.inv(A2), [[3, -1], [-5, 2]])
deep('cp-matrix',
 'Check that the dimensions allow the product and keep the order: AB ≠ BA in general and (AB)⁻¹ = B⁻¹A⁻¹. For a 3 × 3 inverse, lay out minors, then cofactor signs, then the transpose, and confirm one row of AA⁻¹ before using the result.',
 [E('A singular 3 × 3 matrix', 'A = [[1,2,0],[3,−1,2],[1,0,k]]. Find the value of k for which A is singular.', 'Expand along the first row: det A = 1(−k − 0) − 2(3k − 2) + 0.', 'det A = −k − 6k + 4 = 4 − 7k.', 'A is singular when det A = 0.', 'k = 4/7.'),
  E('Inverse of a 3 × 3 matrix', 'Find the inverse of M = [[2,0,1],[1,1,0],[0,1,1]].', 'det M = 2(1 − 0) − 0 + 1(1 − 0) = 3.', 'Matrix of minors: [[1,1,1],[−1,2,2],[−1,−1,2]].', 'Apply the alternating signs: cofactors [[1,−1,1],[1,2,−2],[−1,1,2]].', 'Transpose and divide by 3: M⁻¹ = ⅓[[1,1,−1],[−1,2,1],[1,−2,2]].', 'Check the first row of MM⁻¹: ⅓(2 + 1, 2 − 2, −2 + 2) = (1, 0, 0).')],
 [F('A 2 × 2 determinant.', 'det [[4,3],[2,5]] = 20 − 6 = [[14]]'),
  F('Determinant of a product, with det A = 3 and det B = −2.', 'det(AB) = [[-6]]'),
  F('Matrix times a column vector.', '[[1,2],[3,4]] (2, 1)ᵀ = ([[4]], [[10]])ᵀ')],
 [X('<p>M = [[k,2],[3,k − 1]], where k is a constant.</p>',
    P('Find the values of k for which M is singular.', [('M1', 'det M = k(k − 1) − 6'), ('M1', 'solves k² − k − 6 = 0'), ('A1', 'k = 3 or k = −2')]),
    P('Given that k = 4, find M⁻¹.', [('M1', 'det M = 6 and swaps/negates the entries'), ('A1', '⅙[[3,−2],[−3,4]]')])),
  X('<p>A = [[1,0,2],[2,1,0],[0,3,1]].</p>',
    P('Find det A.', [('M1', '1(1 − 0) − 0 + 2(6 − 0)'), ('A1', '13')], ans=13),
    P('Find A⁻¹.', [('M1', 'finds the matrix of minors'), ('M1', 'applies the cofactor signs'), ('M1', 'transposes and divides by det A'), ('A1', '(1/13)[[1,6,−2],[−2,1,4],[6,−3,1]]')]),
    P('Hence solve x + 2z = 5, 2x + y = 4, 3y + z = 8.', [('M1', 'multiplies A⁻¹ by (5, 4, 8)ᵀ'), ('A1', 'x = 1, y = 2, z = 2')])),
  X('<p>A = [[2,1],[5,3]] and AB = [[4,1],[11,2]].</p>',
    P('Find the matrix B.', [('B1', 'det A = 1, so A⁻¹ = [[3,−1],[−5,2]]'), ('M1', 'B = A⁻¹(AB), multiplying on the left'), ('A1', 'B = [[1,1],[2,−1]]')]))])

# ------------------------------------------------------------------ cp-transform
M = np.array([[4, -2], [1, 1]])
for m in (1, 0.5): v = M @ np.array([1, m]); assert close(v[1], m * v[0])
assert np.array_equal(np.array([[0, 1], [1, 0]]) @ np.array([[0, -1], [1, 0]]), [[1, 0], [0, -1]])
assert close(np.linalg.det(np.array([[3, 1], [2, 4]])), 10)
A = np.array([[1, -1], [1, 1]]) / math.sqrt(2); assert np.allclose(np.linalg.matrix_power(A, 8), np.eye(2)) and np.allclose(np.array([[1, 0], [0, -1]]) @ A * math.sqrt(2), [[1, -1], [-1, -1]])
T = np.array([[3, 2], [1, 4]])
for m in (1, -0.5): v = T @ np.array([1, m]); assert close(v[1], m * v[0])
assert np.array_equal(T @ np.array([1, 1]), [5, 5]) and close(np.linalg.det(np.array([[2, -1], [3, 5]])), 13)
deep('cp-transform',
 'Read a matrix through its columns, the images of (1, 0) and (0, 1), and write composites right to left: the first transformation is the right-hand factor. For an invariant line, transform a general point (t, mt + c) and require the image to satisfy the same equation; do not confuse this with a line of invariant points.',
 [E('Invariant lines through the origin', 'Find the invariant lines through the origin for M = [[4,−2],[1,1]].', 'A general point on y = mx is (t, mt); its image is (4t − 2mt, t + mt).', 'The image lies on y = mx when t + mt = m(4t − 2mt).', '1 + m = 4m − 2m², so 2m² − 3m + 1 = 0.', '(2m − 1)(m − 1) = 0, giving m = ½ or m = 1.', 'The invariant lines are y = ½x and y = x.'),
  E('A composite transformation', 'R is a rotation of 90° anticlockwise about O and S is a reflection in y = x. Find the single transformation equivalent to R followed by S.', 'R = [[0,−1],[1,0]] and S = [[0,1],[1,0]].', 'R followed by S is the product SR.', 'SR = [[0,1],[1,0]][[0,−1],[1,0]] = [[1,0],[0,−1]].', 'This is a reflection in the x-axis.'),
  E('Area scale factor', 'A triangle of area 5 is transformed by [[3,1],[2,4]]. Find the area of its image.', 'det = 3 × 4 − 1 × 2 = 10.', 'The area scale factor is |det| = 10.', 'Image area = 5 × 10 = 50; the positive determinant means orientation is preserved.')],
 [F('Area scale factor of [[3,1],[2,4]].', 'det = [[10]]'),
  F('Rotation of 180° about O.', 'the matrix is [[−1,0],[0,[[-1]]]]'),
  F('Enlargement, scale factor 3, centre O.', 'determinant = [[9]]')],
 [X('<p>A = (1/√2)[[1,−1],[1,1]] and B = [[1,0],[0,−1]].</p>',
    P('Describe fully the transformation represented by A.', [('B1', 'rotation about the origin'), ('B1', '45° anticlockwise')]),
    P('Explain why A⁸ = I.', [('B1', 'eight rotations of 45° make a full turn of 360°')]),
    P('Find the matrix representing A followed by B.', [('M1', 'forms the product BA'), ('A1', '(1/√2)[[1,−1],[−1,−1]]')])),
  X('<p>T = [[3,2],[1,4]].</p>',
    P('Show that the line y = x is invariant under T.', [('M1', 'image of (t, t) is (5t, 5t)'), ('A1', 'the image lies on y = x, so the line maps to itself')]),
    P('Find the other invariant line through the origin.', [('M1', 'image of (t, mt) is (3t + 2mt, t + 4mt)'), ('M1', 'requires t + 4mt = m(3t + 2mt)'), ('A1', '2m² − m − 1 = 0'), ('A1', 'y = −½x')]),
    P('State, with a reason, whether y = x is a line of invariant points.', [('B1', 'no: (t, t) maps to (5t, 5t), so only the origin is fixed')])),
  X('', P('The triangle with vertices (0, 0), (4, 0) and (0, 3) is transformed by [[2,−1],[3,5]]. Find the area of the image.', [('B1', 'original area 6'), ('M1', 'det = 10 + 3 = 13'), ('A1', '78')], ans=78))])

# ------------------------------------------------------------------ cp-systems
A = np.array([[1, 2, -1], [2, -1, 3], [3, 1, 2]]); assert close(np.linalg.det(A), 0) and np.array_equal(A[0] + A[1], A[2])
assert np.allclose(np.linalg.solve(np.array([[2, 1, -1], [1, -1, 2], [3, 2, 1]]), [1, 5, 10]), [1, 2, 3])
for a in (0.0, 2.0, 3.0): assert close(np.linalg.det(np.array([[1, 1, 2], [2, -1, 1], [3, 0, a]])), 9 - 3 * a)
assert np.allclose(np.linalg.solve(np.array([[1, 1, 1], [2, -1, 3], [1, 2, -1]]), [6, 9, 2]), [1, 2, 3])
deep('cp-systems',
 'Find the determinant first: non-zero means one point, zero means you must test consistency. When the determinant is zero, combine the equations to see whether they agree (a line or plane of solutions) or contradict (no common point), and name the configuration: sheaf, prism, or parallel planes.',
 [E('A parameter and a sheaf', 'x + 2y − z = 3, 2x − y + 3z = 4 and 3x + y + 2z = k. Find k for which the equations are consistent and interpret the result.', 'The left side of the third equation is the sum of the first two left sides.', 'So the coefficient determinant is 0: there is no unique solution.', 'Adding the first two equations gives 3x + y + 2z = 7.', 'The system is consistent only when k = 7.', 'For k = 7 the three planes form a sheaf, meeting in a line; otherwise they form a triangular prism with no common point.'),
  E('A unique solution by elimination', 'Solve 2x + y − z = 1, x − y + 2z = 5 and 3x + 2y + z = 10.', 'Add the first two equations: 3x + z = 6.', 'Twice the second plus the third: 5x + 5z = 20, so x + z = 4.', 'Subtract: 2x = 2, so x = 1 and z = 3.', 'From the first equation y = 1 − 2 + 3 = 2.', '(x, y, z) = (1, 2, 3); check in the third: 3 + 4 + 3 = 10.')],
 [F('Two equations: x + y = 5 and x − y = 1.', 'x = [[3]] and y = [[2]]'),
  F('A singular 2 × 2 matrix.', 'det [[1,2],[2,4]] = [[0]]'),
  F('The planes x + y + z = 1 and x + y + z = 4.', 'number of common points = [[0]]')],
 [X('<p>The equations x + y + 2z = 4, 2x − y + z = 3 and 3x + az = b are given, where a and b are constants.</p>',
    P('Find the determinant of the coefficient matrix in terms of a.', [('M1', 'expands a 3 × 3 determinant'), ('A1', '9 − 3a')]),
    P('State the value of a for which there is no unique solution.', [('B1', 'a = 3')]),
    P('Given a = 3 and b = 7, show that the equations are consistent and interpret this geometrically.', [('M1', 'adds the first two equations: 3x + 3z = 7'), ('A1', 'this is the third equation, so the system is consistent'), ('B1', 'the three planes form a sheaf: they meet in a line')])),
  X('', P('Solve the simultaneous equations x + y + z = 6, 2x − y + 3z = 9 and x + 2y − z = 2.', [('M1', 'eliminates one variable from two pairs of equations'), ('M1', 'solves the resulting pair'), ('A1', 'one correct value'), ('A1', 'x = 1, y = 2, z = 3')])),
  X('<p>Π₁: x − 2y + z = 3, Π₂: 2x − 4y + 2z = 1 and Π₃: x + y − z = 0.</p>',
    P('Describe the configuration of the three planes.', [('B1', 'Π₁ and Π₂ are parallel and distinct: normals proportional, constants not'), ('B1', 'no common point; Π₃ cuts them in two parallel lines')]))])

# ------------------------------------------------------------------ cp-roots
r = np.roots([2, -5, 4, -3]); assert close(sum(1 / x for x in r), 4 / 3) and close(sum(x * x for x in r), 9 / 4)
r = np.roots([1, -3, 0, 4]); assert np.allclose(sorted(np.roots([1, -9, 24, -16]).real), sorted((r + 2).real))
r = np.roots([1, -2, 3, 4, -5]); assert close(sum(x * x for x in r), -2)
r = np.roots([1, 2, -3, 4]); assert close(sum(x ** 2 for x in r), 10) and close(sum(x ** 3 for x in r), -38)
assert np.allclose(sorted(np.roots([1, -5, -9, 45]).real), [-3, 3, 5]) and np.allclose(sorted(np.roots([1, -4, 1, 6]).real), [-1, 2, 3])
r = np.roots([2, -6, 7]); assert np.allclose(np.sort_complex(np.roots([4, -8, 49])), np.sort_complex(r ** 2))
deep('cp-roots',
 'Write the equation with its leading coefficient visible before quoting sums and products, since each is divided by that coefficient and the signs alternate. For a transformed equation, substitute the inverse relationship and clear fractions; for powers of roots, use the equation itself to reduce α³ rather than expanding brackets.',
 [E('Symmetric functions of a cubic', 'α, β, γ are the roots of 2x³ − 5x² + 4x − 3 = 0. Find Σ1/α and Σα².', 'Σα = 5/2, Σαβ = 4/2 = 2 and αβγ = 3/2.', 'Σ1/α = Σαβ/αβγ = 2 ÷ 3/2.', 'Σ1/α = 4/3.', 'Σα² = (Σα)² − 2Σαβ = 25/4 − 4.', 'Σα² = 9/4.'),
  E('A linear transformation of the roots', 'The roots of x³ − 3x² + 4 = 0 are α, β, γ. Find the cubic with roots α + 2, β + 2, γ + 2.', 'Let w = x + 2, so x = w − 2.', '(w − 2)³ − 3(w − 2)² + 4 = 0.', 'w³ − 6w² + 12w − 8 − 3w² + 12w − 12 + 4 = 0.', 'w³ − 9w² + 24w − 16 = 0.', 'Check: the sum of the new roots is 3 + 6 = 9, matching the w² coefficient.'),
  E('What a sum of squares can show', 'α, β, γ, δ are the roots of x⁴ − 2x³ + 3x² + 4x − 5 = 0. Find Σα² and explain what it shows.', 'Σα = 2 and Σαβ = 3.', 'Σα² = (Σα)² − 2Σαβ = 4 − 6.', 'Σα² = −2.', 'A sum of squares of real numbers cannot be negative, so the roots are not all real.')],
 [F('For x³ − 7x² + 2x + 5 = 0.', 'Σα = [[7]] and αβγ = [[-5]]'),
  F('Sum of squares.', 'Σα² = (Σα)² − [[2]]Σαβ'),
  F('New roots 3α.', 'substitute x = w/[[3]]')],
 [X('<p>The roots of x³ + 2x² − 3x + 4 = 0 are α, β and γ.</p>',
    P('Write down the values of α + β + γ, αβ + βγ + γα and αβγ.', [('B1', 'two correct'), ('B1', '−2, −3 and −4')]),
    P('Find α² + β² + γ².', [('M1', '(−2)² − 2(−3)'), ('A1', '10')], ans=10),
    P('Find α³ + β³ + γ³.', [('M1', 'uses α³ = −2α² + 3α − 4 for each root'), ('M1', '−2(10) + 3(−2) − 12'), ('A1', '−38')], ans=-38)),
  X('<p>The roots of x³ − 4x² + x + 6 = 0 are α, β and γ.</p>',
    P('Find a cubic equation with integer coefficients whose roots are 2α − 1, 2β − 1 and 2γ − 1.', [('M1', 'substitutes x = (w + 1)/2'), ('M1', 'multiplies through by 8 and expands'), ('A1', 'at least three correct coefficients'), ('A1', 'w³ − 5w² − 9w + 45 = 0')])),
  X('<p>The roots of 2x² − 6x + 7 = 0 are α and β.</p>',
    P('Find a quadratic equation with integer coefficients whose roots are α² and β².', [('B1', 'α + β = 3 and αβ = 7/2'), ('M1', 'α² + β² = 9 − 7 = 2'), ('M1', 'α²β² = 49/4'), ('A1', '4x² − 8x + 49 = 0')]))])

# ------------------------------------------------------------------ cp-series
for n in range(1, 12):
    assert sum(r * (2 * r - 1) for r in range(1, n + 1)) * 6 == n * (n + 1) * (4 * n - 1)
    assert close(sum(2 / ((2 * r - 1) * (2 * r + 1)) for r in range(1, n + 1)), 2 * n / (2 * n + 1))
    assert sum(r * r for r in range(n + 1, 2 * n + 1)) * 6 == n * (2 * n + 1) * (7 * n + 1)
    assert sum(r * (r + 3) for r in range(1, n + 1)) * 3 == n * (n + 1) * (n + 5)
    assert close(sum(1 / (r * (r + 2)) for r in range(1, n + 1)), 0.75 - (2 * n + 3) / (2 * (n + 1) * (n + 2)))
    assert sum(r ** 3 - r for r in range(1, n + 1)) * 4 == (n - 1) * n * (n + 1) * (n + 2)
assert sum(r * (r + 3) for r in range(11, 31)) == 10300 and sum(range(21)) == 210 and sum(r * r for r in range(11)) == 385 and sum(r ** 3 for r in range(6)) == 225
deep('cp-series',
 'Split a polynomial summand into standard sums and factorise as early as possible: n(n + 1) is almost always a common factor. For the method of differences, write out the first two and last two rows so the cancelling pattern is visible, and check the final formula with n = 1.',
 [E('Standard results', 'Show that Σ r(2r − 1) from r = 1 to n equals n(n + 1)(4n − 1)/6.', 'Σ r(2r − 1) = 2Σr² − Σr.', '= 2n(n + 1)(2n + 1)/6 − n(n + 1)/2.', '= n(n + 1)[2(2n + 1) − 3]/6.', '= n(n + 1)(4n − 1)/6; check n = 1: 1 × 2 × 3/6 = 1.'),
  E('Method of differences', 'Find Σ 2/[(2r − 1)(2r + 1)] from r = 1 to n.', '2/[(2r − 1)(2r + 1)] = 1/(2r − 1) − 1/(2r + 1).', 'r = 1: 1 − 1/3; r = 2: 1/3 − 1/5; … ; r = n: 1/(2n − 1) − 1/(2n + 1).', 'All the middle terms cancel.', 'Sum = 1 − 1/(2n + 1) = 2n/(2n + 1).'),
  E('A sum that does not start at 1', 'Find Σ r² from r = n + 1 to 2n in factorised form.', 'Sum = S(2n) − S(n), where S(n) = n(n + 1)(2n + 1)/6.', '= 2n(2n + 1)(4n + 1)/6 − n(n + 1)(2n + 1)/6.', '= n(2n + 1)[2(4n + 1) − (n + 1)]/6.', '= n(2n + 1)(7n + 1)/6.')],
 [F('Sum of the first 20 integers.', 'Σr = ½ × 20 × 21 = [[210]]'),
  F('Sum of the first 10 squares.', 'Σr² = 10 × 11 × 21/6 = [[385]]'),
  F('Sum of the first 5 cubes.', 'Σr³ = ¼ × 25 × 36 = [[225]]')],
 [X('',
    P('Show that Σ r(r + 3) from r = 1 to n equals n(n + 1)(n + 5)/3.', [('M1', 'splits into Σr² + 3Σr'), ('M1', 'substitutes both standard results'), ('M1', 'takes out the factor n(n + 1)/6'), ('A1', 'n(n + 1)(2n + 10)/6 = n(n + 1)(n + 5)/3')]),
    P('Hence evaluate Σ r(r + 3) from r = 11 to 30.', [('M1', 'S(30) − S(10) = 10 850 − 550'), ('A1', '10 300')], ans=10300)),
  X('',
    P('Express 1/[r(r + 2)] in partial fractions.', [('M1', 'A/r + B/(r + 2)'), ('A1', '½[1/r − 1/(r + 2)]')]),
    P('Hence show that Σ 1/[r(r + 2)] from r = 1 to n equals ¾ − (2n + 3)/[2(n + 1)(n + 2)].', [('M1', 'writes out the first and last terms'), ('M1', 'identifies the terms that do not cancel'), ('A1', '½[1 + ½ − 1/(n + 1) − 1/(n + 2)]'), ('A1', 'combines to the given form')]),
    P('State the sum to infinity.', [('B1', '¾')], ans=0.75)),
  X('', P('Show that Σ (r³ − r) from r = 1 to n equals ¼(n − 1)n(n + 1)(n + 2).', [('M1', '¼n²(n + 1)² − ½n(n + 1)'), ('M1', 'takes out ¼n(n + 1): n(n + 1)(n² + n − 2)/4'), ('A1', 'factorises n² + n − 2 = (n − 1)(n + 2)')]))])

# ------------------------------------------------------------------ cp-maclaurin
x = 0.01
assert close(math.log(1 + 2 * x), 2 * x - 2 * x * x + 8 * x ** 3 / 3, 1e-6) and close(math.exp(x) * math.cos(x), 1 + x - x ** 3 / 3, 1e-7)
assert close((1 - math.cos(2 * 1e-4)) / 1e-8, 2, 1e-5)
f = lambda t: math.log(1 + math.sin(t))
assert close(deriv2(f, 0.4), -1 / (1 + math.sin(0.4)), 1e-5) and close(f(x), x - x * x / 2 + x ** 3 / 6, 1e-7)
assert close((1 + 3 * x) * math.exp(-2 * x), 1 + x - 4 * x * x + 14 * x ** 3 / 3, 1e-6)
est = 0.5 - 0.5 ** 5 / 10 + 0.5 ** 9 / 216; assert round(est, 4) == 0.4969 and close(integ(lambda t: math.cos(t * t), 0, 0.5), est, 1e-6)
deep('cp-maclaurin',
 'Decide whether to differentiate repeatedly or to build the series from standard results: a composite of standard functions is usually quicker by substitution. Keep terms only up to the required power when multiplying, and quote the interval of validity when a logarithm or binomial series is involved.',
 [E('A logarithmic series', 'Find the Maclaurin series for ln(1 + 2x) up to the term in x³, stating the values of x for which it is valid.', 'ln(1 + u) = u − u²/2 + u³/3 − …, valid for −1 < u ≤ 1.', 'Replace u by 2x: 2x − (2x)²/2 + (2x)³/3.', 'ln(1 + 2x) = 2x − 2x² + (8/3)x³ − …', 'Valid when −1 < 2x ≤ 1, that is −½ < x ≤ ½.'),
  E('Multiplying two series', 'Find the series expansion of eˣ cos x up to the term in x³.', 'eˣ = 1 + x + x²/2 + x³/6 + … and cos x = 1 − x²/2 + …', 'Multiply, keeping terms up to x³: (1 + x + x²/2 + x³/6) − x²/2 − x³/2.', 'The x² terms cancel; x³: 1/6 − 1/2 = −1/3.', 'eˣ cos x = 1 + x − x³/3 + …'),
  E('A limit from a series', 'Use a series expansion to find the limit of (1 − cos 2x)/x² as x → 0.', 'cos 2x = 1 − (2x)²/2 + (2x)⁴/24 − …', '1 − cos 2x = 2x² − (2/3)x⁴ + …', '(1 − cos 2x)/x² = 2 − (2/3)x² + …', 'As x → 0 the limit is 2.')],
 [F('The x² coefficient in e^(3x).', '3²/2! = [[4.5]]'),
  F('The first two terms of sin x.', 'sin x ≈ x − x³/[[6]]'),
  F('Validity of ln(1 + x).', '−1 < x ≤ [[1]]')],
 [X('<p>f(x) = ln(1 + sin x), for −π/2 &lt; x &lt; π/2.</p>',
    P('Show that f″(x) = −1/(1 + sin x).', [('M1', 'f′(x) = cos x/(1 + sin x) and applies the quotient rule'), ('M1', 'uses sin²x + cos²x = 1 in the numerator: −(1 + sin x)'), ('A1', 'cancels to −1/(1 + sin x)')]),
    P('Find the Maclaurin series for f(x) up to and including the term in x³.', [('M1', 'f‴(x) = cos x/(1 + sin x)²'), ('M1', 'f(0) = 0, f′(0) = 1, f″(0) = −1, f‴(0) = 1'), ('A1', 'x − x²/2 + x³/6')])),
  X('',
    P('Write down the series expansion of e^(−2x) up to and including the term in x³.', [('M1', 'replaces x by −2x in the series for eˣ'), ('A1', '1 − 2x + 2x² − (4/3)x³')]),
    P('Hence find the series expansion of (1 + 3x)e^(−2x) up to and including the term in x³.', [('M1', 'multiplies and collects terms up to x³'), ('A1', '1 + x − 4x²'), ('A1', '+ (14/3)x³')])),
  X('', P('Use the first three non-zero terms of the series for cos x to estimate ∫ cos(x²) dx from 0 to 0.5, giving your answer to 4 decimal places.', [('M1', 'replaces x by x² in the cosine series'), ('A1', '1 − x⁴/2 + x⁸/24'), ('M1', 'integrates term by term: x − x⁵/10 + x⁹/216'), ('A1', '0.4969')], ans=0.4969, tol=2e-4))])

# ------------------------------------------------------------------ cp-improper
assert close(integ(lambda t: t ** -0.5, 1e-10, 1, 200000), 2, 2e-3) and close(integ(lambda t: t * math.exp(-t), 0, 60), 1, 1e-6)
assert close(math.pi * integ(lambda y: y, 0, 4), 8 * math.pi) and close(integ(lambda t: 1 / (t * (t + 1)), 1, 4000, 400000), math.log(2), 1e-3)
assert close(integ(lambda t: math.sin(t) ** 2, 0, math.pi) / math.pi, 0.5) and close(math.pi * integ(lambda t: math.exp(-2 * t), 0, math.log(2)), 3 * math.pi / 8)
deep('cp-improper',
 'Name what makes the integral improper, an infinite limit or an unbounded integrand, and replace that limit by a letter before integrating. Convergence is decided by the limit of the evaluated expression, so write that limit step explicitly; for volumes, square the function first and keep π outside.',
 [E('An unbounded integrand', 'Evaluate ∫ x^(−1/2) dx from 0 to 1.', 'The integrand is unbounded at x = 0, so use the lower limit a and let a → 0⁺.', '∫ x^(−1/2) dx from a to 1 = [2√x] = 2 − 2√a.', 'As a → 0⁺, 2√a → 0.', 'The integral converges to 2.'),
  E('An infinite limit with integration by parts', 'Evaluate ∫ xe^(−x) dx from 0 to ∞.', 'By parts with u = x, dv/dx = e^(−x): ∫ xe^(−x) dx = −xe^(−x) − e^(−x).', 'From 0 to t: −te^(−t) − e^(−t) + 1.', 'As t → ∞, te^(−t) → 0 and e^(−t) → 0.', 'The integral converges to 1.'),
  E('Rotation about the y-axis', 'The region bounded by y = x², the y-axis and y = 4 (x ≥ 0) is rotated through 2π about the y-axis. Find the volume.', 'About the y-axis, V = π∫ x² dy.', 'Here x² = y, so V = π∫ y dy from 0 to 4.', '= π[y²/2] = π × 8.', 'V = 8π.')],
 [F('An infinite limit.', '∫ x⁻³ dx from 1 to ∞ = [[0.5]]'),
  F('An exponential tail.', '∫ e^(−2x) dx from 0 to ∞ = [[0.5]]'),
  F('Mean value of x² on [0, 3].', '(1/3) × 9 = [[3]]')],
 [X('', P('Show that ∫ 1/[x(x + 1)] dx from 1 to ∞ converges and find its exact value.', [('M1', 'partial fractions: 1/x − 1/(x + 1)'), ('A1', 'ln x − ln(x + 1) = ln[x/(x + 1)]'), ('M1', 'considers the limit as the upper limit t → ∞'), ('A1', 'ln[t/(t + 1)] → ln 1 = 0'), ('A1', '0 − ln ½ = ln 2')], ans=math.log(2))),
  X('<p>The region R lies under the curve y = 1/x for x ≥ 1 and above the x-axis.</p>',
    P('Show that the area of R is not finite.', [('M1', '∫ 1/x dx from 1 to t = ln t'), ('A1', 'ln t → ∞ as t → ∞, so the integral diverges')]),
    P('R is rotated through 2π about the x-axis. Show that the volume generated is finite and find it.', [('M1', 'π∫ x⁻² dx from 1 to t'), ('A1', 'π(1 − 1/t)'), ('A1', 'limit π')], ans=math.pi)),
  X('',
    P('Find the mean value of sin²x over the interval 0 ≤ x ≤ π.', [('M1', '(1/π)∫ sin²x dx from 0 to π'), ('M1', 'uses sin²x = ½(1 − cos 2x)'), ('A1', '½')], ans=0.5),
    P('The curve y = e^(−x), 0 ≤ x ≤ ln 2, is rotated through 2π about the x-axis. Find the exact volume generated.', [('M1', 'π∫ e^(−2x) dx'), ('A1', 'π[−½e^(−2x)] from 0 to ln 2'), ('A1', '3π/8')], ans=3 * math.pi / 8))])

# ------------------------------------------------------------------ cp-inverse-calculus
assert close(deriv(lambda t: math.asin(2 * t), 0.2), 2 / math.sqrt(1 - 0.16), 1e-6)
assert close(integ(lambda t: 1 / (t * t + 4 * t + 13), 0, 1), (math.atan(1) - math.atan(2 / 3)) / 3, 1e-7)
assert close(integ(lambda t: 1 / math.sqrt(4 - t * t), 0, 1), math.pi / 6, 1e-7) and close(deriv(lambda t: math.atan(3 * t), 1 / 3), 1.5, 1e-6)
assert close(integ(lambda t: 1 / math.sqrt(9 - 4 * t * t), 0, 0.75), math.pi / 12, 1e-7)
assert close(integ(lambda t: (2 * t + 3) / (t * t + 9), 0, 3), math.log(2) + math.pi / 4, 1e-7)
deep('cp-inverse-calculus',
 'Match the integrand to a standard form before anything else: a² + x² leads to arctan, √(a² − x²) to arcsin. Complete the square to create that form, take any constant factor out so the coefficient of x² is 1, and check the answer by differentiating.',
 [E('Differentiating an inverse sine', 'Differentiate arcsin 2x with respect to x.', 'Let y = arcsin 2x, so sin y = 2x.', 'cos y dy/dx = 2.', 'cos y = √(1 − sin²y) = √(1 − 4x²), positive because −π/2 ≤ y ≤ π/2.', 'dy/dx = 2/√(1 − 4x²).'),
  E('Completing the square', 'Find ∫ 1/(x² + 4x + 13) dx.', 'x² + 4x + 13 = (x + 2)² + 9.', 'This is 1/(u² + a²) with u = x + 2 and a = 3.', '∫ 1/(u² + 3²) du = ⅓ arctan(u/3).', '⅓ arctan((x + 2)/3) + c.'),
  E('A definite inverse-sine integral', 'Evaluate ∫ 1/√(4 − x²) dx from 0 to 1.', '∫ 1/√(a² − x²) dx = arcsin(x/a) with a = 2.', '[arcsin(x/2)] from 0 to 1 = arcsin ½ − arcsin 0.', '= π/6.')],
 [F('Gradient of y = arctan x at x = 1.', '1/(1 + 1²) = [[0.5]]'),
  F('A standard definite integral.', '∫ 1/(1 + x²) dx from 0 to 1 = π/[[4]]'),
  F('Completing the square.', 'x² + 6x + 13 = (x + [[3]])² + [[4]]')],
 [X('',
    P('Show that d/dx(arctan x) = 1/(1 + x²).', [('M1', 'tan y = x, so sec²y dy/dx = 1'), ('M1', 'uses sec²y = 1 + tan²y = 1 + x²'), ('A1', 'dy/dx = 1/(1 + x²)')]),
    P('Find the gradient of the curve y = arctan 3x at the point where x = ⅓.', [('M1', 'dy/dx = 3/(1 + 9x²)'), ('A1', '3/2')], ans=1.5)),
  X('', P('Find the exact value of ∫ 1/√(9 − 4x²) dx from 0 to ¾.', [('M1', 'obtains k arcsin(2x/3)'), ('A1', 'k = ½'), ('M1', 'substitutes the limits: ½ arcsin ½'), ('A1', 'π/12')], ans=math.pi / 12)),
  X('',
    P('Find ∫ (2x + 3)/(x² + 9) dx.', [('M1', 'splits into 2x/(x² + 9) + 3/(x² + 9)'), ('A1', 'ln(x² + 9)'), ('M1', 'k arctan(x/3)'), ('A1', 'ln(x² + 9) + arctan(x/3) + c')]),
    P('Hence find the exact value of the integral from 0 to 3.', [('M1', 'ln 18 − ln 9 + arctan 1'), ('A1', 'ln 2 + π/4')], ans=math.log(2) + math.pi / 4))])

# ------------------------------------------------------------------ cp-vector-lines
v = lambda *a: np.array(a, dtype=float)
assert np.allclose(v(1, 2, 3) + 2 * v(1, -1, 2), v(4, 1, 6) - v(1, 1, -1)) and np.allclose(v(1, 2, 3) + 2 * v(1, -1, 2), v(3, 0, 7))
assert round(math.degrees(math.acos(abs(v(1, -1, 2) @ v(1, 1, -1)) / (math.sqrt(6) * math.sqrt(3)))), 1) == 61.9
AP, d = v(2, 1, 3), v(2, 1, 2); assert close(AP @ AP - (AP @ d) ** 2 / (d @ d), 5 / 9)
assert v(2, -1, 3) @ v(1, 4, 2) == 4 and close(np.linalg.norm(v(2, 3, 6)), 7) and v(1, 2, -2) @ v(2, 1, 2) == 0
assert np.allclose(v(2, -1, 0) + v(1, 2, -1), v(5, 2, -3) - v(2, 1, -2)) and np.allclose(v(2, -1, 0) + v(1, 2, -1), v(3, 1, -1))
assert round(math.degrees(math.acos(v(1, 2, -1) @ v(2, 1, -2) / (math.sqrt(6) * 3))), 1) == 35.3
Pt = v(1, 2, -1) + 0.5 * v(1, -1, 2); assert np.allclose(Pt, v(1.5, 1.5, 0)) and close(Pt @ v(1, -1, 2), 0) and close(np.linalg.norm(Pt), 3 / math.sqrt(2))
deep('cp-vector-lines',
 'Use different parameters for different lines and solve two component equations before testing the third: that test is what separates intersecting from skew lines. Angles between lines come from direction vectors only, and the shortest distance from a point to a line uses a perpendicular, found with a zero scalar product.',
 [E('Do two lines meet?', 'l₁: r = (1,2,3) + λ(1,−1,2) and l₂: r = (4,1,6) + μ(1,1,−1). Show that the lines intersect and find the point of intersection.', 'x: 1 + λ = 4 + μ; y: 2 − λ = 1 + μ.', 'Adding: 3 = 5 + 2μ, so μ = −1 and λ = 2.', 'z: 3 + 2λ = 7 and 6 − μ = 7, so the third equation is satisfied.', 'The lines meet at (3, 0, 7).'),
  E('Angle between two lines', 'Find the acute angle between the lines in the previous example.', 'Use the directions a = (1,−1,2) and b = (1,1,−1).', 'a·b = 1 − 1 − 2 = −2, |a| = √6 and |b| = √3.', 'cos θ = |−2|/(√6 √3) = 2/√18, taking the modulus for the acute angle.', 'θ = 61.9° (1 d.p.).'),
  E('Distance from a point to a line', 'Find the shortest distance from P(3,1,2) to the line r = (1,0,−1) + t(2,1,2).', 'With A(1,0,−1): AP = (2,1,3) and d = (2,1,2).', 'The foot of the perpendicular has t = AP·d/|d|² = 11/9.', 'Distance² = |AP|² − (AP·d)²/|d|² = 14 − 121/9 = 5/9.', 'Shortest distance = √5/3 ≈ 0.745.')],
 [F('Scalar product.', '(2,−1,3)·(1,4,2) = [[4]]'),
  F('Magnitude.', '|(2,3,6)| = [[7]]'),
  F('Perpendicular vectors: (1,2,−2)·(2,1,k) = 0.', 'k = [[2]]')],
 [X('<p>l₁: r = (2,−1,0) + λ(1,2,−1) and l₂: r = (5,2,−3) + μ(2,1,−2).</p>',
    P('Show that l₁ and l₂ intersect and find the coordinates of the point of intersection.', [('M1', 'equates two components'), ('M1', 'solves the pair of equations'), ('A1', 'λ = 1, μ = −1'), ('M1', 'checks the third component'), ('A1', '(3, 1, −1)')]),
    P('Find the acute angle between l₁ and l₂, to 1 decimal place.', [('M1', 'scalar product of the directions: 2 + 2 + 2 = 6'), ('A1', 'cos θ = 6/(3√6)'), ('A1', '35.3°')], ans=35.3, tol=2e-3, unit='°')),
  X('<p>A has coordinates (1, 2, −1) and B has coordinates (3, 0, 3).</p>',
    P('Find a vector equation of the line AB.', [('M1', 'direction AB = (2,−2,4)'), ('A1', 'r = (1,2,−1) + t(1,−1,2), or equivalent')]),
    P('Find the coordinates of the point P on AB that is closest to the origin, and the distance OP.', [('M1', 'general point (1 + t, 2 − t, −1 + 2t)'), ('M1', 'OP·(1,−1,2) = 0'), ('A1', 't = ½'), ('A1', 'P(3/2, 3/2, 0) and OP = 3/√2')])),
  X('<p>l₁: r = (1,0,0) + λ(1,1,0) and l₂: r = (0,1,3) + μ(0,1,1).</p>',
    P('Show that l₁ and l₂ are skew.', [('M1', 'equates components: 1 + λ = 0, λ = 1 + μ, 0 = 3 + μ'), ('M1', 'solves two of them: λ = −1, μ = −2'), ('A1', 'the third gives μ = −3, a contradiction'), ('A1', 'directions are not parallel, so the lines are skew')]))])

# ------------------------------------------------------------------ cp-planes
n = np.cross(v(1, 1, -1), v(-1, 2, 2)); assert np.allclose(n, v(4, -1, 3))
for pt in (v(1, 0, 1), v(2, 1, 0), v(0, 2, 3)): assert close(n @ pt, 7)
assert round(math.degrees(math.asin(abs(v(1, 2, 2) @ v(2, -1, 2)) / 9)), 1) == 26.4
assert np.allclose(np.cross(v(1, 1, 1), v(1, -1, 2)), v(3, -1, -2))
pt = v(1, 3, -2) + 2 * v(2, 1, 1); assert np.allclose(pt, v(5, 5, 0)) and close(v(2, -1, 2) @ pt, 5)
assert round(math.degrees(math.asin(abs(v(2, 1, 1) @ v(2, -1, 2)) / (math.sqrt(6) * 3))), 1) == 42.9 and close(abs(v(2, -1, 2) @ v(1, 3, -2) - 5) / 3, 10 / 3)
assert round(math.degrees(math.acos(abs(v(1, 2, -2) @ v(2, -1, 2)) / 9)), 1) == 63.6
assert close(v(1, -2, 3) @ v(2, 1, -1), -3) and np.allclose(v(4, -3, 5) - 2 * v(1, -2, 3), v(2, 1, -1))
deep('cp-planes',
 'Identify the normal vector first, because it controls every plane calculation: the equation r·n = a·n, the angle with a line (90° minus the angle with the normal) and the perpendicular distance. Substituting a line into a plane gives one linear equation in the parameter, so interpret the outcome: one value, none or all.',
 [E('A plane through three points', 'Find a Cartesian equation of the plane through A(1,0,1), B(2,1,0) and C(0,2,3).', 'AB = (1,1,−1) and AC = (−1,2,2).', 'A normal n = (a,b,c) satisfies a + b − c = 0 and −a + 2b + 2c = 0.', 'Adding: 3b + c = 0; taking b = −1 gives c = 3 and a = 4, so n = (4,−1,3).', 'r·n = a·n: 4x − y + 3z = 4 + 0 + 3.', '4x − y + 3z = 7; check B: 8 − 1 + 0 = 7 and C: 0 − 2 + 9 = 7.'),
  E('Angle between a line and a plane', 'Find the angle between the line with direction (1,2,2) and the plane 2x − y + 2z = 5.', 'The normal to the plane is n = (2,−1,2).', 'The angle φ between the line and the normal has cos φ = |2 − 2 + 4|/(3 × 3) = 4/9.', 'The angle between the line and the plane is θ = 90° − φ, so sin θ = 4/9.', 'θ = 26.4° (1 d.p.).'),
  E('Line of intersection of two planes', 'Find a vector equation of the line in which x + y + z = 3 and x − y + 2z = 2 meet.', 'A direction d is perpendicular to both normals: d·(1,1,1) = 0 and d·(1,−1,2) = 0.', 'Solving gives d = (3,−1,−2).', 'A common point: put z = 0, then x + y = 3 and x − y = 2, so x = 5/2, y = 1/2.', 'r = (5/2, 1/2, 0) + t(3,−1,−2).')],
 [F('Distance from the origin to 2x + 3y + 6z = 14.', '14/√(4 + 9 + 36) = [[2]]'),
  F('Planes with normals (1,0,0) and (0,1,0).', 'angle between them = [[90]]°'),
  F('The point (1, 2, 3) lies on x + y + z = d.', 'd = [[6]]')],
 [X('<p>The plane Π has equation 2x − y + 2z = 5 and the line l has equation r = (1,3,−2) + λ(2,1,1).</p>',
    P('Find the coordinates of the point where l meets Π.', [('M1', 'substitutes: 2(1 + 2λ) − (3 + λ) + 2(−2 + λ) = 5'), ('A1', 'λ = 2'), ('A1', '(5, 5, 0)')]),
    P('Find the acute angle between l and Π, to 1 decimal place.', [('M1', 'scalar product of (2,1,1) with the normal (2,−1,2): 5'), ('M1', 'sin θ = 5/(3√6)'), ('A1', '42.9°')], ans=42.9, tol=2e-3, unit='°'),
    P('Find the perpendicular distance from the point (1, 3, −2) to Π.', [('M1', '|2 − 3 − 4 − 5|/√(4 + 1 + 4)'), ('A1', '10/3')], ans=10 / 3)),
  X('', P('Find the acute angle between the planes x + 2y − 2z = 5 and 2x − y + 2z = 1, to 1 decimal place.', [('M1', 'scalar product of the normals: 2 − 2 − 4 = −4'), ('A1', 'cos θ = 4/9'), ('A1', '63.6°')], ans=63.6, tol=2e-3, unit='°')),
  X('<p>The plane Π passes through A(2, 1, −1) and is perpendicular to the vector (1,−2,3).</p>',
    P('Find a Cartesian equation of Π.', [('M1', 'x − 2y + 3z = (2,1,−1)·(1,−2,3)'), ('A1', 'x − 2y + 3z = −3')]),
    P('Find the coordinates of the foot of the perpendicular from Q(4, −3, 5) to Π.', [('M1', 'line through Q along the normal: (4 + t, −3 − 2t, 5 + 3t)'), ('M1', 'substitutes into Π: 25 + 14t = −3'), ('A1', 't = −2, giving (2, 1, −1)')]))])

# ------------------------------------------------------------------ cp-polar
assert close(integ(lambda t: 0.5 * (2 * (1 + math.cos(t))) ** 2, 0, 2 * math.pi), 6 * math.pi)
for t in (math.pi / 3, -math.pi / 3): assert abs(deriv(lambda u: (1 + math.cos(u)) * math.sin(u), t)) < 1e-6
assert close(integ(lambda t: 0.5 * (3 + 2 * math.cos(t)) ** 2, 0, 2 * math.pi), 11 * math.pi)
assert close(integ(lambda t: 0.5 * (2 * math.sin(2 * t)) ** 2, 0, math.pi / 2), math.pi / 2)
for t in (0, 2 * math.pi / 3, -2 * math.pi / 3): assert abs(deriv(lambda u: 2 * (1 + math.cos(u)) * math.cos(u), t)) < 1e-6
assert close(2 * (1 + math.cos(2 * math.pi / 3)), 1)
deep('cp-polar',
 'Sketch the curve from a short table of θ and r before integrating, so that the limits describe the region once and only once. Area uses ½∫r² dθ, tangents parallel to the initial line come from d(r sin θ)/dθ = 0, and tangents perpendicular to it from d(r cos θ)/dθ = 0.',
 [E('Area of a cardioid', 'Find the area enclosed by the cardioid r = 2(1 + cos θ).', 'Area = ½∫ r² dθ from 0 to 2π = 2∫ (1 + 2cos θ + cos²θ) dθ.', 'cos²θ = ½(1 + cos 2θ), so the integrand is 3/2 + 2cos θ + ½cos 2θ.', 'Over a full turn the cosine terms integrate to 0.', 'Area = 2 × (3/2)(2π) = 6π.'),
  E('Tangents parallel to the initial line', 'Find the points on r = 1 + cos θ where the tangent is parallel to the initial line.', 'y = r sin θ = sin θ + sin θ cos θ.', 'dy/dθ = cos θ + cos 2θ = 2cos²θ + cos θ − 1.', '(2cos θ − 1)(cos θ + 1) = 0, so cos θ = ½ or cos θ = −1.', 'θ = ±π/3, where r = 3/2; θ = π is the pole, where the curve has a cusp.'),
  E('Where two curves meet', 'Find the polar coordinates of the points where r = 1 + cos θ meets r = 3cos θ.', '1 + cos θ = 3cos θ.', 'cos θ = ½, so θ = ±π/3.', 'r = 3 × ½ = 3/2.', 'The curves meet at (3/2, π/3) and (3/2, −π/3); both also pass through the pole, for different values of θ.')],
 [F('The circle r = 2 in Cartesian form.', 'x² + y² = [[4]]'),
  F('Area inside r = 3 for 0 ≤ θ ≤ π/2.', '½ × 9 × π/2 = [[2.25]]π'),
  F('The circle r = 4cos θ at θ = π/3.', 'r = [[2]]')],
 [X('<p>The curve C has polar equation r = 3 + 2cos θ, 0 ≤ θ &lt; 2π.</p>',
    P('State the greatest and least values of r and the values of θ at which they occur.', [('B1', 'greatest r = 5 at θ = 0'), ('B1', 'least r = 1 at θ = π')]),
    P('Find the exact area enclosed by C.', [('M1', '½∫ (3 + 2cos θ)² dθ from 0 to 2π'), ('M1', 'expands: 9 + 12cos θ + 4cos²θ'), ('M1', 'uses cos²θ = ½(1 + cos 2θ)'), ('A1', '½[11θ + 12sin θ + sin 2θ] from 0 to 2π'), ('A1', '11π')], ans=11 * math.pi)),
  X('<p>The curve C has polar equation r = 2sin 2θ, 0 ≤ θ ≤ π/2.</p>',
    P('Find the exact area enclosed by this loop of C.', [('M1', '½∫ 4sin²2θ dθ from 0 to π/2'), ('M1', 'uses sin²2θ = ½(1 − cos 4θ)'), ('A1', '[θ − ¼sin 4θ] from 0 to π/2'), ('A1', 'π/2')], ans=math.pi / 2),
    P('State the greatest value of r on the loop and the value of θ at which it occurs.', [('B1', 'r = 2 at θ = π/4')])),
  X('', P('Find the polar coordinates of the points on the curve r = 2(1 + cos θ), −π &lt; θ ≤ π, at which the tangent is perpendicular to the initial line.', [('M1', 'x = r cos θ = 2cos θ + 2cos²θ'), ('M1', 'differentiates with respect to θ'), ('A1', '−2sin θ(1 + 2cos θ) = 0'), ('A1', '(4, 0)'), ('A1', '(1, 2π/3) and (1, −2π/3); θ = π is the cusp at the pole')]))])

# ------------------------------------------------------------------ cp-hyperbolic
for xx in (0.0, math.log(3)): assert close(2 * math.cosh(xx) - math.sinh(xx), 2)
assert close(math.asinh(0.75), math.log(2)) and close(math.sinh(math.log(2)), 0.75) and close(math.acosh(1.25), math.log(2))
xr = math.log((3 + math.sqrt(5)) / 2); assert close(math.sinh(2 * xr), 3 * math.sinh(xr)) and close(math.cosh(xr), 1.5) and round(xr, 4) == 0.9624
assert close(5 * math.cosh(-math.log(2)) + 3 * math.sinh(-math.log(2)), 4)
assert close(integ(lambda t: 1 / math.sqrt(1 + t * t), 0, 0.75), math.log(2), 1e-7) and close(deriv(math.asinh, 0.6), 1 / math.sqrt(1.36), 1e-6)
deep('cp-hyperbolic',
 'Most equations become a quadratic in eˣ once the definitions are substituted, so multiply through by eˣ and reject any non-positive value of eˣ. Remember that cosh is even, so cosh x = k gives two solutions when k > 1, and that the identities differ from the trigonometric ones by the sign attached to sinh².',
 [E('An equation in sinh and cosh', 'Solve 2cosh x − sinh x = 2.', '(eˣ + e⁻ˣ) − ½(eˣ − e⁻ˣ) = 2.', '½eˣ + (3/2)e⁻ˣ = 2; multiply by 2eˣ: e²ˣ − 4eˣ + 3 = 0.', '(eˣ − 1)(eˣ − 3) = 0.', 'x = 0 or x = ln 3.'),
  E('Proving an identity', 'Prove that cosh²x − sinh²x = 1.', 'cosh²x = ¼(e²ˣ + 2 + e⁻²ˣ).', 'sinh²x = ¼(e²ˣ − 2 + e⁻²ˣ).', 'Subtracting: ¼(2 + 2).', 'cosh²x − sinh²x = 1.'),
  E('An inverse hyperbolic value', 'Find the exact value of arsinh(¾).', 'arsinh x = ln(x + √(x² + 1)).', '√(9/16 + 1) = 5/4.', 'arsinh(¾) = ln(¾ + 5/4).', '= ln 2.')],
 [F('Value at the origin.', 'cosh 0 = [[1]]'),
  F('From the definition.', 'sinh(ln 2) = ½(2 − ½) = [[0.75]]'),
  F('Logarithmic form.', 'arcosh(5/4) = ln(5/4 + ¾) = ln [[2]]')],
 [X('',
    P('Using the definitions in terms of exponentials, prove that sinh 2x = 2sinh x cosh x.', [('M1', 'substitutes the exponential definitions'), ('M1', 'multiplies: 2 × ¼(eˣ − e⁻ˣ)(eˣ + e⁻ˣ)'), ('A1', '½(e²ˣ − e⁻²ˣ) = sinh 2x')]),
    P('Hence solve sinh 2x = 3sinh x, giving non-zero answers as exact logarithms.', [('M1', 'sinh x(2cosh x − 3) = 0'), ('A1', 'x = 0'), ('M1', 'cosh x = 3/2 and uses arcosh x = ln(x + √(x² − 1))'), ('A1', 'x = ±ln[(3 + √5)/2]')])),
  X('', P('Solve 5cosh x + 3sinh x = 4, giving your answer as an exact logarithm.', [('M1', 'substitutes the exponential definitions'), ('A1', '4e²ˣ − 4eˣ + 1 = 0'), ('M1', '(2eˣ − 1)² = 0'), ('A1', 'x = −ln 2')], ans=-math.log(2))),
  X('',
    P('Show that d/dx(arsinh x) = 1/√(1 + x²).', [('M1', 'sinh y = x, so cosh y dy/dx = 1'), ('M1', 'cosh y = √(1 + sinh²y), positive'), ('A1', 'dy/dx = 1/√(1 + x²)')]),
    P('Hence find the exact value of ∫ 1/√(1 + x²) dx from 0 to ¾.', [('M1', '[arsinh x] from 0 to ¾'), ('A1', 'ln 2')], ans=math.log(2)))])

# ------------------------------------------------------------------ cp-de-first
def resid(y, rhs, x): return deriv(y, x) - rhs(x, y(x))
for C in (0.0, 2.5):
    assert abs(resid(lambda t: t ** 3 / 4 + C / t, lambda t, y: t * t - y / t, 1.3)) < 1e-6
    assert abs(resid(lambda t: math.exp(3 * t) + C * math.exp(2 * t), lambda t, y: math.exp(3 * t) + 2 * y, 0.4)) < 1e-5
    assert abs(resid(lambda t: t * t + C / t ** 2, lambda t, y: 4 * t - 2 * y / t, 1.7)) < 1e-6
    assert abs(resid(lambda t: (t + C) * math.cos(t), lambda t, y: math.cos(t) - y * math.tan(t), 0.6)) < 1e-6
assert abs(resid(lambda t: 200 * (1 - math.exp(-0.03 * t)), lambda t, m: 6 - 0.03 * m, 7)) < 1e-6
assert close(4 + 2 / 4, 4.5) and close((math.pi + 2) * math.cos(math.pi), -(math.pi + 2))
assert abs(resid(lambda t: 49 * (1 - math.exp(-0.2 * t)), lambda t, w: 9.8 - 0.2 * w, 3)) < 1e-6 and round(5 * math.log(2), 3) == 3.466
deep('cp-de-first',
 'Rearrange to dy/dx + P(x)y = Q(x) with coefficient 1 on dy/dx before finding the integrating factor e^(∫P dx). Recognise the left side as the derivative of (integrating factor × y), integrate once with a constant, and apply the boundary condition only after that constant is in place.',
 [E('Integrating factor with a power of x', 'Find the general solution of dy/dx + y/x = x², x > 0.', 'P = 1/x, so the integrating factor is e^(ln x) = x.', 'x dy/dx + y = x³, that is d(xy)/dx = x³.', 'xy = x⁴/4 + C.', 'y = x³/4 + C/x.'),
  E('Integrating factor with an exponential', 'Find the general solution of dy/dx − 2y = e^(3x).', 'Integrating factor e^(−2x).', 'd(ye^(−2x))/dx = e^(3x) e^(−2x) = eˣ.', 'ye^(−2x) = eˣ + C.', 'y = e^(3x) + Ce^(2x).'),
  E('A mixing model', 'A tank holds 100 litres of water. Brine containing 2 g of salt per litre flows in at 3 litres per minute and the mixture flows out at the same rate. Initially there is no salt. Find the mass m grams of salt after t minutes.', 'Rate in = 6 g/min; rate out = 3 × m/100 g/min, so dm/dt = 6 − 0.03m.', 'dm/dt + 0.03m = 6 has integrating factor e^(0.03t).', 'me^(0.03t) = 200e^(0.03t) + C.', 'm(0) = 0 gives C = −200.', 'm = 200(1 − e^(−0.03t)); the mass approaches 200 g.')],
 [F('Integrating factor for y′ + 3y = x.', 'e^([[3]]x)'),
  F('Integrating factor for y′ + (2/x)y = 1, x > 0.', 'x to the power [[2]]'),
  F('y′ + y = 0 with y(0) = 5.', 'y = 5e^(−x), so y(ln 5) = [[1]]')],
 [X('<p>dy/dx + 2y/x = 4x, x &gt; 0.</p>',
    P('Find the general solution of the differential equation.', [('B1', 'integrating factor x²'), ('M1', 'd(x²y)/dx = 4x³'), ('A1', 'x²y = x⁴ + C'), ('A1', 'y = x² + C/x²')]),
    P('Given that y = 3 when x = 1, find the value of y when x = 2.', [('M1', 'C = 2'), ('A1', '4.5')], ans=4.5)),
  X('<p>dy/dx + y tan x = cos x, with y = 2 when x = 0.</p>',
    P('Find y in terms of x and hence the value of y when x = π.', [('B1', 'integrating factor sec x'), ('M1', 'd(y sec x)/dx = 1'), ('A1', 'y sec x = x + C'), ('M1', 'uses y(0) = 2'), ('A1', 'y = (x + 2)cos x'), ('A1', 'y(π) = −(π + 2)')], ans=-(math.pi + 2))),
  X('<p>A particle falls from rest. Its speed v m s⁻¹ after t seconds satisfies dv/dt = 9.8 − 0.2v.</p>',
    P('Find v in terms of t.', [('B1', 'integrating factor e^(0.2t)'), ('M1', 've^(0.2t) = 49e^(0.2t) + C'), ('A1', 'C = −49 from v(0) = 0'), ('A1', 'v = 49(1 − e^(−0.2t))')]),
    P('State the terminal speed.', [('B1', '49 m s⁻¹')], ans=49, unit='m s⁻¹'),
    P('Find the time taken to reach half the terminal speed, to 3 significant figures.', [('M1', 'e^(−0.2t) = ½'), ('A1', 't = 5 ln 2 = 3.47 s')], ans=5 * math.log(2), tol=2e-3, unit='s'))])

# ------------------------------------------------------------------ cp-de-second
def ode2(y, a, b, c, rhs, x): return a * deriv2(y, x) + b * deriv(y, x) + c * y(x) - rhs(x)
y1 = lambda t: (1 + 2 * t) * math.exp(-2 * t); assert abs(ode2(y1, 1, 4, 4, lambda t: 0, 0.7)) < 1e-5 and close(y1(0), 1) and abs(deriv(y1, 0)) < 1e-6
assert abs(ode2(lambda t: math.exp(-t) * (1.3 * math.cos(2 * t) - 0.4 * math.sin(2 * t)), 1, 2, 5, lambda t: 0, 0.5)) < 1e-5
assert abs(ode2(lambda t: 2 * math.exp(t) - math.exp(2 * t) + 2 * t + 3, 1, -3, 2, lambda t: 4 * t, 0.5)) < 1e-4
y3 = lambda t: math.exp(t) + math.exp(3 * t) + 2 * t + 1; assert abs(ode2(y3, 1, -4, 3, lambda t: 6 * t - 5, 0.3)) < 1e-4 and close(y3(0), 3) and close(deriv(y3, 0), 6, 1e-6)
assert abs(ode2(lambda t: math.exp(-t) * (0.7 * math.cos(3 * t) + 1.1 * math.sin(3 * t)), 1, 2, 10, lambda t: 0, 0.5)) < 1e-4
y4 = lambda t: math.sin(2 * t) + 4 * math.sin(t); assert abs(ode2(y4, 1, 0, 4, lambda t: 12 * math.sin(t), 0.8)) < 1e-5 and close(y4(0), 0) and close(deriv(y4, 0), 6, 1e-6)
deep('cp-de-second',
 'Solve the auxiliary equation and classify its roots before writing anything else: two real roots, a repeated root and complex roots each have their own form of complementary function. Choose a particular integral that matches the right-hand side, and apply initial conditions only to the full general solution.',
 [E('A repeated root', 'Solve y″ + 4y′ + 4y = 0 given that y = 1 and y′ = 0 when x = 0.', 'Auxiliary equation m² + 4m + 4 = 0 has the repeated root m = −2.', 'y = (A + Bx)e^(−2x).', 'y(0) = 1 gives A = 1.', 'y′ = (B − 2A − 2Bx)e^(−2x), so y′(0) = B − 2 = 0 and B = 2.', 'y = (1 + 2x)e^(−2x).'),
  E('Complex roots', 'Find the general solution of y″ + 2y′ + 5y = 0.', 'm² + 2m + 5 = 0 gives m = −1 ± 2i.', 'The real part gives the exponential factor and the imaginary part the frequency.', 'y = e^(−x)(A cos 2x + B sin 2x).'),
  E('A polynomial particular integral', 'Find the general solution of y″ − 3y′ + 2y = 4x.', 'm² − 3m + 2 = 0 gives m = 1, 2, so the complementary function is Aeˣ + Be^(2x).', 'Try y = ax + b: then y′ = a and y″ = 0.', '−3a + 2ax + 2b = 4x gives a = 2 and b = 3.', 'y = Aeˣ + Be^(2x) + 2x + 3.')],
 [F('Auxiliary equation m² − 5m + 6 = 0.', 'm = [[2]] or m = [[3]]'),
  F('General solution of y″ + 9y = 0.', 'y = A cos [[3]]x + B sin [[3]]x'),
  F('Particular integral for y″ + y = 10.', 'y = [[10]]')],
 [X('<p>y″ − 4y′ + 3y = 6x − 5.</p>',
    P('Find the complementary function.', [('M1', 'm² − 4m + 3 = 0, m = 1 or 3'), ('A1', 'Aeˣ + Be^(3x)')]),
    P('Find a particular integral.', [('M1', 'tries y = ax + b'), ('M1', '−4a + 3ax + 3b = 6x − 5'), ('A1', 'y = 2x + 1')]),
    P('Given that y = 3 and y′ = 6 when x = 0, find y in terms of x.', [('M1', 'A + B + 1 = 3 and A + 3B + 2 = 6'), ('A1', 'A = 1, B = 1'), ('A1', 'y = eˣ + e^(3x) + 2x + 1')])),
  X('<p>y″ + 2y′ + 10y = 0.</p>',
    P('Find the general solution.', [('M1', 'm² + 2m + 10 = 0'), ('A1', 'm = −1 ± 3i'), ('A1', 'y = e^(−x)(A cos 3x + B sin 3x)')]),
    P('Describe the behaviour of y as x → ∞.', [('B1', 'oscillations whose amplitude decays to zero')])),
  X('', P('Solve y″ + 4y = 12sin x, given that y = 0 and y′ = 6 when x = 0.', [('M1', 'complementary function from m² + 4 = 0'), ('A1', 'A cos 2x + B sin 2x'), ('M1', 'particular integral of the form λ sin x + μ cos x'), ('A1', '4sin x'), ('M1', 'applies both conditions to the general solution'), ('A1', 'y = sin 2x + 4sin x')]))])

# ------------------------------------------------------------------ cp-coupled
A_, B_ = 1.3, -0.7
xf = lambda t: A_ * math.exp(t) + B_ * math.exp(2 * t); yf = lambda t: 2 * A_ * math.exp(t) + B_ * math.exp(2 * t)
assert close(deriv(xf, 0.4), 3 * xf(0.4) - yf(0.4), 1e-6) and close(deriv(yf, 0.4), 2 * xf(0.4), 1e-6)
xf = lambda t: math.exp(2 * t) + 2 * math.exp(3 * t); yf = lambda t: math.exp(2 * t) + math.exp(3 * t)
assert close(deriv(xf, 0.3), 4 * xf(0.3) - 2 * yf(0.3), 1e-6) and close(deriv(yf, 0.3), xf(0.3) + yf(0.3), 1e-6) and xf(0) == 3 and yf(0) == 2
xs = lambda t: 2 * math.exp(-2 * t) * math.sin(3 * t); assert abs(ode2(xs, 1, 4, 13, lambda t: 0, 0.4)) < 1e-4 and close(deriv(xs, 0), 6, 1e-6) and abs(xs(math.pi / 3)) < 1e-12
xh = lambda t: 3 * math.cos(2 * t) + 4 * math.sin(2 * t); assert abs(ode2(xh, 1, 0, 4, lambda t: 0, 0.9)) < 1e-5 and close(deriv(xh, 0), 8, 1e-6)
deep('cp-coupled',
 'For a coupled pair, differentiate one equation and use the other to eliminate one variable, giving a single second-order equation; then recover the second variable from the original first-order equation rather than solving again. In a damped model, compare the discriminant of the auxiliary equation with zero to name the type of damping.',
 [E('Eliminating one variable', 'Solve dx/dt = 3x − y and dy/dt = 2x for x and y in terms of t.', 'Differentiate the first equation: x″ = 3x′ − y′ = 3x′ − 2x.', 'x″ − 3x′ + 2x = 0 has auxiliary roots 1 and 2.', 'x = Aeᵗ + Be^(2t).', 'From the first equation y = 3x − x′.', 'y = 2Aeᵗ + Be^(2t).'),
  E('Simple harmonic motion', 'A particle moves so that x″ = −9x, with x = 2 and x′ = 0 when t = 0. Find x, the period and the maximum speed.', 'x″ + 9x = 0 gives x = A cos 3t + B sin 3t.', 'x(0) = 2 gives A = 2 and x′(0) = 0 gives B = 0.', 'x = 2cos 3t, with period 2π/3.', 'x′ = −6sin 3t, so the maximum speed is 6.'),
  E('Classifying damping', 'Classify the damping in x″ + 6x′ + 9x = 0 and in x″ + 2x′ + 9x = 0.', 'First equation: m² + 6m + 9 = 0 has discriminant 36 − 36 = 0.', 'A repeated root: critical damping, x = (A + Bt)e^(−3t), with no oscillation.', 'Second equation: discriminant 4 − 36 < 0.', 'Complex roots −1 ± 2√2 i: light damping, oscillations with decaying amplitude.')],
 [F('Period of x″ + 16x = 0.', '2π/[[4]]'),
  F('x″ + 2kx′ + 25x = 0 is critically damped when', 'k = [[5]]'),
  F('For x = 3cos 2t.', 'maximum speed = [[6]]')],
 [X('<p>dx/dt = 4x − 2y and dy/dt = x + y, with x = 3 and y = 2 when t = 0.</p>',
    P('Show that d²x/dt² − 5 dx/dt + 6x = 0.', [('M1', 'differentiates: x″ = 4x′ − 2y′ = 4x′ − 2x − 2y'), ('M1', 'eliminates y using 2y = 4x − x′'), ('A1', 'x″ − 5x′ + 6x = 0')]),
    P('Find x and y in terms of t.', [('M1', 'auxiliary roots 2 and 3'), ('A1', 'x = Ae^(2t) + Be^(3t)'), ('M1', 'y = ½(4x − x′) = Ae^(2t) + ½Be^(3t)'), ('M1', 'A + B = 3 and A + ½B = 2'), ('A1', 'x = e^(2t) + 2e^(3t) and y = e^(2t) + e^(3t)')])),
  X('<p>The displacement x of a damped oscillator satisfies x″ + 4x′ + 13x = 0, with x = 0 and x′ = 6 when t = 0.</p>',
    P('Find x in terms of t.', [('M1', 'm² + 4m + 13 = 0'), ('A1', 'm = −2 ± 3i'), ('M1', 'applies both initial conditions to e^(−2t)(A cos 3t + B sin 3t)'), ('A1', 'A = 0'), ('A1', 'x = 2e^(−2t) sin 3t')]),
    P('State the type of damping.', [('B1', 'light damping (underdamped)')]),
    P('Find the first time after t = 0 at which x = 0.', [('B1', 't = π/3')], ans=math.pi / 3)),
  X('<p>A particle moves on a line so that x″ = −4x, with x = 3 and x′ = 8 when t = 0.</p>',
    P('Find x in terms of t and the amplitude of the motion.', [('M1', 'x = A cos 2t + B sin 2t'), ('A1', 'x = 3cos 2t + 4sin 2t'), ('A1', 'amplitude √(3² + 4²) = 5')]),
    P('Find the maximum speed.', [('B1', '2 × 5 = 10')], ans=10))])

assert len(DEEP) == 20
for k, dd in DEEP.items():
    assert len(dd['examples']) >= 2 and len(dd['fills']) >= 3 and len(dd['exam']) >= 3 and len(dd['tip']) > 120, k
    codes = set()
    for q in dd['exam']:
        for p in q['parts']:
            assert p['m'] == len(p['ms']); codes |= {c[0][0] for c in p['ms']}
    assert len(codes) >= 2, k
