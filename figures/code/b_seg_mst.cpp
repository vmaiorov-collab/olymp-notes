// Merge Sort Tree: в вершине — отсортированный массив её отрезка. Память O(n log n).
struct MergeSortTree {
    int n; vector<vector<int>> t;
    MergeSortTree(const vector<int> &a) : n(a.size()), t(4 * a.size()) { build(1, 0, n, a); }
    void build(int v, int l, int r, const vector<int> &a) {
        if (l + 1 == r) { t[v] = {a[l]}; return; }
        int m = (l + r) / 2;
        build(2 * v, l, m, a); build(2 * v + 1, m, r, a);
        t[v].resize(r - l);
        merge(t[2 * v].begin(), t[2 * v].end(), t[2 * v + 1].begin(), t[2 * v + 1].end(), t[v].begin());   // слияние как в сортировке
    }
    int countLess(int v, int l, int r, int ql, int qr, int x) {     // сколько чисел < x на [ql, qr):  O(log² n)
        if (qr <= l || r <= ql) return 0;
        if (ql <= l && r <= qr) return lower_bound(t[v].begin(), t[v].end(), x) - t[v].begin();   // бинпоиск внутри вершины
        int m = (l + r) / 2;
        return countLess(2 * v, l, m, ql, qr, x) + countLess(2 * v + 1, m, r, ql, qr, x);
    }
};
// Количество различных на [l, r): prev[i] — позиция предыдущего такого же (или -1); различных = #{i in [l,r): prev[i] < l}
int countDistinct(const MergeSortTree &T, int l, int r) { return const_cast<MergeSortTree&>(T).countLess(1, 0, T.n, l, r, l); }
vector<int> prevEqual(const vector<int> &a) {
    map<int,int> last; vector<int> p(a.size());
    for (int i = 0; i < (int)a.size(); i++) { auto it = last.find(a[i]); p[i] = it == last.end() ? -1 : it->second; last[a[i]] = i; }
    return p;
}
