
"""Core TSP: distance, construction heuristics, local search, SA, TS, ILS, VNS."""

import time
import numpy as np


# ---------- Distance ----------

def dist_matrix(P, metric="Euclidean"):
    d = P[:, None, :] - P[None, :, :]
    if metric == "Euclidean":
        return np.sqrt((d ** 2).sum(2))
    if metric == "Manhattan":
        return np.abs(d).sum(2)
    raise ValueError(f"Distance metric tidak dikenal: {metric}")


def length(r, D):
    r = np.asarray(r, dtype=int)
    return float(D[r, np.roll(r, -1)].sum())


# ---------- Construction heuristics ----------

def nearest_neighbor(D, s):
    r = [s]
    left = set(range(len(D))) - {s}

    while left:
        c = min(left, key=lambda j: D[r[-1], j])
        r.append(c)
        left.remove(c)

    return r


def insertion(D, s, kind, rng):
    """NI: nearest, CI: cheapest, FI: farthest, AI: arbitrary insertion."""
    left = set(range(len(D))) - {s}

    first = (
        int(rng.choice(sorted(left))) if kind == "AI"
        else max(left, key=lambda j: D[s, j]) if kind == "FI"
        else min(left, key=lambda j: D[s, j])
    )

    r = [s, first]
    left.remove(first)

    def cost(c, p):
        return (
            D[r[p], c]
            + D[c, r[(p + 1) % len(r)]]
            - D[r[p], r[(p + 1) % len(r)]]
        )

    while left:
        if kind == "CI":
            c, p = min(
                ((c, p) for c in left for p in range(len(r))),
                key=lambda x: cost(*x),
            )
        else:
            if kind == "NI":
                c = min(left, key=lambda j: min(D[j, k] for k in r))
            elif kind == "FI":
                c = max(left, key=lambda j: min(D[j, k] for k in r))
            else:
                c = int(rng.choice(sorted(left)))

            p = min(range(len(r)), key=lambda p: cost(c, p))

        r.insert(p + 1, c)
        left.remove(c)

    return r


# ---------- Neighborhood moves ----------

def apply(r, m):
    op, i, j, k = m

    if op == "Swap":
        r = r[:]
        r[i], r[j] = r[j], r[i]
        return r

    if op == "2-opt":
        return r[:i] + r[i:j + 1][::-1] + r[j + 1:]

    # 3-opt: segment exchange
    return r[:i] + r[j:k] + r[i:j] + r[k:]


def rand_move(n, op, rng):
    if op == "3-opt":
        i, j, k = sorted(rng.choice(n + 1, 3, replace=False))
        return op, int(i), int(j), int(k)

    i, j = sorted(rng.choice(n, 2, replace=False))
    return op, int(i), int(j), 0


def neighborhood(n, op, size, rng):
    if op != "3-opt" and n * (n - 1) // 2 <= size:
        return [
            (op, i, j, 0)
            for i in range(n)
            for j in range(i + 1, n)
        ]

    return [rand_move(n, op, rng) for _ in range(size)]


def move_key(r, m):
    op, i, j, k = m
    cities = [r[i], r[j]]
    if op == "3-opt":
        cities.append(r[k % len(r)])
    return op, tuple(sorted(cities))


# ---------- Local search ----------

def two_opt_ls(r, D, strategy="Best Improvement", max_pass=200):
    r = r[:]
    n = len(r)

    for _ in range(max_pass):
        best = (-1e-9, None)

        for i in range(1, n - 1):
            for j in range(i + 1, n):
                a, b = r[i - 1], r[i]
                c, d = r[j], r[(j + 1) % n]

                delta = (
                    D[a, c] + D[b, d]
                    - D[a, b] - D[c, d]
                )

                if delta < best[0]:
                    best = (delta, (i, j))

                    if strategy == "First Improvement":
                        break

            if strategy == "First Improvement" and best[1]:
                break

        if best[1] is None:
            break

        i, j = best[1]
        r[i:j + 1] = r[i:j + 1][::-1]

    return r


# ---------- Simulated Annealing ----------

def simulated_annealing(
    r,
    D,
    T0=1000,
    alpha=0.9,
    Tmin=0.1,
    per_T=50,
    max_iter=5000,
    op="2-opt",
    seed=0,
):
    t0 = time.perf_counter()
    rng = np.random.default_rng(seed)

    current = r[:]
    current_dist = length(current, D)
    best = current[:]
    best_dist = current_dist

    temperature = T0
    iteration = 0
    hist = [best_dist]
    log = []

    while temperature > Tmin and iteration < max_iter:
        for _ in range(per_T):
            if iteration >= max_iter:
                break

            iteration += 1
            move = rand_move(len(r), op, rng)
            candidate = apply(current, move)
            candidate_dist = length(candidate, D)

            delta = candidate_dist - current_dist
            accepted = (
                delta < 0
                or rng.random() < np.exp(-delta / temperature)
            )

            if accepted:
                current = candidate
                current_dist = candidate_dist

            if current_dist < best_dist:
                best = current[:]
                best_dist = current_dist

            hist.append(best_dist)
            log.append({
                "Iteration": iteration,
                "Temperature": round(temperature, 4),
                "Move": str(move[:3]),
                "Accepted": bool(accepted),
                "Current_Distance": round(current_dist, 4),
                "Best_Distance": round(best_dist, 4),
            })

        temperature *= alpha

    return {
        "route": best,
        "dist": best_dist,
        "hist": hist,
        "log": log,
        "iters": iteration,
        "time": time.perf_counter() - t0,
    }


# ---------- Tabu Search ----------

def tabu_search(
    r,
    D,
    max_iter=500,
    tabu_size=10,
    nbr_size=50,
    op="2-opt",
    aspiration=True,
    seed=0,
    detail=False,
):
    """Tabu list FIFO berdasarkan atribut move."""
    t0 = time.perf_counter()
    rng = np.random.default_rng(seed)

    current = r[:]
    current_dist = length(current, D)
    best = current[:]
    best_dist = current_dist

    tabu_list = []
    hist = [best_dist]
    log = []

    for iteration in range(1, max_iter + 1):
        candidates = []

        for move in neighborhood(len(r), op, nbr_size, rng):
            route = apply(current, move)
            dist = length(route, D)
            is_tabu = move_key(current, move) in tabu_list
            candidates.append((move, route, dist, is_tabu))

        valid = [
            item for item in candidates
            if not item[3] or (aspiration and item[2] < best_dist)
        ]

        move, route, dist, _ = min(
            valid or candidates,
            key=lambda item: item[2],
        )

        key = move_key(current, move)
        removed = None

        if key in tabu_list:
            tabu_list.remove(key)

        tabu_list.append(key)

        if len(tabu_list) > tabu_size:
            removed = tabu_list.pop(0)

        previous = current
        current = route
        current_dist = dist

        if current_dist < best_dist:
            best = current[:]
            best_dist = current_dist

        hist.append(best_dist)

        row = {
            "Iteration": iteration,
            "Selected_Move": str(tuple(v + 1 for v in key[1])),
            "Current_Distance": round(current_dist, 4),
            "Best_Distance": round(best_dist, 4),
            "Tabu_List": str([
                tuple(v + 1 for v in item[1])
                for item in tabu_list
            ]),
            "Left": (
                str(tuple(v + 1 for v in removed[1]))
                if removed else "-"
            ),
        }

        if detail:
            row["Current_Before"] = [x + 1 for x in previous]
            row["Current_After"] = [x + 1 for x in current]
            row["Candidates"] = [
                {
                    "Move": str(tuple(sorted((
                        previous[m[1]] + 1,
                        previous[m[2]] + 1,
                    )))),
                    "Route": str([v + 1 for v in route_c]),
                    "Distance": round(dist_c, 4),
                    "Tabu": "Ya" if tabu else "Tidak",
                    "Selected": "✓" if m == move else "",
                }
                for m, route_c, dist_c, tabu in candidates
            ]

        log.append(row)

    return {
        "route": best,
        "dist": best_dist,
        "hist": hist,
        "log": log,
        "iters": max_iter,
        "time": time.perf_counter() - t0,
    }


# ---------- Iterated Local Search ----------

def double_bridge(r, rng):
    n = len(r)

    if n < 8:
        route = r[:]
        i, j = rng.choice(n, 2, replace=False)
        route[i], route[j] = route[j], route[i]
        return route

    a, b, c = sorted(
        int(x) for x in rng.choice(range(1, n), 3, replace=False)
    )
    return r[:a] + r[b:c] + r[a:b] + r[c:]


def iterated_local_search(
    r,
    D,
    iters=100,
    strategy="Best Improvement",
    seed=0,
):
    t0 = time.perf_counter()
    rng = np.random.default_rng(seed)

    current = two_opt_ls(r, D, strategy)
    current_dist = length(current, D)
    best = current[:]
    best_dist = current_dist

    hist = [best_dist]
    log = []

    for iteration in range(1, iters + 1):
        candidate = two_opt_ls(
            double_bridge(current, rng), D, strategy
        )
        candidate_dist = length(candidate, D)

        if candidate_dist <= current_dist:
            current = candidate
            current_dist = candidate_dist

        if current_dist < best_dist:
            best = current[:]
            best_dist = current_dist

        hist.append(best_dist)
        log.append({
            "Iteration": iteration,
            "Candidate_Distance": round(candidate_dist, 4),
            "Current_Distance": round(current_dist, 4),
            "Best_Distance": round(best_dist, 4),
        })

    return {
        "route": best,
        "dist": best_dist,
        "hist": hist,
        "log": log,
        "iters": iters,
        "time": time.perf_counter() - t0,
    }


# ---------- Variable Neighborhood Search ----------

def _vns_shake(route, operator, rng, moves=1):
    """Menghasilkan kandidat melalui shaking pada neighborhood tertentu."""
    candidate = route[:]
    n = len(candidate)

    for _ in range(max(1, int(moves))):
        i, j = map(int, rng.choice(n, 2, replace=False))

        if operator == "Swap":
            candidate[i], candidate[j] = candidate[j], candidate[i]

        elif operator == "Insertion":
            city = candidate.pop(i)
            candidate.insert(j, city)

        elif operator == "2-opt":
            i, j = sorted((i, j))
            candidate[i:j + 1] = candidate[i:j + 1][::-1]

        else:
            raise ValueError(
                f"Neighborhood VNS tidak dikenal: {operator}"
            )

    return candidate


def variable_neighborhood_search(
    r,
    D,
    max_iter=500,
    k_max=3,
    neighborhoods=None,
    shaking="Satu move acak",
    local_search=True,
    strategy="Best Improvement",
    seed=0,
):
    """
    Variable Neighborhood Search (VNS).

    Menggunakan shaking, perpindahan neighborhood, dan optional 2-opt.
    Seluruh jarak dihitung dengan matriks D yang diberikan.
    """
    t0 = time.perf_counter()
    rng = np.random.default_rng(seed)

    allowed = ["Swap", "Insertion", "2-opt"]
    neighborhoods = (
        allowed[:]
        if neighborhoods is None
        else [op for op in neighborhoods if op in allowed]
    )

    if not neighborhoods:
        raise ValueError("Pilih minimal satu neighborhood VNS.")

    k_max = max(1, min(int(k_max), len(neighborhoods)))
    neighborhoods = neighborhoods[:k_max]

    current = r[:]
    current_dist = length(current, D)
    best = current[:]
    best_dist = current_dist

    hist = [best_dist]
    log = []
    k = 0

    for iteration in range(1, max(0, int(max_iter)) + 1):
        operator = neighborhoods[k]
        neighborhood_index = k + 1

        moves = (
            1 if shaking == "Satu move acak"
            else neighborhood_index
        )

        candidate = _vns_shake(
            current, operator, rng, moves
        )

        if local_search:
            candidate = two_opt_ls(candidate, D, strategy)

        candidate_dist = length(candidate, D)
        accepted = candidate_dist < current_dist - 1e-12

        if accepted:
            current = candidate
            current_dist = candidate_dist

            if current_dist < best_dist - 1e-12:
                best = current[:]
                best_dist = current_dist

            # Perbaikan: kembali ke neighborhood pertama.
            k = 0
        else:
            # Tidak ada perbaikan: pindah ke neighborhood berikutnya.
            k = (k + 1) % len(neighborhoods)

        hist.append(best_dist)
        log.append({
            "Iteration": iteration,
            "Neighborhood": operator,
            "Neighborhood_Index": neighborhood_index,
            "Shaking_Moves": moves,
            "Candidate_Distance": round(candidate_dist, 4),
            "Current_Distance": round(current_dist, 4),
            "Best_Distance": round(best_dist, 4),
            "Accepted": bool(accepted),
        })

    return {
        "route": best,
        "dist": best_dist,
        "hist": hist,
        "log": log,
        "iters": len(log),
        "time": time.perf_counter() - t0,
    }
