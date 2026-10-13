#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const ll INF = LLONG_MAX / 4;
struct E { int a, b; ll w; };

// Форд–Беллман: n-1 проходов по всем рёбрам; возвращает true, если достижимый из s отрицательный цикл
bool ford(int n, const vector<E>& e, int s, vector<ll>& d) {
    d.assign(n, INF); d[s] = 0;
    for (int it = 0; it < n; it++) {
        bool ch = false;
        for (auto& x : e)
            if (d[x.a] < INF && d[x.b] > d[x.a] + x.w) { d[x.b] = d[x.a] + x.w; ch = true; }
        if (!ch) return false;               // ничего не изменилось — дальше тоже не изменится
        if (it == n - 1) return true;        // изменение на n-м проходе: есть отрицательный цикл
    }
    return false;
}

// Форд–Беллман на очереди (без отрицательных циклов)
vector<ll> spfa(int n, const vector<vector<pair<int,ll>>>& g, int s) {
    vector<ll> d(n, INF); vector<char> in(n, 0); queue<int> q;
    d[s] = 0; q.push(s); in[s] = 1;
    while (!q.empty()) {
        int v = q.front(); q.pop(); in[v] = 0;
        for (auto [u, w] : g[v])
            if (d[u] > d[v] + w) { d[u] = d[v] + w; if (!in[u]) { in[u] = 1; q.push(u); } }
    }
    return d;
}

// Флойд на double: есть ли цикл отрицательного веса (d[x][x] < 0)
bool has_neg(int n, vector<vector<double>> d) {
    for (int k = 0; k < n; k++) for (int a = 0; a < n; a++) for (int b = 0; b < n; b++)
        d[a][b] = min(d[a][b], d[a][k] + d[k][b]);
    for (int i = 0; i < n; i++) if (d[i][i] < -1e-12) return true;
    return false;
}
double min_mean(int n, const vector<vector<double>>& w, double lo, double hi) {
    for (int it = 0; it < 60; it++) {
        double mid = (lo + hi) / 2;
        auto d = w;
        for (auto& r : d) for (auto& x : r) x -= mid;       // вычитаем кандидата из всех рёбер
        if (has_neg(n, d)) hi = mid; else lo = mid;
    }
    return lo;
}

// Дерево отрезков для неявной Дейкстры: chmin на отрезке и вынимание минимума
struct Seg {
    static constexpr ll DEAD = LLONG_MAX;   // метка «вершина уже вынута»
    int n; vector<ll> mn, tg;
    Seg(int n) : n(n), mn(4 * n, INF), tg(4 * n, INF) {}
    void app(int v, ll x) { if (mn[v] != DEAD) { mn[v] = min(mn[v], x); tg[v] = min(tg[v], x); } }
    void push(int v) { if (tg[v] < INF) { app(2*v, tg[v]); app(2*v+1, tg[v]); tg[v] = INF; } }
    void chmin(int v, int l, int r, int a, int b, ll x) {
        if (b < l || r < a) return;
        if (a <= l && r <= b) { app(v, x); return; }
        push(v); int m = (l + r) / 2;
        chmin(2*v, l, m, a, b, x); chmin(2*v+1, m+1, r, a, b, x);
        mn[v] = min(mn[2*v], mn[2*v+1]);
    }
    int take(int v, int l, int r) {          // вынуть вершину с минимальным d, пометить её DEAD
        if (l == r) { mn[v] = DEAD; return l; }
        push(v); int m = (l + r) / 2, res;
        if (mn[2*v] <= mn[2*v+1]) res = take(2*v, l, m); else res = take(2*v+1, m+1, r);
        mn[v] = min(mn[2*v], mn[2*v+1]);
        return res;
    }
};
// ребро-отрезок: из вершины во все вершины l..r с весом w
struct SE { int l, r; ll w; };
// Дейкстра по неявному графу
vector<ll> dijkstra_implicit(int n, const vector<vector<SE>>& g, int s) {
    Seg t(n); vector<ll> d(n, INF);
    t.chmin(1, 0, n - 1, s, s, 0);
    for (int it = 0; it < n; it++) {
        if (t.mn[1] >= INF) break;             // осталось только недостижимое
        ll dv = t.mn[1];
        int v = t.take(1, 0, n - 1);
        d[v] = dv;
        for (auto& e : g[v]) t.chmin(1, 0, n - 1, e.l, e.r, dv + e.w);
    }
    return d;
}

int main() {
    mt19937 rng(5);
    for (int it = 0; it < 4000; it++) {
        int n = rng() % 7 + 1, m = rng() % 18;
        vector<E> e; vector<vector<pair<int,ll>>> g(n);
        bool neg = rng() % 2;
        for (int i = 0; i < m; i++) {
            int a = rng() % n, b = rng() % n; ll w = neg ? (ll)(rng() % 9) - 3 : rng() % 9;
            e.push_back({a, b, w}); g[a].push_back({b, w});
        }
        vector<ll> d; bool nc = ford(n, e, 0, d);
        // эталон: Флойд с проверкой d[x][x]<0 и достижимости из 0
        vector<vector<ll>> f(n, vector<ll>(n, INF)); for (int i = 0; i < n; i++) f[i][i] = 0;
        for (auto& x : e) f[x.a][x.b] = min(f[x.a][x.b], x.w);
        for (int k = 0; k < n; k++) for (int a = 0; a < n; a++) for (int b = 0; b < n; b++)
            if (f[a][k] < INF && f[k][b] < INF) f[a][b] = max(-INF, min(f[a][b], f[a][k] + f[k][b]));
        bool ref = false;
        for (int x = 0; x < n; x++) if (f[x][x] < 0 && f[0][x] < INF) ref = true;
        if (nc != ref) { puts("FAIL negcycle"); return 1; }
        if (!nc) {
            for (int v = 0; v < n; v++) if (d[v] != f[0][v]) { puts("FAIL ford"); return 1; }
            auto s = spfa(n, g, 0);
            for (int v = 0; v < n; v++) if (s[v] != f[0][v]) { puts("FAIL spfa"); return 1; }
        }
    }
    // минимальный средний вес цикла: бин. поиск + Флойд против перебора простых циклов
    for (int it = 0; it < 300; it++) {
        int n = rng() % 5 + 2;
        vector<vector<double>> w(n, vector<double>(n, 1e9)); vector<vector<int>> has(n, vector<int>(n, 0));
        for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) if (rng() % 2) { w[i][j] = (int)(rng() % 20) - 5; has[i][j] = 1; }
        double best = 1e18;
        vector<int> p(n); iota(p.begin(), p.end(), 0);
        for (int mask = 1; mask < (1 << n); mask++) {
            vector<int> vs; for (int i = 0; i < n; i++) if (mask >> i & 1) vs.push_back(i);
            sort(vs.begin(), vs.end());
            do {
                bool ok = true; double s = 0;
                for (size_t i = 0; i < vs.size(); i++) { int a = vs[i], b = vs[(i + 1) % vs.size()]; if (!has[a][b]) { ok = false; break; } s += w[a][b]; }
                if (ok) best = min(best, s / vs.size());
            } while (next_permutation(vs.begin(), vs.end()));
        }
        if (best > 1e17) continue;
        double got = min_mean(n, w, -100, 100);
        if (fabs(got - best) > 1e-6) { printf("FAIL mean %f %f\n", got, best); return 1; }
    }
    // неявная Дейкстра против Дейкстры по явным рёбрам
    for (int it = 0; it < 3000; it++) {
        int n = rng() % 9 + 1, m = rng() % 12;
        vector<vector<SE>> g(n); vector<vector<ll>> w(n, vector<ll>(n, INF));
        for (int i = 0; i < m; i++) {
            int a = rng() % n, l = rng() % n, r = rng() % n; if (l > r) swap(l, r); ll c = rng() % 10;
            g[a].push_back({l, r, c});
            for (int j = l; j <= r; j++) w[a][j] = min(w[a][j], c);
        }
        for (int i = 0; i < n; i++) w[i][i] = min<ll>(w[i][i], 0);
        vector<ll> d(n, INF); d[0] = 0; vector<char> u(n, 0);
        for (int k = 0; k < n; k++) { int v = -1; for (int i = 0; i < n; i++) if (!u[i] && (v < 0 || d[i] < d[v])) v = i;
            if (d[v] >= INF) break; u[v] = 1; for (int j = 0; j < n; j++) if (w[v][j] < INF) d[j] = min(d[j], d[v] + w[v][j]); }
        auto r = dijkstra_implicit(n, g, 0);
        for (int v = 0; v < n; v++) if (r[v] != d[v]) { puts("FAIL implicit"); return 1; }
    }
    puts("ok");
}
