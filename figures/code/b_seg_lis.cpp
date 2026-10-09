// Максимум на префиксе: нижнее (итеративное) дерево отрезков, значения 0..m-1
struct MaxTree {
    int sz; vector<int> t;
    MaxTree(int m) { sz = 1; while (sz < m) sz <<= 1; t.assign(2 * sz, 0); }
    void chmax(int i, int v) { for (i += sz, t[i] = max(t[i], v); i > 1; i >>= 1) t[i >> 1] = max(t[i], t[i ^ 1]); }
    int query(int l, int r) {                                // максимум на [l, r)
        int res = 0;
        for (l += sz, r += sz; l < r; l >>= 1, r >>= 1) {
            if (l & 1) res = max(res, t[l++]);
            if (r & 1) res = max(res, t[--r]);
        }
        return res;
    }
};
// Длина наибольшей строго возрастающей подпоследовательности, O(n log n)
int lis(vector<int> a) {
    vector<int> s(a); sort(s.begin(), s.end()); s.erase(unique(s.begin(), s.end()), s.end());
    for (int &x : a) x = lower_bound(s.begin(), s.end(), x) - s.begin();        // сжатие: числа в 0..m-1
    MaxTree T(s.size());
    int best = 0;
    for (int x : a) {
        int len = T.query(0, x) + 1;                         // лучшая цепочка из чисел < x, плюс сам x
        T.chmax(x, len);                                     // в ячейке x — длина лучшей цепочки, заканчивающейся на x
        best = max(best, len);
    }
    return best;
}
// НОП двух перестановок: сопоставим элементу a[i] его позицию в b — общая подпоследовательность превращается в возрастающую
int lcsPermutations(const vector<int> &a, const vector<int> &b) {
    int n = a.size(); vector<int> posB(n + 1), c(n);
    for (int i = 0; i < n; i++) posB[b[i]] = i;
    for (int i = 0; i < n; i++) c[i] = posB[a[i]];
    return lis(c);
}
