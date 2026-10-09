// Минимальное число рёбер, которые нужно добавить связному графу, чтобы в нём не осталось мостов: ⌈листьев / 2⌉ в дереве компонент рёберной двусвязности.
// Использует Graph и Cut из разбора лекции (мосты одним DFS).
int minEdgesNoBridges(const Graph &g) {
    Cut c(g);
    vector<int> comp(g.n, -1); int k = 0;
    for (int s = 0; s < g.n; s++) {                           // компоненты рёберной двусвязности: связность без мостов
        if (comp[s] >= 0) continue;
        comp[s] = k; vector<int> st{s};
        while (!st.empty()) { int v = st.back(); st.pop_back(); for (auto [to, id] : g.adj[v]) if (!c.isBridge[id] && comp[to] < 0) { comp[to] = k; st.push_back(to); } }
        k++;
    }
    vector<int> deg(k, 0);
    for (int i = 0; i < (int)g.edges.size(); i++) if (c.isBridge[i]) { deg[comp[g.edges[i].first]]++; deg[comp[g.edges[i].second]]++; }
    int leaves = 0;
    for (int d : deg) leaves += (d == 1);
    return (leaves + 1) / 2;                                  // k = 1 (мостов нет) даёт 0
}
