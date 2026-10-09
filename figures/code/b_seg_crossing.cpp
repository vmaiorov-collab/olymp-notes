// Для каждого отрезка [l_i, r_i] (все 2n концов различны) — число отрезков, пересекающих его, но не вложенных ни в него, ни его в них.
// Слагаемое A: отрезки j с l_j < l_i < r_j < r_i. Слагаемое B получим тем же кодом на зеркальных отрезках.
vector<int> crossLeft(const vector<pair<int,int>> &seg) {
    int n = seg.size(), M = 2 * n + 1;
    vector<int> evL(M, -1), evR(M, -1);                       // событие на координате: номер отрезка, у которого здесь левый/правый конец
    for (int i = 0; i < n; i++) { evL[seg[i].first] = i; evR[seg[i].second] = i; }
    vector<int> bit(M + 1, 0), a(n), atLeft(n);
    auto add = [&](int i) { for (i++; i <= M; i += i & -i) bit[i]++; };
    auto cnt = [&](int i) { int r = 0; for (; i > 0; i -= i & -i) r += bit[i]; return r; };   // закрытых с l < i
    for (int x = 1; x < M; x++) {
        if (evL[x] >= 0) atLeft[evL[x]] = cnt(seg[evL[x]].first);   // закрытые к моменту l_i с левым концом левее l_i
        if (evR[x] >= 0) {
            int i = evR[x];
            a[i] = cnt(seg[i].first) - atLeft[i];            // закрылись внутри (l_i, r_i), а начались левее l_i
            add(seg[i].first);                               // отрезок i закрыт: ставим единицу в его левый конец
        }
    }
    return a;
}
vector<int> crossing(vector<pair<int,int>> seg) {
    int n = seg.size(), M = 2 * n + 1;
    vector<int> A = crossLeft(seg);
    for (auto &s : seg) s = {M - s.second, M - s.first};     // зеркало: теперь «начавшиеся внутри и закончившиеся правее» стали типом A
    vector<int> B = crossLeft(seg);
    for (int i = 0; i < n; i++) A[i] += B[i];
    return A;
}
