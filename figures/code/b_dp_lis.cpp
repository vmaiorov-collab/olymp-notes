// НВП за O(n log n): d[len] — минимальное число, которым может заканчиваться возрастающая подпоследовательность длины len на просмотренном префиксе.
// d возрастает, поэтому новое x заменяет первое d[len] >= x (lower_bound). Для восстановления храним, на каком месте и кого заменили, и позицию предшественника.
vector<int> lisRestore(const vector<int> &a) {
    int n = a.size();
    vector<int> d, idx, prv(n, -1);                           // d[len-1] — значение, idx[len-1] — его позиция в a
    for (int i = 0; i < n; i++) {
        int len = lower_bound(d.begin(), d.end(), a[i]) - d.begin();     // строго возрастающая: ищем первое >= a[i]
        if (len == (int)d.size()) { d.push_back(a[i]); idx.push_back(i); }
        else { d[len] = a[i]; idx[len] = i; }
        prv[i] = len ? idx[len - 1] : -1;                      // a[i] продолжает цепочку длины len, заканчивающуюся на idx[len-1]
    }
    vector<int> res;
    for (int i = idx.back(); i >= 0; i = prv[i]) res.push_back(a[i]);
    reverse(res.begin(), res.end());
    return res;
}
