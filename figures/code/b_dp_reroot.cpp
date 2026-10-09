// Сумма расстояний от каждой вершины до всех остальных в дереве с весами рёбер (переподвешивание). Без рекурсии, O(n).
typedef long long ll;
vector<ll> sumDist(int n, const vector<array<int,3>> &edges) {      // (a, b, вес)
    vector<vector<pair<int,int>>> g(n);
    for (auto &e : edges) { g[e[0]].push_back({e[1], e[2]}); g[e[1]].push_back({e[0], e[2]}); }
    vector<int> order, par(n, -1), pw(n, 0);
    order.push_back(0);
    for (size_t i = 0; i < order.size(); i++) { int v = order[i]; for (auto [to, w] : g[v]) if (to != par[v]) { par[to] = v; pw[to] = w; order.push_back(to); } }
    vector<ll> sz(n, 1), down(n, 0), ans(n, 0);
    for (int i = n - 1; i > 0; i--) { int v = order[i]; sz[par[v]] += sz[v]; down[par[v]] += down[v] + (ll)pw[v] * sz[v]; }
    ans[0] = down[0];                                           // ответ для корня — сумма «вниз»
    for (int i = 1; i < n; i++) { int v = order[i]; ans[v] = ans[par[v]] + (ll)pw[v] * (n - 2 * sz[v]); }   // сдвиг корня на ребро (p, v)
    return ans;
}
