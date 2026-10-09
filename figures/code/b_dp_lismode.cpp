// Для каждого элемента: 0 — не лежит ни в одной НВП, 1 — лежит в некоторых, 2 — лежит во всех НВП (максимальной длины).
// Считаем (длина лучшей НВП, число таких НВП) на конце и на начале в каждой позиции Фенвиком по сжатым значениям (максимум пары с суммой количеств).
// Количества огромны: сравниваем произведение с общим числом по нескольким простым модулям.
typedef long long ll;
typedef unsigned long long ull;
const ll MODS[3] = {1000000007LL, 998244353LL, 1000000009LL};
struct Cell { int len = 0; ll cnt[3] = {0, 0, 0}; };
Cell better(const Cell &x, const Cell &y) {                    // объединение: большая длина побеждает, при равенстве количества складываются
    if (x.len != y.len) return x.len > y.len ? x : y;
    Cell r = x; for (int k = 0; k < 3; k++) r.cnt[k] = (x.cnt[k] + y.cnt[k]) % MODS[k];
    return r;
}
struct FenMax {
    int n; vector<Cell> t;
    FenMax(int n) : n(n), t(n + 1) {}
    void add(int i, const Cell &c) { for (i++; i <= n; i += i & -i) t[i] = better(t[i], c); }
    Cell pref(int i) { Cell r; for (; i > 0; i -= i & -i) r = better(r, t[i]); return r; }     // значения с индексом < i
};
vector<int> lisModes(vector<int> a) {
    int n = a.size();
    vector<int> s(a); sort(s.begin(), s.end()); s.erase(unique(s.begin(), s.end()), s.end());
    for (int &x : a) x = lower_bound(s.begin(), s.end(), x) - s.begin();
    int m = s.size();
    vector<Cell> L(n), R(n);
    { FenMax f(m); for (int i = 0; i < n; i++) {                // L[i]: НВП, заканчивающиеся в a[i]
        Cell c = f.pref(a[i]); if (c.len == 0) { c.len = 0; for (int k = 0; k < 3; k++) c.cnt[k] = 1; }
        c.len++; L[i] = c; f.add(a[i], c); } }
    { FenMax f(m); for (int i = n - 1; i >= 0; i--) {           // R[i]: НВП, начинающиеся в a[i] (идём справа налево по убыванию)
        Cell c = f.pref(m - 1 - a[i]); if (c.len == 0) { c.len = 0; for (int k = 0; k < 3; k++) c.cnt[k] = 1; }
        c.len++; R[i] = c; f.add(m - 1 - a[i], c); } }
    int best = 0; Cell tot;
    for (int i = 0; i < n; i++) tot = better(tot, L[i]);
    best = tot.len;
    vector<int> mode(n, 0);
    for (int i = 0; i < n; i++) {
        if (L[i].len + R[i].len - 1 != best) continue;          // даже лучшая цепочка через a[i] короче НВП
        bool all = true;
        for (int k = 0; k < 3; k++) if (L[i].cnt[k] * R[i].cnt[k] % MODS[k] != tot.cnt[k]) all = false;
        mode[i] = all ? 2 : 1;
    }
    return mode;
}
