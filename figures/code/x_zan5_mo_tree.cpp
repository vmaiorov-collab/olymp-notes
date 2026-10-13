#include <bits/stdc++.h>
using namespace std;

// mex чисел на пути в дереве: алгоритм Мо по эйлерову обходу с обновлениями
// структура: добавить/убрать значение за O(1), mex за O(sqrt V)
struct SqrtMex {
    int V, B; vector<int> cnt, nz;          // nz[j] — сколько значений блока j присутствуют
    SqrtMex(int V) : V(V), B(max(1, (int)sqrt((double)V))), cnt(V, 0), nz(V / B + 1, 0) {}
    void add(int x) { if (cnt[x]++ == 0) nz[x / B]++; }
    void del(int x) { if (--cnt[x] == 0) nz[x / B]--; }
    int mex() {
        int j = 0;
        while ((j + 1) * B <= V && nz[j] == B) j++;     // полностью заполненные блоки пропускаем
        int x = j * B;
        while (x < V && cnt[x]) x++;
        return x;
    }
};

struct Query { int l, r, t, extra, id; };

vector<int> path_mex(int n, const vector<vector<int>>& g, vector<int> val,
                     const vector<array<int,3>>& ops /* {1,u,v} или {2,x,newval} */) {
    // эйлеров обход: каждая вершина встречается дважды
    vector<int> tin(n), tout(n), ev, par(n, -1), depth(n, 0);
    vector<vector<int>> up(18, vector<int>(n, 0));
    {   // итеративный обход
        vector<pair<int,int>> st = {{0, 0}};
        tin[0] = 0; ev.push_back(0);
        while (!st.empty()) {
            auto& [v, i] = st.back();
            if (i < (int)g[v].size()) {
                int u = g[v][i++];
                if (u == par[v]) continue;
                par[u] = v; depth[u] = depth[v] + 1; tin[u] = ev.size(); ev.push_back(u); st.push_back({u, 0});
            } else { tout[v] = ev.size(); ev.push_back(v); st.pop_back(); }
        }
    }
    for (int v = 0; v < n; v++) up[0][v] = par[v] < 0 ? v : par[v];
    for (int k = 1; k < 18; k++) for (int v = 0; v < n; v++) up[k][v] = up[k - 1][up[k - 1][v]];
    auto lca = [&](int a, int b) {
        if (depth[a] < depth[b]) swap(a, b);
        for (int k = 17; k >= 0; k--) if (depth[a] - (1 << k) >= depth[b]) a = up[k][a];
        if (a == b) return a;
        for (int k = 17; k >= 0; k--) if (up[k][a] != up[k][b]) { a = up[k][a]; b = up[k][b]; }
        return up[0][a];
    };
    vector<Query> qs; vector<array<int,3>> upd; vector<int> cur = val;   // upd: {вершина, старое, новое}
    int answers = 0;
    for (auto& op : ops) {
        if (op[0] == 2) { upd.push_back({op[1], cur[op[1]], op[2]}); cur[op[1]] = op[2]; }
        else {
            int u = op[1], v = op[2];
            if (tin[u] > tin[v]) swap(u, v);
            int l = lca(u, v);
            if (l == u) qs.push_back({tin[u], tin[v], (int)upd.size(), -1, answers++});
            else qs.push_back({tout[u], tin[v], (int)upd.size(), l, answers++});
        }
    }
    int N = ev.size(), K = max(1, (int)cbrt((double)N * N));
    sort(qs.begin(), qs.end(), [&](const Query& a, const Query& b) {
        if (a.l / K != b.l / K) return a.l / K < b.l / K;
        if (a.r / K != b.r / K) return a.r / K < b.r / K;
        return a.t < b.t;
    });
    SqrtMex M(n + 1); vector<char> used(n, 0); vector<int> res(answers);
    auto toggle = [&](int v) { if (used[v]) { M.del(val[v]); used[v] = 0; } else { M.add(val[v]); used[v] = 1; } };
    auto apply = [&](int i, bool forward) {
        int x = upd[i][0], to = forward ? upd[i][2] : upd[i][1];
        if (used[x]) { M.del(val[x]); M.add(to); }
        val[x] = to;
    };
    int L = 0, R = -1, T = 0;
    for (auto& q : qs) {
        while (T < q.t) apply(T++, true);
        while (T > q.t) apply(--T, false);
        while (L > q.l) toggle(ev[--L]);
        while (R < q.r) toggle(ev[++R]);
        while (L < q.l) toggle(ev[L++]);
        while (R > q.r) toggle(ev[R--]);
        if (q.extra >= 0) toggle(q.extra);            // вершина LCA не лежит в отрезке: добавляем её на время ответа
        res[q.id] = M.mex();
        if (q.extra >= 0) toggle(q.extra);
    }
    return res;
}

#ifdef TEST_MAIN
int main() {
    mt19937 rng(11);
    for (int it = 0; it < 600; it++) {
        int n = rng() % 12 + 1; vector<vector<int>> g(n); vector<int> par(n, -1);
        for (int v = 1; v < n; v++) { int p = rng() % v; par[v] = p; g[p].push_back(v); g[v].push_back(p); }
        vector<int> val(n); for (auto& x : val) x = rng() % (n + 1);
        vector<array<int,3>> ops; vector<int> cur = val; vector<int> expect;
        for (int s = 0; s < 30; s++) {
            if (rng() % 3 == 0) { int x = rng() % n, nv = rng() % (n + 1); ops.push_back({2, x, nv}); cur[x] = nv; }
            else {
                int u = rng() % n, v = rng() % n; ops.push_back({1, u, v});
                set<int> st; vector<int> pu, pv; int a = u, b = v;
                vector<int> anc; for (int x = u; x >= 0; x = par[x]) anc.push_back(x);
                set<int> as(anc.begin(), anc.end());
                int l = v; while (!as.count(l)) l = par[l];
                for (int x = u; x != l; x = par[x]) st.insert(cur[x]);
                for (int x = v; x != l; x = par[x]) st.insert(cur[x]);
                st.insert(cur[l]);
                int mex = 0; while (st.count(mex)) mex++;
                expect.push_back(mex);
            }
        }
        auto got = path_mex(n, g, val, ops);
        if (got != expect) { puts("FAIL mo tree"); return 1; }
    }
    puts("ok");
}
#endif
