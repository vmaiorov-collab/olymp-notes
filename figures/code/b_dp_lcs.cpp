// Длина НОП двух массивов за O(nm) времени и O(min(n, m)) памяти: слой i зависит только от слоя i−1.
int lcsLength(const vector<int> &a, const vector<int> &b) {
    const vector<int> &x = a.size() >= b.size() ? a : b, &y = a.size() >= b.size() ? b : a;     // y — короткий массив
    int m = y.size();
    vector<int> oldDp(m + 1, 0), newDp(m + 1, 0);              // dp[j] — НОП префикса x длины i и префикса y длины j
    for (size_t i = 1; i <= x.size(); i++) {
        for (int j = 1; j <= m; j++)
            newDp[j] = (x[i - 1] == y[j - 1]) ? oldDp[j - 1] + 1 : max(oldDp[j], newDp[j - 1]);
        swap(oldDp, newDp);                                    // swap за O(1), копирование было бы за O(m)
    }
    return oldDp[m];
}
