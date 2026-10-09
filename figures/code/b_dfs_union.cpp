// Сколько целых точек покрыто объединением горизонтальных и вертикальных отрезков (концы включены).
struct Seg { int x1, y1, x2, y2; };
long long unionSize(const vector<Seg> &segs) {
    map<int, vector<pair<int,int>>> hor, ver;                 // горизонтальные по y, вертикальные по x
    for (auto s : segs) {
        if (s.y1 == s.y2) hor[s.y1].push_back({min(s.x1, s.x2), max(s.x1, s.x2)});   // точка считается горизонтальным отрезком
        else ver[s.x1].push_back({min(s.y1, s.y2), max(s.y1, s.y2)});
    }
    auto mergeAll = [](map<int, vector<pair<int,int>>> &m) {  // на каждой прямой объединяем пересекающиеся отрезки
        for (auto &[line, v] : m) {
            sort(v.begin(), v.end());
            vector<pair<int,int>> r;
            for (auto p : v) { if (!r.empty() && p.first <= r.back().second) r.back().second = max(r.back().second, p.second); else r.push_back(p); }
            v = r;
        }
    };
    mergeAll(hor); mergeAll(ver);
    long long total = 0;
    for (auto &[l, v] : hor) for (auto p : v) total += p.second - p.first + 1;
    for (auto &[l, v] : ver) for (auto p : v) total += p.second - p.first + 1;
    // |A ∪ B| = |A| + |B| − |A ∩ B|; после склейки горизонтальный и вертикальный отрезки пересекаются не более чем в одной точке
    vector<int> ys;
    for (auto &[y, v] : hor) ys.push_back(y);                 // сжатие по y (достаточно y горизонтальных)
    struct Ev { int x, type, a, b; };                         // type 0: горизонтальный начался (+1 в y), 1: закончился (−1), 2: запрос вертикального
    vector<Ev> ev;
    for (auto &[y, v] : hor) for (auto p : v) { ev.push_back({p.first, 0, y, y}); ev.push_back({p.second + 1, 1, y, y}); }
    for (auto &[x, v] : ver) for (auto p : v) ev.push_back({x, 2, p.first, p.second});
    sort(ev.begin(), ev.end(), [](const Ev &l, const Ev &r) { return make_pair(l.x, l.type) < make_pair(r.x, r.type); });   // сначала добавления/удаления, потом запросы
    int m = ys.size();
    vector<int> bit(m + 1, 0);
    auto add = [&](int i, int d) { for (i++; i <= m; i += i & -i) bit[i] += d; };
    auto pref = [&](int i) { int r = 0; for (; i > 0; i -= i & -i) r += bit[i]; return r; };
    long long cross = 0;
    for (auto &e : ev) {
        if (e.type < 2) add(lower_bound(ys.begin(), ys.end(), e.a) - ys.begin(), e.type == 0 ? 1 : -1);
        else cross += pref(upper_bound(ys.begin(), ys.end(), e.b) - ys.begin()) - pref(lower_bound(ys.begin(), ys.end(), e.a) - ys.begin());
    }
    return total - cross;
}
