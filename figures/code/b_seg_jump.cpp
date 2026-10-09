// Прыжки на 1 или 2 клетки вправо, у клеток «монеты» v[i] (могут быть отрицательными).
// Максимальная сумма пути из l в r.  Переход через клетку i:  d_i = v_i + max(d_{i-1}, d_{i-2}) — это матрица в полукольце (max, +).
const long long NEG = LLONG_MIN / 4;
struct Mat {                                                  // [[a b],[c d]] в (max, +)
    long long a, b, c, d;
};
Mat mul(const Mat &x, const Mat &y) {                         // сначала x, потом y (строка-вектор · x · y); не коммутативно
    auto mx = [](long long p, long long q) { return max(max(p, q), NEG); };
    return {mx(x.a + y.a, x.b + y.c), mx(x.a + y.b, x.b + y.d),
            mx(x.c + y.a, x.d + y.c), mx(x.c + y.b, x.d + y.d)};
}
Mat step(long long v) { return {v, 0, v, NEG}; }              // строка (d_{i-1}, d_{i-2}) → (d_i, d_{i-1}): d_i = v + max(d_{i-1}, d_{i-2}), d_{i-1} сохраняется
const Mat ID = {0, NEG, NEG, 0};
struct JumpTree {
    int n; vector<Mat> t;
    JumpTree(const vector<long long> &v) : n(v.size()), t(4 * v.size()) { build(1, 0, n, v); }
    void build(int x, int l, int r, const vector<long long> &v) {
        if (l + 1 == r) { t[x] = step(v[l]); return; }
        int m = (l + r) / 2; build(2 * x, l, m, v); build(2 * x + 1, m, r, v);
        t[x] = mul(t[2 * x], t[2 * x + 1]);
    }
    Mat get(int x, int l, int r, int ql, int qr) {
        if (qr <= l || r <= ql) return ID;
        if (ql <= l && r <= qr) return t[x];
        int m = (l + r) / 2; return mul(get(2 * x, l, m, ql, qr), get(2 * x + 1, m, r, ql, qr));
    }
    void update(int x, int l, int r, int pos, long long val) {
        if (l + 1 == r) { t[x] = step(val); return; }
        int m = (l + r) / 2; if (pos < m) update(2 * x, l, m, pos, val); else update(2 * x + 1, m, r, pos, val);
        t[x] = mul(t[2 * x], t[2 * x + 1]);
    }
    long long best(const vector<long long> &v, int l, int r) {   // путь из клетки l в клетку r (l <= r)
        if (l == r) return v[l];
        Mat M = get(1, 0, n, l + 1, r + 1);                     // клетки l+1..r
        // начальное состояние после клетки l:  (d_l, d_{l-1}) = (v_l, -inf);  ответ — d_r
        return max(v[l] + M.a, NEG + M.c);                           // первая компонента строки (v_l, -inf) · M
    }
};
