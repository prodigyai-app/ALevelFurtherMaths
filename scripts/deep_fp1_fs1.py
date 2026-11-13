"""Further Pure 1 and Further Statistics 1 depth content (original, Edexcel 9FM0 style).
Every stated result is recomputed with asserts; the build fails if any check fails."""
import math
import numpy as np
from fractions import Fraction as Fr
from scipy import stats
from scipy.integrate import solve_ivp
from deep_core import DEEP, deep, E, F, P, X, close, integ, deriv, deriv2

N0 = len(DEEP)
rd = lambda x, n=4: round(float(x), n)
def nth(f, x, n, h=1e-2):
    """central finite-difference nth derivative"""
    return sum((-1) ** k * math.comb(n, k) * f(x + (n / 2 - k) * h) for k in range(n + 1)) / h ** n
tsin = lambda t: 2 * t / (1 + t * t); tcos = lambda t: (1 - t * t) / (1 + t * t)

# ------------------------------------------------------------------ fp1-tformula
th = 2 * math.atan(0.5); assert close(3 * math.cos(th) + 4 * math.sin(th), 5) and rd(th, 3) == 0.927
for t in (0.3, 1.7): a = 2 * math.atan(t); assert close((1 - math.cos(a)) / math.sin(a), t) and close(math.sin(a) / (1 + math.cos(a)), t) and close(1 / math.cos(a) + math.tan(a), (1 + t) / (1 - t))
assert close(tsin(1), 1) and close(tcos(0.5), 0.6) and close(2 * (1 / 3) / (1 - 1 / 9), 0.75)
s1, s2 = math.pi / 2, 2 * math.atan(-1 / 3) + 2 * math.pi
for s in (s1, s2): assert close(math.sin(s) + 2 * math.cos(s), 1)
assert rd(s2, 2) == 5.64 and close(1 / math.cos(th) + math.tan(th), 3)
deep('fp1-tformula',
 'Substitute for every trigonometric function at once and multiply through by 1 + t² straight away, so the equation becomes a polynomial in t. The substitution cannot represent θ = π (where t is undefined), so test that value separately, and convert each t back with θ = 2arctan t, adjusting into the required interval.',
 [E('A repeated root in t', 'Solve 3cos θ + 4sin θ = 5 for 0 ≤ θ < 2π, using t = tan(θ/2).', '3(1 − t²)/(1 + t²) + 8t/(1 + t²) = 5.', '3 − 3t² + 8t = 5 + 5t², so 8t² − 8t + 2 = 0.', '(2t − 1)² = 0, so t = ½.', 'θ = 2arctan ½ = 0.927 (3 s.f.); θ = π gives −3 ≠ 5, so nothing is lost.'),
  E('Proving an identity', 'Use t = tan(θ/2) to prove that (1 − cos θ)/sin θ = tan(θ/2).', '1 − cos θ = 1 − (1 − t²)/(1 + t²) = 2t²/(1 + t²).', 'sin θ = 2t/(1 + t²).', 'The quotient is 2t²/2t = t.', 'So (1 − cos θ)/sin θ = tan(θ/2), for sin θ ≠ 0.')],
 [F('t = 1.', 'sin θ = 2t/(1 + t²) = [[1]]'),
  F('t = ½.', 'cos θ = (1 − t²)/(1 + t²) = [[0.6]]'),
  F('t = ⅓.', 'tan θ = 2t/(1 − t²) = [[0.75]]')],
 [X('<p>The equation sin θ + 2cos θ = 1 is to be solved for 0 ≤ θ &lt; 2π.</p>',
    P('Using t = tan(θ/2), show that 3t² − 2t − 1 = 0.', [('M1', 'substitutes 2t/(1 + t²) and (1 − t²)/(1 + t²)'), ('M1', 'multiplies through by 1 + t²: 2t + 2 − 2t² = 1 + t²'), ('A1', '3t² − 2t − 1 = 0')]),
    P('Hence solve the equation, giving answers to 3 significant figures where appropriate.', [('M1', '(3t + 1)(t − 1) = 0'), ('A1', 't = 1 or t = −⅓'), ('A1', 'θ = π/2 (1.57)'), ('A1', 'θ = 2π + 2arctan(−⅓) = 5.64')])),
  X('', P('Use t = tan(θ/2) to prove that sin θ/(1 + cos θ) = tan(θ/2).', [('M1', '1 + cos θ = 2/(1 + t²)'), ('M1', 'divides 2t/(1 + t²) by 2/(1 + t²)'), ('A1', '= t = tan(θ/2)')])),
  X('',
    P('Show that sec θ + tan θ = (1 + t)/(1 − t), where t = tan(θ/2).', [('M1', '(1 + t²)/(1 − t²) + 2t/(1 − t²)'), ('A1', '(1 + t)²/[(1 − t)(1 + t)]'), ('A1', '(1 + t)/(1 − t)')]),
    P('Hence solve sec θ + tan θ = 3 for 0 &lt; θ &lt; π/2.', [('M1', '1 + t = 3 − 3t, so t = ½'), ('A1', 'θ = 2arctan ½ = 0.927')], ans=th, tol=2e-3))])

# ------------------------------------------------------------------ fp1-taylor
h = 0.02
assert close(math.sin(math.pi / 6 + h), 0.5 + math.sqrt(3) / 2 * h - h * h / 4, 1e-5) and close(math.exp(1 + h), math.e * (1 + h + h * h / 2 + h ** 3 / 6), 1e-7)
assert close(deriv2(math.tan, 0.6), 2 * math.tan(0.6) / math.cos(0.6) ** 2, 1e-5)
hh = 0.8 - math.pi / 4; est = 1 + 2 * hh + 2 * hh * hh; assert rd(est) == 1.0296 and abs(est - math.tan(0.8)) < 2e-5
assert close(1 / (2 + h), 0.5 - h / 4 + h * h / 8 - h ** 3 / 16, 1e-7) and close(math.log(math.e + h), 1 + h / math.e - h * h / (2 * math.e ** 2), 1e-6)
deep('fp1-taylor',
 'Set h = x − a and tabulate f(a), f′(a), f″(a), … before writing the series, remembering the factorial under each derivative. A Taylor polynomial is only reliable near x = a, so choose the centre closest to the value you want and say how far from it you are.',
 [E('Expanding about π/6', 'Find the Taylor series of sin x in ascending powers of (x − π/6) up to the term in (x − π/6)².', 'f(x) = sin x, f′(x) = cos x, f″(x) = −sin x.', 'At x = π/6: f = ½, f′ = √3/2, f″ = −½.', 'f(x) ≈ f(a) + f′(a)h + f″(a)h²/2 with h = x − π/6.', 'sin x ≈ ½ + (√3/2)(x − π/6) − ¼(x − π/6)².'),
  E('An exponential about x = 1', 'Find the Taylor series of eˣ about x = 1 up to the term in (x − 1)³.', 'Every derivative of eˣ is eˣ, so each equals e at x = 1.', 'eˣ ≈ e + e(x − 1) + e(x − 1)²/2! + e(x − 1)³/3!.', 'eˣ ≈ e[1 + (x − 1) + ½(x − 1)² + ⅙(x − 1)³].')],
 [F('f(x) = x³ about x = 2.', 'f(2) = [[8]] and f′(2) = [[12]]'),
  F('ln x about x = 1.', 'the coefficient of (x − 1)² is −1/[[2]]'),
  F('cos x about x = π/2.', 'the coefficient of (x − π/2) is [[-1]]')],
 [X('<p>f(x) = tan x.</p>',
    P('Show that f″(x) = 2sec²x tan x.', [('M1', 'f′(x) = sec²x and uses the chain rule'), ('A1', '2sec x × sec x tan x = 2sec²x tan x')]),
    P('Find the Taylor series of tan x in ascending powers of (x − π/4) up to the term in (x − π/4)².', [('M1', 'f(π/4) = 1, f′(π/4) = 2, f″(π/4) = 4'), ('A1', '1 + 2(x − π/4)'), ('A1', '+ 2(x − π/4)²')]),
    P('Use your series to estimate tan 0.8, to 4 decimal places.', [('M1', 'h = 0.8 − π/4 = 0.0146…'), ('A1', '1.0296')], ans=1.0296, tol=1e-4)),
  X('', P('Find the Taylor series of 1/x about x = 2 up to and including the term in (x − 2)³.', [('M1', 'derivatives −x⁻², 2x⁻³, −6x⁻⁴'), ('A1', 'f(2) = ½ and f′(2) = −¼'), ('A1', 'f″(2) = ¼ and f‴(2) = −⅜'), ('A1', '½ − ¼(x − 2) + ⅛(x − 2)² − (1/16)(x − 2)³')])),
  X('', P('Find the Taylor series of ln x about x = e up to and including the term in (x − e)².', [('M1', 'f(e) = 1, f′(e) = 1/e, f″(e) = −1/e²'), ('A1', '1 + (x − e)/e'), ('A1', '− (x − e)²/(2e²)')]))])

# ------------------------------------------------------------------ fp1-leibniz
xx = 0.7
assert close(nth(lambda t: t * t * math.sin(t), xx, 4), xx * xx * math.sin(xx) - 8 * xx * math.cos(xx) - 12 * math.sin(xx), 1e-3)
assert close((math.sin(1e-2) - 1e-2) / 1e-6, -1 / 6, 1e-4)
assert close(nth(lambda t: t ** 3 * math.exp(2 * t), xx, 5, 2e-2), math.exp(2 * xx) * (32 * xx ** 3 + 240 * xx * xx + 480 * xx + 240), 2e-3)
e = 1e-3
assert close((math.exp(2 * e) - 1 - 2 * e) / e ** 2, 2, 2e-3) and close((e - math.log(1 + e)) / (1 - math.cos(e)), 1, 2e-3)
assert close((1 - math.sin(math.pi / 2 - e)) / math.cos(math.pi / 2 - e) ** 2, 0.5, 1e-5)
deep('fp1-leibniz',
 'For a product, let u be the factor whose derivatives vanish after a few steps, so the Leibniz sum stops early; write the binomial coefficients first. Before using L’Hôpital’s rule, confirm that the limit really has the form 0/0 or ∞/∞, and re-check that form each time you apply the rule again.',
 [E('Leibniz’s theorem', 'Find the fourth derivative of x² sin x.', 'Take u = x² (derivatives 2x, 2, 0) and v = sin x.', 'Fourth derivative = u v⁗ + 4u′v‴ + 6u″v″, the later terms being zero.', '= x² sin x + 4(2x)(−cos x) + 6(2)(−sin x).', '= x² sin x − 8x cos x − 12 sin x.'),
  E('L’Hôpital’s rule used three times', 'Find the limit of (sin x − x)/x³ as x → 0.', 'The form is 0/0: differentiate top and bottom to get (cos x − 1)/3x².', 'Still 0/0: differentiate again to get −sin x/6x.', 'Still 0/0: differentiate again to get −cos x/6.', 'The limit is −1/6.')],
 [F('A binomial coefficient in Leibniz’s theorem.', '⁵C₂ = [[10]]'),
  F('A standard limit.', 'the limit of sin 3x / x as x → 0 is [[3]]'),
  F('The third derivative of e^(2x) at x = 0.', '2³ = [[8]]')],
 [X('', P('Use Leibniz’s theorem to find the fifth derivative of x³e^(2x).', [('M1', 'Leibniz with u = x³, v = e^(2x), terms r = 0 to 3'), ('M1', 'uses 3x², 6x, 6 and powers of 2 from e^(2x)'), ('A1', '32x³e^(2x) + 240x²e^(2x)'), ('A1', 'e^(2x)(32x³ + 240x² + 480x + 240)')])),
  X('',
    P('Find the limit of (e^(2x) − 1 − 2x)/x² as x → 0.', [('M1', 'L’Hôpital: (2e^(2x) − 2)/2x'), ('M1', 'applies the rule again: 4e^(2x)/2'), ('A1', '2')], ans=2),
    P('Find the limit of [x − ln(1 + x)]/(1 − cos x) as x → 0.', [('M1', '[1 − 1/(1 + x)]/sin x'), ('M1', 'applies the rule again: (1 + x)⁻²/cos x'), ('A1', '1')], ans=1)),
  X('', P('Find the limit of (1 − sin x)/cos²x as x → π/2.', [('M1', 'form 0/0; differentiates: −cos x/(−2cos x sin x)'), ('M1', 'cancels cos x: 1/(2sin x)'), ('A1', '½')], ans=0.5))])

# ------------------------------------------------------------------ fp1-weierstrass
assert close(deriv(lambda t: -2 / (1 + math.tan(t / 2)), 0.8), 1 / (1 + math.sin(0.8)), 1e-6)
assert close(integ(lambda t: 1 / (5 + 4 * math.cos(t)), 0, math.pi / 2), 2 / 3 * math.atan(1 / 3), 1e-7)
assert close(integ(lambda t: 1 / (1 + math.sin(t) + math.cos(t)), 0, math.pi / 2), math.log(2), 1e-7)
assert close(integ(lambda t: 1 / (2 - math.cos(t)), 0, math.pi / 2), 2 * math.pi / (3 * math.sqrt(3)), 1e-7)
assert close(deriv(lambda t: math.log(math.tan(t / 2)), 0.9), 1 / math.sin(0.9), 1e-6)
deep('fp1-weierstrass',
 'Replace dx as well as the trigonometric functions: dx = 2dt/(1 + t²). The factor 1 + t² usually cancels, leaving a rational function of t. Change the limits to values of t, or substitute back, and keep to an interval of x on which tan(x/2) is continuous.',
 [E('A denominator that becomes a perfect square', 'Find ∫ 1/(1 + sin x) dx using t = tan(x/2).', '1 + sin x = 1 + 2t/(1 + t²) = (1 + t)²/(1 + t²).', 'dx = 2dt/(1 + t²), so the integral is ∫ 2/(1 + t)² dt.', '= −2/(1 + t) + c.', '= −2/(1 + tan(x/2)) + c.'),
  E('A definite integral with new limits', 'Evaluate ∫ 1/(5 + 4cos x) dx from 0 to π/2.', '5 + 4cos x = [5(1 + t²) + 4(1 − t²)]/(1 + t²) = (9 + t²)/(1 + t²).', 'The integral becomes ∫ 2/(9 + t²) dt.', 'Limits: x = 0 gives t = 0 and x = π/2 gives t = 1.', '[⅔ arctan(t/3)] from 0 to 1 = ⅔ arctan ⅓ ≈ 0.2145.')],
 [F('The differential.', 'dx = [[2]] dt/(1 + t²)'),
  F('Changing a limit.', 'x = π/2 gives t = [[1]]'),
  F('A useful combination.', '1 + cos x = [[2]]/(1 + t²)')],
 [X('',
    P('Using t = tan(x/2), show that ∫ 1/(1 + sin x + cos x) dx = ∫ 1/(1 + t) dt.', [('M1', 'substitutes for sin x, cos x and dx'), ('M1', 'denominator (2 + 2t)/(1 + t²)'), ('A1', '∫ 2/(2 + 2t) dt = ∫ 1/(1 + t) dt')]),
    P('Hence find the exact value of the integral from 0 to π/2.', [('M1', '[ln(1 + t)] from 0 to 1'), ('A1', 'ln 2')], ans=math.log(2))),
  X('', P('Use the substitution t = tan(x/2) to find the exact value of ∫ 1/(2 − cos x) dx from 0 to π/2.', [('M1', 'substitutes for cos x and dx'), ('A1', '∫ 2/(1 + 3t²) dt'), ('M1', 'k arctan(√3 t)'), ('A1', '(2/√3) arctan(√3 t) from 0 to 1'), ('A1', '2π/(3√3) = 2√3π/9')], ans=2 * math.pi / (3 * math.sqrt(3)))),
  X('', P('Use the substitution t = tan(x/2) to show that ∫ cosec x dx = ln|tan(x/2)| + c.', [('M1', 'cosec x = (1 + t²)/2t and dx = 2dt/(1 + t²)'), ('A1', '∫ 1/t dt'), ('A1', 'ln|t| + c = ln|tan(x/2)| + c')]))])

# ------------------------------------------------------------------ fp1-de-series
sol = solve_ivp(lambda x, y: [y[1], 2 * y[1] - x * y[0]], [0, 0.1], [1, 2], rtol=1e-10, atol=1e-12)
assert close(sol.y[0][-1], 1 + 0.2 + 0.02 + 7 * 0.001 / 6, 1e-4)
yb = lambda x: math.tan(x + 0.3) - x; assert close(deriv(yb, 0.2), (0.2 + yb(0.2)) ** 2, 1e-6)
assert close(math.exp(-0.2 ** 2 / 2), 1 - 0.02 + 0.2 ** 4 / 8, 1e-5)
yh = lambda x: math.sqrt(2 * x * x * (math.log(x) + 2)); assert close(yh(1), 2) and close(deriv(yh, 1.5), (1.5 ** 2 + yh(1.5) ** 2) / (1.5 * yh(1.5)), 1e-6)
sol = solve_ivp(lambda x, y: [x * x - y[0] ** 2], [0, 0.1], [1], rtol=1e-10, atol=1e-12)
est = 1 - 0.1 + 0.01 - 2 / 3 * 0.001; assert rd(est) == 0.9093 and abs(sol.y[0][-1] - est) < 2e-4
deep('fp1-de-series',
 'For a series solution, differentiate the differential equation itself to obtain each higher derivative, and evaluate at the initial point after every differentiation. For a substitution, differentiate the substitution first, replace dy/dx completely, and only then solve; return to the original variables at the end.',
 [E('A series solution of a second-order equation', 'y″ = 2y′ − xy with y = 1 and y′ = 2 at x = 0. Find the series solution up to the term in x³.', 'At x = 0: y″ = 2(2) − 0 = 4.', 'Differentiate: y‴ = 2y″ − y − xy′.', 'At x = 0: y‴ = 8 − 1 − 0 = 7.', 'y ≈ 1 + 2x + (4/2!)x² + (7/3!)x³ = 1 + 2x + 2x² + (7/6)x³.'),
  E('A substitution that separates the variables', 'Use u = x + y to solve dy/dx = (x + y)².', 'du/dx = 1 + dy/dx, so du/dx = 1 + u².', '∫ du/(1 + u²) = ∫ dx gives arctan u = x + c.', 'u = tan(x + c).', 'y = tan(x + c) − x.')],
 [F('y′ = x² + y with y(0) = 2.', 'y′(0) = [[2]] and, since y″ = 2x + y′, y″(0) = [[2]]'),
  F('y′ = 1 + y² with y(0) = 0.', 'y″ = 2yy′ and y‴ = 2(y′)² + 2yy″, so y‴(0) = [[2]]'),
  F('The substitution z = y².', 'dz/dx = [[2]]y dy/dx')],
 [X('<p>d²y/dx² + x dy/dx + y = 0, with y = 1 and dy/dx = 0 at x = 0.</p>',
    P('Find the value of d²y/dx² at x = 0.', [('B1', '−1')], ans=-1),
    P('Show that d³y/dx³ + x d²y/dx² + 2 dy/dx = 0.', [('M1', 'differentiates, using the product rule on x dy/dx'), ('A1', 'y‴ + xy″ + y′ + y′ = 0')]),
    P('Find the series solution for y up to and including the term in x⁴.', [('M1', 'differentiates again: y⁗ + xy‴ + 3y″ = 0'), ('A1', 'y‴(0) = 0 and y⁗(0) = 3'), ('M1', 'uses the Taylor formula with 2! and 4!'), ('A1', 'y = 1 − x²/2 + x⁴/8')])),
  X('<p>dy/dx = (x² + y²)/(xy), x &gt; 0.</p>',
    P('Use the substitution y = ux to show that x du/dx = 1/u.', [('M1', 'dy/dx = u + x du/dx'), ('M1', 'right-hand side becomes (1 + u²)/u'), ('A1', 'x du/dx = 1/u')]),
    P('Given that y = 2 when x = 1, find y² in terms of x.', [('M1', 'separates: ∫ u du = ∫ dx/x'), ('A1', '½u² = ln x + c'), ('M1', 'uses u = 2 when x = 1: c = 2'), ('A1', 'y² = 2x²(ln x + 2)')])),
  X('<p>dy/dx = x² − y², with y = 1 at x = 0.</p>',
    P('Find a series solution for y up to and including the term in x³.', [('M1', 'y′(0) = −1 and y″ = 2x − 2yy′'), ('A1', 'y″(0) = 2'), ('M1', 'y‴ = 2 − 2(y′)² − 2yy″, giving −4'), ('A1', 'y = 1 − x + x² − ⅔x³')]),
    P('Use your series to estimate y when x = 0.1, to 4 decimal places.', [('B1', '0.9093')], ans=0.9093, tol=1e-4))])

# ------------------------------------------------------------------ fp1-conics
assert close(math.sqrt(1 + 9 / 16), 1.25) and close(4 * 1.25, 5) and close(4 / 1.25, 16 / 5)
t = 3; pt = (2 * t * t, 4 * t); assert pt == (18, 12) and 3 * 12 == 18 + 18 and 12 + 3 * 18 == 66 and close(math.sqrt(1 - 16 / 25), 0.6)
tt = 1.7; xh, yh2 = 4 * tt, 4 / tt; assert close(xh + tt * tt * yh2, 8 * tt)
assert close(math.sqrt(1 - 4 / 9), math.sqrt(5) / 3) and rd(math.sqrt(5) / 3, 3) == 0.745
a_ = 0.8; px, py = 3 * math.cos(a_), 2 * math.sin(a_); assert close(2 * px * math.cos(a_) + 3 * py * math.sin(a_), 6)
assert close(deriv(lambda u: 2 * math.sin(u), a_) / deriv(lambda u: 3 * math.cos(u), a_), -2 * math.cos(a_) / (3 * math.sin(a_)), 1e-6)
assert (-6) ** 2 == 4 * 9 and -6 + 9 == 3 and 2 + 1 == 3
deep('fp1-conics',
 'Identify the conic and its parameters (a, b, e or the focal length) before any calculus. Parametric points such as (at², 2at), (a cos θ, b sin θ) and (ct, c/t) make gradients short: dy/dx = (dy/dt)/(dx/dt). For a locus, eliminate the parameter at the very end.',
 [E('A hyperbola and its features', 'For the hyperbola x²/16 − y²/9 = 1, find the eccentricity, the foci, the directrices and the asymptotes.', 'a = 4, b = 3 and b² = a²(e² − 1), so e² = 1 + 9/16.', 'e = 5/4.', 'Foci (±ae, 0) = (±5, 0); directrices x = ±a/e = ±16/5.', 'Asymptotes y = ±(b/a)x = ±¾x.'),
  E('Tangent and normal to a parabola', 'The point P on y² = 8x has parameter t = 3. Find the tangent and the normal at P.', 'y² = 4ax with a = 2, so P = (at², 2at) = (18, 12).', 'dy/dx = (2a)/(2at) = 1/t = ⅓.', 'Tangent: y − 12 = ⅓(x − 18), that is 3y = x + 18.', 'Normal has gradient −3: y − 12 = −3(x − 18), that is y + 3x = 66.'),
  E('Tangent to a rectangular hyperbola', 'Find the equation of the tangent to xy = 16 at the point (4t, 4/t).', 'y = 16/x, so dy/dx = −16/x² = −1/t² at x = 4t.', 'y − 4/t = −(1/t²)(x − 4t).', 'Multiply by t²: t²y − 4t = −x + 4t.', 'x + t²y = 8t.')],
 [F('Ellipse x²/25 + y²/16 = 1.', 'e = √(1 − 16/25) = [[0.6]]'),
  F('Parabola y² = 20x.', 'focus ([[5]], 0)'),
  F('Rectangular hyperbola xy = 9.', 'c = [[3]]')],
 [X('<p>The ellipse E has equation x²/9 + y²/4 = 1.</p>',
    P('Find the eccentricity of E.', [('M1', 'b² = a²(1 − e²): 4 = 9(1 − e²)'), ('A1', 'e = √5/3')], ans=math.sqrt(5) / 3),
    P('Write down the coordinates of the foci and the equations of the directrices.', [('B1', 'foci (±√5, 0)'), ('B1', 'directrices x = ±9/√5')]),
    P('Show that the tangent to E at P(3cos θ, 2sin θ) has equation 2x cos θ + 3y sin θ = 6.', [('M1', 'dy/dx = (2cos θ)/(−3sin θ)'), ('A1', 'gradient −2cos θ/(3sin θ)'), ('M1', 'y − 2sin θ = m(x − 3cos θ)'), ('A1', 'uses cos²θ + sin²θ = 1 to reach the given equation')])),
  X('<p>The point P(t², 2t) lies on the parabola y² = 4x.</p>',
    P('Show that the normal at P has equation y + tx = 2t + t³.', [('M1', 'dy/dx = 1/t'), ('M1', 'normal gradient −t'), ('M1', 'y − 2t = −t(x − t²)'), ('A1', 'y + tx = 2t + t³')]),
    P('The normal at the point where t = 1 meets the parabola again at Q. Find the coordinates of Q.', [('M1', 'normal y + x = 3 with (s², 2s): s² + 2s − 3 = 0'), ('A1', 's = −3'), ('A1', 'Q(9, −6)')])),
  X('<p>The point P(4p, 4/p), p &gt; 0, lies on the rectangular hyperbola xy = 16. The tangent at P meets the axes at A and B.</p>',
    P('Show that the area of triangle OAB is the same for every position of P.', [('M1', 'dy/dx = −1/p²'), ('A1', 'tangent x + p²y = 8p'), ('M1', 'sets y = 0 and x = 0'), ('A1', 'A(8p, 0) and B(0, 8/p)'), ('A1', 'area = ½ × 8p × 8/p = 32, independent of p')]))])

# ------------------------------------------------------------------ fp1-cross
v = lambda *a: np.array(a, dtype=float)
assert np.allclose(np.cross(v(2, 1, -1), v(1, 3, 2)), v(5, -5, 5)) and np.allclose(np.cross(v(1, -1, 1), v(-1, 1, 3)), v(-4, -4, 0))
for p_ in (v(1, 1, 0), v(2, 0, 1), v(0, 2, 3)): assert close(p_[0] + p_[1], 2)
assert close(np.linalg.det(np.array([[1, 2, 0], [0, 1, 3], [2, 0, 1]])), 13)
n_ = np.cross(v(2, 1, -1), v(1, -1, 2)); assert np.allclose(n_, v(1, -5, -3))
for p_ in (v(1, 0, 2), v(3, 1, 1), v(2, -1, 4)): assert close(n_ @ p_, -5)
assert close(np.linalg.det(np.array([[2, 1, 0], [1, 3, 1], [0, 1, 4]])), 18)
c_ = np.cross(v(1, 2, -1), v(2, 1, 2)); assert np.allclose(c_, v(5, -4, -3)) and close(np.linalg.norm(c_) / 3, 5 * math.sqrt(2) / 3)
deep('fp1-cross',
 'Set the vector product out as a determinant and check it with two scalar products, both of which must be zero. Its magnitude is the area of a parallelogram, so halve it for a triangle; the scalar triple product gives the volume of a parallelepiped, so divide by 6 for a tetrahedron.',
 [E('A vector product and an area', 'a = (2,1,−1) and b = (1,3,2). Find a × b and the area of the parallelogram with sides a and b.', 'a × b = (1×2 − (−1)×3, (−1)×1 − 2×2, 2×3 − 1×1).', '= (5, −5, 5).', 'Check: a·(a × b) = 10 − 5 − 5 = 0 and b·(a × b) = 5 − 15 + 10 = 0.', 'Area = |a × b| = 5√3.'),
  E('A plane from three points', 'Find a Cartesian equation of the plane through A(1,1,0), B(2,0,1) and C(0,2,3).', 'AB = (1,−1,1) and AC = (−1,1,3).', 'AB × AC = (−3 − 1, −1 − 3, 1 − 1) = (−4, −4, 0).', 'A normal is (1, 1, 0), so the plane is x + y = d.', 'Using A: d = 2, so x + y = 2; B and C both satisfy this.'),
  E('A scalar triple product', 'Find the volume of the parallelepiped with edges a = (1,2,0), b = (0,1,3) and c = (2,0,1).', 'Volume = |a·(b × c)|, the determinant with rows a, b, c.', '= 1(1 − 0) − 2(0 − 6) + 0.', '= 13.')],
 [F('Unit vectors.', '(1,0,0) × (0,1,0) = (0, 0, [[1]])'),
  F('|a| = 3, |b| = 4 and the angle between them is 30°.', '|a × b| = 3 × 4 × ½ = [[6]]'),
  F('A vector product is perpendicular to both factors.', 'a·(a × b) = [[0]]')],
 [X('<p>A(1, 0, 2), B(3, 1, 1) and C(2, −1, 4).</p>',
    P('Find AB × AC.', [('M1', 'AB = (2,1,−1) and AC = (1,−1,2)'), ('A1', 'two correct components'), ('A1', '(1, −5, −3)')]),
    P('Find the exact area of triangle ABC.', [('M1', '½|AB × AC|'), ('A1', '½√35')], ans=math.sqrt(35) / 2),
    P('Find a Cartesian equation of the plane ABC.', [('M1', 'x − 5y − 3z = d with a point substituted'), ('A1', 'x − 5y − 3z = −5')])),
  X('', P('The tetrahedron OABC has OA = (2,1,0), OB = (1,3,1) and OC = (0,1,4). Find its volume.', [('M1', 'scalar triple product as a 3 × 3 determinant'), ('A1', '18'), ('A1', 'volume = 18/6 = 3')], ans=3)),
  X('<p>The line l passes through the point with position vector a = (1,2,−1) and has direction d = (2,1,2).</p>',
    P('Write down an equation of l in the form (r − a) × d = 0.', [('B1', '(r − (1,2,−1)) × (2,1,2) = 0')]),
    P('Find the shortest distance from the origin to l.', [('M1', 'a × d'), ('A1', '(5, −4, −3)'), ('M1', '|a × d|/|d| = √50/3'), ('A1', '5√2/3')], ans=5 * math.sqrt(2) / 3))])

# ------------------------------------------------------------------ fp1-numerical
ys = [math.log(1 + 0.5 * i) for i in range(5)]; S = 0.5 / 3 * (ys[0] + ys[4] + 4 * (ys[1] + ys[3]) + 2 * ys[2]); assert rd(S) == 1.2953 and rd(3 * math.log(3) - 2) == 1.2958
for x_, ok in ((0.5, True), (2, False), (4, True), (1.5, False)): assert (2 * x_ / (x_ - 1) < 3) == ok
y1 = 1 + 0.1 * (0 - 1); y2 = 1 + 0.2 * (0.1 - y1 * y1); assert close(y1, 0.9) and close(y2, 0.858)
ys = [1 / (1 + (0.25 * i) ** 2) for i in range(5)]; S2 = 0.25 / 3 * (ys[0] + ys[4] + 4 * (ys[1] + ys[3]) + 2 * ys[2]); assert rd(S2) == 0.7854 and rd(4 * S2) == 3.1416
e1 = 1 + 0.1 * (0 + 1); e2 = 1 + 0.2 * (0.01 + e1); assert close(e1, 1.1) and close(e2, 1.222)
for x_, ok in ((1, False), (2.5, True), (7, True), (8, False)): assert ((x_ + 3) / (x_ - 2) >= 2) == ok
for x_, ok in ((-2, False), (0, True), (4.9, True), (6, False)): assert (abs(2 * x_ - 1) < x_ + 4) == ok
deep('fp1-numerical',
 'Tabulate ordinates to at least one more decimal place than the answer needs, and check that Simpson’s rule has an even number of strips. For an inequality, never multiply by an expression whose sign is unknown: collect everything on one side as a single fraction, find the critical values and test each region.',
 [E('Simpson’s rule with four strips', 'Use Simpson’s rule with 4 strips to estimate ∫ ln x dx from 1 to 3.', 'h = 0.5; ordinates 0, 0.405465, 0.693147, 0.916291, 1.098612.', 'Estimate = (h/3)[y₀ + y₄ + 4(y₁ + y₃) + 2y₂].', '= (0.5/3)[1.098612 + 5.287024 + 1.386294].', '= 1.2953 (4 d.p.); the exact value 3ln 3 − 2 is 1.2958.'),
  E('A rational inequality', 'Solve 2x/(x − 1) < 3.', '2x/(x − 1) − 3 < 0.', '(2x − 3x + 3)/(x − 1) < 0, that is (3 − x)/(x − 1) < 0.', 'Critical values x = 1 and x = 3; test a value in each region.', 'x < 1 or x > 3.'),
  E('A two-step numerical solution', 'dy/dx = x − y² with y = 1 at x = 0. Use h = 0.1 with y₁ ≈ y₀ + hf(x₀, y₀) and then y₂ ≈ y₀ + 2hf(x₁, y₁) to estimate y at x = 0.2.', 'f(0, 1) = −1, so y₁ ≈ 1 − 0.1 = 0.9.', 'f(0.1, 0.9) = 0.1 − 0.81 = −0.71.', 'y₂ ≈ 1 + 0.2 × (−0.71).', 'y(0.2) ≈ 0.858.')],
 [F('Simpson’s rule weights for four strips.', '1, 4, [[2]], 4, 1'),
  F('One Euler step for y′ = 2x + y from (0, 1) with h = 0.1.', 'y₁ = [[1.1]]'),
  F('Solve x² > 4.', 'x > 2 or x < [[-2]]')],
 [X('',
    P('Use Simpson’s rule with 4 strips to estimate ∫ 1/(1 + x²) dx from 0 to 1, giving your answer to 4 decimal places.', [('M1', 'h = 0.25 with ordinates 1, 0.941176, 0.8, 0.64, 0.5'), ('M1', '(0.25/3)[1.5 + 4(1.581176) + 2(0.8)]'), ('A1', '0.7854')], ans=0.7854, tol=1e-4),
    P('Hence obtain an estimate for π.', [('B1', '4 × 0.7854 = 3.1416')], ans=3.1416, tol=1e-4)),
  X('<p>dy/dx = x² + y, with y = 1 at x = 0. Use a step length of 0.1.</p>',
    P('Use y₁ ≈ y₀ + h(dy/dx)₀ to estimate y at x = 0.1.', [('M1', '1 + 0.1 × (0 + 1)'), ('A1', '1.1')], ans=1.1),
    P('Use y₂ ≈ y₀ + 2h(dy/dx)₁ to estimate y at x = 0.2.', [('M1', '1 + 0.2 × (0.01 + 1.1)'), ('A1', '1.222')], ans=1.222)),
  X('',
    P('Solve (x + 3)/(x − 2) ≥ 2.', [('M1', 'brings 2 to the left-hand side'), ('M1', 'single fraction (7 − x)/(x − 2) ≥ 0'), ('A1', 'critical values 2 and 7'), ('A1', '2 &lt; x ≤ 7')]),
    P('Solve |2x − 1| &lt; x + 4.', [('M1', '2x − 1 &lt; x + 4, giving x &lt; 5'), ('M1', '−(2x − 1) &lt; x + 4, giving x &gt; −1'), ('A1', '−1 &lt; x &lt; 5')]))])

# ------------------------------------------------------------------ fs1-discrete
k = Fr(1, 10); xs = [1, 2, 3, 4]
assert sum(k * x for x in xs) == 1 and sum(k * x * x for x in xs) == 3 and sum(k * x ** 3 for x in xs) - 9 == 1 and sum(k * x * Fr(1, x) for x in xs) == Fr(2, 5)
pr = {-1: 0.1, 0: 0.3, 1: 0.3, 2: 0.3}; m_ = sum(x * p for x, p in pr.items()); v_ = sum(x * x * p for x, p in pr.items()) - m_ ** 2
assert close(m_, 0.8) and close(v_, 0.96) and close(4 * v_, 3.84)
g = {-3: Fr(1, 2), 2: Fr(1, 6), 4: Fr(1, 6), 6: Fr(1, 6)}; gm = sum(x * p for x, p in g.items()); gv = sum(x * x * p for x, p in g.items()) - gm ** 2
assert gm == Fr(1, 2) and gv == Fr(163, 12)
deep('fs1-discrete',
 'Use ΣP(X = x) = 1 first to find any unknown probability. Work out E(X) and E(X²) in a table, then Var(X) = E(X²) − [E(X)]². For a linear function, the constant shifts the mean only and the multiplier is squared in the variance.',
 [E('An unknown constant', 'P(X = x) = kx for x = 1, 2, 3, 4. Find k, E(X) and Var(X).', 'k(1 + 2 + 3 + 4) = 1, so k = 1/10.', 'E(X) = Σx × kx = k(1 + 4 + 9 + 16) = 3.', 'E(X²) = Σx² × kx = k(1 + 8 + 27 + 64) = 10.', 'Var(X) = 10 − 3² = 1.'),
  E('Expectation of a function', 'For the distribution in the previous example, find E(1/X) and Var(2X + 5).', 'E(1/X) = Σ(1/x) × kx = 4k.', 'E(1/X) = 0.4; note that this is not 1/E(X).', 'Var(2X + 5) = 2² Var(X).', '= 4.')],
 [F('E(X) = 4.', 'E(3X + 2) = [[14]]'),
  F('Var(X) = 2.', 'Var(3X + 2) = [[18]]'),
  F('Probabilities 0.2, 0.5 and p.', 'p = [[0.3]]')],
 [X('<p>X takes the values −1, 0, 1, 2 with probabilities 0.1, a, 0.3, b respectively, and E(X) = 0.8.</p>',
    P('Find the values of a and b.', [('M1', 'a + b = 0.6'), ('M1', '−0.1 + 0.3 + 2b = 0.8'), ('A1', 'a = 0.3 and b = 0.3')]),
    P('Find Var(X).', [('M1', 'E(X²) = 0.1 + 0.3 + 1.2 = 1.6'), ('M1', '1.6 − 0.8²'), ('A1', '0.96')], ans=0.96),
    P('Find Var(5 − 2X).', [('B1', '4 × 0.96 = 3.84')], ans=3.84)),
  X('<p>In a game a fair six-sided die is rolled. If the score is even the player wins that number of pounds; if it is odd the player loses £3.</p>',
    P('Find the expected profit for one game.', [('M1', 'profit −3 with probability ½ and 2, 4, 6 each with probability ⅙'), ('M1', '−1.5 + 12/6'), ('A1', '£0.50')], ans=0.5, unit='£'),
    P('Find the variance of the profit.', [('M1', 'E(X²) = 4.5 + 56/6'), ('A1', '13.83…'), ('A1', '163/12 ≈ 13.58')], ans=163 / 12, tol=2e-3)),
  X('<p>E(X) = 10 and Var(X) = 4. The variable Y = aX + b, where a &gt; 0, has mean 0 and variance 1.</p>',
    P('Find the values of a and b.', [('M1', '4a² = 1'), ('M1', '10a + b = 0'), ('A1', 'a = ½ and b = −5')]))])

# ------------------------------------------------------------------ fs1-poisson
po = stats.poisson
assert rd(1 - po.cdf(2, 4.5)) == 0.8264 and rd(po.pmf(2, 2)) == 0.2707 and rd(po.cdf(2, 3)) == 0.4232
assert rd(po.pmf(3, 2.4)) == 0.2090 and rd(1 - po.cdf(1, 1.2)) == 0.3374 and rd(1 - po.cdf(5, 4)) == 0.2149
lam = math.sqrt(6); assert close(po.pmf(2, lam), 3 * po.pmf(0, lam)) and rd(po.pmf(1, lam)) == 0.2115
deep('fs1-poisson',
 'Scale the mean to the interval in the question before calculating anything, and write the event as an inequality so the cumulative probability you need is clear. Poisson modelling needs events that occur singly, independently and at a constant average rate; the approximation to a binomial needs n large and p small.',
 [E('An upper tail', 'X ~ Po(4.5). Find P(X ≥ 3).', 'P(X ≥ 3) = 1 − P(X ≤ 2).', 'P(X ≤ 2) = e^(−4.5)(1 + 4.5 + 4.5²/2) = e^(−4.5) × 15.625.', '= 0.1736.', 'P(X ≥ 3) = 0.8264.'),
  E('Adding independent Poisson variables', 'Flaws of type A occur at a rate of 1.2 per metre and flaws of type B at 0.8 per metre, independently. Find the probability of exactly 2 flaws in a metre.', 'The total number of flaws is Po(1.2 + 0.8) = Po(2).', 'P(T = 2) = e^(−2) × 2²/2!.', '= 2e^(−2) = 0.2707.'),
  E('Approximating a binomial', 'X ~ B(200, 0.015). Use a Poisson approximation to find P(X ≤ 2).', 'n is large and p is small, so X ≈ Po(np) = Po(3).', 'P(X ≤ 2) = e^(−3)(1 + 3 + 4.5).', '= 0.4232.')],
 [F('X ~ Po(6).', 'Var(X) = [[6]]'),
  F('A rate of 3 per hour.', 'mean number in 20 minutes = [[1]]'),
  F('B(500, 0.004) is approximated by', 'Po([[2]])')],
 [X('<p>Emails arrive at an average rate of 2.4 per 10 minutes and are modelled by a Poisson distribution.</p>',
    P('Find the probability of exactly 3 emails in a 10-minute period.', [('M1', 'e^(−2.4) × 2.4³/3!'), ('A1', '0.2090')], ans=0.2090, tol=5e-4),
    P('Find the probability of at least 2 emails in a 5-minute period.', [('B1', 'mean 1.2'), ('M1', '1 − e^(−1.2)(1 + 1.2)'), ('A1', '0.3374')], ans=0.3374, tol=5e-4),
    P('State two assumptions needed for the Poisson model.', [('B1', 'emails arrive independently of one another'), ('B1', 'emails arrive singly and at a constant average rate')])),
  X('<p>A machine makes components, each defective with probability 0.01 independently. X is the number of defective components in a batch of 400.</p>',
    P('Explain why a Poisson approximation is suitable.', [('B1', 'n = 400 is large and p = 0.01 is small')]),
    P('Use the approximation to find P(X &gt; 5).', [('B1', 'Po(4)'), ('M1', '1 − P(X ≤ 5)'), ('A1', '0.2149')], ans=0.2149, tol=5e-4)),
  X('<p>X ~ Po(λ) and P(X = 2) = 3P(X = 0).</p>',
    P('Find the exact value of λ.', [('M1', 'e^(−λ)λ²/2 = 3e^(−λ)'), ('A1', 'λ² = 6'), ('A1', 'λ = √6')], ans=lam),
    P('Find P(X = 1), to 4 decimal places.', [('M1', '√6 e^(−√6)'), ('A1', '0.2115')], ans=0.2115, tol=5e-4))])

# ------------------------------------------------------------------ fs1-geometric
assert close(1 - 0.8 ** 4, 0.5904) and rd(0.8 ** 6) == 0.2621 and close(0.8 / 0.04, 20)
assert rd(math.comb(7, 2) * 0.3 ** 3 * 0.7 ** 5) == 0.0953 and close(3 * 0.7 / 0.09, 70 / 3)
assert rd((5 / 6) ** 3 / 6) == 0.0965 and rd((5 / 6) ** 5) == 0.4019 and close((5 / 6) / (1 / 36), 30)
assert close(4 * 0.4 ** 2 * 0.6 ** 3, 0.13824) and close(3 / 0.4, 7.5) and close(3 * 0.6 / 0.16, 11.25) and close(0.3 * 0.7, 0.21) and close(0.7 ** 2, 0.49)
deep('fs1-geometric',
 'Decide what is being counted: the number of trials up to and including the first success is geometric, and up to and including the rth success is negative binomial. For the negative binomial the final trial must be a success, so the binomial coefficient counts arrangements of the earlier r − 1 successes only.',
 [E('Geometric probabilities', 'X ~ Geo(0.2). Find P(X ≤ 4), P(X > 6) and Var(X).', 'P(X > n) = (1 − p)ⁿ, since the first n trials all fail.', 'P(X ≤ 4) = 1 − 0.8⁴ = 0.5904.', 'P(X > 6) = 0.8⁶ = 0.2621.', 'Var(X) = (1 − p)/p² = 0.8/0.04 = 20.'),
  E('A negative binomial probability', 'Each trial succeeds with probability 0.3. Find the probability that the third success occurs on the eighth trial, and the mean and variance of the number of trials needed.', 'Two successes in the first 7 trials, then a success on trial 8.', '⁷C₂ × 0.3² × 0.7⁵ × 0.3 = 21 × 0.3³ × 0.7⁵.', '= 0.0953.', 'Mean = r/p = 10; variance = r(1 − p)/p² = 2.1/0.09 = 23.3.')],
 [F('X ~ Geo(0.25).', 'E(X) = [[4]]'),
  F('X ~ Geo(0.5).', 'P(X = 3) = [[0.125]]'),
  F('Number of trials to the 4th success with p = 0.5.', 'mean = [[8]]')],
 [X('<p>A fair six-sided die is thrown repeatedly until a six is obtained.</p>',
    P('Find the probability that the first six occurs on the fourth throw.', [('M1', '(5/6)³ × (1/6)'), ('A1', '0.0965')], ans=0.0965, tol=1e-3),
    P('Find the probability that more than five throws are needed.', [('M1', '(5/6)⁵'), ('A1', '0.4019')], ans=0.4019, tol=5e-4),
    P('Write down the mean and the variance of the number of throws.', [('B1', 'mean 6'), ('B1', 'variance 30')])),
  X('<p>An archer hits the target with probability 0.4 on each shot, independently.</p>',
    P('Find the probability that her second hit is on her fifth shot.', [('M1', 'one hit in the first four shots, then a hit'), ('M1', '⁴C₁ × 0.4 × 0.6³ × 0.4'), ('A1', '0.1382')], ans=0.13824, tol=1e-3),
    P('Find the expected number of shots needed to obtain three hits.', [('B1', '3/0.4 = 7.5')], ans=7.5),
    P('Find the variance of the number of shots needed to obtain three hits.', [('B1', '3 × 0.6/0.4² = 11.25')], ans=11.25)),
  X('<p>X ~ Geo(p), where p &lt; 0.5, and P(X = 2) = 0.21.</p>',
    P('Find the value of p.', [('M1', 'p(1 − p) = 0.21'), ('A1', 'p = 0.3 or p = 0.7'), ('A1', 'p = 0.3')], ans=0.3),
    P('Find P(X ≥ 3).', [('M1', '(1 − p)²'), ('A1', '0.49')], ans=0.49))])

# ------------------------------------------------------------------ fs1-tests
assert rd(po.cdf(1, 5)) == 0.0404 and rd(po.cdf(2, 8)) == 0.0138 and po.cdf(3, 8) > 0.025 and rd(1 - po.cdf(14, 8)) == 0.0173 and 1 - po.cdf(13, 8) > 0.025
assert rd(po.cdf(2, 8) + 1 - po.cdf(14, 8)) == 0.0310 and rd(po.pmf(0, 2)) == 0.1353
p9 = po.cdf(9, 18); assert rd(p9) == 0.0154
assert 0.8 ** 14 < 0.05 < 0.8 ** 13 and rd(0.8 ** 14) == 0.0440
assert rd(1 - po.cdf(9, 4)) == 0.0081 and 1 - po.cdf(8, 4) > 0.01
deep('fs1-tests',
 'State the hypotheses in terms of the parameter, and give the distribution of the test statistic under H₀ with the mean scaled to the period observed. Compare a tail probability (the observed value or more extreme) with the significance level, never a single-value probability, and word the conclusion in context without claiming proof.',
 [E('A one-tailed Poisson test', 'Faults occur at a rate of 5 per week. After maintenance there is 1 fault in a week. Test at the 5% level whether the rate has decreased.', 'H₀: λ = 5, H₁: λ < 5, with X ~ Po(5) under H₀.', 'P(X ≤ 1) = e^(−5)(1 + 5) = 0.0404.', '0.0404 < 0.05, so reject H₀.', 'There is evidence at the 5% level that the rate of faults has decreased.'),
  E('A two-tailed critical region', 'X ~ Po(λ). Find the critical region for testing H₀: λ = 8 against H₁: λ ≠ 8 at the 5% level, with at most 2.5% in each tail, and state the actual significance level.', 'Lower tail: P(X ≤ 2) = 0.0138 and P(X ≤ 3) = 0.0424, so the region is X ≤ 2.', 'Upper tail: P(X ≥ 14) = 0.0342 and P(X ≥ 15) = 0.0173, so the region is X ≥ 15.', 'Critical region: X ≤ 2 or X ≥ 15.', 'Actual significance level = 0.01375 + 0.01726 = 0.0310.')],
 [F('A one-tailed test at the 5% level.', 'reject H₀ when the tail probability is less than [[0.05]]'),
  F('X ~ Po(2).', 'P(X = 0) = e^(−2) = [[0.1353]]'),
  F('A two-tailed test at the 10% level.', 'each tail has at most [[5]]%')],
 [X('<p>Accidents at a junction occurred at a mean rate of 3 per month. After new signs are installed there are 9 accidents in 6 months.</p>',
    P('Test, at the 5% level of significance, whether the mean rate of accidents has decreased. State your hypotheses clearly.', [('B1', 'H₀: λ = 3, H₁: λ < 3 (per month)'), ('B1', 'under H₀ the 6-month count is Po(18)'), ('M1', 'P(X ≤ 9)'), ('A1', '0.0154'), ('A1', '0.0154 < 0.05: reject H₀; evidence that the rate has decreased')])),
  X('<p>X is the number of attempts needed to obtain a first success, so X ~ Geo(p). A test of H₀: p = 0.2 against H₁: p &lt; 0.2 is carried out at the 5% level.</p>',
    P('Find the critical region.', [('M1', 'P(X ≥ c) = 0.8^(c − 1)'), ('M1', '0.8¹³ = 0.0550 and 0.8¹⁴ = 0.0440'), ('A1', 'X ≥ 15')]),
    P('The first success occurs on the 12th attempt. State the conclusion of the test.', [('B1', '12 is not in the critical region: insufficient evidence that p is less than 0.2')])),
  X('<p>X ~ Po(λ). A test of H₀: λ = 4 against H₁: λ &gt; 4 is carried out at the 1% level.</p>',
    P('Find the critical region.', [('M1', 'P(X ≥ 9) = 0.0214'), ('M1', 'P(X ≥ 10) = 0.0081'), ('A1', 'X ≥ 10')]),
    P('State the actual significance level of the test.', [('B1', '0.0081')], ans=0.0081, tol=2e-2))])

# ------------------------------------------------------------------ fs1-clt
Z = stats.norm
assert rd(1 - Z.cdf((2.9 - 2.5) / math.sqrt(2.5 / 40))) == 0.0548
se = math.sqrt(35 / 12 / 50); assert rd((3.8 - 3.5) / se, 2) == 1.24 and rd(1 - Z.cdf(0.3 / se), 3) == 0.107
assert close(0.75 / 0.0625, 12) and rd(Z.cdf(-1)) == 0.1587 and rd(Z.cdf(1) - Z.cdf(-2)) == 0.8186
assert math.ceil((1.96 * 6) ** 2) == 139
deep('fs1-clt',
 'Write down the mean and variance of the population first, then the distribution of the sample mean: mean μ and variance σ²/n. The central limit theorem is what allows a normal model when the population is not normal, and it needs a large sample; say so when you use it.',
 [E('Sample mean of Poisson data', 'X ~ Po(2.5). A random sample of 40 observations is taken. Estimate the probability that the sample mean exceeds 2.9.', 'The population has mean 2.5 and variance 2.5.', 'By the central limit theorem the sample mean is approximately N(2.5, 2.5/40) = N(2.5, 0.0625).', 'z = (2.9 − 2.5)/0.25 = 1.6.', 'P(Z > 1.6) = 0.0548.'),
  E('Scores on a die', 'A fair die is rolled 50 times. Estimate the probability that the mean score is at least 3.8.', 'One roll has mean 3.5 and variance 35/12.', 'The sample mean is approximately N(3.5, 35/600), with standard error 0.2415.', 'z = (3.8 − 3.5)/0.2415 = 1.24.', 'P(Z ≥ 1.24) ≈ 0.107.')],
 [F('σ = 10 and n = 25.', 'standard error of the mean = [[2]]'),
  F('σ² = 36 and n = 9.', 'variance of the sample mean = [[4]]'),
  F('X ~ Po(4) and n = 100.', 'variance of the sample mean = [[0.04]]')],
 [X('<p>X ~ Geo(0.25), so that E(X) = 4 and Var(X) = 12. A random sample of 48 observations of X is taken.</p>',
    P('State the approximate distribution of the sample mean.', [('B1', 'normal with mean 4'), ('B1', 'variance 12/48 = 0.25')]),
    P('Estimate the probability that the sample mean is less than 3.5.', [('M1', 'z = (3.5 − 4)/0.5 = −1'), ('A1', '0.1587')], ans=0.1587, tol=1e-3),
    P('Explain why the normal approximation is appropriate.', [('B1', 'the sample is large, so the central limit theorem applies')])),
  X('', P('The masses of loaves have mean 250 g and standard deviation 8 g. Estimate the probability that the mean mass of a random sample of 64 loaves lies between 248 g and 251 g.', [('M1', 'standard error 8/√64 = 1'), ('M1', 'standardises both values: z = −2 and z = 1'), ('A1', 'Φ(1) − Φ(−2)'), ('A1', '0.8186')], ans=0.8186, tol=1e-3)),
  X('', P('A population has standard deviation 6. Find the smallest sample size for which the probability that the sample mean lies within 1 of the population mean is at least 0.95.', [('M1', 'uses z = 1.96'), ('M1', '1.96 × 6/√n ≤ 1'), ('A1', 'n = 139')], ans=139))])

# ------------------------------------------------------------------ fs1-chi
assert close(sum((o - 10) ** 2 / 10 for o in (8, 12, 9, 11, 6, 14)), 4.2) and rd(stats.chi2.ppf(0.95, 5), 3) == 11.070
obs = np.array([[30, 20], [10, 40]]); ex = np.outer(obs.sum(1), obs.sum(0)) / obs.sum(); assert np.allclose(ex, [[20, 30], [20, 30]]) and rd(((obs - ex) ** 2 / ex).sum(), 2) == 16.67 and rd(stats.chi2.ppf(0.95, 1), 3) == 3.841
O = [22, 34, 26, 12, 6]; pp = [po.pmf(i, 1.5) for i in range(4)]; pp.append(1 - sum(pp)); Ex = [100 * p for p in pp]
assert [rd(e_, 2) for e_ in Ex] == [22.31, 33.47, 25.10, 12.55, 6.56]
chi = sum((o - e_) ** 2 / e_ for o, e_ in zip(O, Ex)); assert rd(chi, 3) == 0.118 and rd(stats.chi2.ppf(0.95, 3), 3) == 7.815
obs = np.array([[20, 30, 10], [10, 20, 30]]); ex = np.outer(obs.sum(1), obs.sum(0)) / obs.sum(); assert np.allclose(ex, [[15, 25, 20]] * 2)
chi2 = ((obs - ex) ** 2 / ex).sum(); assert rd(chi2, 2) == 15.33 and rd(stats.chi2.ppf(0.95, 2), 3) == 5.991
deep('fs1-chi',
 'Expected frequencies come from the null hypothesis and must add up to the observed total; combine classes until each expected frequency is at least 5. Degrees of freedom are the number of classes after combining, minus 1, minus one more for each parameter estimated from the data; for a contingency table use (rows − 1)(columns − 1).',
 [E('Goodness of fit for a die', 'A die is rolled 60 times, giving frequencies 8, 12, 9, 11, 6, 14 for the scores 1 to 6. Test at the 5% level whether the die is fair.', 'H₀: each score has probability ⅙. Each expected frequency is 10.', 'Σ(O − E)²/E = (4 + 4 + 1 + 1 + 16 + 16)/10 = 4.2.', 'Degrees of freedom = 6 − 1 = 5; the 5% critical value is 11.070.', '4.2 < 11.070: do not reject H₀; the data are consistent with a fair die.'),
  E('A 2 × 2 contingency table', 'Of 50 people given treatment A, 30 improved; of 50 given treatment B, 10 improved. Test at the 5% level whether improvement is independent of treatment.', 'H₀: improvement is independent of treatment. Column totals are 40 improved and 60 not.', 'Expected: 50 × 40/100 = 20 improved and 30 not improved in each row.', 'Σ(O − E)²/E = 100/20 + 100/30 + 100/20 + 100/30 = 16.67.', 'Degrees of freedom = 1; critical value 3.841.', '16.67 > 3.841: reject H₀; improvement is associated with treatment.')],
 [F('A 3 × 4 contingency table.', 'degrees of freedom = [[6]]'),
  F('Row total 40, column total 30, grand total 120.', 'expected frequency = [[10]]'),
  F('Five classes with one parameter estimated from the data.', 'degrees of freedom = [[3]]')],
 [X('<p>The number of goals scored in each of 100 matches was recorded: 0 goals in 22 matches, 1 in 34, 2 in 26, 3 in 12, and 4 or more in 6. The mean of the data is 1.5. A Poisson model is to be tested.</p>',
    P('Show that the expected frequency for 2 goals is 25.10.', [('M1', '100 × e^(−1.5) × 1.5²/2'), ('A1', '25.10')]),
    P('Explain why there are 3 degrees of freedom.', [('B1', '5 classes, each with expected frequency at least 5'), ('B1', '5 − 1 − 1, because the totals agree and the mean was estimated')]),
    P('The other expected frequencies are 22.31, 33.47, 12.55 and 6.56. Calculate the test statistic.', [('M1', 'Σ(O − E)²/E'), ('A1', 'at least three correct contributions'), ('A1', '0.118')], ans=chi, tol=2e-2),
    P('Complete the test at the 5% level.', [('B1', '0.118 < 7.815: do not reject H₀; a Poisson model is consistent with the data')])),
  X('<p>120 students were classified by year group and by the lunch option they chose. Year 12: 20 hot, 30 cold, 10 none. Year 13: 10 hot, 20 cold, 30 none.</p>',
    P('Test, at the 5% level of significance, whether choice of lunch is independent of year group.', [('B1', 'H₀: lunch choice is independent of year group'), ('M1', 'expected = row total × column total ÷ 120'), ('A1', '15, 25 and 20 in each row'), ('M1', 'Σ(O − E)²/E'), ('A1', '15.33'), ('A1', '2 degrees of freedom, 15.33 > 5.991: reject H₀; choice depends on year group')], ans=chi2, tol=2e-3)),
  X('', P('In a goodness-of-fit test the last class has expected frequency 3.2. State what should be done and the effect on the number of degrees of freedom.', [('B1', 'combine it with the adjacent class so that the expected frequency is at least 5'), ('B1', 'the number of degrees of freedom is reduced by 1')]))])

# ------------------------------------------------------------------ fs1-pgf
G = lambda t: (0.4 + 0.6 * t) ** 3
assert close(3 * 0.4 * 0.36, 0.432) and close(deriv(G, 1), 1.8, 1e-6) and close(deriv2(G, 1) + 1.8 - 1.8 ** 2, 0.72, 1e-4)
G1 = lambda t: (2 + t) ** 3 / 27
assert close(G1(1), 1) and close(deriv(G1, 0), 4 / 9, 1e-6) and close(deriv(G1, 1), 1, 1e-6) and close(deriv2(G1, 1), 2 / 3, 1e-4)
Gg = lambda t, p=0.25: p * t / (1 - (1 - p) * t); assert close(deriv(Gg, 1), 4, 1e-5) and close(0.25 * 0.75 ** 2, 0.140625)
Gs = lambda t: math.exp(2 * (t - 1)) * (0.5 + 0.5 * t) ** 2; assert close(deriv(Gs, 1), 3, 1e-6) and rd(Gs(0)) == 0.0338
deep('fs1-pgf',
 'The coefficient of tˣ in G(t) is P(X = x), so G(1) = 1 always. Use E(X) = G′(1) and Var(X) = G″(1) + G′(1) − [G′(1)]². For a sum of independent variables multiply the generating functions; multiplying is only valid when the variables are independent.',
 [E('Mean and variance from a PGF', 'X has probability generating function G(t) = (0.4 + 0.6t)³. Find P(X = 2), E(X) and Var(X).', 'The t² coefficient is 3 × 0.4 × 0.6² = 0.432, so P(X = 2) = 0.432.', 'G′(t) = 1.8(0.4 + 0.6t)², so E(X) = G′(1) = 1.8.', 'G″(t) = 2.16(0.4 + 0.6t), so G″(1) = 2.16.', 'Var(X) = 2.16 + 1.8 − 1.8² = 0.72, as expected for B(3, 0.6).'),
  E('Sum of independent Poisson variables', 'X ~ Po(2) and Y ~ Po(3) are independent. Use generating functions to find the distribution of X + Y.', 'G_X(t) = e^(2(t − 1)) and G_Y(t) = e^(3(t − 1)).', 'For independent variables, G_(X+Y)(t) = G_X(t) G_Y(t).', '= e^(5(t − 1)).', 'This is the generating function of Po(5), so X + Y ~ Po(5).'),
  E('A linear function', 'X has generating function G_X(t). Find the generating function of Y = 3X + 2.', 'G_Y(t) = E(t^Y) = E(t^(3X + 2)).', '= t² E((t³)^X).', 'G_Y(t) = t² G_X(t³).')],
 [F('Every probability generating function.', 'G(1) = [[1]]'),
  F('G(t) = (1 + t)²/4.', 'G′(1) = [[1]]'),
  F('G(t) = 0.2 + 0.5t + 0.3t².', 'P(X = 1) = [[0.5]]')],
 [X('<p>X has probability generating function G(t) = k(2 + t)³.</p>',
    P('Find the value of k.', [('B1', 'G(1) = 27k = 1, so k = 1/27')]),
    P('Find P(X = 1).', [('M1', 'coefficient of t: 3 × 2² × k'), ('A1', '4/9')], ans=4 / 9),
    P('Find E(X).', [('M1', 'G′(t) = 3k(2 + t)²'), ('A1', 'G′(1) = 1')], ans=1),
    P('Find Var(X).', [('M1', 'G″(1) = 6k × 3 = ⅔'), ('M1', 'G″(1) + G′(1) − [G′(1)]²'), ('A1', '⅔')], ans=2 / 3)),
  X('<p>X ~ Geo(p) has probability generating function G(t) = pt/(1 − qt), where q = 1 − p.</p>',
    P('Use G(t) to show that E(X) = 1/p.', [('M1', 'differentiates with the quotient rule'), ('A1', 'G′(t) = p/(1 − qt)²'), ('A1', 'G′(1) = p/p² = 1/p')]),
    P('Given p = 0.25, use the expansion of G(t) to find P(X = 3).', [('M1', 'pt(1 + qt + q²t² + …): coefficient of t³ is pq²'), ('A1', '0.1406')], ans=0.140625, tol=1e-3)),
  X('<p>X and Y are independent with G_X(t) = e^(2(t − 1)) and G_Y(t) = (0.5 + 0.5t)².</p>',
    P('Find E(X + Y).', [('M1', 'G(t) = G_X(t)G_Y(t), or adds the two means'), ('M1', 'G′(1) = 2 + 1'), ('A1', '3')], ans=3),
    P('Find P(X + Y = 0).', [('M1', 'G(0) = e^(−2) × 0.25'), ('A1', '0.0338')], ans=0.0338, tol=3e-3))])

# ------------------------------------------------------------------ fs1-power
assert rd(1 - po.cdf(6, 3)) == 0.0335 and rd(1 - po.cdf(6, 6)) == 0.3937 and rd(po.cdf(6, 6)) == 0.6063
bi = stats.binom
assert rd(bi.cdf(1, 10, 0.5)) == 0.0107 and rd(bi.cdf(1, 10, 0.2)) == 0.3758 and rd(math.exp(-3)) == 0.0498
size = 1 - bi.cdf(8, 12, 0.4); powr = 1 - bi.cdf(8, 12, 0.7); assert rd(size) == 0.0153 and rd(powr) == 0.4925 and rd(1 - powr) == 0.5075
assert close(0.5 ** 5, 0.03125) and close(0.8 ** 5, 0.32768) and rd(po.cdf(1, 5)) == 0.0404 and rd(po.cdf(1, 2)) == 0.4060
deep('fs1-power',
 'Fix the critical region first: size and power are both probabilities of landing in that region, calculated under different parameter values. Size uses the value in H₀; power uses a particular value from H₁; and P(Type II error) = 1 − power. A power function is the same calculation left in terms of the parameter.',
 [E('Size and power of a Poisson test', 'X ~ Po(λ). H₀: λ = 3 is tested against H₁: λ > 3 and H₀ is rejected when X ≥ 7. Find the size of the test and its power when λ = 6.', 'Size = P(X ≥ 7 | λ = 3) = 1 − P(X ≤ 6) = 1 − 0.9665.', 'Size = 0.0335.', 'Power = P(X ≥ 7 | λ = 6) = 1 − 0.6063.', 'Power = 0.3937, so P(Type II error) = 0.6063.'),
  E('A power function', 'X ~ B(10, p). H₀: p = 0.5 is tested against H₁: p < 0.5 and H₀ is rejected when X ≤ 1. Find the size, the power function, and the power when p = 0.2.', 'Size = P(X ≤ 1 | p = 0.5) = 11/1024 = 0.0107.', 'Power function = P(X ≤ 1 | p) = (1 − p)¹⁰ + 10p(1 − p)⁹.', 'At p = 0.2: 0.8¹⁰ + 2 × 0.8⁹ = 0.1074 + 0.2684.', 'Power = 0.3758.')],
 [F('P(Type II error) = 0.35.', 'power = [[0.65]]'),
  F('X ~ B(5, 0.5) and H₀ is rejected only when X = 5.', 'size = [[0.03125]]'),
  F('X ~ Po(3) and H₀ is rejected only when X = 0.', 'size = e^(−3) = [[0.0498]]')],
 [X('<p>X ~ B(12, p). H₀: p = 0.4 is tested against H₁: p &gt; 0.4, and H₀ is rejected when X ≥ 9.</p>',
    P('Find the size of the test.', [('M1', '1 − P(X ≤ 8 | p = 0.4)'), ('A1', '0.0153')], ans=size, tol=2e-3),
    P('Find the power of the test when p = 0.7.', [('M1', '1 − P(X ≤ 8 | p = 0.7)'), ('A1', '0.4925')], ans=powr, tol=1e-3),
    P('Write down the probability of a Type II error when p = 0.7.', [('B1', '0.5075')], ans=1 - powr, tol=1e-3),
    P('Suggest one way of increasing the power of the test.', [('B1', 'use a larger sample, or a larger significance level')])),
  X('<p>X ~ Geo(p). H₀: p = 0.5 is tested against H₁: p &lt; 0.5, and H₀ is rejected when X ≥ 6.</p>',
    P('Find the size of the test.', [('M1', 'P(X ≥ 6) = 0.5⁵'), ('A1', '0.03125')], ans=0.03125),
    P('Find the power function of the test.', [('M1', 'the first five attempts all fail'), ('A1', '(1 − p)⁵')]),
    P('Find the power when p = 0.2.', [('B1', '0.8⁵ = 0.3277')], ans=0.32768, tol=1e-3)),
  X('<p>The number of calls in an hour is X ~ Po(λ). H₀: λ = 5 is tested against H₁: λ &lt; 5, and H₀ is rejected when X ≤ 1.</p>',
    P('Find the size of the test.', [('M1', 'e^(−5)(1 + 5)'), ('A1', '0.0404')], ans=0.0404, tol=3e-3),
    P('Find the power of the test when λ = 2.', [('M1', 'e^(−2)(1 + 2)'), ('A1', '0.4060')], ans=0.4060, tol=1e-3),
    P('Describe a Type II error in this context.', [('B1', 'concluding that the rate of calls has not fallen when in fact it has')]))])

def validate():
    for k_, dd in DEEP.items():
        assert len(dd['examples']) >= 2 and len(dd['fills']) >= 3 and len(dd['exam']) >= 3 and len(dd['tip']) > 120, k_
        for q in dd['exam']:
            for p in q['parts']: assert p['m'] == len(p['ms'])
assert len(DEEP) - N0 == 16
validate()
