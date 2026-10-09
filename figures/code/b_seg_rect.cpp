// Для каждого прямоугольника — число точек внутри (включая границу). Офлайн: заметающая прямая по x + Фенвик по y.
struct Rect { int x1, y1, x2, y2; };
vector<long long> pointsInRects(vector<pair<int,int>> pts, const vector<Rect> &rs) {
    vector<int> ys; for (auto &p : pts) ys.push_back(p.second);
    sort(ys.begin(), ys.end()); ys.erase(unique(ys.begin(), ys.end()), ys.end());     // сжатие по y
    int m = ys.size();
    vector<int> bit(m + 1, 0);
    auto add = [&](int i) { for (i++; i <= m; i += i & -i) bit[i]++; };
    auto pref = [&](int i) { int r = 0; for (; i > 0; i -= i & -i) r += bit[i]; return r; };  // число точек с индексом y < i
    struct Ev { int x, type, id; };                          // type 0: добавить точку, 1: запрос «до x1», 2: запрос «до x2»
    vector<Ev> ev;
    for (int i = 0; i < (int)pts.size(); i++) ev.push_back({pts[i].first, 0, i});
    for (int i = 0; i < (int)rs.size(); i++) { ev.push_back({rs[i].x1 - 1, 1, i}); ev.push_back({rs[i].x2, 2, i}); }
    sort(ev.begin(), ev.end(), [](const Ev &a, const Ev &b) { return make_pair(a.x, a.type) < make_pair(b.x, b.type); });  // при равных x точки раньше запросов
    vector<long long> ans(rs.size(), 0);
    for (auto &e : ev) {
        if (e.type == 0) { add(lower_bound(ys.begin(), ys.end(), pts[e.id].second) - ys.begin()); continue; }
        const Rect &r = rs[e.id];
        int lo = lower_bound(ys.begin(), ys.end(), r.y1) - ys.begin();
        int hi = upper_bound(ys.begin(), ys.end(), r.y2) - ys.begin();
        long long c = pref(hi) - pref(lo);                   // точки с x <= текущего и y в [y1, y2]
        ans[e.id] += (e.type == 2 ? c : -c);                 // запрос до x2 даём со знаком «+», до x1-1 — «−»
    }
    return ans;
}
