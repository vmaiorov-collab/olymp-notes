// Прямоугольник без пробелов выложен квадратами. Известны центры (координаты удвоены, чтобы все были целыми). Восстановить стороны.
// Идём по возрастанию x центра. fen хранит для каждой строки (в удвоенных координатах) x левой границы «ещё не занятой» области.
struct Fen {                                                  // прибавление на отрезке, значение в точке
    int n; vector<long long> t;
    Fen(int n) : n(n), t(n + 2, 0) {}
    void addRange(int l, int r, long long x) { upd(l, x); upd(r + 1, -x); }       // строки l..r
    void upd(int i, long long x) { for (i++; i <= n + 1; i += i & -i) t[i] += x; }
    long long get(int i) { long long s = 0; for (i++; i > 0; i -= i & -i) s += t[i]; return s; }
};
// centers: пары (X, Y) в удвоенных координатах, height2 = 2·H. Возвращает сторону (в исходных единицах) для каждого центра по порядку ввода.
vector<long long> restoreSquares(int height2, const vector<pair<long long,long long>> &centers) {
    int m = centers.size();
    vector<int> ord(m); iota(ord.begin(), ord.end(), 0);
    sort(ord.begin(), ord.end(), [&](int a, int b) { return centers[a].first < centers[b].first; });
    Fen f(height2);
    vector<long long> side(m);
    for (int id : ord) {
        auto [X, Y] = centers[id];
        long long left = f.get((int)Y);                       // левая граница свободной области на уровне центра — левая сторона квадрата
        long long h = X - left;                               // полусторона в удвоенных единицах = сторона в исходных
        side[id] = h;
        f.addRange((int)(Y - h), (int)(Y + h - 1), 2 * h);    // теперь на этих строках граница сдвинулась до правой стороны квадрата
    }
    return side;
}
