// Компоненты сильной связности (алгоритм Косарайю в версии лекции): порядок выхода по обратному графу, затем обход прямого графа.
struct SCC {
    int n, comps = 0;
    vector<vector<int>> g, rg;
    vector<int> comp, order;
    vector<char> seen;
    SCC(int n) : n(n), g(n), rg(n), comp(n, -1), seen(n, 0) {}
    void addEdge(int a, int b) { g[a].push_back(b); rg[b].push_back(a); }
    void dfs1(int v) {                                        // обход обратного графа, вершину кладём в order при ВЫХОДЕ
        seen[v] = 1;
        for (int to : rg[v]) if (!seen[to]) dfs1(to);
        order.push_back(v);
    }
    void dfs2(int v, int c) {                                 // обычный обход прямого графа: всё достижимое окрашиваем в c
        comp[v] = c;
        for (int to : g[v]) if (comp[to] < 0) dfs2(to, c);
    }
    void run() {
        for (int v = 0; v < n; v++) if (!seen[v]) dfs1(v);
        reverse(order.begin(), order.end());                  // убывание времени выхода
        for (int v : order) if (comp[v] < 0) dfs2(v, comps++);
        // номера компонент идут в порядке, ОБРАТНОМ топологическому порядку конденсации: comp 0 — «сток»
    }
};
// топологическая сортировка DAG: порядок выхода из DFS, развёрнутый
vector<int> topSort(const vector<vector<int>> &g, bool &ok) {
    int n = g.size();
    vector<int> out, state(n, 0);
    ok = true;
    function<void(int)> dfs = [&](int v) {
        state[v] = 1;
        for (int to : g[v]) {
            if (state[to] == 1) ok = false;                   // ребро в вершину на стеке — цикл
            else if (state[to] == 0) dfs(to);
        }
        state[v] = 2; out.push_back(v);
    };
    for (int v = 0; v < n; v++) if (!state[v]) dfs(v);
    reverse(out.begin(), out.end());
    return out;
}
