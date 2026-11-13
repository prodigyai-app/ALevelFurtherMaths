"""Decision 1 and Decision 2 depth content (original, Edexcel 9FM0 style).
Every result is recomputed by running the algorithm itself (packing, Kruskal, Dijkstra, critical path,
linear programming, transportation, Hungarian, maximum flow, dynamic programming, games)."""
import math, itertools
import numpy as np
import networkx as nx
from scipy.optimize import linprog, linear_sum_assignment
from deep_core import DEEP, deep, E, F, P, X, close

N0 = len(DEEP)

def pack(items, cap, decreasing=False):
    bins = []
    for it in (sorted(items, reverse=True) if decreasing else items):
        for b in bins:
            if sum(b) + it <= cap: b.append(it); break
        else: bins.append([it])
    return bins
def bubble_pass(a, desc=False):
    a = list(a)
    for i in range(len(a) - 1):
        if (a[i] < a[i + 1]) if desc else (a[i] > a[i + 1]): a[i], a[i + 1] = a[i + 1], a[i]
    return a
def bsearch(lst, t):
    lo, hi, seen = 1, len(lst), []
    while lo <= hi:
        m = math.ceil((lo + hi) / 2); seen.append(lst[m - 1])
        if lst[m - 1] == t: return m, seen
        lo, hi = (m + 1, hi) if t > lst[m - 1] else (lo, m - 1)
    return None, seen
def cpa(acts):
    es, ef = {}, {}
    for a, (d, pre) in acts.items():
        es[a] = max((ef[p] for p in pre), default=0); ef[a] = es[a] + d
    end = max(ef.values()); lf, ls = {}, {}
    for a in reversed(list(acts)):
        succ = [b for b, (_, pre) in acts.items() if a in pre]
        lf[a] = min((ls[b] for b in succ), default=end); ls[a] = lf[a] - acts[a][0]
    return end, es, lf, {a: lf[a] - es[a] - acts[a][0] for a in acts}
def nwc(s, d):
    s, d = list(s), list(d); A = np.zeros((len(s), len(d))); i = j = 0
    while i < len(s) and j < len(d):
        q = min(s[i], d[j]); A[i, j] = q; s[i] -= q; d[j] -= q
        if s[i] == 0: i += 1
        else: j += 1
    return A
def topt(S, D, C):
    m, n = C.shape
    return linprog(C.flatten(), A_eq=np.vstack([np.kron(np.eye(m), np.ones(n)), np.kron(np.ones(m), np.eye(n))]), b_eq=S + D).fun
def game(M):
    M = np.array(M, float); k = 1 - M.min(); M2 = M + k
    r = linprog(np.ones(M.shape[0]), A_ub=-M2.T, b_ub=-np.ones(M.shape[1])); v = 1 / r.x.sum()
    return r.x * v, v - k

# ------------------------------------------------------------------ d1-algorithms
assert bubble_pass([7, 3, 9, 4, 6]) == [3, 7, 4, 6, 9] and bubble_pass([3, 7, 4, 6, 9]) == [3, 4, 6, 7, 9]
assert pack([5, 7, 3, 4, 6, 2, 3], 10) == [[5, 3, 2], [7, 3], [4, 6]] and pack([5, 7, 3, 4, 6, 2, 3], 10, True) == [[7, 3], [6, 4], [5, 3, 2]]
assert bsearch([4, 9, 15, 21, 28, 33, 37, 42, 50], 37) == (7, [28, 42, 37])
Q1 = [8, 4, 7, 3, 6, 5, 2, 5]; assert math.ceil(sum(Q1) / 12) == 4 and pack(Q1, 12, True) == [[8, 4], [7, 5], [6, 5], [3, 2]]
assert bubble_pass([12, 18, 7, 25, 14], True) == [18, 12, 25, 14, 7]
assert bsearch([12, 19, 25, 33, 40, 47, 56, 61, 68, 75], 61) == (8, [47, 68, 61])
assert math.ceil(47 / 10) == 5 and math.ceil((1 + 15) / 2) == 8
deep('d1-algorithms',
 'Carry out an algorithm exactly as stated and record each pass or comparison, because the marks are for the working as well as the result. For bin packing, find the lower bound (total ÷ capacity, rounded up) first, so you can tell whether a packing is optimal; for a binary search, use the middle position rounded up, and halve the list each time.',
 [E('A bubble sort', 'Use a bubble sort to arrange 7, 3, 9, 4, 6 in ascending order, showing the result of each pass.', 'Pass 1: swap 7 and 3; keep 7, 9; swap 9 and 4; swap 9 and 6. Result 3, 7, 4, 6, 9.', 'Pass 2: swap 7 and 4; swap 7 and 6. Result 3, 4, 6, 7, 9.', 'Pass 3: no swaps, so the algorithm stops.', 'Sorted list: 3, 4, 6, 7, 9.'),
  E('First-fit and first-fit decreasing', 'Pack items 5, 7, 3, 4, 6, 2, 3 into bins of capacity 10 using first-fit and first-fit decreasing.', 'Lower bound = 30 ÷ 10 = 3 bins.', 'First-fit: [5, 3, 2], [7, 3], [4, 6].', 'First-fit decreasing on 7, 6, 5, 4, 3, 3, 2: [7, 3], [6, 4], [5, 3, 2].', 'Both use 3 bins, equal to the lower bound, so both packings are optimal.'),
  E('A binary search', 'Use a binary search to locate 37 in the list 4, 9, 15, 21, 28, 33, 37, 42, 50.', 'Middle of positions 1–9 is 5: 28. 37 > 28, so keep positions 6–9.', 'Middle of 6–9 is 7.5, rounded up to 8: 42. 37 < 42, so keep 6–7.', 'Middle of 6–7 is 6.5, rounded up to 7: 37.', '37 is found at position 7 after 3 iterations.')],
 [F('Items with total 47 and bins of capacity 10.', 'lower bound = [[5]] bins'),
  F('A bubble sort of 6 items.', 'the greatest number of passes needed = [[5]]'),
  F('A binary search of 15 items.', 'the first middle position = [[8]]')],
 [X('<p>Items of sizes 8, 4, 7, 3, 6, 5, 2, 5 are to be packed into bins of capacity 12.</p>',
    P('Find a lower bound for the number of bins.', [('M1', '40 ÷ 12 = 3.33…'), ('A1', '4')], ans=4),
    P('Use the first-fit decreasing algorithm to pack the items.', [('M1', 'sorts into decreasing order: 8, 7, 6, 5, 5, 4, 3, 2'), ('M1', 'places each item in the first bin with room'), ('A1', '[8, 4], [7, 5], [6, 5], [3, 2]')]),
    P('Explain whether your packing is optimal.', [('B1', 'it uses 4 bins, equal to the lower bound, so it is optimal')])),
  X('<p>The list 12, 18, 7, 25, 14 is to be sorted into descending order using a bubble sort.</p>',
    P('Write down the list after the first pass.', [('M1', 'compares adjacent pairs from the left'), ('A1', '18, 12, 25, 14, 7')]),
    P('Complete the sort, stating the result of each further pass.', [('A1', 'pass 2: 18, 25, 14, 12, 7'), ('A1', 'pass 3: 25, 18, 14, 12, 7; pass 4 makes no swaps')])),
  X('', P('Use a binary search to locate 61 in the list 12, 19, 25, 33, 40, 47, 56, 61, 68, 75.', [('M1', 'first middle: position 6, value 47'), ('M1', 'then position 9, value 68'), ('A1', 'then position 8: 61 found')]))])
assert bubble_pass([18, 12, 25, 14, 7], True) == [18, 25, 14, 12, 7] and bubble_pass([18, 25, 14, 12, 7], True) == [25, 18, 14, 12, 7]

# ------------------------------------------------------------------ d1-graph
G1 = nx.Graph(); G1.add_weighted_edges_from([('A', 'B', 4), ('A', 'C', 2), ('B', 'C', 1), ('B', 'D', 5), ('C', 'D', 8), ('C', 'E', 10), ('D', 'E', 2)])
assert nx.dijkstra_path(G1, 'A', 'E') == ['A', 'C', 'B', 'D', 'E'] and nx.dijkstra_path_length(G1, 'A', 'E') == 10
assert nx.minimum_spanning_tree(G1).size(weight='weight') == 10 and set(map(frozenset, nx.minimum_spanning_tree(G1).edges())) == {frozenset(e) for e in [('A', 'C'), ('B', 'C'), ('B', 'D'), ('D', 'E')]}
G2 = nx.Graph(); G2.add_weighted_edges_from([('A', 'B', 7), ('A', 'C', 3), ('B', 'C', 2), ('B', 'D', 4), ('C', 'D', 8), ('C', 'E', 6), ('D', 'E', 3), ('D', 'F', 5), ('E', 'F', 4)])
assert nx.minimum_spanning_tree(G2).size(weight='weight') == 16 and nx.dijkstra_path(G2, 'A', 'F') == ['A', 'C', 'E', 'F'] and nx.dijkstra_path_length(G2, 'A', 'F') == 13
Mx = [[0, 6, 9, 4], [6, 0, 5, 7], [9, 5, 0, 3], [4, 7, 3, 0]]
H = nx.Graph(); [H.add_edge('PQRS'[i], 'PQRS'[j], weight=Mx[i][j]) for i in range(4) for j in range(i + 1, 4)]; assert nx.minimum_spanning_tree(H).size(weight='weight') == 12
deep('d1-graph',
 'For a minimum spanning tree, Kruskal adds the cheapest edge that does not make a cycle, while Prim grows one tree from a start vertex (and works directly on a distance matrix). Dijkstra finds shortest paths from one vertex: record order of labelling, final labels and working values, then trace the route back from the destination.',
 [E('Dijkstra’s algorithm', 'In the network AB = 4, AC = 2, BC = 1, BD = 5, CD = 8, CE = 10, DE = 2, find the shortest route from A to E.', 'Label A 0, then C 2 (from A), then B 3 (via C, better than 4).', 'D: from B 3 + 5 = 8, better than 2 + 8 = 10.', 'E: from D 8 + 2 = 10, better than 2 + 10 = 12.', 'Shortest route A–C–B–D–E, length 10.'),
  E('Prim’s algorithm', 'Use Prim’s algorithm, starting at A, to find a minimum spanning tree of the same network.', 'Start at A: add AC (2).', 'Add CB (1), the cheapest edge leaving {A, C}.', 'Add BD (5), then DE (2).', 'Edges AC, CB, BD, DE; total weight 10.'),
  E('Kruskal’s algorithm', 'Use Kruskal’s algorithm on the same network.', 'In order: BC 1, AC 2, DE 2, AB 4, BD 5, …', 'Accept BC, AC and DE.', 'Reject AB (it would make the cycle A–B–C).', 'Accept BD; four edges join five vertices, so stop: total 10.')],
 [F('A spanning tree on 8 vertices.', 'number of edges = [[7]]'),
  F('The minimum spanning tree in the worked examples.', 'total weight = [[10]]'),
  F('Dijkstra in the worked examples.', 'final label of E = [[10]]')],
 [X('<p>A network has edges AB 7, AC 3, BC 2, BD 4, CD 8, CE 6, DE 3, DF 5 and EF 4.</p>',
    P('Use Kruskal’s algorithm to find a minimum spanning tree, stating the order in which you add edges.', [('M1', 'considers edges in order of weight'), ('M1', 'rejects edges that form a cycle'), ('A1', 'BC, AC, DE, BD, EF; total 16')]),
    P('Use Dijkstra’s algorithm to find the shortest route from A to F.', [('M1', 'correct labelling order'), ('M1', 'updates working values'), ('A1', 'route A–C–E–F'), ('A1', 'length 13')])),
  X('<p>The distances between four towns P, Q, R and S are: PQ 6, PR 9, PS 4, QR 5, QS 7, RS 3.</p>',
    P('Use Prim’s algorithm, starting at P, to find a minimum spanning tree and its total length.', [('M1', 'starts at P and adds PS'), ('M1', 'then SR, then RQ'), ('A1', 'total length 12')], ans=12)),
  X('', P('Explain why a minimum spanning tree does not always contain the shortest route between two given vertices.', [('B1', 'the tree minimises the total weight of all edges, not the length of any particular route'), ('B1', 'for example, a direct edge AB of 4 may be left out when AC + CB = 3 is cheaper overall, so the tree route from A to B may be longer than another route')]))])

# ------------------------------------------------------------------ d1-route
assert min(5 + 8, 6 + 9, 7 + 4) == 11 and 85 + 11 == 96 and 85 + 4 == 89
D5 = {('A', 'B'): 8, ('A', 'C'): 5, ('A', 'D'): 9, ('A', 'E'): 7, ('B', 'C'): 6, ('B', 'D'): 4, ('B', 'E'): 10, ('C', 'D'): 7, ('C', 'E'): 3, ('D', 'E'): 6}
d5 = lambda a, b: D5.get((a, b), D5.get((b, a)))
assert min(sum(d5(t[i], t[(i + 1) % 5]) for i in range(5)) for t in itertools.permutations('ABCDE') if t[0] == 'A') == 26
assert d5('A', 'C') + d5('C', 'E') + d5('E', 'D') + d5('D', 'B') + d5('B', 'A') == 26
Hb = nx.Graph(); [Hb.add_edge(a, b, weight=w) for (a, b), w in D5.items() if 'A' not in (a, b)]; assert nx.minimum_spanning_tree(Hb).size(weight='weight') + 5 + 7 == 25
assert min(9 + 11, 7 + 14, 10 + 8) == 18 and 120 + 18 == 138 and 120 + min(8, 14, 11) == 128
V = 'PQRST'; M = [[0, 12, 9, 15, 11], [12, 0, 7, 10, 14], [9, 7, 0, 8, 13], [15, 10, 8, 0, 6], [11, 14, 13, 6, 0]]
cur, vis, L = 0, [0], 0
while len(vis) < 5:
    nxt = min((j for j in range(5) if j not in vis), key=lambda j: M[cur][j]); L += M[cur][nxt]; vis.append(nxt); cur = nxt
L += M[cur][0]; assert ''.join(V[i] for i in vis) == 'PRQST' and L == 43
Hc = nx.Graph(); [Hc.add_edge(V[i], V[j], weight=M[i][j]) for i in range(1, 5) for j in range(i + 1, 5)]; assert nx.minimum_spanning_tree(Hc).size(weight='weight') + 9 + 11 == 41
assert math.comb(6, 2) * math.comb(4, 2) * math.comb(2, 2) // math.factorial(3) == 15
deep('d1-route',
 'For route inspection, list the odd vertices, consider every complete pairing, and add the cheapest pairing to the total edge weight; if the route need not be closed, the start and finish should be odd vertices. For the travelling salesperson problem, an upper bound comes from a tour such as nearest neighbour, and a lower bound from a residual minimum spanning tree plus the two shortest edges at the deleted vertex.',
 [E('Four odd vertices', 'A network has total weight 85 and odd vertices A, B, C, D with shortest distances AB 5, CD 8, AC 6, BD 9, AD 7, BC 4. Find the length of the shortest closed inspection route.', 'Pairings: AB + CD = 13, AC + BD = 15, AD + BC = 11.', 'Repeat the cheapest pairing, AD and BC.', 'Length = 85 + 11 = 96.'),
  E('Different start and finish', 'For the same network, the route may start and finish at different vertices. Find the shortest possible route.', 'Two odd vertices can be the start and the finish, so only one pair needs repeating.', 'Repeat the shortest single path, BC = 4.', 'Start at A and finish at D (or vice versa): length 85 + 4 = 89.'),
  E('Bounds for a travelling salesperson tour', 'Distances: AB 8, AC 5, AD 9, AE 7, BC 6, BD 4, BE 10, CD 7, CE 3, DE 6. Find upper and lower bounds for the shortest tour.', 'Nearest neighbour from A: A–C (5), C–E (3), E–D (6), D–B (4), B–A (8): upper bound 26.', 'Delete A: a minimum spanning tree of B, C, D, E is CE 3, BD 4, BC 6, total 13.', 'Add the two shortest edges from A: 5 + 7. Lower bound 25.', 'So 25 ≤ shortest tour ≤ 26; the tour of length 26 is in fact optimal.')],
 [F('A network with 6 odd vertices.', 'number of complete pairings = [[15]]'),
  F('A network in which every vertex is even.', 'repeated length = [[0]]'),
  F('Lower bound 25 and upper bound 26.', 'the optimal tour is at most [[26]]')],
 [X('<p>A network has total weight 120 and four odd vertices P, Q, R and S. The shortest distances between them are PQ 9, RS 11, PR 7, QS 14, PS 10 and QR 8.</p>',
    P('Find the length of the shortest route that traverses every edge and returns to its start.', [('M1', 'considers all three pairings'), ('A1', '20, 21 and 18'), ('M1', 'adds the least to 120'), ('A1', '138')], ans=138),
    P('The route must start at P but may finish anywhere. Find the length of the shortest route and state where it finishes.', [('M1', 'repeats the shortest path between two of Q, R, S'), ('A1', 'repeats QR (8)'), ('A1', 'length 128, finishing at S')], ans=128)),
  X('<p>The table gives the distances between five towns: PQ 12, PR 9, PS 15, PT 11, QR 7, QS 10, QT 14, RS 8, RT 13, ST 6.</p>',
    P('Use the nearest neighbour algorithm, starting at P, to find an upper bound for the shortest tour.', [('M1', 'P–R–Q–S–T'), ('A1', 'returns to P'), ('A1', '43')], ans=43),
    P('By deleting P, find a lower bound for the length of the tour.', [('M1', 'minimum spanning tree of Q, R, S, T: 21'), ('M1', 'adds the two shortest edges from P: 9 + 11'), ('A1', '41')], ans=41),
    P('What can you conclude?', [('B1', '41 ≤ optimal tour ≤ 43')])),
  X('', P('A network has 6 odd vertices. Explain why 15 different pairings must be considered in the route inspection algorithm.', [('M1', 'the first odd vertex can be paired in 5 ways, then 3, then 1'), ('A1', '5 × 3 × 1 = 15')], ans=15))])

# ------------------------------------------------------------------ d1-critical
acts = {'A': (3, []), 'B': (5, []), 'C': (2, ['A']), 'D': (4, ['A']), 'E': (3, ['B', 'C']), 'F': (2, ['D', 'E'])}
end, es, lf, fl = cpa(acts); assert end == 10 and fl == {'A': 0, 'B': 0, 'C': 0, 'D': 1, 'E': 0, 'F': 0} and math.ceil(19 / 10) == 2
acts2 = {'A': (4, []), 'B': (6, []), 'C': (3, ['A']), 'D': (5, ['A']), 'E': (4, ['B', 'C']), 'F': (2, ['D']), 'G': (3, ['E', 'F'])}
end2, es2, lf2, fl2 = cpa(acts2); assert end2 == 14 and fl2 == {'A': 0, 'B': 1, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0} and es2['E'] == 7 and lf2['B'] == 7
acts3 = dict(acts2); acts3['D'] = (7, ['A']); acts3['B'] = (7, []); assert cpa(acts3)[0] == 16
assert sum(d for d, _ in acts2.values()) == 27 and math.ceil(27 / 14) == 2 and 12 - 4 - 5 == 3 and math.ceil(47 / 20) == 3
deep('d1-critical',
 'Carry out the forward pass for early event times (take the largest incoming value) and the backward pass for late times (take the smallest outgoing value). An activity is critical when its total float, late finish − early start − duration, is zero; a lower bound for the number of workers is the total activity time divided by the project duration, rounded up.',
 [E('Early and late times', 'A (3) and B (5) start the project. C (2) and D (4) follow A. E (3) follows B and C. F (2) follows D and E. Find the duration and the critical activities.', 'Forward pass: C and D start at 3; E starts at max(5, 5) = 5; F starts at max(7, 8) = 8.', 'Duration = 10.', 'Backward pass: F 8–10; E late finish 8; D late finish 8; C late finish 5; B late finish 5; A late finish 3.', 'Floats: D has 1; A, B, C, E and F have 0. Critical paths A–C–E–F and B–E–F.'),
  E('A lower bound for workers', 'For the same project, find a lower bound for the number of workers needed to finish in 10 days.', 'Total activity time = 3 + 5 + 2 + 4 + 3 + 2 = 19.', '19 ÷ 10 = 1.9.', 'At least 2 workers are needed.')],
 [F('LF = 12, ES = 4 and duration 5.', 'total float = [[3]]'),
  F('A critical activity.', 'total float = [[0]]'),
  F('Total activity time 47 hours and duration 20 hours.', 'lower bound = [[3]] workers')],
 [X('<p>A project has activities A (4 days), B (6), C (3, after A), D (5, after A), E (4, after B and C), F (2, after D) and G (3, after E and F).</p>',
    P('Find the early start time of E and the project duration.', [('M1', 'forward pass'), ('A1', 'E starts at 7'), ('A1', 'duration 14 days')]),
    P('Find the late finish time of B and its total float.', [('M1', 'backward pass'), ('A1', 'late finish of B = 7'), ('A1', 'float = 7 − 0 − 6 = 1')]),
    P('List the critical activities.', [('B1', 'A, C, D, E, F and G')]),
    P('Find a lower bound for the number of workers needed to complete the project in 14 days.', [('M1', '27 ÷ 14'), ('A1', '2')], ans=2)),
  X('', P('Explain the purpose of a dummy activity in an activity network.', [('B1', 'it shows a dependency that cannot be shown by the real activities alone'), ('B1', 'or it ensures each activity is uniquely defined by its start and end events')])),
  X('<p>In the project above, activity D is delayed by 2 days and activity B by 1 day.</p>', P('Find the new project duration, explaining your answer.', [('B1', 'D is critical, so a delay of 2 days delays the project by 2 days'), ('B1', 'B had 1 day of float, so its delay has no further effect'), ('A1', '16 days')], ans=16))])

# ------------------------------------------------------------------ d1-lp
verts = [(0, 0), (40, 0), (30, 20), (0, 40)]; assert all(2 * x + 3 * y <= 120 and 2 * x + y <= 80 for x, y in verts) and max(30 * x + 40 * y for x, y in verts) == 1700
r = linprog([-30, -40], A_ub=[[2, 3], [2, 1]], b_ub=[120, 80]); assert np.allclose(r.x, [30, 20])
r = linprog([3, 2], A_ub=[[-1, -1], [-1, -3]], b_ub=[-6, -12]); assert np.allclose(r.x, [0, 6]) and close(r.fun, 12)
assert max((5 * x + 4 * y, x, y) for x in range(10) for y in range(10) if 6 * x + 4 * y <= 24 and x + 2 * y <= 6) == (20, 4, 0)
r = linprog([-5, -4], A_ub=[[6, 4], [1, 2]], b_ub=[24, 6]); assert np.allclose(r.x, [3, 1.5]) and close(-r.fun, 21)
r = linprog([-4, -5], A_ub=[[1, 1], [1, 3], [2, 1]], b_ub=[9, 21, 16]); assert np.allclose(r.x, [3, 6]) and close(-r.fun, 42)
assert [4 * x + 5 * y for x, y in [(0, 0), (8, 0), (7, 2), (3, 6), (0, 7)]] == [0, 32, 38, 42, 35]
r = linprog([2, 3], A_ub=[[-1, -1], [-1, -2], [-3, -1]], b_ub=[-8, -10, -12]); assert np.allclose(r.x, [6, 2]) and close(r.fun, 18)
deep('d1-lp',
 'Define the decision variables with units, write the objective, then every constraint (including non-negativity). Draw the feasible region carefully and test the objective at each vertex, or slide an objective line; if the variables must be integers, check the integer points near the optimal vertex rather than rounding.',
 [E('Formulating and solving', 'A firm makes x units of P and y units of Q. Each P needs 2 hours of machine time and 2 hours of labour; each Q needs 3 hours of machine time and 1 hour of labour. 120 machine hours and 80 labour hours are available. Profits are £30 per P and £40 per Q. Find the best plan.', 'Maximise 30x + 40y subject to 2x + 3y ≤ 120, 2x + y ≤ 80, x, y ≥ 0.', 'Vertices: (0, 0), (40, 0), (30, 20), (0, 40).', 'Profits: 0, 1200, 1700, 1600.', 'Make 30 of P and 20 of Q for a profit of £1700.'),
  E('A minimisation', 'Minimise 3x + 2y subject to x + y ≥ 6, x + 3y ≥ 12, x, y ≥ 0.', 'The feasible region is unbounded, above both lines.', 'Vertices: (12, 0), (3, 3), (0, 6).', 'Costs: 36, 15, 12.', 'Minimum 12 at (0, 6).'),
  E('An integer solution', 'Maximise 5x + 4y subject to 6x + 4y ≤ 24, x + 2y ≤ 6, with x and y non-negative integers.', 'The continuous optimum is at (3, 1.5), with value 21.', 'Test nearby integer points: (3, 1) gives 19, (2, 2) gives 18, (4, 0) gives 20.', '(4, 0) is feasible: 24 ≤ 24 and 4 ≤ 6.', 'The integer optimum is x = 4, y = 0, value 20.')],
 [F('At (30, 20).', 'profit 30x + 40y = [[1700]]'),
  F('The line x + y = 10.', 'meets the y-axis at (0, [[10]])'),
  F('Two ≤ constraints in a simplex tableau.', 'number of slack variables = [[2]]')],
 [X('<p>Maximise P = 4x + 5y subject to x + y ≤ 9, x + 3y ≤ 21, 2x + y ≤ 16, x ≥ 0, y ≥ 0.</p>',
    P('Find the coordinates of the vertices of the feasible region.', [('M1', 'solves pairs of boundary equations'), ('A1', '(8, 0) and (7, 2)'), ('A1', '(3, 6), (0, 7) and (0, 0)')]),
    P('Find the optimal solution and the maximum value of P.', [('M1', 'evaluates P at each vertex'), ('A1', 'x = 3, y = 6'), ('A1', 'P = 42')], ans=42)),
  X('', P('Minimise C = 2x + 3y subject to x + y ≥ 8, x + 2y ≥ 10, 3x + y ≥ 12, x ≥ 0, y ≥ 0.', [('M1', 'identifies the unbounded feasible region'), ('M1', 'vertices (0, 12), (2, 6), (6, 2), (10, 0)'), ('A1', 'evaluates C: 36, 22, 18, 20'), ('A1', 'minimum 18 at (6, 2)')], ans=18)),
  X('', P('Explain why rounding the optimal vertex of a linear programme may not give the optimal integer solution.', [('B1', 'the rounded point may lie outside the feasible region'), ('B1', 'or another integer point may give a better value of the objective')]))])
assert [2 * x + 3 * y for x, y in [(0, 12), (2, 6), (6, 2), (10, 0)]] == [36, 22, 18, 20]

# ------------------------------------------------------------------ d1-simplex
r = linprog([-2, -3], A_ub=[[1, 2], [3, 2]], b_ub=[8, 12]); assert np.allclose(r.x, [2, 3]) and close(-r.fun, 13)
r = linprog([-5, -4], A_ub=[[2, 1], [1, 2]], b_ub=[10, 8]); assert np.allclose(r.x, [4, 2]) and close(-r.fun, 28)
assert 8 / 2 == 4 and 12 / 2 == 6 and 5 / 0.5 == 10 and 3 / 1.5 == 2 and 2 * 2 + 2 * 3 == 10 and 2 + 6 == 8
deep('d1-simplex',
 'Choose the pivot column with the most negative entry in the objective row, then the pivot row by the smallest non-negative ratio of value to pivot-column entry. Divide the pivot row by the pivot, clear the rest of the column, and stop when the objective row has no negative entries; read basic variables from the columns that are unit vectors.',
 [E('Two iterations to the optimum', 'Use the simplex algorithm to maximise P = 2x + 3y subject to x + 2y ≤ 8 and 3x + 2y ≤ 12.', 'Initial tableau with slacks s and t; P row (−2, −3, 0, 0 | 0). Pivot on the y column: ratios 8/2 = 4 and 12/2 = 6, so row 1.', 'After pivoting: y = 4 − ½x − ½s, and the P row becomes (−½, 0, 3/2, 0 | 12).', 'Pivot on the x column: ratios 4/½ = 8 and 4/2 = 2, so row 2.', 'Optimal: x = 2, y = 3, P = 13, with both slacks zero.'),
  E('A ≥ constraint', 'Explain how the constraint x + y ≥ 3 is handled in the two-stage simplex method.', 'Subtract a surplus variable: x + y − s = 3.', 'The origin then gives s = −3, which is not allowed, so add an artificial variable a: x + y − s + a = 3.', 'Stage 1 minimises the sum of the artificial variables.', 'If that minimum is 0 a feasible starting point has been found; if it is positive, the problem has no feasible solution.')],
 [F('Ratios 8/2 and 12/2.', 'pivot row value = [[4]]'),
  F('The final tableau of the first worked example.', 'P = [[13]]'),
  F('At (2, 3) for x + 2y ≤ 8.', 'slack = [[0]]')],
 [X('<p>Maximise P = 5x + 4y subject to 2x + y ≤ 10, x + 2y ≤ 8, x ≥ 0, y ≥ 0.</p>',
    P('Write down the initial simplex tableau.', [('B1', 'slack variables in both constraint rows'), ('B1', 'objective row P − 5x − 4y = 0')]),
    P('Identify the first pivot, explaining your choice.', [('B1', 'x column: most negative entry −5'), ('B1', 'ratios 10/2 = 5 and 8/1 = 8, so row 1')]),
    P('Complete the algorithm and state the optimal values of x, y and P.', [('M1', 'correct first iteration: P = 25'), ('M1', 'second pivot in the y column, row 2'), ('A1', 'x = 4, y = 2'), ('A1', 'P = 28')], ans=28)),
  X('', P('In stage 1 of the two-stage simplex method, the minimum value of the sum of the artificial variables is 3. State what this shows.', [('B1', 'the original problem has no feasible solution')])),
  X('<p>The final tableau for maximising P = 5x + 4y, subject to 2x + y ≤ 10 and x + 2y ≤ 8, gives x = 4, y = 2 with both slack variables non-basic.</p>', P('State the values of the slack variables and interpret them.', [('B1', 'both slack variables are 0'), ('B1', 'both resources are fully used at the optimum')]))])

# ------------------------------------------------------------------ d2-transport
S, Dm, C = [30, 40, 30], [20, 45, 35], np.array([[8, 6, 10], [9, 12, 13], [14, 9, 16]])
A = nwc(S, Dm); assert np.array_equal(A, [[20, 10, 0], [0, 35, 5], [0, 0, 30]]) and (A * C).sum() == 1185
Rr = {'A': 0}; K = {'X': 8, 'Y': 6}; Rr['B'] = 12 - 6; K['Z'] = 13 - Rr['B']; Rr['C'] = 16 - K['Z']
assert (Rr['B'], K['Z'], Rr['C']) == (6, 7, 9)
idx = {'AZ': 10 - 0 - 7, 'BX': 9 - 6 - 8, 'CX': 14 - 9 - 8, 'CY': 9 - 9 - 6}; assert idx == {'AZ': 3, 'BX': -5, 'CX': -3, 'CY': -6}
B2 = A.copy(); B2[2, 1] += 30; B2[1, 1] -= 30; B2[1, 2] += 30; B2[2, 2] -= 30; assert (B2 * C).sum() == 1005 and topt(S, Dm, C) == 950
S2, D2, C2 = [35, 25], [20, 25, 15], np.array([[5, 3, 6], [4, 7, 2]]); A2 = nwc(S2, D2); assert np.array_equal(A2, [[20, 15, 0], [0, 10, 15]]) and (A2 * C2).sum() == 245
# shadow costs R1 = 0: K1 = 5, K2 = 3, R2 = 4, K3 = −2; indices: R1C3 = 6 − 0 + 2 = 8, R2C1 = 4 − 4 − 5 = −5
B3 = A2.copy(); B3[1, 0] += 10; B3[1, 1] -= 10; B3[0, 1] += 10; B3[0, 0] -= 10; assert (B3 * C2).sum() == 195 and topt(S2, D2, C2) == 195
assert 3 + 3 - 1 == 5 and 2 + 3 - 1 == 4 and (6 - 0 - 3, 7 + 1 - 3) == (3, 5) and 4 - 5 == -1 and 2 + 1 == 3
deep('d2-transport',
 'Balance supply and demand first (add a dummy with zero costs if necessary), then check the initial solution has m + n − 1 occupied cells. Find shadow costs from the occupied cells (Rᵢ + Kⱼ = cost), compute improvement indices for the empty cells, and enter the most negative one using a stepping-stone loop of alternating + and − cells.',
 [E('A north-west corner solution', 'Supplies A 30, B 40, C 30; demands X 20, Y 45, Z 35; costs A: 8, 6, 10; B: 9, 12, 13; C: 14, 9, 16. Find the north-west corner solution and its cost.', 'A: X 20, Y 10. B: Y 35, Z 5. C: Z 30.', 'Five occupied cells = 3 + 3 − 1, so the solution is not degenerate.', 'Cost = 160 + 60 + 420 + 65 + 480.', '£1185.'),
  E('Improvement indices and one iteration', 'Improve the solution in the previous example.', 'Shadow costs: R_A = 0, K_X = 8, K_Y = 6, R_B = 6, K_Z = 7, R_C = 9.', 'Indices: AZ 3, BX −5, CX −3, CY −6; enter CY.', 'Loop CY+, BY−, BZ+, CZ−: θ = min(35, 30) = 30.', 'New solution: A X 20, Y 10; B Y 5, Z 35; C Y 30. Cost £1005 (recalculate the indices to test for optimality).')],
 [F('3 sources and 4 destinations.', 'occupied cells needed = [[6]]'),
  F('Occupied cell with cost 12 and R = 6.', 'K = [[6]]'),
  F('Empty cell cost 9, R = 9, K = 6.', 'improvement index = [[-6]]')],
 [X('<p>Supplies: S₁ 35, S₂ 25. Demands: D₁ 20, D₂ 25, D₃ 15. Costs: S₁: 5, 3, 6; S₂: 4, 7, 2.</p>',
    P('Find the north-west corner solution and its cost.', [('M1', 'allocates from the top-left'), ('A1', 'S₁: 20, 15; S₂: 10, 15'), ('A1', 'cost 245')], ans=245),
    P('Calculate shadow costs and improvement indices for the unused cells.', [('M1', 'R₁ = 0, K₁ = 5, K₂ = 3, R₂ = 4, K₃ = −2'), ('A1', 'S₁D₃: 8'), ('A1', 'S₂D₁: −5')]),
    P('Use the stepping-stone method to obtain an improved solution and its cost.', [('M1', 'loop S₂D₁+, S₂D₂−, S₁D₂+, S₁D₁−'), ('A1', 'θ = 10'), ('A1', 'S₁: 10, 25, 0; S₂: 10, 0, 15; cost 195')], ans=195)),
  X('', P('Explain what is meant by a degenerate solution of a transportation problem and how it is dealt with.', [('B1', 'fewer than m + n − 1 cells are occupied'), ('B1', 'place a zero in a suitable empty cell so that shadow costs can be found')])),
  X('<p>The improved solution from question 1 is S₁: 10, 25, 0; S₂: 10, 0, 15.</p>', P('Show that this solution is optimal.', [('M1', 'shadow costs R₁ = 0, K₁ = 5, K₂ = 3, R₂ = −1, K₃ = 3'), ('M1', 'improvement indices S₁D₃ = 3 and S₂D₂ = 5'), ('A1', 'no negative indices, so the solution is optimal')]))])

# ------------------------------------------------------------------ d2-assignment
M1 = np.array([[10, 7, 8], [6, 9, 5], [8, 7, 8]]); r, c = linear_sum_assignment(M1); assert M1[r, c].sum() == 20 and list(c) == [1, 2, 0]
assert sorted(sum(M1[i, p[i]] for i in range(3)) for p in itertools.permutations(range(3)))[:2] == [20, 21]
Mm = np.array([[40, 35, 50], [30, 45, 40], [45, 40, 35]]); r, c = linear_sum_assignment(Mm, maximize=True); assert Mm[r, c].sum() == 140 and list(c) == [2, 1, 0]
M4 = np.array([[12, 9, 14, 10], [8, 11, 10, 13], [15, 12, 9, 11], [10, 14, 12, 9]]); r, c = linear_sum_assignment(M4); assert M4[r, c].sum() == 35 and list(c) == [1, 0, 2, 3]
assert sorted(sum(M4[i, p[i]] for i in range(4)) for p in itertools.permutations(range(4)))[:2] == [35, 40]
Md = np.array([[7, 5, 8], [6, 9, 4], [0, 0, 0]]); r, c = linear_sum_assignment(Md); assert Md[r, c].sum() == 9
deep('d2-assignment',
 'Make the matrix square with a dummy row or column of zeros, and for a maximisation subtract every entry from the largest. Reduce rows then columns, cover the zeros with the fewest lines, and if fewer than n lines are needed adjust by the smallest uncovered value (subtract it from uncovered entries and add it where lines cross) before trying again.',
 [E('The Hungarian algorithm', 'Find the minimum cost allocation for the cost matrix A: 10, 7, 8; B: 6, 9, 5; C: 8, 7, 8.', 'Row reduction: A: 3, 0, 1; B: 1, 4, 0; C: 1, 0, 1.', 'Column reduction (column 1 minimum 1): A: 2, 0, 1; B: 0, 4, 0; C: 0, 0, 1.', 'Covering the zeros needs 3 lines (column 1, column 2, row B), so an allocation is possible.', 'A–2, B–3, C–1: cost 7 + 5 + 8 = 20.'),
  E('A maximisation', 'Maximise the total score for A: 40, 35, 50; B: 30, 45, 40; C: 45, 40, 35.', 'Subtract every entry from 50: A: 10, 15, 0; B: 20, 5, 10; C: 5, 10, 15.', 'Apply the Hungarian algorithm to minimise.', 'A–3, B–2, C–1.', 'Maximum total = 50 + 45 + 45 = 140.'),
  E('A dummy row', 'Two workers are to do two of three jobs. Costs: W₁: 7, 5, 8; W₂: 6, 9, 4. Find the minimum cost.', 'Add a dummy worker with costs 0, 0, 0 to make the matrix square.', 'The Hungarian algorithm gives W₁–job 2, W₂–job 3, dummy–job 1.', 'Minimum cost 5 + 4 = 9; job 1 is not done.')],
 [F('A 3 × 4 cost matrix.', 'add [[1]] dummy row'),
  F('A row 7, 9, 5 reduced.', 'row becomes 2, 4, [[0]]'),
  F('A maximisation with largest entry 50 and an entry 35.', 'transformed entry = [[15]]')],
 [X('<p>Four workers A, B, C, D are to be assigned to tasks 1, 2, 3, 4. Costs: A: 12, 9, 14, 10; B: 8, 11, 10, 13; C: 15, 12, 9, 11; D: 10, 14, 12, 9.</p>',
    P('Reduce the rows and then the columns of the cost matrix.', [('M1', 'subtracts the row minima 9, 8, 9, 9'), ('A1', 'correct reduced matrix after the column step')]),
    P('Use the Hungarian algorithm to find the minimum cost allocation.', [('M1', 'covers the zeros with the minimum number of lines'), ('M1', 'adjusts the matrix if fewer than 4 lines are needed'), ('A1', 'A–2, B–1, C–3, D–4'), ('A1', 'minimum cost 35')], ans=35)),
  X('', P('Explain how the Hungarian algorithm is adapted when the problem is to maximise a total profit.', [('B1', 'subtract every entry from the largest entry (or multiply by −1)'), ('B1', 'then minimise the transformed matrix as usual')])),
  X('', P('Formulate the assignment of 3 workers to 3 tasks with costs cᵢⱼ as a linear programming problem.', [('B1', 'xᵢⱼ = 1 if worker i does task j, otherwise 0; minimise Σcᵢⱼxᵢⱼ'), ('B1', 'Σⱼ xᵢⱼ = 1 for each worker'), ('B1', 'Σᵢ xᵢⱼ = 1 for each task')]))])

# ------------------------------------------------------------------ d2-flow
def mf(edges):
    G = nx.DiGraph(); [G.add_edge(u, v, capacity=c) for u, v, c in edges]
    val, _ = nx.maximum_flow(G, 'S', 'T'); cut, (Sset, Tset) = nx.minimum_cut(G, 'S', 'T'); return val, cut, Sset
e1 = [('S', 'A', 10), ('S', 'B', 8), ('A', 'B', 3), ('A', 'C', 6), ('B', 'D', 9), ('C', 'T', 7), ('D', 'T', 8), ('C', 'D', 4)]
v1, c1, s1 = mf(e1); assert v1 == 14 and c1 == 14 and s1 == {'S', 'A', 'B', 'D'}
e2 = [('S', 'A', 12), ('S', 'B', 9), ('A', 'C', 7), ('A', 'D', 6), ('B', 'D', 8), ('C', 'T', 10), ('D', 'T', 11), ('B', 'C', 3)]
v2, c2, s2 = mf(e2); assert v2 == 21 and s2 == {'S', 'A', 'B', 'C', 'D'}
e3 = [('S', 'S1', 15), ('S', 'S2', 10), ('S1', 'A', 9), ('S1', 'B', 8), ('S2', 'B', 7), ('A', 'T', 12), ('B', 'T', 11)]
v3, _, _ = mf(e3); assert v3 == 20
deep('d2-flow',
 'A flow must satisfy capacities on every arc and conservation at every intermediate vertex. Find flow-augmenting routes until none remain, then prove maximality with a cut: by the max-flow min-cut theorem, a flow equal to the capacity of a cut is maximal. Count only arcs directed from the source side to the sink side when finding a cut’s capacity.',
 [E('Augmenting and a cut', 'Arcs: SA 10, SB 8, AB 3, AC 6, BD 9, CT 7, DT 8, CD 4. Find the maximum flow from S to T.', 'Augment S–A–C–T by 6 and S–B–D–T by 8: flow 14.', 'Any further route must use CT or DT, but DT is full and C can only receive 6.', 'The cut separating {S, A, B, D} from {C, T} has capacity AC + DT = 6 + 8 = 14.', 'Flow 14 = cut 14, so the maximum flow is 14.'),
  E('Several sources', 'Sources S₁ (supply 15) and S₂ (supply 10) feed A and B: S₁A 9, S₁B 8, S₂B 7, AT 12, BT 11. Find the maximum flow.', 'Add a supersource S with arcs SS₁ 15 and SS₂ 10.', 'Through A at most 9 (only S₁ feeds it); through B at most min(11, 8 + 7) = 11.', 'Maximum flow 9 + 11 = 20; the cut through S₁A and BT has capacity 9 + 11 = 20, confirming it.')],
 [F('Arcs from the source side: 6 and 8.', 'cut capacity = [[14]]'),
  F('A flow of 12 and a cut of capacity 12.', 'the maximum flow is [[12]]'),
  F('An arc of capacity 9 carrying 5.', 'spare capacity = [[4]]')],
 [X('<p>Arcs and capacities: SA 12, SB 9, AC 7, AD 6, BD 8, BC 3, CT 10, DT 11.</p>',
    P('Find a flow of value 21.', [('M1', 'routes using SA and SB'), ('A1', 'for example SA 12 (AC 7, AD 5), SB 9 (BC 3, BD 6), CT 10, DT 11')]),
    P('Use a cut to prove that this flow is maximal.', [('M1', 'cut {CT, DT}'), ('A1', 'capacity 21 = flow, so maximal by the max-flow min-cut theorem')]),
    P('The capacity of CT is increased to 12. Explain whether the maximum flow increases.', [('B1', 'the cut {SA, SB} has capacity 21, so the maximum flow is still 21')])),
  X('', P('Explain how a network with two sinks and a vertex of limited capacity can be modelled so that the maximum flow algorithm applies.', [('B1', 'add a supersink joined from each sink by an arc of sufficient capacity'), ('B1', 'replace the vertex by two vertices joined by an arc with the vertex capacity')])),
  X('', P('A cut has capacity 18 and a feasible flow has value 15. What can be concluded about the maximum flow?', [('B1', '15 ≤ maximum flow ≤ 18')]))])
assert mf([('S', 'A', 12), ('S', 'B', 9), ('A', 'C', 7), ('A', 'D', 6), ('B', 'D', 8), ('C', 'T', 12), ('D', 'T', 11), ('B', 'C', 3)])[0] == 21

# ------------------------------------------------------------------ d2-dynamic
Ed = {('S', 'A'): 5, ('S', 'B'): 3, ('S', 'C'): 6, ('A', 'D'): 4, ('A', 'E'): 7, ('B', 'D'): 6, ('B', 'E'): 5, ('C', 'E'): 3, ('C', 'F'): 6, ('D', 'T'): 8, ('E', 'T'): 6, ('F', 'T'): 3}
Gd = nx.DiGraph(); [Gd.add_edge(u, v, weight=w) for (u, v), w in Ed.items()]
paths = list(nx.all_simple_paths(Gd, 'S', 'T')); cost = lambda p: sum(Ed[(p[i], p[i + 1])] for i in range(len(p) - 1))
assert sorted(cost(p) for p in paths)[:2] == [14, 15] and min(paths, key=cost) == ['S', 'B', 'E', 'T']
mm = lambda p: min(Ed[(p[i], p[i + 1])] for i in range(len(p) - 1)); assert sorted((mm(p) for p in paths), reverse=True)[:2] == [5, 4] and max(paths, key=mm) == ['S', 'A', 'E', 'T']
# allocation problem: 4 units between three projects, returns table
ret = {'P': [0, 5, 11, 12, 14], 'Q': [0, 6, 10, 12, 13], 'R': [0, 3, 8, 11, 15]}
bq = [max(ret['Q'][b] + ret['R'][k - b] for b in range(k + 1)) for k in range(5)]; assert bq == [0, 6, 10, 14, 18]
tot = [ret['P'][a] + bq[4 - a] for a in range(5)]; assert tot == [18, 19, 21, 18, 14]
allr = sorted((ret['P'][a] + ret['Q'][b] + ret['R'][4 - a - b], a, b) for a in range(5) for b in range(5 - a)); assert allr[-1] == (21, 2, 2) and allr[-2][0] == 20
prod = {1: 4, 2: 7, 3: 9, 4: 12, 5: 16}; plans = [prod[m1] + (m1 - 3) + prod[6 - m1] for m1 in (3, 4, 5)]; assert plans == [18, 20, 22]
deep('d2-dynamic',
 'Work backwards from the final stage, recording at each state the best value so far and the action that achieves it. The objective may be a minimum total, a maximum total, a minimax (smallest largest stage value) or a maximin (largest smallest stage value), so state which before starting; then trace the optimal decisions forwards from the start.',
 [E('A minimum-cost route', 'Stages: S to A 5, B 3, C 6; A to D 4, E 7; B to D 6, E 5; C to E 3, F 6; D to T 8, E to T 6, F to T 3. Find the cheapest route.', 'Stage 1 (to T): D 8, E 6, F 3.', 'Stage 2: A min(4 + 8, 7 + 6) = 12; B min(6 + 8, 5 + 6) = 11; C min(3 + 6, 6 + 3) = 9.', 'Stage 3: S min(5 + 12, 3 + 11, 6 + 9) = 14.', 'Route S–B–E–T, cost 14.'),
  E('A maximin route', 'For the same network, find the route whose smallest arc value is as large as possible.', 'Stage 1: D 8, E 6, F 3.', 'Stage 2: A max(min(4, 8), min(7, 6)) = 6; B max(min(6, 8), min(5, 6)) = 6; C max(min(3, 6), min(6, 3)) = 3.', 'Stage 3: S max(min(5, 6), min(3, 6), min(6, 3)) = 5.', 'Route S–A–E–T, maximin value 5.'),
  E('Allocating resources', 'Four units of resource are shared between projects P, Q and R. Returns for 0–4 units: P 0, 5, 11, 12, 14; Q 0, 6, 10, 12, 13; R 0, 3, 8, 11, 15. Maximise the total return.', 'Stage Q + R: best return for k units is 0, 6, 10, 14, 18 for k = 0 to 4 (for example k = 3: max(0 + 11, 6 + 8, 10 + 3, 12 + 0) = 14).', 'Stage P: P(a) + best(4 − a) for a = 0 to 4 gives 18, 19, 21, 18, 14.', 'The maximum is 21 with 2 units to P, leaving 2 units, best used as 2 to Q and 0 to R.', 'Allocation P 2, Q 2, R 0: return 11 + 10 + 0 = 21.')],
 [F('Minimum stage values from D, E, F to T: 8, 6, 3.', 'value at C via E (3) = [[9]]'),
  F('Maximin at a state with options min(4, 8) and min(7, 6).', 'value = [[6]]'),
  F('Minimax with stage values 5, 7, 6 on a route.', 'route value = [[7]]')],
 [X('<p>Use the network in the worked examples.</p>',
    P('Explain why dynamic programming works backwards from T.', [('B1', 'the best continuation from each state is then known when earlier decisions are made (principle of optimality)')]),
    P('Find the minimax route from S to T and its value.', [('M1', 'stage values: D 8, E 6, F 3'), ('M1', 'A 7, B 6, C 6 at stage 2'), ('A1', 'S: min(max(5, 7), max(3, 6), max(6, 6)) = 6'), ('A1', 'S–B–E–T (or S–C–E–T / S–C–F–T), value 6')], ans=6)),
  X('<p>A firm must supply 3 machines at the end of each of the next two months. Making 1, 2, 3, 4 or 5 machines in a month costs 4, 7, 9, 12 or 16 respectively. Each machine stored from month 1 to month 2 costs 1. No stock is held at the start or required at the end.</p>',
    P('Use dynamic programming to find the production plan that minimises total cost.', [('M1', 'stage 2: with s machines in stock, make 3 − s, at cost 9, 7 or 4'), ('M1', 'stage 1: make 3 + s with storage cost s'), ('A1', 'totals 18, 20 and 22 for s = 0, 1, 2'), ('A1', 'make 3 in each month: cost 18')], ans=18)),
  X('', P('In dynamic programming, explain the terms stage, state and action.', [('B1', 'a stage is a step in the decision process; a state is the situation at the start of a stage'), ('B1', 'an action is a decision that moves from a state at one stage to a state at the next')]))])
# minimax for exam
mx = lambda p: max(Ed[(p[i], p[i + 1])] for i in range(len(p) - 1)); assert min(mx(p) for p in paths) == 6

# ------------------------------------------------------------------ d2-games
M = np.array([[4, 2, 5], [1, 1, 0], [6, 2, 3]]); assert M.min(1).max() == 2 and M.max(0).min() == 2
p, v = game([[3, -1, 2], [-2, 4, 1]]); assert np.allclose(p, [0.6, 0.4]) and close(v, 1)
p, v = game([[2, -1], [-1, 3]]); assert np.allclose(p, [4 / 7, 3 / 7]) and close(v, 5 / 7)
p, v = game([[4, -2, 1], [-1, 3, 0]]); assert np.allclose(p, [0.5, 0.5]) and close(v, 0.5)
D3 = np.array([[3, 1, 4], [2, 0, 3], [5, 2, 1]]); assert all(D3[0] > D3[1])
p, v = game([[3, 1, 4], [5, 2, 1]]); assert close(v, game(D3)[1])
deep('d2-games',
 'Check for a saddle point first: if the largest row minimum equals the smallest column maximum, both players should play safe. Otherwise remove dominated strategies, then for a 2 × n game plot the row player’s expected gain against p for each column and choose p at the highest point of the lower boundary.',
 [E('A stable solution', 'Find the play-safe strategies for the game with row payoffs R1: 4, 2, 5; R2: 1, 1, 0; R3: 6, 2, 3.', 'Row minima 2, 0, 2: the row player’s maximin is 2 (R1 or R3).', 'Column maxima 6, 2, 5: the column player’s minimax is 2 (C2).', 'Maximin = minimax = 2, so there is a saddle point.', 'Play safe: R1 or R3 against C2; value 2.'),
  E('A 2 × 3 game', 'Row payoffs: R1: 3, −1, 2; R2: −2, 4, 1. Find the row player’s optimal mixed strategy and the value.', 'Let R1 be played with probability p. Expected gains: C1: 5p − 2; C2: 4 − 5p; C3: p + 1.', 'The row player maximises the least of these lines.', 'The lowest boundary is highest where 5p − 2 = 4 − 5p, so p = 0.6 (and then C3 gives 1.6 ≥ 1).', 'Play R1 with probability 0.6 and R2 with 0.4; value 1.'),
  E('Dominance', 'Reduce the game R1: 3, 1, 4; R2: 2, 0, 3; R3: 5, 2, 1 using dominance.', 'Every entry of R1 exceeds the matching entry of R2.', 'So R1 dominates R2, and R2 can be removed.', 'The game reduces to R1: 3, 1, 4; R3: 5, 2, 1, which has the same value.')],
 [F('Row minima 2, 0, 2.', 'maximin = [[2]]'),
  F('Column maxima 6, 2, 5.', 'minimax = [[2]]'),
  F('A zero-sum game where the row player wins 3.', 'the column player’s payoff = [[-3]]')],
 [X('<p>A two-person zero-sum game has row payoffs R1: 2, −1; R2: −1, 3.</p>',
    P('Show that the game has no saddle point.', [('M1', 'row minima −1, −1 and column maxima 2, 3'), ('A1', 'maximin −1 ≠ minimax 2')]),
    P('Find the optimal strategy for the row player and the value of the game.', [('M1', 'expected gains 3p − 1 and 3 − 4p'), ('M1', 'equates: 3p − 1 = 3 − 4p'), ('A1', 'p = 4/7'), ('A1', 'value 5/7')], ans=5 / 7)),
  X('<p>Row payoffs: R1: 4, −2, 1; R2: −1, 3, 0.</p>',
    P('Find the row player’s optimal mixed strategy and the value of the game.', [('M1', 'lines 5p − 1, 3 − 5p, p'), ('M1', 'finds the highest point of the lower boundary'), ('A1', 'p = ½'), ('A1', 'value ½')], ans=0.5)),
  X('', P('Explain how a zero-sum game can be formulated as a linear programming problem for the row player.', [('B1', 'add a constant so that all payoffs are positive'), ('B1', 'maximise V subject to the expected gain against each column being at least V, with the probabilities summing to 1')]))])

# ------------------------------------------------------------------ d2-recurrence
u = [5000.0]
for n in range(40): u.append(1.01 * u[-1] - 200)
assert all(close(u[n], 20000 - 15000 * 1.01 ** n) for n in range(41)) and min(n for n in range(41) if u[n] <= 0) == 29
v = [1, 5]
for n in range(8): v.append(v[-1] + 2 * v[-2])
assert v == [2 ** (n + 1) - (-1) ** n for n in range(10)]
Pp = [2000.0]
for n in range(30): Pp.append(0.9 * Pp[-1] + 400)
assert all(close(Pp[n], 4000 - 2000 * 0.9 ** n) for n in range(31)) and min(n for n in range(31) if Pp[n] > 3500) == 14
w = [1, 4]
for n in range(6): w.append(5 * w[-1] - 6 * w[-2])
assert w == [2 * 3 ** n - 2 ** n for n in range(8)] and w[4] == 146
s = [0.0]
for n in range(24): s.append(1.005 * s[-1] + 100)
assert close(s[24], 20000 * (1.005 ** 24 - 1)) and round(s[24], 2) == 2543.20
assert 6 / 0.5 == 12 and 10 / 0.2 == 50 and 2 * 27 == 54
deep('d2-recurrence',
 'Identify the order and the type before solving: a first-order recurrence uₙ₊₁ = auₙ + b has a constant particular solution b/(1 − a) when a ≠ 1, and second-order linear recurrences use the auxiliary equation. Always check one value from the recurrence, and interpret the long-term behaviour (the limit exists when |a| &lt; 1).',
 [E('Repaying a loan', 'A debt of £5000 has 1% interest added each month, after which £200 is repaid. Find the debt after n months and when it is cleared.', 'uₙ₊₁ = 1.01uₙ − 200, u₀ = 5000.', 'Constant solution c = 1.01c − 200, so c = 20 000.', 'uₙ = 20 000 − 15 000(1.01)ⁿ.', 'uₙ ≤ 0 when 1.01ⁿ ≥ 4/3: n ≥ 28.9, so the debt is cleared in the 29th month.'),
  E('A second-order recurrence', 'Solve uₙ₊₂ = uₙ₊₁ + 2uₙ with u₀ = 1 and u₁ = 5.', 'm² − m − 2 = 0 gives m = 2 or m = −1.', 'uₙ = A(2)ⁿ + B(−1)ⁿ, with A + B = 1 and 2A − B = 5.', 'A = 2 and B = −1.', 'uₙ = 2ⁿ⁺¹ − (−1)ⁿ; check u₂ = 8 − 1 = 7 = 5 + 2.')],
 [F('uₙ₊₁ = 0.5uₙ + 6.', 'constant solution = [[12]]'),
  F('uₙ₊₁ = 0.8uₙ + 10.', 'limit = [[50]]'),
  F('uₙ₊₁ = 3uₙ with u₀ = 2.', 'u₃ = [[54]]')],
 [X('<p>A fish population is modelled by Pₙ₊₁ = 0.9Pₙ + 400, where P₀ = 2000.</p>',
    P('Find Pₙ in terms of n.', [('M1', 'constant solution 4000'), ('M1', 'Pₙ = 4000 + C(0.9)ⁿ'), ('A1', 'Pₙ = 4000 − 2000(0.9)ⁿ')]),
    P('State the long-term population.', [('B1', '4000')], ans=4000),
    P('Find the first year in which the population exceeds 3500.', [('M1', '0.9ⁿ &lt; 0.25'), ('A1', 'n = 14')], ans=14)),
  X('<p>uₙ₊₂ − 5uₙ₊₁ + 6uₙ = 0, with u₀ = 1 and u₁ = 4.</p>',
    P('Find uₙ in terms of n.', [('M1', 'auxiliary equation m² − 5m + 6 = 0'), ('A1', 'm = 2, 3'), ('M1', 'A + B = 1 and 2A + 3B = 4'), ('A1', 'uₙ = 2(3)ⁿ − 2ⁿ')]),
    P('Find u₄.', [('B1', '146')], ans=146)),
  X('<p>£100 is paid into a savings account at the end of each month. Interest of 0.5% is added to the balance each month before the payment. The account starts empty.</p>',
    P('Find the balance after 24 payments.', [('M1', 'sₙ₊₁ = 1.005sₙ + 100'), ('M1', 'sₙ = 20 000(1.005ⁿ − 1)'), ('A1', '£2543.20')], ans=2543.20, unit='£', tol=1e-4))])

# ------------------------------------------------------------------ d2-decision
dev = 0.6 * 200 + 0.4 * 20 - 50; assert dev == 78 and 0.6 * 150 + 0.4 * 60 == 114 and 114 - 78 == 36
L, Sm = 0.7 * 500 + 0.3 * -100, 0.7 * 250 + 0.3 * 80; assert close(L, 320) and close(Sm, 199) and close(0.7 * 500 + 0.3 * 80, 374) and close(374 - 320, 54)
assert close(0.4 * 3000, 1200) and close(1 - 0.25 - 0.35, 0.4) and close(0.4 * 100 + 0.25 * 40 + 0.35 * -30, 39.5)
assert close(0.3 * 100 + 0.7 * -20, 16) and 90 - 72 == 18
deep('d2-decision',
 'Draw the tree from left to right with decision nodes (squares) and chance nodes (circles), and put payoffs at the ends. Roll back from right to left: at a chance node take the expected value; at a decision node choose the best branch and mark the rejected branches. The expected value of perfect information is the expected value with perfect information minus the best expected monetary value without it.',
 [E('Rolling back a tree', 'A firm can develop a product (cost 50) or license it for a fixed 60. If developed, the product succeeds with probability 0.6 (income 200) or fails (income 20). Which option has the greater expected monetary value?', 'Chance node: 0.6 × 200 + 0.4 × 20 = 128.', 'Develop: 128 − 50 = 78.', 'License: 60.', 'Develop, since 78 &gt; 60.'),
  E('Expected value of perfect information', 'For the same decision, find the expected value of perfect information.', 'If success were known in advance: develop, net 150. If failure were known: license, 60.', 'Expected value with perfect information = 0.6 × 150 + 0.4 × 60 = 114.', 'EVPI = 114 − 78 = 36: the most worth paying for a perfect forecast.')],
 [F('Outcomes 100 (probability 0.3) and −20 (probability 0.7).', 'EMV = [[16]]'),
  F('Expected value with perfect information 90; best EMV 72.', 'EVPI = [[18]]'),
  F('The branches leaving a chance node.', 'their probabilities sum to [[1]]')],
 [X('<p>A company can build a large plant, a small plant, or neither. Demand will be high with probability 0.7 or low with probability 0.3. Profits (£k): large plant 500 (high) or −100 (low); small plant 250 (high) or 80 (low); neither 0.</p>',
    P('Use expected monetary value to decide which option the company should choose.', [('M1', 'EMV large = 0.7 × 500 + 0.3 × (−100) = 320'), ('M1', 'EMV small = 0.7 × 250 + 0.3 × 80 = 199'), ('A1', 'build the large plant')]),
    P('Find the expected value of perfect information.', [('M1', 'with perfect information: 0.7 × 500 + 0.3 × 80 = 374'), ('M1', '374 − 320'), ('A1', '54 (£54 000)')], ans=54),
    P('State the most the company should pay for a market survey.', [('B1', 'no more than £54 000, the EVPI')])),
  X('<p>A contestant can take £1000 or gamble: with probability 0.4 she wins £3000, otherwise nothing.</p>',
    P('Find the EMV of gambling and state the decision that maximises EMV.', [('M1', '0.4 × 3000'), ('A1', '£1200: gamble')], ans=1200),
    P('Give a reason why she might still take the £1000.', [('B1', 'she may be risk-averse: the 0.6 chance of nothing outweighs the higher EMV (utility differs from money)')])),
  X('<p>A chance node has outcomes 100, 40 and −30 with probabilities p, 0.25 and 0.35.</p>',
    P('Find p and the expected value at the node.', [('B1', 'p = 0.4'), ('M1', '0.4 × 100 + 0.25 × 40 + 0.35 × (−30)'), ('A1', '39.5')], ans=39.5))])

assert len(DEEP) - N0 == 13
for k_, dd in DEEP.items():
    assert len(dd['examples']) >= 2 and len(dd['fills']) >= 3 and len(dd['exam']) >= 3 and len(dd['tip']) > 120, k_
    for q in dd['exam']:
        for p in q['parts']: assert p['m'] == len(p['ms']), (k_, p['q'])
