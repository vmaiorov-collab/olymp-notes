// Круглоквадратное дерево (block-cut tree): круглые вершины 0..n-1 — вершины графа, квадратные n.. — блоки (компоненты вершинной двусвязности).
struct BlockCut {
    int n, timer = 0;
    vector<vector<int>> g, tree;
    vector<int> tin, up, stk;
    BlockCut(int n, const vector<pair<int,int>> &edges) : n(n), g(n), tin(n, -1), up(n) {
        for (auto &e : edges) { g[e.first].push_back(e.second); g[e.second].push_back(e.first); }
        tree.resize(n);
        for (int v = 0; v < n; v++) if (tin[v] < 0) { dfs(v, -1); stk.clear(); }
    }
    void dfs(int v, int p) {
        tin[v] = up[v] = timer++;
        stk.push_back(v);                                     // стек вершин текущего блока
        for (int to : g[v]) {
            if (to == p) continue;                            // (кратные рёбра на блоки не влияют)
            if (tin[to] >= 0) { up[v] = min(up[v], tin[to]); continue; }
            dfs(to, v);
            up[v] = min(up[v], up[to]);
            if (up[to] >= tin[v]) {                           // v отделяет поддерево to: вынимаем из стека целый блок
                int block = tree.size(); tree.push_back({});
                int x;
                do { x = stk.back(); stk.pop_back(); tree[block].push_back(x); tree[x].push_back(block); } while (x != to);
                tree[block].push_back(v); tree[v].push_back(block);   // сама v остаётся в стеке — она в блоке, но не уходит из стека
            }
        }
    }
};
