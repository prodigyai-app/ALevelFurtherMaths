"""Further Statistics 2 and Further Mechanics 2 depth content (original, Edexcel 9FM0 style).
Every stated result is recomputed with asserts; the build fails if any check fails."""
import math
import numpy as np
from scipy import stats
from deep_core import DEEP, deep, E, F, P, X, close, integ

N0 = len(DEEP)
rd = lambda x, n=4: round(float(x), n)
g = 9.8
Z, T, C2, Fd = stats.norm, stats.t, stats.chi2, stats.f
rcrit = lambda n, a: (lambda t: t / math.sqrt(t * t + n - 2))(T.ppf(1 - a, n - 2))

# ------------------------------------------------------------------ fs2-regression
assert 240 - 40 ** 2 / 8 == 40 and 520 - 40 * 96 / 8 == 40 and 96 / 8 - 1 * 5 == 7 and 50 - 40 ** 2 / 40 == 10
Sxx, Sxy, Syy = 385 - 55 ** 2 / 10, 1953 - 55 * 320 / 10, 10720 - 320 ** 2 / 10
b = Sxy / Sxx; a = 32 - b * 5.5; RSS = Syy - Sxy ** 2 / Sxx
assert Sxx == 82.5 and Sxy == 193 and Syy == 480 and rd(b) == 2.3394 and rd(a, 2) == 19.13 and rd(a + 7 * b, 2) == 35.51 and rd(RSS, 1) == 28.5
assert close(3.2 + 1.5 * 6, 12.2) and close(18 - 12.2, 5.8) and close(30 / 12, 2.5) and 10 - 2 * 3 == 4
deep('fs2-regression',
 'Compute Sxx and Sxy from the summary statistics first; then b = Sxy/Sxx and a = ȳ − bx̄, because the regression line always passes through (x̄, ȳ). A residual is observed minus predicted; the residual sum of squares is Syy − Sxy²/Sxx, and a pattern in the residuals suggests that a linear model is unsuitable.',
 [E('A regression line from summary statistics', 'For 8 pairs, Σx = 40, Σy = 96, Σx² = 240 and Σxy = 520. Find the regression line of y on x.', 'Sxx = 240 − 40²/8 = 40 and Sxy = 520 − 40 × 96/8 = 40.', 'b = Sxy/Sxx = 1.', 'a = ȳ − bx̄ = 12 − 5 = 7.', 'y = 7 + x.'),
  E('Residual sum of squares', 'For the same data, Syy = 50. Find the residual sum of squares and comment.', 'RSS = Syy − Sxy²/Sxx.', '= 50 − 40²/40.', '= 10.', 'The line explains 40 of the 50 units of variation in y.')],
 [F('Sxy = 30 and Sxx = 12.', 'b = [[2.5]]'),
  F('Observed y = 14 and predicted y = 11.5.', 'residual = [[2.5]]'),
  F('x̄ = 3, ȳ = 10 and b = 2.', 'a = [[4]]')],
 [X('<p>For 10 pairs of values: Σx = 55, Σy = 320, Σx² = 385, Σxy = 1953 and Σy² = 10 720.</p>',
    P('Find Sxx and Sxy.', [('B1', 'Sxx = 82.5'), ('B1', 'Sxy = 193')]),
    P('Find the equation of the regression line of y on x.', [('M1', 'b = 193/82.5 = 2.339'), ('M1', 'a = 32 − 2.339 × 5.5'), ('A1', 'y = 19.13 + 2.339x')]),
    P('Estimate y when x = 7.', [('B1', '35.5')], ans=a + 7 * b, tol=2e-3),
    P('Find the residual sum of squares.', [('M1', 'Syy = 480 and RSS = Syy − Sxy²/Sxx'), ('A1', '28.5')], ans=RSS, tol=3e-3)),
  X('<p>A residual plot for a linear regression model shows the residuals forming a clear U-shaped curve.</p>',
    P('Explain what this suggests about the model.', [('B1', 'the residuals are not randomly scattered'), ('B1', 'a non-linear model would be more suitable')])),
  X('<p>The regression line of y on x is y = 3.2 + 1.5x.</p>',
    P('Find the residual for the data point (6, 18).', [('M1', 'predicted value 3.2 + 1.5 × 6 = 12.2'), ('A1', '5.8')], ans=5.8))])

# ------------------------------------------------------------------ fs2-continuous
f = lambda x: 0.75 * x * (2 - x)
assert close(integ(f, 0, 2), 1) and close(integ(lambda x: x * f(x), 0, 2), 1) and close(integ(lambda x: x * x * f(x), 0, 2) - 1, 0.2)
assert close(4 ** (1 / 3) ** 3 if False else (4 ** (1 / 3)) ** 3 / 8, 0.5) and rd(4 ** (1 / 3), 3) == 1.587
assert (2 + 8) / 2 == 5 and 36 / 12 == 3 and 1.5 / 6 == 0.25
f2 = lambda x: (x + 1) / 4
assert close(integ(f2, 0, 2), 1) and close(integ(f2, 0, math.sqrt(5) - 1), 0.5) and close(integ(lambda x: x * f2(x), 0, 2), 7 / 6) and rd(math.sqrt(5) - 1, 3) == 1.236
assert close(((3 - 1) ** 2 - (2 - 1) ** 2) / 9, 1 / 3)
deep('fs2-continuous',
 'Use ∫f(x) dx = 1 over the support to find any constant, and remember that probabilities are areas, so P(X = a) = 0. Move between f and F by integrating and differentiating; the median m satisfies F(m) = ½, the mode is where f is greatest, and Var(X) = E(X²) − [E(X)]².',
 [E('Finding a constant, the mean and the variance', 'X has density f(x) = kx(2 − x) for 0 ≤ x ≤ 2. Find k, E(X) and Var(X).', 'k∫ (2x − x²) dx from 0 to 2 = k(4 − 8/3) = 4k/3 = 1, so k = ¾.', 'The density is symmetric about x = 1, so E(X) = 1.', 'E(X²) = ¾∫ (2x³ − x⁴) dx = ¾(8 − 32/5) = 1.2.', 'Var(X) = 1.2 − 1² = 0.2.'),
  E('A median from the distribution function', 'X has density f(x) = 3x²/8 for 0 ≤ x ≤ 2. Find the median.', 'F(x) = x³/8 for 0 ≤ x ≤ 2.', 'Median m: m³/8 = ½.', 'm³ = 4.', 'm = ∛4 = 1.587.'),
  E('A continuous uniform distribution', 'X ~ U[2, 8]. Find E(X), Var(X) and P(X > 6.5).', 'E(X) = (2 + 8)/2 = 5.', 'Var(X) = (8 − 2)²/12 = 3.', 'P(X > 6.5) = (8 − 6.5)/6 = 0.25.')],
 [F('X ~ U[0, 10].', 'E(X) = [[5]]'),
  F('F(x) = x² for 0 ≤ x ≤ 1.', 'P(X ≤ 0.5) = [[0.25]]'),
  F('f(x) = k for 0 ≤ x ≤ 4.', 'k = [[0.25]]')],
 [X('<p>X has probability density function f(x) = k(x + 1) for 0 ≤ x ≤ 2, and 0 otherwise.</p>',
    P('Find the value of k.', [('M1', 'k∫ (x + 1) dx from 0 to 2 = 4k'), ('A1', 'k = ¼')], ans=0.25),
    P('Find the cumulative distribution function F(x) for 0 ≤ x ≤ 2.', [('M1', 'integrates from 0 to x'), ('A1', 'F(x) = (x² + 2x)/8')]),
    P('Find the median of X, giving your answer to 3 significant figures.', [('M1', '(m² + 2m)/8 = ½'), ('M1', 'm² + 2m − 4 = 0'), ('A1', 'm = −1 + √5 = 1.24')], ans=math.sqrt(5) - 1, tol=3e-3),
    P('Find E(X).', [('M1', '¼∫ x(x + 1) dx from 0 to 2'), ('A1', '7/6')], ans=7 / 6)),
  X('<p>X has distribution function F(x) = 0 for x &lt; 1, F(x) = (x − 1)²/9 for 1 ≤ x ≤ 4, and F(x) = 1 for x &gt; 4.</p>',
    P('Find P(2 &lt; X &lt; 3).', [('M1', 'F(3) − F(2)'), ('A1', '⅓')], ans=1 / 3),
    P('Find the probability density function of X.', [('M1', 'differentiates F'), ('A1', 'f(x) = 2(x − 1)/9 for 1 ≤ x ≤ 4, and 0 otherwise')]),
    P('Write down the mode of X.', [('B1', '4')], ans=4)),
  X('', P('X ~ U[a, b] has mean 6 and variance 3. Find a and b.', [('M1', '(a + b)/2 = 6'), ('M1', '(b − a)²/12 = 3, so b − a = 6'), ('A1', 'a = 3, b = 9')]))])

# ------------------------------------------------------------------ fs2-correlation
assert 54 / math.sqrt(40 * 90) == 0.9 and rd(1 - 6 * 8 / (6 * 35)) == 0.7714
assert rd(rcrit(10, 0.05), 4) == 0.5494 and 0.6 > rcrit(10, 0.05) and rd(rcrit(12, 0.01), 4) == 0.6581
assert 1 - 6 * 4 / 120 == 0.8 and close(-85 / math.sqrt(125 * 80), -0.85)
rA, rB = [1, 2, 3, 4, 5, 6], [2, 1, 3, 4, 6, 5]; d2 = sum((p - q) ** 2 for p, q in zip(rA, rB)); rs = 1 - 6 * d2 / (6 * 35)
assert d2 == 4 and rd(rs) == 0.8857 and close(rs, stats.spearmanr(rA, rB)[0])
deep('fs2-correlation',
 'Use the product moment coefficient r = Sxy/√(SxxSyy) for a linear relationship between bivariate normal data, and Spearman’s rank coefficient when the data are ranks or the relationship is monotonic but not linear. In a test, compare the coefficient with the critical value for the sample size, tail and significance level, and state the conclusion in context.',
 [E('Product moment correlation', 'For a set of data, Sxx = 40, Syy = 90 and Sxy = 54. Find the product moment correlation coefficient.', 'r = Sxy/√(Sxx Syy).', '= 54/√3600.', '= 54/60 = 0.9.'),
  E('Spearman’s rank coefficient', 'Two judges rank 6 entries and Σd² = 8. Find Spearman’s rank correlation coefficient.', 'r_s = 1 − 6Σd²/[n(n² − 1)].', '= 1 − 48/(6 × 35).', '= 0.771.'),
  E('A test for positive correlation', 'For a sample of 10 pairs, r = 0.6. Test at the 5% level whether there is positive correlation in the population.', 'H₀: ρ = 0, H₁: ρ > 0.', 'The 5% one-tailed critical value for n = 10 is 0.5494.', '0.6 > 0.5494, so reject H₀.', 'There is evidence of positive correlation.')],
 [F('n = 5 and Σd² = 4.', 'r_s = [[0.8]]'),
  F('Perfect negative linear correlation.', 'r = [[-1]]'),
  F('Spearman’s formula.', 'r_s = 1 − [[6]]Σd²/[n(n² − 1)]')],
 [X('<p>For 12 pairs of data, Sxx = 125, Syy = 80 and Sxy = −85.</p>',
    P('Calculate the product moment correlation coefficient.', [('M1', '−85/√(125 × 80)'), ('A1', '−0.85')], ans=-0.85),
    P('Test, at the 1% level, whether there is negative correlation in the population. The critical value is −0.6581.', [('B1', 'H₀: ρ = 0, H₁: ρ &lt; 0'), ('M1', 'compares −0.85 with −0.6581'), ('A1', 'reject H₀: evidence of negative correlation')])),
  X('<p>Two judges rank six photographs. Judge A ranks them 1, 2, 3, 4, 5, 6 and Judge B ranks the same photographs 2, 1, 3, 4, 6, 5.</p>',
    P('Calculate Spearman’s rank correlation coefficient.', [('M1', 'Σd² = 4'), ('M1', '1 − 6 × 4/(6 × 35)'), ('A1', '0.886')], ans=rs, tol=2e-3),
    P('Test, at the 5% level, whether the judges agree. The critical value is 0.8286.', [('B1', 'H₀: ρ = 0, H₁: ρ &gt; 0'), ('A1', '0.886 &gt; 0.8286: reject H₀; evidence of agreement')])),
  X('', P('Give two situations in which Spearman’s rank correlation coefficient is more appropriate than the product moment correlation coefficient.', [('B1', 'the data are given as ranks or cannot be measured on a scale'), ('B1', 'the relationship is monotonic but not linear, or the data are not bivariate normal')]))])

# ------------------------------------------------------------------ fs2-combinations
assert rd(1 - Z.cdf(-2)) == 0.9772 and rd(1 - Z.cdf(20 / math.sqrt(500))) == 0.1855
p1 = 1 - Z.cdf((4 - 5) / 2.5); p2 = 1 - Z.cdf((-18 + 20) / math.sqrt(13)); assert rd(p1) == 0.6554 and rd(p2) == 0.2895
assert rd(Z.cdf(-0.5)) == 0.3085 and 2 * 3 + 3 + 1 == 10 and 4 * 2 + 9 * 5 == 53
deep('fs2-combinations',
 'Write the mean and the variance of the combination separately: E(aX + bY) = aE(X) + bE(Y), and for independent variables Var(aX + bY) = a²Var(X) + b²Var(Y), so the variances add even when the variables are subtracted. Distinguish 3X (one value tripled, variance 9σ²) from X₁ + X₂ + X₃ (three independent values, variance 3σ²).',
 [E('Comparing two normal variables', 'X ~ N(50, 9) and Y ~ N(40, 16) are independent. Find P(X > Y).', 'X − Y ~ N(50 − 40, 9 + 16) = N(10, 25).', 'P(X > Y) = P(X − Y > 0).', 'z = (0 − 10)/5 = −2.', 'P(Z > −2) = 0.9772.'),
  E('A total of several values', 'Apples have masses N(120, 10²) grams, independently. Find the probability that 5 apples have a total mass over 620 g.', 'Total T ~ N(5 × 120, 5 × 100) = N(600, 500).', 'z = (620 − 600)/√500 = 0.894.', 'P(T > 620) = 0.1855.'),
  E('Multiples and sums', 'X has variance σ². Compare Var(3X) with Var(X₁ + X₂ + X₃), where the Xᵢ are independent copies of X.', 'Var(3X) = 3²σ² = 9σ².', 'Var(X₁ + X₂ + X₃) = σ² + σ² + σ² = 3σ².', 'Tripling one value is more variable than adding three independent values.')],
 [F('Independent X and Y with Var(X) = 4 and Var(Y) = 9.', 'Var(X + Y) = [[13]]'),
  F('E(X) = 5 and E(Y) = 4.', 'E(3X − 2Y) = [[7]]'),
  F('Var(X) = 3.', 'Var(2X) = [[12]]')],
 [X('<p>A ~ N(30, 2²) and B ~ N(25, 1.5²) are independent.</p>',
    P('Find P(A − B &gt; 4).', [('M1', 'A − B ~ N(5, 6.25)'), ('M1', 'standardises: z = −0.4'), ('A1', '0.6554')], ans=p1, tol=1e-3),
    P('Find P(A &gt; 2B − 18).', [('M1', 'considers A − 2B'), ('M1', 'mean −20, variance 4 + 4 × 2.25 = 13'), ('M1', 'P(A − 2B &gt; −18): z = 2/√13'), ('A1', '0.2895')], ans=p2, tol=1e-3)),
  X('', P('X₁, X₂, X₃ and X₄ are independent, each with distribution N(15, 4). Find the probability that their total is less than 58.', [('M1', 'total ~ N(60, 16)'), ('M1', 'z = (58 − 60)/4'), ('A1', '0.3085')], ans=Z.cdf(-0.5), tol=1e-3)),
  X('<p>X and Y are independent with E(X) = 3, Var(X) = 2, E(Y) = −1 and Var(Y) = 5.</p>',
    P('Find E(2X − 3Y + 1) and Var(2X − 3Y + 1).', [('B1', 'mean 10'), ('M1', '4 × 2 + 9 × 5'), ('A1', 'variance 53')]))])

# ------------------------------------------------------------------ fs2-normal-ci
z99 = Z.ppf(0.995); lo, hi = 52.3 - z99 * 0.8, 52.3 + z99 * 0.8; assert rd(lo, 2) == 50.24 and rd(hi, 2) == 54.36
se = math.sqrt(16 / 40 + 25 / 50); assert rd(1.7 / se, 3) == 1.792 and 1.7 / se > Z.ppf(0.95)
se2 = 2.5 / math.sqrt(50); assert rd(101.4 - 1.96 * se2, 2) == 100.71 and rd(101.4 + 1.96 * se2, 2) == 102.09 and math.ceil((2 * 1.96 * 2.5) ** 2) == 97
se3 = math.sqrt(9 / 60 + 6.25 / 40); assert rd(1.3 / se3, 3) == 2.349 and 1.3 / se3 > 1.96
assert 6 / 6 == 1 and close(2 * 1.96 * 2, 7.84)
deep('fs2-normal-ci',
 'Find the standard error before anything else: σ/√n for one mean, √(σ₁²/n₁ + σ₂²/n₂) for a difference of independent means. A confidence interval is estimate ± z × standard error; a test compares (estimate − hypothesised value)/standard error with a critical value. If the population is not normal, a large sample lets you use the central limit theorem.',
 [E('A 99% confidence interval', 'A normal population has σ = 4. A sample of 25 has mean 52.3. Find a 99% confidence interval for μ.', 'Standard error = 4/√25 = 0.8.', 'For 99%, z = 2.5758.', '52.3 ± 2.5758 × 0.8 = 52.3 ± 2.06.', '(50.24, 54.36).'),
  E('Comparing two means', 'Sample A: n = 40, mean 31.2, σ² = 16. Sample B: n = 50, mean 29.5, σ² = 25. Test at the 5% level whether μ_A > μ_B.', 'H₀: μ_A = μ_B, H₁: μ_A > μ_B.', 'Standard error = √(16/40 + 25/50) = 0.9487.', 'z = (31.2 − 29.5)/0.9487 = 1.792.', '1.792 > 1.6449: reject H₀; evidence that the mean of A is greater.')],
 [F('σ = 6 and n = 36.', 'standard error = [[1]]'),
  F('A 95% confidence interval.', 'z = [[1.96]]'),
  F('Standard error 2 with a 95% interval.', 'width = 2 × 1.96 × 2 = [[7.84]]')],
 [X('<p>The masses of packets are normally distributed with standard deviation 2.5 g. A random sample of 50 packets has mean mass 101.4 g.</p>',
    P('Find a 95% confidence interval for the mean mass.', [('M1', 'standard error 2.5/√50'), ('M1', '101.4 ± 1.96 × 0.354'), ('A1', '(100.71, 102.09)')]),
    P('The manufacturer claims the mean mass is 100 g. Comment on this claim.', [('B1', '100 lies outside the interval, so the evidence suggests the mean is not 100 g')]),
    P('Find the smallest sample size for which the width of a 95% interval is at most 1 g.', [('M1', '2 × 1.96 × 2.5/√n ≤ 1'), ('M1', '√n ≥ 9.8'), ('A1', 'n = 97')], ans=97)),
  X('<p>Group A: 60 observations with mean 12.4 from a population with variance 9. Group B: 40 observations with mean 11.1 from a population with variance 6.25.</p>',
    P('Test, at the 5% level, whether the population means differ.', [('B1', 'H₀: μ_A = μ_B, H₁: μ_A ≠ μ_B'), ('M1', 'standard error √(9/60 + 6.25/40) = 0.553'), ('M1', 'z = 1.3/0.553'), ('A1', '2.35'), ('A1', '2.35 &gt; 1.96: reject H₀; the means differ')])),
  X('', P('Explain why the central limit theorem allows a normal distribution to be used for a sample mean even when the population is not known to be normal.', [('B1', 'for a large sample the sample mean is approximately normally distributed, whatever the population distribution')]))])

# ------------------------------------------------------------------ fs2-variance
st = 11 * 2.9 / 1.5; assert rd(st, 2) == 21.27 and rd(C2.ppf(0.95, 11), 3) == 19.675
assert rd(C2.ppf(0.975, 9), 3) == 19.023 and rd(C2.ppf(0.025, 9), 3) == 2.700 and rd(9 * 4.2 / 19.023, 2) == 1.99 and rd(9 * 4.2 / 2.700, 1) == 14.0
assert rd(8.4 / 3.1, 3) == 2.710 and rd(Fd.ppf(0.95, 8, 12), 3) == 2.849
s1 = 15 * 0.81 / 0.5; assert rd(s1, 1) == 24.3 and rd(C2.ppf(0.025, 15), 3) == 6.262 and rd(C2.ppf(0.975, 15), 3) == 27.488
assert rd(14.2 / 5.1, 3) == 2.784 and rd(Fd.ppf(0.95, 7, 9), 3) == 3.293
l1, l2 = 19 * 3.4 ** 2 / C2.ppf(0.975, 19), 19 * 3.4 ** 2 / C2.ppf(0.025, 19); assert rd(math.sqrt(l1), 2) == 2.59 and rd(math.sqrt(l2), 2) == 4.97
deep('fs2-variance',
 'For one variance, (n − 1)S²/σ² has a χ² distribution with n − 1 degrees of freedom, so tests and confidence intervals both come from χ² tables; note that the interval is not symmetric. To compare two variances, put the larger sample variance on top of the F ratio and use degrees of freedom (numerator n − 1, denominator n − 1) in that order.',
 [E('A test for a variance', 'A sample of 12 from a normal population has s² = 2.9. Test at the 5% level whether σ² > 1.5.', 'H₀: σ² = 1.5, H₁: σ² > 1.5.', 'Test statistic (n − 1)s²/σ² = 11 × 2.9/1.5 = 21.27.', 'χ²₁₁ upper 5% value = 19.675.', '21.27 > 19.675: reject H₀; evidence that the variance exceeds 1.5.'),
  E('A confidence interval for a variance', 'A sample of 10 from a normal population has s² = 4.2. Find a 95% confidence interval for σ².', 'χ²₉ percentage points: 2.700 and 19.023.', 'Lower limit 9 × 4.2/19.023 = 1.99.', 'Upper limit 9 × 4.2/2.700 = 14.0.', 'The interval is (1.99, 14.0).'),
  E('An F-test', 'Samples of sizes 9 and 13 have variances 8.4 and 3.1. Test at the 5% level whether the first population has the larger variance.', 'H₀: σ₁² = σ₂², H₁: σ₁² > σ₂².', 'F = 8.4/3.1 = 2.710 with (8, 12) degrees of freedom.', 'Critical value F₈,₁₂(5%) = 2.849.', '2.710 < 2.849: do not reject H₀.')],
 [F('A test for a variance with n = 15.', 'degrees of freedom = [[14]]'),
  F('An F-test with sample sizes 7 (numerator) and 10.', 'degrees of freedom ([[6]], [[9]])'),
  F('n = 5, s² = 8 and σ² = 4.', '(n − 1)s²/σ² = [[8]]')],
 [X('<p>A sample of 16 observations from a normal population has s² = 0.81.</p>',
    P('Test, at the 5% level, whether the population variance differs from 0.5.', [('B1', 'H₀: σ² = 0.5, H₁: σ² ≠ 0.5'), ('M1', 'statistic 15 × 0.81/0.5'), ('A1', '24.3'), ('B1', 'critical values 6.262 and 27.488'), ('A1', 'do not reject H₀: no evidence that the variance differs from 0.5')])),
  X('<p>Two independent samples from normal populations: sample 1 has n = 8 and s² = 14.2; sample 2 has n = 10 and s² = 5.1.</p>',
    P('Test, at the 10% level, whether the population variances differ.', [('M1', 'F = 14.2/5.1 = 2.78'), ('B1', '(7, 9) degrees of freedom'), ('B1', 'critical value 3.293 for 5% in the upper tail'), ('A1', 'do not reject H₀: no evidence that the variances differ')])),
  X('', P('A sample of 20 from a normal population has standard deviation 3.4. Find a 95% confidence interval for the population standard deviation.', [('M1', '19 × 3.4²/χ² values 32.852 and 8.907'), ('A1', 'interval for σ²: (6.69, 24.7)'), ('M1', 'takes square roots'), ('A1', '(2.59, 4.97)')]),
    P('Explain why this interval is not symmetric about 3.4.', [('B1', 'the χ² distribution is not symmetric (it is positively skewed)')]))])

# ------------------------------------------------------------------ fs2-t
t1 = 1.6 / (1.8 / math.sqrt(8)); assert rd(t1, 3) == 2.514 and rd(T.ppf(0.95, 7), 3) == 1.895
h = T.ppf(0.975, 11) * 5.1 / math.sqrt(12); assert rd(T.ppf(0.975, 11), 3) == 2.201 and rd(48.2 - h, 2) == 44.96 and rd(48.2 + h, 2) == 51.44
sp2 = (5 * 4 + 7 * 5.2) / 12; t3 = 2.4 / math.sqrt(sp2 * (1 / 6 + 1 / 8)); assert close(sp2, 4.7) and rd(t3, 2) == 2.05 and rd(T.ppf(0.95, 12), 3) == 1.782
t4 = 1.75 / (2.05 / math.sqrt(8)); assert rd(t4, 3) == 2.415 and t4 > 1.895
h5 = T.ppf(0.95, 9) * 6.3 / math.sqrt(10); assert rd(T.ppf(0.95, 9), 3) == 1.833 and rd(72.4 - h5, 2) == 68.75 and rd(72.4 + h5, 2) == 76.05
deep('fs2-t',
 'Use the t-distribution when the population is normal but its variance is estimated from the sample. A one-sample or paired test has n − 1 degrees of freedom; a two-sample test with a pooled variance has n₁ + n₂ − 2. For paired data, work with the differences as a single sample.',
 [E('A one-sample t-test', 'A sample of 8 from a normal population has mean 14.6 and s = 1.8. Test at the 5% level whether μ > 13.', 'H₀: μ = 13, H₁: μ > 13.', 't = (14.6 − 13)/(1.8/√8) = 2.514.', 't₇ upper 5% value = 1.895.', '2.514 > 1.895: reject H₀; evidence that the mean exceeds 13.'),
  E('A t confidence interval', 'A sample of 12 from a normal population has mean 48.2 and s = 5.1. Find a 95% confidence interval for μ.', 't₁₁ value for 95% = 2.201.', 'Standard error 5.1/√12 = 1.472.', '48.2 ± 2.201 × 1.472 = 48.2 ± 3.24.', '(44.96, 51.44).'),
  E('A pooled two-sample test', 'Sample 1: n = 6, mean 20.5, s² = 4.0. Sample 2: n = 8, mean 18.1, s² = 5.2. Assuming normal populations with equal variances, test at the 5% level whether μ₁ > μ₂.', 'Pooled s² = (5 × 4.0 + 7 × 5.2)/12 = 4.7.', 't = 2.4/√(4.7(1/6 + 1/8)) = 2.05.', 't₁₂ upper 5% value = 1.782.', '2.05 > 1.782: reject H₀; evidence that μ₁ > μ₂.')],
 [F('A one-sample t-test with n = 15.', 'degrees of freedom = [[14]]'),
  F('A pooled test with n₁ = 6 and n₂ = 8.', 'degrees of freedom = [[12]]'),
  F('s = 4 and n = 16.', 'estimated standard error = [[1]]')],
 [X('<p>Eight students each sit two tests. The differences (second − first) have mean 1.75 and standard deviation 2.05.</p>',
    P('Test, at the 5% level, whether scores on the second test are higher on average.', [('B1', 'H₀: μ_d = 0, H₁: μ_d &gt; 0'), ('M1', 't = 1.75/(2.05/√8)'), ('A1', '2.41'), ('B1', 'critical value t₇ = 1.895'), ('A1', 'reject H₀: evidence that scores are higher on the second test')]),
    P('State an assumption needed for this test.', [('B1', 'the differences are normally distributed')])),
  X('', P('A sample of 10 from a normal population has mean 72.4 and standard deviation 6.3. Find a 90% confidence interval for the population mean.', [('B1', 't₉ = 1.833'), ('M1', '72.4 ± 1.833 × 6.3/√10'), ('A1', '(68.75, 76.05)')])),
  X('', P('State the assumptions needed for a two-sample t-test using a pooled variance.', [('B1', 'both populations are normally distributed'), ('B1', 'the population variances are equal and the samples are independent')]))])

# ------------------------------------------------------------------ fm2-circular
T1 = 0.2 * g / math.cos(math.radians(30)); w2 = T1 * 0.5 / (0.2 * 0.25); assert rd(T1, 3) == 2.263 and rd(math.sqrt(w2), 2) == 4.76
v2 = 49 - 2 * g * 1.6; assert close(v2, 17.64) and close(0.5 * (v2 / 0.8 - g), 6.125) and 36 - 2 * g * 1.6 < 0.8 * g
assert rd(math.sqrt(50 * g * math.tan(math.radians(20))), 2) == 13.35
assert rd(math.sqrt(0.5 * g * 60), 2) == 17.15 and rd(math.degrees(math.acos(2 / 3)), 1) == 48.2
Tc = 0.3 * 16 * 1.2; assert close(Tc, 5.76) and rd(math.degrees(math.acos(0.3 * g / Tc)), 1) == 59.3
assert 3 * 2 == 6 and 16 / 2 == 8
deep('fm2-circular',
 'Mark the centre of the circle and resolve towards it: the resultant inward force equals mv²/r = mrω². In a vertical circle, energy links the speeds at different heights; a string stays taut while the tension is positive, whereas a particle on a rigid rod or inside a tube only needs speed at the top.',
 [E('A conical pendulum', 'A particle of mass 0.2 kg on a string of length 0.5 m moves in a horizontal circle with the string at 30° to the vertical. Find the tension and the angular speed.', 'Vertically: T cos 30° = 0.2g, so T = 2.263 N.', 'Radius r = 0.5 sin 30° = 0.25 m.', 'Horizontally: T sin 30° = 0.2 × 0.25ω².', 'ω² = 22.6, so ω = 4.76 rad s⁻¹.'),
  E('A vertical circle', 'A particle of mass 0.5 kg on a string of length 0.8 m is moving in a vertical circle. Its speed at the lowest point is 7 m s⁻¹. Find its speed and the tension at the highest point.', 'Energy: v² = 7² − 2g(1.6) = 17.64.', 'v = 4.2 m s⁻¹.', 'At the top: T + 0.5g = 0.5 × 17.64/0.8.', 'T = 6.125 N; positive, so the string is taut.'),
  E('A banked track', 'A car travels round a smooth track banked at 20° in a horizontal circle of radius 50 m. Find the speed at which there is no tendency to slip.', 'Vertically: R cos 20° = mg.', 'Horizontally: R sin 20° = mv²/50.', 'Dividing: v² = 50g tan 20° = 178.3.', 'v = 13.4 m s⁻¹.')],
 [F('ω = 3 rad s⁻¹ and r = 2 m.', 'v = [[6]] m s⁻¹'),
  F('v = 4 m s⁻¹ and r = 2 m.', 'acceleration towards the centre = [[8]] m s⁻²'),
  F('2 revolutions per second.', 'ω = [[4]]π rad s⁻¹')],
 [X('', P('A car moves on a horizontal circular track of radius 60 m. The coefficient of friction between the tyres and the track is 0.5. Find the greatest speed at which the car can travel without slipping.', [('M1', 'friction provides the central force: μmg = mv²/60'), ('M1', 'v² = 0.5 × 9.8 × 60'), ('A1', '17.1 m s⁻¹')], ans=math.sqrt(294), unit='m s⁻¹', tol=3e-3)),
  X('<p>A particle is released from rest at the top of a smooth fixed sphere of radius a and slides down its outside surface.</p>',
    P('Find the angle between the radius to the particle and the upward vertical when it leaves the surface.', [('M1', 'energy: v² = 2ga(1 − cos θ)'), ('M1', 'radial equation: mg cos θ − R = mv²/a'), ('M1', 'sets R = 0'), ('A1', 'cos θ = ⅔'), ('A1', 'θ = 48.2°')], ans=48.2, unit='°', tol=3e-3)),
  X('<p>A particle of mass 0.3 kg is attached to a string of length 1.2 m whose other end is fixed. It moves in a horizontal circle with angular speed 4 rad s⁻¹.</p>',
    P('Find the tension in the string.', [('M1', 'T sin θ = m(l sin θ)ω², so T = mlω²'), ('A1', '5.76 N')], ans=5.76, unit='N'),
    P('Find the angle between the string and the vertical.', [('M1', 'T cos θ = mg'), ('A1', 'cos θ = 0.510, θ = 59.3°')], ans=59.3, unit='°', tol=3e-3))])

# ------------------------------------------------------------------ fm2-centres
assert (12 * 3 + 8 * 1) / 20 == 2.2 and (12 * 1 + 8 * 4) / 20 == 2.2
A_ = integ(lambda x: x * x, 0, 2); assert close(A_, 8 / 3) and close(integ(lambda x: x ** 3, 0, 2) / A_, 1.5) and close(0.5 * integ(lambda x: x ** 4, 0, 2) / A_, 1.2)
xs = (16 * 2 - 4 * 3) / 12; assert close(xs, 5 / 3) and rd(math.degrees(math.atan((5 / 3) / (4 - 5 / 3))), 1) == 35.5
A2 = integ(math.sqrt, 0, 4); assert close(A2, 16 / 3) and close(integ(lambda x: x ** 1.5, 0, 4) / A2, 2.4) and close(0.5 * integ(lambda x: x, 0, 4) / A2, 0.75)
assert close((3 * 1 + 2 * 2) / 6, 7 / 6) and (2 * 0 + 6 * 4) / 8 == 3
deep('fm2-centres',
 'Split a composite body into simple parts, list each part’s mass (or area) and centre in a table, and take moments about a chosen axis; a removed part contributes a negative mass. For a region under a curve, use x̄ = ∫xy dx/∫y dx and ȳ = ½∫y² dx/∫y dx. A suspended body hangs with its centre of mass vertically below the point of suspension.',
 [E('A composite lamina', 'An L-shaped lamina is made from a 6 × 2 rectangle along the x-axis (0 ≤ x ≤ 6, 0 ≤ y ≤ 2) and a 2 × 4 rectangle on top (0 ≤ x ≤ 2, 2 ≤ y ≤ 6). Find its centre of mass.', 'Areas 12 and 8, with centres (3, 1) and (1, 4).', 'x̄ = (12 × 3 + 8 × 1)/20 = 2.2.', 'ȳ = (12 × 1 + 8 × 4)/20 = 2.2.', 'The centre of mass is (2.2, 2.2).'),
  E('A region under a curve', 'Find the centre of mass of the uniform lamina bounded by y = x², the x-axis and x = 2.', 'Area = ∫ x² dx from 0 to 2 = 8/3.', 'x̄ = ∫ x³ dx/(8/3) = 4/(8/3) = 1.5.', 'ȳ = ½∫ x⁴ dx/(8/3) = 3.2/(8/3) = 1.2.', 'The centre of mass is (1.5, 1.2).'),
  E('Hanging freely', 'The L-shaped lamina in the first example is suspended from the origin. Find the angle between the edge along the x-axis and the vertical.', 'The centre of mass (2.2, 2.2) hangs vertically below the origin.', 'The angle between the x-axis edge and the line to the centre of mass has tan θ = 2.2/2.2.', 'θ = 45°.')],
 [F('Particles of 2 kg at x = 0 and 6 kg at x = 4.', 'x̄ = [[3]]'),
  F('A uniform rod from x = 0 to x = 8.', 'x̄ = [[4]]'),
  F('A triangle with vertices (0, 0), (6, 0) and (0, 3).', 'x̄ = [[2]]')],
 [X('<p>A uniform square lamina OABC has side 4 cm, with O at the origin and A at (4, 0). A square of side 2 cm in the corner 2 ≤ x ≤ 4, 2 ≤ y ≤ 4 is removed.</p>',
    P('Show that the centre of mass of the remaining lamina is at (5/3, 5/3).', [('M1', 'areas 16 and −4 with centres (2, 2) and (3, 3)'), ('M1', 'moments: (16 × 2 − 4 × 3)/12'), ('A1', '5/3 for both coordinates by symmetry')]),
    P('The lamina is suspended from A and hangs in equilibrium. Find the angle between OA and the vertical.', [('M1', 'horizontal and vertical distances from A: 7/3 and 5/3'), ('M1', 'tan θ = (5/3)/(7/3)'), ('A1', '35.5°')], ans=35.5, unit='°', tol=3e-3)),
  X('<p>R is the region bounded by y = √x, the x-axis and the line x = 4.</p>',
    P('Find the coordinates of the centre of mass of a uniform lamina occupying R.', [('M1', 'area 16/3'), ('M1', '∫ x√x dx = 64/5'), ('A1', 'x̄ = 2.4'), ('M1', '½∫ x dx = 4'), ('A1', 'ȳ = 0.75')])),
  X('', P('A uniform rod AB of length 2 m and mass 3 kg has particles of mass 1 kg at A and 2 kg at B. Find the distance of the centre of mass from A.', [('M1', '(3 × 1 + 1 × 0 + 2 × 2)/6'), ('A1', '7/6 m')], ans=7 / 6, unit='m'))])

# ------------------------------------------------------------------ fm2-equilibrium
S = 20 * g * 2.5 * math.cos(math.radians(60)) / (5 * math.sin(math.radians(60))); assert rd(S, 2) == 56.58 and close(S / (20 * g), 1 / (2 * math.sqrt(3)))
assert rd(math.degrees(math.atan(0.6)), 1) == 31.0 and rd(math.degrees(math.atan(0.5 / 1.2)), 1) == 22.6
assert close(1 / (2 * 0.4), 1.25) and rd(math.degrees(math.atan(1.25)), 1) == 51.3
Tr = 10 * g * 1.5 / (3 * 2 / math.sqrt(13)); assert rd(Tr, 1) == 88.3
assert 30 * 0.4 == 12 and 0.3 * 50 == 15 and 0.3 / 0.6 == 0.5
deep('fm2-equilibrium',
 'Draw every force and take moments about a point that removes unknown forces, then resolve in two perpendicular directions. In limiting equilibrium friction equals μR, acting to oppose the impending motion. For a block on a slope, compare the angle for sliding (tan α = μ) with the angle for toppling (the weight’s line of action passes through the lower edge).',
 [E('A ladder against a smooth wall', 'A uniform ladder of length 5 m and mass 20 kg rests against a smooth vertical wall at 60° to rough horizontal ground. It is about to slip. Find the coefficient of friction.', 'Moments about the foot: S × 5 sin 60° = 20g × 2.5 cos 60°.', 'S = 56.6 N.', 'Resolving: F = S and R = 20g = 196 N.', 'μ = F/R = 56.6/196 = 0.289 (exactly 1/(2√3)).'),
  E('Slide or topple?', 'A uniform block with base 0.5 m and height 1.2 m stands on a rough plane (μ = 0.6) whose angle is slowly increased. Does it slide or topple first?', 'It would slide when tan α = μ = 0.6, at α = 31.0°.', 'It would topple when tan α = 0.5/1.2, at α = 22.6°.', '22.6° < 31.0°, so the block topples first.')],
 [F('A force of 30 N at a perpendicular distance of 0.4 m.', 'moment = [[12]] N m'),
  F('μ = 0.3 and R = 50 N.', 'limiting friction = [[15]] N'),
  F('A block of width 0.3 m and height 0.6 m.', 'topples when tan α = [[0.5]]')],
 [X('<p>A uniform ladder of length 4 m and mass 12 kg rests with its foot on rough horizontal ground and its top against a smooth vertical wall. The coefficient of friction is 0.4, and the ladder makes an angle α with the ground.</p>',
    P('Find the least value of tan α for which the ladder can rest in equilibrium.', [('M1', 'moments about the foot: S × 4 sin α = 12g × 2 cos α'), ('M1', 'R = 12g and F = S'), ('M1', 'limiting: F = 0.4R'), ('A1', 'tan α = 1.25'), ('A1', 'α = 51.3°')], ans=1.25),
    P('State how you have used the fact that the wall is smooth.', [('B1', 'the reaction at the wall is perpendicular to the wall: there is no friction there')])),
  X('<p>A uniform rod AB of length 3 m and mass 10 kg is hinged to a vertical wall at A. It is held horizontal by a light string from B to the point C on the wall 2 m vertically above A.</p>',
    P('Find the tension in the string.', [('M1', 'moments about A'), ('M1', 'perpendicular distance from A to BC: 3 × 2/√13'), ('A1', 'T × 6/√13 = 10g × 1.5'), ('A1', '88.3 N')], ans=Tr, unit='N', tol=3e-3)),
  X('', P('A uniform cube rests on a rough plane with coefficient of friction 0.8. The angle of the plane is slowly increased. Determine whether the cube slides or topples first.', [('B1', 'slides when tan α = 0.8'), ('B1', 'topples when tan α = 1 (45°)'), ('B1', '0.8 &lt; 1, so it slides first')]))])

# ------------------------------------------------------------------ fm2-dynamics
assert 1.5 * 4 == 6 and 0.5 * 8 == 4 and rd(math.log(2) / 0.04, 2) == 17.33
assert close(2 * math.sqrt(0.25 - 0.09), 0.8)
assert 8 * 2 - 2 * 4 == 8 and rd(4 * 16 - 2 / 3 * 64, 2) == 21.33
w = 12 / 3; A_ = 3 / w; assert w == 4 and A_ == 0.75 and close(math.asin(0.5) / 4, math.pi / 24)
tt = 10 * math.log(4); assert rd(tt, 2) == 13.86 and close(200 * (1 - math.exp(-0.1 * tt)), 150)
deep('fm2-dynamics',
 'Write Newton’s second law with the right form of acceleration: dv/dt for force as a function of time, v dv/dx for force as a function of displacement, and separate the variables. For simple harmonic motion, identify ω from ẍ = −ω²x, then use v² = ω²(a² − x²), maximum speed aω, and period 2π/ω.',
 [E('A force varying with time', 'A particle of mass 2 kg starts from rest at the origin and is acted on by a force of 6t N. Find its velocity and displacement at t = 2.', 'a = 6t/2 = 3t.', 'v = 1.5t² (v = 0 at t = 0), so v(2) = 6 m s⁻¹.', 'x = 0.5t³, so x(2) = 4 m.'),
  E('Resistance proportional to v²', 'A boat of mass 200 kg cuts its engine at 10 m s⁻¹. The resistance is 8v² N. Find how far it travels before its speed halves.', '200v dv/dx = −8v², so dv/v = −0.04 dx.', 'ln v = −0.04x + ln 10, so v = 10e^(−0.04x).', 'v = 5 when e^(−0.04x) = ½.', 'x = ln 2/0.04 = 17.3 m.'),
  E('Simple harmonic motion', 'A particle moves with simple harmonic motion of amplitude 0.5 m and period π s. Find its maximum speed and its speed 0.3 m from the centre.', 'Period 2π/ω = π, so ω = 2.', 'Maximum speed aω = 1 m s⁻¹.', 'v² = ω²(a² − x²) = 4(0.25 − 0.09).', 'v = 0.8 m s⁻¹.')],
 [F('SHM with ω = 3 and amplitude 2 m.', 'maximum speed = [[6]] m s⁻¹'),
  F('SHM with ω = 4.', 'period = π/[[2]] s'),
  F('ẍ = −25x at x = 0.2 m.', '|acceleration| = [[5]] m s⁻²')],
 [X('<p>A particle of mass 0.5 kg moves in a straight line. At time t seconds the resultant force on it is (4 − 2t) N. It starts from rest at the origin.</p>',
    P('Find the greatest speed of the particle in the first 4 seconds.', [('M1', 'a = 8 − 4t'), ('M1', 'v = 8t − 2t²'), ('A1', 'greatest at t = 2: 8 m s⁻¹')], ans=8, unit='m s⁻¹'),
    P('Find the distance travelled before the particle next comes to rest.', [('M1', 'v = 0 at t = 4'), ('A1', 'x = 4t² − ⅔t³ = 21.3 m')], ans=64 / 3, unit='m', tol=2e-3)),
  X('<p>A particle moves with simple harmonic motion. Its maximum speed is 3 m s⁻¹ and its maximum acceleration is 12 m s⁻².</p>',
    P('Find the amplitude and the period of the motion.', [('M1', 'aω = 3 and aω² = 12'), ('A1', 'ω = 4'), ('A1', 'a = 0.75 m'), ('A1', 'period π/2 s')]),
    P('Find the time taken to move from the centre to a point 0.375 m from the centre.', [('M1', '0.375 = 0.75 sin 4t'), ('A1', 't = π/24 = 0.131 s')], ans=math.pi / 24, unit='s', tol=3e-3)),
  X('<p>A car moving at 20 m s⁻¹ freewheels so that its deceleration is 0.1v m s⁻².</p>',
    P('Find the time taken for its speed to fall to 5 m s⁻¹.', [('M1', 'separates: ∫ dv/v = −0.1∫ dt'), ('A1', 'v = 20e^(−0.1t)'), ('A1', 't = 10 ln 4 = 13.9 s')], ans=tt, unit='s', tol=3e-3),
    P('Find the distance travelled in this time.', [('M1', 'x = ∫ 20e^(−0.1t) dt = 200(1 − e^(−0.1t))'), ('A1', '150 m')], ans=150, unit='m'))])

# ------------------------------------------------------------------ fm2-kinematics
u, th = 25, math.radians(40); tf = 2 * u * math.sin(th) / g
assert rd(tf, 2) == 3.28 and rd(u * math.cos(th) * tf, 1) == 62.8 and rd((u * math.sin(th)) ** 2 / (2 * g), 1) == 13.2
assert (2 ** 3 + 1, 4 * 2 - 4 + 2) == (9, 6)
tc = math.sqrt(80 / g); assert rd(tc, 3) == 2.857 and rd(15 * tc, 1) == 42.9
assert rd(24 / g, 3) == 2.449 and rd(16 * 24 / g, 1) == 39.2
r_ = np.roots([4.9, -12, 5]); assert rd(abs(r_[0] - r_[1]), 3) == 1.384
assert close(math.hypot(6, 6), 6 * math.sqrt(2)) and (3 * 4 - 8, 8) == (4, 8)
t5 = (15 + math.sqrt(225 + 4 * 4.9 * 20)) / 9.8; assert rd(t5, 3) == 4.065 and rd(30 * math.cos(math.radians(30)) * t5, 1) == 105.6
assert 2 * 9.8 / 9.8 == 2 and 10 * 3 == 30
deep('fm2-kinematics',
 'Treat horizontal and vertical motion separately: the horizontal component of velocity is constant, while the vertical motion has acceleration g downwards. For vector kinematics, differentiate r to get v and a, and integrate the other way, using the initial position or velocity to find each constant vector.',
 [E('A projectile from the ground', 'A ball is projected from level ground at 25 m s⁻¹ at 40° above the horizontal. Find the time of flight, the range and the greatest height.', 'Vertical: 0 = 25 sin 40° t − 4.9t², so t = 3.28 s.', 'Range = 25 cos 40° × 3.28 = 62.8 m.', 'Greatest height = (25 sin 40°)²/(2g) = 13.2 m.'),
  E('Integrating a velocity vector', 'A particle has velocity v = 3t²i + (4 − 2t)j and is at (i + 2j) when t = 0. Find its position when it is moving parallel to i.', 'r = (t³ + 1)i + (4t − t² + 2)j, using the initial position.', 'Parallel to i when the j-component of velocity is 0: 4 − 2t = 0.', 't = 2.', 'r = 9i + 6j.'),
  E('Horizontal projection from a cliff', 'A stone is thrown horizontally at 15 m s⁻¹ from a cliff 40 m high. Find how far from the foot of the cliff it lands.', 'Vertical: 40 = 4.9t², so t = 2.857 s.', 'Horizontal distance = 15 × 2.857.', '42.9 m.')],
 [F('v = 2t i + 3j.', 'a = [[2]]i'),
  F('Vertical component of the initial velocity 9.8 m s⁻¹.', 'time of flight on level ground = [[2]] s'),
  F('Horizontal velocity 10 m s⁻¹ for 3 s.', 'horizontal distance = [[30]] m')],
 [X('<p>A ball is projected from level ground at 20 m s⁻¹ at an angle α above the horizontal, where tan α = ¾.</p>',
    P('Find the time of flight.', [('M1', '0 = 12t − 4.9t²'), ('A1', '2.45 s')], ans=24 / g, unit='s', tol=3e-3),
    P('Find the horizontal range.', [('M1', '16 × 2.449'), ('A1', '39.2 m')], ans=16 * 24 / g, unit='m', tol=3e-3),
    P('Find the length of time for which the ball is more than 5 m above the ground.', [('M1', '12t − 4.9t² = 5'), ('M1', 'solves 4.9t² − 12t + 5 = 0'), ('A1', 't = 0.532 and t = 1.917'), ('A1', '1.38 s')], ans=abs(r_[0] - r_[1]), unit='s', tol=3e-3)),
  X('<p>A particle moves with velocity v = (6t − 4)i + 3t²j m s⁻¹.</p>',
    P('Find the magnitude of its acceleration when t = 1.', [('M1', 'a = 6i + 6tj'), ('A1', '6√2 = 8.49 m s⁻²')], ans=6 * math.sqrt(2), tol=2e-3),
    P('Find its displacement from t = 0 to t = 2.', [('M1', 'integrates: (3t² − 4t)i + t³j'), ('M1', 'substitutes the limits'), ('A1', '4i + 8j m')])),
  X('', P('A stone is projected from the top of a cliff 20 m above the sea, at 30 m s⁻¹ at 30° above the horizontal. Find the horizontal distance from the foot of the cliff to where it lands.', [('M1', '−20 = 15t − 4.9t²'), ('M1', 'solves the quadratic and takes the positive root'), ('A1', 't = 4.065'), ('A1', '106 m')], ans=30 * math.cos(math.radians(30)) * t5, unit='m', tol=3e-3))])

assert len(DEEP) - N0 == 12
for k_, dd in DEEP.items():
    assert len(dd['examples']) >= 2 and len(dd['fills']) >= 3 and len(dd['exam']) >= 3 and len(dd['tip']) > 120, k_
    for q in dd['exam']:
        for p in q['parts']: assert p['m'] == len(p['ms']), (k_, p['q'])
