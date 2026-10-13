#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

static int isqrt_ceil(ll x) { int r = (int)sqrt((double)x); while ((ll)r * r < x) r++; return max(r, 1); }

// ---------- 1. Блоки: присвоение в точке и сумма на отрезке [l, r) ----------
struct BlockSum {
    int n, B; vector<ll> a, blk;
    BlockSum(const vector<ll>& v) : n(v.size()), B(isqrt_ceil(v.size())), a(v), blk((v.size() + B - 1) / B + 1, 0) {
        for (int i = 0; i < n; i++) blk[i / B] += a[i];
    }
    void assign(int i, ll x) { blk[i / B] += x - a[i]; a[i] = x; }          // O(1)
    ll sum(int l, int r) {                                                  // O(sqrt n)
        ll s = 0;
        for (int i = l; i < r;) {
            if (i % B == 0 && i + B <= r) { s += blk[i / B]; i += B; }     // перепрыгнули через целый блок
            else { s += a[i]; i++; }                                        // идём по префиксу/суффиксу по одному
        }
        return s;
    }
};

// ---------- 2. Префиксные суммы внутри блоков: запрос за O(1), изменение за O(sqrt n) ----------
struct PrefixBlocks {
    int n, B; vector<ll> a, in, before;          // in[i] — сумма a от начала блока до i включительно; before[b] — сумма всех блоков до b
    PrefixBlocks(const vector<ll>& v) : n(v.size()), B(isqrt_ceil(v.size())), a(v), in(v.size()), before((v.size() + B - 1) / B + 1, 0) {
        int nb = (n + B - 1) / B;
        for (int b = 0; b < nb; b++) {
            ll run = 0;
            for (int i = b * B; i < min(n, (b + 1) * B); i++) { run += a[i]; in[i] = run; }
            before[b + 1] = before[b] + run;
        }
    }
    void add(int i, ll d) {
        a[i] += d;
        for (int j = i; j < min(n, (i / B + 1) * B); j++) in[j] += d;      // свой блок пересчитываем честно
        for (int b = i / B + 1; b < (int)before.size(); b++) before[b] += d;  // остальным блокам — «отложенная» добавка
    }
    ll pref(int i) { return i == 0 ? 0 : in[i - 1] + before[(i - 1) / B]; }   // сумма a[0..i)
    ll sum(int l, int r) { return pref(r) - pref(l); }
};

// ---------- 3. Отсортированные блоки: += x на отрезке и «сколько элементов <= x» ----------
struct SortedBlocks {
    int n, B; vector<ll> a, lazy; vector<vector<ll>> s;    // истинное значение = a[i] + lazy[блок]
    SortedBlocks(const vector<ll>& v, int B) : n(v.size()), B(B), a(v), lazy((v.size() + B - 1) / B, 0), s(lazy.size()) {
        for (int b = 0; b < (int)s.size(); b++) rebuild(b);
    }
    void rebuild(int b) { s[b].assign(a.begin() + b * B, a.begin() + min(n, (b + 1) * B)); sort(s[b].begin(), s[b].end()); }
    void part(int b, int l, int r, ll x) { for (int i = l; i < r; i++) a[i] += x; rebuild(b); }
    void add(int l, int r, ll x) {                         // [l, r)
        if (l >= r) return;
        int bl = l / B, br = (r - 1) / B;
        if (bl == br) { part(bl, l, r, x); return; }
        part(bl, l, (bl + 1) * B, x); part(br, br * B, r, x);
        for (int b = bl + 1; b < br; b++) lazy[b] += x;
    }
    int count_le(int l, int r, ll x) {                     // сколько a[i] <= x на [l, r)
        if (l >= r) return 0;
        int bl = l / B, br = (r - 1) / B, res = 0;
        auto scan = [&](int lo, int hi) { for (int i = lo; i < hi; i++) res += a[i] + lazy[i / B] <= x; };
        if (bl == br) { scan(l, r); return res; }
        scan(l, (bl + 1) * B); scan(br * B, r);
        for (int b = bl + 1; b < br; b++) res += upper_bound(s[b].begin(), s[b].end(), x - lazy[b]) - s[b].begin();
        return res;
    }
};

// ---------- 4. Обход точек полосами шириной B ----------
vector<int> strip_order(const vector<pair<int, int>>& p, int B, bool snake) {
    vector<int> id(p.size()); iota(id.begin(), id.end(), 0);
    sort(id.begin(), id.end(), [&](int i, int j) {
        int bi = p[i].first / B, bj = p[j].first / B;
        if (bi != bj) return bi < bj;
        if (snake && bi % 2) return p[i].second > p[j].second;     // на нечётных полосах идём вниз
        return p[i].second < p[j].second;
    });
    return id;
}
ll tour_length(const vector<pair<int, int>>& p, const vector<int>& ord) {   // манхэттенская длина пути от (0, 0)
    ll len = 0; int x = 0, y = 0;
    for (int i : ord) { len += abs(p[i].first - x) + abs(p[i].second - y); x = p[i].first; y = p[i].second; }
    return len;
}

// ---------- 5. Порядок запросов в алгоритме Мо (змейка) ----------
vector<int> mo_order(const vector<int>& L, const vector<int>& R, int B, bool snake = true) {
    vector<int> id(L.size()); iota(id.begin(), id.end(), 0);
    sort(id.begin(), id.end(), [&](int i, int j) {
        int bi = L[i] / B, bj = L[j] / B;
        if (bi != bj) return bi < bj;
        return (snake && bi % 2) ? R[i] > R[j] : R[i] < R[j];
    });
    return id;
}

// ---------- 6. Мультимножество с mex: добавление и удаление за O(1), mex за O(sqrt V) ----------
struct MexSet {
    int V, B; vector<int> cnt, zeros;               // zeros[b] — сколько значений в блоке b отсутствуют
    MexSet(int V) : V(V), B(isqrt_ceil(V)), cnt(V, 0), zeros((V + B - 1) / B, 0) { for (int v = 0; v < V; v++) zeros[v / B]++; }
    void add(int x) { if (x < V && cnt[x]++ == 0) zeros[x / B]--; }
    void rem(int x) { if (x < V && --cnt[x] == 0) zeros[x / B]++; }
    int mex() const {
        int b = 0;
        while (b < (int)zeros.size() && zeros[b] == 0) b++;      // первый блок, где есть «дырка»
        if (b == (int)zeros.size()) return V;
        int v = b * B; while (cnt[v]) v++;                       // внутри блока ищем честно
        return v;
    }
};

// mex на отрезках [l, r] (включительно) алгоритмом Мо
vector<int> mo_mex(const vector<int>& a, const vector<pair<int, int>>& qs) {
    int n = a.size(), q = qs.size();
    vector<int> L(q), R(q);
    for (int i = 0; i < q; i++) { L[i] = qs[i].first; R[i] = qs[i].second; }
    MexSet ms(n + 1);
    vector<int> ans(q), ord = mo_order(L, R, isqrt_ceil(n));
    int l = 0, r = -1;                                           // текущий отрезок [l, r], пока пустой
    for (int i : ord) {
        while (l > L[i]) ms.add(a[--l]);                         // сначала расширяем...
        while (r < R[i]) ms.add(a[++r]);
        while (l < L[i]) ms.rem(a[l++]);                         // ...потом сужаем
        while (r > R[i]) ms.rem(a[r--]);
        ans[i] = ms.mex();
    }
    return ans;
}

// ---------- 7. Дерево: порядки обхода и LCA ----------
struct Tree {
    int n, LOG; vector<vector<int>> adj, up; vector<int> par, dep, tin, out, e_in, e_out, ord2;
    Tree(int n) : n(n), adj(n) {}
    void edge(int a, int b) { adj[a].push_back(b); adj[b].push_back(a); }
    void build(int root = 0) {
        par.assign(n, root); dep.assign(n, 0); tin.assign(n, 0); out.assign(n, 0); e_in.assign(n, 0); e_out.assign(n, 0); ord2.clear();
        int timer = 0;
        vector<pair<int, int>> st{{root, 0}};
        tin[root] = timer++; e_in[root] = ord2.size(); ord2.push_back(root);
        while (!st.empty()) {
            int v = st.back().first, i = st.back().second;
            if (i < (int)adj[v].size()) {
                st.back().second++;
                int u = adj[v][i];
                if (u == par[v] && v != root) continue;
                if (v == root && u == root) continue;
                par[u] = v; dep[u] = dep[v] + 1; tin[u] = timer++; e_in[u] = ord2.size(); ord2.push_back(u);
                st.push_back({u, 0});
            } else {
                out[v] = timer; e_out[v] = ord2.size(); ord2.push_back(v);   // вершина записана второй раз — при выходе
                st.pop_back();
            }
        }
        LOG = 1; while ((1 << LOG) < n) LOG++;
        up.assign(LOG, par);
        for (int k = 1; k < LOG; k++) for (int v = 0; v < n; v++) up[k][v] = up[k - 1][up[k - 1][v]];
    }
    int lca(int a, int b) const {
        if (dep[a] < dep[b]) swap(a, b);
        for (int k = LOG - 1; k >= 0; k--) if (dep[a] - (1 << k) >= dep[b]) a = up[k][a];
        if (a == b) return a;
        for (int k = LOG - 1; k >= 0; k--) if (up[k][a] != up[k][b]) { a = up[k][a]; b = up[k][b]; }
        return par[a];
    }
    int dist(int a, int b) const { return dep[a] + dep[b] - 2 * dep[lca(a, b)]; }
};

// mex значений на путях дерева: Мо по эйлерову обходу длины 2n, вершины, встретившиеся дважды, «гасят» друг друга
vector<int> tree_mex(const Tree& T, const vector<int>& val, const vector<pair<int, int>>& qs) {
    int n = T.n, q = qs.size();
    vector<int> L(q), R(q), extra(q, -1);
    for (int i = 0; i < q; i++) {
        int u = qs[i].first, v = qs[i].second;
        if (T.e_in[u] > T.e_in[v]) swap(u, v);
        int w = T.lca(u, v);
        if (w == u) { L[i] = T.e_in[u]; R[i] = T.e_in[v]; }
        else { L[i] = T.e_out[u]; R[i] = T.e_in[v]; extra[i] = w; }   // LCA в отрезок не попадает — добавим отдельно
    }
    MexSet ms(n + 1); vector<char> in(n, 0);
    auto flip = [&](int pos) { int v = T.ord2[pos]; if (in[v] ^= 1) ms.add(val[v]); else ms.rem(val[v]); };
    vector<int> ans(q), ord = mo_order(L, R, isqrt_ceil(2 * n));
    int l = 0, r = -1;
    for (int i : ord) {
        while (l > L[i]) flip(--l);
        while (r < R[i]) flip(++r);
        while (l < L[i]) flip(l++);
        while (r > R[i]) flip(r--);
        if (extra[i] >= 0) ms.add(val[extra[i]]);
        ans[i] = ms.mex();
        if (extra[i] >= 0) ms.rem(val[extra[i]]);
    }
    return ans;
}

// ---------- 8. Трёхмерный Мо: mex на отрезке с точечными изменениями ----------
struct Upd { int pos, val; };
vector<int> mo_mex_updates(vector<int> a, const vector<Upd>& upd, const vector<array<int, 3>>& qs /* l, r, сколько изменений уже применено */) {
    int n = a.size(), q = qs.size();
    vector<int> oldv(upd.size()); { vector<int> b = a; for (size_t k = 0; k < upd.size(); k++) { oldv[k] = b[upd[k].pos]; b[upd[k].pos] = upd[k].val; } }
    int B = max(1, (int)cbrt((double)n * n));                      // блок ~ n^(2/3)
    vector<int> id(q); iota(id.begin(), id.end(), 0);
    sort(id.begin(), id.end(), [&](int i, int j) {
        const auto &x = qs[i], &y = qs[j];
        if (x[0] / B != y[0] / B) return x[0] / B < y[0] / B;
        if (x[1] / B != y[1] / B) return x[1] / B < y[1] / B;
        return x[2] < y[2];
    });
    MexSet ms(n + 1); int l = 0, r = -1, t = 0; vector<int> ans(q);
    auto apply = [&](int k, bool forward) {
        int p = upd[k].pos, nv = forward ? upd[k].val : oldv[k], ov = forward ? oldv[k] : upd[k].val;
        if (l <= p && p <= r) { ms.rem(ov); ms.add(nv); }
        a[p] = nv;
    };
    for (int i : id) {
        int L = qs[i][0], R = qs[i][1], T = qs[i][2];
        while (l > L) ms.add(a[--l]);
        while (r < R) ms.add(a[++r]);
        while (l < L) ms.rem(a[l++]);
        while (r > R) ms.rem(a[r--]);
        while (t < T) apply(t++, true);
        while (t > T) apply(--t, false);
        ans[i] = ms.mex();
    }
    return ans;
}

// ---------- 9. Мо: сумма (y - x) по парам равных элементов x < y на отрезке ----------
vector<ll> mo_equal_pairs(vector<int> a, const vector<pair<int, int>>& qs) {
    int n = a.size(), q = qs.size();
    { vector<int> s = a; sort(s.begin(), s.end()); s.erase(unique(s.begin(), s.end()), s.end());
      for (int& x : a) x = lower_bound(s.begin(), s.end(), x) - s.begin(); }
    vector<ll> cnt(n, 0), sumIdx(n, 0), res(q); ll cur = 0;
    auto add_right = [&](int p) { int v = a[p]; cur += cnt[v] * p - sumIdx[v]; cnt[v]++; sumIdx[v] += p; };   // новый индекс — самый большой
    auto add_left  = [&](int p) { int v = a[p]; cur += sumIdx[v] - cnt[v] * p; cnt[v]++; sumIdx[v] += p; };   // новый индекс — самый маленький
    auto rem_right = [&](int p) { int v = a[p]; cnt[v]--; sumIdx[v] -= p; cur -= cnt[v] * p - sumIdx[v]; };
    auto rem_left  = [&](int p) { int v = a[p]; cnt[v]--; sumIdx[v] -= p; cur -= sumIdx[v] - cnt[v] * p; };
    vector<int> L(q), R(q);
    for (int i = 0; i < q; i++) { L[i] = qs[i].first; R[i] = qs[i].second; }
    int l = 0, r = -1;
    for (int i : mo_order(L, R, isqrt_ceil(n))) {
        while (l > L[i]) add_left(--l);
        while (r < R[i]) add_right(++r);
        while (l < L[i]) rem_left(l++);
        while (r > R[i]) rem_right(r--);
        res[i] = cur;
    }
    return res;
}

// ---------- 10. Тяжёлые и лёгкие вершины: треугольники в графе ----------
// (a) делим вершины на лёгкие (deg <= B) и тяжёлые; тяжёлых не больше 2m / B
ll triangles_heavy_light(int n, const vector<pair<int, int>>& edges) {
    int m = edges.size(), B = isqrt_ceil(2LL * m);
    vector<vector<int>> adj(n);
    for (auto [u, v] : edges) { adj[u].push_back(v); adj[v].push_back(u); }
    vector<char> heavy(n); for (int v = 0; v < n; v++) heavy[v] = (int)adj[v].size() > B;
    ll c[4] = {0, 0, 0, 0}; vector<char> mark(n, 0);
    for (int v = 0; v < n; v++) {
        for (int x : adj[v]) mark[x] = 1;                        // строка матрицы смежности для v
        for (int u : adj[v]) if (!heavy[u])                      // лёгкий сосед u: у него не больше B соседей
            for (int w : adj[u]) if (mark[w]) c[!heavy[v] + !heavy[u] + !heavy[w]]++;
        for (int x : adj[v]) mark[x] = 0;
    }
    // тройка (v; лёгкий u; w) встречается 2k раз у треугольника с k лёгкими вершинами
    ll ans = c[1] / 2 + c[2] / 4 + c[3] / 6;
    vector<int> hv, hid(n, -1);
    for (int v = 0; v < n; v++) if (heavy[v]) { hid[v] = hv.size(); hv.push_back(v); }
    int h = hv.size(); vector<vector<char>> g(h, vector<char>(h, 0));
    for (auto [u, v] : edges) if (heavy[u] && heavy[v]) g[hid[u]][hid[v]] = g[hid[v]][hid[u]] = 1;
    for (int i = 0; i < h; i++) for (int j = i + 1; j < h; j++) if (g[i][j])
        for (int k = j + 1; k < h; k++) ans += g[i][k] && g[j][k];
    return ans;
}
// (b) ориентируем каждое ребро от меньшей степени к большей: исходящая степень <= sqrt(2m)
ll triangles_oriented(int n, const vector<pair<int, int>>& edges) {
    vector<int> deg(n, 0); for (auto [u, v] : edges) deg[u]++, deg[v]++;
    auto less_ = [&](int a, int b) { return make_pair(deg[a], a) < make_pair(deg[b], b); };
    vector<vector<int>> out(n);
    for (auto [u, v] : edges) { if (less_(u, v)) out[u].push_back(v); else out[v].push_back(u); }
    ll ans = 0; vector<char> mark(n, 0);
    for (int u = 0; u < n; u++) {
        for (int v : out[u]) mark[v] = 1;
        for (int v : out[u]) for (int w : out[v]) ans += mark[w];
        for (int v : out[u]) mark[v] = 0;
    }
    return ans;
}

// ---------- 11. Тяжёлые и лёгкие: «+= x всем соседям» и «значение в вершине» ----------
struct NeighborAdd {
    int n, B; vector<vector<int>> adj; vector<ll> val, pend; vector<int> hv, hid; vector<vector<char>> adjH;
    NeighborAdd(int n, const vector<pair<int, int>>& edges) : n(n), adj(n), val(n, 0), hid(n, -1) {
        for (auto [u, v] : edges) { adj[u].push_back(v); adj[v].push_back(u); }
        B = isqrt_ceil(2LL * edges.size());
        for (int v = 0; v < n; v++) if ((int)adj[v].size() > B) { hid[v] = hv.size(); hv.push_back(v); }
        pend.assign(hv.size(), 0); adjH.assign(hv.size(), vector<char>(n, 0));
        for (size_t h = 0; h < hv.size(); h++) for (int u : adj[hv[h]]) adjH[h][u] = 1;   // матрица «тяжёлая × все»: корень × n
    }
    void add_neighbors(int v, ll x) {
        if (hid[v] < 0) { for (int u : adj[v]) val[u] += x; }     // лёгкая: пройти по <= B соседям
        else pend[hid[v]] += x;                                   // тяжёлая: только записать отложенную добавку
    }
    ll get(int u) { ll r = val[u]; for (size_t h = 0; h < hv.size(); h++) if (adjH[h][u]) r += pend[h]; return r; }
};

// ---------- 12. Прыжки: число путей из клетки 0 (a[i] >= 1), ответ — сумма dp ----------
ll jump_paths(const vector<int>& a, ll mod) {
    int n = a.size(), B = isqrt_ceil(n);
    vector<ll> dp(n, 0); dp[0] = 1;
    vector<vector<ll>> f(B);                                      // f[l][r] — сумма dp[j] по j с a[j] = l, j % l = r
    for (int l = 1; l < B; l++) f[l].assign(l, 0);
    ll ans = 0;
    for (int i = 0; i < n; i++) {
        for (int l = 1; l < B; l++) dp[i] = (dp[i] + f[l][i % l]) % mod;   // малые прыжки «назад»
        ans = (ans + dp[i]) % mod;
        if (a[i] >= B) { for (int j = i + a[i]; j < n; j += a[i]) dp[j] = (dp[j] + dp[i]) % mod; }   // большие — вперёд честно
        else f[a[i]][i % a[i]] = (f[a[i]][i % a[i]] + dp[i]) % mod;
    }
    return ans;
}

// ---------- 13. Строки: сумма w_j * (число различающихся позиций) по строкам той же длины ----------
struct HammingWeights {
    vector<string> s; vector<ll> w; int B;
    map<int, vector<int>> group;                  // длина -> номера тяжёлых строк
    map<int, vector<vector<int>>> dist;           // длина -> матрица попарных расстояний (только тяжёлые длины)
    vector<int> pos;                              // номер строки внутри своей группы
    map<int, vector<ll>> C, D;                    // лёгкие длины: C[L][p*26+c] и D[L][p]
    HammingWeights(const vector<string>& str, const vector<ll>& weight) : s(str), w(weight), pos(str.size(), -1) {
        ll N = 0; for (auto& x : s) N += x.size();
        B = isqrt_ceil(N);
        for (size_t i = 0; i < s.size(); i++) {
            int L = s[i].size();
            if (L > B) { pos[i] = group[L].size(); group[L].push_back(i); }
            else {
                if (!C.count(L)) { C[L].assign(L * 26, 0); D[L].assign(L, 0); }
                for (int p = 0; p < L; p++) { C[L][p * 26 + s[i][p] - 'a'] += w[i]; D[L][p] += w[i]; }
            }
        }
        for (auto& [L, g] : group) {                   // тяжёлых строк мало, так что матрица небольшая
            dist[L].assign(g.size(), vector<int>(g.size(), 0));
            for (size_t i = 0; i < g.size(); i++) for (size_t j = 0; j < g.size(); j++)
                for (int p = 0; p < L; p++) dist[L][i][j] += s[g[i]][p] != s[g[j]][p];
        }
    }
    void update(int i, ll nw) {
        int L = s[i].size();
        if (L <= B) for (int p = 0; p < L; p++) { C[L][p * 26 + s[i][p] - 'a'] += nw - w[i]; D[L][p] += nw - w[i]; }
        w[i] = nw;
    }
    ll query(int i) {
        int L = s[i].size(); ll r = 0;
        if (L > B) { auto& g = group[L]; for (size_t j = 0; j < g.size(); j++) r += w[g[j]] * dist[L][pos[i]][j]; }
        else for (int p = 0; p < L; p++) r += D[L][p] - C[L][p * 26 + s[i][p] - 'a'];
        return r;
    }
};

// ---------- 14. Корневая по запросам: связность в оффлайне ----------
struct DSU {
    vector<int> p; DSU(int n = 0) : p(n) { iota(p.begin(), p.end(), 0); }
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
    bool unite(int a, int b) { a = find(a); b = find(b); if (a == b) return false; p[a] = b; return true; }
};
struct ConnOp { int type, u, v; };            // 0 — добавить ребро, 1 — удалить ребро, 2 — «лежат ли u и v в одной компоненте»
vector<char> offline_connectivity(int n, const vector<ConnOp>& ops, int B) {
    set<pair<int, int>> cur; vector<char> ans;
    auto norm = [](int u, int v) { return make_pair(min(u, v), max(u, v)); };
    vector<vector<int>> g(n); vector<int> stamp(n, -1); int cs = 0;
    for (int s = 0; s < (int)ops.size(); s += B) {
        int e = min((int)ops.size(), s + B);
        set<pair<int, int>> touched;
        for (int i = s; i < e; i++) if (ops[i].type != 2) touched.insert(norm(ops[i].u, ops[i].v));
        DSU d(n);
        for (auto& ed : cur) if (!touched.count(ed)) d.unite(ed.first, ed.second);     // «прибитые гвоздями» рёбра
        vector<int> comp(n); for (int v = 0; v < n; v++) comp[v] = d.find(v);
        vector<pair<int, int>> fl;                                                   // плавающие рёбра, живые сейчас
        for (auto& ed : touched) if (cur.count(ed)) fl.push_back(ed);
        for (int i = s; i < e; i++) {
            auto ed = norm(ops[i].u, ops[i].v);
            if (ops[i].type == 0) { cur.insert(ed); fl.push_back(ed); }
            else if (ops[i].type == 1) { cur.erase(ed); fl.erase(find(fl.begin(), fl.end(), ed)); }
            else {
                for (auto& f : fl) { int a = comp[f.first], b = comp[f.second]; g[a].push_back(b); g[b].push_back(a); }
                int src = comp[ops[i].u], dst = comp[ops[i].v]; cs++;
                vector<int> st{src}; stamp[src] = cs;
                while (!st.empty()) { int x = st.back(); st.pop_back(); for (int y : g[x]) if (stamp[y] != cs) { stamp[y] = cs; st.push_back(y); } }
                ans.push_back(stamp[dst] == cs);
                for (auto& f : fl) { g[comp[f.first]].clear(); g[comp[f.second]].clear(); }
            }
        }
    }
    return ans;
}

// ---------- 15. Корневая по запросам: расстояние до ближайшей чёрной клетки ----------
// тип 0 — покрасить в чёрный, 1 — вернуть белый, 2 — спросить; -1, если чёрных клеток нет
vector<int> grid_nearest(int n, int m, const vector<array<int, 3>>& ops, int B) {
    vector<char> black(n * m, 0); vector<int> ans; const int INF = 1e9;
    for (int s = 0; s < (int)ops.size(); s += B) {
        int e = min((int)ops.size(), s + B);
        vector<char> touched(n * m, 0); vector<int> cells;
        for (int i = s; i < e; i++) if (ops[i][0] != 2) { int c = ops[i][1] * m + ops[i][2]; if (!touched[c]) { touched[c] = 1; cells.push_back(c); } }
        vector<int> dist(n * m, INF); queue<int> q;
        for (int c = 0; c < n * m; c++) if (black[c] && !touched[c]) { dist[c] = 0; q.push(c); }      // мультиBFS из «прибитых» чёрных
        while (!q.empty()) {
            int c = q.front(); q.pop(); int x = c / m, y = c % m;
            const int dx[4] = {1, -1, 0, 0}, dy[4] = {0, 0, 1, -1};
            for (int k = 0; k < 4; k++) {
                int nx = x + dx[k], ny = y + dy[k];
                if (nx < 0 || ny < 0 || nx >= n || ny >= m || dist[nx * m + ny] != INF) continue;
                dist[nx * m + ny] = dist[c] + 1; q.push(nx * m + ny);
            }
        }
        for (int i = s; i < e; i++) {
            int c = ops[i][1] * m + ops[i][2];
            if (ops[i][0] == 0) black[c] = 1;
            else if (ops[i][0] == 1) black[c] = 0;
            else {
                int best = dist[c];
                for (int f : cells) if (black[f]) best = min(best, abs(f / m - ops[i][1]) + abs(f % m - ops[i][2]));   // плавающие — в лоб
                ans.push_back(best >= INF ? -1 : best);
            }
        }
    }
    return ans;
}

// ---------- 16. Корневая по запросам: вес минимального остова при добавлении и удалении рёбер ----------
struct MstOp { int type, id, u, v; ll w; };    // 0 — добавить ребро id, 1 — удалить ребро id, 2 — спросить вес остова (-1, если граф несвязен)
struct MEdge { int id, u, v; ll w; };
vector<ll> offline_mst(int n, const vector<MstOp>& ops, int B) {
    map<int, MEdge> cur; vector<ll> ans;
    auto cmp = [](const MEdge& a, const MEdge& b) { return make_pair(a.w, a.id) < make_pair(b.w, b.id); };
    for (int s = 0; s < (int)ops.size(); s += B) {
        int e = min((int)ops.size(), s + B);
        set<int> touched; vector<MEdge> all;
        for (auto& kv : cur) all.push_back(kv.second);
        for (int i = s; i < e; i++) if (ops[i].type != 2) {
            touched.insert(ops[i].id);
            if (ops[i].type == 0) all.push_back({ops[i].id, ops[i].u, ops[i].v, ops[i].w});
        }
        sort(all.begin(), all.end(), cmp);
        // шаг А: остов на всех рёбрах, живых хоть когда-то в блоке; неплавающие рёбра остова лежат в остове всегда
        DSU d(n); vector<MEdge> forced; ll wForced = 0; int comps = n;
        for (auto& ed : all) if (d.unite(ed.u, ed.v)) { comps--; if (!touched.count(ed.id)) { forced.push_back(ed); wForced += ed.w; } }
        bool spanning = comps == 1;
        vector<MEdge> cand; vector<int> cid(n); int C = 0;
        if (spanning) {
            DSU d2(n); for (auto& ed : forced) d2.unite(ed.u, ed.v);        // сжимаем граф по ним
            vector<int> label(n, -1);
            for (int v = 0; v < n; v++) { int r = d2.find(v); if (label[r] < 0) label[r] = C++; cid[v] = label[r]; }
            // шаг Б: из остальных неплавающих рёбер оставляем только те, что нужны остову сжатого графа
            DSU d3(C);
            for (auto& ed : all) if (!touched.count(ed.id) && d3.unite(cid[ed.u], cid[ed.v])) cand.push_back(ed);
        }
        set<int> alive;                                                      // плавающие рёбра, живые прямо сейчас
        for (int id : touched) if (cur.count(id)) alive.insert(id);
        map<int, MEdge> fl; for (int i = s; i < e; i++) if (ops[i].type == 0) fl[ops[i].id] = {ops[i].id, ops[i].u, ops[i].v, ops[i].w};
        for (int id : alive) fl[id] = cur[id];
        for (int i = s; i < e; i++) {
            if (ops[i].type == 0) { cur[ops[i].id] = fl[ops[i].id]; alive.insert(ops[i].id); }
            else if (ops[i].type == 1) { cur.erase(ops[i].id); alive.erase(ops[i].id); }
            else {
                if (!spanning) { ans.push_back(-1); continue; }
                vector<MEdge> es = cand; for (int id : alive) es.push_back(fl[id]);
                sort(es.begin(), es.end(), cmp);                              // не больше 2B рёбер на запрос
                DSU dq(C); ll tot = wForced; int cc = C;
                for (auto& ed : es) if (dq.unite(cid[ed.u], cid[ed.v])) { tot += ed.w; cc--; }
                ans.push_back(cc == 1 ? tot : -1);
            }
        }
    }
    return ans;
}

// ---------- 17. Все различные значения floor(x / i) ----------
vector<array<ll, 3>> floor_blocks(ll x) {                  // {значение k, i от, i до}
    vector<array<ll, 3>> r;
    for (ll i = 1; i <= x;) { ll k = x / i, j = x / k; r.push_back({k, i, j}); i = j + 1; }   // следующий i — это x/k + 1
    return r;
}

// ---------- 18. Максимум на отрезках в оффлайне: стек максимумов + СНМ ----------
vector<ll> offline_range_max(const vector<ll>& a, const vector<pair<int, int>>& qs) {    // отрезки [l, r] включительно
    int n = a.size(); vector<vector<pair<int, int>>> byR(n);
    for (int i = 0; i < (int)qs.size(); i++) byR[qs[i].second].push_back({qs[i].first, i});
    vector<int> par(n), st; iota(par.begin(), par.end(), 0);
    function<int(int)> find = [&](int x) { while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; } return x; };
    vector<ll> ans(qs.size());
    for (int i = 0; i < n; i++) {
        while (!st.empty() && a[st.back()] <= a[i]) { par[st.back()] = i; st.pop_back(); }   // вытесненный элемент «приклеивается» к вытеснившему
        st.push_back(i);
        for (auto [l, id] : byR[i]) ans[id] = a[find(l)];      // корень l — позиция максимума на [l, i]
    }
    return ans;
}

// ---------- 19. Сжатое (виртуальное) дерево ----------
void build_virtual(const Tree& T, vector<int> v, vector<int>& nodes, vector<int>& pidx) {
    auto byTin = [&](int a, int b) { return T.tin[a] < T.tin[b]; };
    sort(v.begin(), v.end(), byTin); v.erase(unique(v.begin(), v.end()), v.end());
    int k = v.size();
    for (int i = 0; i + 1 < k; i++) v.push_back(T.lca(v[i], v[i + 1]));
    sort(v.begin(), v.end(), byTin); v.erase(unique(v.begin(), v.end()), v.end());
    nodes = v; pidx.assign(v.size(), -1);
    for (size_t i = 1; i < v.size(); i++) {
        int p = T.lca(v[i - 1], v[i]);                          // родитель в сжатом дереве
        pidx[i] = lower_bound(v.begin(), v.end(), p, byTin) - v.begin();
    }
}
ll sum_pair_dist(const Tree& T, vector<int> v) {              // сумма расстояний по всем парам различных вершин
    sort(v.begin(), v.end()); v.erase(unique(v.begin(), v.end()), v.end());
    int k = v.size(); vector<int> nodes, pidx; build_virtual(T, v, nodes, pidx);
    vector<ll> cnt(nodes.size(), 0);
    for (int x : v) cnt[lower_bound(nodes.begin(), nodes.end(), x, [&](int a, int b) { return T.tin[a] < T.tin[b]; }) - nodes.begin()] = 1;
    ll ans = 0;
    for (int i = nodes.size() - 1; i >= 1; i--) {                // дети всегда имеют больший tin, чем родитель
        ans += (ll)(T.dep[nodes[i]] - T.dep[nodes[pidx[i]]]) * cnt[i] * (k - cnt[i]);
        cnt[pidx[i]] += cnt[i];
    }
    return ans;
}
int steiner_size(const Tree& T, const vector<int>& v) {      // сколько вершин в наименьшем поддереве, содержащем все v
    vector<int> nodes, pidx; build_virtual(T, v, nodes, pidx);
    int r = 1;
    for (size_t i = 1; i < nodes.size(); i++) r += T.dep[nodes[i]] - T.dep[nodes[pidx[i]]];
    return r;
}

// ---------- 20. Два дерева: пары (v, u), где v — предок u в обоих ----------
struct Fen {
    vector<int> t; Fen(int n) : t(n + 1, 0) {}
    void add(int i, int d) { for (i++; i < (int)t.size(); i += i & -i) t[i] += d; }
    int pre(int i) { int s = 0; for (; i > 0; i -= i & -i) s += t[i]; return s; }       // сумма по [0, i)
    int sum(int l, int r) { return pre(r) - pre(l); }
};
ll common_ancestor_pairs(const Tree& A, const Tree& Bt) {
    int n = A.n; Fen f(n); ll ans = 0;
    vector<int> before(n);
    vector<pair<int, int>> st{{0, 0}};
    before[0] = f.sum(A.tin[0], A.out[0]);
    while (!st.empty()) {
        int v = st.back().first, i = st.back().second;
        if (i < (int)Bt.adj[v].size()) {
            st.back().second++;
            int u = Bt.adj[v][i];
            if (u == Bt.par[v] && v != 0) continue;
            before[u] = f.sum(A.tin[u], A.out[u]);               // «красное»: что уже было в поддереве u первого дерева
            st.push_back({u, 0});
        } else {
            ans += f.sum(A.tin[v], A.out[v]) - before[v];        // «зелёное»: добавилось, пока мы были внутри v
            f.add(A.tin[v], 1);
            st.pop_back();
        }
    }
    return ans;
}

// ---------- 21. Дерево отрезков с присвоением и маской цветов (до 60 цветов) ----------
struct ColorTree {
    int n; vector<ll> mask; vector<int> lz;
    ColorTree(const vector<int>& c) : n(c.size()), mask(4 * c.size(), 0), lz(4 * c.size(), -1) { build(1, 0, n, c); }
    void build(int v, int l, int r, const vector<int>& c) {
        if (r - l == 1) { mask[v] = 1LL << c[l]; return; }
        int m = (l + r) / 2; build(2 * v, l, m, c); build(2 * v + 1, m, r, c); mask[v] = mask[2 * v] | mask[2 * v + 1];
    }
    void apply(int v, int col) { mask[v] = 1LL << col; lz[v] = col; }
    void push(int v) { if (lz[v] >= 0) { apply(2 * v, lz[v]); apply(2 * v + 1, lz[v]); lz[v] = -1; } }
    void assign(int v, int l, int r, int ql, int qr, int col) {
        if (qr <= l || r <= ql) return;
        if (ql <= l && r <= qr) { apply(v, col); return; }
        push(v); int m = (l + r) / 2;
        assign(2 * v, l, m, ql, qr, col); assign(2 * v + 1, m, r, ql, qr, col);
        mask[v] = mask[2 * v] | mask[2 * v + 1];
    }
    ll get(int v, int l, int r, int ql, int qr) {
        if (qr <= l || r <= ql) return 0;
        if (ql <= l && r <= qr) return mask[v];
        push(v); int m = (l + r) / 2;
        return get(2 * v, l, m, ql, qr) | get(2 * v + 1, m, r, ql, qr);
    }
    void recolor(int l, int r, int col) { assign(1, 0, n, l, r, col); }
    int distinct(int l, int r) { return __builtin_popcountll(get(1, 0, n, l, r)); }
};

#ifdef TEST_MAIN
static mt19937 rng(12345);
static int rnd(int a, int b) { return a + (int)(rng() % (b - a + 1)); }
static Tree random_tree(int n) { Tree t(n); for (int i = 1; i < n; i++) t.edge(rnd(0, i - 1), i); t.build(0); return t; }

int main() {
    // 1–3: блоки
    for (int it = 0; it < 300; it++) {
        int n = rnd(1, 40); vector<ll> a(n); for (auto& x : a) x = rnd(-20, 20);
        BlockSum bs(a); PrefixBlocks pb(a);
        int B = rnd(1, 8); SortedBlocks sb(a, B);
        vector<ll> b = a;
        for (int q = 0; q < 60; q++) {
            int t = rnd(0, 3), l = rnd(0, n - 1), r = rnd(l + 1, n);
            if (t == 0) { int i = rnd(0, n - 1); ll x = rnd(-20, 20); bs.assign(i, x); pb.add(i, x - b[i]); sb.add(i, i + 1, x - b[i]); b[i] = x; }
            else if (t == 1) { ll s = 0; for (int i = l; i < r; i++) s += b[i]; assert(bs.sum(l, r) == s); assert(pb.sum(l, r) == s); }
            else if (t == 2) { ll x = rnd(-20, 20); for (int i = l; i < r; i++) b[i] += x; sb.add(l, r, x); bs = BlockSum(b); pb = PrefixBlocks(b); }
            else { ll x = rnd(-30, 30); int c = 0; for (int i = l; i < r; i++) c += b[i] <= x; assert(sb.count_le(l, r, x) == c); }
        }
    }
    // 4: обход точек
    for (int it = 0; it < 20; it++) {
        int N = rnd(50, 400), n = N; vector<pair<int, int>> p(n); for (auto& q : p) q = {rnd(0, N), rnd(0, N)};
        int B = isqrt_ceil(N);
        auto o1 = strip_order(p, B, true), o2 = strip_order(p, B, false), o0 = strip_order(p, N + 1, false);
        assert(o1.size() == p.size() && set<int>(o1.begin(), o1.end()).size() == p.size());
        ll l1 = tour_length(p, o1), l2 = tour_length(p, o2);
        assert(l1 <= (ll)(N / B + 2) * N + (ll)n * B + 2 * N);
        assert(l2 <= 2LL * (N / B + 2) * N + (ll)n * B + 2 * N);
        (void)o0;
    }
    // 5–6: mex на отрезке
    for (int it = 0; it < 300; it++) {
        int n = rnd(1, 30); vector<int> a(n); int top = rnd(0, 6); for (auto& x : a) x = rnd(0, top);
        vector<pair<int, int>> qs; for (int i = 0; i < 40; i++) { int l = rnd(0, n - 1); qs.push_back({l, rnd(l, n - 1)}); }
        auto res = mo_mex(a, qs);
        for (size_t k = 0; k < qs.size(); k++) {
            set<int> s(a.begin() + qs[k].first, a.begin() + qs[k].second + 1); int m = 0; while (s.count(m)) m++;
            assert(res[k] == m);
        }
    }
    // 7: mex на путях дерева
    for (int it = 0; it < 300; it++) {
        int n = rnd(1, 25); Tree t = random_tree(n); vector<int> val(n); int top = rnd(0, 6); for (auto& x : val) x = rnd(0, top);
        vector<pair<int, int>> qs; for (int i = 0; i < 40; i++) qs.push_back({rnd(0, n - 1), rnd(0, n - 1)});
        auto res = tree_mex(t, val, qs);
        for (size_t k = 0; k < qs.size(); k++) {
            int u = qs[k].first, v = qs[k].second, w = t.lca(u, v); set<int> s;
            for (int x = u; x != w; x = t.par[x]) s.insert(val[x]);
            for (int x = v; x != w; x = t.par[x]) s.insert(val[x]);
            s.insert(val[w]); int m = 0; while (s.count(m)) m++;
            assert(res[k] == m);
        }
    }
    // 8: 3D Мо
    for (int it = 0; it < 300; it++) {
        int n = rnd(1, 25); vector<int> a(n); int top = rnd(0, 6); for (auto& x : a) x = rnd(0, top);
        vector<Upd> upd; int U = rnd(0, 10); for (int i = 0; i < U; i++) upd.push_back({rnd(0, n - 1), rnd(0, top + 1)});
        vector<array<int, 3>> qs; for (int i = 0; i < 40; i++) { int l = rnd(0, n - 1); qs.push_back({l, rnd(l, n - 1), rnd(0, U)}); }
        auto res = mo_mex_updates(a, upd, qs);
        for (size_t k = 0; k < qs.size(); k++) {
            vector<int> b = a; for (int j = 0; j < qs[k][2]; j++) b[upd[j].pos] = upd[j].val;
            set<int> s(b.begin() + qs[k][0], b.begin() + qs[k][1] + 1); int m = 0; while (s.count(m)) m++;
            assert(res[k] == m);
        }
    }
    // 9: пары равных
    for (int it = 0; it < 300; it++) {
        int n = rnd(1, 30); vector<int> a(n); int top = rnd(0, 5); for (auto& x : a) x = rnd(0, top) * 7 - 3;
        vector<pair<int, int>> qs; for (int i = 0; i < 40; i++) { int l = rnd(0, n - 1); qs.push_back({l, rnd(l, n - 1)}); }
        auto res = mo_equal_pairs(a, qs);
        for (size_t k = 0; k < qs.size(); k++) {
            ll s = 0; for (int x = qs[k].first; x <= qs[k].second; x++) for (int y = x + 1; y <= qs[k].second; y++) if (a[x] == a[y]) s += y - x;
            assert(res[k] == s);
        }
    }
    // 10–11: графы
    for (int it = 0; it < 300; it++) {
        int n = rnd(3, 14); vector<pair<int, int>> ed; vector<vector<char>> g(n, vector<char>(n, 0));
        int target = rnd(1, n * (n - 1) / 2);
        for (int i = 0; i < target; i++) { int u = rnd(0, n - 1), v = rnd(0, n - 1); if (u != v && !g[u][v]) { g[u][v] = g[v][u] = 1; ed.push_back({u, v}); } }
        ll br = 0; for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) for (int k = j + 1; k < n; k++) br += g[i][j] && g[j][k] && g[i][k];
        assert(triangles_heavy_light(n, ed) == br); assert(triangles_oriented(n, ed) == br);
        NeighborAdd na(n, ed); vector<ll> val(n, 0);
        for (int q = 0; q < 50; q++) {
            if (rnd(0, 1)) { int v = rnd(0, n - 1); ll x = rnd(-5, 5); na.add_neighbors(v, x); for (int u = 0; u < n; u++) if (g[v][u]) val[u] += x; }
            else { int u = rnd(0, n - 1); assert(na.get(u) == val[u]); }
        }
    }
    {   // тяжёлые вершины точно встречаются: звезда плюс лишние рёбра
        int n = 40; vector<pair<int, int>> ed; vector<vector<char>> g(n, vector<char>(n, 0));
        for (int i = 1; i < n; i++) { ed.push_back({0, i}); g[0][i] = g[i][0] = 1; }
        for (int i = 0; i < 30; i++) { int u = rnd(1, n - 1), v = rnd(1, n - 1); if (u != v && !g[u][v]) { g[u][v] = g[v][u] = 1; ed.push_back({u, v}); } }
        ll br = 0; for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) for (int k = j + 1; k < n; k++) br += g[i][j] && g[j][k] && g[i][k];
        assert(triangles_heavy_light(n, ed) == br); assert(triangles_oriented(n, ed) == br);
        NeighborAdd na(n, ed); assert(!na.hv.empty()); vector<ll> val(n, 0);
        for (int q = 0; q < 200; q++) {
            if (rnd(0, 1)) { int v = rnd(0, n - 1); ll x = rnd(-5, 5); na.add_neighbors(v, x); for (int u = 0; u < n; u++) if (g[v][u]) val[u] += x; }
            else { int u = rnd(0, n - 1); assert(na.get(u) == val[u]); }
        }
    }
    // 12: прыжки
    for (int it = 0; it < 300; it++) {
        int n = rnd(1, 60); vector<int> a(n); int top = rnd(1, 12); for (auto& x : a) x = rnd(1, top);
        const ll mod = 998244353; vector<ll> dp(n, 0); dp[0] = 1; ll s = 0;
        for (int i = 0; i < n; i++) { s = (s + dp[i]) % mod; for (int j = i + a[i]; j < n; j += a[i]) dp[j] = (dp[j] + dp[i]) % mod; }
        assert(jump_paths(a, mod) == s);
    }
    // 13: строки
    for (int it = 0; it < 200; it++) {
        int k = rnd(5, 14); vector<string> s(k); vector<ll> w(k);
        bool mixed = it % 2 == 0;                                  // в половине случаев — несколько длинных строк среди коротких
        for (int i = 0; i < k; i++) { int L = mixed ? (i < 4 ? 12 : rnd(1, 2)) : rnd(1, 3); for (int p = 0; p < L; p++) s[i] += 'a' + rnd(0, 2); w[i] = rnd(0, 9); }
        HammingWeights hw(s, w);
        if (mixed && k >= 5) assert(!hw.group.empty());           // тяжёлая ветка действительно проверяется
        for (int q = 0; q < 40; q++) {
            if (rnd(0, 1)) { int i = rnd(0, k - 1); ll nw = rnd(0, 9); hw.update(i, nw); w[i] = nw; }
            else {
                int i = rnd(0, k - 1); ll r = 0;
                for (int j = 0; j < k; j++) if (s[j].size() == s[i].size()) for (size_t p = 0; p < s[i].size(); p++) r += w[j] * (s[i][p] != s[j][p]);
                assert(hw.query(i) == r);
            }
        }
    }
    // 14: связность
    for (int it = 0; it < 200; it++) {
        int n = rnd(2, 10); vector<ConnOp> ops; set<pair<int, int>> cur; int Q = rnd(5, 60);
        for (int i = 0; i < Q; i++) {
            int u = rnd(0, n - 1), v = rnd(0, n - 1); if (u == v) { i--; continue; }
            auto e = make_pair(min(u, v), max(u, v)); int t = rnd(0, 2);
            if (t == 0 && !cur.count(e)) { cur.insert(e); ops.push_back({0, u, v}); }
            else if (t == 1 && cur.count(e)) { cur.erase(e); ops.push_back({1, u, v}); }
            else ops.push_back({2, u, v});
        }
        auto res = offline_connectivity(n, ops, rnd(1, 8));
        set<pair<int, int>> c2; size_t qi = 0;
        for (auto& op : ops) {
            auto e = make_pair(min(op.u, op.v), max(op.u, op.v));
            if (op.type == 0) c2.insert(e); else if (op.type == 1) c2.erase(e);
            else { DSU d(n); for (auto& x : c2) d.unite(x.first, x.second); assert((bool)res[qi++] == (d.find(op.u) == d.find(op.v))); }
        }
        assert(qi == res.size());
    }
    // 15: сетка
    for (int it = 0; it < 200; it++) {
        int n = rnd(1, 7), m = rnd(1, 7); vector<array<int, 3>> ops; int Q = rnd(5, 50);
        for (int i = 0; i < Q; i++) ops.push_back({rnd(0, 2), rnd(0, n - 1), rnd(0, m - 1)});
        auto res = grid_nearest(n, m, ops, rnd(1, 8));
        vector<vector<char>> bl(n, vector<char>(m, 0)); size_t qi = 0;
        for (auto& o : ops) {
            if (o[0] == 0) bl[o[1]][o[2]] = 1; else if (o[0] == 1) bl[o[1]][o[2]] = 0;
            else { int best = -1; for (int x = 0; x < n; x++) for (int y = 0; y < m; y++) if (bl[x][y]) { int d = abs(x - o[1]) + abs(y - o[2]); if (best < 0 || d < best) best = d; } assert(res[qi++] == best); }
        }
    }
    // 16: остов
    for (int it = 0; it < 300; it++) {
        int n = rnd(2, 8); vector<MstOp> ops; map<int, MEdge> cur; int nextId = 0, Q = rnd(5, 60);
        for (int i = 0; i < Q; i++) {
            int t = rnd(0, 2);
            if (t == 0) { int u = rnd(0, n - 1), v = rnd(0, n - 1); if (u == v) { i--; continue; } ll w = rnd(1, 6); ops.push_back({0, nextId, u, v, w}); cur[nextId] = {nextId, u, v, w}; nextId++; }
            else if (t == 1 && !cur.empty()) { auto itx = cur.begin(); advance(itx, rnd(0, cur.size() - 1)); ops.push_back({1, itx->first, 0, 0, 0}); cur.erase(itx); }
            else ops.push_back({2, 0, 0, 0, 0});
        }
        auto res = offline_mst(n, ops, rnd(1, 8));
        map<int, MEdge> c2; size_t qi = 0;
        for (auto& op : ops) {
            if (op.type == 0) c2[op.id] = {op.id, op.u, op.v, op.w}; else if (op.type == 1) c2.erase(op.id);
            else {
                vector<MEdge> es; for (auto& kv : c2) es.push_back(kv.second);
                sort(es.begin(), es.end(), [](const MEdge& a, const MEdge& b) { return make_pair(a.w, a.id) < make_pair(b.w, b.id); });
                DSU d(n); ll tot = 0; int cc = n; for (auto& e : es) if (d.unite(e.u, e.v)) { tot += e.w; cc--; }
                assert(res[qi++] == (cc == 1 ? tot : -1));
            }
        }
    }
    // 17: floor(x / i)
    for (ll x : {1LL, 2LL, 10LL, 99LL, 100LL, 12345LL, 1000000007LL}) {
        auto bl = floor_blocks(x); assert((ll)bl.size() <= 2 * (ll)sqrt((double)x) + 2);
        ll next = 1; for (auto& b : bl) { assert(b[1] == next); assert(x / b[1] == b[0] && x / b[2] == b[0]); next = b[2] + 1; }
        assert(next == x + 1);
    }
    // 18: максимум на отрезках
    for (int it = 0; it < 300; it++) {
        int n = rnd(1, 30); vector<ll> a(n); for (auto& x : a) x = rnd(-5, 5);
        vector<pair<int, int>> qs; for (int i = 0; i < 40; i++) { int l = rnd(0, n - 1); qs.push_back({l, rnd(l, n - 1)}); }
        auto res = offline_range_max(a, qs);
        for (size_t k = 0; k < qs.size(); k++) assert(res[k] == *max_element(a.begin() + qs[k].first, a.begin() + qs[k].second + 1));
    }
    // 19: сжатое дерево
    for (int it = 0; it < 300; it++) {
        int n = rnd(1, 20); Tree t = random_tree(n); vector<int> v; int k = rnd(1, n); for (int i = 0; i < k; i++) v.push_back(rnd(0, n - 1));
        vector<int> d = v; sort(d.begin(), d.end()); d.erase(unique(d.begin(), d.end()), d.end());
        ll s = 0; for (size_t i = 0; i < d.size(); i++) for (size_t j = i + 1; j < d.size(); j++) s += t.dist(d[i], d[j]);
        assert(sum_pair_dist(t, v) == s);
        vector<int> deg(n, 0); vector<char> keep(n, 1);
        for (int x = 0; x < n; x++) deg[x] = t.adj[x].size();
        set<int> need(d.begin(), d.end());
        for (bool ch = true; ch;) { ch = false; for (int x = 0; x < n; x++) if (keep[x] && deg[x] <= 1 && !need.count(x) && n > 1) { keep[x] = 0; for (int y : t.adj[x]) if (keep[y]) deg[y]--; ch = true; } }
        assert(steiner_size(t, v) == accumulate(keep.begin(), keep.end(), 0));
    }
    // 20: два дерева
    for (int it = 0; it < 300; it++) {
        int n = rnd(1, 20); Tree A = random_tree(n), Bt = random_tree(n); ll s = 0;
        auto anc = [&](const Tree& T, int v, int u) { return T.tin[v] <= T.tin[u] && T.tin[u] < T.out[v]; };
        for (int v = 0; v < n; v++) for (int u = 0; u < n; u++) if (v != u && anc(A, v, u) && anc(Bt, v, u)) s++;
        assert(common_ancestor_pairs(A, Bt) == s);
    }
    // 21: цвета на поддеревьях
    for (int it = 0; it < 300; it++) {
        int n = rnd(1, 25); vector<int> c(n); for (auto& x : c) x = rnd(0, 59);
        ColorTree ct(c);
        for (int q = 0; q < 50; q++) {
            int l = rnd(0, n - 1), r = rnd(l + 1, n);
            if (rnd(0, 1)) { int col = rnd(0, 59); ct.recolor(l, r, col); for (int i = l; i < r; i++) c[i] = col; }
            else { set<int> s(c.begin() + l, c.begin() + r); assert(ct.distinct(l, r) == (int)s.size()); }
        }
    }
    puts("ok");
}
#endif
