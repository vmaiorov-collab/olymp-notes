// Ходим по рёбрам графа; на ребре с запасом x за проход забираем ceil(x/2), остаётся floor(x/2). Закончить можно только когда ход невозможен. Максимум собранного.
// Ребро с запасом w — это k ≤ ~30 «слоёв» с выигрышами g_1 ≥ g_2 ≥ ...; проход по ребру использует слои по порядку. Маршрут по c_e слоям каждого ребра — эйлеров путь в мультиграфе.
// Критерий: связный мультиграф, не более двух вершин нечётной степени. Достаточно рассматривать c_e ∈ {k_e, k_e − 1} (убрать последний слой): две копии не меняют чётность.
typedef long long ll;
ll bestWalk(int n, const vector<array<int,3>> &edges) {          // edges: (u, v, w)
    int m = edges.size();
    vector<vector<ll>> g(m);
    for (int i = 0; i < m; i++) { ll w = edges[i][2]; while (w > 0) { g[i].push_back((w + 1) / 2); w /= 2; } }   // слои: ceil(w/2), затем остаток floor(w/2)
    ll best = 0;
    for (int mask = 0; mask < (1 << m); mask++) {             // mask — рёбра, у которых убираем последний слой
        vector<int> p(n), deg(n, 0);
        iota(p.begin(), p.end(), 0);
        function<int(int)> f = [&](int x) { return p[x] == x ? x : p[x] = f(p[x]); };
        vector<int> cnt(m);
        for (int i = 0; i < m; i++) {
            cnt[i] = (int)g[i].size() - ((mask >> i) & 1);
            if (cnt[i] > 0) { p[f(edges[i][0])] = f(edges[i][1]); deg[edges[i][0]] += cnt[i]; deg[edges[i][1]] += cnt[i]; }
        }
        vector<ll> sum(n, 0); vector<int> odd(n, 0);
        for (int i = 0; i < m; i++) if (cnt[i] > 0) {
            ll s = 0; for (int k = 0; k < cnt[i]; k++) s += g[i][k];
            sum[f(edges[i][0])] += s;
        }
        for (int v = 0; v < n; v++) if (deg[v] % 2) odd[f(v)]++;
        for (int v = 0; v < n; v++) if (f(v) == v && odd[v] <= 2) best = max(best, sum[v]);   // берём одну компоненту связности целиком
    }
    return best;
}
