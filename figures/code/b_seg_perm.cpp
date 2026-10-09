// Восстановление перестановки по s[i] = сумма элементов слева от i, меньших p[i].  Идём с конца, Фенвик на «ещё не использованных» числах.
vector<int> restorePermutation(const vector<long long> &s) {
    int n = s.size(), LOG = 1; while ((1 << LOG) <= n) LOG++;
    vector<long long> bit(n + 1, 0);
    auto add = [&](int i, long long x) { for (; i <= n; i += i & -i) bit[i] += x; };
    for (int v = 1; v <= n; v++) add(v, v);                  // сначала все числа 1..n свободны (вес = само число)
    vector<int> p(n);
    for (int i = n - 1; i >= 0; i--) {
        // x — наименьшее свободное число, у которого сумма свободных чисел до него включительно больше s[i]  (спуск по Фенвику)
        int pos = 0; long long rest = s[i];
        for (int b = LOG; b >= 0; b--) {
            int np = pos + (1 << b);
            if (np <= n && bit[np] <= rest) { pos = np; rest -= bit[np]; }
        }
        p[i] = pos + 1;
        add(p[i], -p[i]);                                    // число использовано
    }
    return p;
}
