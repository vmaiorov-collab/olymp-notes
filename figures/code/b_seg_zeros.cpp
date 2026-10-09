// Узел: самая длинная серия нулей на отрезке. Склейка двух соседних отрезков — «сложение».
struct Node {
    int len = 0;              // длина отрезка
    int pre = 0, suf = 0;     // самый длинный префикс / суффикс из нулей
    int best = 0;             // самая длинная серия нулей внутри
    bool all = true;          // весь отрезок состоит из нулей
};
Node merge(const Node &a, const Node &b) {
    Node r;
    r.len  = a.len + b.len;
    r.pre  = a.all ? a.len + b.pre : a.pre;                 // префикс продолжается в правую часть, если левая вся нулевая
    r.suf  = b.all ? b.len + a.suf : b.suf;
    r.best = max({a.best, b.best, a.suf + b.pre});          // внутри левой, внутри правой или через границу
    r.all  = a.all && b.all;
    return r;
}
Node leaf(int v) { return v == 0 ? Node{1, 1, 1, 1, true} : Node{1, 0, 0, 0, false}; }
const Node NEUTRAL = {0, 0, 0, 0, true};                    // «пустой отрезок»: merge(NEUTRAL, x) = x

struct SegTree {                                            // дерево на полуинтервалах [l, r), корень — вершина 1
    int n; vector<Node> t;
    SegTree(const vector<int> &a) : n(a.size()), t(4 * a.size()) { build(1, 0, n, a); }
    void build(int v, int l, int r, const vector<int> &a) {
        if (l + 1 == r) { t[v] = leaf(a[l]); return; }
        int m = (l + r) / 2;
        build(2 * v, l, m, a); build(2 * v + 1, m, r, a);
        t[v] = merge(t[2 * v], t[2 * v + 1]);
    }
    Node get(int v, int l, int r, int ql, int qr) {         // [ql, qr)
        if (qr <= l || r <= ql) return NEUTRAL;
        if (ql <= l && r <= qr) return t[v];
        int m = (l + r) / 2;
        return merge(get(2 * v, l, m, ql, qr), get(2 * v + 1, m, r, ql, qr));
    }
    void update(int v, int l, int r, int pos, int val) {
        if (l + 1 == r) { t[v] = leaf(val); return; }
        int m = (l + r) / 2;
        if (pos < m) update(2 * v, l, m, pos, val); else update(2 * v + 1, m, r, pos, val);
        t[v] = merge(t[2 * v], t[2 * v + 1]);               // пересчёт на обратном пути
    }
};
