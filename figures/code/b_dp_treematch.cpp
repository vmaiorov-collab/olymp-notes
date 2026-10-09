// Максимальное паросочетание в дереве: dp0[v] — максимум в поддереве v, если v никому не поставлена пара; dp1[v] — максимум, где v занята (или не имеет значения).
// Здесь dp1 храним как «лучшее значение вообще», dp0 как «v свободна».
struct TreeMatch {
    int n; vector<vector<int>> g; vector<int> free0, best;      // free0[v]: v свободна; best[v] = максимум по поддереву v
    TreeMatch(int n) : n(n), g(n), free0(n), best(n) {}
    void addEdge(int a, int b) { g[a].push_back(b); g[b].push_back(a); }
    void dfs(int v, int p) {
        int sum = 0;
        for (int to : g[v]) if (to != p) { dfs(to, v); sum += best[to]; }
        free0[v] = sum;                                         // v свободна: дети независимы
        best[v] = sum;
        for (int to : g[v]) if (to != p)                        // пара v—to: у to должна быть свободная вершина
            best[v] = max(best[v], sum - best[to] + free0[to] + 1);
    }
    int solve() { dfs(0, -1); return best[0]; }
};
