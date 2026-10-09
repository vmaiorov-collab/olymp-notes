// Есть ли два равных числа на отрезке [l, r)?  Храним nxt[i] — позицию следующего равного (или n), дерево на минимум.
struct EqualQuery {
    int n, sz; vector<int> a, t;                            // t — нижний (итеративный) вариант дерева на минимум
    map<int, set<int>> pos;
    EqualQuery(const vector<int> &arr) : n(arr.size()), a(arr) {
        sz = 1; while (sz < n) sz <<= 1;
        t.assign(2 * sz, n);
        for (int i = 0; i < n; i++) pos[a[i]].insert(i);
        for (int i = 0; i < n; i++) setNxt(i);
    }
    int nxtOf(int i) { auto &s = pos[a[i]]; auto it = s.upper_bound(i); return it == s.end() ? n : *it; }
    void setNxt(int i) {
        int p = i + sz; t[p] = nxtOf(i);
        for (p >>= 1; p; p >>= 1) t[p] = min(t[2 * p], t[2 * p + 1]);
    }
    void change(int i, int y) {                              // a[i] = y: «перевешиваем» односвязные списки двух значений
        auto &sx = pos[a[i]];
        auto it = sx.find(i);
        int prv = (it == sx.begin()) ? -1 : *prev(it);       // предыдущий равный старому значению
        sx.erase(it);
        if (prv >= 0) setNxt(prv);                           // он теперь указывает на следующий после i
        a[i] = y;
        auto &sy = pos[y];
        auto jt = sy.insert(i).first;
        if (jt != sy.begin()) setNxt(*prev(jt));             // предыдущий равный новому значению теперь указывает на i
        setNxt(i);
    }
    bool hasEqual(int l, int r) {                            // минимум nxt на [l, r) должен быть < r
        int res = n;
        for (int lo = l + sz, hi = r + sz; lo < hi; lo >>= 1, hi >>= 1) {
            if (lo & 1) res = min(res, t[lo++]);
            if (hi & 1) res = min(res, t[--hi]);
        }
        return res < r;
    }
};
