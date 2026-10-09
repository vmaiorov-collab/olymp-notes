// Ладьи: прямоугольник «полностью под боем» ⇔ в каждой строке есть ладья ИЛИ в каждом столбце есть ладья (внутри прямоугольника).
// Заметающая прямая по x; дерево на минимум по y хранит x последней ладьи в этой строке (0 — не было).
struct Q { int x1, y1, x2, y2; };
vector<bool> everyRowHasRook(int n, const vector<pair<int,int>> &rooks, const vector<Q> &qs) {
    int sz = 1; while (sz < n + 1) sz <<= 1;
    vector<int> t(2 * sz, 0);                                // t[y + sz] = x последней ладьи на строке y
    auto setv = [&](int y, int x) { for (y += sz, t[y] = x; y > 1; y >>= 1) t[y >> 1] = min(t[y], t[y ^ 1]); };
    auto getmin = [&](int l, int r) { int res = INT_MAX; for (l += sz, r += sz; l < r; l >>= 1, r >>= 1) { if (l & 1) res = min(res, t[l++]); if (r & 1) res = min(res, t[--r]); } return res; };
    vector<int> orderR(rooks.size()), orderQ(qs.size());
    iota(orderR.begin(), orderR.end(), 0); iota(orderQ.begin(), orderQ.end(), 0);
    sort(orderR.begin(), orderR.end(), [&](int a, int b) { return rooks[a].first < rooks[b].first; });
    sort(orderQ.begin(), orderQ.end(), [&](int a, int b) { return qs[a].x2 < qs[b].x2; });
    vector<bool> res(qs.size());
    size_t p = 0;
    for (int qi : orderQ) {
        while (p < orderR.size() && rooks[orderR[p]].first <= qs[qi].x2) { setv(rooks[orderR[p]].second, rooks[orderR[p]].first); p++; }
        res[qi] = getmin(qs[qi].y1, qs[qi].y2 + 1) >= qs[qi].x1;      // у каждой строки последняя ладья не левее x1
    }
    return res;
}
vector<bool> rooksCovered(int n, vector<pair<int,int>> rooks, vector<Q> qs) {
    vector<bool> a = everyRowHasRook(n, rooks, qs);
    for (auto &r : rooks) swap(r.first, r.second);           // то же самое для столбцов: меняем x и y местами
    for (auto &q : qs) { swap(q.x1, q.y1); swap(q.x2, q.y2); }
    vector<bool> b = everyRowHasRook(n, rooks, qs);
    for (size_t i = 0; i < a.size(); i++) a[i] = a[i] || b[i];
    return a;
}
