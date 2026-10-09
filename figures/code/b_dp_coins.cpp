// Вершины v, после удаления которых граф становится двудольным. DFS-дерево; «нечётное» вертикальное ребро — то, что вместе с путём по дереву даёт нечётный цикл.
struct Bip {
    int n, oddTotal = 0;
    vector<vector<pair<int,int>>> adj;                        // (сосед, номер ребра)
    vector<int> depth, par, cover, minOdd, minEven;
    vector<vector<int>> child;
    int m = 0;
    Bip(int n) : n(n), adj(n), depth(n, -1), par(n, -1), cover(n, 0), minOdd(n, INT_MAX), minEven(n, INT_MAX), child(n) {}
    void addEdge(int a, int b) { adj[a].push_back({b, m}); if (a != b) adj[b].push_back({a, m}); m++; }
    void dfs(int v, int pe) {
        for (auto [to, id] : adj[v]) {
            if (id == pe) continue;
            if (depth[to] < 0) { depth[to] = depth[v] + 1; par[to] = v; child[v].push_back(to); dfs(to, id); }
            else if (depth[to] <= depth[v]) {                  // вертикальное ребро v → предок to (или петля)
                bool odd = (depth[v] - depth[to]) % 2 == 0;     // чётная разность глубин ⇒ цикл нечётной длины
                if (odd) { oddTotal++; cover[v]++; if (par[to] >= 0) cover[par[to]]--; minOdd[v] = min(minOdd[v], depth[to]); }
                else minEven[v] = min(minEven[v], depth[to]);
            }
        }
        for (int c : child[v]) {                              // подъём значений и накопление покрытий по поддереву
            cover[v] += cover[c]; minOdd[v] = min(minOdd[v], minOdd[c]); minEven[v] = min(minEven[v], minEven[c]);
        }
    }
    vector<int> goodVertices() {                              // все вершины, удаление которых даёт двудольный граф
        for (int r = 0; r < n; r++) if (depth[r] < 0) { depth[r] = 0; dfs(r, -1); }
        vector<int> res;
        for (int v = 0; v < n; v++) {
            if (cover[v] != oddTotal) continue;                // каждое нечётное ребро должно «накрывать» v (или заканчиваться в нём)
            bool ok = true;
            for (int c : child[v]) if (minOdd[c] < depth[v] && minEven[c] < depth[v]) ok = false;   // из одного поддерева наверх не должно идти рёбер обеих чётностей
            if (ok) res.push_back(v);
        }
        return res;
    }
};
