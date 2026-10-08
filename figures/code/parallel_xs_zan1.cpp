//---- fenwick
struct Fenwick {                                 // сумма на префиксе, добавление в точке; индексы с 0
    int n; vector<long long> t;
    Fenwick(int n = 0) : n(n), t(n + 1, 0) {}
    void add(int i, long long x) { for (i++; i <= n; i += i & -i) t[i] += x; }
    long long pref(int i) {                      // сумма на [0, i]; pref(-1) = 0
        long long s = 0;
        for (i++; i > 0; i -= i & -i) s += t[i];
        return s;
    }
};
//---- binup
const int N = 200000, LG = 18;
vector<int> g[N];
int up[LG][N];                                   // up[j][v] — предок на 2^j выше; у корня это он сам
int h[N], tin[N], tout[N], T;

void dfs(int v, int p) {                         // вызов: dfs(0, 0)
    tin[v] = T++;
    up[0][v] = p;
    h[v] = (p == v ? 0 : h[p] + 1);
    for (int j = 1; j < LG; j++) up[j][v] = up[j - 1][up[j - 1][v]];   // предки уже посчитаны
    for (int u : g[v]) if (u != p) dfs(u, v);
    tout[v] = T++;
}
int jump(int v, int k) {                         // предок на k выше (k < 2^LG)
    for (int j = 0; j < LG; j++) if (k >> j & 1) v = up[j][v];
    return v;
}
bool anc(int a, int b) {                         // a — предок b (или сама b)
    return tin[a] <= tin[b] && tout[b] <= tout[a];
}
int lca1(int u, int v) {                         // способ 1: проверка «является ли предком»
    if (anc(v, u)) return v;
    for (int j = LG - 1; j >= 0; j--)
        if (!anc(up[j][v], u)) v = up[j][v];     // прыгаем, пока не попали в предка u
    return up[0][v];
}
int lca2(int u, int v) {                         // способ 2: выровнять высоты, прыгать одновременно
    if (h[u] < h[v]) swap(u, v);
    u = jump(u, h[u] - h[v]);
    if (u == v) return u;
    for (int j = LG - 1; j >= 0; j--)
        if (up[j][u] != up[j][v]) u = up[j][u], v = up[j][v];
    return up[0][u];
}
//---- binup_min
const int INF = 1e9;
int w[N];                                        // w[v] — вес ребра (v, родитель); у корня INF
int mn[LG][N];                                   // mn[j][v] — минимум на 2^j рёбрах вверх от v
// заполняется в dfs после up[j][v]:
//   mn[0][v] = w[v];
//   mn[j][v] = min(mn[j-1][v], mn[j-1][up[j-1][v]]);
int pathMin(int v, int k) {                      // минимум на k рёбрах вверх от v
    int res = INF;
    for (int j = 0; j < LG; j++)
        if (k >> j & 1) res = min(res, mn[j][v]), v = up[j][v];
    return res;
}
//---- sparse
const int N = 1 << 17, LG = 18;
int lg[N + 1], sp[LG][N];
void build(const vector<int>& a) {               // O(n log n) по времени и памяти
    int n = a.size();
    for (int i = 2; i <= n; i++) lg[i] = lg[i / 2] + 1;   // lg[i] = ⌊log2 i⌋
    for (int i = 0; i < n; i++) sp[0][i] = a[i];
    for (int j = 1; (1 << j) <= n; j++)
        for (int i = 0; i + (1 << j) <= n; i++)
            sp[j][i] = min(sp[j - 1][i], sp[j - 1][i + (1 << (j - 1))]);
}
int query(int l, int r) {                        // минимум на [l, r] включительно, O(1)
    int j = lg[r - l + 1];                       // два отрезка длины 2^j перекрываются и покрывают [l, r]
    return min(sp[j][l], sp[j][r - (1 << j) + 1]);
}
//---- sparse2d
struct Sparse2D {
    int n, m; vector<int> lg;
    vector<vector<vector<vector<int>>>> t;       // t[k][l][i][j] — минимум в прямоугольнике 2^k × 2^l с углом (i, j)
    Sparse2D(const vector<vector<int>>& a) : n(a.size()), m(a[0].size()) {
        lg.assign(max(n, m) + 1, 0);
        for (int i = 2; i < (int)lg.size(); i++) lg[i] = lg[i / 2] + 1;
        int K = lg[n] + 1, L = lg[m] + 1;
        t.assign(K, vector<vector<vector<int>>>(L));
        for (int k = 0; k < K; k++)
            for (int l = 0; l < L; l++) {
                int H = n - (1 << k) + 1, W = m - (1 << l) + 1;
                t[k][l].assign(H, vector<int>(W));
                for (int i = 0; i < H; i++)
                    for (int j = 0; j < W; j++) {
                        if (k > 0)      t[k][l][i][j] = min(t[k - 1][l][i][j], t[k - 1][l][i + (1 << (k - 1))][j]);
                        else if (l > 0) t[k][l][i][j] = min(t[k][l - 1][i][j], t[k][l - 1][i][j + (1 << (l - 1))]);
                        else            t[k][l][i][j] = a[i][j];
                    }
            }
    }
    int query(int x1, int y1, int x2, int y2) {  // прямоугольник [x1..x2] × [y1..y2], включительно
        int k = lg[x2 - x1 + 1], l = lg[y2 - y1 + 1];
        int x3 = x2 - (1 << k) + 1, y3 = y2 - (1 << l) + 1;
        return min({t[k][l][x1][y1], t[k][l][x3][y1], t[k][l][x1][y3], t[k][l][x3][y3]});
    }
};
//---- euler
const int N = 100000, LG = 18;
vector<int> g[N];
int h[N], firstPos[N], lg[2 * N + 1];
vector<pair<int, int>> ord;                      // (высота, вершина) в порядке обхода, длина 2n − 1
pair<int, int> sp[LG][2 * N];

void dfs(int v, int p) {
    firstPos[v] = ord.size();
    ord.push_back({h[v], v});
    for (int u : g[v]) if (u != p) {
        h[u] = h[v] + 1;
        dfs(u, v);
        ord.push_back({h[v], v});                // возвращаемся в v после каждого ребёнка
    }
}
void build() {
    dfs(0, -1);
    int m = ord.size();
    for (int i = 2; i <= m; i++) lg[i] = lg[i / 2] + 1;
    for (int i = 0; i < m; i++) sp[0][i] = ord[i];
    for (int j = 1; (1 << j) <= m; j++)
        for (int i = 0; i + (1 << j) <= m; i++)
            sp[j][i] = min(sp[j - 1][i], sp[j - 1][i + (1 << (j - 1))]);
}
int lca(int u, int v) {                          // O(1): вершина минимальной высоты между первыми вхождениями
    int l = firstPos[u], r = firstPos[v];
    if (l > r) swap(l, r);
    int j = lg[r - l + 1];
    return min(sp[j][l], sp[j][r - (1 << j) + 1]).second;
}
//---- fenwick_path
// tin, tout (времена из [0, 2n)), lca1 — из «binup»; Fenwick — из «fenwick»
struct RootSum {
    Fenwick fw;
    RootSum(int n) : fw(2 * n) {}
    void add(int v, long long x) { fw.add(tin[v], x); fw.add(tout[v], -x); }   // +x при входе, −x при выходе
    long long get(int v) { return fw.pref(tin[v]); }                           // сумма по предкам v (включая v)
};
// 1) значение в вершине += x, сумма на пути u–v
RootSum vals(N);  long long val[N];
void addValue(int v, long long x) { vals.add(v, x); val[v] += x; }
long long pathSum(int u, int v) {
    int l = lca1(u, v);
    return vals.get(u) + vals.get(v) - 2 * vals.get(l) + val[l];   // l учтена дважды лишнего, вернём её значение
}
// 2) прибавить x всем вершинам поддерева v, узнать значение в вершине u
RootSum sub(N);
void addSubtree(int v, long long x) { sub.add(v, x); }
long long valueAt(int u) { return sub.get(u); }
//---- prepost
// Два массива: порядок входа (pre) и порядок выхода (post). Fenwick — из «fenwick»
const int N = 200000;
vector<int> g[N];  int pre[N], post[N], leftCnt[N], sz[N], cp, cq;
void dfs(int v, int p) {
    pre[v] = cp++;  leftCnt[v] = cq;             // leftCnt[v] — сколько вершин уже вышли к моменту входа в v
    sz[v] = 1;
    for (int u : g[v]) if (u != p) dfs(u, v), sz[v] += sz[u];
    post[v] = cq++;
}
Fenwick A(N), B(N);                              // A — по pre, B — по post
void add(int v, long long x) { A.add(pre[v], x); B.add(post[v], x); }
long long ancestorsSum(int v) {                  // предки v и сама v
    return A.pref(pre[v]) - B.pref(leftCnt[v] - 1);   // вошли, но ещё не вышли
}
long long subtreeSum(int v) {                    // поддерево — отрезок в порядке входа
    return A.pref(pre[v] + sz[v] - 1) - A.pref(pre[v] - 1);
}
//---- tarjan_lca
const int N = 200000;
vector<int> g[N];
vector<pair<int, int>> qs[N];                    // qs[v] — пары (другой конец, номер запроса)
int dsu[N], ans[N];  bool vis[N];
int find(int x) { return dsu[x] == x ? x : dsu[x] = find(dsu[x]); }

void dfs(int v, int p) {
    vis[v] = true;  dsu[v] = v;
    for (int u : g[v]) if (u != p) {
        dfs(u, v);
        dsu[find(u)] = v;                        // поддерево ребёнка «схлопывается» в v
    }
    for (auto [w, id] : qs[v])
        if (vis[w]) ans[id] = find(w);           // второй конец уже побывал: его компонента — это LCA
}
//---- offline_rmq
const int N = 200000;
int a[N], dsu[N], ans[N];
vector<pair<int, int>> byR[N];                   // byR[r] — пары (l, номер запроса)
int find(int x) { return dsu[x] == x ? x : dsu[x] = find(dsu[x]); }

void solve(int n) {
    vector<int> st;                              // стек минимумов: индексы, значения возрастают
    for (int r = 0; r < n; r++) {
        dsu[r] = r;
        while (!st.empty() && a[st.back()] >= a[r]) {
            dsu[st.back()] = r;                  // отрезок, где ответом был st.back(), теперь отдаёт r
            st.pop_back();
        }
        st.push_back(r);
        for (auto [l, id] : byR[r])
            ans[id] = a[find(l)];                // find(l) — ближайший к l элемент стека справа
    }
}
//---- linear_jump
const int N = 200000;
int par[N], jmp[N], h[N];                        // корень: par = jmp = он сам, h = 0
void addLeaf(int v, int p) {                     // p уже обработана
    par[v] = p;  h[v] = h[p] + 1;
    if (h[p] - h[jmp[p]] == h[jmp[p]] - h[jmp[jmp[p]]]) jmp[v] = jmp[jmp[p]];   // два равных прыжка → сливаем
    else jmp[v] = p;
}
int upTo(int v, int d) {                         // предок v на глубине d ≤ h[v]
    while (h[v] > d) {
        if (h[jmp[v]] >= d) v = jmp[v];          // прыжок не перелетает цель
        else v = par[v];
    }
    return v;
}
int lca(int u, int v) {
    if (h[u] < h[v]) swap(u, v);
    u = upTo(u, h[v]);
    while (u != v) {
        if (jmp[u] != jmp[v]) u = jmp[u], v = jmp[v];   // длины прыжков зависят только от высоты
        else u = par[u], v = par[v];
    }
    return u;
}
//---- ladder
const int N = 200000, LG = 18;
vector<int> g[N];
int up[LG][N], h[N], len[N], son[N], lg[N + 1];
int pathId[N], pos[N];
vector<vector<int>> lad;                         // «лестницы»: путь, продолженный вверх на свою длину

void dfs(int v, int p) {                         // вызов: dfs(0, 0)
    up[0][v] = p;  h[v] = (p == v ? 0 : h[p] + 1);
    for (int j = 1; j < LG; j++) up[j][v] = up[j - 1][up[j - 1][v]];
    len[v] = 1;  son[v] = -1;
    for (int u : g[v]) if (u != p) {
        dfs(u, v);
        if (len[u] + 1 > len[v]) len[v] = len[u] + 1, son[v] = u;   // сын на самом длинном пути вниз
    }
}
void buildLadders(int n) {
    for (int i = 2; i <= n; i++) lg[i] = lg[i / 2] + 1;
    for (int t = 0; t < n; t++) {
        if (t != 0 && son[up[0][t]] == t) continue;       // t — не начало длинного пути
        vector<int> path;
        for (int x = t; x != -1; x = son[x]) path.push_back(x);
        int L = path.size(), ext = min(L, h[t]);          // продлеваем вверх не более чем на L вершин
        vector<int> ladder(ext);
        int x = t;
        for (int i = ext - 1; i >= 0; i--) ladder[i] = x = up[0][x];
        ladder.insert(ladder.end(), path.begin(), path.end());
        for (int i = 0; i < L; i++) pathId[path[i]] = lad.size(), pos[path[i]] = ext + i;
        lad.push_back(ladder);
    }
}
int kth(int v, int k) {                          // предок на k выше, k ≤ h[v]; O(1)
    if (k == 0) return v;
    int j = lg[k];
    v = up[j][v];  k -= 1 << j;                  // один прыжок на старшую степень двойки
    return lad[pathId[v]][pos[v] - k];           // остаток k < 2^j гарантированно внутри лестницы
}
//---- rmq_pm1
// Массив a, соседние элементы которого отличаются ровно на 1. Возвращает позицию минимума на [l, r].
struct RmqPm1 {
    int n, B, nb;
    vector<int> a, mask, pre, suf, lg;
    vector<vector<int>> big;                     // разреженная таблица по блокам (хранит позиции минимумов)
    vector<vector<unsigned char>> tab;           // tab[mask][l*B + r] — позиция минимума внутри блока
    int better(int i, int j) { return a[j] < a[i] ? j : i; }
    RmqPm1(const vector<int>& v) : n(v.size()), a(v) {
        B = max(1, (int)(log2(max(n, 2)) / 2));  // размер блока ≈ (log n) / 2
        nb = (n + B - 1) / B;
        mask.assign(nb, 0);  pre.resize(n);  suf.resize(n);
        tab.assign(1 << (B - 1), {});
        for (int b = 0; b < nb; b++) {
            int s = b * B, e = min(n, s + B) - 1;
            for (int t = 0; t + 1 < B; t++)      // форма блока: растёт или убывает на каждом шаге
                if (s + t + 1 <= e && a[s + t + 1] > a[s + t]) mask[b] |= 1 << t;
            pre[s] = s;
            for (int i = s + 1; i <= e; i++) pre[i] = better(pre[i - 1], i);
            suf[e] = e;
            for (int i = e - 1; i >= s; i--) suf[i] = a[i] < a[suf[i + 1]] ? i : suf[i + 1];
            if (tab[mask[b]].empty()) {          // таблица для этой формы строится один раз
                vector<int> d(B);
                for (int t = 0; t + 1 < B; t++) d[t + 1] = d[t] + (mask[b] >> t & 1 ? 1 : -1);
                auto& T = tab[mask[b]];  T.assign(B * B, 0);
                for (int l = 0; l < B; l++) {
                    int best = l;
                    for (int r = l; r < B; r++) {
                        if (d[r] < d[best]) best = r;
                        T[l * B + r] = best;
                    }
                }
            }
        }
        lg.assign(nb + 1, 0);
        for (int i = 2; i <= nb; i++) lg[i] = lg[i / 2] + 1;
        big.assign(lg[nb] + 1, vector<int>(nb));
        for (int b = 0; b < nb; b++) big[0][b] = pre[min(n, b * B + B) - 1];
        for (int j = 1; j <= lg[nb]; j++)
            for (int b = 0; b + (1 << j) <= nb; b++)
                big[j][b] = better(big[j - 1][b], big[j - 1][b + (1 << (j - 1))]);
    }
    int query(int l, int r) {
        int bl = l / B, br = r / B;
        if (bl == br) return bl * B + tab[mask[bl]][(l - bl * B) * B + (r - bl * B)];   // внутри блока — по таблице
        int res = better(suf[l], pre[r]);        // суффикс первого блока и префикс последнего
        if (br - bl > 1) {                       // целые блоки между ними — разреженная таблица
            int j = lg[br - bl - 1];
            res = better(res, better(big[j][bl + 1], big[j][br - (1 << j)]));
        }
        return res;
    }
};
//---- cartesian
// Декартово дерево по минимуму (x — индекс, y — значение a[i]); строится за O(n) стеком.
vector<int> cartesian(const vector<int>& a, vector<int>& par) {
    int n = a.size();
    vector<int> L(n, -1), R(n, -1), st;
    par.assign(n, -1);
    for (int i = 0; i < n; i++) {
        int last = -1;
        while (!st.empty() && a[st.back()] > a[i]) last = st.back(), st.pop_back();
        if (last != -1) L[i] = last, par[last] = i;      // снятое с вершины стека становится левым поддеревом
        if (!st.empty()) R[st.back()] = i, par[i] = st.back();   // i — новый правый сын вершины стека
        st.push_back(i);
    }
    return L;                                    // минимум на [l, r] = LCA(l, r) в этом дереве
}
//---- virtual_sorted
// tin, h, anc, lca — из «binup». vs — вершины, УЖЕ отсортированные по tin, без повторов.
// Возвращает рёбра (родитель, ребёнок) сжатого дерева; корень — LCA всех вершин.
vector<pair<int, int>> virtualSorted(const vector<int>& vs, int& root) {
    root = vs[0];
    for (int v : vs) root = lca1(root, v);       // корень = LCA всех вершин
    vector<pair<int, int>> edges;
    vector<int> st = {root};                     // стек: путь от корня до последней вершины
    for (int c : vs) {
        if (c == root) continue;
        if (!anc(st.back(), c)) {                // c ушла вбок: ищем развилку
            int l = lca1(st.back(), c);
            while (st.size() >= 2 && h[st[st.size() - 2]] >= h[l]) {
                edges.push_back({st[st.size() - 2], st.back()});
                st.pop_back();
            }
            if (st.back() != l) {                // развилка — новая вершина: ставим её на место верхушки
                edges.push_back({l, st.back()});
                st.back() = l;
            }
        }
        st.push_back(c);
    }
    while (st.size() >= 2) {
        edges.push_back({st[st.size() - 2], st.back()});
        st.pop_back();
    }
    return edges;
}
//---- virtual_unsorted
// Способ 1: отсортировать, добавить LCA соседей, отсортировать ещё раз и пройти стеком.
vector<pair<int, int>> virtualTree(vector<int> vs, vector<int>& nodes) {
    auto byTin = [&](int a, int b) { return tin[a] < tin[b]; };
    sort(vs.begin(), vs.end(), byTin);
    vs.erase(unique(vs.begin(), vs.end()), vs.end());
    int k = vs.size();
    for (int i = 0; i + 1 < k; i++) vs.push_back(lca1(vs[i], vs[i + 1]));   // LCA соседних по tin
    sort(vs.begin(), vs.end(), byTin);
    vs.erase(unique(vs.begin(), vs.end()), vs.end());
    vector<pair<int, int>> edges;
    vector<int> st;
    for (int v : vs) {
        while (!st.empty() && !anc(st.back(), v)) st.pop_back();   // выходим из «рекурсии», пока не встретим предка
        if (!st.empty()) edges.push_back({st.back(), v});
        st.push_back(v);
    }
    nodes = vs;
    return edges;
}
//---- colors
// Дерево с цветами рёбер. Найти сумму по всем парам вершин (u, v) числа цветов,
// которые встречаются на пути u–v ровно один раз. Нужны tin, tout, anc из «binup».
vector<int> byColor[N];                          // byColor[c] — нижние концы рёбер цвета c
int comp[N], parS[N];
int subSize(int v) { return (tout[v] - tin[v] + 1) / 2; }

long long solveColors(int n, int colors) {
    long long total = 0;
    for (int c = 0; c < colors; c++) {
        vector<int> vs = byColor[c];
        if (vs.empty()) continue;
        sort(vs.begin(), vs.end(), [&](int a, int b) { return tin[a] < tin[b]; });
        comp[0] = n;                             // компонента корня после удаления рёбер цвета c
        vector<int> st = {0};
        for (int v : vs) {
            comp[v] = subSize(v);
            while (!anc(st.back(), v)) st.pop_back();
            parS[v] = st.back();                 // ближайшая выше вершина-верх другой компоненты
            comp[parS[v]] -= subSize(v);
            st.push_back(v);
        }
        for (int v : vs) total += 1LL * comp[v] * comp[parS[v]];   // ровно одно ребро цвета c на пути
    }
    return total;
}
//---- cut_vertices
// Выделены вершины sel[]. Какое наименьшее число НЕвыделенных вершин удалить,
// чтобы никакие две выделенные не были связаны? -1, если невозможно.
// virtualSorted — из «virtual_sorted».
bool sel[N];
int cutVertices(vector<int> vs) {
    sort(vs.begin(), vs.end(), [&](int a, int b) { return tin[a] < tin[b]; });
    int root;
    auto edges = virtualSorted(vs, root);
    vector<int> nodes = {root};
    map<int, int> vp;                            // родитель в сжатом дереве
    for (auto [p, c] : edges) nodes.push_back(c), vp[c] = p;
    sort(nodes.begin(), nodes.end(), [&](int a, int b) { return tin[a] > tin[b]; });   // дети раньше родителей
    map<int, int> kids;                          // сколько «открытых» детей (оттуда достижима выделенная)
    int ans = 0;
    for (int v : nodes) {
        bool open;
        if (sel[v]) open = true;                         // выделенная вершина «открыта» всегда
        else if (kids[v] >= 2) { ans++; open = false; }  // развилка: удаляем саму v
        else open = kids[v] == 1;
        if (!open || v == root) continue;
        int p = vp[v];
        if (sel[p]) {
            if (sel[v] && h[v] == h[p] + 1) return -1;   // две выделенные рядом — разрезать нечем
            ans++;                                       // удаляем v (если не выделена) или вершину между ними
        } else kids[p]++;
    }
    return ans;
}
