// Wavelet Tree: вершина отвечает за диапазон ЗНАЧЕНИЙ [lo, hi]; хранит, сколько из первых i элементов ушло влево (значение <= mid).
struct Wavelet {
    struct Node { int lo, hi; vector<int> toLeft; int L = -1, R = -1; };
    vector<Node> t;
    Wavelet(const vector<int> &a, int lo, int hi) { build(a, lo, hi); }
    int build(const vector<int> &a, int lo, int hi) {
        int id = t.size(); t.push_back({lo, hi, {}});
        if (lo == hi || a.empty()) return id;
        int mid = (lo + hi) / 2;
        vector<int> left, right, pref(1, 0);
        for (int x : a) { (x <= mid ? left : right).push_back(x); pref.push_back(pref.back() + (x <= mid)); }   // сохраняем относительный порядок
        t[id].toLeft = pref;
        int l = build(left, lo, mid), r = build(right, mid + 1, hi);
        t[id].L = l; t[id].R = r;
        return id;
    }
    // сколько чисел < x среди позиций [l, r) (в терминах исходного массива)
    int countLess(int id, int l, int r, int x) {
        if (l >= r) return 0;
        Node &nd = t[id];
        if (x <= nd.lo) return 0;
        if (nd.hi < x) return r - l;                         // диапазон значений целиком меньше x: берём весь текущий отрезок
        int mid = (nd.lo + nd.hi) / 2;
        int ll = nd.toLeft[l], lr = nd.toLeft[r];            // отрезок в левом ребёнке: [ll, lr)
        return countLess(nd.L, ll, lr, x) + countLess(nd.R, l - ll, r - lr, x);
    }
    // k-я по величине (k с 0) среди [l, r) — спуск по дереву
    int kth(int id, int l, int r, int k) {
        Node &nd = t[id];
        if (nd.lo == nd.hi) return nd.lo;
        int ll = nd.toLeft[l], lr = nd.toLeft[r], inLeft = lr - ll;
        if (k < inLeft) return kth(nd.L, ll, lr, k);
        return kth(nd.R, l - ll, r - lr, k - inLeft);
    }
};
