// Прибавление на отрезке и сумма на отрезке БЕЗ проталкивания: в вершине храним модификатор add[v]
struct AddSum {
    int n; vector<long long> sum, add;
    AddSum(int n) : n(n), sum(4 * n, 0), add(4 * n, 0) {}
    // sum[v] — настоящая сумма на отрезке вершины (с учётом add[v] и всех модификаторов ниже)
    void update(int v, int l, int r, int ql, int qr, long long x) {
        if (qr <= l || r <= ql) return;
        if (ql <= l && r <= qr) { add[v] += x; sum[v] += x * (r - l); return; }   // отрезок целиком внутри запроса
        int m = (l + r) / 2;
        update(2 * v, l, m, ql, qr, x); update(2 * v + 1, m, r, ql, qr, x);
        sum[v] = sum[2 * v] + sum[2 * v + 1] + add[v] * (r - l);                   // add[v] «лежит сверху» над детьми
    }
    long long get(int v, int l, int r, int ql, int qr) {
        if (qr <= l || r <= ql) return 0;
        if (ql <= l && r <= qr) return sum[v];
        int m = (l + r) / 2;
        long long inter = min(r, qr) - max(l, ql);          // сколько элементов запроса лежит под вершиной v
        return get(2 * v, l, m, ql, qr) + get(2 * v + 1, m, r, ql, qr) + add[v] * inter;
    }
};
