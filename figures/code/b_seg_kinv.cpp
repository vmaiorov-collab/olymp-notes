// Число k-инверсий: цепочек i1 < ... < ik с a[i1] > a[i2] > ... > a[ik];  O(n k log n)
long long countKInversions(vector<int> a, int k) {
    int n = a.size();
    vector<int> s(a); sort(s.begin(), s.end()); s.erase(unique(s.begin(), s.end()), s.end());
    for (int &x : a) x = lower_bound(s.begin(), s.end(), x) - s.begin() + 1;   // значения 1..m
    int m = s.size();
    vector<vector<long long>> bit(k + 1, vector<long long>(m + 1, 0));         // bit[j] — Фенвик «цепочки длины j по последнему элементу»
    auto add = [&](int j, int i, long long x) { for (; i <= m; i += i & -i) bit[j][i] += x; };
    auto sum = [&](int j, int i) { long long r = 0; for (; i > 0; i -= i & -i) r += bit[j][i]; return r; };
    long long total = 0;
    for (int x : a) {
        for (int j = k; j >= 2; j--) {                       // от длинных цепочек к коротким, чтобы не использовать x дважды
            long long cnt = sum(j - 1, m) - sum(j - 1, x);   // цепочки длины j-1 с последним элементом > x
            if (j == k) total += cnt;                        // для последней длины достаточно просто суммы
            else add(j, x, cnt);
        }
        add(1, x, 1);                                        // цепочка из одного элемента
    }
    return k == 1 ? n : total;
}
