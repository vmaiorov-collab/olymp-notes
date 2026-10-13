#include <bits/stdc++.h>
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/tree_policy.hpp>
using namespace std;
using namespace __gnu_pbds;
typedef long long ll;

// ---------- 1. Дерево отрезков: прибавление на отрезке и сумма, ленивые операции и push ----------
struct LazySum {
    int n;
    vector<ll> sum, add;                         // add[v] — сколько ещё нужно добавить сыновьям
    LazySum(int n) : n(n), sum(4 * n, 0), add(4 * n, 0) {}
    void apply(int v, int l, int r, ll x) { sum[v] += x * (r - l); add[v] += x; }
    void push(int v, int l, int r) {             // безвредно вызывать сколько угодно раз
        if (!add[v]) return;
        int m = (l + r) / 2;
        apply(2 * v, l, m, add[v]); apply(2 * v + 1, m, r, add[v]);
        add[v] = 0;
    }
    void update(int v, int l, int r, int ql, int qr, ll x) {   // [ql, qr) += x
        if (qr <= l || r <= ql) return;
        if (ql <= l && r <= qr) { apply(v, l, r, x); return; }
        push(v, l, r);
        int m = (l + r) / 2;
        update(2 * v, l, m, ql, qr, x); update(2 * v + 1, m, r, ql, qr, x);
        sum[v] = sum[2 * v] + sum[2 * v + 1];
    }
    ll get(int v, int l, int r, int ql, int qr) {
        if (qr <= l || r <= ql) return 0;
        if (ql <= l && r <= qr) return sum[v];
        push(v, l, r);
        int m = (l + r) / 2;
        return get(2 * v, l, m, ql, qr) + get(2 * v + 1, m, r, ql, qr);
    }
    void update(int l, int r, ll x) { update(1, 0, n, l, r, x); }
    ll get(int l, int r) { return get(1, 0, n, l, r); }
};

// ---------- 2. Минимум и количество минимумов с прибавлением на отрезке ----------
struct MinCount {
    int n;
    vector<ll> mn, add;
    vector<ll> cnt;                              // суммарный вес позиций, где достигается минимум
    MinCount(const vector<ll>& w) : n(w.size()), mn(4 * w.size(), 0), add(4 * w.size(), 0), cnt(4 * w.size(), 0) { build(1, 0, n, w); }
    void build(int v, int l, int r, const vector<ll>& w) {
        if (r - l == 1) { cnt[v] = w[l]; return; }
        int m = (l + r) / 2;
        build(2 * v, l, m, w); build(2 * v + 1, m, r, w);
        pull(v);
    }
    void pull(int v) {
        mn[v] = min(mn[2 * v], mn[2 * v + 1]);
        cnt[v] = (mn[2 * v] == mn[v] ? cnt[2 * v] : 0) + (mn[2 * v + 1] == mn[v] ? cnt[2 * v + 1] : 0);
    }
    void apply(int v, ll x) { mn[v] += x; add[v] += x; }
    void push(int v) { if (add[v]) { apply(2 * v, add[v]); apply(2 * v + 1, add[v]); add[v] = 0; } }
    void update(int v, int l, int r, int ql, int qr, ll x) {
        if (qr <= l || r <= ql) return;
        if (ql <= l && r <= qr) { apply(v, x); return; }
        push(v);
        int m = (l + r) / 2;
        update(2 * v, l, m, ql, qr, x); update(2 * v + 1, m, r, ql, qr, x);
        pull(v);
    }
    pair<ll, ll> query(int v, int l, int r, int ql, int qr) {      // (минимум, вес минимумов)
        if (qr <= l || r <= ql) return {LLONG_MAX, 0};
        if (ql <= l && r <= qr) return {mn[v], cnt[v]};
        push(v);
        int m = (l + r) / 2;
        auto a = query(2 * v, l, m, ql, qr), b = query(2 * v + 1, m, r, ql, qr);
        if (a.first < b.first) return a;
        if (b.first < a.first) return b;
        return {a.first, a.second + b.second};
    }
    void update(int l, int r, ll x) { update(1, 0, n, l, r, x); }
    pair<ll, ll> query(int l, int r) { return query(1, 0, n, l, r); }
};

// ---------- 3. Площадь объединения прямоугольников: заметающая прямая ----------
ll union_area(const vector<array<int, 4>>& rect) {            // {x1, y1, x2, y2}, x1 < x2, y1 < y2
    vector<int> ys;
    for (auto& r : rect) { ys.push_back(r[1]); ys.push_back(r[3]); }
    sort(ys.begin(), ys.end()); ys.erase(unique(ys.begin(), ys.end()), ys.end());
    int m = (int)ys.size() - 1;                                // полоса i = [ys[i], ys[i+1]) с весом длины
    if (m <= 0) return 0;
    vector<ll> w(m);
    for (int i = 0; i < m; i++) w[i] = ys[i + 1] - ys[i];
    ll total = ys.back() - ys[0];
    MinCount tree(w);
    vector<array<int, 4>> ev;                                  // {x, -тип, l, r}: открытие (+1) идёт раньше закрытия
    for (auto& r : rect) {
        int l = lower_bound(ys.begin(), ys.end(), r[1]) - ys.begin();
        int h = lower_bound(ys.begin(), ys.end(), r[3]) - ys.begin();
        ev.push_back({r[0], -1, l, h}); ev.push_back({r[2], 1, l, h});
    }
    sort(ev.begin(), ev.end());
    ll area = 0;
    for (size_t i = 0; i < ev.size(); i++) {
        if (i) {
            auto [mn, c] = tree.query(0, m);
            ll covered = total - (mn == 0 ? c : 0);            // ненулевые = всё минус нули
            area += covered * (ev[i][0] - ev[i - 1][0]);
        }
        tree.update(ev[i][2], ev[i][3], -ev[i][1]);            // -(-1) = +1 при открытии, -1 при закрытии
    }
    return area;
}

// ---------- 4. Неявное дерево отрезков на [0, N): память растёт только по запросам ----------
struct DynTree {
    struct Node { ll sum = 0; int l = -1, r = -1; };
    vector<Node> t; ll N;
    DynTree(ll N) : N(N) { t.emplace_back(); }
    int child(int v, bool right) {
        int c = right ? t[v].r : t[v].l;
        if (c < 0) { c = t.size(); t.emplace_back(); (right ? t[v].r : t[v].l) = c; }
        return c;
    }
    void add(ll pos, ll x) {                                   // a[pos] += x, создаём только вершины на пути
        int v = 0; ll lo = 0, hi = N;
        t[v].sum += x;
        while (hi - lo > 1) {
            ll m = (lo + hi) / 2;
            bool right = pos >= m;
            v = child(v, right);
            (right ? lo : hi) = m;
            t[v].sum += x;
        }
    }
    ll get(int v, ll lo, ll hi, ll l, ll r) {                  // сумма на [l, r)
        if (v < 0 || r <= lo || hi <= l) return 0;             // отсутствующая вершина — нули
        if (l <= lo && hi <= r) return t[v].sum;
        ll m = (lo + hi) / 2;
        return get(t[v].l, lo, m, l, r) + get(t[v].r, m, hi, l, r);
    }
    ll get(ll l, ll r) { return get(0, 0, N, l, r); }
};

// ---------- 5. Дерево Фенвика: префиксная сумма, поиск k-й порядковой статистики ----------
struct Fenwick {
    int n; vector<ll> t;
    Fenwick(int n) : n(n), t(n + 1, 0) {}
    void add(int i, ll x) { for (; i <= n; i += i & -i) t[i] += x; }   // индексы с 1
    ll pref(int i) { ll r = 0; for (; i > 0; i -= i & -i) r += t[i]; return r; }
    int kth(ll k) {                                                     // минимальное i с pref(i) >= k
        int pos = 0;
        for (int pw = 1 << __lg(n); pw; pw >>= 1)
            if (pos + pw <= n && t[pos + pw] < k) { pos += pw; k -= t[pos]; }
        return pos + 1;
    }
};

// ---------- 6. Прибавление на отрезке и сумма на отрезке на двух деревьях Фенвика ----------
// S(r) = sum_{j<=r} d_j (r - j + 1) = (r + 1) * sum d_j  -  sum j * d_j
struct RangeFenwick {
    Fenwick b1, b2;
    RangeFenwick(int n) : b1(n + 1), b2(n + 1) {}
    void upd(int i, ll x) { b1.add(i, x); b2.add(i, x * i); }
    void add(int l, int r, ll x) { upd(l, x); upd(r + 1, -x); }       // [l, r] += x, индексы с 1
    ll pref(int r) { return (r + 1) * b1.pref(r) - b2.pref(r); }
    ll get(int l, int r) { return pref(r) - pref(l - 1); }
};

// ---------- 7. НОП двух перестановок через НВП и «максимум на префиксе» в Фенвике ----------
struct FenwickMax {
    int n; vector<int> t;
    FenwickMax(int n) : n(n), t(n + 1, 0) {}
    void upd(int i, int x) { for (; i <= n; i += i & -i) t[i] = max(t[i], x); }   // значения только растут
    int get(int i) { int r = 0; for (; i > 0; i -= i & -i) r = max(r, t[i]); return r; }
};
int lcs_of_permutations(const vector<int>& p, const vector<int>& q) {   // значения 0..n-1
    int n = p.size();
    vector<int> pos(n);
    for (int i = 0; i < n; i++) pos[p[i]] = i + 1;
    FenwickMax f(n);
    int best = 0;
    for (int x : q) {                                 // идём по q, для каждого числа берём его позицию в p
        int len = f.get(pos[x] - 1) + 1;              // длина лучшей цепочки, кончающейся левее в p
        f.upd(pos[x], len);
        best = max(best, len);
    }
    return best;
}

// ---------- 8. Дерево отрезков в 2n ячейках: нумерация в порядке обхода в глубину ----------
struct SegSum2n {
    int n; vector<ll> t;
    SegSum2n(const vector<ll>& a) : n(a.size()), t(2 * a.size()) { build(0, 0, n, a); }
    void build(int x, int l, int r, const vector<ll>& a) {           // отрезок [l, r)
        if (r - l == 1) { t[x] = a[l]; return; }
        int m = (l + r) / 2;
        int L = x + 1, R = x + 2 * (m - l);                          // у левого поддерева 2(m-l)-1 вершин
        build(L, l, m, a); build(R, m, r, a);
        t[x] = t[L] + t[R];
    }
    ll get(int x, int l, int r, int ql, int qr) {
        if (qr <= l || r <= ql) return 0;
        if (ql <= l && r <= qr) return t[x];
        int m = (l + r) / 2;
        return get(x + 1, l, m, ql, qr) + get(x + 2 * (m - l), m, r, ql, qr);
    }
    ll get(int l, int r) { return get(0, 0, n, l, r); }
};

// ---------- 9. Прибавление на отрезке и сумма без push: модификаторы остаются в вершинах ----------
struct NoPushTree {
    int n; vector<ll> sum, mod;       // sum[v] учитывает все изменения внутри поддерева v; mod[v] — прибавка всем элементам v
    NoPushTree(const vector<ll>& a) : n(a.size()), sum(4 * a.size(), 0), mod(4 * a.size(), 0) { build(1, 0, n, a); }
    void build(int v, int l, int r, const vector<ll>& a) {
        if (r - l == 1) { sum[v] = a[l]; return; }
        int m = (l + r) / 2;
        build(2 * v, l, m, a); build(2 * v + 1, m, r, a);
        sum[v] = sum[2 * v] + sum[2 * v + 1];
    }
    void add(int v, int l, int r, int ql, int qr, ll x) {
        if (qr <= l || r <= ql) return;
        if (ql <= l && r <= qr) { mod[v] += x; sum[v] += x * (r - l); return; }
        int m = (l + r) / 2;
        add(2 * v, l, m, ql, qr, x); add(2 * v + 1, m, r, ql, qr, x);
        sum[v] = sum[2 * v] + sum[2 * v + 1] + mod[v] * (r - l);
    }
    ll get(int v, int l, int r, int ql, int qr) {
        if (qr <= l || r <= ql) return 0;
        if (ql <= l && r <= qr) return sum[v];
        int m = (l + r) / 2;
        ll res = mod[v] * (min(r, qr) - max(l, ql));      // вклад модификатора, который не спускали вниз
        return res + get(2 * v, l, m, ql, qr) + get(2 * v + 1, m, r, ql, qr);
    }
    void add(int l, int r, ll x) { add(1, 0, n, l, r, x); }
    ll get(int l, int r) { return get(1, 0, n, l, r); }
};

// ---------- 10. НОД на отрезке при прибавлении на отрезке: gcd(a_l, a_{l+1}-a_l, ..., a_r-a_{r-1}) ----------
struct RangeAddGcd {
    int n, sz; vector<ll> d, seg; Fenwick bit;     // d[i] = a[i] - a[i-1]; bit хранит d, чтобы получить a[i]
    RangeAddGcd(const vector<ll>& a) : n(a.size()), d(a.size()), bit(a.size() + 1) {
        for (int i = 0; i < n; i++) { d[i] = a[i] - (i ? a[i - 1] : 0); bit.add(i + 1, d[i]); }
        sz = 1; while (sz < n) sz <<= 1;
        seg.assign(2 * sz, 0);
        for (int i = 1; i < n; i++) seg[sz + i] = llabs(d[i]);
        for (int v = sz - 1; v >= 1; v--) seg[v] = std::gcd(seg[2 * v], seg[2 * v + 1]);
    }
    void bump(int i, ll x) {
        if (i >= n) return;
        d[i] += x; bit.add(i + 1, x);
        if (i == 0) return;                           // d[0] = a[0] в дереве НОД не участвует
        int v = sz + i; seg[v] = llabs(d[i]);
        for (v >>= 1; v; v >>= 1) seg[v] = std::gcd(seg[2 * v], seg[2 * v + 1]);
    }
    void add(int l, int r, ll x) { bump(l, x); bump(r + 1, -x); }          // [l, r] += x
    ll gcd_query(int l, int r) {                                          // НОД на [l, r]
        ll g = llabs(bit.pref(l + 1));                // a_l
        ll res = 0;
        for (int lo = l + 1 + sz, hi = r + 1 + sz; lo < hi; lo >>= 1, hi >>= 1) {
            if (lo & 1) res = std::gcd(res, seg[lo++]);
            if (hi & 1) res = std::gcd(res, seg[--hi]);
        }
        return std::gcd(g, res);
    }
};

// ---------- 11. Дерево отрезков-сортировок с каскадированием: сколько чисел < x на отрезке ----------
struct MergeSortTree {
    int n; vector<vector<int>> val, toL;          // toL[v][i]: сколько из первых i элементов val[v] лежат в левом сыне
    MergeSortTree(const vector<int>& a) : n(a.size()), val(4 * a.size()), toL(4 * a.size()) { build(1, 0, n, a); }
    void build(int v, int l, int r, const vector<int>& a) {
        if (r - l == 1) { val[v] = {a[l]}; return; }
        int m = (l + r) / 2;
        build(2 * v, l, m, a); build(2 * v + 1, m, r, a);
        auto &L = val[2 * v], &R = val[2 * v + 1];
        val[v].resize(r - l); toL[v].assign(r - l + 1, 0);
        size_t i = 0, j = 0;
        for (int k = 0; k < r - l; k++) {
            bool left = j == R.size() || (i < L.size() && L[i] <= R[j]);
            val[v][k] = left ? L[i++] : R[j++];
            toL[v][k + 1] = toL[v][k] + left;
        }
    }
    int cnt(int v, int l, int r, int ql, int qr, int p) {   // p — сколько элементов вершины v меньше x
        if (qr <= l || r <= ql || p == 0) return 0;
        if (ql <= l && r <= qr) return p;
        int m = (l + r) / 2;
        return cnt(2 * v, l, m, ql, qr, toL[v][p]) + cnt(2 * v + 1, m, r, ql, qr, p - toL[v][p]);
    }
    int count_less(int ql, int qr, int x) {                 // на [ql, qr): один бинпоиск в корне, дальше O(1) на вершину
        int p = lower_bound(val[1].begin(), val[1].end(), x) - val[1].begin();
        return cnt(1, 0, n, ql, qr, p);
    }
};
// k-я порядковая статистика на [l, r): бинпоиск по ответу, O(log^2)
int kth_on_range(MergeSortTree& t, int l, int r, int k) {   // k с 1
    auto& all = t.val[1];
    int lo = 0, hi = (int)all.size() - 1;
    while (lo < hi) {
        int mid = (lo + hi) / 2;
        if (t.count_less(l, r, all[mid] + 1) >= k) hi = mid; else lo = mid + 1;
    }
    return all[lo];
}
// число различных на [l, r): считаем позиции, у которых следующее равное лежит за пределами отрезка
int distinct_on_range(MergeSortTree& tnext, int l, int r) { // tnext построено по nxt[i] = индекс следующего равного (или n)
    return (r - l) - tnext.count_less(l, r, r);
}

// ---------- 12. Бесполезные тройки (a, b, c): строго хуже другой по всем трём ----------
vector<char> dominated_3d(const vector<array<int, 3>>& p) {
    int n = p.size();
    vector<int> bs;
    for (auto& x : p) bs.push_back(x[1]);
    sort(bs.begin(), bs.end()); bs.erase(unique(bs.begin(), bs.end()), bs.end());
    int m = bs.size();
    FenwickMax f(m);                                // по «перевёрнутому» b хранит максимум c: суффикс по b
    auto rb = [&](int b) { return m - (int)(lower_bound(bs.begin(), bs.end(), b) - bs.begin()); };   // 1..m, больше b — меньше номер
    vector<int> ord(n); iota(ord.begin(), ord.end(), 0);
    sort(ord.begin(), ord.end(), [&](int x, int y) { return p[x][0] > p[y][0]; });
    vector<char> dead(n, 0);
    for (int i = 0; i < n;) {
        int j = i;
        while (j < n && p[ord[j]][0] == p[ord[i]][0]) j++;
        for (int k = i; k < j; k++) {               // сначала все запросы группы: равные a друг друга не убивают
            int id = ord[k];
            if (f.get(rb(p[id][1]) - 1) > p[id][2]) dead[id] = 1;   // есть b' > b с c' > c (c хранится +1, 0 = пусто)
        }
        for (int k = i; k < j; k++) { int id = ord[k]; f.upd(rb(p[id][1]), p[id][2]); }
        i = j;
    }
    return dead;
}

// ---------- 13. Бесполезные четвёрки (a, b, c, d): разделяй и властвуй ----------
struct Dominance4D {
    vector<array<int, 4>> P; vector<char> dead;
    Dominance4D(vector<array<int, 4>> p) : P(move(p)), dead(P.size(), 0) {   // a попарно различны
        sort(P.begin(), P.end());
        solve(0, P.size());
    }
    // возвращает индексы [l, r), отсортированные по b; дополнительно отмечает убитых «через границу» половин
    vector<int> solve(int l, int r) {
        if (r - l == 1) return {l};
        int m = (l + r) / 2;
        auto A = solve(l, m), B = solve(m, r);        // у B значения a больше, чем у A
        vector<int> mg; mg.reserve(r - l);
        size_t i = 0, j = 0;
        while (i < A.size() || j < B.size()) {        // слияние по b; при равных b правая половина идёт раньше
            if (j == B.size() || (i < A.size() && P[A[i]][1] < P[B[j]][1])) mg.push_back(A[i++]);
            else mg.push_back(B[j++]);
        }
        map<int, int> front;                          // «ступенчатый стек»: c растёт, d убывает
        for (int k = (int)mg.size() - 1; k >= 0; k--) {   // по убыванию b
            int id = mg[k], c = P[id][2], d = P[id][3];
            if (id >= m) {                            // из правой половины — добавляем в структуру
                auto it = front.lower_bound(c);
                if (it != front.end() && it->second >= d) continue;       // нас уже перекрывают
                if (it != front.end() && it->first == c) it = front.erase(it);
                while (it != front.begin() && prev(it)->second <= d) front.erase(prev(it));
                front[c] = d;
            } else {                                  // из левой — спрашиваем: есть ли c' > c и d' > d
                auto it = front.upper_bound(c);
                if (it != front.end() && it->second > d) dead[id] = 1;
            }
        }
        return mg;
    }
};

// ---------- 14. Сколько позиций i из [L, R] таковы, что отрезок a[i..R] содержит все числа от 0 до максимума ----------
// (то же самое: mex(a[i..R]) = max(a[i..R]) + 1). Оффлайн, заметаем R слева направо.
vector<int> count_full_suffixes(const vector<int>& a, const vector<pair<int, int>>& qs) {   // запросы [L, R], с 0
    int n = a.size();
    MinCount tree(vector<ll>(n, 1));                // val[i] = max(a[i..R]) + 1 - (число различных в a[i..R])
    vector<vector<pair<int, int>>> byR(n);
    for (int i = 0; i < (int)qs.size(); i++) byR[qs[i].second].push_back({qs[i].first, i});
    vector<int> ans(qs.size(), 0);
    map<int, int> last;                             // последнее вхождение числа
    vector<array<int, 3>> st;                       // стек суффиксных максимумов: {начало, конец, значение}
    for (int R = 0; R < n; R++) {
        int x = a[R];
        auto it = last.find(x);
        int prevPos = it == last.end() ? -1 : it->second;
        last[x] = R;
        tree.update(prevPos + 1, R + 1, -1);        // +1 различное для всех левых границ правее прошлого вхождения
        int start = R;
        while (!st.empty() && st.back()[2] <= x) {  // поглощаем блоки, где максимум был не больше x
            auto [s, e, v] = st.back(); st.pop_back();
            tree.update(s, e + 1, x - v);           // старый максимум v заменяется на x
            start = s;
        }
        tree.update(R, R + 1, x + 1);               // новая позиция: максимум x и константа +1
        st.push_back({start, R, x});
        for (auto [L, id] : byR[R]) {
            auto [mn, c] = tree.query(L, R + 1);
            ans[id] = mn == 0 ? (int)c : 0;
        }
    }
    return ans;
}

// ---------- 15. Разбиения на отрезки со строго возрастающим OR: динамика + заметающая прямая + Фенвик ----------
const int MOD = 998244353;
int or_partitions(const vector<int>& a) {
    int n = a.size();
    struct Grp { int x, lo, hi; };                  // OR(a[p..i]) = x для всех начал p в [lo, hi] (индексы с 1)
    vector<vector<Grp>> g(n + 1);
    vector<Grp> cur;
    for (int i = 1; i <= n; i++) {
        for (auto& e : cur) e.x |= a[i - 1];
        cur.push_back({a[i - 1], i, i});
        vector<Grp> nw;                             // склеиваем соседние группы с одинаковым OR; их не более log A
        for (auto& e : cur) {
            if (!nw.empty() && nw.back().x == e.x) nw.back().hi = e.hi; else nw.push_back(e);
        }
        cur = nw; g[i] = cur;
    }
    vector<int> xs = {-1};                          // -1 — виртуальное «предыдущее значение» для первого отрезка
    for (int i = 1; i <= n; i++) for (auto& e : g[i]) xs.push_back(e.x);
    sort(xs.begin(), xs.end()); xs.erase(unique(xs.begin(), xs.end()), xs.end());
    auto id = [&](int x) { return int(lower_bound(xs.begin(), xs.end(), x) - xs.begin()) + 1; };
    struct Qr { int i, k, sign; };                  // для dp[i][g[i][k].x] нужно прибавить sign * F(t, x)
    vector<vector<Qr>> at(n + 1);                   // at[t]: запросы с порогом t
    vector<vector<ll>> dp(n + 1);
    for (int i = 1; i <= n; i++) {
        dp[i].assign(g[i].size(), 0);
        for (int k = 0; k < (int)g[i].size(); k++) {
            at[g[i][k].hi - 1].push_back({i, k, +1});                       // j <= hi - 1
            if (g[i][k].lo - 2 >= 0) at[g[i][k].lo - 2].push_back({i, k, -1});  // j <= lo - 2
        }
    }
    Fenwick f(xs.size());                           // по значению OR храним сумму dp[j][y]
    for (int t = 0; t < n; t++) {
        if (t == 0) f.add(id(-1), 1);               // dp[0][-1] = 1
        else for (int k = 0; k < (int)g[t].size(); k++) f.add(id(g[t][k].x), dp[t][k] % MOD);
        for (auto& q : at[t]) {
            ll v = f.pref(id(g[q.i][q.k].x) - 1) % MOD;                      // сумма по y < x
            dp[q.i][q.k] = ((dp[q.i][q.k] + q.sign * v) % MOD + MOD) % MOD;
        }
    }
    ll ans = 0;
    for (ll v : dp[n]) ans = (ans + v) % MOD;
    return ans;
}

// ---------- 16. Порядковая статистика через ordered set из pb_ds ----------
typedef tree<int, null_type, less<int>, rb_tree_tag, tree_order_statistics_node_update> ordered_set;
// s.order_of_key(x)   — сколько элементов меньше x
// *s.find_by_order(k) — k-й по порядку элемент (с 0)

#ifdef TEST_MAIN
mt19937 rng(12345);
int rnd(int l, int r) { return l + (int)(rng() % (r - l + 1)); }
int main() {
    for (int it = 0; it < 300; it++) {
        int n = rnd(1, 30);
        vector<ll> a(n); for (auto& x : a) x = rnd(-20, 20);
        // 1, 9: прибавление и сумма
        LazySum ls(n); NoPushTree np(a); RangeFenwick rf(n); SegSum2n sg(a);
        for (int i = 0; i < n; i++) { ls.update(i, i + 1, a[i]); rf.add(i + 1, i + 1, a[i]); }
        vector<ll> b = a;
        for (int q = 0; q < 60; q++) {
            int l = rnd(0, n - 1), r = rnd(l, n - 1);
            if (rnd(0, 1)) { ll x = rnd(-9, 9); for (int i = l; i <= r; i++) b[i] += x; ls.update(l, r + 1, x); np.add(l, r + 1, x); rf.add(l + 1, r + 1, x); sg = SegSum2n(b); }
            else { ll s = 0; for (int i = l; i <= r; i++) s += b[i]; assert(ls.get(l, r + 1) == s); assert(np.get(l, r + 1) == s); assert(rf.get(l + 1, r + 1) == s); assert(sg.get(l, r + 1) == s); }
        }
        // 8: все ячейки используются ровно один раз
        { vector<int> seen(2 * n, 0); function<void(int,int,int)> go = [&](int x, int l, int r) { seen[x]++; if (r - l == 1) return; int m = (l + r) / 2; go(x + 1, l, m); go(x + 2 * (m - l), m, r); }; go(0, 0, n); for (int x = 0; x < 2 * n - 1; x++) assert(seen[x] == 1); assert(seen[2 * n - 1] == 0); }
    }
    // 3: площадь объединения
    for (int it = 0; it < 300; it++) {
        int k = rnd(1, 8), M = 12;
        vector<array<int, 4>> r;
        for (int i = 0; i < k; i++) { int x1 = rnd(0, M - 1), x2 = rnd(x1 + 1, M), y1 = rnd(0, M - 1), y2 = rnd(y1 + 1, M); r.push_back({x1, y1, x2, y2}); }
        vector<vector<char>> g(M, vector<char>(M, 0)); ll s = 0;
        for (auto& q : r) for (int x = q[0]; x < q[2]; x++) for (int y = q[1]; y < q[3]; y++) g[x][y] = 1;
        for (auto& row : g) for (char c : row) s += c;
        assert(union_area(r) == s);
    }
    // 4: неявное дерево
    { DynTree t((ll)1 << 60); map<ll, ll> m; vector<ll> keys;
      for (int i = 0; i < 2000; i++) { ll p = (ll)(rng() % 1000000000000000000ULL); keys.push_back(p); ll x = rnd(-5, 5); t.add(p, x); m[p] += x; }
      for (int i = 0; i < 300; i++) { ll l = keys[rnd(0, 1999)], r = keys[rnd(0, 1999)]; if (l > r) swap(l, r); ll s = 0; for (auto it = m.lower_bound(l); it != m.end() && it->first < r; ++it) s += it->second; assert(t.get(l, r) == s); }
      assert(t.t.size() < 2000 * 62 + 5); }
    // 5: Фенвик, kth
    for (int it = 0; it < 200; it++) {
        int n = rnd(1, 40); Fenwick f(n); vector<int> c(n + 1, 0);
        for (int i = 0; i < 80; i++) { int x = rnd(1, n); f.add(x, 1); c[x]++; }
        int tot = 0; for (int i = 1; i <= n; i++) tot += c[i];
        for (int k = 1; k <= tot; k++) { int s = 0, x = 0; while (s < k) s += c[++x]; assert(f.kth(k) == x); }
    }
    // 7: НОП перестановок
    for (int it = 0; it < 300; it++) {
        int n = rnd(1, 9); vector<int> p(n), q(n); iota(p.begin(), p.end(), 0); iota(q.begin(), q.end(), 0);
        shuffle(p.begin(), p.end(), rng); shuffle(q.begin(), q.end(), rng);
        vector<vector<int>> d(n + 1, vector<int>(n + 1, 0));
        for (int i = 1; i <= n; i++) for (int j = 1; j <= n; j++) d[i][j] = p[i - 1] == q[j - 1] ? d[i - 1][j - 1] + 1 : max(d[i - 1][j], d[i][j - 1]);
        assert(lcs_of_permutations(p, q) == d[n][n]);
    }
    // 10: НОД с прибавлением
    for (int it = 0; it < 300; it++) {
        int n = rnd(1, 12); vector<ll> a(n); for (auto& x : a) x = rnd(-30, 30);
        RangeAddGcd t(a);
        for (int q = 0; q < 50; q++) {
            int l = rnd(0, n - 1), r = rnd(l, n - 1);
            if (rnd(0, 1)) { ll x = rnd(-9, 9); for (int i = l; i <= r; i++) a[i] += x; t.add(l, r, x); }
            else { ll g = 0; for (int i = l; i <= r; i++) g = std::gcd(g, llabs(a[i])); assert(t.gcd_query(l, r) == g); }
        }
    }
    // 11: MST, kth, distinct
    for (int it = 0; it < 200; it++) {
        int n = rnd(1, 30); vector<int> a(n); for (auto& x : a) x = rnd(0, 9);
        MergeSortTree t(a);
        vector<int> nxt(n, n); map<int, int> lst;
        for (int i = n - 1; i >= 0; i--) { if (lst.count(a[i])) nxt[i] = lst[a[i]]; lst[a[i]] = i; }
        MergeSortTree tn(nxt);
        for (int q = 0; q < 40; q++) {
            int l = rnd(0, n - 1), r = rnd(l + 1, n), x = rnd(-1, 11);
            int c = 0; for (int i = l; i < r; i++) c += a[i] < x;
            assert(t.count_less(l, r, x) == c);
            vector<int> s(a.begin() + l, a.begin() + r); sort(s.begin(), s.end());
            int k = rnd(1, r - l); assert(kth_on_range(t, l, r, k) == s[k - 1]);
            s.erase(unique(s.begin(), s.end()), s.end()); assert(distinct_on_range(tn, l, r) == (int)s.size());
        }
    }
    // 12, 13: бесполезные тройки и четвёрки
    for (int it = 0; it < 400; it++) {
        int n = rnd(1, 25);
        vector<array<int, 3>> p(n); for (auto& x : p) x = {rnd(0, 6), rnd(0, 6), rnd(0, 6)};
        auto dead = dominated_3d(p);
        for (int i = 0; i < n; i++) { bool d = false; for (int j = 0; j < n; j++) if (p[j][0] > p[i][0] && p[j][1] > p[i][1] && p[j][2] > p[i][2]) d = true; assert(d == (bool)dead[i]); }
        vector<array<int, 4>> q(n); vector<int> pa(n); iota(pa.begin(), pa.end(), 0); shuffle(pa.begin(), pa.end(), rng);
        for (int i = 0; i < n; i++) q[i] = {pa[i], rnd(0, 6), rnd(0, 6), rnd(0, 6)};
        Dominance4D dm(q);
        for (int i = 0; i < n; i++) { bool d = false; for (int j = 0; j < n; j++) { bool all = true; for (int k = 0; k < 4; k++) if (dm.P[j][k] <= dm.P[i][k]) all = false; d |= all; } assert(d == (bool)dm.dead[i]); }
    }
    // 14: позиции, где суффикс содержит 0..max
    for (int it = 0; it < 500; it++) {
        int n = rnd(1, 14); vector<int> a(n); int top = rnd(0, 5); for (auto& x : a) x = rnd(0, top);
        vector<pair<int, int>> qs; for (int i = 0; i < 20; i++) { int l = rnd(0, n - 1); qs.push_back({l, rnd(l, n - 1)}); }
        auto res = count_full_suffixes(a, qs);
        for (size_t k = 0; k < qs.size(); k++) {
            int c = 0;
            for (int i = qs[k].first; i <= qs[k].second; i++) {
                int mx = 0; set<int> s; for (int j = i; j <= qs[k].second; j++) { mx = max(mx, a[j]); s.insert(a[j]); }
                int mex = 0; while (s.count(mex)) mex++;
                c += mex == mx + 1;
            }
            assert(res[k] == c);
        }
    }
    // 15: разбиения со строго возрастающим OR
    for (int it = 0; it < 500; it++) {
        int n = rnd(1, 14); vector<int> a(n); for (auto& x : a) x = rnd(0, 15);
        ll cnt = 0;
        for (int mask = 0; mask < (1 << (n - 1)); mask++) {
            int prev = -1, cur = 0; bool ok = true;
            for (int i = 0; i < n; i++) { cur |= a[i]; if (i == n - 1 || (mask >> i & 1)) { if (cur <= prev) ok = false; prev = cur; cur = 0; } }
            cnt += ok;
        }
        assert(or_partitions(a) == cnt % MOD);
    }
    { ordered_set s; for (int x : {5, 1, 9}) s.insert(x); assert(s.order_of_key(5) == 1 && *s.find_by_order(2) == 9); }
    puts("ok");
}
#endif
