// Алгоритм Хирхольцера (итеративный): стек вершин, рёбра удаляются сразу при проходе. O(n + m).
// Возвращает вершины в порядке обхода всех рёбер; пустой результат — обход невозможен.
vector<int> euler(int n, const vector<pair<int,int>> &edges, int start) {
    vector<vector<pair<int,int>>> adj(n);
    for (int i = 0; i < (int)edges.size(); i++) {
        adj[edges[i].first].push_back({edges[i].second, i});
        adj[edges[i].second].push_back({edges[i].first, i});
    }
    vector<char> used(edges.size(), 0);
    vector<int> ptr(n, 0), stack{start}, res;
    while (!stack.empty()) {
        int v = stack.back();
        while (ptr[v] < (int)adj[v].size() && used[adj[v][ptr[v]].second]) ptr[v]++;   // пропускаем уже пройденные рёбра
        if (ptr[v] == (int)adj[v].size()) { res.push_back(v); stack.pop_back(); continue; }   // из v выходить некуда — вершина идёт в ответ
        auto [to, id] = adj[v][ptr[v]];
        used[id] = 1;                                         // ребро удалено сразу, как только прошли
        stack.push_back(to);
    }
    if (res.size() != edges.size() + 1) return {};            // не все рёбра достижимы из start (граф «несвязен»)
    reverse(res.begin(), res.end());                          // для цикла порядок безразличен, для пути — от start до конца
    return res;
}
// Критерий: цикл существует ⇔ все степени чётны и рёбра связны; путь ⇔ нечётных вершин 0 или 2 (старт — в нечётной).
vector<int> eulerCycleOrPath(int n, const vector<pair<int,int>> &edges, bool wantCycle) {
    if (edges.empty()) return {};
    vector<int> deg(n, 0), odd;
    for (auto &e : edges) { deg[e.first]++; deg[e.second]++; }
    for (int v = 0; v < n; v++) if (deg[v] % 2) odd.push_back(v);
    if (wantCycle ? !odd.empty() : (odd.size() != 0 && odd.size() != 2)) return {};
    int start = (!wantCycle && !odd.empty()) ? odd[0] : edges[0].first;
    return euler(n, edges, start);
}
