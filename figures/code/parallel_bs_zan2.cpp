//---- bounds
// Условие «a[i] >= x» нулей и единиц: сначала false, потом true.
// Инвариант: a[l] < x (или l = -1), a[r] >= x (или r = n).
int lowerBound(const vector<int>& a, int x) {   // первый индекс i с a[i] >= x
    int l = -1, r = a.size();
    while (r - l > 1) {
        int m = (l + r) / 2;
        if (a[m] < x) l = m;                     // m «нулевой» — ответ правее
        else r = m;                              // m «единичный» — ответ в m или левее
    }
    return r;
}
int upperBound(const vector<int>& a, int x) {   // первый индекс i с a[i] > x
    int l = -1, r = a.size();
    while (r - l > 1) {
        int m = (l + r) / 2;
        if (a[m] <= x) l = m;
        else r = m;
    }
    return r;
}
int countEqual(const vector<int>& a, int x) {  // сколько раз x встречается в отсортированном a
    return upperBound(a, x) - lowerBound(a, x);
}
//---- cows
// Расставить k коров по стойлам x[0..n-1] (по возрастанию) так, чтобы минимальное расстояние было максимальным.
bool canPlace(const vector<int>& x, int k, int d) {     // можно ли расставить k коров с расстояниями >= d
    int cnt = 1, last = x[0];                            // первую корову — в первое стойло
    for (size_t i = 1; i < x.size(); i++)
        if (x[i] - last >= d) { cnt++; last = x[i]; }    // ставим жадно, как только расстояние достаточно
    return cnt >= k;
}
int maxMinDist(const vector<int>& x, int k) {           // нужно 2 <= k <= n
    int l = 0, r = x.back() - x.front() + 1;             // canPlace(l) истинно (d = 0), canPlace(r) ложно
    while (r - l > 1) {
        int m = (l + r) / 2;
        if (canPlace(x, k, m)) l = m;
        else r = m;
    }
    return l;
}
//---- real
// Корень кубический из a (a > 0) и корень квадратный: бинпоиск по вещественным, фиксированное число итераций.
double cbrtBS(double a) {
    double l = 0, r = max(1.0, a);                       // f(x)=x^3 возрастает; на [0, max(1,a)] есть искомая точка
    for (int it = 0; it < 100; it++) {
        double m = (l + r) / 2;
        if (m * m * m < a) l = m;
        else r = m;
    }
    return (l + r) / 2;
}
//---- tern
// Точка максимума строго унимодальной (сначала строго растёт, потом строго убывает) функции на [l, r].
template <class F>
double ternaryMax(F f, double l, double r) {
    for (int it = 0; it < 100; it++) {
        double m1 = l + (r - l) / 3, m2 = r - (r - l) / 3;
        if (f(m1) > f(m2)) r = m2;                       // справа от m2 максимума нет
        else l = m1;                                     // слева от m1 максимума нет
    }
    return (l + r) / 2;
}
//---- twoptr
// Есть ли в массиве НЕОТРИЦАТЕЛЬНЫХ чисел непустой подотрезок с суммой S? Возвращает [l, r) или {-1,-1}.
pair<int,int> segmentWithSum(const vector<long long>& a, long long S) {
    int n = a.size(), l = 0, r = 0;                      // отрезок [l, r), сумма cur
    long long cur = 0;
    while (true) {
        if (cur == S && r > l) return {l, r};
        if (cur < S || r == l) {                         // не хватает — расширяем вправо (пустой отрезок тоже расширяем)
            if (r == n) break;
            cur += a[r++];
        } else {                                         // cur > S — убираем левый элемент
            cur -= a[l++];
        }
    }
    return {-1, -1};
}
//---- lamps
// k фонарей радиуса R освещают дома по прямой: фонарь в точке p освещает [p-R, p+R].
bool covered(const vector<int>& h, int k, double R) {   // h отсортирован
    int used = 0;
    size_t i = 0;
    while (i < h.size()) {
        used++;
        double reach = h[i] + 2 * R;                     // фонарь ставим в h[i]+R — он закроет всё до h[i]+2R
        while (i < h.size() && h[i] <= reach + 1e-12) i++;
    }
    return used <= k;
}
double minRadius(const vector<int>& h, int k) {
    double l = 0, r = h.back() - h.front();              // при R = r хватит одного фонаря
    for (int it = 0; it < 100; it++) {
        double m = (l + r) / 2;
        if (covered(h, k, m)) r = m;
        else l = m;
    }
    return r;
}
//---- peak
// a[-1] = a[n] = -inf, соседние элементы различны. Найти i с a[i-1] < a[i] > a[i+1].
int findPeak(const vector<int>& a) {
    int l = 0, r = (int)a.size() - 1;                    // инвариант: пик есть в [l, r]
    while (l < r) {
        int m = (l + r) / 2;
        if (a[m] < a[m + 1]) l = m + 1;                  // справа выше — поднимаемся вправо
        else r = m;                                      // справа ниже — пик в [l, m]
    }
    return l;
}
//---- kth_diff
// k-я по величине (с 1) среди попарных |a[i]-a[j]|, i<j, для отсортированного a.
long long pairsAtMost(const vector<long long>& a, long long M) {   // сколько пар с a[j]-a[i] <= M
    long long cnt = 0;
    size_t i = 0;
    for (size_t j = 0; j < a.size(); j++) {              // два указателя: левый только вправо
        while (a[j] - a[i] > M) i++;
        cnt += j - i;                                    // пары (i..j-1, j)
    }
    return cnt;
}
long long kthDiff(const vector<long long>& a, long long k) {
    long long l = -1, r = a.back() - a.front();          // pairsAtMost(l) < k, pairsAtMost(r) >= k
    while (r - l > 1) {
        long long m = (l + r) / 2;
        if (pairsAtMost(a, m) >= k) r = m;
        else l = m;
    }
    return r;
}
//---- median
// f(x) = sum |x - p_i|: выпуклая; минимум в медиане.
long long sumDist(const vector<long long>& p, long long x) {
    long long s = 0;
    for (long long v : p) s += llabs(x - v);
    return s;
}
// Бинпоиск по знаку разности f(x+1) - f(x): она не убывает (функция выпукла).
long long argminSum(const vector<long long>& p, long long lo, long long hi) {
    while (lo < hi) {
        long long m = lo + (hi - lo) / 2;
        if (sumDist(p, m + 1) - sumDist(p, m) >= 0) hi = m;   // дальше только хуже — минимум в [lo, m]
        else lo = m + 1;
    }
    return lo;
}
//---- workers
// Нанять w рабочих стоит K каждому; заказ из n изделий, один рабочий делает изделие за t. Штраф — (время)^2.
// cost(w) = K*w + (ceil(n/w)*t)^2. Перебираем блоки с одинаковым ceil(n/w): в блоке берём наименьшее w.
long long minCost(long long n, long long K, long long t) {
    long long best = LLONG_MAX;
    for (long long w = 1; w <= n; ) {
        long long c = (n + w - 1) / w;                   // ceil(n/w)
        best = min(best, K * w + (c * t) * (c * t));
        // следующий w, при котором ceil(n/w) станет меньше c
        long long nw = (c == 1) ? n + 1 : (n + c - 2) / (c - 1);
        if (nw <= w) nw = w + 1;
        w = nw;
    }
    return best;
}
//---- mex
// Запросы mex на отрезках; считаем, что отрезки идут подряд и сдвиги границ суммарно невелики.
struct MexSet {
    int n; vector<int> cnt; set<int> missing;
    MexSet(int n) : n(n), cnt(n + 2, 0) { for (int v = 0; v <= n + 1; v++) missing.insert(v); }
    void add(int v) { if (v <= n + 1 && cnt[v]++ == 0) missing.erase(v); }
    void del(int v) { if (v <= n + 1 && --cnt[v] == 0) missing.insert(v); }
    int mex() const { return *missing.begin(); }
};
vector<int> mexQueries(const vector<int>& a, const vector<pair<int,int>>& q) {   // отрезки [l, r), заданные подряд
    MexSet s(a.size());
    int L = 0, R = 0;
    vector<int> ans;
    for (auto [l, r] : q) {
        while (R < r) s.add(a[R++]);                     // сначала расширяем, потом сужаем — счётчики не уходят в минус
        while (L > l) s.add(a[--L]);
        while (R > r) s.del(a[--R]);
        while (L < l) s.del(a[L++]);
        ans.push_back(s.mex());
    }
    return ans;
}
