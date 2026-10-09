// Мосты и точки сочленения одним DFS, O(n + m). Рёбра различаем по номеру, поэтому кратные рёбра обрабатываются верно.
struct Graph {
    int n;
    vector<vector<pair<int,int>>> adj;                        // (сосед, номер ребра)
    vector<pair<int,int>> edges;
    Graph(int n) : n(n), adj(n) {}
    void addEdge(int a, int b) { adj[a].push_back({b, (int)edges.size()}); adj[b].push_back({a, (int)edges.size()}); edges.push_back({a, b}); }
};
struct Cut {
    vector<int> depth, up;                                    // up[v] — минимальная глубина, достижимая из поддерева v одним обратным ребром
    vector<char> isBridge, isCut;
    Cut(const Graph &g) : depth(g.n, -1), up(g.n), isBridge(g.edges.size(), 0), isCut(g.n, 0) {
        for (int v = 0; v < g.n; v++) if (depth[v] < 0) { depth[v] = 0; dfs(g, v, -1); }
    }
    void dfs(const Graph &g, int v, int parentEdge) {         // parentEdge — НОМЕР ребра, по которому пришли в v
        up[v] = depth[v];
        int children = 0;
        for (auto [to, id] : g.adj[v]) {
            if (id == parentEdge) continue;                   // не ходим назад по тому же ребру (но параллельное ребро — другой номер!)
            if (depth[to] >= 0) { up[v] = min(up[v], depth[to]); continue; }   // обратное ребро вверх
            depth[to] = depth[v] + 1;
            dfs(g, to, id); children++;
            up[v] = min(up[v], up[to]);
            if (up[to] >= depth[to]) isBridge[id] = 1;        // из поддерева to не подняться выше v по другому ребру
            if (parentEdge >= 0 && up[to] >= depth[v]) isCut[v] = 1;     // поддерево to отвалится при удалении v
        }
        if (parentEdge < 0 && children >= 2) isCut[v] = 1;    // корень — точка сочленения, если у него два и более сына
    }
};
