#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

// ---------- 1. Граф: «прибавить ко всем соседям» и «узнать значение», лёгкие и тяжёлые вершины ----------
struct HeavyLight {
    int n, K;
    vector<vector<int>> g, heavyNb;   // heavyNb[v] — тяжёлые соседи v
    vector<ll> a, lazy;               // lazy[h] — сколько прибавили всем соседям тяжёлой вершины h
    vector<char> heavy;
    HeavyLight(int n, const vector<pair<int,int>>& edges, int K) : n(n), K(K), g(n), heavyNb(n), a(n, 0), lazy(n, 0), heavy(n, 0) {
        for (auto [u, v] : edges) { g[u].push_back(v); g[v].push_back(u); }
        for (int v = 0; v < n; v++) heavy[v] = (int)g[v].size() >= K;
        for (int v = 0; v < n; v++) for (int u : g[v]) if (heavy[u]) heavyNb[v].push_back(u);
    }
    void add(int v, ll x) {                    // прибавить x всем соседям v
        if (!heavy[v]) { for (int u : g[v]) a[u] += x; }   // лёгкая: deg < K
        else lazy[v] += x;                                  // тяжёлая: откладываем
    }
    ll get(int v) {                            // не более 2m/K тяжёлых соседей
        ll r = a[v];
        for (int h : heavyNb[v]) r += lazy[h];
        return r;
    }
};

// ---------- 2. Рюкзак: различные суммы за O(W sqrt W) ----------
// если вес x встречается ≥ 3 раз, два предмета x заменяем одним 2x
vector<char> reachable_sums(vector<int> w, int W) {
    vector<int> cnt(W + 1, 0);
    for (int x : w) cnt[x]++;
    vector<int> items;
    for (int x = 1; x <= W; x++) {
        while (cnt[x] >= 3) { cnt[x] -= 2; if (2 * x <= W) cnt[2 * x]++; }   // 2x > W недостижим
        for (int i = 0; i < cnt[x]; i++) items.push_back(x);
    }
    vector<char> dp(W + 1, 0); dp[0] = 1;
    for (int x : items) for (int s = W; s >= x; s--) if (dp[s - x]) dp[s] = 1;
    return dp;
}
// минимальное число предметов: k копий веса x дробим на пачки 1,2,4,... и остаток; пачка из c копий стоит c
vector<int> min_items(vector<int> w, int W) {
    map<int,int> k; for (int x : w) k[x]++;
    vector<pair<int,int>> packs;                 // (вес, число предметов в пачке)
    for (auto [x, c] : k) {
        int p = 1;
        while (c > 0) { int t = min(p, c); packs.push_back({x * t, t}); c -= t; p *= 2; }
    }
    const int INF = 1e9;
    vector<int> dp(W + 1, INF); dp[0] = 0;
    for (auto [pw, pc] : packs) for (int s = W; s >= pw; s--) if (dp[s - pw] < INF) dp[s] = min(dp[s], dp[s - pw] + pc);
    return dp;
}

// ---------- 3. Блоки: точечное прибавление O(1) + сумма на отрезке O(sqrt n) ----------
struct BlockSum {
    int n, K; vector<ll> a, bs;
    BlockSum(int n, int K) : n(n), K(K), a(n, 0), bs(n / K + 1, 0) {}
    void add(int i, ll x) { a[i] += x; bs[i / K] += x; }               // O(1)
    ll sum(int l, int r) {                                              // [l, r]
        ll s = 0;
        while (l <= r && l % K) s += a[l++];
        while (l + K - 1 <= r) { s += bs[l / K]; l += K; }
        while (l <= r) s += a[l++];
        return s;
    }
};

// ---------- 4. Прибавление арифметической прогрессии за O(1), сумма за O(sqrt n) ----------
// prefix(p, b, c): ко всем i ≤ p прибавить b + c·i. Отрезок [l, r] = prefix(r) − prefix(l−1).
struct APBlocks {
    int n, K, nb; vector<ll> a, bs;     // a — исходный массив, bs — его суммы по блокам
    vector<ll> lb, lc;      // для блока j: прибавить ВСЕМ блокам левее j
    vector<ll> ib, ic;      // для позиции p: прибавить всем элементам ≤ p в том же блоке
    vector<ll> ex;          // готовая добавка к сумме блока от prefix-обновлений внутри него
    APBlocks(const vector<ll>& init, int K) : n(init.size()), K(K), nb((n + K - 1) / K), a(init), bs(nb, 0), lb(nb, 0), lc(nb, 0), ib(n, 0), ic(n, 0), ex(nb, 0) {
        for (int i = 0; i < n; i++) bs[i / K] += a[i];
    }
    ll idxsum(ll l, ll r) { return (l + r) * (r - l + 1) / 2; }
    void prefix(int p, ll b, ll c) {
        if (p < 0) return;
        int j = p / K, st = j * K;
        lb[j] += b; lc[j] += c;
        ib[p] += b; ic[p] += c;
        ex[j] += b * (p - st + 1) + c * idxsum(st, p);
    }
    void update(int l, int r, ll b, ll c) {      // a[i] += b + c·i на [l, r]
        prefix(r, b, c); prefix(l - 1, -b, -c);
    }
    ll sum(int l, int r) {
        ll res = 0, B = 0, C = 0;                // накопленные добавки от блоков правее текущего
        for (int j = nb - 1; j >= 0; j--) {
            int st = j * K, en = min(n, st + K) - 1;
            if (st > r) { B += lb[j]; C += lc[j]; continue; }
            if (en < l) break;                   // левее запроса — ничего не нужно
            if (l <= st && en <= r) {
                ll s = bs[j] + ex[j];                       // O(1) на целый блок
                s += B * (en - st + 1) + C * idxsum(st, en);
                res += s;
            } else {                             // частичный блок: идём справа налево, копим ib/ic внутри блока
                ll bb = 0, cc = 0;
                for (int i = en; i >= st; i--) {
                    bb += ib[i]; cc += ic[i];
                    if (l <= i && i <= r) res += a[i] + bb + cc * i + B + C * i;
                }
            }
            B += lb[j]; C += lc[j];
        }
        return res;
    }
};

// ---------- 5. Множество: insert/erase за O(1), min и k-я статистика за O(sqrt M) ----------
struct SqrtSet {
    int M, K; vector<int> cnt, bc;
    SqrtSet(int M, int K) : M(M), K(K), cnt(M, 0), bc(M / K + 1, 0) {}
    void insert(int x) { cnt[x]++; bc[x / K]++; }
    void erase(int x) { cnt[x]--; bc[x / K]--; }
    int kth(int k) {                             // k = 1 — минимум
        int j = 0;
        while (k > bc[j]) { k -= bc[j]; j++; }
        for (int x = j * K; ; x++) { if (k <= cnt[x]) return x; k -= cnt[x]; }
    }
};

// ---------- 6. Прибавление на отрезке + «сколько чисел ≤ x на отрезке» ----------
struct SortedBlocks {
    int n, K, nb; vector<ll> a, mod; vector<vector<int>> ord;   // ord[j] — индексы блока по возрастанию a
    SortedBlocks(const vector<ll>& v, int K) : n(v.size()), K(K), nb((n + K - 1) / K), a(v), mod(nb, 0), ord(nb) { for (int j = 0; j < nb; j++) rebuild(j); }
    void rebuild(int j) {
        int st = j * K, en = min(n, st + K);
        ord[j].resize(en - st); iota(ord[j].begin(), ord[j].end(), st);
        sort(ord[j].begin(), ord[j].end(), [&](int x, int y) { return a[x] < a[y]; });
    }
    void partial(int j, int l, int r, ll x) {    // прибавить x к a[l..r] внутри блока j: два отсортированных куска сливаем
        vector<int> in, out;
        for (int i : ord[j]) (l <= i && i <= r ? in : out).push_back(i);
        for (int i = l; i <= r; i++) a[i] += x;
        ord[j].clear();
        merge(in.begin(), in.end(), out.begin(), out.end(), back_inserter(ord[j]), [&](int p, int q) { return a[p] < a[q]; });
    }
    void add(int l, int r, ll x) {
        int jl = l / K, jr = r / K;
        if (jl == jr) { partial(jl, l, r, x); return; }
        partial(jl, l, (jl + 1) * K - 1, x);
        partial(jr, jr * K, r, x);
        for (int j = jl + 1; j < jr; j++) mod[j] += x;           // целый блок: порядок не меняется
    }
    int count_le(int l, int r, ll x) {
        int jl = l / K, jr = r / K, res = 0;
        auto brute = [&](int a_, int b_) { for (int i = a_; i <= b_; i++) res += a[i] + mod[i / K] <= x; };
        if (jl == jr) { brute(l, r); return res; }
        brute(l, (jl + 1) * K - 1); brute(jr * K, r);
        for (int j = jl + 1; j < jr; j++) {                       // бинарный поиск по x − modifier
            ll t = x - mod[j];
            int lo = 0, hi = ord[j].size();
            while (lo < hi) { int m = (lo + hi) / 2; if (a[ord[j][m]] <= t) lo = m + 1; else hi = m; }
            res += lo;
        }
        return res;
    }
};

// ---------- 7. Mo: сумма разностей индексов равных элементов на отрезке ----------
vector<ll> mo_pairs(const vector<int>& a, const vector<array<int,3>>& qs /* l, r, id */) {
    int n = a.size(), q = qs.size();
    int K = max(1, (int)(n / sqrt((double)max(1, q))));
    vector<int> ord(q); iota(ord.begin(), ord.end(), 0);
    sort(ord.begin(), ord.end(), [&](int x, int y) {
        int bx = qs[x][0] / K, by = qs[y][0] / K;
        if (bx != by) return bx < by;
        return (bx & 1) ? qs[x][1] > qs[y][1] : qs[x][1] < qs[y][1];
    });
    vector<ll> cnt(n + 1, 0), sidx(n + 1, 0), ans(q);
    ll cur = 0; int L = 0, R = -1;
    auto addR = [&](int i) { cur += (ll)i * cnt[a[i]] - sidx[a[i]]; cnt[a[i]]++; sidx[a[i]] += i; };      // новые пары: i − j для j в отрезке
    auto addL = [&](int i) { cur += sidx[a[i]] - (ll)i * cnt[a[i]]; cnt[a[i]]++; sidx[a[i]] += i; };      // j − i
    auto delR = [&](int i) { cnt[a[i]]--; sidx[a[i]] -= i; cur -= (ll)i * cnt[a[i]] - sidx[a[i]]; };
    auto delL = [&](int i) { cnt[a[i]]--; sidx[a[i]] -= i; cur -= sidx[a[i]] - (ll)i * cnt[a[i]]; };
    for (int id : ord) {
        int l = qs[id][0], r = qs[id][1];
        while (R < r) addR(++R);
        while (L > l) addL(--L);
        while (R > r) delR(R--);
        while (L < l) delL(L++);
        ans[qs[id][2]] = cur;
    }
    return ans;
}

// ---------- 8. Mo без удалений: самый длинный подотрезок с нулевой суммой ----------
vector<int> mo_rollback_zero(const vector<ll>& a, const vector<array<int,2>>& qs) {
    int n = a.size(), q = qs.size();
    vector<ll> p(n + 1, 0); for (int i = 0; i < n; i++) p[i + 1] = p[i] + a[i];       // нужна пара x<y из [l, r+1] с p[x]=p[y]
    vector<ll> vals(p.begin(), p.end()); sort(vals.begin(), vals.end()); vals.erase(unique(vals.begin(), vals.end()), vals.end());
    vector<int> id(n + 1); for (int i = 0; i <= n; i++) id[i] = lower_bound(vals.begin(), vals.end(), p[i]) - vals.begin();
    int K = max(1, (int)(n / sqrt((double)max(1, q))));
    vector<int> ord(q); iota(ord.begin(), ord.end(), 0);
    sort(ord.begin(), ord.end(), [&](int x, int y) { int bx = qs[x][0] / K, by = qs[y][0] / K; return bx != by ? bx < by : qs[x][1] < qs[y][1]; });
    vector<int> ans(q, 0), first(vals.size(), -1), last(vals.size(), -1);
    vector<int> first2(vals.size(), -1);
    auto inblock = [&](int l, int r) {           // запрос целиком в одном блоке: добавляем префиксы l..r+1 слева направо, за O(K)
        int best = 0;
        for (int x = l; x <= r + 1; x++) { int v = id[x]; if (first2[v] < 0) first2[v] = x; best = max(best, x - first2[v]); }
        for (int x = l; x <= r + 1; x++) first2[id[x]] = -1;
        return best;
    };
    int curBlock = -1, R = 0, ans0 = 0;          // в структуре лежат индексы префиксов (blockEnd .. R]
    for (int qi : ord) {
        int l = qs[qi][0], r = qs[qi][1], b = l / K;
        if (r / K == b) { ans[qi] = inblock(l, r); continue; }               // запрос внутри одного блока
        if (b != curBlock) {                       // новый блок: чистим структуру
            fill(first.begin(), first.end(), -1); fill(last.begin(), last.end(), -1);
            curBlock = b; R = (b + 1) * K - 1; ans0 = 0;               // граница блока: индексы префиксов > R пока не добавлены
            // структура пуста; R+1 — первый добавляемый индекс префикса
        }
        while (R + 1 <= r + 1) {                   // добавляем справа: индекс префикса R+1
            ++R; int v = id[R];
            if (first[v] < 0) first[v] = R;
            last[v] = R; ans0 = max(ans0, last[v] - first[v]);
        }
        // временно добавляем слева индексы префиксов l .. (b+1)K − 1 (в обратном порядке), потом откатываем
        vector<array<int,3>> undo; int ansTmp = ans0;
        for (int x = (b + 1) * K - 1; x >= l; x--) {
            int v = id[x];
            undo.push_back({v, first[v], last[v]});
            if (last[v] < 0) last[v] = x;
            first[v] = x; ansTmp = max(ansTmp, last[v] - first[v]);
        }
        ans[qi] = ansTmp;
        for (int i = (int)undo.size() - 1; i >= 0; i--) { first[undo[i][0]] = undo[i][1]; last[undo[i][0]] = undo[i][2]; }
    }
    return ans;
}

// свёртка массива с самим собой (здесь наивная, в решении — БПФ за M log M)
vector<ll> convolve(const vector<ll>& c) { int M = c.size(); vector<ll> r(2 * M, 0); for (int i = 0; i < M; i++) if (c[i]) for (int j = 0; j < M; j++) r[i + j] += c[i] * c[j]; return r; }
// «сколько упорядоченных пар (x, y) из мультимножества дают x + y = S»; полная пересборка раз в K изменений
struct TwoSum {
    int M; vector<ll> cnt, snapshot, base; vector<pair<int,int>> pend;       // pend: (знак, x) изменения после последней сборки
    TwoSum(int M) : M(M), cnt(M, 0) { rebuild(); }
    void rebuild() { snapshot = cnt; base = convolve(snapshot); pend.clear(); }
    void change(int sign, int x) { cnt[x] += sign; pend.push_back({sign, x}); }   // вызывающий пересобирает каждые K изменений
    ll query(int S) {
        ll res = base[S];
        for (auto [sg, x] : pend) {                   // вклад одного изменения: sg · 2 · snapshot[S−x] (+ сама пара x,x)
            int y = S - x;
            ll other = (y >= 0 && y < M) ? snapshot[y] : 0;
            res += (y == x) ? sg * (2 * other + sg) : sg * 2 * other;
            snapshot[x] += sg;                        // следующее изменение видит предыдущие
        }
        for (int i = (int)pend.size() - 1; i >= 0; i--) snapshot[pend[i].second] -= pend[i].first;   // откат
        return res;
    }
};

// ---------- 10. Прямоугольник максимальной площади с нулевой суммой: O(nm · min(n, m)) ----------
int max_zero_rect(vector<vector<ll>> g) {
    int n = g.size(), m = g[0].size();
    if (n > m) {                                   // транспонируем: перебираем пары строк у короткой стороны
        vector<vector<ll>> t(m, vector<ll>(n));
        for (int i = 0; i < n; i++) for (int j = 0; j < m; j++) t[j][i] = g[i][j];
        g = t; swap(n, m);
    }
    int best = 0;
    for (int top = 0; top < n; top++) {
        vector<ll> col(m, 0);
        for (int bot = top; bot < n; bot++) {
            for (int j = 0; j < m; j++) col[j] += g[bot][j];
            unordered_map<ll,int> firstPos; firstPos[0] = 0; ll s = 0;
            for (int j = 0; j < m; j++) {
                s += col[j];
                auto it = firstPos.find(s);
                if (it == firstPos.end()) firstPos[s] = j + 1;
                else best = max(best, (bot - top + 1) * (j + 1 - it->second));
            }
        }
    }
    return best;
}

// ---------- 11. Площадь объединения ≤ 4 квадратов включениями-исключениями ----------
// прямоугольник [x1,x2) × [y1,y2)
struct Rect { ll x1, y1, x2, y2; };
ll union_area(const vector<Rect>& r) {
    int k = r.size(); ll res = 0;
    for (int mask = 1; mask < (1 << k); mask++) {
        ll x1 = LLONG_MIN, y1 = LLONG_MIN, x2 = LLONG_MAX, y2 = LLONG_MAX;
        for (int i = 0; i < k; i++) if (mask >> i & 1) { x1 = max(x1, r[i].x1); y1 = max(y1, r[i].y1); x2 = min(x2, r[i].x2); y2 = min(y2, r[i].y2); }
        ll area = max(0LL, x2 - x1) * max(0LL, y2 - y1);
        res += (__builtin_popcount(mask) % 2 ? 1 : -1) * area;
    }
    return res;
}

#ifdef TEST_MAIN
int main() {
    mt19937 rng(7);
    // 1
    for (int it = 0; it < 300; it++) {
        int n = rng() % 12 + 2, m = rng() % 25; vector<pair<int,int>> e;
        for (int i = 0; i < m; i++) { int u = rng() % n, v = rng() % n; if (u != v) e.push_back({u, v}); }
        HeavyLight h(n, e, rng() % 4 + 1); vector<ll> ref(n, 0);
        vector<vector<int>> g(n); for (auto [u, v] : e) { g[u].push_back(v); g[v].push_back(u); }
        for (int s = 0; s < 40; s++) {
            int v = rng() % n; ll x = rng() % 10;
            if (rng() % 2) { h.add(v, x); for (int u : g[v]) ref[u] += x; }
            else if (h.get(v) != ref[v]) { puts("FAIL heavy"); return 1; }
        }
    }
    // 2
    for (int it = 0; it < 500; it++) {
        int W = rng() % 40 + 1, k = rng() % 14; vector<int> w; int tot = 0;
        for (int i = 0; i < k; i++) { int x = rng() % 6 + 1; if (tot + x <= W) { w.push_back(x); tot += x; } }
        auto fast = reachable_sums(w, W); auto mi = min_items(w, W);
        vector<char> br(W + 1, 0); br[0] = 1; vector<int> bi(W + 1, 1e9); bi[0] = 0;
        for (int x : w) for (int s = W; s >= x; s--) { if (br[s - x]) br[s] = 1; if (bi[s - x] < 1e9) bi[s] = min(bi[s], bi[s - x] + 1); }
        if (fast != br || mi != bi) { puts("FAIL knap"); return 1; }
    }
    // 3, 4
    for (int it = 0; it < 300; it++) {
        int n = rng() % 30 + 1, K = rng() % 5 + 1; vector<ll> init(n); for (auto& x : init) x = (ll)(rng() % 11) - 5; BlockSum bs(n, K); APBlocks ap(init, K); vector<ll> r1(n, 0), r2 = init;
        for (int s = 0; s < 60; s++) {
            int l = rng() % n, r = rng() % n; if (l > r) swap(l, r); ll b = (ll)(rng() % 9) - 4, c = (ll)(rng() % 7) - 3;
            int t = rng() % 4;
            if (t == 0) { int i = l; bs.add(i, b); r1[i] += b; }
            else if (t == 1) { ll x = 0; for (int i = l; i <= r; i++) x += r1[i]; if (bs.sum(l, r) != x) { puts("FAIL bs"); return 1; } }
            else if (t == 2) { ap.update(l, r, b, c); for (int i = l; i <= r; i++) r2[i] += b + c * i; }
            else { ll x = 0; for (int i = l; i <= r; i++) x += r2[i]; if (ap.sum(l, r) != x) { puts("FAIL ap"); return 1; } }
        }
    }
    // 5
    for (int it = 0; it < 300; it++) {
        int M = rng() % 40 + 1, K = rng() % 6 + 1; SqrtSet s(M, K); multiset<int> ref;
        for (int st = 0; st < 60; st++) {
            int t = rng() % 3, x = rng() % M;
            if (t == 0) { s.insert(x); ref.insert(x); }
            else if (t == 1 && ref.count(x)) { s.erase(x); ref.erase(ref.find(x)); }
            else if (t == 2 && !ref.empty()) { int k = rng() % ref.size() + 1; if (s.kth(k) != *next(ref.begin(), k - 1)) { puts("FAIL kth"); return 1; } }
        }
    }
    // 6
    for (int it = 0; it < 300; it++) {
        int n = rng() % 25 + 1, K = rng() % 5 + 1; vector<ll> v(n); for (auto& x : v) x = (ll)(rng() % 21) - 10;
        SortedBlocks sb(v, K);
        for (int st = 0; st < 40; st++) {
            int l = rng() % n, r = rng() % n; if (l > r) swap(l, r); ll x = (ll)(rng() % 21) - 10;
            if (rng() % 2) { sb.add(l, r, x); for (int i = l; i <= r; i++) v[i] += x; }
            else { int c = 0; for (int i = l; i <= r; i++) c += v[i] <= x; if (sb.count_le(l, r, x) != c) { puts("FAIL sorted"); return 1; } }
        }
    }
    // 7
    for (int it = 0; it < 200; it++) {
        int n = rng() % 30 + 1, q = rng() % 30 + 1; vector<int> a(n); for (auto& x : a) x = rng() % min(n, 5);
        vector<array<int,3>> qs; for (int i = 0; i < q; i++) { int l = rng() % n, r = rng() % n; if (l > r) swap(l, r); qs.push_back({l, r, i}); }
        auto ans = mo_pairs(a, qs);
        for (auto& qq : qs) { ll s = 0; for (int i = qq[0]; i <= qq[1]; i++) for (int j = i + 1; j <= qq[1]; j++) if (a[i] == a[j]) s += j - i; if (ans[qq[2]] != s) { puts("FAIL mo"); return 1; } }
    }
    // 8
    for (int it = 0; it < 300; it++) {
        int n = rng() % 30 + 1, q = rng() % 30 + 1; vector<ll> a(n); for (auto& x : a) x = (ll)(rng() % 5) - 2;
        vector<array<int,2>> qs; for (int i = 0; i < q; i++) { int l = rng() % n, r = rng() % n; if (l > r) swap(l, r); qs.push_back({l, r}); }
        auto ans = mo_rollback_zero(a, qs);
        for (int i = 0; i < q; i++) { int best = 0, l = qs[i][0], r = qs[i][1]; for (int x = l; x <= r; x++) { ll s = 0; for (int y = x; y <= r; y++) { s += a[y]; if (s == 0) best = max(best, y - x + 1); } } if (ans[i] != best) { printf("FAIL rollback %d %d\n", ans[i], best); return 1; } }
    }
    // 9
    for (int it = 0; it < 200; it++) {
        int M = rng() % 10 + 1; TwoSum ts(M); multiset<int> ref;
        for (int st = 0; st < 40; st++) {
            int t = rng() % 3, x = rng() % M;
            if (t == 0) { ts.change(+1, x); ref.insert(x); }
            else if (t == 1 && ref.count(x)) { ts.change(-1, x); ref.erase(ref.find(x)); }
            else if (t == 2) { int S = rng() % (2 * M); ll c = 0; for (int a : ref) for (int b : ref) c += a + b == S; if (ts.query(S) != c) { puts("FAIL twosum"); return 1; } }
            if (ts.pend.size() >= 4) ts.rebuild();
        }
    }
    // 10
    for (int it = 0; it < 300; it++) {
        int n = rng() % 6 + 1, m = rng() % 6 + 1; vector<vector<ll>> g(n, vector<ll>(m)); for (auto& r : g) for (auto& x : r) x = (ll)(rng() % 5) - 2;
        int best = 0;
        for (int a = 0; a < n; a++) for (int b = a; b < n; b++) for (int c = 0; c < m; c++) for (int d = c; d < m; d++) { ll s = 0; for (int i = a; i <= b; i++) for (int j = c; j <= d; j++) s += g[i][j]; if (s == 0) best = max(best, (b - a + 1) * (d - c + 1)); }
        if (max_zero_rect(g) != best) { puts("FAIL rect"); return 1; }
    }
    // 11
    for (int it = 0; it < 300; it++) {
        int k = rng() % 4 + 1; vector<Rect> r;
        for (int i = 0; i < k; i++) { ll x = rng() % 8, y = rng() % 8, s = rng() % 5 + 1; r.push_back({x, y, x + s, y + s}); }
        ll c = 0; for (int x = 0; x < 14; x++) for (int y = 0; y < 14; y++) { bool in = false; for (auto& q : r) if (q.x1 <= x && x < q.x2 && q.y1 <= y && y < q.y2) in = true; c += in; }
        if (union_area(r) != c) { puts("FAIL union"); return 1; }
    }
    puts("ok");
}
#endif
