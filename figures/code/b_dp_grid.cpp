// Сетка n×m, стоимость шага из клетки со значением a в клетку со значением b равна (a − b)^X, X нечётно. Запрос: минимальная стоимость пути между клетками.
// Нечётная степень ⇒ стоимость обратного шага противоположна. Если все циклы 2×2 имеют нулевую стоимость, то стоимость пути зависит только от концов.
typedef long long ll;
ll ipow(ll b, int e) { ll r = 1; while (e--) r *= b; return r; }
struct GridCost {
    int n, m, X; bool valid = true;
    vector<vector<int>> a;
    vector<vector<ll>> rowPref, colPref;                       // rowPref[i][j]: цена пути по строке i от столбца 0 до j; colPref[i][j]: по столбцу j от строки 0 до i
    GridCost(vector<vector<int>> g, int X) : n(g.size()), m(g[0].size()), X(X), a(g) {
        for (int i = 0; i + 1 < n && valid; i++)
            for (int j = 0; j + 1 < m; j++) {                  // цикл (i,j) → (i,j+1) → (i+1,j+1) → (i+1,j) → (i,j)
                ll c = ipow(a[i][j] - a[i][j + 1], X) + ipow(a[i][j + 1] - a[i + 1][j + 1], X)
                     + ipow(a[i + 1][j + 1] - a[i + 1][j], X) + ipow(a[i + 1][j] - a[i][j], X);
                if (c != 0) { valid = false; break; }          // цикл ненулевого веса: пройдя его в нужную сторону бесконечно, получаем −∞
            }
        rowPref.assign(n, vector<ll>(m, 0)); colPref.assign(n, vector<ll>(m, 0));
        for (int i = 0; i < n; i++) for (int j = 1; j < m; j++) rowPref[i][j] = rowPref[i][j - 1] + ipow(a[i][j - 1] - a[i][j], X);
        for (int j = 0; j < m; j++) for (int i = 1; i < n; i++) colPref[i][j] = colPref[i - 1][j] + ipow(a[i - 1][j] - a[i][j], X);
    }
    // стоимость пути из (r1,c1) в (r2,c2): сначала по строке r1 до столбца c2, затем по столбцу c2 до строки r2
    bool query(int r1, int c1, int r2, int c2, ll &res) {
        if (!valid) return false;
        res = (rowPref[r1][c2] - rowPref[r1][c1]) + (colPref[r2][c2] - colPref[r1][c2]);
        return true;
    }
};
